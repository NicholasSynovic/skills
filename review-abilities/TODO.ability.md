# TODO.ability — Code Quality Review

_Scope: the `review-abilities` skill — `SKILL.md` and `references/rubric.md` (read fully). Looked outside scope at sibling `readme-generator/` skill, repo `Makefile`, `AGENTS.md`, and `.pre-commit-config.yaml` to judge cohesion and interoperability._
_Last reviewed: 2026-08-04 10:10_

## Summary

| Ability          | 5 Crit | 4 Maj | 3 Mod | 2 Min | 1 Nag |
| ---------------- | ------ | ----- | ----- | ----- | ----- |
| Accessibility    | 0      | 0     | 0     | 0     | 0     |
| Documentation    | 0      | 0     | 2     | 1     | 0     |
| Maintainability  | 0      | 0     | 1     | 0     | 0     |
| Interpretability | 0      | 0     | 1     | 1     | 0     |
| Interoperability | 0      | 0     | 0     | 1     | 0     |
| Reusability      | 0      | 0     | 0     | 1     | 0     |
| Sustainability   | 0      | 0     | 0     | 0     | 1     |
| Cohesion         | 0      | 0     | 1     | 1     | 0     |

## Accessibility

_No findings._

The skill is self-contained: `SKILL.md` states its purpose, the full procedure,
and a copy-paste output template, and it points to `references/rubric.md` for
detail. A reader can start and run it with no hidden prerequisites.

## Documentation

- [ ] **[S3] "The eight abilities" section promises one-line summaries but has none** — `SKILL.md:32-36`
      Why it matters: The heading says "One-line summaries below," then the very
      next line jumps to the Severity scale. A reader who does not open the rubric
      never gets even a one-line gloss of the eight abilities, defeating the
      section's stated purpose and forcing a file jump for the skill's core
      vocabulary.
      Suggested fix: Add the eight one-liners (name + a single clause each) under
      that heading, or change the sentence to say the summaries live only in the
      rubric.

- [ ] **[S3] Output-location rule is stated two different ways** — `SKILL.md:72-74` vs `SKILL.md:78`
      Why it matters: Step 3 says write the file "at the **root of the reviewed
      target** ... **or** in the current working directory," while the Output
      section (line 78) says unconditionally "Write to the root of the reviewed
      target." The `or ... current working directory` escape hatch has no
      condition attached, so the reviewer cannot tell when to use it; two runs on
      the same target could put the file in different places.
      Suggested fix: State one primary location and an explicit fallback
      condition, e.g. "write to the root of the reviewed target; if that
      location is not writable, fall back to the current working directory,"
      and make lines 72-74 and 78 agree.

- [ ] **[S2] No guidance on how to obtain the `Last reviewed` timestamp** — `SKILL.md:84`
      Why it matters: The template requires a real `YYYY-MM-DD HH:MM` timestamp,
      but nothing tells the reviewer to read the actual current time rather than
      guess it. An agent may invent a plausible-but-wrong date, which corrupts
      the review-log history that the re-run section (lines 120-134) depends on.
      Suggested fix: Add a one-line instruction in step 3 to obtain the current
      date/time from the system (e.g. `date`) rather than estimating it.

## Maintainability

- [ ] **[S3] Severity scale and its anchors are duplicated across two files** — `SKILL.md:38-51` and `references/rubric.md:11-17`
      Why it matters: The 1–5 severity definitions appear both in `SKILL.md` and
      near-verbatim in `rubric.md`. When one wording is refined (e.g. tightening
      the "Critical" definition) the other silently drifts, and there is no test
      suite to catch the divergence — exactly the maintenance trap the skill
      itself scores against other projects.
      Suggested fix: Keep the authoritative scale in one place (the rubric) and
      have `SKILL.md` give a brief pointer, or add a note marking one copy as the
      canonical source so future edits update both deliberately.

## Interpretability

- [ ] **[S3] Re-run review-log example wraps mid-string and is hard to read** — `SKILL.md:131-134`
      Why it matters: The example log line breaks across lines 132-134 with the
      continuation `1 resolved.` dedented to column 0, so on its face it reads as
      a stray fragment rather than part of the backticked example. A reader
      copying the format may reproduce the broken layout.
      Suggested fix: Reflow the example onto a single logical line, or format it
      as a fenced code block so the wrap is unambiguous.

