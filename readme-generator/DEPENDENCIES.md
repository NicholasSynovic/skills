# Dependencies

External tools required to run this skill's scripts (primarily
`scripts/scan_project.py`).

| Dependency | Minimum version | Check command | Required? | Purpose |
| --- | --- | --- | --- | --- |
| `tree` | 2.3.2 | `tree --version` | Yes | Directory-structure scanning via `tree -J` in `scripts/scan_project.py`. The scanner emits a JSON error and exits non-zero if `tree` is missing or older. |
| `scc` | 3.7.0 | `scc --version` | Yes | Code-line counting for existing READMEs via `scc --by-file -f json` in `scripts/scan_project.py`. The scanner emits a JSON error and exits non-zero if `scc` is missing or older. |
| Python | 3.11 | `python3 --version` | Yes | Runs `scripts/scan_project.py`; uses the stdlib `tomllib` (3.11+). |
| `git` | 2.0 | `git --version` | No | Enables owner/repo/default-branch detection from the `origin` remote. The scanner degrades gracefully (empty git fields) when absent. |

## Notes

- **`tree` and `scc` are hard requirements.** The scanner shells out to
  `tree -J` for the `directory_structure` field and to `scc --by-file -f json`
  for existing-README line counts. Without a compatible version of either it
  returns `{"error": "..."}` on stdout and exits with a non-zero status.
- **`scc` respects `.gitignore` by default.** A gitignored README is still
  listed in `existing_readmes` (with headings), but its `line_count` reports 0.
- **`git` is optional.** Its absence only blanks the `git` fields; all other
  facts are still collected.
