import json
import logging
from pathlib import Path
from typing import Any

import yaml

log = logging.getLogger(__name__)


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
        log.warning(
            "summary variant '%s' not found, falling back to 'default'", summary_variant
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
    log.info("Wrote %s", path)
