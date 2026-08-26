"""Emit one page per class meeting, at build time, from ``data/schedule.yml``.

These pages are never written by hand and never committed -- ``docs/sessions/``
is gitignored. Editing the YAML is the only way to change what a session says,
which is what keeps the schedule table and the session pages from disagreeing.
"""

from __future__ import annotations

import sys
from pathlib import Path

import mkdocs_gen_files

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from course_site.guides import load_guides
from course_site.loaders import load_resources, load_schedule, load_themes
from course_site.models import DatedSession, GenAI, SessionKind
from course_site.render import guide_block, reading_block

KIND_LABEL = {
    SessionKind.SEMINAR: "Seminar",
    SessionKind.LAB: "Lab",
    SessionKind.MILESTONE: "Milestone",
}


def render(d: DatedSession, prev: DatedSession | None, nxt: DatedSession | None) -> str:
    s = d.session
    themes = load_themes()
    resources = load_resources()
    theme = themes[s.theme]

    out: list[str] = []
    out.append(f"# {s.topic}\n")

    # --- Header block: when, where, what kind of meeting -------------------
    where = "By individual appointment" if d.is_conference else "PRC 106"
    out.append(
        f"**{d.long_date}** · 2:00–3:30 PM · {where}  \n"
        f"Week {s.week} · {KIND_LABEL[s.kind]} · Theme {theme.number}: {theme.name}\n"
    )

    # An individual-meeting day is simply what that session is -- the topic says
    # so. This note is logistics only: no explanation is offered and none is
    # owed. See ConferenceWeek in models.py.
    if d.is_conference and d.conference:
        out.append(
            '!!! info "Individual meetings — sign up for a slot"\n\n'
            f"    Meetings run {d.conference.span_label}. The sign-up sheet goes\n"
            "    out the week before; if nothing on it works, email me.\n\n"
            "    The work below is yours to complete at your own pace.\n"
        )

    if s.summary:
        out.append(f"{s.summary.strip()}\n")

    # Above the reading, not below the activity: a student who is stuck is
    # stuck before they start, and this is the page they are already on.
    if s.guides:
        out.append(guide_block(load_guides(), s.guides))

    if s.due:
        out.append(f'!!! danger "Due today"\n\n    {s.due}\n')

    # The course policy is permissive by default, so a prohibition is the
    # exception and must be impossible to miss on the page it applies to.
    if s.genai is GenAI.PROHIBITED:
        out.append(
            '!!! failure "No generative AI on this work"\n\n'
            f"    {s.genai_note.strip()}\n\n"
            "    Using GenAI here means failing the assignment and a referral to\n"
            "    the Honor Court. See the [AI policy](../syllabus.md#using-ai).\n"
        )

    # --- Preparation -------------------------------------------------------
    if s.readings:
        heading = "Work through this week" if d.is_conference else "Read before class"
        out.append(f"## {heading}\n")
        out.append(reading_block(resources, s.readings))
        out.append("")
        total = sum(resources[rid].est_minutes or 0 for rid in s.readings)
        if total:
            out.append(f"<small>Estimated preparation: about {total} minutes.</small>\n")
    elif s.kind is SessionKind.LAB:
        out.append("## Read before class\n")
        out.append(
            '!!! success "Nothing new to read"\n\n'
            "    Labs assign no new preparation. Bring what you built last session.\n"
        )

    if s.questions:
        out.append("## Come prepared to answer\n")
        out.extend(f"{i}. {q.strip()}" for i, q in enumerate(s.questions, 1))
        out.append("")

    if s.activity:
        out.append("## In session\n")
        out.append(f"{s.activity.strip()}\n")

    if s.optional:
        out.append("## Going further\n")
        out.append("Optional. Useful for projects, not required for class.\n")
        out.append(reading_block(resources, s.optional))
        out.append("")

    # --- Footer navigation -------------------------------------------------
    out.append("---\n")
    links: list[str] = []
    if prev:
        links.append(f"[:material-arrow-left: {prev.session.topic}]({prev.slug}.md)")
    links.append("[All sessions](../schedule.md)")
    if nxt:
        links.append(f"[{nxt.session.topic} :material-arrow-right:]({nxt.slug}.md)")
    out.append(" &nbsp;·&nbsp; ".join(links))

    return "\n".join(out)


def main() -> None:
    schedule = load_schedule()
    for i, d in enumerate(schedule):
        prev = schedule[i - 1] if i > 0 else None
        nxt = schedule[i + 1] if i + 1 < len(schedule) else None
        path = f"sessions/{d.slug}.md"
        with mkdocs_gen_files.open(path, "w") as fh:
            fh.write(render(d, prev, nxt))


main()
