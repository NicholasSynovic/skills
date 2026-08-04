---
name: readme-generator
description: >-
    Generate a high-quality README.md for a software project by scanning the
    codebase for facts (manifests, license, git remote, package manager,
    directory tree), classifying the project into one of seven types
    (CLI/tool, library/SDK, application, framework, monorepo, collection,
    personal), and filling a type-specific, depth-tiered template with real
    scanned values — plus static badges and architecture/file-tree diagrams.
    Use this whenever the user asks to write, create, generate, draft, or
    scaffold a README or README.md; wants project documentation for a repo,
    package, CLI, library, or monorepo; or asks "document this project" — even
    if they don't say the word "README" explicitly. Anti-fabrication is a hard
    rule: it reads code before asking and omits any section the scan cannot
    support.
---

<!--
  Built section by section from the CLUSTERED_FEATURES.md inventory.
  Sections present: 1 (scanning), 2 (type awareness & section selection),
  3 (templates & section assembly), 4 (badges), 5 (visuals & diagrams).
  Scope is generation only — audit/update modes are not implemented here.
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

Prerequisites: see `DEPENDENCIES.md` (`tree`, `scc`, `licensee`, Python ≥ 3.11). A
missing/old tool makes the scanner emit `{"error": ...}` (which points to
`DEPENDENCIES.md`) and exit 1.

The output is the source of truth for mechanical facts. Fields:

