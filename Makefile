# Package each first-party skill into build/<skill>.skill (a zip).
# Uses `git archive` so only git-tracked files are bundled: the gitignored
# vendored corpus (readme-generator/references/vendor) and editor/OS cruft are
# excluded automatically, and each build writes a fresh archive (no appends).
# REF selects the tree to package; it defaults to the last commit (HEAD), so
# uncommitted working-tree changes are NOT included — commit first, or override
# with `make build REF=<branch-or-sha>`.

.PHONY: build check clean

REF ?= HEAD

# Discovered, not hand-maintained: every directory holding a SKILL.md is a
# first-party skill and gets packaged. Adding a skill needs no Makefile edit.
SKILLS := $(patsubst %/SKILL.md,%,$(wildcard */SKILL.md))

build:
	mkdir -p build
	@for skill in $(SKILLS); do \
		echo "git archive $$skill"; \
		git archive --format=zip -o "build/$$skill.skill" $(REF) "$$skill" || exit 1; \
	done

# Repo-level validation: SKILL.md frontmatter and intra-skill relative links.
check:
	python3 scripts/check_skills.py

clean:
	rm -rf build

create-dev:
	pre-commit install
	pre-commit autoupdate
