<!-- prettier-ignore -->
<div align="center">

# skills

First-party agent skills for OpenCode and Claude Code — small, focused
instruction packages that teach your agent how to do one thing well.

[![License](docs/license_badge.svg)](LICENSE)

[Overview](#overview) • [Getting started](#getting-started) • [Development](#development)

</div>

## Overview

A skill is a directory containing a `SKILL.md` file: YAML frontmatter with a
name and description, followed by instructions the agent loads when a task
matches. Any top-level directory here that holds a `SKILL.md` is discovered
automatically — no registration needed — and validated with
[skills-ref](https://pypi.org/project/skills-ref/).

## Available skills

| Skill                                   | What it does                                                                         |
| --------------------------------------- | ------------------------------------------------------------------------------------ |
| [`readme-creator`](readme-creator/)     | Creates, rewrites, or improves a project's `README.md` by analyzing the repository   |
| [`review-abilities`](review-abilities/) | Audits eight cross-cutting code qualities into a ranked `TODO.ability.md`            |
| [`skill-creator`](skill-creator/)       | Creates, edits, and improves agent skills — frontmatter, body, and bundled resources |

## Getting started

Copy a skill directory into your agent's skills directory:

```bash
# global, for OpenCode
cp -r review-abilities ~/.config/opencode/skills/

# or project-local
mkdir -p .agents/skills
cp -r review-abilities .agents/skills/
```

Alternatively, unzip a packaged skill into the same location:

```bash
make build
unzip build/review-abilities.skill -d ~/.config/opencode/skills/review-abilities/
```

## Development

This is a [uv](https://docs.astral.sh/uv/)-managed Python project that pins the
validation tooling; there is no application code.

```bash
make check       # validate every skill with skills-ref
make build       # zip each skill into build/<skill>.skill
make clean       # remove build/
make create-dev  # set up pre-commit hooks and uv sync
```

## Notes

- `make check` calls the `skills-ref` binary from your PATH — install it
  globally (e.g. `uv tool install skills-ref`), not just in the project venv.
- `make build` packages the **last commit** (`git archive` with `REF=HEAD`):
  uncommitted working-tree changes are not included. Commit first, or pass
  `make build REF=<branch-or-sha>`.
- Adding a skill needs no Makefile edit: create a top-level directory with a
  `SKILL.md` (name + description frontmatter) and it is picked up by
  `make check` and `make build`.
- Formatting is enforced by pre-commit on commit: prettier for
  markdown/JSON/YAML (4-space indent, 80-column, LF) and ruff for Python.
  Run it yourself with `pre-commit run --all-files`.
