# TODO.ability — Code Quality Review

_Scope: `readme-generator/` first-party skill (SKILL.md, scripts/scan_project.py,
templates/, references/section-library.md, DEPENDENCIES.md, CLUSTERED_FEATURES.md).
Excludes `references/vendor/**` (vendored third-party skills). Cohesion/interop
judged against repo-root config: .pre-commit-config.yaml, AGENTS.md._
_Last reviewed: 2026-08-04 08:20_

## Summary

| Ability          | 5 Crit | 4 Maj | 3 Mod | 2 Min | 1 Nag |
| ---------------- | ------ | ----- | ----- | ----- | ----- |
| Accessibility    | 0      | 0     | 1     | 1     | 0     |
| Documentation    | 0      | 0     | 1     | 1     | 0     |
| Maintainability  | 0      | 0     | 2     | 1     | 0     |
| Interpretability | 0      | 0     | 0     | 1     | 0     |
| Interoperability | 0      | 0     | 1     | 0     | 0     |
| Reusability      | 0      | 0     | 0     | 1     | 0     |
| Sustainability   | 0      | 1     | 0     | 1     | 0     |
| Cohesion         | 0      | 1     | 1     | 0     | 0     |

## Accessibility

- [ ] **[S3] No top-level README for the skill; entry point is implicit** — `readme-generator/`
      Why it matters: The directory has no `README.md`. A newcomer must infer that
      `SKILL.md` is the entry point and that `CLUSTERED_FEATURES.md` is the build
      source vs. `FutureReadmeSkills.md` (a stale root duplicate). All of this
      lives only in the repo-root `AGENTS.md`; someone landing in this subdir first
      has no "start here". (Ironic for a README-generator.)
      Suggested fix: Add a short `readme-generator/README.md` (or a header block in
      SKILL.md) naming the entry point, the scanner invocation, and the
      CLUSTERED_FEATURES-vs-FutureReadmeSkills distinction.

- [ ] **[S2] Setup/install steps for the hard dependencies are not one command** — `readme-generator/DEPENDENCIES.md:6`
      Why it matters: `tree`, `scc`, `licensee`, and `pybadges` are hard
      requirements, but the doc lists them as a table with no copy-paste install
      line (e.g. brew/apt/gem/pip). A new user assembles the install by hand.
      Suggested fix: Add a "Quick install" block with per-platform commands, e.g.
      `brew install tree scc; gem install licensee; pip install pybadges standard-imghdr`.

## Documentation

- [ ] **[S3] `pybadges` version-check command in DEPENDENCIES.md is wrong** — `readme-generator/DEPENDENCIES.md:12`
      Why it matters: The check command is `python3 -m pybadges -v`, but `pybadges`
      has no `-v`/version flag — and on Python 3.13+ it raises `ModuleNotFoundError:
imghdr` on _any_ invocation (documented four lines below at :34). A user
      following the check command gets a crash, not a version, contradicting the
      table's own purpose.
      Suggested fix: Replace with a working probe (e.g.
      `python3 -c "import pybadges; print(pybadges.__version__)"`) and cross-note the
      `standard-imghdr` requirement inline in the check column.

- [ ] **[S2] Scanner docstring omits the offline `pybadges`/imghdr operational caveat** — `readme-generator/scripts/scan_project.py:12`
      Why it matters: The module docstring lists tree/scc/licensee/Python deps but
      not that the _skill's_ Step 4 needs `pybadges` (and `standard-imghdr` on
      3.13+). A maintainer reading only the script won't learn the runtime gotcha
      that AGENTS.md and DEPENDENCIES.md both flag.
      Suggested fix: Add a one-line pointer in the docstring to DEPENDENCIES.md for
      badge-generation deps, or state that this script itself has no pybadges dep.

## Maintainability

- [ ] **[S3] 738-line script with many parsers/subprocess integrations has no tests** — `readme-generator/scripts/scan_project.py:1`
      Why it matters: The scanner shells out to `tree`/`scc`/`licensee`/`git`,
      parses TOML/JSON/go.mod, and has version-regex logic and a hand-rolled TOML
      fallback (`_fallback_toml`, :173). AGENTS.md states "there is no test suite";
      verification is manual `py_compile` + a live run. Regressions in parsing or
      the "never crash" contract can ship silently.
      Suggested fix: Add a small `pytest` suite with fixture project dirs (a
      package.json project, a pyproject project, a go.mod project, an empty dir) and
      assert the JSON shape and graceful-degradation behavior. Mock or gate the
      external-tool paths.

- [ ] **[S3] Three version checkers are near-identical copy-paste** — `readme-generator/scripts/scan_project.py:433`
      Why it matters: `check_tree` (:433), `check_scc` (:466), and `check_licensee`
      (:499) differ only in the binary name, version-arg, regex, and minimum tuple.
      ~30 duplicated lines each; a fix to the error-handling contract must be made in
      three places (and kept in sync with the regexes, which already differ subtly).
      Suggested fix: Extract one `check_tool(name, version_args, regex, min_version)`
      helper and call it three times.

- [ ] **[S2] `load_toml` swallows all parse errors as `{}` via bare `except Exception`** — `readme-generator/scripts/scan_project.py:168`
      Why it matters: A malformed `pyproject.toml` yields empty metadata
      indistinguishable from "no metadata", so the README silently loses the real
      name/version/description with no signal to the agent. This is intentional
      (never-crash design) but the total-silence loses recoverable information.
      Suggested fix: Keep the non-crashing behavior but narrow to
      `tomllib.TOMLDecodeError` and surface a soft warning field (e.g. a
      `warnings: []` key in the output) so the agent knows a manifest failed to parse.

