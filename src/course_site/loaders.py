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
from .models import Assignment, DatedSession, Resource, Semester, Session, SessionKind, Theme

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


def resource(rid: str) -> Resource:
    return load_resources()[rid]


def session_by_slug(slug: str) -> DatedSession:
    return next(d for d in load_schedule() if d.slug == slug)
