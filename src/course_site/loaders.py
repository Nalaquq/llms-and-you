"""Load and validate ``data/*.yml`` into typed models.

Loading is strict and eager: a typo in a resource id or a session pointing at a
reading that does not exist raises here, at build time, instead of rendering an
empty reading list on a page a student is relying on.
"""

from __future__ import annotations

import functools
from pathlib import Path
from typing import Any

import yaml
from pydantic import TypeAdapter

from .calendar import assign_dates
from .guides import load_guides, split_ref
from .models import (
    Assignment,
    Concept,
    DatedSession,
    Resource,
    Semester,
    Session,
    SessionKind,
    Theme,
)

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


class _StrictLoader(yaml.SafeLoader):
    """SafeLoader that refuses duplicate mapping keys.

    Plain YAML silently keeps the last of a repeated key. In course data that is
    a quiet content loss -- adding a second ``optional:`` to a session drops the
    first one's readings with no error, and nobody notices until a student does.
    """


def _no_duplicate_keys(loader: yaml.Loader, node: yaml.MappingNode) -> dict:
    seen: set = set()
    for key_node, _ in node.value:
        key = loader.construct_object(key_node, deep=True)
        if key in seen:
            mark = key_node.start_mark
            raise ValueError(
                f"duplicate key {key!r} at line {mark.line + 1} of {mark.name}. "
                "YAML would silently keep only the last one."
            )
        seen.add(key)
    return loader.construct_mapping(node, deep=True)


_StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _no_duplicate_keys)


def _read(name: str) -> Any:
    path = DATA_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"missing course data file: {path}")
    # Pass the handle rather than the text so YAML error marks name the file.
    with path.open(encoding="utf-8") as fh:
        return yaml.load(fh, Loader=_StrictLoader)


@functools.cache
def load_semester() -> Semester:
    return Semester.model_validate(_read("semester.yml"))


@functools.cache
def load_themes() -> dict[str, Theme]:
    themes = TypeAdapter(list[Theme]).validate_python(_read("themes.yml"))
    return {t.id: t for t in sorted(themes, key=lambda t: t.number)}


@functools.cache
def load_resources() -> dict[str, Resource]:
    items = TypeAdapter(list[Resource]).validate_python(_read("resources.yml"))
    seen: dict[str, Resource] = {}
    for r in items:
        if r.id in seen:
            raise ValueError(f"duplicate resource id: {r.id}")
        seen[r.id] = r

    themes = load_themes()
    for r in seen.values():
        for t in r.themes:
            if t not in themes:
                raise ValueError(f"resource {r.id!r} references unknown theme {t!r}")
    return seen


@functools.cache
def load_assignments() -> list[Assignment]:
    return TypeAdapter(list[Assignment]).validate_python(_read("assignments.yml"))


@functools.cache
def load_schedule() -> list[DatedSession]:
    """The fully resolved schedule: validated, cross-checked, and dated."""
    sessions = TypeAdapter(list[Session]).validate_python(_read("schedule.yml"))
    resources = load_resources()
    themes = load_themes()
    guides = load_guides()

    for s in sessions:
        if s.theme not in themes:
            raise ValueError(f"session {s.slug!r} references unknown theme {s.theme!r}")
        for rid in [*s.readings, *s.optional]:
            if rid not in resources:
                raise ValueError(f"session {s.slug!r} references unknown resource {rid!r}")
        for ref in s.guides:
            gid, anchor = split_ref(ref)
            guide = guides.get(gid)
            if guide is None:
                raise ValueError(
                    f"session {s.slug!r} points at guide {gid!r}, which is not a page in "
                    f"docs/guides/. Available: {sorted(guides)}"
                )
            if anchor and anchor not in guide.sections:
                raise ValueError(
                    f"session {s.slug!r} points at {ref!r}, but {gid}.md has no such "
                    f"heading. A renamed heading breaks the link silently otherwise."
                )
        if s.kind is SessionKind.LAB and s.readings:
            raise ValueError(
                f"lab session {s.slug!r} assigns readings. Labs carry no new prep by "
                "design -- move these to the preceding Tuesday, or use 'optional'."
            )

    dated = assign_dates(load_semester(), sessions)

    by_slug = {d.slug: d for d in dated}
    for a in load_assignments():
        for adr in a.adrs:
            d = by_slug.get(adr.slug)
            if d is None:
                raise ValueError(
                    f"{adr.id} is due at {adr.slug!r}, which is not a meeting in the schedule"
                )
            if adr.id not in (d.session.due or ""):
                raise ValueError(
                    f"{adr.id} is due on {adr.slug}, but that session's 'due' does not "
                    f"mention it: {d.session.due!r}. A deliverable students cannot see "
                    "on the session page is one they will miss."
                )

    return dated


