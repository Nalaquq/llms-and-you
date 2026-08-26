# Changelog

All notable changes to this course and its website.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses [Semantic Versioning](https://semver.org/) with a course
reading of what the numbers mean:

| | Means |
|:---|:---|
| **Major** (1.0.0) | A new offering of the course — a new semester |
| **Minor** (0.2.0) | A change students need to know about: readings, due dates, grading, schedule |
| **Patch** (0.1.1) | Corrections and site work that change nothing about the course |

Changes marked **[student-facing]** affect what is assigned, when it is due, or
how it is graded. During term, those are also announced in class — this file is
the record, not the announcement.

---

## [Unreleased]

### Changed — the Week 1 lab now sets up your whole repository **[student-facing]**

Thursday of Week 1 was *Lab: Keeping a Decision Record*, and it installed
Claude Code. It is now **Lab: Your Repository, and a Decision Record**, and it
runs the full setup in seven steps: a GitHub account, your own copy of the
[project template](https://github.com/Nalaquq/llms-and-you-project) via **Use
this template**, a clone onto your machine, `git config core.hooksPath
.githooks`, the Claude Code CLI, VS Code, and a walk through what every folder
in the repository is for.

The decision-record exercise is unchanged and still ends the session, and
**ADR-001 is still due that day** — but it now gets committed and pushed rather
than living on your laptop, and there are six or seven real decisions behind it
instead of one. Why the order changed is in
[ADR-007](https://Nalaquq.github.io/llms-and-you/adr/#adr-007-put-students-in-version-control-on-day-two-not-at-the-project).

Week 2 Thursday is unchanged: Python, a virtual environment, and the tokenizer
exercise. VS Code appears there now as the Python extension, plus a fallback
install for anyone who missed Week 1.

### Added — `TODO.txt` in the project template **[student-facing]**

A running list of what the next draft of your prompt has to do, sectioned by
where each item ends up — in the prompt, in `evals/`, in an ADR, or in a
question for me. Write the line the moment you have the thought; an hour later
you no longer have it. You start using it in the Week 1 lab. This repository
keeps the same file at its root.


### Changed — the project template is now findable **[student-facing]**

It was linked once, mid-way down the assignments page. It is now also on the
home page as a button, in the Guides index as a card and in that page's tools
table, and in the setup guide where students are already installing things.

### Changed — syllabus and schedule wording **[student-facing]**

Instructor revisions to the course description, the lecture/lab split, and the
prerequisites note. Three substantive changes inside them:

- **Both logs are now graded.** The project is assessed on an ADR log (why you
  chose something over the alternative) *and* a changelog (what actually
  changed, and when). They answer different questions and neither substitutes
  for the other. The [project template](https://github.com/Nalaquq/llms-and-you-project)
  now ships a `CHANGELOG.md` scaffold alongside `docs/adr/`.
- **Required Content now lists what is actually assigned.** The 3Blue1Brown
  entry pointed at the Neural Networks playlist dropped in ADR-006; it now
  links Chapters 5 and 6 directly.
- **Tooling is no longer prescribed as a single stack.** After API and CLI
  access are taught, students may fall back to whichever ecosystem works for
  them for other tasks.

### Added — a project template to start from **[student-facing]**

[Nalaquq/llms-and-you-project](https://github.com/Nalaquq/llms-and-you-project)
is a GitHub template repository for the semester project. Prompts as versioned
files, an evaluation set, an ADR log matching the format the course grades, and
a pre-commit hook that blocks committing an API key. It contains no project —
only the structure. Linked from the assignments page; using it is optional,
ending up with what it contains is not.

### Changed — foundations now starts at embeddings, not at gradient descent **[student-facing]**

3Blue1Brown's *Neural Networks* series (chapters 1-3) has been **dropped**. The
same deep-learning and gradient-descent material is already covered in the
instructor's remote sensing and computer vision courses, and covered there in a
pixel-forward form that points away from language. The history of AI/ML is not a
focus of this course. Full reasoning in [ADR-006](https://Nalaquq.github.io/llms-and-you/adr/#adr-006-enter-the-foundations-theme-at-the-embedding-matrix-not-at-gradient-descent).

Replaced by three videos from the same author, entering the theme at the point
where text becomes numbers:

- **Week 2** — *How word vectors encode meaning* (1 min) and *Transformers, the
  tech behind LLMs* (Chapter 5, 27 min).
- **Week 3** — *Attention in transformers, step-by-step* (Chapter 6, 26 min),
  assigned between Alammar and Vaswani so that query/key/value are familiar
  before Section 3 of the paper uses them unexplained.

Week 2 preparation drops from 180 to 143 minutes; Week 3 rises to 121. Close
reading is unchanged in Week 2 and still under cap in Week 3. Gradient descent
is now assumed rather than taught; Prince's *Understanding Deep Learning*
remains optional depth.

### Added — the post that earns the Transformer **[student-facing]**

Jay Alammar's *Visualizing a Neural Machine Translation Model (Seq2seq with
Attention)* is now required in **Week 2**. Week 3 asks "what problem was
attention invented to solve?" and, until now, nothing assigned answered it:
*The Illustrated Transformer* opens at self-attention and Vaswani assumes
seq2seq is already familiar. This is the missing first rung — the fixed-length
context vector, what breaks when the sentence is long, and the alignment
heatmaps that show what attention means before any mathematics is attached.

### Changed — every reading is now free and open access **[student-facing]**

**There is no longer a textbook to buy.** All 78 resources are open access; a
test (`test_every_reading_is_free_and_open`) now fails the build if a paywalled,
library-gated, or purchase-required reading is ever added.

Replacements:

- *Why Machines Learn* (purchase) → **3Blue1Brown's Neural Networks series**
  (chapters 1–3) as the foundations spine, with Simon Prince's *Understanding
  Deep Learning* (free MIT Press PDF) as optional depth.
- *Prompt Engineering for LLMs*, O'Reilly (purchase) → **Lee Boonstra,
  *Prompt Engineering*** (Google whitepaper, 68pp, free). Now required reading
  in Week 4 and carries the technique, RAG, and agent themes.
- ACM hallucination survey (paywalled) → the **arXiv version**
  ([2311.05232](https://arxiv.org/abs/2311.05232)) — same content, no gate.
- Dropped two unassigned gated items: the NYT open-weight piece and a
  ScienceDirect article.

Also enforced: **no `http://` reading URLs.** Michael Nielsen's excellent free
book was cut for being HTTP-only rather than sending students to an insecure
link.

### Added — technical spine: Python, VS Code, Claude API **[student-facing]**

The instructor's course description named Python, VS Code, and Anthropic's
Claude as core tools and gave "special emphasis" to deployment at scale. The
course now delivers that.

- **Theme 11 — Deployment, Cost & Production.** API integration, token
  accounting, prompt caching, batching, rate limits, and cost per user per
  month. Eleven new resources, all verified against the current API reference.
- **Setup is now two sessions, a week apart.** Week 1 Thursday installs
  **Claude Code** — no Python, no API key, no terminal experience assumed.
  Week 2 Thursday installs Python and VS Code and puts them straight to work on
  tokenization.
- **Week 1's lab is about the decision log, not the install.** Setting up Claude
  Code generates small decisions students make without noticing — install
  method, folder layout, whether they accepted the first suggestion. They write
  three of those up retrospectively, then do a task while writing the record
  *as they decide*, and feel the difference. The retrospective ones are tidy;
  the live one contains doubt, and that is the point.
- **[Setting up your tools](https://Nalaquq.github.io/llms-and-you/guides/setup/)** —
  a guide written for someone who has never opened a terminal, covering both
  sessions plus the errors that actually happen and what each one means.
- **Week 13 is now the deployment unit.** Tuesday is a cost teardown; Thursday
  instruments each student's project and then runs an open-weight model locally
  to ask whether self-hosting would be cheaper.

### Fixed — a lab that would have failed in class

- **The Week 1 temperature exercise was broken.** It asked students to run the
  same task at three `temperature` values. Frontier Claude models **removed**
  `temperature`, `top_p`, and `top_k` — sending them returns a 400. The lab
  would have errored in front of the room in week one.

  Rewritten as a Week 4 exercise sweeping `effort` instead, and turned into the
  lesson it should always have been: nearly every prompt-engineering tutorial
  online still tells you to adjust temperature, and the API reference is the
  authority when they disagree.

### Changed — schedule **[student-facing]**

- **Open-weight models lose their dedicated week** and are woven into the two
  places the question actually bites: the Week 13 cost lab (self-host vs API)
  and the Week 14 release-policy discussion (Amodei alongside *Auditing AI*).
  A test now enforces that a theme without sessions is still assigned somewhere,
  so "woven in" cannot quietly become "dropped."
- **Week 14 gained the release-policy argument** alongside auditing and labour —
  the same accountability question at two scales.

### Added — AI-use policy **[student-facing]**

- **The instructor's AI policy replaces the placeholder draft** in the syllabus.
  Generative AI is permitted by default and **must be cited**; each assignment
  states explicitly where it is not allowed. Hallucinations or AI slop fail the
  assignment regardless of whether AI was permitted. Use of AI on a no-AI
  assignment fails the assignment and goes to the Honor Court.
- **College-provided platforms** added to the course library and linked from the
  syllabus: [Microsoft Co-Pilot](https://m365.cloud.microsoft/) and
  [BoodleBox](https://boodlebox.ai/). Students should not be paying for personal
  subscriptions.
- **Guidance on acknowledging AI use**, with a worked example of an adequate
  citation, plus working definitions of "hallucination" and "slop" for grading
  purposes — pointing forward to Week 7, where both get defined properly.
- **Week 1 Tuesday expanded** to cover the policy at length, as the policy
  itself promises. Added a discussion question on what good and bad use looks
  like in a course about these tools.

### Changed — where restrictions appear

- `genai` is now a field on every assignment and session rather than prose.
  Prohibitions render as a red banner on the page they apply to and cannot be
  saved without a stated reason — the schema rejects them. The grading table
  gained a GenAI column. See
  [ADR-005](https://Nalaquq.github.io/llms-and-you/adr/).
- **Currently prohibited:** reading responses and Burchell reflections
  (including the in-class Week 15 reflection). Everything else permits AI with
  citation. **These are proposals awaiting instructor sign-off.**

### Changed — individual meetings replace the online-class framing **[student-facing]**

- Sessions in these weeks are titled **"Individual Meetings: …"** on the
  schedule — the meeting is what the session is, not a substitute for one.
- The Week 5 and Week 10 meetings now close with a **written goal** for the next
  milestone, checked at the following meeting.

### Fixed

- **Honor Code link was a 404.** `hsc.edu/student-life/honor-code` does not
  exist; corrected to
  [`/student-life/honor-and-conduct`](https://www.hsc.edu/student-life/honor-and-conduct).
- **Duplicate YAML keys now fail the build.** Plain YAML silently keeps the last
  of a repeated key; a duplicate `optional:` in a session dropped a reading with
  no error. The loader now rejects duplicates, naming the file and line.

---

## [0.1.0] — 2026-08-25

Initial build. Course website generated from structured data, covering all 15
weeks of Fall 2026.

### Added — course content

- **Ten themes**, up from the nine in the original resource map. Theme 10,
  *Agents & Tool Use*, was added to cover reasoning-and-acting loops, tool
  interfaces, and agent evaluation — a gap in the source material despite the
  applied course text devoting chapters to it. Placed in Weeks 11–12, after RAG.
- **28 sessions** across 15 weeks, each with a topic, theme, readings,
  discussion questions, and an in-class activity.
- **62 resources** in the course library, every URL verified with a live HTTP
  request on 2026-08-25.
- **Eight new resources** for the agents theme: ReAct, Toolformer, Reflexion,
  SWE-bench, τ-bench, Anthropic's *Building Effective Agents* and *Writing Tools
  for Agents*, and the Model Context Protocol documentation.
- **Grading scheme**: project + ADR log 35%, HackAPrompt red-team midterm 15%,
  labs 20%, reading responses 20%, participation 10%.
- **Four required ADR checkpoints** in Weeks 1, 5, 9, and 10.
- **The Burchell arc** as the course's recurring spine — five *Real Python*
  episodes with one guest from Aug 2022 to Apr 2026, assigned in Weeks 2, 7, and
  15 with a reflection after each.
- Guides: how to read a paper you cannot fully understand, how to write ADRs,
  and how individual-meeting weeks work.
- Public [decision log](https://Nalaquq.github.io/llms-and-you/adr/) recording the four structural
  choices behind the course, including the arguable ones.

### Added — site

- MkDocs Material site with light/dark themes, instant search, and a mobile
  layout.
- Bare clickable schedule table — week, date, topic — with each topic linking
  to a full session page. Cancelled meetings stay visible rather than being
  silently skipped.
- Session pages generated at build time; `docs/sessions/` is not committed.
- Pydantic schemas over all course data, so a bad reference fails the build.
- 93 tests validating that the *course* is coherent: 28 meetings on real dates,
  no session on a holiday, every reading reference resolving, grading weights
  totalling 100, labs assigning no new reading.
- GitHub Actions: lint, test, build, and deploy to Pages; weekly `lychee` link
  check with an issue opened automatically when a reading rots.

### Fixed — corrections to the source resource list

Found by verifying every URL and claim rather than trusting the list:

- **HaluEval** had no URL and an imprecise sample count. Now
  [arXiv:2305.11747](https://arxiv.org/abs/2305.11747); 35,000 samples total
  (5,000 human-annotated + 30,000 generated), not "10,000–35,000".
- **Qi et al., durable safeguards** was a `Search: ...` placeholder. Resolved to
  [arXiv:2412.07097](https://arxiv.org/abs/2412.07097), plus a code repository.
- **"Is Chain-of-Thought Reasoning a Mirage?"** was missing its subtitle:
  *A Data Distribution Lens*.
- ***Auditing AI*** confirmed genuinely open access, so it is assignable with no
  purchase — the only free book on the list.
- **Theme numbering** normalised to 1–10; the source file numbered them 1–9 but
  ordered them 1-7, 9, 8.
- Four links return 403/400 to automated clients (ACM, MIT Press, ScienceDirect,
  NYT). All verified live by hand and recorded in `.lycheeignore` so CI stops
  re-flagging them; the paywalled ones are marked as such on the site.

### Changed — five sessions become individual meetings **[student-facing]**

Five sessions across Weeks 4, 5, and 10 cannot run as a group class. Each
becomes a scheduled 15-minute individual meeting per student, with self-paced
work for the week. This forced a rearrangement:

- **Week 5 → Week 6**: the chain-of-thought debate moved to a week that meets
  as a group. It is the most discussion-dependent session in the course.
- **Week 5** now carries self-paced taxonomy work and the project-proposal
  meeting.
- **Week 10** now carries the RAG unit as self-paced work plus a prototype
  review.
- Individual-meeting windows are date ranges in `data/semester.yml`; session
  modality is derived, never tagged by hand. **The schema records no reason** —
  only dates and a label — and a test fails if someone adds a field that could
  disclose one.

**Known cost:** RAG lost a week. It now gets Week 10 alone and is introduced
without a live session, which is thin for a technical topic. Recorded in
[ADR-004](https://Nalaquq.github.io/llms-and-you/adr/) and flagged as the first thing to revisit after
this offering.

---

## Keeping this file

Add an entry whenever course content changes, not only when code does. During
term the useful question is "what changed since a student last looked at this
page?" — a moved deadline matters more to them than a refactor.

Mark anything affecting assignments, deadlines, or grading as
**[student-facing]** so it can be found quickly.

[Unreleased]: https://github.com/Nalaquq/llms-and-you/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Nalaquq/llms-and-you/releases/tag/v0.1.0
