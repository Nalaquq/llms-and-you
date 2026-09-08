"""Render the syllabus and calendar to a PDF for submission to the College.

    python scripts/build_syllabus_pdf.py        # -> LLMs-and-You-Syllabus-Fall-2026.pdf

The PDF is built from ``docs/syllabus.md`` and the same macros the website
calls, so it carries the same dates, the same grading weights and the same
policies as the site. It is generated, never edited, and never committed --
identical treatment to the session pages and the lecture decks (ADR-001,
ADR-019, ADR-022).

Deliberately NOT a print of the website. WeasyPrint is given a small
purpose-built stylesheet instead of the Material theme, because a syllabus
handed to a dean is a paper document with margins, page numbers and a running
header, not a screenshot of a web page.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import jinja2  # noqa: E402
import markdown  # noqa: E402
import yaml  # noqa: E402

from course_site import macros  # noqa: E402

# The same extension list mkdocs.yml gives the site, minus the ones that only
# make sense in a browser (tabbed content, clipboard buttons, emoji sprites).
EXTENSIONS = [
    "abbr",
    "admonition",
    "attr_list",
    "def_list",
    "footnotes",
    "md_in_html",
    "tables",
    "pymdownx.betterem",
    "pymdownx.caret",
    "pymdownx.mark",
    "pymdownx.smartsymbols",
    "pymdownx.tilde",
]

# Material renders these as SVG icons and shows their `title` on hover. Print
# has neither, so an icon either becomes words or it becomes noise. The ones
# that carry information in the calendar are spelled out; the decorative ones
# (an envelope beside an email address) are dropped.
ICON_TEXT = {
    "material-flag-checkered": "(deliverable due)",
    "material-account-clock-outline": "(individual meetings)",
    "material-close-octagon": "(no generative AI)",
    "material-check": "(generative AI permitted)",
    # In the contact block these icons ARE the separators. Removing them ran
    # the name, the address and the office into one word.
    "material-email-outline": "·",
    "material-map-marker-outline": "·",
}
# Matches the shortcode plus any attr_list block glued to it, so the raw
# `{ title='...' }` never reaches the page either.
ICON = re.compile(r"\s*:(material-[a-z0-9-]+):\s*(\{[^}\n]*\})?")


def deiconify(text: str) -> str:
    def swap(m: re.Match) -> str:
        label = ICON_TEXT.get(m.group(1))
        return f" {label} " if label else ""

    return ICON.sub(swap, text)


STYLESHEET = """
@page {
  size: letter;
  margin: 0.9in 0.85in 0.85in 0.85in;
  @top-right { content: "LLMs & You — Fall 2026"; font-size: 8.5pt; color: #666; }
  @bottom-right { content: counter(page) " of " counter(pages);
                  font-size: 8.5pt; color: #666; }
}
@page :first { @top-right { content: ""; } }

body { font-family: "Source Serif 4", "DejaVu Serif", Georgia, serif;
       font-size: 10.5pt; line-height: 1.45; color: #111; }

h1 { font-size: 21pt; margin: 0 0 0.15em 0; line-height: 1.2; }
h2 { font-size: 13.5pt; margin: 1.5em 0 0.4em 0; padding-bottom: 0.15em;
     border-bottom: 1px solid #bbb; break-after: avoid; }
h3 { font-size: 11.5pt; margin: 1.1em 0 0.3em 0; break-after: avoid; }
h4 { font-size: 10.5pt; margin: 0.9em 0 0.25em 0; break-after: avoid; }
p, li { orphans: 2; widows: 2; }
a { color: #111; text-decoration: none; }
/* A printed page cannot be clicked, so a bare link has to say where it goes. */
a[href^="http"]::after { content: " (" attr(href) ")"; font-size: 8pt; color: #666;
                         word-break: break-all; }

table { border-collapse: collapse; width: 100%; margin: 0.6em 0; font-size: 9.5pt; }
th, td { border: 1px solid #ccc; padding: 3.5pt 5pt; text-align: left;
         vertical-align: top; }
th { background: #f0f0f0; font-weight: bold; }
tr { break-inside: avoid; }
thead { display: table-header-group; }

blockquote { margin: 0.6em 0 0.6em 1.2em; padding-left: 0.8em;
             border-left: 2px solid #ccc; color: #333; }
code { font-family: "DejaVu Sans Mono", monospace; font-size: 9pt; }

.admonition { border: 1px solid #bbb; border-left: 3px solid #666;
              padding: 6pt 9pt; margin: 0.7em 0; background: #fafafa;
              break-inside: avoid; }
.admonition-title { font-weight: bold; margin: 0 0 0.25em 0; font-size: 10pt; }

.cover-sub { font-size: 12pt; color: #333; margin: 0 0 1.2em 0; }
.section-break { break-before: page; }
.calendar-note { font-size: 9.5pt; color: #444; margin: 0 0 0.8em 0; }
"""


def build_env():
    """The macro environment mkdocs-macros would build, without mkdocs."""

    class Env:
        def __init__(self):
            self.variables: dict = {}
            self.filters: dict = {}

        def macro(self, fn):
            self.variables[fn.__name__] = fn
            return fn

    env = Env()
    macros.define_env(env)
    # mkdocs.yml carries !!python/name: tags that plain yaml refuses to load,
    # and nothing here needs them.
    raw = (ROOT / "mkdocs.yml").read_text().replace("!!python/name:", "#")
    env.variables["config"] = yaml.safe_load(raw)
    return env


def render_markdown(text: str, env) -> str:
    body = jinja2.Template(text).render(**env.variables)
    body = deiconify(body)
    return markdown.markdown(body, extensions=EXTENSIONS)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "-o", "--output", type=Path, default=ROOT / "LLMs-and-You-Syllabus-Fall-2026.pdf"
    )
    args = ap.parse_args()

    try:
        from weasyprint import CSS, HTML
    except ImportError:
        raise SystemExit(
            "weasyprint is not installed. Run:\n  .venv/bin/pip install -e '.[pdf]'"
        ) from None

    env = build_env()
    sem = env.variables["semester"]

    syllabus = render_markdown((ROOT / "docs" / "syllabus.md").read_text(), env)
    # On the web the page is headed "Syllabus" and names the course underneath.
    # On paper the course name is the title, so the H1 takes it and the line
    # below keeps only the institution and term.
    syllabus = syllabus.replace(
        "<h1>Syllabus</h1>", "<h1>LLMs &amp; You: Attention is All You Need</h1>", 1
    )
    syllabus = re.sub(
        r"<p><strong>LLMs &amp; You: Attention is All You Need</strong>\s*",
        '<p class="cover-sub">',
        syllabus,
        count=1,
    )
    # A borderless two-column table on the site has an empty header row. Printed
    # with visible rules it becomes a stripe of empty boxes.
    syllabus = re.sub(r"<thead>\s*<tr>(?:\s*<th[^>]*>\s*</th>)+\s*</tr>\s*</thead>", "", syllabus)

    calendar = deiconify(env.variables["schedule_table"]())
    calendar_html = markdown.markdown(calendar, extensions=EXTENSIONS)

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>LLMs &amp; You — Syllabus, {sem.term}</title></head><body>
{syllabus}
<div class="section-break">
<h2>Course calendar</h2>
<p class="calendar-note">Every meeting of the term. Readings and activities for
each session are on the course website; this table is the spine.</p>
{calendar_html}
</div>
</body></html>"""

    HTML(string=html, base_url=str(ROOT)).write_pdf(
        args.output, stylesheets=[CSS(string=STYLESHEET)]
    )
    size = args.output.stat().st_size / 1024
    print(f"saved {args.output} ({size:.0f} KB)")


if __name__ == "__main__":
    main()
