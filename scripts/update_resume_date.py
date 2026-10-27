#!/usr/bin/env python3
"""Stamp the resume's actual update date into the static homepage."""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
import re
import subprocess
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
DATE_TAG = re.compile(r'<time id="resume-updated" datetime="[^"]*">[^<]*</time>')
LONDON = ZoneInfo("Europe/London")


def resume_date(root: Path, pdf: Path) -> date:
    """Use file history, not checkout time; use mtime for local, uncommitted PDFs."""
    relative = pdf.relative_to(root).as_posix()
    try:
        unchanged = subprocess.run(
            ["git", "diff", "--quiet", "HEAD", "--", relative],
            cwd=root, capture_output=True,
        )
        if unchanged.returncode == 0:
            history = subprocess.run(
                ["git", "log", "-1", "--format=%cI", "--", relative],
                cwd=root, capture_output=True, text=True, check=True,
            ).stdout.strip()
            if history:
                return datetime.fromisoformat(history.replace("Z", "+00:00")).astimezone(LONDON).date()
    except (OSError, subprocess.CalledProcessError):
        pass
    return datetime.fromtimestamp(pdf.stat().st_mtime, LONDON).date()


def stamp_date(html: str, updated: date) -> str:
    if len(DATE_TAG.findall(html)) != 1:
        raise ValueError("Expected exactly one resume-updated time element")
    label = f"{updated.day} {MONTHS[updated.month - 1]} {updated.year}"
    return DATE_TAG.sub(
        f'<time id="resume-updated" datetime="{updated.isoformat()}">{label}</time>',
        html,
    )


def main() -> None:
    pdf = ROOT / "static-html/resources/personal/resume.pdf"
    homepage = ROOT / "static-html/index.html"
    updated = resume_date(ROOT, pdf)
    original = homepage.read_text(encoding="utf-8")
    rendered = stamp_date(original, updated)
    if rendered != original:
        homepage.write_text(rendered, encoding="utf-8")
    print(f"Resume updated: {updated.isoformat()}")


if __name__ == "__main__":
    main()
