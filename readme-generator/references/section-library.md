<!--
  First-party skill content — NOT a vendored skill (unlike references/vendor/**).
  Edit freely.
-->

# Extended section library

Optional, specialized README sections. The per-type skeletons in `templates/`
cover the common sections; pull from here for the rest. Each block is a fill-in
skeleton: copy it into the README, replace every `{{token}}` with a real value
from the scan, and delete any block whose data the scan does not support (never
fabricate). Include per the depth tier from Step 3a — most of these belong to the
`comprehensive` tier.

Contents:

- [Comparison / Alternatives](#comparison--alternatives)
- [Performance](#performance)
- [Security](#security)
- [Data Model](#data-model)
- [API Reference](#api-reference)
- [Migration / Upgrade](#migration--upgrade)
- [Ecosystem / Integration](#ecosystem--integration)
- [Environment Variables](#environment-variables)
- [Shell Completions](#shell-completions)
- [Release Notes](#release-notes)
- [Acknowledgments](#acknowledgments)

---

## Comparison / Alternatives

For projects with well-known alternatives; be fair, not promotional.

```markdown
## Comparison

|                      | {{name}} | {{alternative-a}} | {{alternative-b}} |
| -------------------- | :------: | :---------------: | :---------------: |
| {{capability-one}}   |    ✅    |   ⚠️ {{caveat}}   |        ❌         |
| {{capability-two}}   |    ✅    |        ✅         |        ❌         |
| {{capability-three}} |    ✅    |        ❌         |        ✅         |

✅ full support · ⚠️ partial · ❌ not supported
```

---

## Performance

For projects where speed or resource use is a selling point. Only include real,
measured numbers.

```markdown
## Performance

| Operation         | Time              | Notes    |
| ----------------- | ----------------- | -------- |
| {{operation-one}} | {{measured-time}} | {{note}} |
| {{operation-two}} | {{measured-time}} | {{note}} |

### Benchmarks

{{describe the workload, then the numbers.}}

| Operation     | {{name}}          | {{alternative}}   |
| ------------- | ----------------- | ----------------- |
| {{operation}} | {{measured-time}} | {{measured-time}} |

_Measured on {{hardware/OS}}. Your results may vary._
```

---

## Security

For projects handling sensitive data.

```markdown
## Security

### {{headline claim, e.g. "Your data never leaves your machine"}}

{{one paragraph on the security/privacy posture.}}

### What's Stored Where

| Location   | Contents     | Sensitive? |
| ---------- | ------------ | ---------- |
| `{{path}}` | {{contents}} | {{yes/no}} |

### Reporting a Vulnerability

{{how to report; a private contact, not a public issue.}}
```

---

## Data Model

For projects with a non-trivial persisted schema.

```markdown
## Data Model

| Field       | Indexed    | Stored     | Notes    |
| ----------- | ---------- | ---------- | -------- |
| `{{field}}` | {{yes/no}} | {{yes/no}} | {{note}} |

### Schema

\`\`\`{{lang}}
{{schema-definition}}
\`\`\`
```

---

## API Reference

For libraries and frameworks exposing a programmatic API.

```markdown
## API Reference

### `{{symbol}}({{params}})`

{{what it does.}}

- `{{param}}` (`{{type}}`) — {{description}}.
- Returns `{{return-type}}` — {{description}}.

\`\`\`{{lang}}
{{usage-example}}
\`\`\`

### Errors

| Error       | When it happens |
| ----------- | --------------- |
| `{{error}}` | {{condition}}   |
```

---

## Migration / Upgrade

For projects with breaking changes between major versions.

```markdown
## Upgrading

### From {{old-version}} to {{new-version}}

**Breaking changes:**

- {{breaking-change}}

**Migration steps:**

\`\`\`bash
{{migration-commands}}
\`\`\`
```

---

## Ecosystem / Integration

For projects that plug into a larger toolchain.

```markdown
## Ecosystem

| Tool         | Integration           | Use case     |
| ------------ | --------------------- | ------------ |
| **{{tool}}** | {{native/plugin/CLI}} | {{use case}} |

### With {{tool}}

\`\`\`bash
{{integration-example}}
\`\`\`
```

---

## Environment Variables

Full reference for configurable environment variables (from `.env.example` and
code).

```markdown
## Environment Variables

| Variable  | Description     | Default       |
| --------- | --------------- | ------------- |
| `{{VAR}}` | {{description}} | `{{default}}` |

\`\`\`bash
export {{VAR}}={{value}}
{{run-command}}
\`\`\`
```

---

## Shell Completions

For CLIs that ship completion scripts.

```markdown
## Shell Completions

\`\`\`bash

# Bash

eval "$({{name}} completions bash)"

# Zsh

eval "$({{name}} completions zsh)"

# Fish

{{name}} completions fish > ~/.config/fish/completions/{{name}}.fish
\`\`\`
```

---

## Release Notes

An in-README alternative to a separate CHANGELOG.md (see
`templates/companion/CHANGELOG.md` for the standalone form).

```markdown
## Release Notes

### {{version}} ({{YYYY-MM-DD}})

**New features:**

- {{feature}}

**Fixes:**

- {{fix}}

**Breaking changes:**

- {{breaking-change, or "None"}}
```

---

## Acknowledgments

Credit dependencies, inspirations, and contributors.

```markdown
## Acknowledgments

Built with:

- [{{dependency}}]({{url}}) — {{role}}.

Inspired by:

- [{{project}}]({{url}}) — {{what you borrowed}}.

Thanks to all [contributors](https://github.com/{{owner}}/{{repo}}/graphs/contributors).
```
