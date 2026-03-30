from __future__ import annotations

import logging
from pathlib import Path

import typer

import cv.build as build
from cv.settings import get_settings, setup_logging

setup_logging()
log = logging.getLogger(__name__)

app = typer.Typer()


@app.command()
def main(
    profile: str = typer.Option(
        "default", help="Profile name (data/profiles/<name>.yaml)"
    ),
) -> None:
    s = get_settings()
    resume_path = s.data_dir / "content.yaml"
    profile_path = s.data_dir / "profiles" / f"{profile}.yaml"

    require(resume_path)
    require(profile_path)

    resume = build.load_yaml(resume_path)
    prof = build.load_yaml(profile_path)

    resolved = build.resolve_resume(resume, prof)
    template = prof.get("template", "default")
    build.write_json(resolved, s.templates_dir / template / "content.json")


def require(path: Path) -> None:
    if not path.exists():
        log.error(f"file not found: {path}")
        raise typer.Exit(1)