| Field                                    | Meaning                                                                                                   | Feeds                                           |
| ---------------------------------------- | --------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| `project_name`, `description`, `version` | From the primary manifest (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`)                      | Title, intro, version badge                     |
| `license`                                | Detected from `LICENSE*` text (`licensee`), falling back to the manifest SPDX `license` field             | License section + badge                         |
| `git.owner`, `git.repo`                  | Parsed from `origin` remote (SSH + HTTPS)                                                                 | Badge URLs, clone command, links                |
| `package_manager`                        | Lockfile precedence, then `packageManager` field                                                          | Install/run commands                            |
| `manifests`, `package_scripts`           | All manifests + npm scripts                                                                               | Install / build / test / run commands           |
| `is_monorepo`, `packages`                | True when ≥3 sub-manifests; the package dirs                                                              | Component table, per-package scoping            |
| `task_files`                             | Makefile / Taskfile / justfile                                                                            | Task/command discovery                          |
| `config_examples`                        | `.env.example` etc.                                                                                       | Environment-variable section                    |
| `deploy_files`                           | Dockerfile / compose / vercel / etc.                                                                      | Deployment section                              |
| `ci`                                     | Provider + workflow filenames                                                                             | CI badge, workflow filename                     |
| `sibling_docs`                           | ARCHITECTURE / AGENTS / CLAUDE / CONTRIBUTING / CHANGELOG / etc.                                          | Read these instead of re-deriving               |
| `existing_readmes`                       | Path, line count, headings of any current README                                                          | Detect & avoid clobbering an existing README    |
| `directory_structure`                    | 2-level, folder-first tree as nested JSON (from `tree -J`, generated dirs and `.gitignore`d paths pruned) | Project-structure section (render to ASCII art) |

Do not re-derive by hand anything the scanner already reports.

### 1b. Gather judgement (you do this, after reading the facts)

The scanner deliberately stops at facts. These signals need reasoning, so gather
them yourself using `Read`, `Glob`, and `Grep`, guided by the scan output:

- **Public API / signatures.** Start from manifest entry points (`main`,
  `module`, `exports`, `bin`), follow re-exports, and capture the public
  functions/classes with their parameter and return types. (Pattern:
  `references/vendor/accelint-readme-writer/references/codebase-analysis.md`.)
- **Real usage examples.** Pull examples from tests, `@example`/docstring
  blocks, and any `examples/` directory. **Never fabricate examples** — if none
  exist, say so or omit the section.
  (`references/vendor/accelint-readme-writer/references/codebase-analysis.md`.)
- **Project type.** Classified in Step 2 from scanner signals, not here. If a
  read of the code gives you a provisional type, note it — but the decisive
  rules and the section/voice dispatch it drives live in Step 2.
- **Read the sibling docs** the scanner listed (`sibling_docs`) rather than
  reconstructing architecture from source.
  (`references/vendor/accelint-readme-writer/SKILL.md`,
  `references/vendor/readme-blueprint-generator/SKILL.md`.)
- **Rank evidence** when sources disagree: manifest scripts and declared config
  outrank a lockfile, which outranks a version-manager file, which outranks a
  guess. Prefer the strongest evidence and note assumptions.
  (`references/vendor/repository-readme-writer/references/repository-audit.md`.)

### Guardrails

- **Read code before asking the user.** Only ask about things the scan and code
  cannot answer. (`references/vendor/readme/SKILL.md`.)
- **No fabrication.** If a fact is missing (empty scanner field, no examples, no
  license), skip the dependent section rather than invent content.
- **Offline.** The scanner makes no network requests; keep it that way. Fetch
  anything external only on explicit need, and never for private repos.

## Step 2 — Classify the project & select sections

The scanner tells you _what is there_; this step decides _what the README should
contain_. Turn the facts (Step 1a) and your reading of the code (Step 1b) into
exactly one **project type**, then dispatch a **section set** and a **voice
profile**. Do this before writing any prose.

### 2a. Detect the project type

Classify into exactly one of these seven types: **CLI/tool, library/SDK,
application, framework, monorepo, collection, personal.** Detect from evidence —
mostly fields the scanner already reported — not from what the user says.

**First matching row wins**, top to bottom (most specific first):

| Decisive signal (from the scan)                                                                                                                                            | Type        |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| `is_monorepo` is true (≥3 sub-manifests / `packages` populated)                                                                                                            | monorepo    |
| A `skills/` dir of `SKILL.md` files, or a `templates/`/`actions/` dir of many like files                                                                                   | collection  |
| Manifest declares a `bin` (npm), `[project.scripts]` (pyproject), `[[bin]]` (Cargo), or `go.mod` + root `main.go`; and/or a CLI parser dep (commander/yargs/clap/argparse) | CLI/tool    |
| Plugin/middleware architecture with a documented config/extension API (framework config, `register`/`use` extension points)                                                | framework   |
| Web/app framework config with no publish (`next.config.*`, `nuxt.config.*`, `vite.config.*`, `app/`/`pages/` + framework config), or `"private": true` app                 | application |
| Manifest sets `main`/`exports`/`module` (or `[lib]` / library `pyproject`) and has no `bin`                                                                                | library/SDK |
| Single-owner project with no registry publish and a personal framing (dotfiles, hobby repo, first-person intent)                                                           | personal    |

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
`references/vendor/github-readme/REFERENCE.md` (lines 362-385) and
`references/vendor/readme-creator/SKILL.md` (lines 34-52, 110).)

### 2b. Select sections (type → section matrix)

Include every **Required** section; add **Recommended** when the scan supports it;
add **Optional** only when it earns its place. Skip any selected section whose
data the scan proves absent (note the assumption) — never fabricate to fill it.
These are section _names_; the skeletons come later (templates step).

Legend: **R** required · **r** recommended · **o** optional · **—** omit.

| Section                       | CLI/tool | library/SDK | application | framework | monorepo | collection | personal |
| ----------------------------- | :------: | :---------: | :---------: | :-------: | :------: | :--------: | :------: |
| Title + one-liner             |    R     |      R      |      R      |     R     |    R     |     R      |    R     |
| Badges                        |    R     |      R      |      —      |     R     |    —     |     r      |    —     |
| Features / highlights         |    r     |      r      |      R      |     r     |    —     |     —      |    o     |
| Install                       |    R     |      R      |      r      |     R     |    r     |     r      |    R     |
| Usage / Quick start           |    R     |      R      |      R      |     R     |    R     |     R      |    R     |
| API Reference / Options       |    R     |      R      |      —      |     R     |    —     |     —      |    —     |
| Configuration                 |    r     |      r      |      R      |     R     |    o     |     —      |    —     |
| Environment variables         |    —     |      —      |      R      |     —     |    —     |     —      |    —     |
| What's Here (catalog / index) |    —     |      —      |      —      |     —     |    —     |     R      |    —     |
| How to Extend                 |    —     |      —      |      —      |     R     |    —     |     o      |    —     |
| Packages / Components table   |    —     |      —      |      —      |     —     |    R     |     —      |    —     |
| Architecture                  |    —     |      —      |      r      |     r     |    o     |     —      |    —     |
| Requirements                  |    R     |      R      |      o      |     R     |    r     |     o      |    —     |
| Why I built this              |    —     |      —      |      —      |     —     |    —     |     —      |    R     |
| Who this is for               |    r     |      r      |      —      |     r     |    —     |     r      |    —     |
| Contributing                  |    r     |      R      |      r      |     r     |    r     |     r      |    —     |
| License                       |    R     |      R      |      R      |     R     |    R     |     R      |    o     |

Notes:

- **No badges (and no version column) for personal or monorepo** projects here —
  they have no registry entry behind them, so badges render broken or stale.
  Collections get badges only if the collection itself is published.
- The **Packages / Components table** appears only when `is_monorepo` is true; it
  is driven by the scanner's `packages` list.
- **What's Here** (collection) and **How to Extend** (framework/collection) are
  the catalog/extension-point sections folded in from the config/XDG family.

(Reconciled from
`references/vendor/github-readme/SKILL.md` (lines 207-223),
`references/vendor/readme-creator/SKILL.md` (lines 61-80, 111), and
`references/vendor/crafting-effective-readmes/section-checklist.md`.)

### 2c. Voice profile per type

The type also sets tone. Lead the intro in the matching voice:

| Type        | Default tone                   | Example opening                                    |
| ----------- | ------------------------------ | -------------------------------------------------- |
| CLI/tool    | Direct, practical              | "Fast Markdown linting for CI pipelines."          |
| library/SDK | Technical, precise             | "A typed HTTP client for the Stripe API."          |
| application | Product-focused, clear         | "Real-time project dashboard with team analytics." |
| framework   | Precise, extensibility-forward | "A plugin-driven static-site engine."              |
| monorepo    | Organized, scannable           | "Six packages that power the Acme design system."  |
| collection  | Organized, scannable           | "50+ reusable GitHub Actions workflows."           |
| personal    | First-person, opinionated      | "I needed a better way to track reading habits."   |

- **Always:** direct, specific, opinionated; short paragraphs (≤4 sentences).
- **Never:** hedge language, marketing fluff, passive voice in problem
  statements, emojis in prose.
- **Default professional.** First person is opt-in — natural for `personal`,
  otherwise only when the user asks. This sets the tone to write in; after
  drafting, read the prose back and cut hedges, buzzwords, and passive voice by
  hand.

(Voice matrix from
`references/vendor/github-readme/SKILL.md` (lines 227-238).)

### Guardrails

- **Classify before writing.** A mismatched type sends readers down a dead path
  (see the wrong-type smell test in 2a).
- **Required ≠ invent.** Include every Required section, but if the scan proves
  its data does not exist, omit it and record the assumption rather than
  fabricate.
- **One type, one dispatch.** Resolve dual roles in 2a; do not blend two full
  section sets.
- The section set you pick here is _realized_ by the Step 3 skeletons — one
  fill-in template per type under `templates/`. Step 2 decides **which** sections;
  Step 3 lays them out and fills them.

## Step 3 — Choose a template & assemble sections

Step 2 gave you a type and a section set. Now pick a depth, load the matching
fill-in skeleton, and fill it from the scan. The skeletons are scaffolding: every
`{{token}}` must be replaced and every guiding HTML comment deleted before you
ship.

### 3a. Pick a depth tier

The tier decides how many of the Step 2 sections to include:

| Tier                   | Use for                                             | Includes                                                    |
| ---------------------- | --------------------------------------------------- | ----------------------------------------------------------- |
| **minimal**            | small utilities, internal tools, one clear use case | **Required** sections only                                  |
| **standard** (default) | projects expecting external users or contributors   | Required **+ Recommended**                                  |
| **comprehensive**      | mature projects, public APIs, large communities     | Required + Recommended **+ Optional** and extended sections |

Map the tier onto the Step 2 matrix markers: minimal = **R**; standard = **R + r**;
comprehensive = **R + r + o** (plus anything from the section library). Default to
standard unless the project or the user says otherwise.
(Tiers from `references/vendor/make-readme/SKILL.md` lines 53-58.)

### 3b. Load the type skeleton

Open `templates/<type>.md` for the type you classified in Step 2 (`cli`,
`library`, `application`, `framework`, `monorepo`, `collection`, `personal`). Each
skeleton lays the Step 2 sections out in **inverted-pyramid order** — strongest
fact first, then install/quick start, then the "why", then reference detail, then
the tail (contributing, license). **Type = shape, depth = filter:** the file gives
the shape; drop the sections your 3a tier excludes.

Each skeleton opens with two filled title + one-liner examples (few-shot). Use
them to calibrate the voice for that type (per the Step 2 voice profile), then
**delete that comment** along with every other HTML comment.
(Skeletons reconciled from
`references/vendor/readme-creator/references/section-templates.md`; order from
`references/vendor/write-readme/REFERENCE.md` lines 3-21.)

### 3c. Write the intro (4-paragraph formula)

The slot under the title carries the most weight. Build it from four short beats:

1. One memorable sentence — what it **is**.
2. One to three sentences — what it **does**.
3. What **need** it meets.
4. **Whom** it is for.

Collapse to one or two sentences for the minimal tier; the one-liner alone may
suffice. (`references/vendor/diataxis-gen-readme/SKILL.md` lines 9-19.)

### 3d. Pull optional sections

For anything beyond the base skeleton — Performance, Security, Migration/Upgrade,
Shell Completions, Comparison/Alternatives, and the rest — copy the matching
skeleton from `references/section-library.md`. Include per the 3a tier and only
when the scan supports the section; skip it otherwise rather than invent content.

The Project Structure and Architecture blocks are produced in Step 5 (file tree
from the scanner's `directory_structure`; architecture diagram in Mermaid/ASCII).

### 3e. Table of contents (conditional)

Add a TOC **only when the finished README exceeds ~100 lines** — below that it
just pushes install below the fold. Keep it to at most two heading levels.

GitHub's anchor autogeneration breaks on headings with badges or emoji. When that
happens, put an explicit anchor on its own line before the heading and link to it:

```markdown
<a id="quick-start"></a>

## Quick Start
```

(Threshold from `references/vendor/standard-readme/SKILL.md` lines 96-108; anchor
technique from `references/vendor/make-readme/SKILL.md` lines 100-109.)

### 3f. Progressive disclosure

Keep the README focused on the 80% use case. Use `<details>` collapsibles for
content that matters but breaks the happy path — raw benchmark tables, alternative
install paths, exhaustive config references, contributor-only architecture notes.
Never hide something a first-time user needs; if you are tempted to, restructure
instead. Once a README grows past ~1000 lines, split detail out into `docs/`
files and link to them under a Documentation section.
(`references/vendor/write-readme/REFERENCE.md` lines 259-269;
`references/vendor/crafting-readme-files/SKILL.md` lines 488-512.)

### 3g. Companion files

When the Contributing or Changelog sections warrant their own files, start from
`templates/companion/CONTRIBUTING.md` and `templates/companion/CHANGELOG.md`
(Keep-a-Changelog / SemVer). Fill and trim them the same way as the README.

### Guardrails

- **Consume the scaffolding.** Replace every `{{token}}` and delete every HTML
  comment. No `{{...}}` may survive into the output — the audit step's
  `rg -n "foo|bar|TODO|\{\{"` render-check treats any hit as not-done.
- **Real values only.** Every code block must run as-is after copy-paste; use
  values from the scan, never `foo`/`bar`/`example`/`test`.
- **Empty fact, no section.** If a selected section has no supporting scan data,
  omit it and note the assumption — do not fabricate to fill the skeleton.
- **The skeleton is a starting point,** not a form to ship verbatim; adapt
  ordering and wording to the actual project.

## Step 4 — Badges

Badges go in the slot directly under the title and one-liner. They are optional
and easy to overdo: a badge earns its place only when it states a verifiable fact
a reader would act on. Work through the gate, the set, the design, and the layout
in order, then check the result against the anti-patterns.

**Badges are generated as static local SVG files with `pybadges`**, committed to
the repo, and referenced by relative path — not hosted shields.io URLs. This keeps
the README self-contained and free of third-party runtime fetches, at the cost of
being a snapshot: a committed badge shows the value at generation time and must be
regenerated to change. `pybadges` is a hard dependency (see `DEPENDENCIES.md`);
install it from the maintained fork, which supports Python 3.9–3.14:
`pip install git+https://github.com/NicholasSynovic/pybadges`.

The vendored `readme-badger` skill remains the **design** reference for badge
_content_ — which badges suit each project type, the color system, Simple-Icons
logo slugs, layout conventions, and anti-patterns. Its shields.io URL syntax and
dynamic-endpoint sections no longer apply; use `pybadges` to render instead.

### 4a. Gate: should this project have badges at all?

Skip badges **entirely** unless the project publishes to a public registry (PyPI,
npm, crates.io, Docker Hub, Go pkg) or is a public GitHub repo where a
version/license/build fact is worth stating. Private apps, internal monorepos, and
unpublished skill bundles get **no badges** — a badge that states nothing is worse
than none. Use the scan's `git.owner`/`git.repo` (empty when there's no git
remote) and the package name to decide; if there's no published fact, stop here.
(`references/vendor/readme-creator/SKILL.md` lines 94-98;
`references/vendor/readme/SKILL.md` lines 105-118.)

