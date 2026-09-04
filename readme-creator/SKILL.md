---
name: readme-creator
description: "Create, rewrite, or improve a project's README.md by analyzing the repository itself — its manifests, build config, CI workflows, docs, and source. Use this whenever the user asks for a README, project overview, or repository documentation, wants to polish or expand an existing README, or is setting up a new project that lacks one — even if they never say the word 'README'."
---

# README Creator

Write a README that lets a newcomer understand what the project is, why it
exists, and how to run it — based only on evidence found in the repository.
A README documenting commands that don't work or features that don't exist is
worse than a shorter, truthful one, so everything you write must trace back to
something you actually saw in the repo.

## Exemplars

Before writing, skim these four READMEs; they demonstrate the target style:
a centered header with logo and badge row, a one-line pitch, a nav line of
anchor links, GitHub admonitions, and fenced command blocks.

- `assets/README_0.md` — large application sample
- `assets/README_1.md` — multi-sample collection (uses `<details>` sections)
- `assets/README_2.md` — small CLI tool
- `assets/README_3.md` — compact, prose-first README

Emulate their _style_, never their _content_. In particular, do not copy the
Contributing/CLA and Trademarks boilerplate that some of them contain — it is
specific to those projects, and this skill excludes those sections anyway.

## Step 1: Discover the project

Read the repository before writing anything. Good sources, in rough priority:

1. **Manifests and lockfiles** — `package.json`, `pyproject.toml`,
   `Cargo.toml`, `go.mod`, etc. These give the name, description, tech stack,
   version constraints, and defined scripts.
2. **Build, test, lint, and CI config** — Makefiles, task runners, `.github`
   workflow files. These reveal the install/build/test commands that actually
   work, rather than the ones you'd guess.
3. **Existing docs and source** — any current `README.md`, `docs/`,
   `CHANGELOG.md`, `LICENSE`, and the code entry points showing how the
   project is really used.
4. **Instruction files, if present** — `AGENTS.md`, `CLAUDE.md`,
   `.github/copilot-instructions.md`, `CONTRIBUTING.md`. These may capture
   conventions worth reflecting, but they are optional inputs: most repos
   don't have them, and their absence changes nothing.

Check that each file exists before reading it, and work from what is actually
there — not from what a typical project of this kind would contain.

## Step 2: Choose the structure

Start from the skeleton below, then adapt it to the project type: a library
leads with installation, an application leads with getting started and
running, a sample collection leads with a samples table. Omit any section
with no truthful content — an empty section is worse than a missing one.

Recommended flow:

1. Title, plus the project's logo/icon if the repo has one
2. Badge row (see the rules below)
3. One-line pitch — what this is, and for whom
4. Overview — what it does and why it exists
5. Features — the few that distinguish it
6. Getting started — prerequisites, installation, first run
7. Usage — main commands or API, with runnable examples
8. Project structure — only if the layout is non-obvious
9. Resources — related documentation and links
10. Troubleshooting — only if real guidance exists

## Step 3: Write

- Use GitHub Flavored Markdown, with GitHub admonition syntax where it adds
  value: `> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`.
  Reference: https://github.com/orgs/community/discussions/16925
- Put every command in a fenced code block.
- Use a centered header block like the exemplars: `<!-- prettier-ignore -->`,
  `<div align="center">`, logo, title, badge row, nav links.
- Keep emojis rare, if used at all — a few in feature bullets is the most the
  exemplars use.

## Rules

**Link out, don't inline.** Never duplicate the content of `LICENSE`,
`CONTRIBUTING`, `CHANGELOG`, or `CODE_OF_CONDUCT` files in the README. These
files already exist for that purpose, and a second copy drifts out of date.
A one-line link is the right amount of README coverage for them.

**Be concise.** Readers skim. Every section should survive the question
"what does a newcomer need here?" — if the answer is "details live in
`docs/x.md`", write one sentence and link.

**Never fabricate.** This is the hard rule, because a confident README full
of invented facts actively misleads users:

- Only add badges for facts you verified: CI status if workflow files exist,
  license from the `LICENSE` file, language/runtime versions from manifests.
  If there is no CI, there is no build badge.
- Only include links that resolve within the repo; for external links, only
  ones found in repo files.
- Only document commands the repo's configs or docs actually define.
- When information is missing, omit the section rather than filling it with
  plausible-sounding content.

## Self-check

Before finishing, verify:

- Every command in the README matches something defined in the repo.
- Every badge and link is backed by repo evidence.
- No LICENSE/CONTRIBUTING/CHANGELOG content is inlined.
- The structure fits the project type, and no section is empty filler.
