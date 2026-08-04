.PHONY: build clean

build:
	mkdir -p build
	zip -r -u build/readme-generator.skill readme-generator
	zip -r -u build/review-abilities.skill review-abilities

clean:
	rm -rf build