### 4b. Cap the count

Aim for **3-6 badges; hard cap at ~6.** Beyond that is noise, and duplicate facts
(a "Built with Python" badge next to a version badge) add none. Minimal-tier
READMEs (Step 3a) should carry at most the essentials — build status and version.
Order badges by importance: **build status → version → downloads → license**,
with any identity/hero badge first.
(`references/vendor/readme/SKILL.md` line 116;
`references/vendor/readme-badger/SKILL.md` lines 330-332 for the overload rule.)

### 4c. Pick the badge content by project type

Decide _which_ badges to show from the Step 2 project type / language, using the
per-type badge sets in `readme-badger` as the content guide — Python library/CLI,
JS/TS package, Rust crate, Claude Code plugin, or general open-source. Take the
left/right text and colors from those sets and from the scan (version from the
manifest/latest tag, license from the license scan, package name), but render each
one locally with `pybadges` (4d) rather than emitting a shields.io URL.
(Badge content by type: `references/vendor/readme-badger/SKILL.md` lines 83-160;
color reference lines 269-298; Simple-Icons slugs lines 233-267.)

### 4d. Generate each badge with `pybadges`

Run the `pybadges` CLI once per badge, redirecting stdout to an SVG file under a
committed assets directory (e.g. `assets/badges/`):

