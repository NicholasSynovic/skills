# Citations — Source Skills Reviewed

The `readme-generator` skill is a synthesis of a corpus of third-party
README-generator agent skills. This file records which GitHub repositories were
reviewed and leveraged as design input.

- The corpus was added via the `skills` CLI; the full command list lives in
  [`references.txt`](references.txt) (49 `npx skills add` commands).
- The vendored copies live under `references/vendor/<skill>/` and are
  **gitignored**, so they are not present on a fresh clone (see
  [`AGENTS.md`](../AGENTS.md)). Restore them with the commands in
  `references.txt`.
- The clustered, section-by-section feature analysis derived from these skills
  is in [`CLUSTERED_FEATURES.md`](CLUSTERED_FEATURES.md), which cites each source
  as `<skill>/<file> (lines X-Y)` relative to `references/vendor/`.

## Repositories reviewed and leveraged (34 skills present)

Of the 49 `npx skills add` commands in `references.txt`, 34 skills resolved into
`references/vendor/` and were used in the analysis. Each row lists the vendored
skill directory, its source repository, and the `--skill` name requested.

| Vendored skill (`references/vendor/`) | Source repository                                        | `--skill` name                |
| ------------------------------------- | -------------------------------------------------------- | ----------------------------- |
| `accelint-readme-writer`              | https://github.com/gohypergiant/agent-skills             | `accelint-readme-writer`      |
| `configure-readme`                    | https://github.com/laurigates/claude-plugins             | `configure-readme`            |
| `crafting-effective-readmes`          | https://github.com/softaworks/agent-toolkit              | `crafting-effective-readmes`  |
| `crafting-readme-files`               | https://github.com/dicklesworthstone/meta_skill          | `crafting-readme-files`       |
| `create-github-readme`                | https://github.com/alfredang/skills                      | `Create GitHub README`        |
| `create-readme`                       | https://github.com/github/awesome-copilot                | `create-readme`               |
| `diataxis-gen-readme`                 | https://github.com/trogonstack/agentskills               | `diataxis-gen-readme`         |
| `generate-readme-screenshots`         | https://github.com/coder/mux                             | `generate-readme-screenshots` |
| `generate-readme`                     | https://github.com/cowork-os/cowork-os                   | `generate-readme`             |
| `github-readme`                       | https://github.com/thatrebeccarae/claude-marketing       | `github-readme`               |
| `humanize-readme`                     | https://github.com/b4r7x/agent-skills                    | `humanize-readme`             |
| `indexion-readme`                     | https://github.com/trkbt10/indexion-skills               | `indexion-readme`             |
| `make-readme`                         | https://github.com/gupsammy/claudest                     | `make-readme`                 |
| `prowler-readme-table`                | https://github.com/prowler-cloud/prowler                 | `prowler-readme-table`        |
| `pypi-readme-creator`                 | https://github.com/jamie-bitflight/claude_skills         | `pypi-readme-creator`         |
| `readme-badger`                       | https://github.com/jamie-bitflight/claude_skills         | `readme-badger`               |
| `readme-blueprint-generator`          | https://github.com/github/awesome-copilot                | `readme-blueprint-generator`  |
| `readme-com`                          | https://github.com/membranedev/application-skills        | `readme-com`                  |
| `readme-craft`                        | https://github.com/majesticlabs-dev/majestic-marketplace | `readme-craft`                |
| `readme-creator`                      | https://github.com/mblode/agent-skills                   | `readme-creator`              |
| `readme-sync`                         | https://github.com/shipshitdev/library                   | `readme-sync`                 |
| `readme-updater`                      | https://github.com/ovachiever/droid-tings                | `readme-updater`              |
| `readme-updates`                      | https://github.com/sgcarstrends/sgcarstrends             | `readme-updates`              |
| `readme-wizard`                       | https://github.com/debs-obrien/learn-agent-skills        | `readme-wizard`               |
| `readme-writer`                       | https://github.com/steveclarke/dotfiles                  | `readme-writer`               |
| `repository-readme-writer`            | https://github.com/jpcaparas/skills                      | `repository-readme-writer`    |
| `sc-readme`                           | https://github.com/tony363/superclaude                   | `sc-readme`                   |
| `standard-readme`                     | https://github.com/tenequm/skills                        | `standard-readme`             |
| `wp-readme-optimizer`                 | https://github.com/jdevalk/skills                        | `wp-readme-optimizer`         |
| `zr-readme`                           | https://github.com/zenon-red/skills                      | `zr-readme`                   |

### Skills with an ambiguous source repository

Some `--skill` names appear in `references.txt` under more than one repository.
The `skills` CLI installs by skill name, so on a name collision the last-added
copy wins and the exact source of the vendored directory cannot be confirmed
from the files alone. The candidate repositories for each are listed below.

| Vendored skill     | Confirmed / candidate source repositories                                                                                                                                                                                                                                                                                                                                          |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `readme`           | Confirmed https://github.com/tushaarmehtaa/tushar-skills (SKILL.md frontmatter `author: tushaarmehtaa`). Other repos requesting `readme`: https://github.com/boshu2/agentops, https://github.com/dropseed/plain, https://github.com/jimweller/clanker-skills, https://github.com/oimiragieo/agent-studio, https://github.com/shpigford/skills, https://github.com/statelyai/skills |
| `update-readme`    | Candidates: https://github.com/athola/claude-night-market, https://github.com/fradser/dotclaude, https://github.com/gupsammy/claudest                                                                                                                                                                                                                                              |
| `readme-generator` | Candidates: https://github.com/dengineproblem/agents-monorepo, https://github.com/jeremylongshore/claude-code-plugins-plus-skills, https://github.com/patricio0312rev/skills                                                                                                                                                                                                       |
| `write-readme`     | Candidates: https://github.com/gkwa/volcanicviper, https://github.com/remix-run/remix (vendored content matches gkwa/volcanicviper's library/CLI/agent-tool framing)                                                                                                                                                                                                               |

## Requested but not resolved (15 skills)

These `npx skills add` commands are listed in `references.txt` but did not
produce a distinct vendored directory. Some are name collisions resolved above
(the same skill name from a different repo); the remainder did not resolve at
all and were **not** used in the analysis:

- `readme-standards` — https://github.com/laurigates/claude-plugins
- `readme-to-landing-page` — https://github.com/luongnv89/skills
- `skills-readme-updater` — https://github.com/oldwinter/skills
- `update-readme` (duplicate names) — https://github.com/athola/claude-night-market, https://github.com/fradser/dotclaude
- `readme-generator` (duplicate names) — two of {https://github.com/dengineproblem/agents-monorepo, https://github.com/jeremylongshore/claude-code-plugins-plus-skills, https://github.com/patricio0312rev/skills}
- `readme` (duplicate names) — https://github.com/boshu2/agentops, https://github.com/dropseed/plain, https://github.com/jimweller/clanker-skills, https://github.com/oimiragieo/agent-studio, https://github.com/shpigford/skills, https://github.com/statelyai/skills
- `write-readme` (duplicate name) — https://github.com/remix-run/remix

## Acknowledgements

Thanks to the authors and maintainers of all the repositories above. Their
skills served as the design corpus for `readme-generator`. Vendored content
under `references/vendor/**` remains the property of its respective authors and
is included for reference only.
