<!--
  SKILL.md — work in progress, built section by section from README.features.md.
  Frontmatter (name / description / allowed-tools) is intentionally deferred.
  Sections present so far: 1 (scanning), 2 (type awareness & section selection).
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
- **Project type.** Classified in Step 2 from scanner signals, not here. If a
  read of the code gives you a provisional type, note it — but the decisive
  rules and the section/voice dispatch it drives live in Step 2.
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

## Step 2 — Classify the project & select sections

The scanner tells you *what is there*; this step decides *what the README should
contain*. Turn the facts (Step 1a) and your reading of the code (Step 1b) into
exactly one **project type**, then dispatch a **section set** and a **voice
profile**. Do this before writing any prose.

### 2a. Detect the project type

Classify into exactly one of these seven types: **CLI/tool, library/SDK,
application, framework, monorepo, collection, personal.** Detect from evidence —
mostly fields the scanner already reported — not from what the user says.

**First matching row wins**, top to bottom (most specific first):

| Decisive signal (from the scan) | Type |
| --- | --- |
| `is_monorepo` is true (≥3 sub-manifests / `packages` populated) | monorepo |
| A `skills/` dir of `SKILL.md` files, or a `templates/`/`actions/` dir of many like files | collection |
| Manifest declares a `bin` (npm), `[project.scripts]` (pyproject), `[[bin]]` (Cargo), or `go.mod` + root `main.go`; and/or a CLI parser dep (commander/yargs/clap/argparse) | CLI/tool |
| Plugin/middleware architecture with a documented config/extension API (framework config, `register`/`use` extension points) | framework |
| Web/app framework config with no publish (`next.config.*`, `nuxt.config.*`, `vite.config.*`, `app/`/`pages/` + framework config), or `"private": true` app | application |
| Manifest sets `main`/`exports`/`module` (or `[lib]` / library `pyproject`) and has no `bin` | library/SDK |
| Single-owner project with no registry publish and a personal framing (dotfiles, hobby repo, first-person intent) | personal |

Rules:

- **Detect before asking.** Read code first; only ask the user what the code
  cannot reveal (the "why", the audience, forced-in/out sections).
- **Dual roles.** If two types fit (a CLI that also exports an API; a framework
  published as a library), pick **how most users consume it** and fold the
  secondary role into one extra section rather than switching type.
- **Wrong-type smell test.** A library README with a `git clone` getting-started,
  or an app README carrying registry/version badges, means the type was guessed
  wrong — reclassify.

(Signals distilled from
`references/skills/github-readme/REFERENCE.md` (lines 362-385) and
`references/skills/readme-creator/SKILL.md` (lines 34-52, 110).)

### 2b. Select sections (type → section matrix)

Include every **Required** section; add **Recommended** when the scan supports it;
add **Optional** only when it earns its place. Skip any selected section whose
data the scan proves absent (note the assumption) — never fabricate to fill it.
These are section *names*; the skeletons come later (templates step).

Legend: **R** required · **r** recommended · **o** optional · **—** omit.

| Section | CLI/tool | library/SDK | application | framework | monorepo | collection | personal |
| --- | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
| Title + one-liner | R | R | R | R | R | R | R |
| Badges | R | R | — | R | — | r | — |
| Features / highlights | r | r | R | r | — | — | o |
| Install | R | R | r | R | r | r | R |
| Usage / Quick start | R | R | R | R | R | R | R |
| API Reference / Options | R | R | — | R | — | — | — |
| Configuration | r | r | R | R | o | — | — |
| Environment variables | — | — | R | — | — | — | — |
| What's Here (catalog / index) | — | — | — | — | — | R | — |
| How to Extend | — | — | — | R | — | o | — |
| Packages / Components table | — | — | — | — | R | — | — |
| Architecture | — | — | r | r | o | — | — |
| Requirements | R | R | o | R | r | o | — |
| Why I built this | — | — | — | — | — | — | R |
| Who this is for | r | r | — | r | — | r | — |
| Contributing | r | R | r | r | r | r | — |
| License | R | R | R | R | R | R | o |

Notes:

- **No badges (and no version column) for personal or monorepo** projects here —
  they have no registry entry behind them, so badges render broken or stale.
  Collections get badges only if the collection itself is published.
- The **Packages / Components table** appears only when `is_monorepo` is true; it
  is driven by the scanner's `packages` list.
- **What's Here** (collection) and **How to Extend** (framework/collection) are
  the catalog/extension-point sections folded in from the config/XDG family.

(Reconciled from
`references/skills/github-readme/SKILL.md` (lines 207-223),
`references/skills/readme-creator/SKILL.md` (lines 61-80, 111), and
`references/skills/crafting-effective-readmes/section-checklist.md`.)

### 2c. Voice profile per type

The type also sets tone. Lead the intro in the matching voice:

| Type | Default tone | Example opening |
| --- | --- | --- |
| CLI/tool | Direct, practical | "Fast Markdown linting for CI pipelines." |
| library/SDK | Technical, precise | "A typed HTTP client for the Stripe API." |
| application | Product-focused, clear | "Real-time project dashboard with team analytics." |
| framework | Precise, extensibility-forward | "A plugin-driven static-site engine." |
| monorepo | Organized, scannable | "Six packages that power the Acme design system." |
| collection | Organized, scannable | "50+ reusable GitHub Actions workflows." |
| personal | First-person, opinionated | "I needed a better way to track reading habits." |

- **Always:** direct, specific, opinionated; short paragraphs (≤4 sentences).
- **Never:** hedge language, marketing fluff, passive voice in problem
  statements, emojis in prose.
- **Default professional.** First person is opt-in — natural for `personal`,
  otherwise only when the user asks. The full humanize / lint pass is a later
  step; this is just the tone to write in.

(Voice matrix from
`references/skills/github-readme/SKILL.md` (lines 227-238).)

### Guardrails

- **Classify before writing.** A mismatched type sends readers down a dead path
  (see the wrong-type smell test in 2a).
- **Required ≠ invent.** Include every Required section, but if the scan proves
  its data does not exist, omit it and record the assumption rather than
  fabricate.
- **One type, one dispatch.** Resolve dual roles in 2a; do not blend two full
  section sets.
