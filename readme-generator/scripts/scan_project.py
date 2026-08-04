#!/usr/bin/env python3
"""Scan a project directory and emit README-relevant facts as JSON.

Offline and deterministic: no network calls. This is the mechanical
"facts" half of the scan-first workflow. Judgement-based signals
(public-API extraction, example harvesting, project-type classification)
are left to the agent, which reads this output first.

Usage:
    python3 scan_project.py [path]

Requirements (see DEPENDENCIES.md):
- Python >= 3.11 (uses the stdlib ``tomllib``)
- ``tree`` >= 2.3.2 (hard requirement; used for the directory structure via
  ``tree -J``).
- ``licensee`` >= 10.0.0 (hard requirement; used for license detection via
  ``licensee detect --json``, with a manifest SPDX fallback).
- ``scc`` >= 3.7.0 (optional; used solely to line-count pre-existing READMEs via
  ``scc --by-file -f json``). When absent, that count degrades to 0 and the scan
  still runs.
If a *hard* required tool is missing or too old the scanner emits a JSON error
object and exits non-zero.

Design goals:
- never crash on a malformed/partial project; degrade to empty fields
- valid JSON on stdout, always
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

try:  # Python 3.11+
    import tomllib  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - depends on interpreter
    tomllib = None  # type: ignore


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MANIFESTS = [
    "package.json",
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
    "Cargo.toml",
    "go.mod",
    "Gemfile",
    "composer.json",
    "deno.json",
    "deno.jsonc",
    "build.gradle",
    "build.gradle.kts",
    "pom.xml",
]

# Lockfile -> package manager, in precedence order.
LOCKFILES = [
    ("pnpm-lock.yaml", "pnpm"),
    ("yarn.lock", "yarn"),
    ("package-lock.json", "npm"),
    ("bun.lockb", "bun"),
    ("bun.lock", "bun"),
    ("uv.lock", "uv"),
    ("poetry.lock", "poetry"),
    ("Pipfile.lock", "pipenv"),
    ("Cargo.lock", "cargo"),
    ("go.sum", "go"),
]

TASK_FILES = [
    "Makefile",
    "Taskfile.yml",
    "Taskfile.yaml",
    "justfile",
    "Justfile",
]

CONFIG_EXAMPLES = [
    ".env.example",
    ".env.local.example",
    ".env.sample",
    "config.example.json",
    "config.example.yaml",
    "config.example.yml",
]

DEPLOY_FILES = [
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    "vercel.json",
    "netlify.toml",
    "wrangler.toml",
    "fly.toml",
    "Procfile",
]

# Sibling docs the agent should read instead of re-deriving from source.
SIBLING_DOCS = [
    "ARCHITECTURE.md",
    "AGENTS.md",
    "CLAUDE.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
]

PRUNE_DIRS = {
    ".cache",
    ".git",
    ".hg",
    ".idea",
    ".next",
    ".nuxt",
    ".turbo",
    ".venv",
    ".vscode",
    ".yarn",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "target",
    "vendor",
    "venv",
}

MONOREPO_MIN_PACKAGES = 3
MAX_DEPTH = 3
TREE_DEPTH = 2
MIN_TREE_VERSION = (2, 3, 2)
MIN_LICENSEE_VERSION = (10, 0, 0)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def rel(path: Path, root: Path) -> str:
    """Return path relative to root as a POSIX string, or the raw POSIX path if unrelated."""
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def load_toml(path: Path) -> dict[str, Any]:
    """Load a TOML file, using tomllib when available with a tiny fallback."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    if tomllib is not None:
        try:
            return tomllib.loads(text)
        except Exception:
            return {}
    return _fallback_toml(text)


