# AGENTS.md

## What this repo is

First-party OpenCode/Claude skills (AGPL-3.0). Every top-level directory
containing a `SKILL.md` is a skill — auto-discovered by the Makefile and
validated with `skills-ref`; adding one needs no Makefile edit. No application,
test suite, or CI exists. `.agents/skills/` holds symlinks to all three skills — editing any of them
edits the live installed skill (and vice versa).

## Build and verify

- Python tooling is uv-managed: `uv sync` (requires-python >=3.12, pinned to
  3.14 in `.python-version`). Dependencies: `skills-ref` (skill validation)
  and `pybadges` (README license badges).
- `pybadges` is pinned to a git fork (NicholasSynovic/pybadges, via
  `tool.uv.sources`) because upstream imports the removed `imghdr` stdlib
  module and crashes on Python >=3.13 — the fork uses `filetype` instead.
  Don't swap it for the PyPI release. Run its CLI as `uv run pybadges` (it
  lives in `.venv/bin`, not on PATH).
- `make check` runs `skills-ref validate` on each skill. It calls the bare
  `skills-ref` binary, which must be on PATH (e.g. `uv tool install
skills-ref`) — a project-venv install is not enough.
- `make build` zips each skill into `build/<skill>.skill`. It uses `git archive`
  with `REF ?= HEAD`, so **uncommitted working-tree changes are NOT packaged** —
  commit first, or override with `make build REF=<branch-or-sha>`.
- One-shot setup: `make create-dev` (pre-commit install + autoupdate +
  `uv sync`). Primary verification is `make check`; pre-commit also runs on
  commit, or invoke it directly with `pre-commit run --all-files`.

## Formatting (pre-commit enforces on commit)

- prettier (system binary): markdown/JSON/YAML/JS — 4-space indent, print width
  80, LF line endings, es5 trailing commas.
- JSON: pretty-format-json rewrites to 4-space indent; keys are NOT sorted.
- ruff (`ruff-check --fix` + `ruff-format`) for any Python files.
- `.editorconfig` sets `insert_final_newline = false`, but the pre-commit
  `end-of-file-fixer` enforces a trailing newline — the hook wins.
