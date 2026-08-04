# Package each first-party skill into build/<skill>.skill (a zip).
# Uses `git archive` so only git-tracked files are bundled: the gitignored
# vendored corpus (readme-generator/references/vendor) and editor/OS cruft are
# excluded automatically, and each build writes a fresh archive (no appends).
# REF selects the tree to package; it defaults to the last commit (HEAD), so
# uncommitted working-tree changes are NOT included — commit first, or override
# with `make build REF=<branch-or-sha>`.

.PHONY: build clean

REF ?= HEAD

build:
	mkdir -p build
	git archive --format=zip -o build/readme-generator.skill $(REF) readme-generator
	git archive --format=zip -o build/review-abilities.skill $(REF) review-abilities

clean:
	rm -rf build
