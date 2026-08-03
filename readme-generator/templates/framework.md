<!--
  Fill-in skeleton for a framework README. First-party skill content.
  Replace every {{token}} with a real value from the scan; delete this comment
  and every other HTML comment before shipping. No {{...}} may remain in output.

  Section order follows the Step 2 matrix for framework, in inverted-pyramid
  order. Depth filter (Step 3a): minimal = Required only; standard = + Recommended;
  comprehensive = + Optional + extended sections from references/section-library.md.

  Feature descriptions run longer than CLI/library: explain the "why" with the
  "what". Progressive disclosure: Quick Start -> Basic -> Advanced -> Configuration.

  Few-shot — study these two filled title + one-liner pairs, then write your own
  in the same voice (precise, extensibility-forward):

    # Fastify
    A fast and low-overhead web framework for Node.js, built around plugins.

    # Astro
    The web framework for content-driven sites, with a plugin-based islands model.
-->

# {{name}}

[![version](https://img.shields.io/npm/v/{{name}}.svg)](https://www.npmjs.com/package/{{name}})
[![license](https://img.shields.io/badge/license-{{license}}-blue.svg)](LICENSE)

{{one-liner explaining the core value proposition}}

## Install

```bash
{{install-command}}
```

## Quick Start

<!-- Minimal working example, ~5 lines. -->

```{{lang}}
{{minimal-working-example}}
```

<!-- Recommended (standard+): why it exists / what it is not -->

## Why {{name}}

{{one-paragraph on the problem it solves and its intended scope; name what it
deliberately does not do.}}

<!-- Recommended (standard+) -->

## Features

- **{{feature-one}}:** {{detailed explanation of what it does and why it matters}}.
- **{{feature-two}}:** {{detailed explanation}}.
- **{{feature-three}}:** {{detailed explanation}}.

## Usage

### Basic

```{{lang}}
{{basic-usage}}
```

### Advanced

```{{lang}}
{{advanced-usage-with-configuration}}
```

## Configuration

| Option       | Type       | Default       | Description          |
| ------------ | ---------- | ------------- | -------------------- |
| `{{option}}` | `{{type}}` | `{{default}}` | {{what it controls}} |

## How to Extend

<!-- Document the extension points: plugins, middleware, hooks. -->

```{{lang}}
{{plugin-or-extension-example}}
```

## Requirements

- {{runtime}} {{min-version}}+
- {{other-requirement}}

## Contributing

{{how to contribute; link CONTRIBUTING.md if present.}}

## License

[{{license}}](LICENSE)
