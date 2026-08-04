# TODO.ability — Code Quality Review

_Scope: the first-party `readme-generator` skill — `SKILL.md`, `scripts/scan_project.py`, `templates/**`, `references/section-library.md`, `DEPENDENCIES.md`, `references.txt`, `.gitignore`. Excludes the gitignored vendored corpus under `references/vendor/**` (design references, not shipped) and `CLUSTERED_FEATURES.md` (build-source inventory). Looked just outside scope at the repo `AGENTS.md` for project conventions._
_Last reviewed: 2026-08-04 10:11_

## Summary

| Ability          | 5 Crit | 4 Maj | 3 Mod | 2 Min | 1 Nag |
| ---------------- | ------ | ----- | ----- | ----- | ----- |
| Accessibility    | 0      | 0     | 1     | 1     | 0     |
| Documentation    | 0      | 0     | 1     | 1     | 1     |
| Maintainability  | 0      | 0     | 1     | 1     | 0     |
| Interpretability | 0      | 0     | 0     | 1     | 0     |
| Interoperability | 0      | 0     | 1     | 0     | 0     |
| Reusability      | 0      | 0     | 0     | 1     | 0     |
| Sustainability   | 0      | 1     | 1     | 0     | 0     |
| Cohesion         | 0      | 1     | 0     | 1     | 0     |

## Accessibility

- [ ] **[S3] Skill entry point does not state its own toolchain preconditions up front** — `SKILL.md:36`
      Why it matters: Step 1a tells the agent to run `python3 scripts/scan_project.py <project-dir>` as the very first action, but the four hard prerequisites (`tree`, `scc`, `licensee`, Python ≥ 3.11) live only in `DEPENDENCIES.md`, which the step never links. A first-time operator whose environment is missing `licensee` gets a JSON `{"error": ...}` and exit 1 with no pointer to how to fix it from the place they started.
      Suggested fix: Add a one-line "Prerequisites: see `DEPENDENCIES.md` (`tree`, `scc`, `licensee`, Python ≥ 3.11)" note directly under the Step 1a code block, and have the error path already references `DEPENDENCIES.md` in its message (it does — surface that link in the doc too).

- [ ] **[S2] `pybadges` install/interpreter caveat is discoverable only by reading to the end of `DEPENDENCIES.md`** — `SKILL.md:333`
      Why it matters: Step 4 calls `pybadges` a hard dependency and links `DEPENDENCIES.md`, but the load-time crash on Python 3.13+ (see Sustainability S4) is only in the last bullet of that file. An operator on a modern default Python will hit an opaque `imghdr` ImportError mid-run.
      Suggested fix: In Step 4's intro paragraph, add "on Python 3.13+ install `standard-imghdr` or run under 3.11/3.12" inline where `pybadges` is first named.

## Documentation

- [ ] **[S3] `scan_project.py` module docstring and `DEPENDENCIES.md` disagree on why `scc` is required** — `scripts/scan_project.py:16` and `DEPENDENCIES.md:9`
      Why it matters: The docstring says `scc` counts "code-line counting" generally, while `DEPENDENCIES.md` scopes it to "code-line counting for existing READMEs." In the code, `line_count()` is called **only** for `existing_readmes` (`scan_project.py:697`). A maintainer reading the docstring will overestimate how much of the scan depends on `scc` and may hesitate to touch it. See also Sustainability S3.
      Suggested fix: Make the docstring match reality — `scc` is used solely to report line counts of any pre-existing README; nothing else needs it.

- [ ] **[S2] `git.default_branch` is documented as feeding output it never reaches** — `SKILL.md:46`
      Why it matters: The Step 1a field table lists `git.default_branch` as feeding "clone command, links," but no template or SKILL step consumes it — every template hardcodes `main` / `blob/main` (`templates/monorepo.md:31`, `SKILL.md:381`). The doc promises a data flow that does not exist. See Maintainability S3.
      Suggested fix: Either wire `default_branch` into the clone/link tokens, or drop it from the "Feeds" column and note it as informational-only.

