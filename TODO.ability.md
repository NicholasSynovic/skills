# TODO.ability — Code Quality Review

_Scope: whole-repo, **first-party only** — repo-root config (Makefile,
.gitignore, .pre-commit-config.yaml, README.md, AGENTS.md), the `review-abilities/`
skill, and repo-wide/build/packaging concerns for `readme-generator/`. The
`readme-generator/` skill internals (SKILL.md, scan_project.py, templates/,
DEPENDENCIES.md) have their own deeper review in
`readme-generator/TODO.ability.md` — findings there are not duplicated here;
this file adds only repo-level and `review-abilities/` findings. Excludes
`readme-generator/references/vendor/**` (vendored third-party skills)._
_Last reviewed: 2026-08-04 08:30_

## Summary

| Ability          | 5 Crit | 4 Maj | 3 Mod | 2 Min | 1 Nag |
| ---------------- | ------ | ----- | ----- | ----- | ----- |
| Accessibility    | 0      | 0     | 1     | 1     | 0     |
| Documentation    | 0      | 1     | 1     | 0     | 0     |
| Maintainability  | 0      | 1     | 1     | 0     | 0     |
| Interpretability | 0      | 0     | 0     | 0     | 0     |
| Interoperability | 0      | 0     | 1     | 0     | 0     |
| Reusability      | 0      | 0     | 0     | 1     | 0     |
| Sustainability   | 0      | 1     | 1     | 0     | 0     |
| Cohesion         | 0      | 1     | 1     | 1     | 0     |

## Accessibility

- [ ] **[S3] Root `README.md` is empty; the repo has no "start here"** — `README.md:1`
      Why it matters: The root README is 0 bytes. Everything a newcomer needs
      (first-party vs vendored, the two skills, the build flow) lives only in
      `AGENTS.md`, which is agent-facing. A human landing on the repo has no map.
      Suggested fix: Add a short root README pointing at the two skills, the
      `make build` flow, and `AGENTS.md` for contributor rules.

- [ ] **[S2] `make build` is undocumented outside the Makefile itself** — `Makefile:1`
      Why it matters: The only way to discover the packaging step (`make build` →
      `build/*.skill` zips) is to open the Makefile. Neither `AGENTS.md` nor any
      README mentions it, so an agent asked to "build/package the skills" would
      guess.
      Suggested fix: Document `make build` and its `build/*.skill` outputs in
      `AGENTS.md` (Toolchain section) and/or the root README.

## Documentation

- [ ] **[S4] `AGENTS.md` is stale re: build flow and Python version after recent changes** — `AGENTS.md:41`
      Why it matters: `AGENTS.md:41` states "There is no Makefile/pyproject," but a
      `Makefile` with a `build` target now exists. AGENTS.md is the primary
      instruction file; a factually wrong opening claim in its Toolchain section
      misleads every future session. (The Python-version line was corrected this
      session, but the Makefile claim was missed.)
      Suggested fix: Update the Toolchain section to acknowledge the Makefile and
      the `make build` packaging step; re-audit AGENTS.md against the current tree.

- [ ] **[S3] `review-abilities/SKILL.md` never states where `references/rubric.md` output/scope files land relative to a scanned target** — `review-abilities/SKILL.md:92`
      Why it matters: The skill tells the agent to write `TODO.ability.md` "at the
      root of the reviewed target," but gives no guidance for the whole-repo case
      where a per-directory `TODO.ability.md` may already exist (as here), risking
      duplicate/competing files. This review had to invent a reconciliation policy.
      Suggested fix: Add a sentence on nested reviews — e.g. a broader review
      references narrower `TODO.ability.md` files rather than duplicating them.

## Maintainability

- [ ] **[S4] `make build` uses `zip -r` without removing the old archive — stale/deleted files persist** — `Makefile:4`
      Why it matters: `zip -r build/x.skill dir` (Makefile:4-6) _appends_ to an
      existing zip. `build/` is gitignored and there is no `clean` target, so files
      deleted or renamed between builds remain inside the shipped `.skill` bundle.
      A packaged skill can therefore contain removed source, silently.
      Suggested fix: `rm -f build/*.skill` before zipping (or `cd` + `zip` fresh),
      and add a `clean` target: `clean: rm -rf build`.

- [ ] **[S3] No CI runs pre-commit; correctness relies on the author remembering** — `.pre-commit-config.yaml:1`
      Why it matters: `AGENTS.md` calls pre-commit "the source of truth," but there
      is no `.github/workflows/` or other CI to enforce it. A contributor without
      the hooks installed can push unformatted/unlinted content, and the
      first-party Python (`scan_project.py`) has no automated check gate.
      Suggested fix: Add a minimal CI workflow running `pre-commit run --all-files`
      (and, once tests exist, the scanner test suite) on PRs.

## Interpretability

_No findings._ (Root config and `review-abilities/` prose are clear and readable;
scanner-internal interpretability findings are in `readme-generator/TODO.ability.md`.)

## Interoperability