@functools.cache
def load_concepts() -> dict[str, Concept]:
    """The study guide, cross-checked against everything it claims to reference.

    A concept names a session, a theme, some readings, and the assignments it is
    assessed on. Every one of those is a chance for the study guide to promise a
    student something the course does not deliver, so all four are resolved here
    rather than rendered hopefully.
    """
    items = TypeAdapter(list[Concept]).validate_python(_read("concepts.yml"))

    found: dict[str, Concept] = {}
    for c in items:
        if c.id in found:
            raise ValueError(f"duplicate concept id: {c.id}")
        found[c.id] = c

    themes = load_themes()
    resources = load_resources()
    assignments = {a.id for a in load_assignments()}
    sessions = {d.slug for d in load_schedule()}

    for c in found.values():
        if c.theme not in themes:
            raise ValueError(f"concept {c.id!r} references unknown theme {c.theme!r}")
        if c.slug not in sessions:
            raise ValueError(
                f"concept {c.id!r} says it was introduced at {c.slug!r}, which is not a "
                "meeting in the schedule"
            )
        for rid in c.resources:
            if rid not in resources:
                raise ValueError(f"concept {c.id!r} references unknown resource {rid!r}")
        for aid in c.assessed_in:
            if aid not in assignments:
                raise ValueError(
                    f"concept {c.id!r} claims it is assessed in {aid!r}, which is not a "
                    f"graded component. Known: {sorted(assignments)}"
                )

    # Second pass: the concept-to-concept edges, which can only be checked once
    # every concept is known.
    order = {d.slug: i for i, d in enumerate(load_schedule())}
    for c in found.values():
        for other in c.related:
            if other not in found:
                raise ValueError(f"concept {c.id!r} links unknown concept {other!r}")
            if other == c.id:
                raise ValueError(f"concept {c.id!r} lists itself as related")
        for other in c.builds_on:
            if other not in found:
                raise ValueError(f"concept {c.id!r} builds on unknown concept {other!r}")
            if other == c.id:
                raise ValueError(f"concept {c.id!r} lists itself as a prerequisite")
            # A prerequisite introduced after the thing needing it is not a
            # prerequisite, it is a forward reference. Students read this page in
            # week order, so the ladder has to be climbable in that order.
            if order[found[other].slug] > order[c.slug]:
                raise ValueError(
                    f"concept {c.id!r} ({c.slug}) builds on {other!r}, which is not "
                    f"introduced until {found[other].slug}"
                )
        if set(c.builds_on) & set(c.related):
            both = sorted(set(c.builds_on) & set(c.related))
            raise ValueError(
                f"concept {c.id!r} lists {both} as both a prerequisite and a "
                "cross-reference. Pick one: builds_on is the stronger claim."
            )

    _refuse_prerequisite_cycles(found)
    return found


def _refuse_prerequisite_cycles(concepts: dict[str, Concept]) -> None:
    """A cycle in ``builds_on`` is a page that cannot be read in any order.

    Same-session concepts make this reachable by accident -- two ideas taught on
    one Tuesday can each look like the other's foundation. The build refuses,
    because a student following the prerequisites would walk in a circle.
    """
    unvisited, on_stack, done = 0, 1, 2
    state = dict.fromkeys(concepts, unvisited)

    def walk(cid: str, path: list[str]) -> None:
        state[cid] = on_stack
        for parent in concepts[cid].builds_on:
            if state[parent] == on_stack:
                loop = " -> ".join([*path[path.index(parent) :], cid, parent])
                raise ValueError(f"prerequisite cycle among concepts: {loop}")
            if state[parent] == unvisited:
                walk(parent, [*path, cid])
        state[cid] = done

    for cid in concepts:
        if state[cid] == unvisited:
            walk(cid, [])


def resource(rid: str) -> Resource:
    return load_resources()[rid]


def session_by_slug(slug: str) -> DatedSession:
    return next(d for d in load_schedule() if d.slug == slug)
