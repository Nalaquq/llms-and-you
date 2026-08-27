"""Tests over the course data itself.

These are not tests of the rendering code. They are tests that the *course* is
coherent -- that no session assigns a reading that does not exist, that the
grading weights add up, that nobody scheduled class on Thanksgiving. Broken
course logistics fail here rather than reaching a student.
"""

from __future__ import annotations

import datetime as dt
import re

import pytest

from course_site.calendar import held_dates, meeting_dates, week_of
from course_site.guides import GUIDES_DIR, load_guides, split_ref
from course_site.loaders import (
    load_assignments,
    load_resources,
    load_schedule,
    load_semester,
    load_themes,
)
from course_site.models import Access, Day, GenAI, Kind, Modality, SessionKind

SEM = load_semester()
SCHEDULE = load_schedule()
RESOURCES = load_resources()
THEMES = load_themes()
GUIDES = load_guides()


# --- Calendar ------------------------------------------------------------


def test_term_runs_fifteen_weeks():
    """The last *meeting* is in week 15.

    Not the last day of term: classes end Monday Dec 7, which is a stray Monday
    in a 16th partial week that this T/Th course never sees.
    """
    assert week_of(SEM, SCHEDULE[0].date) == 1
    assert week_of(SEM, SCHEDULE[-1].date) == 15
    assert {d.session.week for d in SCHEDULE} == set(range(1, 16))


def test_twenty_eight_meetings():
    """30 T/Th slots minus Fall Break and Thanksgiving."""
    assert len(meeting_dates(SEM)) == 30
    assert len(held_dates(SEM)) == 28
    assert len(SCHEDULE) == 28


def test_every_meeting_has_a_session():
    """No held meeting date is left without a session defined for it."""
    assert {d.date for d in SCHEDULE} == set(held_dates(SEM))


def test_no_session_on_an_excluded_date():
    for d in SCHEDULE:
        assert d.date not in SEM.excluded_dates, f"{d.slug} lands on a holiday"


def test_all_sessions_are_tuesday_or_thursday():
    for d in SCHEDULE:
        assert d.date.weekday() in (1, 3), f"{d.slug} is a {d.date:%A}"


def test_session_day_matches_its_date():
    for d in SCHEDULE:
        expected = Day.TUE if d.date.weekday() == 1 else Day.THU
        assert d.session.day is expected, f"{d.slug} says {d.session.day} but is {d.date:%A}"


def test_schedule_is_chronological():
    dates = [d.date for d in SCHEDULE]
    assert dates == sorted(dates)
    assert len(set(dates)) == len(dates), "two sessions share a date"


def test_first_and_last_meetings():
    assert SCHEDULE[0].date == dt.date(2026, 8, 25)
    assert SCHEDULE[-1].date == dt.date(2026, 12, 3)


def test_broken_weeks_are_the_expected_ones():
    """Week 8 loses its Tuesday, Week 14 its Thursday. Nothing else is short."""
    per_week: dict[int, int] = {}
    for d in SCHEDULE:
        per_week[d.session.week] = per_week.get(d.session.week, 0) + 1
    short = {w for w, n in per_week.items() if n == 1}
    assert short == {8, 14}
    assert all(n == 2 for w, n in per_week.items() if w not in short)


# --- Individual meetings and modality ------------------------------------


def test_five_sessions_are_conference_meetings():
    conf = [d for d in SCHEDULE if d.is_conference]
    assert len(conf) == 5
    assert {d.date for d in conf} == {
        dt.date(2026, 9, 15),
        dt.date(2026, 9, 22),
        dt.date(2026, 9, 24),
        dt.date(2026, 10, 27),
        dt.date(2026, 10, 29),
    }


def test_conference_sessions_carry_their_window():
    for d in SCHEDULE:
        if d.is_conference:
            assert d.conference is not None, f"{d.slug} is a conference session with no window"
        else:
            assert d.modality is Modality.GROUP


def test_conference_windows_record_no_reason():
    """The schema must not grow a field that could disclose why a week is off.

    The instructor's reasons are private and this repository is public. If
    someone adds a `reason` or `location` field to ConferenceWeek, this fails.
    """
    from course_site.models import ConferenceWeek

    fields = set(ConferenceWeek.model_fields)
    assert fields == {"start", "end", "label"}, f"unexpected fields: {fields}"


def test_weeks_five_and_ten_are_fully_conference_weeks():
    for week in (5, 10):
        sessions = [d for d in SCHEDULE if d.session.week == week]
        assert all(d.is_conference for d in sessions), f"week {week} is not all conferences"


def test_discussion_heavy_sessions_meet_as_a_group():
    """Sessions built around live argument must not land in a conference week.

    ADR-003 and ADR-004 both depend on this; if a conference window moves, this
    test is the thing that notices the pedagogy broke.
    """
    for slug in ("w06-tue", "w13-tue", "w14-tue"):
        d = next(x for x in SCHEDULE if x.slug == slug)
        assert not d.is_conference, f"{slug} ({d.session.topic}) needs a room"


