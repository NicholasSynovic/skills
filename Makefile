.PHONY: build

build:
	mkdir -p build
	zip -r build/readme-generator.skill readme-generator
	zip -r build/review-abilities.skill review-abilities
