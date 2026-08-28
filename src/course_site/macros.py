"""Macros exposed to Markdown pages via mkdocs-macros.

Pages call these instead of hardcoding course facts, so nothing on the site can
drift out of sync with ``data/``. Call ``{{ schedule_table() }}`` in a page and
you get the current schedule, whatever the YAML says today.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# mkdocs-macros imports this file directly rather than as an installed package,
# so make `src/` importable before the sibling modules are pulled in.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from course_site.calendar import cancelled, conference_weeks
from course_site.loaders import (
    load_assignments,
    load_concepts,
    load_resources,
    load_schedule,
    load_semester,
    load_themes,
)
from course_site.models import Concept, DatedSession, GenAI, Kind, Resource
from course_site.render import concept_entry, reading_block, reading_entry


def define_env(env) -> None:
    """mkdocs-macros entry point."""

    sem = load_semester()
    schedule = load_schedule()
    themes = load_themes()

    env.variables["semester"] = sem
    env.variables["schedule"] = schedule
    env.variables["themes"] = themes
    env.variables["resources"] = load_resources()
    env.variables["assignments"] = load_assignments()
    env.variables["concepts"] = load_concepts()
    env.variables["concept_count"] = len(load_concepts())
    env.variables["session_count"] = len(schedule)
    env.variables["conference_count"] = sum(1 for d in schedule if d.is_conference)
    env.variables["first_meeting"] = schedule[0]
    env.variables["last_meeting"] = schedule[-1]

    @env.macro
    def schedule_table() -> str:
        """The bare clickable spine: week, date, topic. Nothing else.

        Readings deliberately do not appear here -- the whole point of this page
        is that it fits on one screen and every row is a link.
        """
        lost = {d: (reason, wk) for d, reason, wk in cancelled(sem)}
        rows = ["| Week | Date | Topic |", "|:---|:---|:---|"]

        shown: set[int] = set()
        pending = sorted(lost.items())

        for d in schedule:
            # Emit any cancelled meeting that falls before this session.
            while pending and pending[0][0] < d.date:
                when, (reason, wk) = pending.pop(0)
                label = _week_cell(wk, shown)
                rows.append(f"| {label} | {when:%a} {when:%b} {when.day} | *No class — {reason}* |")
            rows.append(_schedule_row(d, shown))

        for when, (reason, wk) in pending:
            label = _week_cell(wk, shown)
            rows.append(f"| {label} | {when:%a} {when:%b} {when.day} | *No class — {reason}* |")

        return "\n".join(rows)

    @env.macro
    def reading_list(session: DatedSession, optional: bool = False) -> str:
        """Full reading entries for a session, for use on hand-written pages."""
        ids = session.session.optional if optional else session.session.readings
        return reading_block(load_resources(), ids) if ids else ""

    @env.macro
    def resources_by_theme() -> str:
        """The full library, grouped by theme, for the Readings page."""
        by_theme: dict[str, list[Resource]] = {tid: [] for tid in themes}
        for r in load_resources().values():
            for tid in r.themes:
                by_theme[tid].append(r)

        out: list[str] = []
        for tid, theme in themes.items():
            items = sorted(by_theme[tid], key=lambda r: (r.kind.value, r.title))
            if not items:
                continue
            out.append(f"## Theme {theme.number} — {theme.name}\n")
            out.append(f"{theme.blurb}\n")
            out.extend(reading_entry(r) for r in items)
            out.append("")
        return "\n".join(out)

    @env.macro
    def study_guide() -> str:
        """Every concept, grouped by theme and ordered by when it was taught.

        Theme order matches the Readings page so the two can be read side by
        side; inside a theme, concepts run in the order the course met them,
        which is the order a student revising will want them in.
        """
        by_slug = {d.slug: d for d in schedule}
        assignments = {a.id: a for a in load_assignments()}
        resources = load_resources()
        concepts = load_concepts()

        grouped: dict[str, list[Concept]] = {tid: [] for tid in themes}
        for c in concepts.values():
            grouped[c.theme].append(c)

        out: list[str] = []
        for tid, theme in themes.items():
            items = sorted(grouped[tid], key=lambda c: (by_slug[c.slug].date, c.name))
            if not items:
                continue
            out.append(f"## Theme {theme.number} — {theme.name}\n")
            out.append(f"{theme.blurb}\n")
            for c in items:
                out.append(concept_entry(c, by_slug[c.slug], assignments, resources, concepts))
            out.append("")
        return "\n".join(out)

    @env.macro
    def concept_checklist() -> str:
        """The whole study guide as one table, for checking yourself against.

        Deliberately the first thing on the page: a student revising wants to
        know how many things there are before they want to know what any one of
        them means.
        """
        by_slug = {d.slug: d for d in schedule}
        assignments = {a.id: a for a in load_assignments()}
        rows = ["| Concept | Introduced | Assessed in |", "|:---|:---|:---|"]
        for c in sorted(load_concepts().values(), key=lambda c: (by_slug[c.slug].date, c.name)):
            d = by_slug[c.slug]
            graded = ", ".join(assignments[aid].title for aid in c.assessed_in)
            rows.append(
                f"| [{c.name}](#{c.id}) | [Week {c.week} ({d.date_label})]"
                f"(sessions/{c.slug}.md) | {graded} |"
            )
        return "\n".join(rows)

    @env.macro
    def burchell_arc() -> str:
        """The Real Python episodes with the same guest, in the order they aired.

        Derived, not typed: any podcast in the library by this guest joins the
        table, ordered by episode number, with its assignment read off the
        schedule. Adding a seventh episode to ``resources.yml`` is the whole job.
        """
        # Burchell is also in the library as an author of written pieces; only
        # the numbered podcast episodes are part of the arc.
        numbered = [
            (int(m.group(1)), r)
            for r in load_resources().values()
            if "Jodie Burchell" in r.authors
            and r.kind is Kind.PODCAST
            and (m := re.search(r"#(\d+)", r.title))
        ]
        where: dict[str, str] = {}
        for d in schedule:
            for rid in d.session.readings:
                where[rid] = f"Week {d.session.week}"
            for rid in d.session.optional:
                where.setdefault(rid, "Optional")

        rows = ["| # | Episode | Aired | Assigned |", "|:---|:---|:---|:---|"]
        for i, (num, r) in enumerate(sorted(numbered), 1):
            title = r.title.split(": ", 1)[1] if ": " in r.title else r.title
            rows.append(
                f"| {i} | [#{num} — {title}]({r.url}) | {r.year} | "
                f"{where.get(r.id, 'Not assigned')} |"
            )
        return "\n".join(rows)

    @env.macro
    def conference_table() -> str:
        """Weeks where individual meetings replace the group class.

        Dates and sessions only. The data model has no field for *why* a week is
        a conference week, so there is nothing here that could disclose one.
        """
        rows = ["| Week | Meetings run | Sessions replaced |", "|:---|:---|:---|"]
        for window, weeks in conference_weeks(sem):
            hit = [d for d in schedule if window.covers(d.date)]
            which = ", ".join(f"{d.date:%a} {d.date:%b} {d.date.day}" for d in hit)
            wk = f"Week {weeks[0]}" if len(weeks) == 1 else f"Weeks {weeks[0]}–{weeks[-1]}"
            rows.append(f"| {wk} | {window.span_label} | {which} |")
        return "\n".join(rows)

    @env.macro
    def required_adrs_table(prefix: str = "") -> str:
        """The decision records the project is graded on, with derived dates.

        ``prefix`` is the path from the calling page back to the docs root --
        ``"../"`` from inside ``guides/``.
        """
        by_slug = {d.slug: d for d in schedule}
        rows = ["| | Due | Decision |", "|:---|:---|:---|"]
        for a in load_assignments():
            for adr in a.adrs:
                d = by_slug[adr.slug]
                rows.append(
                    f"| **{adr.id}** | [Week {adr.week} ({d.date_label})]"
                    f"({prefix}sessions/{adr.slug}.md) | {adr.decision} |"
                )
        return "\n".join(rows)

    @env.macro
    def milestone_table(prefix: str = "") -> str:
        """Everything with a due date, read off the sessions that announce it.

        Derived rather than written, so this table and the "Due today" banner on
        the session page are the same fact rendered twice.
        """
        rows = ["| Due | Deliverable |", "|:---|:---|"]
        for d in schedule:
            if d.session.due:
                rows.append(
                    f"| **Week {d.session.week}** ([{d.date_label}]"
                    f"(sessions/{d.slug}.md)) | {d.session.due.strip()} |"
                )
        return "\n".join(rows)

    @env.macro
    def grading_table() -> str:
        """Components, weights, and whether GenAI is permitted on each.

        The AI column is here rather than buried in prose because the policy
        promises students that every restriction is stated where they will see it.
        """
        rows = ["| Component | Weight | GenAI |", "|:---|---:|:---|"]
        for a in load_assignments():
            ai = (
                ":material-close-octagon:{ title='Not permitted' } **No**"
                if a.genai is GenAI.PROHIBITED
                else ":material-check:{ title='Permitted, must be cited' } Cite it"
            )
            rows.append(f"| [{a.title}](assignments.md#{a.id}) | {a.weight}% | {ai} |")
        total = sum(a.weight for a in load_assignments())
        rows.append(f"| **Total** | **{total}%** | |")
        return "\n".join(rows)

    @env.macro
    def genai_banner(assignment_id: str) -> str:
        """The red prohibition banner, or a short reminder that citation is required."""
        a = next(x for x in load_assignments() if x.id == assignment_id)
        if a.genai is GenAI.PROHIBITED:
            return f'!!! failure "No generative AI on this work"\n\n    {a.genai_note.strip()}\n'
        return (
            '!!! note "Generative AI is permitted here — cite it"\n\n'
            "    Use the college subscriptions ([Co-Pilot](https://m365.cloud.microsoft/),\n"
            "    [BoodleBox](https://boodlebox.ai/)) and acknowledge what you used and how.\n"
            "    Hallucinations or slop in submitted work fail the assignment regardless.\n"
        )


def _week_cell(week: int, shown: set[int]) -> str:
    """Show the week number once per week, so the table reads as grouped rows."""
    if week in shown:
        return ""
    shown.add(week)
    return f"**{week}**"


def _schedule_row(d: DatedSession, shown: set[int]) -> str:
    label = _week_cell(d.session.week, shown)
    topic = f"[{d.session.topic}](sessions/{d.slug}.md)"

    suffix = ""
    if d.is_conference:
        tip = "Individual meetings"
        suffix += f" &nbsp;:material-account-clock-outline:{{ title='{tip}' }}"
    if d.session.due:
        suffix += " &nbsp;:material-flag-checkered:{ title='Something is due' }"

    return f"| {label} | {d.date_label} | {topic}{suffix} |"