def _fallback_toml(text: str) -> dict[str, Any]:
    """Minimal TOML reader: top-level and [section] key = "value" pairs.

    Only good enough to pull name/description/version/license out of common
    manifests when tomllib is missing (pre-3.11). Not a full parser.
    """
    data: dict[str, Any] = {}
    section: dict[str, Any] = data
    kv = re.compile(r'^\s*([A-Za-z0-9_.-]+)\s*=\s*"([^"]*)"')
    header = re.compile(r"^\s*\[([^\]]+)\]\s*$")
    for line in text.splitlines():
        line = line.split("#", 1)[0]
        m = header.match(line)
        if m:
            section = {}
            data[m.group(1)] = section
            continue
        m = kv.match(line)
        if m:
            section[m.group(1)] = m.group(2)
    return data


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON file, returning {} on read/parse error or non-object top level."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def find_named(root: Path, names: list[str], max_depth: int = MAX_DEPTH) -> list[str]:
    """Return sorted relative paths of files matching names, up to max_depth.

    Matching is case-insensitive. Prunes generated/vendor directories and
    hidden directories (except ``.github``).
    """
    wanted = {name.lower() for name in names}
    hits: set[str] = set()
    for current, dirs, files in os.walk(root):
        current_path = Path(current)
        try:
            depth = len(current_path.relative_to(root).parts)
        except ValueError:
            continue
        dirs[:] = [
            d
            for d in dirs
            if d not in PRUNE_DIRS and not (d.startswith(".") and d != ".github")
        ]
        if depth >= max_depth:
            dirs[:] = []
        for filename in files:
            if filename.lower() in wanted:
                candidate = current_path / filename
                if len(candidate.relative_to(root).parts) <= max_depth:
                    hits.add(rel(candidate, root))
    return sorted(hits)


# ---------------------------------------------------------------------------
# Field extractors
# ---------------------------------------------------------------------------


def extract_metadata(root: Path) -> dict[str, str]:
    """Name / description / version from the primary manifest."""
    name = description = version = ""

    pkg = root / "package.json"
    pyproject = root / "pyproject.toml"
    cargo = root / "Cargo.toml"
    gomod = root / "go.mod"

    if pkg.exists():
        data = load_json(pkg)
        name = str(data.get("name", "") or "")
        description = str(data.get("description", "") or "")
        version = str(data.get("version", "") or "")
    elif pyproject.exists():
        data = load_toml(pyproject)
        project = (
            data.get("project", {}) if isinstance(data.get("project"), dict) else {}
        )
        poetry = (
            data.get("tool", {}).get("poetry", {})
            if isinstance(data.get("tool"), dict)
            else {}
        )
        src = project or poetry
        name = str(src.get("name", "") or "")
        description = str(src.get("description", "") or "")
        version = str(src.get("version", "") or "")
    elif cargo.exists():
        data = load_toml(cargo)
        pkgsec = (
            data.get("package", {}) if isinstance(data.get("package"), dict) else {}
        )
        name = str(pkgsec.get("name", "") or "")
        description = str(pkgsec.get("description", "") or "")
        version = str(pkgsec.get("version", "") or "")
    elif gomod.exists():
        try:
            for line in gomod.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("module "):
                    module = line[len("module ") :].strip()
                    module = re.sub(r"/v[0-9]+$", "", module)
                    name = module.rsplit("/", 1)[-1]
                    break
        except OSError:
            pass

    if not name:
        name = root.name

    return {"name": name, "description": description, "version": version}


def license_from_manifest(root: Path) -> str:
    """Return an SPDX license id declared in a package manifest, or "".

    Fallback for when ``licensee`` yields nothing. Reads the standard SPDX
    ``license`` field from ``package.json`` (npm), ``Cargo.toml`` (``[package]``),
    and ``pyproject.toml`` (PEP 621 ``[project].license``, either a bare SPDX
    expression string or the legacy ``{text = "..."}`` table). Returns "" when no
    manifest carries a usable value.
    """
    pkg = root / "package.json"
    if pkg.exists():
        value = load_json(pkg).get("license")
        if isinstance(value, str) and value.strip():
            return value.strip()

    cargo = root / "Cargo.toml"
    if cargo.exists():
        data = load_toml(cargo)
        section = (
            data.get("package", {}) if isinstance(data.get("package"), dict) else {}
        )
        value = section.get("license")
        if isinstance(value, str) and value.strip():
            return value.strip()

    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        data = load_toml(pyproject)
        project = (
            data.get("project", {}) if isinstance(data.get("project"), dict) else {}
        )
        value = project.get("license")
        if isinstance(value, str) and value.strip():
            return value.strip()
        if isinstance(value, dict):
            text = value.get("text")
            if isinstance(text, str) and text.strip():
                return text.strip()

    return ""


