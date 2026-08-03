# Dependencies

External tools required to run this skill's scripts (`scripts/scan_project.py`)
and its badge generation (Step 4, `pybadges`).

| Dependency | Minimum version | Check command            | Required? | Purpose                                                                                                                                                                           |
| ---------- | --------------- | ------------------------ | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tree`     | 2.3.2           | `tree --version`         | Yes       | Directory-structure scanning via `tree -J` in `scripts/scan_project.py`. The scanner emits a JSON error and exits non-zero if `tree` is missing or older.                         |
| `scc`      | 3.7.0           | `scc --version`          | Yes       | Code-line counting for existing READMEs via `scc --by-file -f json` in `scripts/scan_project.py`. The scanner emits a JSON error and exits non-zero if `scc` is missing or older. |
| `licensee` | 10.0.0          | `licensee version`       | Yes       | License detection via `licensee detect --json` in `scripts/scan_project.py`. The scanner emits a JSON error and exits non-zero if `licensee` is missing or older.                 |
| Python     | 3.11            | `python3 --version`      | Yes       | Runs `scripts/scan_project.py`; uses the stdlib `tomllib` (3.11+).                                                                                                                |
| `pybadges` | 3.0.1           | `python3 -m pybadges -v` | Yes       | Badge generation (Step 4). Renders each badge to a static SVG on stdout via `python3 -m pybadges`; the SVGs are committed and referenced by relative path.                        |
| `git`      | 2.0             | `git --version`          | No        | Enables owner/repo/default-branch detection from the `origin` remote. The scanner degrades gracefully (empty git fields) when absent.                                             |

## Notes

- **`tree`, `scc`, and `licensee` are hard requirements.** The scanner shells
  out to `tree -J` for the `directory_structure` field, to `scc --by-file -f
json` for existing-README line counts, and to `licensee detect --json` for
  license detection. Without a compatible version of any of them it returns
  `{"error": "..."}` on stdout and exits with a non-zero status.
- **License detection uses `licensee` exclusively.** The `license` field is the
  first `spdx_id` reported by `licensee detect --json`; it is `""` when no
  license is found or the top result is `NOASSERTION`.
- **`scc` respects `.gitignore` by default.** A gitignored README is still
  listed in `existing_readmes` (with headings), but its `line_count` reports 0.
- **`git` is optional.** Its absence only blanks the `git` fields; all other
  facts are still collected.
- **`pybadges` renders static SVGs, not URLs.** Install with `pip install
pybadges`; invoke as `python3 -m pybadges ... > badge.svg`. It produces a
  single flat github-style badge and has no `for-the-badge`/`flat-square`/
  `social`/`plastic` style variants. Badges are a snapshot at generation time and
  must be regenerated when the underlying value changes.
- **`pybadges` needs `imghdr` on Python 3.13+.** `imghdr` was removed from the
  stdlib in Python 3.13; `pybadges` 3.0.1 imports it at load time and will crash
  on _any_ invocation without it. On 3.13+ either install the `standard-imghdr`
  shim (`pip install standard-imghdr`) or run `pybadges` under Python 3.11/3.12.
