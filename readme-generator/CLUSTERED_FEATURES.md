# README Generator/Updater — Feature Inventory

Clustered feature analysis of the 34 vendored README-generator skills under
`references/vendor/`. Purpose: **design input for a single merged README
generator + updater skill.**

## How to read this doc

- Features are grouped by **capability cluster**, not by source skill.
- Each feature cites its supporting source as `skill-name/file (lines X-Y)`,
  relative to `references/vendor/`.
- Each cluster ends with a **> For the merged skill** note recommending what to
  adopt.
- Skills that are not general README.md generators (WordPress `readme.txt`, the
  readme.com SaaS, single-table maintenance, etc.) are flagged in
  [Out-of-scope / edge-case skills](#out-of-scope--edge-case-skills).

---

## 1. Codebase / repository scanning & metadata extraction

Automatically learn about the project instead of asking the user everything.

- **Manifest metadata extraction** (name/version/license/keywords) from
  `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`
    - `configure-readme/SKILL.md` (lines 52-67)
    - `make-readme/SKILL.md` (lines 22-33)
    - `update-readme/SKILL.md` (lines 67-81)
    - `standard-readme/SKILL.md` (lines 203-204)
- **Lockfile → package-manager detection** (pnpm/yarn/bun/npm/pip/poetry/cargo/go)
    - `accelint-readme-writer/SKILL.md` (lines 196-201); `accelint-readme-writer/references/writing-principles.md` (lines 179-187)
    - `readme-wizard/scripts/scan_project.sh` (lines 104-130)
- **Public-API / signature extraction** (functions, generics, overloads, classes with param/return types)
    - `accelint-readme-writer/references/codebase-analysis.md` (lines 135-219)
- **Example extraction from tests / JSDoc `@example` / `examples/`** (never fabricated)
    - `accelint-readme-writer/references/codebase-analysis.md` (lines 223-281)
- **Project-type detection from signals** (CLI/library/app/framework/monorepo/collection/personal)
    - `github-readme/SKILL.md` (lines 86-98); `github-readme/REFERENCE.md` (lines 362-385)
    - `readme-creator/SKILL.md` (lines 34-51)
    - `write-readme/SKILL.md` (line 20)
- **Monorepo / plugin-collection detection** (3+ sub-manifests → component table; per-package scoping)
    - `make-readme/SKILL.md` (lines 30-32, 96-99)
    - `accelint-readme-writer/references/codebase-analysis.md` (lines 8-35)
    - `readme-updates/SKILL.md` (lines 9-110)
    - `repository-readme-writer/references/repository-audit.md` (lines 87-89)
- **Project-structure tree generation** (`tree -L 2`, generated dirs excluded; folders-first alphabetized)
    - `configure-readme/SKILL.md` (lines 137-139)
    - `readme-wizard/scripts/scan_project.sh` (lines 219-247)
    - `scan_project.py` emits the structure as `tree -J` JSON; Step 5 of
      `SKILL.md` renders that JSON into an ASCII-art tree for the
      project-structure section.
- **Auto-detected project commands** (install/run/test/build per package manager)
    - `configure-readme/SKILL.md` (lines 126-136)
- **Repository signal probe** (task runners Makefile/Taskfile/justfile, config examples, deploy files, CI workflows, existing README headings)
    - `repository-readme-writer/scripts/repo_readme_probe.py`
- **Structured JSON scan output** (name, description, license, git remote owner/repo, CI, social links, tree)
    - `readme-wizard/scripts/scan_project.sh`
- **Social-link harvesting** (GitHub API homepage + homepage crawl for YouTube/Discord/Twitter/LinkedIn/Bluesky/Twitch)
    - `readme-wizard/scripts/scan_project.sh` (lines 161-217)
- **Cross-reference to sibling docs** (ARCHITECTURE.md, AGENTS.md/CLAUDE.md, openspec, `.github/copilot/*`) to reduce scanning
    - `accelint-readme-writer/SKILL.md` (lines 57-83, 144)
    - `readme-blueprint-generator/SKILL.md` (lines 8-19)
- **Evidence-ranking methodology** (manifest scripts > lockfile > version-manager file)
    - `repository-readme-writer/references/repository-audit.md`

> For the merged skill: adopt a scan-first workflow with a reusable scan script
> (model on `scan_project.sh` + `repo_readme_probe.py`) feeding manifest
> metadata, package-manager, project-type, tree, and commands. Read code before
> asking the user (`readme/SKILL.md` lines 17-24). Never fabricate examples.

---

## 2. Project-type awareness & section selection

Adapt which sections, tone, and badges appear based on project type.

- **Type → section matrix** (required/recommended/optional per type)
    - `github-readme/SKILL.md` (lines 207-224)
    - `readme-creator/SKILL.md` (lines 62-81)
    - `crafting-effective-readmes/section-checklist.md`
- **Audience/project-type template families** (OSS, personal, internal, config/XDG)
    - `crafting-effective-readmes/templates/oss.md`, `templates/personal.md`, `templates/internal.md`, `templates/xdg-config.md`
- **Voice calibration by type** (tone / lead-with / avoid matrix; professional default, opt-in first person)
    - `github-readme/SKILL.md` (lines 139-143, 227-238); `github-readme/REFERENCE.md` (lines 564-593)
- **Project-type-specific sections** (CLI global-install, library API, web-app Demo/Screenshots/env-vars)
    - `configure-readme/REFERENCE.md` (lines 298-304)
- **Type-specific templates** (library / CLI / agent-tool)
    - `write-readme/REFERENCE.md` (Tool/CLI, Library, Agent templates)

> For the merged skill: detect type in cluster 1, then dispatch a section set +
> voice profile. `readme-creator` (scored, rigorous) and `github-readme` (6
> types + voice matrix) are the strongest models.

---

## 3. Templates & section libraries

- **Depth tiers** (minimal / standard / comprehensive)
    - `make-readme/SKILL.md` (lines 53-58, 83-125)
    - `create-github-readme/templates/{minimal,standard,comprehensive}.md`
    - `configure-readme/SKILL.md` (lines 43-46, 168)
- **"Golden structure" / sales-pitch flow** (Hero → TL;DR → Quick Start → Reference → Support)
    - `readme-craft/SKILL.md` (lines 19-96)
    - `crafting-readme-files/SKILL.md` (lines 54-86)
- **Inverted-pyramid structure** (value → install → why/boundaries → reference tail)
    - `write-readme/REFERENCE.md` (lines 3-21)
- **Diátaxis 4-paragraph intro** (what it is / what it does / what need / for whom)
    - `diataxis-gen-readme/SKILL.md` (lines 9-19)
- **Full comprehensive ready-to-fill template** (~320 lines: header→acknowledgments)
    - `readme-generator/SKILL.md` (lines 21-342)
- **Specialized/extended section templates** (Performance/Benchmarks, Security, Data Model, API Reference, Migration/Upgrade, Ecosystem, Env-Var, Shell Completions, Release Notes)
    - `crafting-readme-files/references/section-templates.md`
    - `readme-craft/references/section-templates.md`
    - `readme-creator/references/section-templates.md`
    - `crafting-readme-files/references/section-templates.md`
- **Comparison / alternatives table** (✅/⚠️/❌ vs alternatives)
    - `crafting-readme-files/SKILL.md` (lines 164-182)
    - `readme-craft/SKILL.md` (lines 99-112)
- **Troubleshooting / Limitations / FAQ** (mandatory troubleshooting; limitation/workaround/planned table; collapsible FAQ)
    - `crafting-readme-files/SKILL.md` (lines 280-346)
    - `readme-craft/SKILL.md` (lines 172-227)
- **Multi-path install** (curl one-liner, package managers, from source)
    - `crafting-readme-files/SKILL.md` (lines 184-227)
    - `readme-craft/SKILL.md` (lines 114-146)
    - `readme-generator/SKILL.md` (lines 60-80)
- **Companion-file templates** (CONTRIBUTING.md, CHANGELOG.md — Keep-a-Changelog/SemVer)
    - `readme-generator/SKILL.md` (lines 383-519)
- **Environment-variable section from `.env.example`**
    - `readme-updates/SKILL.md` (lines 121-133)
- **Progressive disclosure** (`<details>` collapsibles, doc-link splitting for long READMEs)
    - `crafting-readme-files/SKILL.md` (lines 488-512)
    - `write-readme/REFERENCE.md` (lines 234-269)
- **TOC generation** (conditional: only when README exceeds ~100-200 lines; anchor workaround)
    - `accelint-readme-writer/references/writing-principles.md` (lines 222-239)
    - `standard-readme/SKILL.md` (lines 96-108)
    - `make-readme/SKILL.md` (lines 100-109)
- **AGENTS.md condensed-reference blurb** (scannable block for AI agents)
    - `crafting-readme-files/SKILL.md` (lines 378-416)

> For the merged skill: ship tiered templates + a specialized-section library,
> and a conditional-TOC rule. Draw the section catalog primarily from
> `crafting-readme-files`, `readme-craft`, and `readme-generator`.

---

## 4. Badges

- **shields.io URL generation with encoding rules** (`_`→space, `__`→`_`, `--`→`-`)
    - `readme-badger/SKILL.md` (lines 16-54)
    - `make-readme/references/badges.md` (lines 33-42)
- **Style selection** (flat / flat-square / for-the-badge / social / plastic)
    - `readme-badger/SKILL.md` (lines 57-81)
    - `github-readme/SKILL.md` (lines 242-257) — `for-the-badge`
- **Project-type badge sets** (Python/JS-TS/Rust/plugins/general OSS)
    - `readme-badger/SKILL.md` (lines 83-160)
- **Layout patterns** (two-tier hero+metadata, inline, centered, stacked, reference, table)
    - `readme-badger/references/layout-patterns.md`
- **Simple Icons logo slugs** (non-obvious slugs, `logoColor` decision tree, forbidden brands)
    - `readme-badger/references/simple-icons-catalog.md`
- **Dynamic vs static badge decision logic** (+ endpoint reference)
    - `readme-badger/SKILL.md` (lines 300-324)
- **Badge anti-patterns** (overload, mismatched styles, missing alt text, broken slugs, unlinked/no-info)
    - `readme-badger/SKILL.md` (lines 328-353)
- **Multi-markup badge syntax** (Markdown, RST, AsciiDoc, Textile, RDoc, Org, MediaWiki, Pod, plaintext)
    - `readme-badger/references/format-support.md`
- **Alternative badge services** (Badgen, ForTheBadge, pepy.tech)
    - `readme-badger/references/badge-services.md`
- **Conditional / capped badges** (only for registry-published projects; cap ~3-6)
    - `readme-creator/SKILL.md` (lines 94-98)
    - `readme/SKILL.md` (lines 105-118)
- **Badge galleries / references**
    - `readme-generator/SKILL.md` (lines 344-381)
    - `github-readme/REFERENCE.md` (lines 7-116)
    - `readme-wizard/assets/badges.json`

> For the merged skill: badge generation uses `pybadges` to render static local
> SVGs (committed, referenced by relative path), replacing shields.io URLs
> entirely. The `readme-badger` corpus is retained as the **design** reference
> for badge content — which badges suit each type, colors, Simple-Icons slugs,
> layout, anti-patterns — while its shields.io URL and dynamic-endpoint sections
> no longer apply. The conditional/capped gate from `readme-creator` still holds.
> Realized as Step 4 of `SKILL.md`; `pybadges` documented in `DEPENDENCIES.md`.
>
> Migration notes, now resolved:
>
> - Badges are static snapshots — dynamic values (version, downloads, stars, CI,
>   coverage) are captured at generation time and must be regenerated on change;
>   the updater (Step 6) is responsible for refreshing them.
> - `pybadges` renders only one flat github-style badge — no `for-the-badge`/
>   `flat-square`/`social`/`plastic` variants — so style selection is dropped.
> - `pybadges` 3.0.1 imports the removed `imghdr` module and crashes on Python
>   3.13+ without the `standard-imghdr` shim (or a 3.11/3.12 interpreter); see
>   `DEPENDENCIES.md`.

---

## 5. Visuals & diagrams

- **Mermaid architecture diagrams** (API/web app, monorepo, pipeline, CLI, plugin)
    - `readme-wizard/assets/diagrams.md`
    - `configure-readme/REFERENCE.md` (lines 374-385)
    - `create-github-readme/prompt.md` (lines 72-84)
- **ASCII architecture diagrams** (favored over screenshots in some skills)
    - `crafting-readme-files/SKILL.md` (lines 253-278)
- **Screenshot automation via Playwright MCP** (navigate → wait → full-page → save; live-demo URL auto-detection; idempotent skip)
    - `create-github-readme/SKILL.md` (lines 63-140)
- **Deterministic screenshot generation from Storybook** (Playwright + Sharp, WebP, Chromatic-triggered) — _asset maintenance, edge case_
    - `generate-readme-screenshots/SKILL.md` (lines 72-104, 176-181)
- **Screenshot/demo guidance** (tight crops, <15s demos, WebP/AVIF over 8MB GIFs, dated captions)
    - `write-readme/REFERENCE.md` (lines 271-290)
    - `readme-updater/SKILL.md` (lines 201-212)
- **Contributor avatars (contrib.rocks) + star-history chart footer**
    - `readme-wizard/assets/readme-template.md` (lines 35-37, 52)

> For the merged skill: support Mermaid (default) + ASCII architecture diagrams
> inline, both generated from the scanned structure; render the project-structure
> file tree from the scanner's `directory_structure`; and offer an optional
> star-history footer for public repos. **Out of scope:** Playwright/automated
> screenshot capture, Storybook image regeneration, and contributor-avatar
> (contrib.rocks) blocks. Realized as Step 5 of `SKILL.md`.

---

## 6. Updating / syncing an existing README

Core of the "updater" half of the merged skill.

- **Create-or-update detection** (existing README → preserve project-specific details; delegate creation if none/thin)
    - `create-github-readme/SKILL.md` (lines 44-60)
    - `update-readme/SKILL.md` (lines 22-31)
    - `github-readme/SKILL.md` (lines 34-43)
- **Git-diff-driven suggestions** (map code changes → README sections)
    - `readme-updater/SKILL.md` (lines 46-126)
    - `sc-readme/SKILL.md` (lines 60-83, 109-121)
- **Git-history-driven change categorization** (new features / breaking / deprecations / fixes since last README touch)
    - `update-readme/SKILL.md` (lines 83-104)
- **Code-change → section mapping** (package.json→deps, routes→API, .env.example→env vars, docker-compose→setup)
    - `readme-updater/SKILL.md` (lines 106-126)
    - `sc-readme/SKILL.md` (lines 73-83)
- **Documentation-audit diff** (missing exports, stale examples, signature changes)
    - `accelint-readme-writer/references/codebase-analysis.md` (lines 284-325)
- **Stale-content & placeholder detection** (YOUR_USERNAME, TODO, `{{...}}`, angle-bracket values, thin sections)
    - `update-readme/SKILL.md` (lines 47-65)
    - `readme-creator/SKILL.md` (line 104)
- **Structure/tone preservation** (keep emoji style, formatting, voice, organization)
    - `readme-updater/SKILL.md` (lines 128-138)
- **Minimal-edit / prioritized update strategy** (version/badge → stale → placeholders → new features → thin; Edit vs Write >60% threshold)
    - `update-readme/SKILL.md` (lines 113-139)
- **Version-compatibility & version/badge updates**
    - `readme-updater/SKILL.md` (lines 122-124, 174-184)
- **CHANGELOG.md sync integration**
    - `update-readme/SKILL.md` (lines 33-39, 108-111)
    - `readme-updater/SKILL.md` (lines 186-199)
- **Cross-reference validation** (API routes, env vars, file paths, component names, commands still exist)
    - `sc-readme/SKILL.md` (lines 122-131)
- **Staleness report** (STALE / UP-TO-DATE checkboxes)
    - `sc-readme/SKILL.md` (lines 132-155)
- **Drift verification / additive-edit guard** (vocab/cosine similarity; CI threshold; cross-lingual pairs)
    - `indexion-readme/SKILL.md` (lines 133-157)
- **Diff-summary report output**
    - `update-readme/SKILL.md` (lines 141-149)
    - `github-readme/SKILL.md` (lines 192-204)
- **Section-in-place replacement / table regeneration** (edge cases)
    - `readme-sync/SKILL.md` (lines 34-41)
    - `prowler-readme-table/SKILL.md` (lines 57-84)
- **Guardrails** (backup, no silent section removal, git rollback, no auto-commit)
    - `sc-readme/SKILL.md` (lines 156-234)
    - `prowler-readme-table/SKILL.md` (lines 100-105)

> For the merged skill: the updater path should = git-diff/history scan +
> stale/placeholder detection + tone preservation + minimal-edit strategy +
> diff-summary. `update-readme` and `sc-readme` are the strongest models;
> `readme-updater` supplies the change→section mapping.

---

## 7. Auditing & scoring

- **Scored quality audit (0-100 weighted rubric)**
    - `github-readme/SKILL.md` (lines 156-190); `github-readme/REFERENCE.md` (lines 388-409)
    - `readme/SKILL.md` (lines 26-44) — 8-dimension rubric
    - `wp-readme-optimizer/SKILL.md` (lines 37-107) — /80 (WordPress, edge case)
- **Compliance report** (PASS/MISSING/PARTIAL per section)
    - `configure-readme/SKILL.md` (lines 69-98); `configure-readme/REFERENCE.md` (lines 84-109)
- **Audit output report** (score table + "Top 3 rewrites" / findings by severity)
    - `readme/SKILL.md` (lines 120-141)
    - `standard-readme/SKILL.md` (lines 229-251)
    - `repository-readme-writer/templates/readme-review.md`
- **Scored quality checklist with hard-fail gate**
    - `readme-creator/references/quality-checklist.md`; `readme-creator/SKILL.md` (lines 100-107)
- **Currency/freshness checks** (versions vs config, stale links)
    - `github-readme/SKILL.md` (lines 166-169)
- **Placeholder/render scan** (`rg` for `foo|bar|TODO|{{`)
    - `readme-creator/SKILL.md` (line 104)
- **Final verify checklist** (≤300 lines, ≤15-word one-liner, copy-paste install)
    - `readme/SKILL.md` (lines 143-156)
- **markdownlint / markdown-link-check validation**
    - `readme-updates/SKILL.md` (lines 143-151)
    - `configure-readme/SKILL.md` (lines 153-161)
- **Evals / self-test scripts**
    - `readme-wizard/evals/evals.json`
    - `repository-readme-writer/evals/evals.json`, `scripts/test_skill.py`, `scripts/validate.py`

> For the merged skill: offer an explicit **audit mode** (read-only, scored
> rubric + severity findings) alongside generate/update. `github-readme`'s
> weighted 0-100 rubric + `readme-creator`'s hard-fail checklist are the model.

---

## 8. Writing quality / humanizing

- **AI-slop removal** (banned buzzwords, generic openers, fake enthusiasm, formulaic structure)
    - `humanize-readme/SKILL.md` (lines 30-43); `humanize-readme/references/slop-patterns.md` (lines 5-64)
    - `accelint-readme-writer/references/writing-principles.md` (lines 243-369)
    - `write-readme/SKILL.md` (lines 33, 64)
- **Buzzword ban list** (comprehensive/robust/seamless/leverage/utilize)
    - `readme-writer/SKILL.md` (lines 88-99)
- **Burstiness / sentence-rhythm check** (uniform length = AI tell)
    - `humanize-readme/references/slop-patterns.md` (lines 171-183)
- **Personal-voice injection** (why it exists, honest limitations, tradeoffs)
    - `humanize-readme/references/slop-patterns.md` (lines 185-208)
- **Content-preservation guardrails** (keep code/links/badges; don't change technical claims)
    - `humanize-readme/SKILL.md` (lines 52-72)
- **Flesch-Kincaid readability scoring** (target grade ≤11)
    - `readme-writer/scripts/flesch_kincaid.rb`
- **ESL vocabulary profiler** (% words in top-1000 basic English)
    - `readme-writer/scripts/vocabulary_profiler.rb`; `readme-writer/scripts/top1000.txt`
- **ESL-friendly writing rules** (active voice, short noun phrases, explicit transitions, no idioms)
    - `readme-writer/SKILL.md` (lines 36-61)
- **GFM callout/admonition guidance** (`[!NOTE]`, `[!WARNING]`)
    - `readme-writer/SKILL.md` (lines 72-81)
    - `create-readme/SKILL.md` (line 18)
- **Feature-bullet style** (colon not hyphen; benefit-first)
    - `readme-creator/SKILL.md` (lines 108-116)
- **"Ruthless cut" pass** (remove badge noise, duplicated sections, copied `--help` tables)
    - `write-readme/SKILL.md` (lines 37-46)

> For the merged skill: bundle a humanize/lint pass (from `humanize-readme` +
> `readme-writer` scripts) as a required final step, with strict
> content-preservation guardrails.

---

## 9. Security / privacy / agent-safety

- **PII / secret scrubbing** (IPs, API keys/tokens, private hostnames, key material, username paths)
    - `github-readme/SKILL.md` (lines 261-276); `github-readme/REFERENCE.md` (lines 463-560)
- **Secret-scan on push** (via `/github-push`)
    - `create-github-readme/SKILL.md` (lines 215-224)
- **"Agent-safe" README design** (avoid brittle path tours / version pins agents follow verbatim)
    - `repository-readme-writer/references/gotchas.md`; `repository-readme-writer/SKILL.md` (lines 49-56)

> For the merged skill: run a secret/PII scrub in every mode; adopt agent-safe
> phrasing conventions.

---

## 10. Discoverability (SEO / AEO)

- **SEO audit** (repo name, GitHub About/description, topics ≤20, social preview image)
    - `github-readme/SKILL.md` (lines 102-127); `github-readme/REFERENCE.md` (lines 412-437)
- **AEO + llms.txt generation** (LLM-friendly structure; `llms.txt`/`llms-full.txt`)
    - `github-readme/REFERENCE.md` (lines 439-459)
- **Keyword optimization / CTR** (short-description char limits, caption SEO) — _WordPress, edge case_
    - `wp-readme-optimizer/SKILL.md` (lines 27-33, 54-61)

> For the merged skill: offer an optional discoverability add-on (topics,
> About text, social preview, llms.txt) from `github-readme`.

---

## 11. Workflow, interaction & integration

- **Interactive interview** (AskUserQuestion rounds: type/language/depth/license/sections/badges/style)
    - `make-readme/SKILL.md` (lines 35-79)
- **Explicit modes** (generate / audit / update)
    - `github-readme/SKILL.md` (lines 34-43)
    - `standard-readme/SKILL.md` (lines 18-22)
- **CLI-flag interface** (`--check-only`, `--fix`, `--style`, `--badges`; `--base`, `--scope`, `--commits`, `--consensus`)
    - `configure-readme/SKILL.md` (lines 33-47)
    - `sc-readme/SKILL.md` (lines 48-59)
- **Parallel sub-agent research** (entry points / deps / examples / git history concurrently)
    - `accelint-readme-writer/SKILL.md` (lines 84-116)
    - `update-readme/SKILL.md` (lines 41-106)
- **Decision-tree routing by task** (new / improve / fix-setup / review)
    - `repository-readme-writer/SKILL.md` (lines 19-37)
- **Inspiration from real-world READMEs** (fetch exemplars for structure/tone)
    - `create-readme/SKILL.md` (lines 13-17)
    - `readme-craft/SKILL.md` (lines 259-265)
- **Multi-model consensus** (PAL MCP for API/breaking changes)
    - `sc-readme/SKILL.md` (lines 163-181)
- **Auto-push to GitHub** (secret-scan, stage, commit, push, repo config)
    - `create-github-readme/SKILL.md` (lines 215-224)
- **Sub-agent / command / CI handoff** (`@docs-writer`, `/docs-gen`, CI workflows)
    - `readme-updater/SKILL.md` (lines 214-233)
- **Standards-tracking file** (`.project-standards.yaml`)
    - `configure-readme/SKILL.md` (lines 141-151)
- **Anti-fabrication guardrails** (skip sections/badges when data is empty)
    - `readme-wizard/SKILL.md` (lines 26, 48)

> For the merged skill: expose three modes (generate/audit/update), a
> decision-tree router, optional interview, and parallel sub-agent scanning for
> speed. Keep auto-push and CI handoff as optional integrations.

---

## 12. Standards & specification compliance

- **Standard Readme spec** (16-item section order, banner rules, License last, conditional TOC, compliance badge)
    - `standard-readme/SKILL.md` (lines 26-196)
    - `crafting-effective-readmes/references/standard-readme-spec.md` + minimal/maximal examples
- **Prescribed section-order structure** (12-section ordering, required/optional)
    - `accelint-readme-writer/references/readme-structure.md`
- **Organization house style** (fixed template, enforced section order, centered header, house tagline)
    - `zr-readme/SKILL.md` (lines 14-63); `zr-readme/assets/readme-template.md`
- **Multi-format output** (Plain text / Markdown / RST for PyPI) — _partially in scope_
    - `pypi-readme-creator/SKILL.md` (lines 25-70)

> For the merged skill: support an optional "spec mode" (Standard Readme) and
> configurable house-style templates. RST/PyPI output is a niche add-on.

---

## Feature × skill matrix

Legend: ● primary strength · ○ present. Edge-case skills marked in the last section.

| Cluster                  | Key skills                                                                                                                                        |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Codebase scanning     | ● readme-wizard, repository-readme-writer, accelint-readme-writer, update-readme ○ configure-readme, make-readme, readme-blueprint-generator      |
| 2. Type awareness        | ● github-readme, readme-creator ○ crafting-effective-readmes, write-readme, configure-readme                                                      |
| 3. Templates/sections    | ● crafting-readme-files, readme-craft, readme-generator ○ create-github-readme, readme-creator, write-readme, diataxis-gen-readme                 |
| 4. Badges                | ● readme-badger ○ configure-readme, github-readme, make-readme, readme-generator                                                                  |
| 5. Visuals/diagrams      | ● create-github-readme, generate-readme-screenshots, readme-wizard ○ crafting-readme-files, configure-readme, write-readme                        |
| 6. Update/sync           | ● update-readme, sc-readme, readme-updater ○ accelint-readme-writer, github-readme, indexion-readme, readme-sync, prowler-readme-table            |
| 7. Audit/scoring         | ● github-readme, readme, readme-creator ○ configure-readme, standard-readme, repository-readme-writer                                             |
| 8. Writing/humanizing    | ● humanize-readme, readme-writer ○ accelint-readme-writer, write-readme, create-readme                                                            |
| 9. Security/agent-safe   | ● github-readme ○ create-github-readme, repository-readme-writer                                                                                  |
| 10. Discoverability      | ● github-readme ○ wp-readme-optimizer                                                                                                             |
| 11. Workflow/integration | ● make-readme, github-readme, sc-readme ○ configure-readme, accelint-readme-writer, update-readme, repository-readme-writer, create-github-readme |
| 12. Standards/specs      | ● standard-readme ○ accelint-readme-writer, zr-readme, crafting-effective-readmes, pypi-readme-creator                                            |

---

## Out-of-scope / edge-case skills

Flagged so their ideas can be borrowed selectively without warping the core
merged skill (general `README.md` generate + update).

- **readme-com** — integrates with the **readme.com documentation-hosting SaaS**
  (Projects/Docs/Categories via Membrane CLI), _not_ `README.md` files. Fully
  out of scope. `readme-com/SKILL.md` (lines 15-35)
- **wp-readme-optimizer** — targets the **WordPress.org plugin `readme.txt`**
  format (`=== ===` syntax, Stable tag, WP search SEO). Borrow: SEO/keyword,
  scoring-audit, caption-SEO ideas. `wp-readme-optimizer/SKILL.md`,
  `wp-readme-optimizer/AGENTS.md`
- **pypi-readme-creator** — Markdown/**RST**/PyPI-specific output, `twine check`,
  Sphinx roles, `pyproject.toml readme` field. In scope only if RST/PyPI output
  is a goal; otherwise a niche add-on. `pypi-readme-creator/SKILL.md`
- **generate-readme-screenshots** — regenerates **image assets** from Storybook
  (Playwright + Sharp + Chromatic), not README prose. Borrow: screenshot
  pipeline ideas. `generate-readme-screenshots/SKILL.md`
- **prowler-readme-table** — updates **one specific table** ("Prowler at a
  Glance") from CLI stats. Narrow maintenance automation. Borrow: safe
  in-place-table-update + no-auto-commit guardrails. `prowler-readme-table/SKILL.md`
- **readme-sync** — regenerates a **skills table** from the filesystem. Narrow
  maintenance automation. Borrow: section-in-place replacement + count syncing.
  `readme-sync/SKILL.md`
- **indexion-readme** — **build-tool-oriented** assembly/verification (`doc.json`,
  `plan drift`, template placeholders, per-package generation). Borrow:
  drift-verification / additive-edit guard for the updater. `indexion-readme/SKILL.md`
- **zr-readme** — **single-organization house style** (zenon-red). Borrow:
  configurable house-style template concept. `zr-readme/SKILL.md`
- **diataxis-gen-readme** — generates only the **README introduction**, not the
  full file. Borrow: the 4-paragraph intro pattern. `diataxis-gen-readme/SKILL.md`
- **generate-readme** — thin **router** skill; actual prompt externalized to
  `../generate-readme.json` (outside the vendored dir). Little reusable content.
  `generate-readme/SKILL.md`
