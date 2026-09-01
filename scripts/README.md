# Slide-generation scripts

GIF/PNG slide generators for lecture decks, following the pattern from the
CV course (`~/Desktop/cv_course/scripts/`): matplotlib figures assembled into
GIFs with PIL — phase-based builds, `loop=1`, 60-second last-frame hold —
restyled dark to match this site's Material slate theme, with 3blue1brown-style
motion (eased tweens, vectors, minimal on-screen text).

Shared style lives in `style_dark.py`. Every generated slide carries a footer
naming the study-guide entries it teaches, so the deck and
`docs/study-guide.md` stay in step.

## Build the Week 2 deck

The project venv carries everything (matplotlib, numpy, pillow,
python-pptx). Activate it once, then:

```bash
# macOS / Linux
source .venv/bin/activate
cd scripts
for f in gen_*.py; do python "$f"; done
python build_deck.py
```

```powershell
# Windows (PowerShell) — same steps, different paths
.venv\Scripts\Activate.ps1
cd scripts
Get-ChildItem gen_*.py | ForEach-Object { python $_.Name }
python build_deck.py
```

Outputs land in `demo_photos/` (a GIF per animated slide, plus a full-res
`_final.png` of its finished state) and two decks: the animated
`W02_How_Text_Becomes_Numbers.pptx` for presenting, and `..._print.pptx` —
final frames as stills — for printing notes pages and handouts. PowerPoint
renders a GIF's first frame anywhere static, which for a build-up animation
is nearly blank; the print edition exists because of that. Nothing generated
is committed; the scripts are the source of truth.

GIFs animate in PowerPoint's slideshow mode (not in the editor). Each plays
once per slide visit and holds its final frame. Notes pages carry explicit
16:9 geometry because python-pptx's default notes layout is 4:3 and renders
badly in PowerPoint otherwise.
