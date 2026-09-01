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
DECK = SCRIPTS / "W02_How_Text_Becomes_Numbers.pptx"
DECK_PRINT = SCRIPTS / "W02_How_Text_Becomes_Numbers_print.pptx"

sys.path.insert(0, str(SCRIPTS))

from deck_order import ORDER  # noqa: E402


def main() -> None:
    missing = [f for f in ORDER if not (PHOTOS / f).exists()]
    missing += [d.name for d in (DECK, DECK_PRINT) if not d.exists()]
    if missing:
        gone = missing
        raise SystemExit(
            f"slides media not generated yet ({len(gone)} file(s) missing, "
            f"first: {gone[0]}). Run the generators:\n"
            "  cd scripts && for f in gen_*.py; do python $f; done "
            "&& python build_deck.py\n"
            "(needs `pip install -e '.[slides]'`)"
        )

    for name in ORDER:
        with mkdocs_gen_files.open(f"slides/media/{name}", "wb") as out:
            out.write((PHOTOS / name).read_bytes())
    for deck in (DECK, DECK_PRINT):
        with mkdocs_gen_files.open(f"slides/media/{deck.name}", "wb") as out:
            out.write(deck.read_bytes())


main()