- [ ] **[S2] "Ability" column vs "eight abilities" naming is slightly opaque** — `SKILL.md:66-70`
      Why it matters: Step 2 says "Evaluate each ability" and asks the reviewer to
      "capture ... the ability," but the eight names are never listed in
      `SKILL.md` itself (see the Documentation finding above), so "the ability"
      is an unresolved referent until the rubric is opened.
      Suggested fix: Resolving the missing-summaries finding also fixes this;
      once the eight names appear in `SKILL.md`, "the ability" is self-explaining.

## Interoperability

- [ ] **[S2] Output template mixes a fixed table width with variable-length content** — `SKILL.md:86-97`
      Why it matters: The Summary table is hand-aligned, but the repo's prettier
      hook reflows markdown (`--tab-width 4 --print-width 80`), so a generated
      `TODO.ability.md` that is committed will be re-aligned by pre-commit and may
      differ from the literal template — a minor friction when diffing template
      vs. output.
      Suggested fix: Note in the skill that the emitted file will be
      prettier-normalized on commit, or keep the template's column widths
      prettier-stable so generated files match without reflow.

## Reusability

- [ ] **[S2] The output format spec lives inline in SKILL.md, not in a reusable template file** — `SKILL.md:76-118`
      Why it matters: The sibling `readme-generator` skill factors reusable
      artifacts into `templates/` and `references/`. Here the entire
      `TODO.ability.md` structure is embedded in prose, so another tool or skill
      that wants to emit the same format must scrape it out of `SKILL.md` rather
      than reference a canonical template.
      Suggested fix: Consider extracting the output skeleton to
      `references/output-template.md` and pointing `SKILL.md` at it, mirroring
      `readme-generator`'s `templates/` pattern.

## Sustainability

- [ ] **[S1] No pinned "rubric version" to detect drift between runs** — `references/rubric.md:1-9`
      Why it matters: The rubric header says severities should "stay consistent
      across runs," but there is no version marker, so a re-run after the rubric
      is edited cannot tell that prior findings were scored under different
      anchors. Low impact today (single maintainer, short file) but a cheap
      hedge against future inconsistency.
      Suggested fix: Add a small version/date stamp at the top of `rubric.md` and
      optionally record it in the review-log entry.

## Cohesion

- [ ] **[S3] Skill omits packaging/companion files the sibling skill provides** — `SKILL.md` (whole file); cf. `readme-generator/{DEPENDENCIES.md,templates/,scripts/}`
      Why it matters: `readme-generator` ships `DEPENDENCIES.md`, `templates/`,
      and `scripts/`, and `AGENTS.md` documents both skills as first-party peers.
      `review-abilities` has only `SKILL.md` + `references/rubric.md`. That is
      defensible (it needs no scripts/deps), but the asymmetry is undocumented,
      so a maintainer cannot tell whether files are intentionally absent or
      simply not written yet.
      Suggested fix: Add a one-line note (in `SKILL.md` or `AGENTS.md`) that this
      skill is intentionally script-free and needs no external dependencies, so
      the minimal footprint reads as a decision rather than an omission.

- [ ] **[S2] Base-directory note phrasing differs from how the sibling skill documents paths** — `SKILL.md` (base-dir note appended at load) vs `readme-generator/SKILL.md` header comment
      Why it matters: `readme-generator` tracks build state in an HTML header
      comment; `review-abilities` has no such in-file provenance/status note.
      Minor, but consistency across the two first-party skills helps a maintainer
      navigate both the same way.
      Suggested fix: Optionally add a short header comment to `review-abilities/SKILL.md`
      mirroring the sibling's convention (status / what's implemented).

## Review log

- 2026-08-04 10:10 — Initial review of `review-abilities` skill (`SKILL.md`,
  `references/rubric.md`); 9 findings (0 crit, 0 maj, 5 mod, 5 min, 1 nag). No
  Accessibility findings. No prior `TODO.ability.md` existed.
