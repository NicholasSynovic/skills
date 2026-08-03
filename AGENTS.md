# AGENTS.md

## What this repo is

A curated **collection of third-party README-generator skills** fetched from
public GitHub repos with the `skills` CLI (`npx skills add ...`). It is a
reference corpus, not an application: there is no build, test, lint, or runtime.

## Layout

- `readme-generator/references.txt` — the source-of-truth list of `npx skills add`
  commands used to populate this collection (49 commands).
- `readme-generator/skills-lock.json` — lockfile written by the `skills` CLI.
  Maps skill name -> GitHub source, `skillPath`, and content hash. 34 entries.
- `readme-generator/references/skills/<skill-name>/` — the **vendored** skill
  content (34 dirs, each usually a `SKILL.md` plus its own references/assets).

Note the mismatch: `references.txt` lists 49 adds but only 34 resolved into the
lockfile and `references/skills/`. Some sources fail to resolve or duplicate an
existing skill name; treat `skills-lock.json` + `references/skills/` as the
authoritative installed set, not `references.txt`.

## Working conventions

- `references/skills/**` is vendored external content. Do **not** hand-edit it;
  it is meant to mirror upstream and is validated against `computedHash` in the
  lockfile. Editing a file will make it diverge from its recorded hash.
- To add or update a skill, run the `skills` CLI (`npx skills add <repo> --skill
<name>`) rather than copying files in manually, so the lockfile stays correct.
- The AGENTS.md / README.md / SKILL.md files found under `references/skills/**`
  belong to the vendored skills, not to this repo. Don't mistake them for
  repo-level instructions.

## Git

The repo currently has **no commits** (empty `master`); everything is untracked.
