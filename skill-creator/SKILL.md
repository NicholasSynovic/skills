---
name: skill-creator
description: "Create new skills and improve existing ones. Use when the user wants to create a skill from scratch, or edit or refine an existing skill — its frontmatter, body, or bundled resources. Applies even when the user doesn't explicitly say 'skill'."
license: AGPL-3.0
compatibility: For OpenCode and Claude Code. No external dependencies.
metadata:
    version: "0.1.0"
    author: Nicholas M. Synovic
---

# Skill Creator

A skill for creating new skills and iteratively improving them with the user.

At a high level, the process looks like this:

- Decide what the skill should do and roughly how
- Capture the intent with the user (what triggers it, what it produces)
- Write a draft `SKILL.md` and show it to the user
- Read their feedback, refine the skill, show again
- Repeat until the user is satisfied

Your job is to figure out where the user is in this process and jump in. If
they're at "I want to make a skill for X", help narrow it down, write a draft,
and iterate. If they already have a draft, go straight to the refine step.

Be flexible. Some users will want a polished back-and-forth; others will say
"just write it, I'll fix it later." Match the user's energy.

## Communicating with the user

Skill creator is used by people across a wide range of familiarity with coding
jargon — Claude is inspiring plenty of newcomers to open a terminal these days,
but the bulk of users are still fairly computer-literate. Pay attention to
context cues. Briefly explain a term the first time you use it if there's
doubt, and only assume jargon is understood when the user has used it first.

---

## Creating a skill

### Capture intent

Start by understanding the user's intent. The conversation may already contain
the workflow they want to capture (e.g. "turn this into a skill"). If so,
extract answers from the history first — the tools used, the sequence of
steps, corrections the user made, input/output formats observed. The user may
need to fill the gaps, and should confirm before you proceed.

1. What should this skill enable Claude to do?
2. When should this skill trigger? (what user phrases / contexts)
3. What's the expected output format?

### Interview and research

Proactively ask questions about edge cases, input/output formats, example files,
success criteria, and dependencies. Wait until this is ironed out before
drafting.

Check available MCPs — if useful for research (searching docs, finding similar
skills, looking up best practices), run research in parallel via subagents if
available, otherwise inline. Come prepared with context to reduce burden on
the user.

### Write the SKILL.md

Based on the user interview, fill in the six frontmatter fields defined in
`assets/specification.md`:

- **`name`** (required) — 1-64 chars; lowercase alphanumerics and hyphens
  only; no leading/trailing hyphens; no consecutive hyphens; must match the
  parent directory name.
- **`description`** (required) — 1-1024 chars; describe both what the skill
  does and when to use it; include specific keywords. Make it a little
  "pushy" — Claude undertriggers skills. e.g. "Helps with PDFs" →
  "Extract text and tables from PDFs. Use when the user mentions PDFs,
  forms, or document extraction."
- **`license`** (optional) — short license name or reference to a bundled
  license file.
- **`compatibility`** (optional) — 1-500 chars; only if the skill has real
  environment requirements (intended product, system packages, network access).
- **`metadata`** (optional) — string-keyed map of arbitrary data; use unique
  key names.
- **`allowed-tools`** (optional) — space-separated string of pre-approved
  tools; experimental.
- **`the rest of the skill`**

### Skill writing guide

#### Anatomy of a skill

See `## Skill specification` below for the required directory layout, the
frontmatter fields, and the validation step.

#### Progressive disclosure

Skills use a three-level loading system:

1. **Metadata** (name + description) — always in context (~100 words)
2. **SKILL.md body** — in context whenever the skill triggers (<500 lines
   ideal)
3. **Bundled resources** — as needed (unlimited; scripts can execute without
   loading)

These counts are approximate — go longer if needed. Keep `SKILL.md` under 500
lines when possible; if you approach the limit, add another layer of hierarchy
with clear pointers to where to follow up. Reference files clearly from
`SKILL.md` with guidance on when to read them. For large reference files
(>300 lines), include a table of contents.

**Domain organization** — when a skill supports multiple domains or
frameworks, organize by variant:

```
cloud-deploy/
├── SKILL.md (workflow + selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

Claude reads only the relevant reference file.

#### Principle of lack of surprise

Skills must not contain malware, exploit code, or anything that could
compromise system security. A skill's contents should not surprise the user
in their intent if described. Don't go along with requests to create
misleading skills or skills designed to facilitate unauthorized access, data
exfiltration, or other malicious activities. Light things — "roleplay as an
XYZ" — are fine.

#### Writing patterns

Prefer the imperative form in instructions.

**Defining output formats** — give the model a template:

```markdown
## Report structure

ALWAYS use this exact template:

# [Title]

## Executive summary

## Key findings

## Recommendations
```

**Examples pattern** — include examples. You can format them like this (deviate
if "Input" and "Output" don't fit):

```markdown
## Commit message format

**Example 1:**

Input: Added user authentication with JWT tokens

