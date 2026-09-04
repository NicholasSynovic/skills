# AGENTS.md

## What this repo is

First-party OpenCode/Claude skills. Every top-level directory containing a
`SKILL.md` is a skill (auto-discovered by the Makefile — no Makefile edit needed
when adding one). No application, test suite, or CI exists; the root `README.md`
is an empty placeholder.

## Build and verify

- `make build` zips each skill into `build/<skill>.skill`. It uses `git archive`
  with `REF ?= HEAD`, so **uncommitted working-tree changes are NOT packaged** —
  commit first, or override with `make build REF=<branch-or-sha>`.
- `make check` currently fails: it invokes `scripts/check_skills.py`, which does
  not exist yet.
- The only verification is pre-commit (set up with `make create-dev`; pins
  Python 3.14). Run `pre-commit run --all-files` before committing.

## Formatting (pre-commit enforces on commit)

- prettier (system binary): markdown/JSON/YAML/JS — 4-space indent, print width
  80, LF line endings, es5 trailing commas.
- JSON: pretty-format-json rewrites to 4-space indent; keys are NOT sorted.
- ruff (`ruff-check --fix` + `ruff-format`) for any Python files.
- `.editorconfig` sets `insert_final_newline = false`, but the pre-commit
  `end-of-file-fixer` enforces a trailing newline — the hook wins.
