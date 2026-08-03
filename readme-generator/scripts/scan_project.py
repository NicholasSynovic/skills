#!/usr/bin/env python3
"""Scan a project directory and emit README-relevant facts as JSON.

Offline and deterministic: no network calls. This is the mechanical
"facts" half of the scan-first workflow. Judgement-based signals
(public-API extraction, example harvesting, project-type classification)
are left to the agent, which reads this output first.

Usage:
    python3 scan_project.py [path] [--pretty]

Requirements (see DEPENDENCIES.md):
- Python >= 3.11 (uses the stdlib ``tomllib``)
- ``tree`` >= 2.3.2 (hard requirement; used for the directory structure via
  ``tree -J``).
- ``scc`` >= 3.7.0 (hard requirement; used for code-line counting via
  ``scc --by-file -f json``).
If a required tool is missing or too old the scanner emits a JSON error object
and exits non-zero.

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

LICENSE_MARKERS = [
    ("Apache License", "Apache-2.0"),
    ("Apache-2.0", "Apache-2.0"),
    ("MIT License", "MIT"),
    ("Permission is hereby granted, free of charge", "MIT"),
    ("GNU GENERAL PUBLIC LICENSE", "GPL"),
    ("GNU AFFERO", "AGPL"),
    ("GNU LESSER", "LGPL"),
    ("BSD 3-Clause", "BSD-3-Clause"),
    ("BSD 2-Clause", "BSD-2-Clause"),
    ("Redistribution and use in source and binary forms", "BSD"),
    ("Mozilla Public License", "MPL-2.0"),
    ("The Unlicense", "Unlicense"),
    ("ISC License", "ISC"),
]

MONOREPO_MIN_PACKAGES = 3
MAX_DEPTH = 3
TREE_DEPTH = 2
MIN_TREE_VERSION = (2, 3, 2)
MIN_SCC_VERSION = (3, 7, 0)


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
        project = data.get("project", {}) if isinstance(data.get("project"), dict) else {}
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
        pkgsec = data.get("package", {}) if isinstance(data.get("package"), dict) else {}
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


def detect_license(root: Path) -> str:
    """Detect the SPDX license id from LICENSE* text, falling back to package.json."""
    for fname in ("LICENSE", "LICENSE.md", "LICENSE.txt", "LICENCE", "COPYING"):
        f = root / fname
        if f.exists():
            try:
                head = f.read_text(encoding="utf-8", errors="ignore")[:2000]
            except OSError:
                return f"Found ({fname})"
            for marker, spdx in LICENSE_MARKERS:
                if marker.lower() in head.lower():
                    return spdx
            return f"Found ({fname})"
    # Manifest-declared license as a fallback.
    pkg = load_json(root / "package.json")
    lic = pkg.get("license")
    if isinstance(lic, str) and lic:
        return lic
    return ""


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
    """Return git owner/repo/default_branch parsed from the origin remote.

    Uses local ``git`` only; makes no network calls. Handles both SSH
    (``git@host:owner/repo.git``) and HTTPS remote URL forms.
    """
    info = {"owner": "", "repo": "", "default_branch": ""}
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

    branch = git("symbolic-ref", "--short", "HEAD")
    if branch:
        info["default_branch"] = branch
    return info


def check_tree() -> str | None:
    """Return an error message if ``tree`` is missing or older than the minimum.

    Returns None when a suitable ``tree`` (>= MIN_TREE_VERSION) is available.
    """
    try:
        out = subprocess.run(
            ["tree", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except FileNotFoundError:
        return (
            "'tree' is required but was not found on PATH. "
            f"Install tree >= {'.'.join(map(str, MIN_TREE_VERSION))} (see DEPENDENCIES.md)."
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return f"failed to run 'tree --version': {exc}"

    match = re.search(r"v(\d+)\.(\d+)\.(\d+)", out.stdout)
    if not match:
        return f"could not parse tree version from: {out.stdout.strip()!r}"

    version = tuple(int(part) for part in match.groups())
    if version < MIN_TREE_VERSION:
        return (
            f"tree {'.'.join(map(str, version))} is too old; "
            f"require >= {'.'.join(map(str, MIN_TREE_VERSION))} (see DEPENDENCIES.md)."
        )
    return None


def check_scc() -> str | None:
    """Return an error message if ``scc`` is missing or older than the minimum.

    Returns None when a suitable ``scc`` (>= MIN_SCC_VERSION) is available.
    """
    try:
        out = subprocess.run(
            ["scc", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except FileNotFoundError:
        return (
            "'scc' is required but was not found on PATH. "
            f"Install scc >= {'.'.join(map(str, MIN_SCC_VERSION))} (see DEPENDENCIES.md)."
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return f"failed to run 'scc --version': {exc}"

    match = re.search(r"version\s+(\d+)\.(\d+)\.(\d+)", out.stdout)
    if not match:
        return f"could not parse scc version from: {out.stdout.strip()!r}"

    version = tuple(int(part) for part in match.groups())
    if version < MIN_SCC_VERSION:
        return (
            f"scc {'.'.join(map(str, version))} is too old; "
            f"require >= {'.'.join(map(str, MIN_SCC_VERSION))} (see DEPENDENCIES.md)."
        )
    return None


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


def line_count(path: Path) -> int:
    """Return the code-line count (scc "Code", excludes blank/comment lines).

    Uses ``scc --by-file -f json``. Returns 0 on any failure, including files
    that scc skips (e.g. ``.gitignore``d paths).
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
        "version": metadata["version"],
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
                "line_count": line_count(root / item),
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
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    args = parser.parse_args()

    root = Path(args.repo)
    if not root.exists() or not root.is_dir():
        parser.error(f"path does not exist or is not a directory: {root}")

    indent = 2 if args.pretty else None

    dependency_error = check_tree() or check_scc()
    if dependency_error is not None:
        print(
            json.dumps(
                {"error": dependency_error, "root": str(root.resolve())},
                indent=indent,
                sort_keys=True,
            )
        )
        return 1

    try:
        data = collect(root)
    except Exception as exc:  # never crash the workflow
        data = {"error": f"{type(exc).__name__}: {exc}", "root": str(root.resolve())}

    print(json.dumps(data, indent=indent, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
