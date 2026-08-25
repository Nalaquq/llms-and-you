# LLMs & You: Attention is All You Need

Course website for a 15-week prompt engineering course at Hampden-Sydney
College, Fall 2026.

**Live site:** https://Nalaquq.github.io/llms-and-you/

---

## What this is

A syllabus, a schedule, and 28 session pages — generated from structured data
rather than written by hand.

Every date, reading, and session page derives from four YAML files. A reading is
defined once and referenced by id everywhere it appears. Semester dates exist in
exactly one place; changing a holiday reflows the whole schedule. A session that
references a reading which does not exist fails the build rather than rendering
an empty list to a student.

The repository is also a teaching artifact. The course asks students to keep a
decision log while building; [this site keeps
one](https://Nalaquq.github.io/llms-and-you/adr/), including the arguable
decisions about how the course itself is structured.

Course content lives in `data/*.yml` — that is the only source of truth. Session
pages under `docs/sessions/` are generated at build time and are not committed;
edit the YAML instead.

## Quick start

```bash
python -m venv .venv
.venv/bin/pip install -e ".[dev]"

.venv/bin/python -m mkdocs serve    # preview at localhost:8000
.venv/bin/python -m pytest          # validate the course data
```

## How it fits together

```
data/schedule.yml ──┐
data/resources.yml ─┼──> Pydantic validation ──> mkdocs-macros ──> schedule table
data/semester.yml ──┤         (loaders.py)      mkdocs-gen-files ─> 28 session pages
data/themes.yml ────┘                                              ──> readings page
```

`semester.yml` holds term bounds, two holidays, and three windows where sessions
run as individual meetings. `calendar.py` turns those into 28 dated meetings and
flags five of them — no session declares its own date or modality.

The individual-meeting windows record **only dates and a label**; the schema has
no field for why, and a test fails if someone adds one.

Conventions and common maintenance tasks are documented in the local
`CLAUDE.md` (not tracked).

## Tests

`tests/` checks that the *course* is coherent, not that the code runs:

- 28 meetings across 15 weeks, none on a holiday, each on a Tuesday or Thursday
- every referenced reading and theme exists
- labs assign no new reading — the workload promise, enforced
- sessions built around live debate do not land in an individual-meeting week
- grading weights total 100
- no reading is orphaned in the library

```
93 passed
```

## Course themes

1. How LLMs Work · 2. Prompt Engineering Technique · 3. Truthfulness,
Hallucination & Evaluation · 4. RAG & Retrieval · 5. Critical Perspectives ·
6. Responsible AI & Society · 7. Tools & Ecosystem · 8. Project Methodology &
Documentation · 9. Open-Weight Models · 10. Agents & Tool Use

## License

Course materials © 2026 Sean Gleason, released under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Linked readings
remain the property of their publishers; this site hosts none of them.
