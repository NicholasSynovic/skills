# Ability Rubric

**Rubric version: 1 (2026-08-04).** Bump this version and date whenever the
severity anchors or ability definitions below change, and record the version in
each review-log entry so a re-run can tell whether prior findings were scored
under different anchors.

Full definitions and severity anchors for the eight abilities. Read this before
writing findings so severities stay consistent across runs and across projects.

Severity is always about **how bad the finding is**, never how good the code is.
The anchors below describe what a finding at each level typically looks like for
that ability. Use judgment — a finding's real-world impact wins over a literal
keyword match.

General severity meaning:

- **5 Critical** — blocks use or actively breaks something.
- **4 Major** — serious friction/risk; hits soon or affects many.
- **3 Moderate** — real problem worth scheduling; not urgent.
- **2 Minor** — small, low-impact improvement.
- **1 Nag** — cosmetic / nice-to-have.

---

## 1. Accessibility (code approachability)

**Definition.** How easily a person who is not the author can _discover_, _set
up_, _run_, and _begin contributing to_ this code. This is about approachability
of the codebase — not UI/WCAG accessibility.

**Look for:** missing or wrong setup/run instructions; undocumented environment
requirements; hidden prerequisites; no entry point or unclear "start here";
build/install steps that fail or are out of date; secrets/config needed but
undocumented; no license clarity for would-be users; onboarding that assumes
tribal knowledge.

**Severity anchors**

- **5** — A new user genuinely cannot run or set up the project: instructions
  are absent or broken, required config is undocumented, no working entry point.
- **4** — Setup is possible but painful and error-prone; key prerequisites are
  only discoverable by reading source or trial-and-error.
- **3** — Onboarding works but has notable gaps (e.g. no "getting started",
  stale steps) that slow a newcomer.
- **2** — Minor friction: a missing example command, an unclear default.
- **1** — Cosmetic approachability nit (e.g. install note buried lower than it
  should be).

## 2. Documentation

**Definition.** Whether the code, its usage, and its intent are adequately
explained for the intended audience (users, callers, future maintainers).

**Look for:** missing/inaccurate README or API docs; public functions without
docstrings/comments where intent isn't obvious; out-of-date docs contradicting
code; undocumented parameters, return values, errors, side effects; missing
rationale for non-obvious decisions; examples that don't run.

**Severity anchors**

- **5** — Documentation is absent or so wrong it misleads users into breaking
  things; a critical public API is undocumented.
- **4** — Major surfaces (primary API, main workflow) are undocumented or stale
  enough to cause real mistakes.
- **3** — Meaningful gaps: some public items undocumented, examples missing.
- **2** — Small gaps: a parameter or edge case unexplained.
- **1** — Typos, formatting, or trivially-improvable phrasing.

## 3. Maintainability

**Definition.** How safely and cheaply the code can be changed over time.

**Look for:** high complexity (long functions, deep nesting, tangled control
flow); tight coupling and poor separation of concerns; significant duplication;
missing or ineffective tests around changeable logic; fragile/implicit
dependencies; dead code; configuration hard-coded where it should be
parameterized; no error handling where failure is likely.

**Severity anchors**

- **5** — Changing the code safely is effectively impossible: no tests around
  critical logic plus deep coupling, or a structure that guarantees regressions.
- **4** — High risk of regressions on change: major duplication, a god
  object/function, or a critical path with no test coverage.
- **3** — Noticeable maintenance burden: overly complex function, moderate
  duplication, thin tests.
- **2** — Small smells: a slightly-too-long function, a magic number.
- **1** — Trivial cleanup (dead variable, minor tidy-up).

## 4. Interpretability

**Definition.** How readable the code is on its face — how easily a reader can
understand what a piece of code does without running it or hunting elsewhere.

**Look for:** unclear/misleading names; abbreviations and cryptic identifiers;
non-local reasoning (must jump across many files to understand one thing);
surprising behavior that contradicts names/signatures; clever code without
explanation; inconsistent abstractions; comments that lie.

