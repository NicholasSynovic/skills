---
name: review-abilities
description: >-
    Review a project, directory, subdirectory, collection of files, or a single
    file to surface potential issues across eight cross-cutting qualities —
    accessibility (code approachability), documentation, maintainability,
    interpretability, interoperability, reusability, sustainability, and cohesion
    with other project components. Each finding is ranked 1 (nag) to 5 (critical)
    and written to a TODO.ability.md. Use this whenever the user asks to review,
    audit, assess, or critique code quality; asks "what's wrong with" or "how do I
    improve" a codebase; wants a TODO/action list for a project; or mentions any of
    maintainability, reusability, sustainability, documentation quality,
    interoperability, or code cohesion — even if they don't name this skill or the
    output file explicitly.
---

# Review Abilities

## Why this matters

Ordinary code review catches bugs and style nits. It rarely catches the
_cross-cutting_ qualities that decide whether a project survives contact with
other people and with time: can a newcomer run it, will the next maintainer
understand it, does it play well with the rest of the system, will it still work
in a year. This skill makes those qualities explicit, evaluates them
deliberately, and leaves behind a durable, checkable action list.

The goal is an honest, useful audit — not a rubber stamp. Report real problems
plainly, and don't invent findings to fill space. A clean area getting no
findings is a valid and good result.

## The eight abilities

Each finding you record belongs to exactly one of these. One-line summaries
below; **read `references/rubric.md` for the full definition of each ability and
its severity anchors before writing findings**.

- **Accessibility** — how easily a non-author can discover, set up, run, and
  start contributing to the code.
- **Documentation** — whether the code, its usage, and its intent are adequately
  explained for the intended audience.
- **Maintainability** — how safely and cheaply the code can be changed over time.
- **Interpretability** — how readable the code is on its face, without running it
  or hunting elsewhere.
- **Interoperability** — how well it works with other tools, systems, formats,
  platforms, and standards.
- **Reusability** — how easily parts can be lifted and reused elsewhere.
- **Sustainability** — how well it holds up over time; its ongoing health and
  cost of ownership.
- **Cohesion** — how well the reviewed code fits the rest of the project.

## Severity scale

Severity describes **how bad a finding is**, not how good the code is. Every
finding gets a whole number 1–5, from **5 — Critical** (blocks use or actively
breaks things) down to **1 — Nag** (cosmetic or nice-to-have).

**`references/rubric.md` is the canonical source for the severity scale and its
per-ability anchors** — read it before scoring findings, and edit it (not this
file) when the definitions change.

## Procedure

1. **Establish scope.** Identify exactly what you were asked to review — whole
   project, a directory, a subset of files, or one file. State the scope in the
   output.
    - For a **single file or small set**, read them fully.
    - For a **directory or whole project**, start from the map (README,
      manifest/build files, entry points, directory layout), then read the files
      that carry the most weight. Sample representatively rather than reading
      everything blindly; note if scope forced you to sample.
    - Always look just far enough _outside_ the scope to judge **cohesion** and
      **interoperability** (e.g. sibling modules, project conventions, configs).

2. **Evaluate each ability deliberately.** Go through all eight — don't stop at
   the obvious two or three. For each, decide whether there are genuine issues,
   and for each issue capture: a short title, the ability, a severity (with the
   rubric anchors in mind), a `path:line` reference where applicable, _why it
   matters_, and a _concrete suggested fix_.

3. **Write / update `TODO.ability.md`** at the **root of the reviewed target**
   (the project/directory top; for a single file, the directory containing it);
   if that location is not writable, fall back to the current working directory.
   Use the format below, and obtain the `Last reviewed` value from the real
   current system date/time (e.g. run `date`) rather than estimating it.

## Output: TODO.ability.md

Write to the root of the reviewed target (fall back to the current working
directory if it is not writable). Use this structure exactly.

```markdown
# TODO.ability — Code Quality Review

_Scope: <what was reviewed>_
_Last reviewed: <YYYY-MM-DD HH:MM>_

## Summary

| Ability          | 5 Crit | 4 Maj | 3 Mod | 2 Min | 1 Nag |
| ---------------- | ------ | ----- | ----- | ----- | ----- |
| Accessibility    | 0      | 1     | 0     | 0     | 0     |
| Documentation    | ...    |       |       |       |       |
| Maintainability  | ...    |       |       |       |       |
| Interpretability | ...    |       |       |       |       |
| Interoperability | ...    |       |       |       |       |
| Reusability      | ...    |       |       |       |       |
| Sustainability   | ...    |       |       |       |       |
| Cohesion         | ...    |       |       |       |       |

## Accessibility

- [ ] **[S4] Title of finding** — `path/to/file.ext:123`
      Why it matters: <one or two sentences>
      Suggested fix: <concrete action>

## Documentation

...
```

Rules for the output:

- One section per ability, in the order listed above. **Group by ability, then
  sort findings by severity, highest first.**
- If an ability has no findings, keep its heading and write `_No findings._`
  so readers can see it was actually checked.
- Every finding is a GitHub checkbox `- [ ]`, prefixed with `[S<n>]` for
  severity, so users can track progress.
- Keep each finding self-contained: title, `path:line`, why-it-matters, fix.

## Re-running on an existing TODO.ability.md

If the file already exists, **update rather than clobber**:

1. Read the existing file first.
2. **Preserve checkbox state**: a finding the user already checked (`- [x]`)
   stays checked. Don't re-open resolved items.
3. If a previously reported issue now appears **fixed**, mark it `- [x]` and add
   `_(resolved <date>)_` to the line rather than deleting it, so history is
   visible.
4. Refresh the summary table and merge in new findings in the right sections.
5. Append a short **timestamped review log** entry at the bottom under a
   `## Review log` heading, including the rubric version you scored against (see
   the version stamp at the top of `references/rubric.md`), e.g.:

    ```markdown
    - 2026-08-03 14:22 — re-reviewed src/ (rubric v1); 2 new, 1 resolved.
    ```

    This keeps a lightweight record of each run without bloating the findings.
