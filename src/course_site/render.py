"""Shared Markdown rendering helpers.

Both the macros (which render the Readings page) and the session-page generator
need to render a reading the same way. It lives here so the two cannot drift --
a reading looks identical wherever a student meets it.
"""

from __future__ import annotations

from .guides import split_ref
from .models import Access, Assignment, Concept, DatedSession, Guide, Resource


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


def concept_entry(
    c: Concept,
    introduced: DatedSession,
    assignments: dict[str, Assignment],
    resources: dict[str, Resource],
    concepts: dict[str, Concept],
) -> str:
    """One concept, as it appears on the study guide.

    Written to be read the night before rather than browsed: the definition
    first, then what you are expected to *do* with it, then the mistake people
    make, then where to go back to. The explicit anchor is the id, because a
    session page links here and rewording the heading must not move it.
    """
    where = f"[Week {c.week} — {introduced.date_label}](sessions/{c.slug}.md)"
    graded = " · ".join(
        f"[{assignments[aid].title}](assignments.md#{aid})" for aid in c.assessed_in
    )

    out = [
        f"### {c.name} {{ #{c.id} }}\n",
        f"<small>:material-school-outline: Introduced {where} &nbsp;·&nbsp; "
        f":material-flag-checkered: Assessed in {graded}</small>\n",
        f"{c.definition.strip()}\n",
    ]

    if c.in_practice:
        out.append(f"**In this course.** {c.in_practice.strip()}\n")

    out.append("**You should be able to**\n")
    out.extend(f"{i}. {m.strip()}" for i, m in enumerate(c.mastery, 1))
    out.append("")

    if c.pitfall:
        out.append(f'???+ warning "Where this goes wrong"\n\n    {c.pitfall.strip()}\n')

    if c.resources:
        out.append("**Review and go further**\n")
        out.append(reading_block(resources, c.resources))
        out.append("")

    if c.related:
        links = ", ".join(f"[{concepts[o].name}](#{o})" for o in c.related)
        out.append(f"<small>See also: {links}</small>\n")

    return "\n".join(out)


def concept_block(concepts: list[Concept], prefix: str = "") -> str:
    """The concepts a session introduced, as an admonition on that session page.

    ``prefix`` is the path back to the docs root -- ``"../"`` from a generated
    session page. A concept exists to be revised later, so the session it came
    from has to say which ones it was; otherwise the study guide is a page
    students find in December.
    """
    lines = [
        '!!! abstract "Concepts from this session"',
        "",
        f"    You are responsible for these. The [study guide]({prefix}study-guide.md) has",
        "    the definition, what you should be able to do with it, and where to review it.",
        "",
    ]
    for c in concepts:
        lines.append(f"    - :material-school-outline: **[{c.name}]({prefix}{c.anchor})**")
    return "\n".join(lines) + "\n"