```bash
python3 -m pybadges \
  --left-text=license --right-text=MIT \
  --right-color='#4c1' \
  --whole-link='https://github.com/OWNER/REPO/blob/main/LICENSE' \
  > assets/badges/license.svg
```

Key flags (`python3 -m pybadges --help` for the full list):

- `--left-text` / `--right-text` — the label and value.
- `--left-color` / `--right-color` — backgrounds (default left `#555`, right
  `#007ec6`); use the `readme-badger` color reference for semantic colors.
- `--whole-link` (or `--left-link` / `--right-link`, which are mutually exclusive
  with `--whole-link`) — the click target.
- `--logo` — a URI or file path to a Simple-Icons SVG; add `--embed-logo` to
  inline the icon as a data-URI so the badge stays self-contained offline.
- `--left-title` / `--right-title` — accessibility titles on the SVG parts.

`pybadges` renders one flat github-style badge; it has **no** `for-the-badge` /
`flat-square` / `social` / `plastic` style variants, so treat "flat" as the only
style and drop any style-selection guidance from `readme-badger`.

### 4e. Reference and lay out the generated SVGs

Reference each committed SVG by **relative path**, wrapped in a Markdown image and
a link to its data source:

```markdown
[![License](./assets/badges/license.svg)](./LICENSE)
```

