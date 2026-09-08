"""Publish the lecture-deck media into the site at build time.

Same philosophy as ``gen_sessions.py`` (ADR-001, ADR-019): the generator
scripts in ``scripts/`` are the committed source of truth, their GIF/PNG/PPTX
outputs are gitignored, and the site picks the outputs up at build time. CI
runs the generators before ``mkdocs build``; locally, run them once (see
``scripts/README.md``) or this fails loud with the command you need.
"""

from __future__ import annotations

import sys
from pathlib import Path

import mkdocs_gen_files

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
PHOTOS = SCRIPTS / "demo_photos"

sys.path.insert(0, str(SCRIPTS))

from deck_order import DECKS  # noqa: E402


def main() -> None:
    # A deck the slides page does not show yet is not published, and its media
    # is not required to build the site -- see `publish` in deck_order.py.
    decks = [d for d in DECKS if d.publish]

    files = []
    for deck in decks:
        files += [PHOTOS / name for name in deck.order]
        files += [SCRIPTS / f"{deck.stem}.pptx", SCRIPTS / f"{deck.stem}_print.pptx"]

    missing = [f.name for f in files if not f.exists()]
    if missing:
        raise SystemExit(
            f"slides media not generated yet ({len(missing)} file(s) missing, "
            f"first: {missing[0]}). Run the generators:\n"
            "  cd scripts && for f in gen_*.py; do python $f; done "
            "&& python build_deck.py\n"
            "(needs `pip install -e '.[slides]'`)"
        )

    for path in files:
        with mkdocs_gen_files.open(f"slides/media/{path.name}", "wb") as out:
            out.write(path.read_bytes())


main()
