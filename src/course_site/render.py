"""Shared Markdown rendering helpers.

Both the macros (which render the Readings page) and the session-page generator
need to render a reading the same way. It lives here so the two cannot drift --
a reading looks identical wherever a student meets it.
"""

from __future__ import annotations

from .models import Access, Resource


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
