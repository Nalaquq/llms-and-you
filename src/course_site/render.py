"""Shared Markdown rendering helpers.

Both the macros (which render the Readings page) and the session-page generator
need to render a reading the same way. It lives here so the two cannot drift --
a reading looks identical wherever a student meets it.
"""

from __future__ import annotations

from .guides import split_ref
from .models import Access, Guide, Resource


def reading_entry(r: Resource) -> str:
    """One reading as a Markdown list item.

    Icon, linked title, byline, then a quiet metadata line for time and access,
    then the assignment note hanging underneath. The note is the important part
    for papers assigned in sections rather than whole.
    """
    head = f"{r.icon} **[{r.title}]({r.url})**"
    if r.byline:
        head += f" — {r.byline}"

    bits: list[str] = []
    if r.est_minutes:
        bits.append(f"~{r.est_minutes} min")
    if r.access is not Access.OPEN:
        bits.append(r.access_label)
    meta = f" <small>({' · '.join(bits)})</small>" if bits else ""

    lines = [f"- {head}{meta}"]
    if r.assign_note:
        lines.append(f"    <br>:material-information-outline: {r.assign_note.strip()}")
    return "\n".join(lines)


def reading_block(resources: dict[str, Resource], ids: list[str]) -> str:
    """Several readings, in the order the session lists them."""
    return "\n".join(reading_entry(resources[rid]) for rid in ids)


def guide_block(guides: dict[str, Guide], refs: list[str]) -> str:
    """The guides for a session, as an admonition placed above the reading.

    A session page is where a student who is stuck actually is, so the pointer
    to the written-down version belongs there rather than only in the Guides
    index. When a reference carries an anchor, the section it lands on is named
    -- "the setup guide" is not much use at 11pm; "Week 1: your repository and
    your tools" is.
    """
    lines = ['!!! tip "Guides for this session"', ""]
    for ref in refs:
        gid, anchor = split_ref(ref)
        g = guides[gid]
        target = f"{g.path}#{anchor}" if anchor else g.path
        entry = f"    - :material-compass-outline: **[{g.title}]({target})**"
        if anchor:
            entry += f" — {g.sections[anchor]}"
        lines.append(entry)
    return "\n".join(lines) + "\n"
