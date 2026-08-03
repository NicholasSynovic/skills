<!--
  Fill-in skeleton for an application / web-app README. First-party skill content.
  Replace every {{token}} with a real value from the scan; delete this comment
  and every other HTML comment before shipping. No {{...}} may remain in output.

  Section order follows the Step 2 matrix for application, in inverted-pyramid
  order. Depth filter (Step 3a): minimal = Required only; standard = + Recommended;
  comprehensive = + Optional + extended sections from references/section-library.md.

  No badges and no centered title for apps (no registry presence).

  Few-shot — study these two filled title + one-liner pairs, then write your own
  in the same voice (product-focused, clear; what it does and who it's for):

    # Excalidraw
    An open-source virtual whiteboard for sketching hand-drawn-style diagrams.

    # Cal.com
    Scheduling infrastructure for everyone — the open-source Calendly alternative.
-->

# {{name}}

{{one-liner describing what the app does and who it is for}}

## Features

- **{{feature-one}}:** {{what it does}}.
- **{{feature-two}}:** {{what it does}}.
- **{{feature-three}}:** {{what it does}}.

## Getting Started

<!-- Getting Started replaces Install: readers clone and configure. -->

```bash
git clone https://github.com/{{owner}}/{{repo}}.git
cd {{repo}}
{{install-command}}
cp .env.example .env.local
{{run-command}}
```

Open [http://localhost:{{port}}](http://localhost:{{port}}).

## Environment Variables

<!-- Critical for apps; include a .env.example in the repo. -->

| Variable      | Description     | Required |
| ------------- | --------------- | -------- |
| `{{VAR_ONE}}` | {{description}} | Yes      |
| `{{VAR_TWO}}` | {{description}} | No       |

<!-- Recommended (standard+) -->

## Configuration

{{how configuration is loaded and the key options.}}

<!-- Recommended (standard+) -->

## Architecture

<!-- Rendered from the scanner's directory_structure; see the Step 3 note. -->

```
{{project-structure-tree}}
```

<!-- Optional (comprehensive): Tech Stack helps contributors -->

## Tech Stack

- [{{tech-one}}]({{url}}): {{role}}
- [{{tech-two}}]({{url}}): {{role}}
- [{{tech-three}}]({{url}}): {{role}}

## Contributing

{{how to contribute; link CONTRIBUTING.md if present.}}

## License

[{{license}}](LICENSE)
