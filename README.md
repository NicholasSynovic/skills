# skills

First-party agent skills for OpenCode and Claude Code — small, focused
instruction packages that teach your agent how to do one thing well.

## What is a skill?

A skill is a directory containing a `SKILL.md` file: YAML frontmatter with a
name and description, followed by instructions the agent loads when a task
matches. Any top-level directory here that holds a `SKILL.md` is discovered
automatically — no registration needed — and validated with
[skills-ref](https://pypi.org/project/skills-ref/).

## Available skills

| Skill                                   | What it does                                                                       |
| --------------------------------------- | ---------------------------------------------------------------------------------- |
| [`readme-creator`](readme-creator/)     | Creates, rewrites, or improves a project's `README.md` by analyzing the repository |
| [`review-abilities`](review-abilities/) | Audits eight cross-cutting code qualities into a ranked `TODO.ability.md`          |

## Installation

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
uv sync          # install dependencies (Python >= 3.12, pinned to 3.14)
make check       # validate every skill with skills-ref
make build       # zip each skill into build/<skill>.skill
make clean       # remove build/
make create-dev  # install pre-commit hooks
```

Notes:

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

## License

[AGPL-3.0](LICENSE)
