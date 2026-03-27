"""Build script: YAML resume + profile → JSON → Typst → PDF."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
TEMPLATES_DIR = ROOT / "templates"
BUILD_DIR = ROOT / "build"


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def resolve_resume(
    resume: dict[str, Any],
    profile: dict[str, Any],
) -> dict[str, Any]:
    """Apply profile selections to resume data and return a flat structure."""
    summary_variant = profile.get("summary_variant", "default")
    summaries = resume.get("summaries", {})
    if summary_variant not in summaries:
        print(
            f"Warning: summary variant '{summary_variant}' not found, "
            f"falling back to 'default'.",
            file=sys.stderr,
        )
        summary_variant = "default"

    section_order = profile.get(
        "sections",
        [
            "summary",
            "experience",
            "education",
            "skills",
            "certifications",
            "languages",
            "hobbies",
        ],
    )

    sections: list[dict[str, Any]] = []
    for key in section_order:
        if key == "summary":
            sections.append({"type": "summary", "content": summaries[summary_variant]})
        elif key in resume:
            sections.append({"type": key, "content": resume[key]})

    return {
        "meta": resume["meta"],
        "sections": sections,
    }


def write_json(data: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Wrote {path}")


def compile_typst(template: str, output: Path) -> None:
    typst_bin = shutil.which("typst")
    if typst_bin is None:
        print(
            "Error: 'typst' not found on PATH.\n"
            "Install via: cargo install typst-cli\n"
            "  or: https://github.com/typst/typst/releases",
            file=sys.stderr,
        )
        sys.exit(1)

    template_entry = TEMPLATES_DIR / template / "main.typ"
    if not template_entry.exists():
        print(
            f"Error: template '{template}' not found at {template_entry}",
            file=sys.stderr,
        )
        sys.exit(1)

    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [typst_bin, "compile", "--root", str(ROOT), str(template_entry), str(output)]
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Typst error:\n{result.stderr}", file=sys.stderr)
        sys.exit(result.returncode)
    print(f"Wrote {output}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Build resume PDF from YAML data + Typst template."
    )
    parser.add_argument(
        "--profile",
        default="default",
        help="Profile name (file in data/profiles/, without .yaml). Default: 'default'.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output PDF path. Default: build/resume.pdf.",
    )
    args = parser.parse_args(argv)

    resume_path = DATA_DIR / "resume.yaml"
    profile_path = DATA_DIR / "profiles" / f"{args.profile}.yaml"

    if not resume_path.exists():
        print(f"Error: resume data not found at {resume_path}", file=sys.stderr)
        sys.exit(1)
    if not profile_path.exists():
        print(f"Error: profile not found at {profile_path}", file=sys.stderr)
        sys.exit(1)

    resume = load_yaml(resume_path)
    profile = load_yaml(profile_path)

    resolved = resolve_resume(resume, profile)

    json_path = BUILD_DIR / "resume.json"
    write_json(resolved, json_path)

    template_name = profile.get("template", "mckinsey")
    output_path = Path(args.output) if args.output else BUILD_DIR / "resume.pdf"

    compile_typst(template_name, output_path)


if __name__ == "__main__":
    main()
