.PHONY: build serve clean

PROFILE  ?= default
TEMPLATE ?= default

# generate JSON resume from YAML resume and compile PDF from typst main
build:
	uv run cv-build --profile $(PROFILE)
	typst compile templates/$(TEMPLATE)/main.typ data/output.pdf

# generate JSON resume from YAML resume and launch live preview in browser
serve:
	uv run cv-build --profile $(PROFILE)
	typst-live templates/$(TEMPLATE)/main.typ

clean:
	rm -rf data/output.pdf templates/$(TEMPLATE)/content.json

