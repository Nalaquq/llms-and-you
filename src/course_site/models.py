"""Typed schemas for all course data.

Every fact about the course lives in ``data/*.yml`` and is validated through these
models before it can reach a page. If a reading is missing a URL, or a session
points at a resource that does not exist, the build fails here rather than
silently shipping a broken syllabus to students.
"""

from __future__ import annotations

import re
from datetime import date
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator, model_validator


class Kind(StrEnum):
    """What sort of thing a resource is. Drives the icon shown next to it."""

    PAPER = "paper"
    BOOK = "book"
    PODCAST = "podcast"
    VIDEO = "video"
    GUIDE = "guide"
    ARTICLE = "article"
    TOOL = "tool"


class Access(StrEnum):
    """How a student actually gets to the thing.

    We never host copyrighted PDFs, so this is the honest answer to "can I read
    this right now?" and it renders as a badge on every session page.
    """

    OPEN = "open"
    PAYWALLED = "paywalled"
    LIBRARY = "library"
    PURCHASE = "purchase"


class Day(StrEnum):
    TUE = "tue"
    THU = "thu"


class SessionKind(StrEnum):
    """Tuesdays carry reading; Thursdays are hands-on and assign no new prep."""

    SEMINAR = "seminar"
    LAB = "lab"
    MILESTONE = "milestone"


class GenAI(StrEnum):
    """Whether generative AI may be used on a piece of work.

    The course policy is permissive by default: students may use GenAI unless an
    assignment says otherwise. That makes ``PROHIBITED`` the exceptional case
    that must be stated explicitly on the page -- which is why this is a field
    rather than a sentence someone remembers to write.
    """

    ALLOWED = "allowed"
    PROHIBITED = "prohibited"


class Modality(StrEnum):
    """How a session runs: as a group class, or as individual meetings.

    Never set by hand on a session. It is derived from the conference windows in
    ``semester.yml``, so declaring a window automatically reflags every session
    it covers.
    """

    GROUP = "group"
    CONFERENCE = "conference"


ICONS: dict[Kind, str] = {
    Kind.PAPER: ":material-file-document-outline:",
    Kind.BOOK: ":material-book-open-variant:",
    Kind.PODCAST: ":material-podcast:",
    Kind.VIDEO: ":material-play-circle-outline:",
    Kind.GUIDE: ":material-compass-outline:",
    Kind.ARTICLE: ":material-newspaper-variant-outline:",
    Kind.TOOL: ":material-wrench-outline:",
}

ACCESS_LABELS: dict[Access, str] = {
    Access.OPEN: "Free online",
    Access.PAYWALLED: "Paywalled — use library access",
    Access.LIBRARY: "Via Bortz Library",
    Access.PURCHASE: "Required text — purchase",
}