# --- Referential integrity -----------------------------------------------


def test_every_referenced_resource_exists():
    for d in SCHEDULE:
        for rid in [*d.session.readings, *d.session.optional]:
            assert rid in RESOURCES, f"{d.slug} references missing resource {rid!r}"


def test_every_referenced_theme_exists():
    for d in SCHEDULE:
        assert d.session.theme in THEMES


def test_no_resource_is_listed_twice_in_one_session():
    for d in SCHEDULE:
        ids = [*d.session.readings, *d.session.optional]
        assert len(ids) == len(set(ids)), f"{d.slug} repeats a resource"


# --- Guides ---------------------------------------------------------------


def test_every_session_guide_reference_resolves():
    """A session may only point at a guide page that exists, at a heading that exists."""
    for d in SCHEDULE:
        for ref in d.session.guides:
            gid, anchor = split_ref(ref)
            assert gid in GUIDES, f"{d.slug} points at missing guide {gid!r}"
            if anchor:
                assert anchor in GUIDES[gid].sections, (
                    f"{d.slug} points at {ref!r}, but that heading is gone"
                )


def test_every_guide_is_reachable_from_a_session():
    """A guide nobody is sent to is a guide nobody reads.

    The Guides index lists them all, but students arrive at this site through
    the schedule -- they open the session they are stuck on. If we wrote a
    guide, some session has to name it.
    """
    named = {split_ref(ref)[0] for d in SCHEDULE for ref in d.session.guides}
    unreachable = sorted(set(GUIDES) - named)
    assert not unreachable, (
        f"guides no session points at: {unreachable}. "
        "Add the guide to the session where a student needs it."
    )


def test_setup_sessions_point_at_the_setup_guide():
    """Both install labs, specifically. These are the sessions people get stuck in."""
    for slug in ("w01-thu", "w02-thu"):
        session = next(d for d in SCHEDULE if d.slug == slug).session
        assert any(ref.startswith("setup") for ref in session.guides), (
            f"{slug} installs tools without naming the setup guide"
        )


def test_individual_meeting_sessions_explain_themselves():
    """A student whose class is replaced by a meeting needs the logistics page."""
    for d in SCHEDULE:
        if d.is_conference:
            assert "conference-weeks" in d.session.guides, (
                f"{d.slug} is an individual meeting and does not link the guide"
            )


def test_guide_anchors_match_what_markdown_will_generate():
    """Our slug logic mirrors the toc extension's. If that drifts, links rot silently."""
    from markdown.extensions.toc import slugify

    from course_site.guides import _plain, _slug

    for guide in GUIDES.values():
        for anchor, label in guide.sections.items():
            # Explicit `{ #anchor }` headings are exempt -- they set their own.
            if slugify(_plain(label), "-") != anchor:
                text = (GUIDES_DIR / f"{guide.id}.md").read_text(encoding="utf-8")
                assert f"{{ #{anchor} }}" in text, (
                    f"{guide.id}.md#{anchor} is neither an explicit anchor nor the "
                    f"slug markdown would generate for {label!r}"
                )
            assert _slug(label) == slugify(_plain(label), "-"), (
                f"_slug disagrees with markdown's slugify on {label!r}"
            )


def test_guide_links_written_into_prose_still_resolve():
    """Session prose links to guides by relative path. Check those too.

    The `guides` field is validated on load, but a link typed into an activity
    is just text. This is the same check applied to the text, so that renaming
    a heading in a guide fails the build rather than quietly producing a link
    that lands at the top of the page.
    """
    link = re.compile(r"\.\./guides/([a-z0-9-]+)\.md(?:#([\w-]+))?")
    for d in SCHEDULE:
        prose = " ".join(x for x in (d.session.activity, d.session.summary, d.session.due) if x)
        for gid, anchor in link.findall(prose):
            assert gid in GUIDES, f"{d.slug} links ../guides/{gid}.md, which does not exist"
            if anchor:
                assert anchor in GUIDES[gid].sections, (
                    f"{d.slug} links {gid}.md#{anchor}, but that heading is gone"
                )


def test_resource_themes_are_real():
    for r in RESOURCES.values():
        for t in r.themes:
            assert t in THEMES, f"{r.id} claims unknown theme {t!r}"


def test_themes_are_numbered_consecutively_from_one():
    assert sorted(t.number for t in THEMES.values()) == list(range(1, len(THEMES) + 1))


# --- Course design invariants --------------------------------------------


def test_every_seminar_assigns_reading():
    """A Tuesday with nothing to read is almost always an unfinished session."""
    for d in SCHEDULE:
        if d.session.kind is SessionKind.SEMINAR and d.session.week > 1:
            assert d.session.readings, f"{d.slug} is a seminar with no readings"


