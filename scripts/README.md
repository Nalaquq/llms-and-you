# Slide-generation scripts

GIF/PNG slide generators for lecture decks, following the pattern from the
CV course (`~/Desktop/cv_course/scripts/`): matplotlib figures assembled into
GIFs with PIL — phase-based builds, `loop=1`, 60-second last-frame hold —
restyled dark to match this site's Material slate theme, with 3blue1brown-style
motion (eased tweens, vectors, minimal on-screen text).

Shared style lives in `style_dark.py`. Every generated slide carries a footer
naming the study-guide entries it teaches, so the deck and
`docs/study-guide.md` stay in step.

## Build the decks

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
`_final.png` of its finished state) and two files per deck: the animated
`.pptx` for presenting, and `..._print.pptx` — final frames as stills — for
printing notes pages and handouts.

`deck_order.py` is the registry: one `Deck` per lecture, holding its teaching
order, its filename stem, and whether the site publishes it. Adding a deck
means adding an entry there and generator scripts named for its slides;
nothing else needs to change.

| Deck | Slides | On the site |
|:---|:---|:---|
| `W02_How_Text_Becomes_Numbers` | 27 | yes |
| `W03_Attention_and_the_Transformer` | 31 | yes |

Week 3 is a twenty-minute review (five representations, then the
perceptron, CNN and RNN, then the three problems the 2017 paper answers)
followed by the transformer itself, one head at a time.

The head-anatomy slides (s14–s17) and the mask (s22) take their pictures
from 3Blue1Brown's *Attention in transformers, step-by-step* — the Chapter 6
video assigned for the week, whose source is `_2024/transformers/attention.py`
in the `3b1b/videos` repository: query and key as two arrows that line up or
do not; the grid of every word against every word, a dot per cell sized by
the score; softmax normalising that grid in place; the mask stamping minus
infinity on the not-yet-written cells before the softmax; and the value as a
nudge added to the vector the word arrived with. One departure, on purpose:
the video runs queries across the top and softmax down a column; these grids
put the asking word on the rows and softmax along a row, because that is the
orientation of every heatmap in Thursday's notebook. The grid furniture lives
in `style_dark.py` so the three grid slides cannot drift apart.

The Week 3 architecture slides began as ports of the computer-vision course's
scripts (`~/Desktop/cv_course/scripts/generate_perceptron_explainer_slides.py`,
`generate_cnn_slides.py`). The perceptron now runs on the classic example
instead — bedrooms and miles to downtown in, a price out, the arithmetic built
term by term on screen — because the room needs to watch one unit calculate
before it can follow one failing. The CNN and RNN slides then introduce
themselves as that same unit rearranged: copied along a sentence with shared
weights, or handed its own previous answer. Both of those keep a sentence as
the input, since the sentence is where the transformer's argument lives. There
was no RNN script to port; that one is new. PowerPoint
renders a GIF's first frame anywhere static, which for a build-up animation
is nearly blank; the print edition exists because of that. Nothing generated
is committed; the scripts are the source of truth.

GIFs animate in PowerPoint's slideshow mode (not in the editor). Each plays
once per slide visit and holds its final frame. Notes pages carry explicit
16:9 geometry because python-pptx's default notes layout is 4:3 and renders
badly in PowerPoint otherwise.