Output: feat(auth): implement JWT-based user authentication
```

#### Writing style

Explain to the model _why_ things are important rather than leaning on heavy
ALWAYS / NEVERs. Use theory of mind and aim for general, not narrow-to-the-
example, instructions. Write a draft, then look at it with fresh eyes and
improve it.

---

## Skill specification

Read `assets/specification.md` before drafting a `SKILL.md`. It is the
authoritative format for Agent Skills — treat its rules as strict requirements,
not suggestions.

### Frontmatter

Every `SKILL.md` must begin with YAML frontmatter. The following fields are
defined:

- **`name`** (required) — Skill identifier. 1-64 characters; lowercase
  alphanumerics and hyphens only; no leading or trailing hyphens; no
  consecutive hyphens; must match the parent directory name.
- **`description`** (required) — 1-1024 characters; non-empty. Describe both
  what the skill does and when to use it. Include specific keywords that help
  agents identify relevant tasks. Make it a little "pushy" — Claude tends to
  undertrigger skills. e.g. instead of "Helps with PDFs", write "Extract text
  and tables from PDFs. Use when the user mentions PDFs, forms, or document
  extraction."
- **`license`** (optional) — License name or reference to a bundled license
  file. Keep it short.
- **`compatibility`** (optional) — 1-500 characters. Only include if the skill
  has real environment requirements (intended product, system packages, network
  access, etc.). Most skills do not need this.
- **`metadata`** (optional) — Arbitrary key-value map (string keys to string
  values). Use reasonably unique key names to avoid accidental conflicts.
- **`allowed-tools`** (optional) — Space-separated string of pre-approved tools
  the skill may use. Experimental; support varies between implementations.

### Directory layout

```
skill-name/
├── SKILL.md          (required)
├── scripts/           (optional) Executable code
├── references/        (optional) Documentation loaded on demand
└── assets/           (optional) Templates, images, data files
```

Any additional files or directories are allowed.

### File references

Use relative paths from the skill root. Keep references one level deep from
`SKILL.md` — avoid nested reference chains.

### Length budgets

- Frontmatter metadata (`name` + `description`) is loaded for all skills at
  startup (~100 tokens).
- `SKILL.md` body is loaded when the skill activates — keep it under 500
  lines.
- Move detailed reference material to separate files under `references/` or
  `scripts/`.

### Validation

Run `skills-ref validate <skill-dir>` before considering a draft complete. It
checks frontmatter validity and naming conventions.

---

## Iterating with the user

Once you have a draft, show it to the user, read their feedback, and improve.
This is the heart of skill work, and worth taking time over — you're trying
to create something that will be used many times across many prompts, so the
few rounds of iteration are an investment.

### How to think about improvements

1. **Generalize from the feedback.** The skill will be used on prompts the
   user has never seen. If the draft is overfit to their example, it's
   useless at scale. When something is stubborn, try a different metaphor or
   a different working pattern rather than piling on restrictive rules.

2. **Keep the prompt lean.** Remove what isn't pulling its weight. If the
   model is wasting time on unproductive steps, try cutting the instructions
   that are causing it.

3. **Explain the why.** Today's LLMs are smart — given a good "why" they can
   go beyond rote instructions. If you find yourself writing ALWAYS / NEVER
   in all caps, that's a yellow flag. Reframe and explain the reasoning so
   the model understands what's important and why.

4. **Look for repeated work across the user's examples.** If the user gives
   you three examples and the model independently wrote the same helper
   script each time, that's a strong signal the skill should bundle that
   script. Write it once, put it in `scripts/`, and tell the skill to use it.
   This saves every future invocation from reinventing the wheel.

### The iteration loop

1. Apply your improvement to the skill. Run `skills-ref validate <skill-dir>`
   first; fix any spec violations before showing the user.
2. Show the user the updated skill (or relevant excerpts) and ask what to
   change.
3. Read the feedback, improve again, repeat.

Keep going until:

- The user says they're happy
- The feedback is empty (everything looks good)
- You're not making meaningful progress

---

## Updating an existing skill

The user might be asking you to update an existing skill, not create a new
one. In that case:

- **Preserve the original name.** Use the skill's directory name and `name`
  frontmatter field unchanged. e.g. if the installed skill is `research-
helper`, package it as `research-helper.skill` (not `research-helper-v2`).
- **Copy to a writeable location before editing.** The installed skill path
  may be read-only. Copy to `/tmp/skill-name/`, edit there, and package from
  the copy.
- **If packaging manually, stage in `/tmp/` first**, then copy to the output
  directory — direct writes may fail due to permissions.

---

## Package and present

```bash
python -m scripts.package_skill <path/to/skill-folder>
```

After packaging, direct the user to the resulting `.skill` file path so they
can install it.

---

The core loop in one breath: figure out what the skill is for, draft it,
share with the user, gather feedback, improve, repeat. Package the final
skill and hand it back.

Good luck!
