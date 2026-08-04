<!--
  Fill-in skeleton for a monorepo README. First-party skill content.
  Replace every {{token}} with a real value from the scan; delete this comment
  and every other HTML comment before shipping. No {{...}} may remain in output.

  Section order follows the Step 2 matrix for monorepo, in inverted-pyramid order.
  Depth filter (Step 3a): minimal = Required only; standard = + Recommended;
  comprehensive = + Optional + extended sections from references/section-library.md.

  No badges and no version column here (no registry presence). The Packages /
  Components table is the centerpiece; drive it from the scanner's `packages` list
  and link each package to its directory (which should have its own README).

  Few-shot — study these two filled title + one-liner pairs, then write your own
  in the same voice (organized, scannable):

    # Turborepo
    High-performance build system for JavaScript and TypeScript monorepos.

    # Nx
    Smart monorepos with fast CI — one workspace, many apps and libraries.
-->

# {{name}}

<!-- No badges for monorepo: no registry presence (Step 2b). Omission is deliberate — do not add a badge slot here. -->

{{one-liner}}

## Getting Started

```bash
git clone https://github.com/{{owner}}/{{repo}}.git
cd {{repo}}
{{install-command}}
{{run-command}}
```

## Packages

<!-- One row per entry in the scanner's `packages` list. -->

| Package                   | Purpose          |
| ------------------------- | ---------------- |
| [`{{pkg-a}}`]({{path-a}}) | {{what it does}} |
| [`{{pkg-b}}`]({{path-b}}) | {{what it does}} |

<!-- Recommended (standard+) -->

## Requirements

- {{runtime}} {{min-version}}+ ({{package-manager}}, see `packageManager` in `package.json`)
- {{additional-runtime}}

<!-- Recommended (standard+) -->

## Common commands

```bash
{{build-command}}            # build all workspaces
{{test-command}}             # run all tests
{{project-specific-command}} # {{what it does}}
```

<!-- Optional (comprehensive) -->

## Architecture

<!-- Rendered from the scanner's directory_structure; see the Step 3 note. -->

```
{{project-structure-tree}}
```

## Contributing

{{how to contribute; see individual package READMEs for package-specific setup.}}

## License

[{{license}}](LICENSE)