- [ ] **[S1] Section-library TOC anchors use double-hyphen slugs that may not match GitHub's slugger** — `references/section-library.md:17`
      Why it matters: Entries like `[Comparison / Alternatives](#comparison--alternatives)` assume a specific slug for `/`. If rendered on GitHub the anchor could 404, a cosmetic nav annoyance in an internal reference file.
      Suggested fix: Verify the generated anchors against GitHub's rules (drop `/`, collapse spaces to single hyphens) or generate the TOC with a tool.

## Maintainability

- [ ] **[S3] `default_branch` is computed but never consumed — dead output field** — `scripts/scan_project.py:396`
      Why it matters: `detect_git` runs an extra `git symbolic-ref` subprocess to populate `default_branch`, but nothing downstream reads it (templates hardcode `main`). Dead facts invite drift: a maintainer may "fix" branch handling in one place and miss that the field is inert, or waste effort wiring a value that turns out unused.
      Suggested fix: Consume it (feed clone/link tokens in the templates) or remove the field and its subprocess to keep the scan output honest about what it drives.

- [ ] **[S2] Three near-identical tool version-check functions duplicate ~30 lines each** — `scripts/scan_project.py:433`
      Why it matters: `check_tree`, `check_scc`, and `check_licensee` (`:433`, `:466`, `:499`) differ only in the binary name, version subcommand, regex, and minimum tuple. The triplication means a fix to the "too old" message or the FileNotFoundError wording must be made three times, and it is easy to update two and forget one.
      Suggested fix: Extract a single `check_tool(cmd, version_args, version_regex, min_version, name)` helper and call it three times with a small config table.

## Interpretability

- [ ] **[S2] `line_count` name understates that it shells out to `scc` and returns 0 on skip** — `scripts/scan_project.py:591`
      Why it matters: A reader sees `line_count(path)` and reasonably expects a cheap line tally; it actually spawns `scc --by-file -f json` with a 30s timeout and silently returns 0 for gitignored files (`DEPENDENCIES.md:25`). The gap between the name and the behavior (a 0 that means "skipped," not "empty file") can mislead anyone debugging why an existing README shows 0 lines.
      Suggested fix: Rename to `scc_code_lines` (or similar) and add a one-line comment at the call site (`:697`) noting that gitignored READMEs legitimately report 0.

## Interoperability

- [ ] **[S3] License detection depends solely on `licensee`, with no manifest fallback** — `scripts/scan_project.py:293`
      Why it matters: `detect_license` returns `""` whenever `licensee` yields `NOASSERTION` or fails, even though the SKILL field table promises license "detected from `LICENSE*` text **or manifest**" (`SKILL.md:45`). Manifests routinely carry an SPDX `license` field (`package.json`, `[project].license`, `Cargo.toml`) that would resolve the many cases `licensee` marks `NOASSERTION`; not reading them makes the tool interoperate worse with standard package metadata than it claims to.
      Suggested fix: Add a manifest-based fallback in `detect_license` (read the `license`/`license.text`/`classifiers` fields already parsed by `extract_metadata`) when `licensee` returns empty, matching the documented behavior.

## Reusability

- [ ] **[S2] Version-check helpers hardcode their subprocess invocation, blocking reuse of the parse logic** — `scripts/scan_project.py:433`
      Why it matters: The "parse `vX.Y.Z`, compare to a minimum tuple" logic is genuinely reusable, but it is welded to `subprocess.run` and to per-tool version subcommands, so nothing can reuse the comparison without also running the process. Combined with the triplication (Maintainability S2), the useful part cannot be lifted out.
      Suggested fix: Split a pure `parse_version(text) -> tuple | None` and `at_least(version, minimum)` from the I/O, so the comparison is testable and reusable independent of shelling out.

## Sustainability

