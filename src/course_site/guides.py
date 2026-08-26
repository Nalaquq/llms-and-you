"""The hand-written guides in ``docs/guides/``, read as data.

Sessions reference a guide the way they reference a reading -- by id, never by
path -- so a session can be checked at build time for pointing somewhere real.
The guide's own file is the source of truth for its title and its anchors; there
is no second place to update when a heading is reworded.
"""

from __future__ import annotations

import functools
import re
from pathlib import Path

from .models import Guide

GUIDES_DIR = Path(__file__).resolve().parents[2] / "docs" / "guides"

_H1 = re.compile(r"^#\s+(.+?)\s*$", re.M)
_HEADING = re.compile(r"^(#{2,6})\s+(.+?)\s*$", re.M)
_EXPLICIT_ANCHOR = re.compile(r"\{\s*#([\w-]+)\s*\}\s*$")
_INLINE = re.compile(r"[*`_]|\[(?P<text>[^\]]*)\]\([^)]*\)")


def _plain(text: str) -> str:
    """Heading text as a reader sees it, with inline Markdown stripped."""
    return _INLINE.sub(lambda m: m.group("text") or "", text).strip()


def _slug(text: str) -> str:
    """The anchor mkdocs' toc extension will generate for this heading.

    Mirrors ``markdown.extensions.toc.slugify`` at its default settings. If that
    ever drifts, ``test_guide_anchors_match_the_built_site`` catches it.
    """
    value = re.sub(r"[^\w\s-]", "", _plain(text)).strip().lower()
    return re.sub(r"[-\s]+", "-", value)


def _parse(path: Path) -> Guide:
    text = path.read_text(encoding="utf-8")

    title = _H1.search(text)
    if not title:
        raise ValueError(f"guide {path.name} has no top-level heading to use as its title")

    sections: dict[str, str] = {}
    for _, heading in _HEADING.findall(text):
        explicit = _EXPLICIT_ANCHOR.search(heading)
        label = _plain(_EXPLICIT_ANCHOR.sub("", heading))
        sections[explicit.group(1) if explicit else _slug(heading)] = label

    return Guide(id=path.stem, title=_plain(title.group(1)), sections=sections)


@functools.cache
def load_guides() -> dict[str, Guide]:
    """Every guide except the index, which is a directory of the others."""
    found = (_parse(p) for p in sorted(GUIDES_DIR.glob("*.md")) if p.stem != "index")
    return {g.id: g for g in found}


def split_ref(ref: str) -> tuple[str, str | None]:
    """``'setup#week-1-...'`` -> ``('setup', 'week-1-...')``."""
    guide, _, anchor = ref.partition("#")
    return guide, anchor or None
