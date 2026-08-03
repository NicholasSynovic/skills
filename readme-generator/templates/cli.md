<!--
  Fill-in skeleton for a CLI / tool README. First-party skill content.
  Replace every {{token}} with a real value from the scan; delete this comment
  and every other HTML comment before shipping. No {{...}} may remain in output.

  Section order follows the Step 2 matrix for CLI/tool, in inverted-pyramid order.
  Depth filter (Step 3a): minimal = Required only; standard = + Recommended;
  comprehensive = + Optional + extended sections from references/section-library.md.

  Few-shot — study these two filled title + one-liner pairs, then write your own
  in the same voice (direct, practical; state what it does, not what it "is"):

    # ripgrep
    Recursively search directories for a regex pattern, faster than grep.

    # fd
    A simple, fast, and user-friendly alternative to find.
-->

<h1 align="center">{{name}}</h1>

<p align="center">{{one-liner}}</p>

<p align="center">
  <a href="https://www.npmjs.com/package/{{name}}"><img alt="version" src="https://img.shields.io/npm/v/{{name}}.svg"></a>
  <a href="LICENSE"><img alt="license" src="https://img.shields.io/badge/license-{{license}}-blue.svg"></a>
</p>

## Install

```bash
{{install-command}}
```

Requires {{runtime}} {{min-version}}+.

## Usage

```bash
{{name}} {{basic-command}}
{{name}} {{command-with-flag}}
{{name}} {{command-with-options}}
```

<!-- Recommended (standard+): why it exists / what it is not -->

## Why {{name}}

{{one-paragraph on the problem it solves and its intended scope; name what it
deliberately does not do.}}

<!-- Recommended (standard+) -->

## Features

- **{{feature-one}}:** {{what it does}}.
- **{{feature-two}}:** {{what it does}}.
- **{{feature-three}}:** {{what it does}}.

## Options

<!-- Copy from `--help` output; keep as a code block, not a table. -->

```
{{-o, --option <value>    Description}}
{{-v, --verbose           Description}}
-h, --help               Show help
-V, --version            Show version
```

<!-- Optional (comprehensive): only if the CLI also exports a programmatic API -->

## API

```{{lang}}
import { {{mainExport}} } from "{{name}}";

const result = await {{mainExport}}({{args}});
```

## Requirements

- {{runtime}} {{min-version}}+
- {{other-requirement}}

<!-- Recommended (standard+) -->

## Contributing

{{how to contribute; link CONTRIBUTING.md if present.}}

## License

[{{license}}](LICENSE)
