# CV

YAML content → Python → JSON → Typst → PDF.

## Setup

```bash
uv sync                          # install Python deps
# install Typst: https://github.com/typst/typst/releases
# install typst-live: https://github.com/ItsEthra/typst-live
```

## Commands

```bash
make build                       # compile PDF → data/output.pdf
make build PROFILE=ml_short      # use a specific profile
make serve                       # live preview in browser (typst-live)
make serve PROFILE=ml_short
make clean
```

## Structure

```
data/resume.yaml               ← all content (edit this)
data/profiles/default.yaml     ← which sections, summary variant, template
templates/default/             ← Typst template (main.typ + components.typ)
cv/                            ← Python build package
```

## Profiles

A profile (`data/profiles/<name>.yaml`) controls:
- `template` — which folder under `templates/` to use
- `summary_variant` — which summary from `resume.yaml`'s `summaries:` map
- `sections` — ordered list of sections to include

```bash
cp data/profiles/default.yaml data/profiles/myprofile.yaml
make build PROFILE=myprofile
```

## Adding a template

Create `templates/<name>/main.typ` + `components.typ`, set `template: <name>` in a profile.
The build writes `templates/<name>/content.json` — read it as `json("content.json")` in `main.typ`.
