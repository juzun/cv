.PHONY: build watch serve clean

PROFILE ?= default
PORT    ?= 8787

# One-shot build → PDF
build:
	uv run python scripts/build.py --profile $(PROFILE)

# Live-reload: regenerate JSON, then watch Typst → SVG + serve in browser
serve:
	@mkdir -p build/preview
	uv run python scripts/build.py --profile $(PROFILE)
	typst watch --root . \
		templates/$$(uv run python -c "import yaml; print(yaml.safe_load(open('data/profiles/$(PROFILE).yaml'))['template'])")/main.typ \
		build/preview/resume-{p}.svg &
	uv run python scripts/serve.py --port $(PORT)

# Watch Typst → PDF only (no browser)
watch:
	uv run python scripts/build.py --profile $(PROFILE)
	typst watch --root . \
		templates/$$(uv run python -c "import yaml; print(yaml.safe_load(open('data/profiles/$(PROFILE).yaml'))['template'])")/main.typ \
		build/resume.pdf

clean:
	rm -rf build/
