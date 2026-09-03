"""Tests that the Thursday notebooks exist, open, and say what they are.

A notebook is the whole instruction for a lab now, so the failure modes worth
catching are the ones a student meets at 9pm on a Wednesday: a session pointing
at a file that is not there, a file Colab will refuse to open, or a draft
presented as though it were finished.

These check the notebooks as *course material*. Whether the code inside them
produces correct output is not something a test can tell you -- that is what
running them is for.
"""

from __future__ import annotations

import json

from course_site.loaders import load_schedule
from course_site.models import SessionKind
from course_site.notebooks import NOTEBOOKS_DIR, load_notebooks

SCHEDULE = load_schedule()
NOTEBOOKS = load_notebooks()
LABS = [d for d in SCHEDULE if d.session.kind is SessionKind.LAB]


def test_there_are_notebooks_at_all():
    assert NOTEBOOKS, f"no notebooks found in {NOTEBOOKS_DIR}"


def test_every_session_notebook_reference_resolves():
    """A session may only point at a notebook that exists."""
    for d in SCHEDULE:
        if d.session.notebook:
            assert d.session.notebook in NOTEBOOKS, (
                f"{d.slug} points at missing notebook {d.session.notebook!r}"
            )


def test_every_notebook_belongs_to_a_session():
    """A notebook nothing points at is a notebook nobody opens.

    Same rule as the guides: students arrive through the schedule, so an
    unreferenced notebook is reachable only by browsing the repository, which
    they do not do.
    """
    named = {d.session.notebook for d in SCHEDULE if d.session.notebook}
    orphans = sorted(set(NOTEBOOKS) - named)
    assert not orphans, f"notebooks no session points at: {orphans}"


def test_every_lab_has_a_notebook_or_says_why_not():
    """Thursdays are shown, not followed. A lab with nothing to prepare gives
    students nothing to bring.

    The model already refuses this, so reaching the assertion means the schema
    was loosened -- which is the change worth failing loudly on.
    """
    for d in LABS:
        s = d.session
        assert s.notebook or s.notebook_exempt, (
            f"lab {d.slug} has neither a notebook nor a stated reason for having none"
        )


def test_notebooks_are_named_for_their_session():
    """``w02-thu.ipynb`` belongs to ``w02-thu``. Anything else invites a mismatch."""
    for d in SCHEDULE:
        if d.session.notebook:
            assert d.session.notebook == d.slug, (
                f"{d.slug} uses notebook {d.session.notebook!r}; name it after the session"
            )


def test_no_two_sessions_share_a_notebook():
    used = [d.session.notebook for d in SCHEDULE if d.session.notebook]
    assert len(used) == len(set(used)), "two sessions claim the same notebook"


def test_every_notebook_is_valid_json_with_cells():
    """Colab will not open a malformed notebook, and says so unhelpfully."""
    for path in sorted(NOTEBOOKS_DIR.glob("*.ipynb")):
        raw = json.loads(path.read_text(encoding="utf-8"))
        assert raw.get("nbformat") == 4, f"{path.name} is not nbformat 4"
        assert raw.get("cells"), f"{path.name} has no cells"
        for i, cell in enumerate(raw["cells"]):
            assert cell.get("cell_type") in {"code", "markdown"}, (
                f"{path.name} cell {i} has an unexpected type"
            )
            if cell["cell_type"] == "code":
                # Colab tolerates a missing outputs key; nbformat validators do not.
                assert "outputs" in cell, f"{path.name} code cell {i} has no outputs key"


def test_no_notebook_ships_with_saved_output():
    """Committed output makes diffs unreadable and can leak whatever was on screen.

    It also lies to the student: a notebook that already shows results looks
    like it ran, so nobody notices it no longer does.
    """
    for path in sorted(NOTEBOOKS_DIR.glob("*.ipynb")):
        raw = json.loads(path.read_text(encoding="utf-8"))
        dirty = [
            i
            for i, c in enumerate(raw["cells"])
            if c.get("cell_type") == "code" and (c.get("outputs") or c.get("execution_count"))
        ]
        assert not dirty, f"{path.name} has saved output in cells {dirty}. Clear before committing"