Arrange them to fit the badge count and tone (layout conventions still apply):

- **Inline after the title** — 2-4 badges, no HTML. Developer-facing.
- **Centered single row** — 3-8 badges in `<p align="center">`. Polished.

(Layout conventions: `references/vendor/readme-badger/SKILL.md` lines 162-221.)

### Guardrails

- **No badge without a gate.** If 4a says there's no published fact, ship zero
  badges — do not generate a badge for a version, registry, or CI status that
  does not exist.
- **Real values only.** Fill `--left-text`/`--right-text` from the scan (manifest
  version, detected license, package name); never invent a version or a passing
  build status.
- **Commit the SVGs and link by relative path.** The generated files must live in
  the repo (e.g. `assets/badges/`) and be referenced relatively; a badge pointing
  at a missing file renders broken.
- **Every badge is linked and labelled.** Wrap each in a link to its data source
  (`[![alt](svg)](url)`) with descriptive alt text and, where useful, a
  `--*-title`; an unlinked or alt-less badge fails accessibility.
- **Verify logo slugs.** Non-obvious Simple-Icons slugs (`gnubash`, `vuedotjs`,
  `nextdotjs`, `openjdk`, `nodedotjs`, `cplusplus`) and forbidden brands (AWS,
  Azure, VS Code, OpenAI, …) render a missing icon if wrong — check the catalog.
  (`references/vendor/readme-badger/SKILL.md` lines 233-267.)