- [ ] **[S4] `pybadges` — a declared hard dependency — crashes on load under Python 3.13+ (this host runs 3.14.6)** — `DEPENDENCIES.md:34`
      Why it matters: Step 4 makes `pybadges` ≥ 3.0.1 a hard dependency, but it imports the stdlib `imghdr` removed in Python 3.13, so it raises `ImportError` on _any_ invocation on 3.13+. `DEPENDENCIES.md:11` simultaneously pins the scanner to Python ≥ 3.11 with no upper bound, and the local interpreter is 3.14.6 — meaning the default, documented environment cannot generate badges at all without an undocumented-at-point-of-use shim. This will bite every operator on a current Python and is a near-term breakage of a shipped feature.
      Suggested fix: Either declare a supported Python band for the badge step (3.11–3.12), add `standard-imghdr` to the required install for 3.13+, or replace `pybadges` with a maintained badge renderer. Surface the constraint in Step 4 (see Accessibility S2), not just the last bullet of `DEPENDENCIES.md`.

- [ ] **[S3] `scc` is a hard dependency solely to line-count pre-existing READMEs** — `scripts/scan_project.py:596` and `DEPENDENCIES.md:9`
      Why it matters: `scc` gates the entire scan (`check_scc` aborts with exit 1 if missing) but its only consumer is `line_count`, used just for the `existing_readmes[].line_count` field (`:697`) — a minor, informational number. Making a whole external toolchain dependency mandatory for one cosmetic field raises the cost of ownership and the odds the scanner refuses to run on otherwise-fine environments.
      Suggested fix: Downgrade `scc` to optional — degrade `line_count` to `0`/`null` (or a stdlib line count) when `scc` is absent, and move it out of the hard `check_tree() or check_scc() or check_licensee()` gate at `:718`.

## Cohesion

- [ ] **[S4] Type templates emit shields.io badge URLs, directly contradicting Step 4's pybadges-only mandate** — `templates/cli.md:25`, `templates/library.md:24`, `templates/framework.md:25`
      Why it matters: SKILL.md Step 4 states badges are "generated as static local SVG files with `pybadges` ... referenced by relative path — **not** hosted shields.io URLs" (`SKILL.md:329`, guardrail `:424`), yet three of the seven skeletons hardcode `https://img.shields.io/...` `<img>`/badge markup. An agent that fills a template verbatim ships exactly the third-party runtime-fetch badges the skill claims to have migrated away from — a parallel, incompatible implementation of a core feature within the same skill.
      Suggested fix: Replace the shields.io `<img>`/badge lines in `cli.md`, `library.md`, and `framework.md` with the pybadges relative-path form from `SKILL.md:406` (`[![License](./assets/badges/license.svg)](./LICENSE)`), or leave a `<!-- badges: generated in Step 4 -->` placeholder so the templates stop competing with Step 4.

- [ ] **[S2] Only 3 of 7 templates carry a badge slot, with no rule for the other 4** — `templates/monorepo.md:24`
      Why it matters: `cli`, `library`, and `framework` include badge markup; `monorepo`, `application`, `collection`, and `personal` omit it. That matches the Step 2 matrix intent (no badges for monorepo/personal), but the templates encode the policy silently and inconsistently — a maintainer adding badges to `application` has no in-template signal that badges were deliberately excluded there.
      Suggested fix: Add a short HTML comment at the badge slot in each template stating the Step 2 badge policy for that type (e.g. `<!-- No badges for monorepo: no registry presence (Step 2b) -->`), so the omission reads as intentional.

## Review log

- 2026-08-04 10:11 — initial review of the first-party `readme-generator` skill (SKILL.md, scan_project.py, templates/, section-library.md, DEPENDENCIES.md, references.txt); vendored corpus excluded. 12 findings (0 crit, 2 major, 5 moderate, 5 minor/nag). Verified scanner compiles and runs (exit 0) with `tree` 2.3.2 / `scc` 3.7.0 / `licensee` 10.0.0 present; confirmed local Python is 3.14.6 (pybadges/imghdr risk is live).