**Severity anchors**

- **5** — Code is effectively unreadable where correctness depends on
  understanding it (e.g. critical logic that no reasonable reader can follow).
- **4** — Core logic is seriously confusing: misleading names or behavior that
  contradicts the interface, likely to cause misuse.
- **3** — Notable readability problems in non-trivial code.
- **2** — Minor clarity issues: an awkward name, a slightly opaque expression.
- **1** — Cosmetic naming/formatting preferences.

## 5. Interoperability

**Definition.** How well the code works with other tools, systems, formats,
platforms, and standards.

**Look for:** non-standard or proprietary formats where standards exist;
platform-specific assumptions (paths, line endings, OS) that break portability;
hard-coded hosts/ports/paths; ignoring established protocols or schemas;
brittle integration points; missing versioning on public interfaces/APIs;
encoding/locale assumptions.

**Severity anchors**

- **5** — Cannot integrate with a required system/platform, or breaks a
  standard contract other components depend on.
- **4** — Serious portability/integration barrier likely to block real use
  cases (e.g. OS-specific code in a cross-platform tool).
- **3** — Works but deviates from a common standard in ways that cause friction.
- **2** — Minor portability assumption unlikely to bite most users.
- **1** — Cosmetic deviation from a convention.

## 6. Reusability

**Definition.** How easily parts of this code can be lifted and reused elsewhere.

**Look for:** clean vs. leaky boundaries; hidden global state and side effects;
tight coupling to app-specific context; hard-coded assumptions that block reuse;
over- or under-generalization; missing extension points; utilities buried in
unrelated modules; unclear public vs. private surface.

**Severity anchors**

- **5** — A component that clearly should be reusable is impossible to reuse
  without copy-paste-and-rewrite due to entangled dependencies/global state.
- **4** — Significant coupling or hidden state blocks reuse of an important
  component.
- **3** — Reuse is possible but awkward: some hard-coded assumptions or unclear
  boundaries.
- **2** — Minor reuse friction (e.g. a helper that could be parameterized).
- **1** — Cosmetic (e.g. a utility that would be nicer in a shared module).

## 7. Sustainability

**Definition.** How well the code holds up over time — its ongoing health and
cost of ownership.

**Look for:** outdated/abandoned/unmaintained dependencies; use of deprecated
APIs; unpinned or over-pinned versions creating risk; known-vulnerable packages;
license risks/incompatibilities; reliance on end-of-life runtimes/tech; lack of
CI or automated checks; accumulating tech debt with no path to pay it down;
resource leaks or unbounded growth.

**Severity anchors**

- **5** — Imminent breakage or legal/security risk: known-vulnerable or
  abandoned critical dependency, EOL runtime, license conflict that forbids use.
- **4** — Deprecated core dependency/API that will break on the next upgrade; no
  version pinning on a fragile stack.
- **3** — Aging dependencies or debt that will need attention before long.
- **2** — Minor: a slightly stale dependency, a soft-deprecated call.
- **1** — Cosmetic (e.g. a newer alternative exists but current one is fine).

## 8. Cohesion (with other project components)

**Definition.** How well the reviewed code fits the rest of the project.

**Look for:** inconsistent conventions vs. the surrounding codebase (style,
error handling, logging, naming, structure); reinventing something the project
already provides; misplaced files/modules; drift from established patterns;
duplicated concepts that should be unified; violating the project's architectural
boundaries; configuration that contradicts project-wide settings.

**Severity anchors**

- **5** — Directly conflicts with or bypasses core project architecture in a way
  that will cause breakage or divergence (e.g. a parallel, incompatible
  implementation of a core system).
- **4** — Significant divergence from project patterns that undermines
  consistency where it matters (e.g. its own error/logging scheme).
- **3** — Noticeable inconsistency or a redundant reimplementation of an
  existing utility.
- **2** — Minor convention drift (naming/style differing from neighbors).
- **1** — Cosmetic inconsistency.
