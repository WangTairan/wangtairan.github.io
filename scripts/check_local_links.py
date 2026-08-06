#!/usr/bin/env python3
"""Validate local HTML and CSS references in the static site."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


SITE_ROOT = Path(__file__).resolve().parents[1] / "static-html"
CSS_URL = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)")
IGNORED_SCHEMES = {"data", "http", "https", "mailto", "tel", "javascript"}


class ReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        del tag
        for name, value in attrs:
            if name in {"href", "src"} and value:
                self.references.append(value)


def is_local(reference: str) -> bool:
    parsed = urlsplit(reference)
    return not parsed.scheme and not parsed.netloc and reference != "#"


def resolve_reference(source: Path, reference: str) -> Path | None:
    parsed = urlsplit(reference)
    if parsed.scheme in IGNORED_SCHEMES or parsed.netloc or not parsed.path:
        return None

    if parsed.path.startswith("/"):
        target = SITE_ROOT / parsed.path.lstrip("/")
    else:
        target = source.parent / parsed.path

    if target.is_dir():
        target /= "index.html"
    return target.resolve()


def html_references(path: Path) -> list[str]:
    parser = ReferenceParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.references


def css_references(path: Path) -> list[str]:
    content = path.read_text(encoding="utf-8")
    return [match.group(2) for match in CSS_URL.finditer(content)]


def main() -> int:
    missing: list[tuple[Path, str, Path]] = []
    checked = 0

    sources = [
        *((path, html_references(path)) for path in SITE_ROOT.rglob("*.html")),
        *((path, css_references(path)) for path in SITE_ROOT.rglob("*.css")),
    ]

    for source, references in sources:
        for reference in references:
            if not is_local(reference):
                continue
            target = resolve_reference(source, reference)
            if target is None:
                continue
            checked += 1
            if not target.exists():
                missing.append((source, reference, target))

    if missing:
        for source, reference, target in missing:
            print(
                f"MISSING: {source.relative_to(SITE_ROOT)} -> {reference} "
                f"({target})"
            )
        return 1

    print(f"Checked {checked} local references: all targets exist.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
