<!--
  Fill-in skeleton for CONTRIBUTING.md. First-party skill content.
  Replace every {{token}} with a real value from the scan; delete this comment
  before shipping. No {{...}} may remain in output. Drop sections that do not
  apply (e.g. Code of Conduct if there is no CODE_OF_CONDUCT.md).
-->

# Contributing to {{name}}

Thank you for your interest in contributing! This document covers how to report
issues and submit changes.

## How Can I Contribute?

### Reporting Bugs

- Check existing issues first.
- Include reproduction steps and environment details.

### Suggesting Features

- Check existing feature requests first.
- Explain the use case, not just the solution.

### Pull Requests

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/{{short-name}}`.
3. Make your changes and add or update tests.
4. Run the test suite: `{{test-command}}`.
5. Commit using conventional commits: `git commit -m 'feat: {{summary}}'`.
6. Push to your fork: `git push origin feature/{{short-name}}`.
7. Open a Pull Request.

## Development Setup

```bash
git clone https://github.com/{{your-username}}/{{repo}}.git
cd {{repo}}
git remote add upstream https://github.com/{{owner}}/{{repo}}.git
{{install-command}}
```

## Coding Standards

- Follow the existing code style.
- Write meaningful commit messages.
- Add tests for new behavior.
- Update documentation as needed.

## Testing

```bash
{{test-command}}
```

## Questions?

Open an issue{{ or reach out via <contact>}}.
