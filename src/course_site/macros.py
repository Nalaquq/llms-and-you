"""Macros exposed to Markdown pages via mkdocs-macros.

Pages call these instead of hardcoding course facts, so nothing on the site can
drift out of sync with ``data/``. Call ``{{ schedule_table() }}`` in a page and
you get the current schedule, whatever the YAML says today.
"""

from __future__ import annotations

import sys
from pathlib import Path

# mkdocs-macros imports this file directly rather than as an installed package,
# so make `src/` importable before the sibling modules are pulled in.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from course_site.calendar import cancelled, conference_weeks
from course_site.loaders import (
    load_assignments,
    load_resources,
    load_schedule,
    load_semester,
    load_themes,
)
from course_site.models import DatedSession, GenAI, Resource
from course_site.render import reading_block, reading_entry


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
