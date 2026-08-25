"""Derive the semester's meeting dates from term bounds and holidays.

No date is ever typed by hand into course content. ``data/semester.yml`` holds the
first day, the last day, and the days we lose to breaks; everything downstream --
the schedule table, every session page, every due date -- is computed from those.

Move Fall Break by a day in the YAML and the entire site reflows correctly.
"""

from __future__ import annotations

from datetime import date, timedelta

from .models import ConferenceWeek, DatedSession, Day, Modality, Semester, Session

WEEKDAY: dict[Day, int] = {Day.TUE: 1, Day.THU: 3}


def meeting_dates(semester: Semester) -> list[date]:
    """Every date the class *could* meet, holidays included.

    Holidays stay in this list on purpose: the schedule shows cancelled meetings
    rather than quietly skipping them, so students can see why a week is short.
    """
    wanted = {WEEKDAY[d] for d in semester.meeting_days}
    out: list[date] = []
    cursor = semester.first_day
    while cursor <= semester.last_day:
        if cursor.weekday() in wanted:
            out.append(cursor)
        cursor += timedelta(days=1)
    return out


def held_dates(semester: Semester) -> list[date]:
    """Dates the class actually meets."""
    excluded = semester.excluded_dates
    return [d for d in meeting_dates(semester) if d not in excluded]


def week_of(semester: Semester, when: date) -> int:
    """Which numbered course week a date falls in.

    Weeks are anchored to the Monday of the term's first week, so a Tuesday and
    the Thursday after it always share a week number -- including across the two
    weeks where a break removes one of the pair.
    """
    anchor = semester.first_day - timedelta(days=semester.first_day.weekday())
    return ((when - anchor).days // 7) + 1


def assign_dates(semester: Semester, sessions: list[Session]) -> list[DatedSession]:
    """Attach a real date to each session by matching on (week, day).

    Raises if a session has no corresponding meeting -- which is exactly what we
    want when someone schedules class on Thanksgiving.
    """
    slots: dict[tuple[int, Day], date] = {}
    for when in held_dates(semester):
        day = next(d for d, wd in WEEKDAY.items() if wd == when.weekday())
        slots[(week_of(semester, when), day)] = when

    dated: list[DatedSession] = []
    for s in sessions:
        key = (s.week, s.day)
        if key not in slots:
            reason = _why_missing(semester, key)
            raise ValueError(
                f"Session '{s.topic}' is scheduled for week {s.week} {s.day.value}, "
                f"which is not a meeting date. {reason}"
            )
        when = slots[key]
        window = semester.conference_on(when)
        dated.append(
            DatedSession(
                session=s,
                date=when,
                modality=Modality.CONFERENCE if window else Modality.GROUP,
                conference=window,
            )
        )

    dated.sort(key=lambda d: d.date)
    return dated


def conference_sessions(semester: Semester, sessions: list[Session]) -> list[DatedSession]:
    """Every meeting that falls inside a conference window."""
    return [d for d in assign_dates(semester, sessions) if d.is_conference]


def conference_weeks(semester: Semester) -> list[tuple[ConferenceWeek, list[int]]]:
    """(window, affected course weeks) -- for the schedule's conference table."""
    out: list[tuple[ConferenceWeek, list[int]]] = []
    for window in sorted(semester.conference_weeks, key=lambda c: c.start):
        weeks = sorted({week_of(semester, d) for d in held_dates(semester) if window.covers(d)})
        out.append((window, weeks))
    return out


def _why_missing(semester: Semester, key: tuple[int, Day]) -> str:
    week, day = key
    for when in meeting_dates(semester):
        if week_of(semester, when) == week and when.weekday() == WEEKDAY[day]:
            reason = semester.reason_for(when)
            return f"That date ({when:%b %d}) is cancelled: {reason}."
    return "No such slot exists in the term."


def cancelled(semester: Semester) -> list[tuple[date, str, int]]:
    """(date, reason, week) for each lost meeting, for display on the schedule."""
    return [
        (h.date, h.reason, week_of(semester, h.date))
        for h in sorted(semester.exclusions, key=lambda h: h.date)
    ]