class Base(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Theme(Base):
    """One of the ten conceptual units the course is organised around."""

    id: str
    number: int
    name: str
    blurb: str


class Guide(Base):
    """One hand-written page in ``docs/guides/``, read back out of its own file.

    Sessions point at these by id so that a guide we wrote is a guide students
    are actually sent to. Nothing here is authored twice: the title is the
    file's H1, and ``sections`` maps every anchor in it to the heading it names.
    """

    id: str
    title: str
    sections: dict[str, str] = Field(default_factory=dict)

    @property
    def path(self) -> str:
        """Link target from a generated session page."""
        return f"../guides/{self.id}.md"


class Resource(Base):
    """A single assignable thing, defined exactly once and referenced by id.

    A reading used in three sessions is described here one time. Correcting a
    URL corrects it everywhere it appears.
    """

    id: str
    title: str
    kind: Kind
    url: HttpUrl
    themes: list[str] = Field(min_length=1)
    access: Access = Access.OPEN
    authors: list[str] = Field(default_factory=list)
    year: int | None = None
    est_minutes: int | None = None
    assign_note: str | None = None
    """What to actually read. Crucial for papers we assign only in part."""
    note: str | None = None
    """Instructor-facing context about why this resource is on the list."""

    @field_validator("id")
    @classmethod
    def _slug(cls, v: str) -> str:
        if not v.replace("-", "").replace(".", "").isalnum():
            raise ValueError(f"resource id must be a slug, got {v!r}")
        return v

    @property
    def icon(self) -> str:
        return ICONS[self.kind]

    @property
    def access_label(self) -> str:
        return ACCESS_LABELS[self.access]

    @property
    def byline(self) -> str:
        """'Vaswani et al. (2017)' — omitting whichever half is missing."""
        who = ", ".join(self.authors)
        if who and self.year:
            return f"{who} ({self.year})"
        return who or (str(self.year) if self.year else "")


class Concept(Base):
    """One idea students are responsible for knowing and applying.

    A concept is not a topic. A topic is what a session was about; a concept is
    something a student can be asked to define, apply, and get wrong -- which is
    why ``mastery`` and ``assessed_in`` are both required. The study guide
    promises that everything on it is assessable, and a required field is how
    that promise survives the person adding the twentieth entry in November.

    ``theme`` files the concept by what it is. ``week``/``day`` records where it
    was introduced, and the two are allowed to disagree: a design idea can
    arrive in a session about architecture.
    """

    id: str
    name: str
    theme: str
    week: int = Field(ge=1, le=15)
    day: Day
    definition: str
    """The short version, in the terms the course uses. Rendered first."""
    in_practice: str | None = None
    """How the idea lands on prompting specifically, rather than in general."""
    mastery: list[str] = Field(min_length=1)
    """What a student should be able to *do*. Each entry completes 'you should
    be able to', and each one is a thing that could be asked."""
    pitfall: str | None = None
    """The mistake people actually make. Renders as a warning on the page."""
    assessed_in: list[str] = Field(min_length=1)
    """Assignment ids, checked against ``assignments.yml``."""
    resources: list[str] = Field(default_factory=list)
    """Review material, by resource id. Never a URL."""
    builds_on: list[str] = Field(default_factory=list)
    """Concept ids this one cannot be understood without, in the order a student
    should meet them. This is a prerequisite edge, not a cross-reference: the
    loader refuses a cycle and refuses a prerequisite taught later than the
    concept that needs it. See ADR-018."""
    related: list[str] = Field(default_factory=list)
    """Other concept ids worth reading beside this one. Unordered, undirected,
    and explicitly not a prerequisite -- use ``builds_on`` for that."""

    @field_validator("id")
    @classmethod
    def _slug(cls, v: str) -> str:
        # The id is the page anchor a session links to, so it has to be one.
        if not re.fullmatch(r"[a-z0-9-]+", v):
            raise ValueError(f"concept id must be a lowercase slug, got {v!r}")
        return v

    @property
    def slug(self) -> str:
        """The session this concept was introduced in."""
        return f"w{self.week:02d}-{self.day.value}"

    @property
    def anchor(self) -> str:
        return f"study-guide.md#{self.id}"


class Session(Base):
    """One 75-minute meeting. Dates are never stored here — they are computed."""

    week: int = Field(ge=1, le=15)
    day: Day
    topic: str
    theme: str
    kind: SessionKind = SessionKind.SEMINAR
    readings: list[str] = Field(default_factory=list)
    optional: list[str] = Field(default_factory=list)
    questions: list[str] = Field(default_factory=list)
    activity: str | None = None
    due: str | None = None
    summary: str | None = None
    genai: GenAI = GenAI.ALLOWED
    genai_note: str | None = None
    guides: list[str] = Field(default_factory=list)
    """Guides to send students to, as ``slug`` or ``slug#anchor``.

    A guide exists so that a student stuck at 11pm the night before has
    somewhere to go. That only works if the session they are stuck on names it,
    so this is a field with a test behind it rather than a link someone
    remembers to paste in.
    """

    @field_validator("guides")
    @classmethod
    def _guide_refs_are_well_formed(cls, v: list[str]) -> list[str]:
        for ref in v:
            if not re.fullmatch(r"[a-z0-9-]+(#[\w-]+)?", ref):
                raise ValueError(f"guide reference {ref!r} must be 'slug' or 'slug#anchor'")
        if len(set(v)) != len(v):
            raise ValueError(f"a session lists the same guide twice: {v}")
        return v

    @model_validator(mode="after")
    def _prohibition_must_be_explained(self) -> Session:
        if self.genai is GenAI.PROHIBITED and not self.genai_note:
            raise ValueError(
                f"session {self.slug!r} prohibits GenAI without saying why. "
                "The policy requires the restriction to be stated on the page."
            )
        return self

    @property
    def slug(self) -> str:
        return f"w{self.week:02d}-{self.day.value}"

    @property
    def is_lab(self) -> bool:
        return self.kind is SessionKind.LAB


class DatedSession(Base):
    """A Session with its computed calendar date and meeting modality attached."""

    session: Session
    date: date
    modality: Modality = Modality.GROUP
    conference: ConferenceWeek | None = None
    """Set when this session is replaced by individual meetings."""

    @property
    def slug(self) -> str:
        return self.session.slug

    @property
    def is_conference(self) -> bool:
        return self.modality is Modality.CONFERENCE

    @property
    def date_label(self) -> str:
        # "Tue Sep 8" — no zero padding, which reads better in a dense table.
        return f"{self.date:%a} {self.date:%b} {self.date.day}"

    @property
    def long_date(self) -> str:
        return f"{self.date:%A, %B} {self.date.day}, {self.date:%Y}"


class Holiday(Base):
    """A cancelled meeting. Kept in the schedule so the gap is visible, not silent."""

    date: date
    reason: str


class ConferenceWeek(Base):
    """A window where the group class is replaced by individual meetings.

    Deliberately records only *what happens* -- a date range and a
    student-facing label -- and never why. This repository is public; the
    instructor's reasons for a given week are nobody's business but their own,
    and a field that does not exist cannot leak.
    """

    start: date
    end: date
    label: str = "Individual conferences"

    def covers(self, when: date) -> bool:
        return self.start <= when <= self.end

    @property
    def span_label(self) -> str:
        if self.start.month == self.end.month:
            return f"{self.start:%B} {self.start.day}-{self.end.day}"
        return f"{self.start:%B} {self.start.day} - {self.end:%B} {self.end.day}"


class Semester(Base):
    term: str
    first_day: date
    last_day: date
    meeting_days: list[Day]
    exclusions: list[Holiday] = Field(default_factory=list)
    conference_weeks: list[ConferenceWeek] = Field(default_factory=list)

    @property
    def excluded_dates(self) -> set[date]:
        return {h.date for h in self.exclusions}

    def reason_for(self, when: date) -> str | None:
        return next((h.reason for h in self.exclusions if h.date == when), None)

    def conference_on(self, when: date) -> ConferenceWeek | None:
        return next((c for c in self.conference_weeks if c.covers(when)), None)


class RequiredADR(Base):
    """One of the decision records the project is graded on.

    Written down here because it was previously written down in three places --
    two Markdown tables and a session's ``due`` string -- and one of the three
    was missing two of the four. The session pages, the guide, and the milestone
    table all derive from this list, and a test checks the session actually
    announces it.
    """

    id: str
    week: int = Field(ge=1, le=15)
    day: Day
    decision: str
    """What the record is about, in the words the guide's table shows."""

    @field_validator("id")
    @classmethod
    def _numbered(cls, v: str) -> str:
        if not re.fullmatch(r"ADR-\d{3}", v):
            raise ValueError(f"required ADR id must look like 'ADR-001', got {v!r}")
        return v

    @property
    def slug(self) -> str:
        return f"w{self.week:02d}-{self.day.value}"


class Assignment(Base):
    id: str
    title: str
    weight: int
    """Percentage of the final grade."""
    summary: str
    due: str | None = None
    adrs: list[RequiredADR] = Field(default_factory=list)
    """Decision records due at checkpoints, for assignments graded on a log."""
    genai: GenAI = GenAI.ALLOWED
    genai_note: str | None = None

    @model_validator(mode="after")
    def _prohibition_must_be_explained(self) -> Assignment:
        if self.genai is GenAI.PROHIBITED and not self.genai_note:
            raise ValueError(
                f"assignment {self.id!r} prohibits GenAI without saying why. "
                "The policy requires the restriction to be stated on the page."
            )
        return self
