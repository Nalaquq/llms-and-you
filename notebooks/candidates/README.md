# Candidate notebooks

Notebooks being evaluated, not yet taught. Nothing in this directory is wired to
a session: `notebooks.py` globs `notebooks/*.ipynb` and does not recurse, so a
file in here is invisible to the loader, to the site, and to
`test_every_notebook_belongs_to_a_session`. That is the point — a candidate can
sit alongside the notebook it might replace without either one pretending to be
the other.

To promote one: move it to `notebooks/`, point the session's `notebook` field at
its stem, flip `metadata.course.status` to `complete`, and run `pytest`.

Open a candidate in Colab by pasting its GitHub path into
<https://colab.research.google.com/github/Nalaquq/llms-and-you>, or by editing
a normal notebook's Colab URL to include `candidates/`.

---

## Promoted

`w03-thu-english.ipynb` was evaluated here and promoted in September 2026. It is
now `notebooks/w03-thu.ipynb`, the primary Week 3 lab, and the translation
notebook it replaced is `notebooks/w03-thu-translation.ipynb`, offered beside it
through the session's `deep_dive` field. See ADR-024 for the reasoning and the
costs.

This directory is empty of candidates again, which is its resting state.