def detect_license(root: Path) -> str:
    """Return the SPDX license id, from ``licensee`` or a manifest fallback.

    First reads the first entry of the ``licenses`` list reported by
    ``licensee detect --json``. When that is unavailable (detection fails, no
    license found, or the top result is ``NOASSERTION``), falls back to the SPDX
    ``license`` field of a package manifest (see ``license_from_manifest``).
    Returns "" only when neither source yields a value.
    """
    try:
        out = subprocess.run(
            ["licensee", "detect", "--json", str(root)],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return license_from_manifest(root)

    try:
        data = json.loads(out.stdout)
    except json.JSONDecodeError:
        return license_from_manifest(root)

    licenses = data.get("licenses") if isinstance(data, dict) else None
    if not isinstance(licenses, list) or not licenses:
        return license_from_manifest(root)

    first = licenses[0]
    if not isinstance(first, dict):
        return license_from_manifest(root)

    spdx = first.get("spdx_id")
    if not isinstance(spdx, str) or spdx == "NOASSERTION":
        return license_from_manifest(root)
    return spdx


def detect_package_manager(root: Path) -> str:
    """Detect the package manager from lockfiles, the packageManager field, then manifests."""
    for lockfile, manager in LOCKFILES:
        if (root / lockfile).exists():
            return manager
    pkg = load_json(root / "package.json")
    manager = pkg.get("packageManager")
    if isinstance(manager, str) and manager:
        return manager.split("@", 1)[0]
    if (root / "package.json").exists():
        return "npm"
    if (root / "go.mod").exists():
        return "go"
    if (root / "requirements.txt").exists():
        return "pip"
    if (root / "build.gradle").exists() or (root / "build.gradle.kts").exists():
        return "gradle"
    if (root / "deno.json").exists() or (root / "deno.jsonc").exists():
        return "deno"
    return ""


def detect_git(root: Path) -> dict[str, str]:
    """Return git owner/repo parsed from the origin remote.

    Uses local ``git`` only; makes no network calls. Handles both SSH
    (``git@host:owner/repo.git``) and HTTPS remote URL forms.
    """
    info = {"owner": "", "repo": ""}
    if not (root / ".git").exists():
        try:
            inside = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "--is-inside-work-tree"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if inside.returncode != 0:
                return info
        except (OSError, subprocess.SubprocessError):
            return info

    def git(*args: str) -> str:
        """Run a git subcommand in root and return trimmed stdout, or "" on failure."""
        try:
            out = subprocess.run(
                ["git", "-C", str(root), *args],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return out.stdout.strip() if out.returncode == 0 else ""
        except (OSError, subprocess.SubprocessError):
            return ""

    remote = git("remote", "get-url", "origin")
    if remote:
        owner_repo = ""
        if remote.startswith("git@"):
            owner_repo = remote.split(":", 1)[-1]
        elif remote.startswith("http://") or remote.startswith("https://"):
            owner_repo = re.sub(r"https?://[^/]+/", "", remote)
        owner_repo = re.sub(r"\.git$", "", owner_repo)
        parts = owner_repo.split("/")
        if len(parts) >= 2:
            info["owner"] = parts[-2]
            info["repo"] = parts[-1]

    return info


def detect_latest_tag(root: Path) -> str:
    """Return the latest git tag reachable from HEAD, or "" if none/unavailable.

    Uses local ``git describe --tags --abbrev=0`` only; makes no network calls
    and degrades gracefully (empty string) when git or a tag is absent.
    """
    if not (root / ".git").exists():
        try:
            inside = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "--is-inside-work-tree"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if inside.returncode != 0:
                return ""
        except (OSError, subprocess.SubprocessError):
            return ""

    try:
        out = subprocess.run(
            ["git", "-C", str(root), "describe", "--tags", "--abbrev=0"],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return out.stdout.strip() if out.returncode == 0 else ""


def parse_version(
    text: str, pattern: str = r"(\d+)\.(\d+)\.(\d+)"
) -> tuple[int, ...] | None:
    """Parse the first ``X.Y.Z`` triple matching ``pattern`` into an int tuple.

    Pure and I/O-free so the comparison logic is testable without shelling out.
    ``pattern`` must expose three numeric capture groups. Returns None when no
    match is found.
    """
    match = re.search(pattern, text)
    if not match:
        return None
    return tuple(int(part) for part in match.groups())


def at_least(version: tuple[int, ...], minimum: tuple[int, ...]) -> bool:
    """Return True when ``version`` is greater than or equal to ``minimum``."""
    return version >= minimum


def check_tool(
    name: str,
    version_args: list[str],
    version_pattern: str,
    min_version: tuple[int, ...],
) -> str | None:
    """Return an error message if ``name`` is missing or older than ``min_version``.

    Shells out to ``name`` with ``version_args`` and parses its output with
    ``version_pattern`` (see ``parse_version``). Returns None when a suitable
    version is available. Every error string points to DEPENDENCIES.md.
    """
    min_str = ".".join(map(str, min_version))
    try:
        out = subprocess.run(
            [name, *version_args],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except FileNotFoundError:
        return (
            f"'{name}' is required but was not found on PATH. "
            f"Install {name} >= {min_str} (see DEPENDENCIES.md)."
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return f"failed to run '{name} {' '.join(version_args)}': {exc}"

    version = parse_version(out.stdout, version_pattern)
    if version is None:
        return f"could not parse {name} version from: {out.stdout.strip()!r}"

    if not at_least(version, min_version):
        return (
            f"{name} {'.'.join(map(str, version))} is too old; "
            f"require >= {min_str} (see DEPENDENCIES.md)."
        )
    return None


def check_tree() -> str | None:
    """Return an error message if ``tree`` is missing or too old, else None."""
    return check_tool("tree", ["--version"], r"v(\d+)\.(\d+)\.(\d+)", MIN_TREE_VERSION)


def check_licensee() -> str | None:
    """Return an error message if ``licensee`` is missing or too old, else None."""
    return check_tool(
        "licensee", ["version"], r"(\d+)\.(\d+)\.(\d+)", MIN_LICENSEE_VERSION
    )


def build_tree(root: Path) -> Any:
    """Return the directory structure as a nested object from ``tree -J``.

    Runs ``tree`` two levels deep, listing hidden entries but excluding the
    prune-list patterns and anything ignored by ``.gitignore``. Emits the
    project's own subtree (the ``contents`` of the ``.`` root node) so the
    result drops straight into downstream rendering. Returns [] on any failure.
    """
    ignore_pattern = "|".join(sorted(PRUNE_DIRS))
    try:
        out = subprocess.run(
            [
                "tree",
                "-J",
                "-L",
                str(TREE_DEPTH),
                "-a",
                "-F",
                "--dirsfirst",
                "--noreport",
                "--gitignore",
                "-I",
                ignore_pattern,
                ".",
            ],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=root,
        )
    except (OSError, subprocess.SubprocessError):
        return []

    try:
        parsed = json.loads(out.stdout)
    except json.JSONDecodeError:
        return []

    # tree -J returns a list; the first element is the '.' root directory node.
    if isinstance(parsed, list) and parsed and isinstance(parsed[0], dict):
        return parsed[0].get("contents", [])
    return []


def heading_summary(readme: Path) -> list[str]:
    """Return the Markdown heading texts (any level) from a README file."""
    try:
        lines = readme.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    headings = []
    for line in lines:
        if line.startswith("#"):
            stripped = line.lstrip("#").strip()
            if stripped:
                headings.append(stripped)
    return headings


def scc_code_lines(path: Path) -> int:
    """Return the code-line count (scc "Code", excludes blank/comment lines).

    Shells out to ``scc --by-file -f json``. ``scc`` is optional: this returns 0
    on any failure — including when ``scc`` is not installed and files that scc
    skips (e.g. ``.gitignore``d paths). A 0 therefore means "unavailable/skipped",
    not necessarily "empty file".
    """
    try:
        out = subprocess.run(
            ["scc", "--by-file", "-f", "json", str(path)],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return 0

    try:
        groups = json.loads(out.stdout)
    except json.JSONDecodeError:
        return 0

    if not isinstance(groups, list):
        return 0

    total = 0
    for group in groups:
        if not isinstance(group, dict):
            continue
        for file_entry in group.get("Files", []):
            if isinstance(file_entry, dict):
                total += int(file_entry.get("Code", 0) or 0)
    return total


def read_package_scripts(path: Path) -> dict[str, str]:
    """Return the sorted "scripts" map from a package.json, or {} if absent/invalid."""
    data = load_json(path)
    scripts = data.get("scripts", {})
    if not isinstance(scripts, dict):
        return {}
    return {str(k): str(v) for k, v in sorted(scripts.items())}


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------


def collect(root: Path) -> dict[str, Any]:
    """Scan root and assemble the full facts dict emitted as JSON.

    Gathers project metadata, license, git remote, package manager, manifests
    and scripts, monorepo/package layout, task/config/deploy files, CI setup,
    sibling docs, existing READMEs (path/line count/headings), and a directory
    tree.
    """
    root = root.resolve()

    manifests = find_named(root, MANIFESTS)
    package_jsons = [m for m in manifests if m.endswith("package.json")]
    sub_manifests = [m for m in manifests if "/" in m]
    is_monorepo = len(sub_manifests) >= MONOREPO_MIN_PACKAGES

    existing_readmes = find_named(root, ["README.md", "readme.md", "README.rst"])

    ci_provider = ""
    ci_workflows: list[str] = []
    wf_dir = root / ".github" / "workflows"
    if wf_dir.is_dir():
        ci_provider = "github-actions"
        ci_workflows = sorted(
            p.name for p in wf_dir.iterdir() if p.suffix in (".yml", ".yaml")
        )
    elif (root / ".circleci" / "config.yml").exists():
        ci_provider = "circleci"
    elif (root / ".gitlab-ci.yml").exists():
        ci_provider = "gitlab"
    elif (root / ".travis.yml").exists():
        ci_provider = "travis"
    elif (root / "Jenkinsfile").exists():
        ci_provider = "jenkins"

    metadata = extract_metadata(root)

    return {
        "root": str(root),
        "project_name": metadata["name"],
        "description": metadata["description"],
        "version": detect_latest_tag(root) or metadata["version"],
        "license": detect_license(root),
        "git": detect_git(root),
        "package_manager": detect_package_manager(root),
        "manifests": manifests,
        "package_scripts": {
            item: read_package_scripts(root / item) for item in package_jsons
        },
        "is_monorepo": is_monorepo,
        "packages": sorted({m.rsplit("/", 1)[0] for m in sub_manifests}),
        "task_files": find_named(root, TASK_FILES, max_depth=2),
        "config_examples": find_named(root, CONFIG_EXAMPLES),
        "deploy_files": find_named(root, DEPLOY_FILES),
        "ci": {"provider": ci_provider, "workflows": ci_workflows},
        "sibling_docs": find_named(root, SIBLING_DOCS, max_depth=2),
        "existing_readmes": [
            {
                "path": item,
                # 0 when scc is absent or the README is gitignored (both legitimate),
                # not only when the file is empty. See scc_code_lines / DEPENDENCIES.md.
                "line_count": scc_code_lines(root / item),
                "headings": heading_summary(root / item),
            }
            for item in existing_readmes
        ],
        "directory_structure": build_tree(root),
    }


def main() -> int:
    """Parse args, scan the target directory, and print the facts as JSON."""
    parser = argparse.ArgumentParser(
        description="Scan a project and emit README-relevant facts as JSON (offline)."
    )
    parser.add_argument("repo", nargs="?", default=".", help="Project path to scan")
    args = parser.parse_args()

    root = Path(args.repo)
    if not root.exists() or not root.is_dir():
        parser.error(f"path does not exist or is not a directory: {root}")

    dependency_error = check_tree() or check_licensee()
    if dependency_error is not None:
        print(
            json.dumps(
                {"error": dependency_error, "root": str(root.resolve())},
                sort_keys=True,
            )
        )
        return 1

    try:
        data = collect(root)
    except Exception as exc:  # never crash the workflow
        data = {"error": f"{type(exc).__name__}: {exc}", "root": str(root.resolve())}

    print(json.dumps(data, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