- [ ] **[S3] `make build` zips will include OS/editor cruft and (for readme-generator) the vendored corpus** — `Makefile:5`
      Why it matters: `zip -r ... readme-generator` does not honor `.gitignore`, so
      the 1.3 MB `references/vendor/**` (which SKILL.md/AGENTS.md say is _not_ part
      of the shipped skill) and any `.DS_Store`/`__pycache__` get packaged into the
      distributable `.skill`. The resulting artifact is bloated and ships content
      the project explicitly excludes. (Observed: `build/readme-generator.skill` is
      1.3 MB vs `review-abilities.skill` at 7.6 KB.)
      Suggested fix: Exclude vendored/generated paths in the zip
      (`zip -r ... -x 'readme-generator/references/vendor/*' '*/__pycache__/*' '*.DS_Store'`)
      or build from a `git archive` so `.gitignore` is honored.

## Reusability

- [ ] **[S2] Rubric and output format are duplicated between the skill body and its injected copy** — `review-abilities/SKILL.md:96`
      Why it matters: The eight-ability definitions and the exact output template
      live both in `SKILL.md` and (in expanded form) in `references/rubric.md`.
      Keeping severity anchors consistent across runs depends on the two staying in
      sync; drift between them would produce inconsistent reviews.
      Suggested fix: Make `SKILL.md` the one-line summary and let `references/rubric.md`
      own the authoritative definitions (the skill already points there) — avoid
      restating full anchors in both.

## Sustainability

- [ ] **[S4] Vendored corpus is gitignored, so every `references/vendor/...` citation is unverifiable on a fresh clone** — `readme-generator/.gitignore:1`
      Why it matters: `readme-generator/.gitignore:1` ignores `references/vendor`
      (confirmed: `git ls-files readme-generator/references/` returns only
      `section-library.md`). SKILL.md cites `references/vendor/<skill>/file (lines
X-Y)` as authoritative design sources throughout, and AGENTS.md says to "trust
      the lockfile + `references/vendor/`" — but neither the corpus nor a
      `skills-lock.json` is committed. A fresh clone cannot verify a single citation
      or reproduce the corpus; the design rationale is effectively lost to everyone
      but the original author's machine.
      Suggested fix: Commit a `skills-lock.json` (the `skills` CLI lockfile) so the
      corpus is reproducible via `npx skills add`, and/or document the exact restore
      command in `AGENTS.md`. If the corpus must stay out of git, make its
      reproducibility a first-class, documented step.

- [ ] **[S3] `.pre-commit-config.yaml` pins `python3.14`, the newest release, with no fallback** — `.pre-commit-config.yaml:2`
      Why it matters: Pinning the language to the latest major (`python3.14`) means
      any contributor without exactly 3.14 on PATH cannot run the hooks, and it
      collides with the documented `pybadges`/`imghdr` breakage on 3.13+ (see
      `readme-generator/TODO.ability.md` Sustainability). The pin maximizes churn
      for little benefit — `scan_project.py` only needs ≥3.11.
      Suggested fix: Relax the pin to a widely-installed floor (e.g. `python3.11`)
      unless a 3.14-only feature is actually used; document the required interpreter
      in `AGENTS.md`.

## Cohesion

- [ ] **[S4] Skill `name` frontmatter is misspelled and mismatches the directory** — `review-abilities/SKILL.md:2`
      Why it matters: `SKILL.md:2` declares `name: review-abilites` (missing the
      second `i`), but the directory is `review-abilities/` and the Makefile packages
      `review-abilities.skill`. A name/dir/artifact mismatch can break skill
      resolution and tooling that keys on the declared name, and it contradicts the
      recent "fix spelling mistake" commit that renamed the directory.
      Suggested fix: Set `name: review-abilities` in the frontmatter to match the
      directory and the build artifact.

- [ ] **[S3] Two divergent copies of the feature inventory remain in the repo** — `FutureReadmeSkills.md:1`
      Why it matters: `FutureReadmeSkills.md` (repo root) and
      `readme-generator/CLUSTERED_FEATURES.md` are near-identical feature inventories
      that differ only in the badge cluster (root copy has stale, unresolved
      pybadges TODOs). AGENTS.md flags this, but the stale duplicate still sits at
      the repo root where it is the more prominent of the two, inviting edits to the
      wrong file.
      Suggested fix: Delete `FutureReadmeSkills.md` (or replace it with a one-line
      stub pointing at `readme-generator/CLUSTERED_FEATURES.md`) now that the badge
      migration is resolved.

- [ ] **[S2] Root `.gitignore` `references/*` rule is broader than intended and overlaps the skill-local ignore** — `.gitignore:1`
      Why it matters: The root `.gitignore:1` ignores `references/*` globally, which
      matches `readme-generator/references/*` as well; only the already-tracked
      `section-library.md` survives. The intent (ignore the vendored corpus) is
      already served by `readme-generator/.gitignore`. The broad root rule risks
      silently ignoring future first-party `references/*.md` files (like
      section-library) that _should_ be tracked.
      Suggested fix: Scope the root ignore to the vendored path
      (`readme-generator/references/vendor/`) instead of the blanket `references/*`,
      keeping first-party `references/*.md` trackable by default.

## Review log

- 2026-08-04 08:30 — whole-repo first-party review (readme-generator/ internals
  covered separately in readme-generator/TODO.ability.md). 11 new findings:
  4 major, 5 moderate, 2 minor. Notable: Makefile `zip` append bug + vendored
  corpus packaged into .skill; vendored corpus gitignored (citations
  unverifiable); review-abilities skill name misspelled; AGENTS.md "no Makefile"
  claim now stale. No prior root TODO.ability.md existed.
