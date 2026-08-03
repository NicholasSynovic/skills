<!--
  SKILL.md — work in progress, built section by section from README.features.md.
  Frontmatter (name / description / allowed-tools) is intentionally deferred.
  Sections present so far: 1 (scanning).
-->

## Step 1 — Scan the project

Always start here. Learn about the project from its files before asking the user
anything or writing a single line. The scan has two halves: **facts** gathered
mechanically by a bundled script, and **judgement** gathered by you afterward.

### 1a. Gather facts (run the scanner)

Run the bundled scanner and read its JSON output. It is offline and
deterministic — no network calls — and never crashes on a partial project.

```bash
python3 scripts/scan_project.py <project-dir>
```

The output is the source of truth for mechanical facts. Fields:

| Field | Meaning | Feeds |
| --- | --- | --- |
| `project_name`, `description`, `version` | From the primary manifest (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`) | Title, intro, version badge |
| `license` | Detected from `LICENSE*` text or manifest | License section + badge |
| `git.owner`, `git.repo`, `git.default_branch` | Parsed from `origin` remote (SSH + HTTPS) | Badge URLs, clone command, links |
| `package_manager` | Lockfile precedence, then `packageManager` field | Install/run commands |
| `manifests`, `package_scripts` | All manifests + npm scripts | Install / build / test / run commands |
| `is_monorepo`, `packages` | True when ≥3 sub-manifests; the package dirs | Component table, per-package scoping |
| `task_files` | Makefile / Taskfile / justfile | Task/command discovery |
| `config_examples` | `.env.example` etc. | Environment-variable section |
| `deploy_files` | Dockerfile / compose / vercel / etc. | Deployment section |
| `ci` | Provider + workflow filenames | CI badge, workflow filename |
| `sibling_docs` | ARCHITECTURE / AGENTS / CLAUDE / CONTRIBUTING / CHANGELOG / etc. | Read these instead of re-deriving |
| `existing_readmes` | Path, line count, headings of any current README | Update / audit modes |
| `directory_structure` | 2-level, folder-first tree as nested JSON (from `tree -J`, generated dirs and `.gitignore`d paths pruned) | Project-structure section (render to ASCII art) |

Do not re-derive by hand anything the scanner already reports.

### 1b. Gather judgement (you do this, after reading the facts)

The scanner deliberately stops at facts. These signals need reasoning, so gather
them yourself using `Read`, `Glob`, and `Grep`, guided by the scan output:

- **Public API / signatures.** Start from manifest entry points (`main`,
  `module`, `exports`, `bin`), follow re-exports, and capture the public
  functions/classes with their parameter and return types. (Pattern:
  `references/skills/accelint-readme-writer/references/codebase-analysis.md`.)
- **Real usage examples.** Pull examples from tests, `@example`/docstring
  blocks, and any `examples/` directory. **Never fabricate examples** — if none
  exist, say so or omit the section.
  (`references/skills/accelint-readme-writer/references/codebase-analysis.md`.)
- **Project type.** Classify as one of: CLI/tool, library/SDK, application,
  framework, monorepo, collection, or personal — using signals (a `bin` field
  and CLI parsing → CLI; exported API + no entry app → library; etc.). This
  drives section and voice choices in the next step.
  (`references/skills/github-readme/SKILL.md`,
  `references/skills/readme-creator/SKILL.md`.)
- **Read the sibling docs** the scanner listed (`sibling_docs`) rather than
  reconstructing architecture from source.
  (`references/skills/accelint-readme-writer/SKILL.md`,
  `references/skills/readme-blueprint-generator/SKILL.md`.)
- **Rank evidence** when sources disagree: manifest scripts and declared config
  outrank a lockfile, which outranks a version-manager file, which outranks a
  guess. Prefer the strongest evidence and note assumptions.
  (`references/skills/repository-readme-writer/references/repository-audit.md`.)

### Guardrails

- **Read code before asking the user.** Only ask about things the scan and code
  cannot answer. (`references/skills/readme/SKILL.md`.)
- **No fabrication.** If a fact is missing (empty scanner field, no examples, no
  license), skip the dependent section rather than invent content.
- **Offline.** The scanner makes no network requests; keep it that way. Fetch
  anything external only on explicit need, and never for private repos.