def test_labs_assign_no_new_reading():
    """The Tuesday/Thursday split is the course's workload promise. Enforce it."""
    for d in SCHEDULE:
        if d.session.kind is SessionKind.LAB:
            assert not d.session.readings, f"lab {d.slug} assigns reading"


def test_every_session_has_an_activity_or_readings():
    for d in SCHEDULE:
        assert d.session.activity or d.session.readings, f"{d.slug} is empty"


READ_CAP = 120
TOTAL_CAP = 200

# Sessions the instructor has deliberately loaded past the total cap, with the
# ceiling that session may not itself exceed. An entry here is a decision, not a
# waiver: the number is exact, so a week that grows further fails again and has
# to be decided again. The close-reading cap has no exceptions and never has --
# an hour at a desk is the expensive hour, and every entry here overruns on
# listening. Anything added must also be visible to students on the session
# page, which test_overloaded_sessions_warn_students checks.
HEAVY_SESSIONS: dict[str, int] = {
    # Foundations week. Two Burchell episodes and three explainers, because
    # every week after this one assumes embeddings are understood. 136 of the
    # 241 minutes are listening. See ADR-010.
    "w02-tue": 241,
}


def _load(d) -> tuple[int, int]:
    """Minutes of close reading, and minutes of everything, for one session."""
    listening = {Kind.PODCAST, Kind.VIDEO}
    items = [RESOURCES[r] for r in d.session.readings]
    read = sum(r.est_minutes or 0 for r in items if r.kind not in listening)
    heard = sum(r.est_minutes or 0 for r in items if r.kind in listening)
    return read, read + heard


def test_weekly_reading_load_stays_reasonable():
    """Close reading and listening are not the same cost, so they cap separately.

    An hour of paper is an hour at a desk. An hour of podcast is a walk across
    campus. The course promises one substantial reading per week; these are the
    numbers that keep that promise honest.
    """
    for d in SCHEDULE:
        read, total = _load(d)
        assert read <= READ_CAP, f"{d.slug} assigns {read} minutes of close reading"
        ceiling = HEAVY_SESSIONS.get(d.slug, TOTAL_CAP)
        assert total <= ceiling, (
            f"{d.slug} assigns {total} minutes total, over its {ceiling}-minute ceiling. "
            "Move something, or record the decision in HEAVY_SESSIONS with an ADR."
        )


def test_heavy_sessions_are_actually_heavy():
    """Delete the exception when the week that needed it slims back down."""
    for slug, ceiling in HEAVY_SESSIONS.items():
        d = next(x for x in SCHEDULE if x.slug == slug)
        _, total = _load(d)
        assert total > TOTAL_CAP, (
            f"{slug} is at {total} minutes and no longer needs an exception -- "
            "remove it from HEAVY_SESSIONS so the cap applies again"
        )
        assert total == ceiling, (
            f"{slug} is at {total} minutes but HEAVY_SESSIONS says {ceiling}. "
            "The ceiling is exact on purpose: update it as a decision, not a patch."
        )


def test_overloaded_sessions_warn_students():
    """A week over the cap has to say so where students will see it.

    The workload promise is made to students, so an exception to it is owed to
    students too -- not recorded only in a test file they never open.
    """
    for slug in HEAVY_SESSIONS:
        session = next(x for x in SCHEDULE if x.slug == slug).session
        prose = " ".join(x for x in (session.summary, session.activity) if x).lower()
        assert "heaviest" in prose or "heavy" in prose, (
            f"{slug} is deliberately over the reading cap and does not say so on the page"
        )


def test_all_themes_are_taught():
    """Every theme reaches students, whether or not it owns a session.

    Three themes are cross-cutting by design and carry no session of their own:
    `ecosystem` (tools, used in every lab), `methodology` (ADRs, practised all
    term), and `openweight` — whose readings sit inside the Week 13 cost lab
    (self-host vs API) and the Week 14 release-policy discussion, because that
    is where the open-weight question actually bites.
    """
    taught = {d.session.theme for d in SCHEDULE}
    cross_cutting = {"ecosystem", "openweight"}
    assert taught | cross_cutting == set(THEMES)

    # Cross-cutting themes must still be assigned somewhere, or they are simply
    # missing rather than woven in.
    for theme in cross_cutting:
        appears = any(
            theme in RESOURCES[rid].themes
            for d in SCHEDULE
            for rid in [*d.session.readings, *d.session.optional]
        )
        assert appears, f"theme {theme!r} owns no session and is never assigned"


def test_agents_theme_lands_in_weeks_eleven_and_twelve():
    weeks = {d.session.week for d in SCHEDULE if d.session.theme == "agents"}
    assert weeks == {11, 12}


