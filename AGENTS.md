# AGENTS.md

## What this repo is

A workspace holding **first-party OpenCode/Claude skills under construction** plus
a **vendored corpus** of third-party README-generator skills used as design input.
There is no application, server, or package build.

- `readme-generator/` — the main first-party skill, built section by section from
  `readme-generator/CLUSTERED_FEATURES.md` (a capability-cluster feature inventory
  of the vendored skills). See `readme-generator/SKILL.md`.
- `review-abilites/` — a second first-party skill (code-quality review →
  `TODO.ability.md`). Independent of `readme-generator/`.
- `readme-generator/references/vendor/<skill>/` — 34 vendored third-party skills
  (design references, not part of the shipped skill).
- **`FutureReadmeSkills.md` (repo root) is a STALE duplicate** of
  `CLUSTERED_FEATURES.md` — same doc, older badge cluster with unresolved pybadges
  TODOs. `CLUSTERED_FEATURES.md` is the current inventory; edit that one, not the
  root copy.

## First-party vs vendored (do not confuse them)

- **Edit freely:** `readme-generator/SKILL.md`, `scripts/`, `templates/`,
  `references/*.md` (e.g. `section-library.md`), `DEPENDENCIES.md`,
  `CLUSTERED_FEATURES.md`; all of `review-abilites/`.
- **Do NOT hand-edit** `readme-generator/references/vendor/**` — vendored upstream
  content, validated against `computedHash` in the `skills` lockfile. Editing
  diverges it from its hash. Add/update via the `skills` CLI
  (`npx skills add <repo> --skill <name>`), not by copying files.
- The `SKILL.md` / `AGENTS.md` / `README.md` files _inside_ `references/vendor/**`
  belong to vendored skills, not this repo.
- Cite vendored sources as `references/vendor/<skill>/file (lines X-Y)`. The path
  is `references/vendor/`, **not** `references/skills/` (a stale path that keeps
  reappearing — grep for it before committing).
- `readme-generator/references.txt` lists 49 `npx skills add` commands but only 34
  resolved; trust the lockfile + `references/vendor/` as the installed set, not
  `references.txt`. No `skills-lock.json` is checked in at the moment.

## Toolchain — pre-commit is the source of truth

There is no Makefile/pyproject. All lint/format/checks run via
`.pre-commit-config.yaml`. Run before committing:

```bash
pre-commit run --all-files      # or: pre-commit run --files <path>
```

Non-obvious gotchas baked into the hooks:

- **`no-commit-to-branch` blocks commits to `main`.** Work on a branch and open a
  PR; a direct `git commit` on `main` fails the hook.
- **`pretty-format-json --autofix`** rewrites every JSON file to 4-space indent,
  `--no-sort-keys`. Emit JSON in that shape or the hook will reflow it.
- **ruff** (`ruff-check --fix` + `ruff-format`) and **bandit** run on Python;
  the only Python is `readme-generator/scripts/scan_project.py`. Keep it clean.
- **prettier** (system-installed) formats md/json/yaml/etc. at
  `--tab-width 4 --print-width 80 --trailing-comma es5`, LF.
- `.editorconfig` sets `insert_final_newline = false`, but the pre-commit
  `end-of-file-fixer` hook enforces a trailing newline — the hook wins on commit.
- pre-commit pins `python3.14` (local `python3` is 3.14.x). `scan_project.py`
  requires **Python ≥ 3.11** (stdlib `tomllib`) and runs fine on 3.14, but the
  Step 4 `pybadges` badge step does NOT — see below.

## scan_project.py

- Run: `python3 readme-generator/scripts/scan_project.py <project-dir>` → JSON on
  stdout. Offline, deterministic, never crashes on partial projects.
- **Hard external deps** (see `readme-generator/DEPENDENCIES.md`): `tree` ≥ 2.3.2,
  `scc` ≥ 3.7.0, `licensee` ≥ 10.0.0. Missing/old → JSON `{"error": ...}` + exit 1.
  `git` is optional (degrades gracefully).
- Verify edits with `python3 -m py_compile readme-generator/scripts/scan_project.py`
  and a real run; there is no test suite.
- Badge generation (SKILL.md Step 4) uses `pybadges` ≥ 3.0.1 (static local SVGs,
  not shields.io URLs). On **Python 3.13+** `pybadges` crashes on any invocation
  because it imports the removed stdlib `imghdr` — install `standard-imghdr` or
  run it under Python 3.11/3.12.

## Building the README skill

- `CLUSTERED_FEATURES.md` is the section-by-section build source; `SKILL.md`'s
  header comment tracks which sections (steps) are done. Sections 1–5 exist (scanning,
  type awareness, templates, badges, visuals). **Scope is generation only** —
  the audit/update mode (a "Step 6 updater" referenced in `CLUSTERED_FEATURES.md`)
  is not implemented in `SKILL.md`.
- Content model: **Step 1** scans (facts via script + agent judgement), **Step 2**
  classifies project type (7 types) and selects sections via a matrix, **Step 3**
  fills per-type skeletons in `templates/` (literal `{{token}}` fill-ins) filtered
  by depth tier. `templates/companion/` holds CHANGELOG/CONTRIBUTING skeletons.
  Keep these consistent when editing one of them.
- Anti-fabrication is a hard rule throughout: never invent examples/values; omit a
  section when scan data is absent.
