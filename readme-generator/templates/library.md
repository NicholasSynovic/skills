<!--
  Fill-in skeleton for a library / SDK README. First-party skill content.
  Replace every {{token}} with a real value from the scan; delete this comment
  and every other HTML comment before shipping. No {{...}} may remain in output.

  Section order follows the Step 2 matrix for library/SDK, in inverted-pyramid
  order. Depth filter (Step 3a): minimal = Required only; standard = + Recommended;
  comprehensive = + Optional + extended sections from references/section-library.md.

  Few-shot — study these two filled title + one-liner pairs, then write your own
  in the same voice (technical, precise; name the concrete capability):

    # zod
    TypeScript-first schema validation with static type inference.

    # httpx
    A next-generation HTTP client for Python, with sync and async APIs.
-->

<h3 align="center">{{name}}</h3>
<p align="center">{{one-liner}}</p>

<p align="center">
  <a href="https://www.npmjs.com/package/{{name}}"><img alt="version" src="https://img.shields.io/npm/v/{{name}}.svg"></a>
  <a href="LICENSE"><img alt="license" src="https://img.shields.io/badge/license-{{license}}-blue.svg"></a>
</p>

## Highlights

<!-- "Highlights" not "Features": show what makes the library stand out. -->

- {{highlight-one}}
- {{highlight-two}}
- {{highlight-three}}

## Quick Start

<!-- Install + minimal working example, under 10 lines total. -->

```bash
{{install-command}}
```

```{{lang}}
import { {{mainExport}} } from "{{name}}";

{{minimal-usage-example}}
```

<!-- Recommended (standard+): why it exists / what it is not -->

## Why {{name}}

{{one-paragraph on the problem it solves and its intended scope; name what it
deliberately does not do.}}

<!-- Recommended (standard+) -->

## Usage

```{{lang}}
// {{pattern-one}}
import { {{A}} } from "{{name}}";

// {{pattern-two}}
import { {{B}} } from "{{name}}/{{subpath}}";
```

{{Each export accepts these options:}}

- `{{option}}`: {{description}} (default: `{{value}}`).

## API Reference

### `{{mainExport}}({{params}})`

{{what it does.}}

- `{{param}}` (`{{type}}`) — {{description}}.
- Returns `{{return-type}}` — {{description}}.

```{{lang}}
{{api-example}}
```

## Requirements

- {{runtime}} {{min-version}}+
- {{other-requirement}}

## Contributing

{{how to contribute; link CONTRIBUTING.md if present.}}

## License

[{{license}}](LICENSE)