# --- Assignments ---------------------------------------------------------


def test_grading_weights_total_one_hundred():
    assert sum(a.weight for a in load_assignments()) == 100


def test_assignment_ids_are_unique():
    ids = [a.id for a in load_assignments()]
    assert len(ids) == len(set(ids))


def test_due_dates_fall_on_real_sessions():
    """Anything marked due must be attached to a meeting that happens."""
    due = [d for d in SCHEDULE if d.session.due]
    assert len(due) >= 4
    for d in due:
        assert d.date in set(held_dates(SEM))


# --- AI policy -----------------------------------------------------------
#
# The policy promises students two things: that AI is permitted unless a page
# says otherwise, and that every restriction is stated where they will see it.
# These tests are what make those promises structural rather than aspirational.


def test_every_prohibition_states_a_reason():
    """A restriction with no explanation breaks the promise made in the syllabus."""
    for a in load_assignments():
        if a.genai is GenAI.PROHIBITED:
            assert a.genai_note, f"assignment {a.id!r} prohibits GenAI with no reason"
    for d in SCHEDULE:
        if d.session.genai is GenAI.PROHIBITED:
            assert d.session.genai_note, f"session {d.slug!r} prohibits GenAI with no reason"


def test_genai_defaults_to_permitted():
    """Permissive by default. If this inverts, the syllabus text is wrong."""
    from course_site.models import Session

    probe = Session(week=1, day=Day.TUE, topic="probe", theme="foundations")
    assert probe.genai is GenAI.ALLOWED


def test_notes_only_accompany_prohibitions():
    """A genai_note on permitted work would render nothing and confuse the author."""
    for a in load_assignments():
        if a.genai is GenAI.ALLOWED:
            assert not a.genai_note, f"assignment {a.id!r} has an unused genai_note"


def test_in_class_written_work_prohibits_genai():
    """Anything written by hand in the room cannot permit AI without contradiction."""
    d = next(x for x in SCHEDULE if x.slug == "w15-tue")
    assert d.session.genai is GenAI.PROHIBITED


def test_college_platforms_are_in_the_library():
    """The syllabus points students at these; they must resolve on the site."""
    for rid in ("ms-copilot", "boodlebox"):
        assert rid in RESOURCES, f"{rid} missing from resources.yml"
        assert RESOURCES[rid].access.value == "open"


def test_ai_policy_is_discussed_in_week_one():
    """The policy says 'we will discuss this extensively during the first week'."""
    first = next(x for x in SCHEDULE if x.session.week == 1 and x.session.day is Day.TUE)
    assert first.session.activity and "policy" in first.session.activity.lower()


# --- Resource hygiene ----------------------------------------------------


@pytest.mark.parametrize("rid", sorted(load_resources()))
def test_resource_url_is_https(rid: str):
    assert str(RESOURCES[rid].url).startswith("https://")


def test_no_known_paywalled_hosts():
    """Belt and braces: these hosts gate content regardless of how it is marked."""
    blocked_hosts = ("dl.acm.org", "sciencedirect.com", "nytimes.com", "amazon.com")
    for r in RESOURCES.values():
        host_hit = next((h for h in blocked_hosts if h in str(r.url)), None)
        assert host_hit is None, f"{r.id} links to gated host {host_hit}"


def test_every_reading_is_free_and_open():
    """No student should be priced out of the reading list.

    The course promises that every assigned reading is free to access. This is
    the enforcement: adding a resource behind a paywall, a library gate, or a
    purchase requirement fails the build until an open alternative is found or
    the claim on the syllabus is changed.
    """
    gated = sorted(r.id for r in RESOURCES.values() if r.access is not Access.OPEN)
    assert not gated, f"non-open readings: {gated}"


def test_no_insecure_reading_urls():
    """We do not send students to http:// — including for good free books."""
    insecure = sorted(r.id for r in RESOURCES.values() if str(r.url).startswith("http://"))
    assert not insecure, f"http:// readings: {insecure}"


def test_every_resource_is_used_or_deliberately_reference_only():
    """Catch resources added to the library and then forgotten."""
    used = {rid for d in SCHEDULE for rid in [*d.session.readings, *d.session.optional]}
    reference_only = {
        "cmu-17630",  # peer syllabus, instructor reference
        "rpp-232-sentiment",  # optional Burchell episode, listed on Readings page
        "alphaxiv-skill",
        "dlai-prompt-engineering",
        "nyt-open-weight-ai",
        "leon-2025-gpt5-open-weight",
        "adr-templates",
        "claude-ai",
        "openai-playground",
        "huggingface",
        "hackaprompt",
        "adr-github",
        "ms-copilot",
        "boodlebox",
    }
    orphans = set(RESOURCES) - used - reference_only
    assert not orphans, f"unused resources: {sorted(orphans)}"