def test_every_notebook_opens_with_a_title_and_the_course():
    """The first cell is what a student sees before deciding to keep reading."""
    for nb in NOTEBOOKS.values():
        assert nb.title, f"{nb.id} has no title"
        assert nb.markdown_cells >= nb.code_cells, (
            f"{nb.id} has more code than prose. These are read as much as run"
        )


def test_no_notebook_contains_something_shaped_like_an_api_key():
    """The same guard the project template's pre-commit hook applies.

    A key in a notebook is a key in a file that gets shared, published, and
    screenshotted. Colab has a secrets panel precisely so this never has to
    happen, and the Colab guide points at it.
    """
    import re

    looks_like = re.compile(r"(sk-ant-[A-Za-z0-9_-]{8,}|sk-[A-Za-z0-9]{32,}|ghp_[A-Za-z0-9]{20,})")
    for path in sorted(NOTEBOOKS_DIR.glob("*.ipynb")):
        hit = looks_like.search(path.read_text(encoding="utf-8"))
        assert not hit, f"{path.name} contains something shaped like a credential"


def test_complete_notebooks_are_actually_complete():
    """A notebook marked finished must not still be carrying TODO markers."""
    for path in sorted(NOTEBOOKS_DIR.glob("*.ipynb")):
        nb = NOTEBOOKS[path.stem]
        if nb.is_draft:
            continue
        raw = json.loads(path.read_text(encoding="utf-8"))
        for i, cell in enumerate(raw["cells"]):
            src = "".join(cell.get("source", []))
            assert "TODO(" not in src, (
                f"{path.name} is marked complete but cell {i} still has a TODO"
            )


def test_the_week_two_notebook_covers_what_week_two_taught():
    """The lab exists to make Tuesday's concepts concrete, so it has to touch them.

    Named explicitly rather than derived: this is the session the whole
    foundations week builds to, and a refactor that quietly drops word2vec from
    it would leave 46 study-guide concepts with nothing that exercises them.
    """
    raw = json.loads((NOTEBOOKS_DIR / "w02-thu.ipynb").read_text(encoding="utf-8"))
    text = "".join("".join(c.get("source", [])) for c in raw["cells"]).lower()

    for term in (
        "tokeniz",  # tokenization
        "countvectorizer",  # bag of words
        "tfidfvectorizer",  # tf-idf
        "idf",
        "word2vec",
        "cosine_similarity",
        "stop_words",
        "stem",
        "lemmat",
        "ngram_range",
        "skip-gram",
        "cbow",
        "polysemy",
        "pca",
    ):
        assert term in text, f"the Week 2 notebook no longer covers {term!r}"


def test_the_week_two_notebook_needs_no_api_key():
    """It runs on libraries, not on a paid endpoint.

    That is the whole reason it is the first one: nobody is blocked on access
    they have not been given yet, and nothing about embeddings requires it.
    """
    raw = json.loads((NOTEBOOKS_DIR / "w02-thu.ipynb").read_text(encoding="utf-8"))
    text = "".join("".join(c.get("source", [])) for c in raw["cells"])
    for forbidden in ("anthropic", "openai", "userdata.get", "API_KEY"):
        assert forbidden.lower() not in text.lower(), (
            f"the Week 2 notebook references {forbidden!r}; it is meant to need no account"
        )


def test_draft_notebooks_are_reported():
    """Not a failure -- a standing reminder of what is still owed.

    Printed rather than asserted because a draft is a legitimate state during
    term; what is not legitimate is losing track of how many there are.
    """
    drafts = sorted(n.id for n in NOTEBOOKS.values() if n.is_draft)
    if drafts:
        print(f"\n  {len(drafts)} notebook(s) still in draft: {', '.join(drafts)}")
    assert not NOTEBOOKS["w02-thu"].is_draft, "the Week 2 notebook must be finished"
