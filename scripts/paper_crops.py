"""Figures and tables cut from the assigned papers, for slides that show the source.

A slide that redraws a paper's result is easier to read than the paper, and
harder to check against it. So the Week 6 deck shows the original first -- the
crop the student has already met in the reading -- and redraws it second. This
module is where the originals come from.

Nothing cropped is committed. Each paper is fetched from arXiv on first use
into ``.paper_cache/`` (gitignored), and each crop is re-rendered from the PDF
on every build, the same rule as every other generated slide: the script is
the source of truth.

Papers are named by their id in ``data/resources.yml`` and their URL is read
from there -- the repository's one-place-for-a-fact rule. What this module
adds is an arXiv *version*: the boxes below are page coordinates, and a
revised version moves them. Bumping a version means re-checking every box
that points at that paper (``python paper_crops.py`` writes a contact sheet).
"""

import os
import urllib.request

import pypdfium2 as pdfium
import yaml
from PIL import Image

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES = os.path.join(SCRIPT_DIR, "..", "data", "resources.yml")
CACHE = os.path.join(SCRIPT_DIR, ".paper_cache")

# resource id -> the arXiv version the crop boxes were measured on.
VERSIONS = {
    "wei-2022-chain-of-thought": "v6",
    "cot-mirage": "v6",
}

# name -> (resource id, page number as printed in the PDF viewer (1-based),
#          box in PDF points measured from the TOP-left: x0, top, x1, bottom)
# A list of boxes is stacked top to bottom -- for a figure whose axis labels sit
# below rows the slide does not need (Wei's Figure 4 is a 3 x 3 grid).
CROPS = {
    "wei_fig1_prompts": ("wei-2022-chain-of-thought", 1, (106, 450, 506, 642)),
    "wei_fig4_scale": ("wei-2022-chain-of-thought", 5, [(300, 74, 510, 206), (300, 360, 510, 386)]),
    "wei_fig5_ablation": ("wei-2022-chain-of-thought", 6, (360, 70, 512, 312)),
    "mirage_fig2_framework": ("cot-mirage", 5, (58, 72, 532, 206)),
    "mirage_tab1_collapse": ("cot-mirage", 7, (170, 165, 428, 243)),
    "mirage_tab2_unfaithful": ("cot-mirage", 7, (148, 580, 448, 666)),
    "mirage_fig4_sft": ("cot-mirage", 8, (319, 88, 530, 225)),
    "mirage_fig6_steps": ("cot-mirage", 9, (60, 80, 536, 204)),
    "mirage_fig7_format": ("cot-mirage", 9, (60, 366, 536, 508)),
}


def _url(resource_id):
    with open(RESOURCES, encoding="utf-8") as f:
        entry = next(r for r in yaml.safe_load(f) if r["id"] == resource_id)
    abs_url = entry["url"]
    if "arxiv.org/abs/" not in abs_url:
        raise SystemExit(f"{resource_id} is not an arXiv abstract URL: {abs_url}")
    return abs_url.replace("/abs/", "/pdf/") + VERSIONS[resource_id]


def _pdf(resource_id):
    os.makedirs(CACHE, exist_ok=True)
    url = _url(resource_id)
    path = os.path.join(CACHE, url.rsplit("/", 1)[-1] + ".pdf")
    if not os.path.exists(path):
        print(f"fetching {url}")
        req = urllib.request.Request(url, headers={"User-Agent": "llms-and-you slide build"})
        with urllib.request.urlopen(req, timeout=60) as r, open(path, "wb") as f:
            f.write(r.read())
    return path


def crop(name, scale=4.0):
    """Render one registered crop as a PIL image, `scale` pixels per PDF point.

    Rendering the page at 4x and cutting afterwards keeps the text sharp when
    a small figure is blown up to fill half a projected slide.
    """
    resource_id, page_no, boxes = CROPS[name]
    doc = pdfium.PdfDocument(_pdf(resource_id))
    page = doc[page_no - 1]
    img = page.render(scale=scale).to_pil().convert("RGB")
    doc.close()
    parts = [
        img.crop(tuple(round(v * scale) for v in b))
        for b in (boxes if isinstance(boxes, list) else [boxes])
    ]
    out = Image.new("RGB", (max(p.width for p in parts), sum(p.height for p in parts)), "white")
    y = 0
    for p in parts:
        out.paste(p, (0, y))
        y += p.height
    return out


def contact_sheet(path):
    """Every crop on one image, for checking the boxes after a version bump."""
    imgs = [crop(n, scale=2.0) for n in CROPS]
    w = max(i.width for i in imgs)
    sheet = Image.new("RGB", (w, sum(i.height + 20 for i in imgs)), "#888888")
    y = 0
    for i in imgs:
        sheet.paste(i, (0, y))
        y += i.height + 20
    sheet.save(path)
    print(f"saved {path}")


if __name__ == "__main__":
    contact_sheet(os.path.join(SCRIPT_DIR, "demo_photos", "paper_crops_preview.png"))