## Interpretability

- [ ] **[S2] `find_named` depth semantics are subtle and under-explained** — `readme-generator/scripts/scan_project.py:205`
      Why it matters: The function both prunes `dirs[:] = []` at `depth >= max_depth`
      (:224) _and_ re-checks `len(candidate.relative_to(root).parts) <= max_depth`
      (:229). The interaction between the walk-pruning and the per-file recheck is
      non-obvious, and callers pass different `max_depth` values (2 vs default 3)
      with no comment on why.
      Suggested fix: Add a short comment explaining the two-layer depth guard and why
      task/sibling-doc scans use `max_depth=2`.

## Interoperability

- [ ] **[S3] Version parsing relies on fragile per-tool regexes against `--version` text** — `readme-generator/scripts/scan_project.py:453`
      Why it matters: `tree` uses `v(\d+)\.(\d+)\.(\d+)` (:453), `scc` uses
      `version\s+(\d+)\.(\d+)\.(\d+)` (:486), `licensee` uses a bare
      `(\d+)\.(\d+)\.(\d+)` (:519). Upstream output-format changes, distro-patched
      version strings, or localized output silently become "could not parse
      version" errors and block the whole scan even when the installed tool is new
      enough. The bare licensee regex could also match an unrelated leading number.
      Suggested fix: Loosen matching (search first semver-looking token) and, on
      parse failure, warn-and-continue rather than hard-fail the dependency gate.

## Reusability

- [ ] **[S2] `MIN_*_VERSION` constants and check logic are baked into the scanner module** — `readme-generator/scripts/scan_project.py:141`
      Why it matters: The dependency-checking machinery (constants at :141-143,
      three checkers, the `check_tree() or check_scc() or ...` gate at :718) is
      generically useful but entangled with this one script's `main`. Reusing the
      "verify external CLI versions" capability elsewhere means copy-paste.
      Suggested fix: If a second script ever needs it, factor the tool-version
      checking into a tiny reusable helper module. Low priority while there is only
      one script.

## Sustainability

- [ ] **[S4] Step 4 (`pybadges`) crashes on the repo's own pinned Python (3.14)** — `readme-generator/DEPENDENCIES.md:34`
      Why it matters: `.pre-commit-config.yaml:2` pins `python3.14` and the local
      interpreter is 3.14.6; `imghdr` was removed in 3.13, so `pybadges` 3.0.1
      (a hard dependency for SKILL.md Step 4) fails to import on the very runtime the
      project standardizes on, unless `standard-imghdr` is installed. A core
      advertised capability (badge generation) is broken out of the box on the
      supported interpreter.
      Suggested fix: Make `standard-imghdr` a listed hard dependency alongside
      `pybadges` for Python ≥3.13 (not just a note), or pin badge generation to run
      under 3.11/3.12, and state the resolution once, authoritatively, in
      DEPENDENCIES.md.

- [ ] **[S2] `bun.lockb` (binary) precedence may mis-detect with the newer text `bun.lock`** — `readme-generator/scripts/scan_project.py:69`
      Why it matters: Bun moved from the binary `bun.lockb` to a text `bun.lock`.
      Both are listed (:69-70) which is good, but ecosystems churn here; the pinned
      lockfile list will drift as package managers change formats, silently
      degrading `package_manager` detection over time.
      Suggested fix: Add a brief comment dating the lockfile list and note it needs
      periodic review; consider a test asserting each manager is detected.

## Cohesion

- [ ] **[S4] Type templates hard-code shields.io badge URLs, contradicting SKILL.md Step 4** — `readme-generator/templates/cli.md:25`
      Why it matters: `cli.md:25-26`, `library.md:24-25`, and `framework.md:25-26`
      embed live `https://img.shields.io/...` badge URLs. SKILL.md Step 4
      (:329-338) mandates static local `pybadges` SVGs committed and referenced by
      relative path, and explicitly states "shields.io URL syntax ... no longer
      apply." These are exactly the three types whose Step 2 matrix marks Badges as
      **Required**, so the default path an agent follows produces the wrong,
      deprecated badge style — a parallel, incompatible implementation of a
      just-migrated subsystem.
      Suggested fix: Replace the shields.io `<img>`/`![]()` blocks in cli.md,
      library.md, and framework.md with the relative-path `pybadges` SVG pattern
      from SKILL.md Step 4e (`[![License](./assets/badges/license.svg)](./LICENSE)`),
      or a `{{badges}}` placeholder the Step 4 procedure fills.

- [ ] **[S3] SKILL.md header claims generation-only scope, but Step 3 and CLUSTERED_FEATURES reference a "Step 6" updater** — `readme-generator/SKILL.md:22`
      Why it matters: The header comment (:22) says "audit/update modes are not
      implemented here," yet Step 3's guardrail cites "the audit step's render-check"
      (:313-314) and Step 4e/CLUSTERED_FEATURES refer to a Step 6 updater that does
      not exist in SKILL.md. A reader can't tell whether the audit/update flow is
      in-scope, planned, or dropped.
      Suggested fix: Reconcile the references — either scope the render-check as a
      manual pre-ship check owned by the generator, or explicitly mark the
      audit/update mode as future work in one place and stop citing it as if present.

## Review log

- 2026-08-04 08:20 — initial review of readme-generator/ (first-party only;
  vendored excluded). 12 findings: 2 major, 6 moderate, 4 minor. Scanner verified
  to compile and run (Python 3.14.6, all external deps present). No prior
  TODO.ability.md existed.
