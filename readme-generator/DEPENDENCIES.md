# Dependencies

External tools required to run this skill's scripts (`scripts/scan_project.py`)
and its badge generation (Step 4, `pybadges`).

| Dependency | Minimum version | Check command            | Required? | Purpose                                                                                                                                                                                                                      |
| ---------- | --------------- | ------------------------ | --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tree`     | 2.3.2           | `tree --version`         | Yes       | Directory-structure scanning via `tree -J` in `scripts/scan_project.py`. The scanner emits a JSON error and exits non-zero if `tree` is missing or older.                                                                    |
| `licensee` | 10.0.0          | `licensee version`       | Yes       | License detection via `licensee detect --json` in `scripts/scan_project.py` (with a manifest SPDX fallback). The scanner emits a JSON error and exits non-zero if `licensee` is missing or older.                            |
| Python     | 3.11            | `python3 --version`      | Yes       | Runs `scripts/scan_project.py`; uses the stdlib `tomllib` (3.11+).                                                                                                                                                           |
| `scc`      | 3.7.0           | `scc --version`          | No        | Code-line counting for existing READMEs via `scc --by-file -f json` in `scripts/scan_project.py`. Optional: when absent the `existing_readmes[].line_count` field degrades to `0` and the scan still completes.              |
| `pybadges` | 3.0.1           | `python3 -m pybadges -v` | Yes       | Badge generation (Step 4). Renders each badge to a static SVG on stdout via `python3 -m pybadges`; the SVGs are committed and referenced by relative path. Install the maintained fork (see notes) for Python 3.13+ support. |
| `git`      | 2.0             | `git --version`          | No        | Enables owner/repo detection from the `origin` remote, plus the latest tag. The scanner degrades gracefully (empty git fields) when absent.                                                                                  |

## Notes

- **`tree` and `licensee` are the hard requirements.** The scanner shells out to
  `tree -J` for the `directory_structure` field and to `licensee detect --json`
  for license detection. Without a compatible version of either it returns
  `{"error": "..."}` on stdout and exits with a non-zero status.
- **License detection falls back to the manifest.** The `license` field is the
  first `spdx_id` reported by `licensee detect --json`. When that is unavailable
  (detection fails, nothing found, or the top result is `NOASSERTION`), the
  scanner reads the SPDX `license` field from `package.json`, `Cargo.toml`
  (`[package]`), or `pyproject.toml` (`[project].license`, string or
  `{text = "..."}`). It is `""` only when neither source yields a value.
- **`scc` is optional.** Its only consumer is the `existing_readmes[].line_count`
  field. When `scc` is missing, too old, or fails, that count degrades to `0` and
  every other fact is still collected — the scan does not abort.
- **`scc` respects `.gitignore` by default.** A gitignored README is still
  listed in `existing_readmes` (with headings), but its `line_count` reports 0.
  A `0` therefore means "unavailable or skipped", not necessarily "empty file".
- **`git` is optional.** Its absence only blanks the `git` fields (`owner`,
  `repo`); all other facts are still collected.
- **`pybadges` renders static SVGs, not URLs.** Invoke as
  `python3 -m pybadges ... > badge.svg`. It produces a single flat github-style
  badge and has no `for-the-badge`/`flat-square`/`social`/`plastic` style
  variants. Badges are a snapshot at generation time and must be regenerated when
  the underlying value changes.
- **Install `pybadges` from the maintained fork.** Upstream `pybadges` 3.0.1
  imports the stdlib `imghdr`, removed in Python 3.13, so it crashes on _any_
  invocation under 3.13+. The fork replaces that import with the maintained
  `filetype` library and runs on Python 3.9 through 3.14:

    ```bash
    pip install git+https://github.com/NicholasSynovic/pybadges
    ```

    No `standard-imghdr` shim and no downgraded interpreter are needed.
