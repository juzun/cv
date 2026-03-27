# CV Pipeline

Data-driven resume: YAML content → Python build script → JSON → Typst → PDF.

## Prerequisites

- **Python 3.13+** with `pyyaml` (`uv sync` to install)
- **Typst CLI** — [install](https://github.com/typst/typst/releases) or `cargo install typst-cli`

## Usage

```bash
# Build with default profile
make build

# Build with a specific profile
make build PROFILE=short

# Watch for Typst template changes (live reload)
make watch

# Clean build artifacts
make clean
```

Or call the script directly:

```bash
python scripts/build.py --profile default --output build/resume.pdf
```

## Structure

```
data/resume.yaml            ← all CV content (source of truth)
data/profiles/default.yaml  ← template + variant + section order
templates/mckinsey/          ← Typst template (main.typ + components.typ)
scripts/build.py             ← build orchestration
build/                       ← generated JSON + PDF (gitignored)
```

## Switching Variants

Edit `data/profiles/default.yaml`:

- **`summary_variant`**: picks from `summaries` in `resume.yaml` (`default`, `short`, `ml_focused`)
- **`sections`**: ordered list of sections to include — reorder or remove entries
- **`template`**: switch rendering template (e.g., `mckinsey`)

To create a new profile, copy `data/profiles/default.yaml` to a new file and adjust.

## Adding a Template

1. Create `templates/<name>/main.typ` and `components.typ`
2. Set `template: <name>` in a profile
3. `make build PROFILE=<your-profile>`