- **Drop no-information badges.** "Open Source", "Maintained", "Awesome" and the
  like consume space without stating a verifiable fact — cut them.
  (`references/vendor/readme-badger/SKILL.md` lines 328-353.)
- **Regenerate on change.** Static SVGs are snapshots; when a version or license
  changes, re-run `pybadges` to refresh the committed files.

## Step 5 — Visuals & diagrams

A good diagram earns a reader's understanding faster than a paragraph — but a bad
or unnecessary one is clutter. This step produces two kinds of visual from the
scan: an **architecture diagram** (how the components relate) and the
**project-structure file tree** (what's on disk). It also adds an optional
star-history footer. Everything here is generated from scanned facts; never draw a
component that isn't in the project.

### 5a. Decide whether a diagram is warranted

Add an architecture diagram **only** when the project has multiple components or a
clear data flow. Skip it entirely for simple projects — a single library, a small
CLI, or a docs-only repo. Prefer a diagram over a screenshot when it conveys the
same structure with less maintenance.
(`references/vendor/readme-wizard/assets/diagrams.md` line 3;
`references/vendor/crafting-readme-files/SKILL.md` lines 253-278.)

### 5b. Architecture diagram — Mermaid (default)

Mermaid is the default: it renders natively on GitHub and stays diffable as text.
Build it from the **actual** scanned structure — `directory_structure`, detected
components, and monorepo packages — not a stock template. Use the archetype that
matches the Step 2 project type as a starting point, then adapt node names and
edges to the real project:

- **application / framework** → `graph LR` client → API → data/cache/queue.
- **monorepo** → `graph TD` root → packages, with inter-package edges.
- **cli** → `graph LR` input → parser → command handler → output/filesystem.
- **collection (plugins)** → `graph TD` core → plugins → shared API.
- **pipeline / content** → `graph LR` source → transform → output → deploy.

Adapt, don't paste — a diagram that names generic boxes tells the reader nothing.
(Archetypes: `references/vendor/readme-wizard/assets/diagrams.md`, with the
"adapt, don't use as-is" rule at line 62; Mermaid-in-Architecture examples at
`references/vendor/configure-readme/REFERENCE.md` lines 374-385 and
`references/vendor/create-github-readme/prompt.md` lines 72-84.)

### 5c. Architecture diagram — ASCII (fallback)

When Mermaid won't render — plain-text READMEs, PyPI/RST output, terminal viewers
— or when a lighter touch fits, draw the same architecture as a box-and-arrow
ASCII diagram in a fenced block (layers stacked top-to-bottom, arrows for flow).
It conveys the same structure and never depends on a renderer.
(`references/vendor/crafting-readme-files/SKILL.md` lines 253-278.)

### 5d. Project-structure file tree

For the Project Structure section, render the scanner's `directory_structure`
(nested `tree -J` JSON, two levels deep, directories first) into an ASCII tree
inside a fenced code block. This is a **file tree** — distinct from the
architecture diagram in 5b/5c, which shows components and data flow, not files.
Include it when the layout is not obvious from the intro; skip it for
single-file projects.

### 5e. Star-history footer (optional)

For a public GitHub repo, you may close the README with a star-history chart.
Gate it on the scan: include only when `git.owner` and `git.repo` are both present
(empty means no remote — omit the footer). Fill owner/repo from the scan:

```markdown
[![Star History Chart](https://api.star-history.com/svg?repos=OWNER/REPO&type=Date)](https://star-history.com/#OWNER/REPO&Date)
```

Note this is a **hosted external image** (star-history.com renders it live), the
same category of dependency the badge migration is moving away from — include it
only if the project wants that trade-off.
(`references/vendor/readme-wizard/assets/readme-template.md` line 52.)

### Guardrails

- **Diagrams reflect real structure.** Every node and edge must correspond to a
  scanned component, package, or data flow — never invent boxes to fill a diagram.
- **Gate on complexity and facts.** No architecture diagram for simple projects
  (5a); no star-history footer without `git.owner`/`git.repo` (5e).
- **Out of scope — do not add:** Playwright/automated screenshot capture,
  Storybook image regeneration, and contributor-avatar blocks (contrib.rocks).
  These are deliberately excluded from this skill.
- **Fenced blocks render as-is.** Mermaid must be valid Mermaid; ASCII trees and
  diagrams go in plain fenced blocks so they survive every renderer.
