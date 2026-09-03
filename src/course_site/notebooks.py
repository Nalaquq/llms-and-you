"""The Colab notebooks in ``notebooks/``, read as data.

Same contract as ``guides.py``: the file is the source of truth for its own
contents, and a session points at one by stem so the pointer can be checked at
build time rather than discovered broken by a student on a Thursday morning.

A notebook also declares whether it is finished. Drafts are visible on the site
as drafts -- a half-written notebook that looks finished is worse than one that
says so, because a student who cannot get a result out of it will assume the
fault is theirs.
"""

from __future__ import annotations

import functools
import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict

ROOT = Path(__file__).resolve().parents[2]
NOTEBOOKS_DIR = ROOT / "notebooks"

# Colab opens a notebook straight out of a public GitHub repository, which is
# what lets a student with no account and nothing installed run it in one click.
# The branch is pinned rather than derived: a link that silently followed the
# default branch would change under a student mid-semester.
COLAB_BASE = "https://colab.research.google.com/github/Nalaquq/llms-and-you/blob/main/notebooks"
GITHUB_BASE = "https://github.com/Nalaquq/llms-and-you/blob/main/notebooks"


class Notebook(BaseModel):
    """One ``.ipynb``, described by what is actually inside it."""

    model_config = ConfigDict(frozen=True)

    id: str
    """Filename stem, and the value a session's ``notebook`` field carries."""
    title: str
    """First heading of the first markdown cell."""
    status: str = "draft"
    code_cells: int = 0
    markdown_cells: int = 0

    @property
    def is_draft(self) -> bool:
        return self.status != "complete"

    @property
    def colab_url(self) -> str:
        return f"{COLAB_BASE}/{self.id}.ipynb"

    @property
    def github_url(self) -> str:
        return f"{GITHUB_BASE}/{self.id}.ipynb"


def _parse(path: Path) -> Notebook:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:  # a notebook that will not open in Colab either
        raise ValueError(f"notebook {path.name} is not valid JSON: {exc}") from exc

    cells = raw.get("cells", [])
    if not cells:
        raise ValueError(f"notebook {path.name} has no cells")

    first = "".join(cells[0].get("source", []))
    title = next(
        (line.lstrip("# ").strip() for line in first.splitlines() if line.startswith("# ")),
        "",
    )
    if not title:
        raise ValueError(
            f"notebook {path.name} does not open with a '# ' heading to use as its title"
        )

    course = raw.get("metadata", {}).get("course", {})
    return Notebook(
        id=path.stem,
        title=title,
        status=course.get("status", "draft"),
        code_cells=sum(1 for c in cells if c.get("cell_type") == "code"),
        markdown_cells=sum(1 for c in cells if c.get("cell_type") == "markdown"),
    )


@functools.cache
def load_notebooks() -> dict[str, Notebook]:
    found = (_parse(p) for p in sorted(NOTEBOOKS_DIR.glob("*.ipynb")))
    return {n.id: n for n in found}
