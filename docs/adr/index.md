# Decision log

This course website keeps the same kind of decision log it asks students to
keep. Every significant choice — technical and pedagogical — is recorded here
with its reasoning and its alternatives.

It is public for two reasons. It is the clearest available example of the
format applied to real decisions, and several of these decisions are debatable,
which makes them better examples than clean ones would be.

Entries are deliberately short: the guide tells students an ADR is a short
document, so this log should be reviewable in about half a minute an entry. The
**Alternatives** section is the part worth reading.

See [Writing ADRs](../guides/writing-adrs.md) for the template.

---

## ADR-001: Generate the site from structured data rather than writing pages

**Status:** Accepted

### Context

The same fact appears in many places — a reading on the schedule, on a session
page, in the readings list. Hand-maintained, these drift, and a session page
listing a dropped reading is how a site stops being trusted.

### Decision

All course facts live in `data/*.yml`, validated by Pydantic. Every page derives
from them; session pages are generated at build time and not committed.

### Alternatives considered

- **Write 28 pages by hand.** Drift is the normal end state by about Week 9.
- **Readings only in the syllabus,** as CMU's 17-630 does. We wanted a clickable
  schedule where each session carries its own readings.
- **A database.** Absurd for 28 sessions, and unreviewable in a diff.

### Consequences

Changing a reading is a one-line edit; a bad resource id fails the build. The
cost: `docs/sessions/` is generated and must never be hand-edited.

---

## ADR-002: Derive dates and modality; never write them by hand

**Status:** Accepted

### Context

Two holidays remove meetings and three windows replace the group class. By hand
that is 28 chances to get a date wrong, and a recurring error where the schedule
and a session page disagree.

### Decision

`semester.yml` holds term bounds, holidays and individual-meeting ranges only.
`calendar.py` derives every date, week and modality.

### Alternatives considered

- **A date and a flag on each session.** Five hand-maintained flags that can
  silently disagree with the ranges they reflect.
- **Treat those dates as cancellations.** They are not — the session happens, as
  fifteen minutes per student. Students would see five cancelled sessions.

### Consequences

Adding a window is a three-line edit and every affected session reflags itself.
The cost is indirection: you cannot read a date off `schedule.yml`.

---

## ADR-003: Assign chain-of-thought and its refutation in the same week

**Status:** Accepted

### Context

Chain-of-thought is the most-cited technique in the field and the subject of
[a 2025 paper](https://arxiv.org/abs/2508.01191) calling it a mirage. The
convention saves the critique for an end-of-term unit there is never time for.

### Decision

Both in Week 6, in person, as a structured debate. Thursday's lab has students
test the disagreement themselves.

### Alternatives considered

- **CoT in Week 5, critique in Week 15.** Ten weeks of using a technique as
  settled makes the critique read as a footnote.
- **Teach only the technique.** Misrepresents the field to students who cannot yet
  tell that it is being misrepresented.

### Consequences

Students meet a technique and its strongest objection at once. Risk: some
conclude CoT does not work, which is not the claim — so the session questions
separate what the paper claims from what it does not. Week 6 must be in person.

---

## ADR-004: Replace the group class with individual meetings on five dates

**Status:** Accepted

### Context

Five sessions across Weeks 4, 5 and 10 cannot run as a group class.

### Decision

Each student gets a 15-minute slot and the week is self-paced. Both project
milestones land here; discussion-dependent material moves to weeks that meet.

### Alternatives considered

- **Run it over video.** Worse than the same seminar in a room, and everyone knows
  it.
- **Cancel and redistribute.** Too much content to absorb, and it removes contact
  during the project proposal.
- **Record lectures.** Strictly worse than one-to-one time, which is only possible
  because the class is small.

### Consequences

Guaranteed one-to-one time where the project needs it. The RAG unit drops to one
week and loses its group session — thin, and the part of the schedule most worth
revisiting after the first offering.

**One privacy consequence, designed in:** the schema records dates and a label
only. `test_conference_windows_record_no_reason` fails if someone adds a *why*.
This repository is public; a reason that does not exist cannot leak.

---

## ADR-005: Make the AI-use policy a field, not a sentence

**Status:** Accepted

### Context

The policy promises that every assignment will say if AI is not allowed. Backed
by an Honor Court referral, that cannot depend on remembering to write a
sentence — a restriction the student never saw is not enforceable.

### Decision

`genai` is a field on `Assignment` and `Session`, defaulting to `allowed`. A
prohibition without a `genai_note` fails to construct, and renders as a red
banner on the page it applies to.

### Alternatives considered

- **State it once in the syllabus.** Inverts the burden: a student would have to
  notice the *absence* of a permission.
- **Prohibit by default.** Contradicts the actual policy.
- **A boolean.** An enum with a required reason instead — "why is this one
  different?" always has an answer worth writing down.

### Consequences

Every restriction is visible and explained. An ad-hoc one now means touching the
data model rather than typing a sentence; that friction is intentional.

---

## ADR-006: Enter the foundations theme at the embedding matrix, not at gradient descent

**Status:** Accepted

### Context

The spine was 3Blue1Brown's *Neural Networks* chapters 1–3 — outstanding, and
wrong here. The instructor's remote sensing and computer vision courses teach the
same material more thoroughly and **pixel-forward**, pointing away from language.
Opening there also implies the history of ML is part of this course. It is not.

### Decision

Enter at the embedding matrix instead — word vectors and transformers in Week 2,
attention in Week 3. Gradient descent is assumed, not taught.

### Alternatives considered

- **Keep them, accept the duplication.** Costs the two weeks this course most
  needs.
- **Keep them as optional.** A prerequisite most of the room already has does not
  earn a place on a list whose value is that everything there is worth the time.
- **A language-first intro from another author.** Fixes pixel-forward, leaves the
  scope problem.

### Consequences

Week 2 drops from 180 to 143 minutes, entirely in listening. The risk is a
student who has taken neither prior course — check in Week 1 rather than
discovering it in Week 3, and restore chapters 1–2 as optional depth if the room
is mostly new.

---

## ADR-007: Put students in version control on day two, not at the project

**Status:** Accepted, amended by [ADR-014](#adr-014-make-the-project-copy-with-a-command-not-a-button)
and superseded in part by
[ADR-020](#adr-020-make-the-browser-the-supported-path-and-the-local-toolchain-optional)
— it now happens in the browser, not a terminal

### Context

The project template arrived around Week 5, so the first four ADRs lived outside
version control — and the practice of keeping prompts as versioned files was
taught weeks before students had anywhere to keep them.

### Decision

Week 1 Thursday runs the full setup: a GitHub account, a copy of the template, a
walk through the structure, then the decision-record exercise — which now has
real decisions behind it.

### Alternatives considered

- **Add only GitHub to Week 1.** An account without a repository is a form
  students fill in and forget.
- **Split across Weeks 1 and 2.** The walkthrough is what makes the copy mean
  anything, and Week 2 already carries its own lab.
- **Let students build the structure themselves.** What a professional would do.
  The structure is not what the course teaches; the practices it holds are.

### Consequences

Every ADR is committed, so the log is reviewable during term. Week 1 became the
densest session of the term — a cost ADR-020 later removed by taking the installs
out of it.

---

## ADR-008: Make "link the guide" a field with a test, not a habit

**Status:** Accepted

### Context

The site had four guides and **no session linked to any of them.** Students do
not browse this site; they open the session they are stuck on, the night before.
Remembering to paste links in is the fix that fails.

### Decision

`Session` gains a `guides` field. `guides.py` reads titles and anchors out of the
guide's own Markdown, so nothing is authored twice, and references are validated
at load time.

### Alternatives considered

- **Paste links into the prose and stop.** Half the answer — the inline per-step
  links stayed. Alone it leaves the next guide unlinked.
- **A `guides.yml`.** A second copy of headings that already exist — the exact
  drift this repo prevents.
- **Auto-link by keyword.** Which guide helps is a judgement about where students
  get stuck, and should be written down as one.
- **Validate anchors by building the site.** Too slow for a suite that runs on
  every edit.

### Consequences

Adding a guide fails the suite until a session points at it, forcing "who is
stuck, and where?" at the moment of writing. Renaming a linked heading fails too,
naming the sessions that pointed at it.

---

## ADR-009: Give every shell command a PowerShell half

**Status:** Accepted, amended by [ADR-012](#adr-012-tab-every-shell-command-including-the-identical-ones)
— the decision to leave identical commands untabbed was reversed

### Context

Every command was written for a Unix shell. To a student with no terminal
experience, `export: command not recognized` says nothing about what the command
should have been — and the likely conclusion is that the problem is them.

### Decision

Every divergent command appears for both platforms in linked tabs labelled
exactly **macOS / Linux** and **Windows (PowerShell)**. Choosing once follows the
reader across the site. `tests/test_platform_parity.py` enforces it.

### Alternatives considered

- **A `# Windows: ...` comment.** What the template did, and why this was easy to
  miss — it looks handled. A comment cannot be copied and run.
- **Write for WSL.** Adds an install and a class of path confusion for the student
  least sure of themselves.
- **Require one shell.** The first lab exists so everyone leaves with a working
  setup on the machine they own.
- **Show only the matching half.** In class we project one screen.

### Consequences

A wrong half only affects students the author does not share a platform with,
which is why the tests check the shape of the page rather than trusting review.
Pages are longer; accepted.

---

## ADR-010: Let Week 2 run over the reading cap, and say so on the page

**Status:** Accepted

### Context

The tests cap a session at 200 minutes total — the workload promise made
concrete. Week 2 is the foundations week everything after it assumes, and two
wanted additions take it to 241.

### Decision

Week 2 runs at 241 as an explicit exception rather than by relaxing the cap.
`HEAVY_SESSIONS` names the exact ceiling, so the next addition has to be decided
again. The **close-reading cap is never exceptioned** — all 41 minutes of
overrun are listening — and a test fails unless the page tells students it is
heavy.

### Alternatives considered

- **Raise the global cap.** Converts one deliberate week into a permanent licence.
- **Move Burchell #121 to Week 3.** Attractive — its title is Week 3's topic
  almost word for word. But the two episodes were recorded two weeks apart in the
  last summer before ChatGPT, and hearing them back to back is the point.
- **Demote #121 to optional.** Weakens the Week 15 reflection that traces the arc.
- **Add the primer as optional.** Contextual embeddings have no other source, and
  optional readings are not read.

### Consequences

241 minutes against a term norm of 140, in the week students are least practised
at pacing, mitigated only by telling them. Moving #121 stays costed and
available. The exception mechanism should stay rare.

---

## ADR-011: Make the required ADRs data, so the session pages announce them

**Status:** Accepted

### Context

Which four ADRs are due, and when, was written down three times. Two disagreed:
**ADR-001 and ADR-003 were in both Markdown tables and in neither session's `due`
field**, so no banner rendered and a student working from the schedule saw two of
their four graded ADRs announced nowhere.

### Decision

They move into `assignments.yml` as a `RequiredADR` list. Both tables become
macros, and the loader refuses to build if a required ADR's session does not name
it.

### Alternatives considered

- **Add the two missing `due:` lines.** Fixes today's bug in two lines; the bug
  was one fact living in three hand-maintained places with nothing checking them.
- **Keep the tables by hand, add a test.** A test comparing two hand-written
  tables says they disagree without saying which is right.
- **Its own `data/adrs.yml`.** A fifth data file for four rows belonging to one
  assignment.

### Consequences

Moving a session moves its deadline everywhere, including the guide page that
previously carried hand-typed dates. `due` strings stay prose — they are what the
banner says.

---

## ADR-012: Tab every shell command, including the identical ones

**Status:** Accepted. Amends [ADR-009](#adr-009-give-every-shell-command-a-powershell-half)

### Context

ADR-009 left identical commands untabbed, assuming a reader who notices and
infers "this is the same everywhere." For a student who has never opened a
terminal, "this is the Mac one and mine is missing" reads just as well — and
nothing distinguishes them, least of all the word `bash`, which names a shell
they do not have.

A duplicated tab costs one glance. A missing one costs the evening.

### Decision

Every shell block sits in a tab set with both halves, identical or not. The setup
guide says so outright, so an identical pair reads as convention rather than
error. Non-shell blocks are untouched.

### Alternatives considered

- **Explain the untabbed blocks in a note.** Asks the reader to learn a rule in
  order to read a page.
- **A third "Any platform" label.** Breaks tab linking: a reader who chose Windows
  lands on a set where their choice does not appear.

### Consequences

The rule is blanket and therefore checkable without judgement. Duplication
introduces a new failure — two halves that drift — which
`test_each_tab_holds_the_right_platform` covers.

---

## ADR-013: Authenticate GitHub with `gh`, and install the tools before using them

**Status:** Accepted. Largely retired by
[ADR-020](#adr-020-make-the-browser-the-supported-path-and-the-local-toolchain-optional)
— the command-line route is now optional

### Context

The guide had students run `git clone` and `git push` and never installed Git;
the only mention was a troubleshooting row, which is where you look *after* it
failed. Git also refuses to commit without an identity, and GitHub dropped
password auth in 2021 — each invisible to anyone who set their machine up years
ago, which is everyone who writes course material.

### Decision

Install Git, set the identity, then install and sign into `gh`, in that order,
before anything is cloned.

### Alternatives considered

- **A personal access token.** What GitHub's docs lead with: a scope page, an
  expiry decision, and a long-lived secret — in a course that spends the term
  saying not to paste keys into things.
- **SSH keys.** Better hygiene, wrong week: more new concepts than the rest of the
  lab combined.
- **GitHub Desktop.** Easier, and it hides what a commit is.
- **Let students hit the error.** The status quo, not a choice anyone made.

### Consequences

`test_labs_do_not_use_a_tool_the_guide_never_installs` checks the class of bug
rather than this instance, matching whole words — `git` is a substring of
`github`, and the first version passed while the bug was still present. Since
ADR-020 the labs run no shell commands, so it guards almost nothing.

---

## ADR-014: Make the project copy with a command, not a button

**Status:** Accepted. Amends [ADR-007](#adr-007-put-students-in-version-control-on-day-two-not-at-the-project).
Reversed by [ADR-020](#adr-020-make-the-browser-the-supported-path-and-the-local-toolchain-optional)

### Context

The lab said to press the green **Use this template** button; the instructor,
reading the page, could not find it. Describing a control by colour and position
fails readers who cannot tell "I am on the wrong page" from "the button moved" —
and colour is the one attribute some readers cannot perceive at all.

### Decision

One command — `gh repo create … --template … --public --clone` — which creates
and clones in one step. The web route survives as a collapsed fallback pointing
at the `/generate` form rather than at a button to hunt for.

### Alternatives considered

- **Plain `git clone`.** `origin` would be the instructor's repository, so
  everything works until `git push` fails at the end of the first lab. A fork
  stays tied to the original.
- **Describe the button better, or screenshot it.** A screenshot is stale at the
  next redesign; description by position is what just failed.
- **Link `/generate` as the primary route.** A genuine improvement, and what the
  fallback does — but the CLI is installed two steps earlier.

### Consequences

A failure surfaces at step 3 rather than an hour later, and no page names a
control by its colour. ADR-020 reversed this — not because the reasoning was
wrong, but because it assumed a terminal, which was the real problem.

---

## ADR-015: Order Week 2's readings general to specific

**Status:** Accepted

### Context

Week 2's seven items were ordered by accident of arrival, so a student meets
**word2vec before being told what an embedding is** — inviting the reasonable,
wrong conclusion that word2vec is what embeddings *are*.

### Decision

Three movements: what an embedding is, one way of building them, then what
replaced it. The session page says *take them in the order they are listed*, with
the reason — an unordered list of seven gets read shortest first.

### Alternatives considered

- **Shortest first,** for momentum. It is the order students use anyway if we give
  them none, and it puts the transformer video before the primer — the same
  inversion in a different disguise.
- **Interleave listening and reading.** The Burchell episodes are four years
  apart; playing them either side of word2vec suggests they belong together.
- **Explain it in prose instead.** The list is what students act on.

### Consequences

`test_foundations_week_runs_general_to_specific` pins the relationships rather
than the list, so a reorder that breaks the argument fails while adding an eighth
reading sensibly does not. Reading order is invisible in a YAML list, and exactly
what a later edit disturbs without noticing.

---

## ADR-016: Put the BoodleBox guide on every session that assigns reading

**Status:** Accepted

### Context

The college pays for BoodleBox, and the site mentioned it twice — on pages read
once in August. The students who would benefit most are the ones least sure they
are allowed, so the result is a paid-for subscription going unused.

The tension is real: reading responses are the one place GenAI is prohibited, and
they attach to exactly the readings a student would want help with.

### Decision

A guide linked from **every session that assigns reading** — thirteen — through
the ADR-008 mechanism. It leads with the boundary rather than burying it: *asking
a model to explain a passage you did not follow is fine; asking it to write your
response is not.*

### Alternatives considered

- **A syllabus paragraph.** What existed. It fails at the moment of need, which is
  a Sunday evening in Week 6.
- **A line in each session's prose.** Thirteen copies drifting apart, and prose
  renders as nothing the eye catches.
- **Link it from labs too.** Labs assign no reading, and a link that appears
  everywhere stops carrying information.
- **Name specific models for specific readings.** A shelf life in months.

### Consequences

Two tests hold it: one requires the link on any session with readings, the other
requires the guide to name the prohibited work, since a student arriving from a
session page may never open the syllabus.

---

## ADR-017: Make course concepts data, and give them a page of their own

**Status:** Accepted

### Context

Week 1's discussion of Norman's affordances was the most useful thing that
happened that day, and by the end the concept existed nowhere on this site. The
schedule records what a session *was about*, not what a student is *responsible
for* — so students revise from a sixty-item reading list they cannot triage.

### Decision

`data/concepts.yml` and a generated [study guide](../study-guide.md). Two fields
are required that could have been optional: `mastery`, because a guide that lists
topics says what to worry about rather than what to practise; and `assessed_in`,
because the page promises everything on it is assessable.

### Alternatives considered

- **Put it in the session's `summary`.** Nobody reopens eleven session pages to
  reconstruct a list.
- **A hand-written glossary.** The copy goes stale while claiming to say what
  students are graded on.
- **Attach concepts to themes, not sessions.** Loses *when* we did this, and
  therefore which reading it came with.
- **Make `assessed_in` optional.** A study guide is useful in proportion to what
  it leaves out.

### Consequences

Adding a concept is a YAML entry and everything follows. Nothing in the build can
detect an idea that was never written down — what it can do is refuse to let a
written-down one be vague, unassessed, or unreachable.

---

## ADR-018: Break the study guide down to the vocabulary, and record what each concept needs first

**Status:** Accepted

### Context

Week 2's readings assume a vocabulary the class does not have — "one hidden
layer" without explaining a layer, TF-IDF without saying what a corpus is. The
first draft grouped them: one "bag of words" entry absorbing five techniques,
which offers no way to find out *which* of the five lost you.

### Decision

**Split to the individual term** — if a student can get it wrong on its own, it
is its own entry. Week 2 goes to forty-six.

**Add `builds_on`,** a directed prerequisite edge. The loader refuses a missing
prerequisite, a self-reference, one introduced later than the concept needing it,
and a cycle.

### Alternatives considered

- **Keep the grouping, write longer entries.** A paragraph with five undefined
  terms fails silently — the student cannot report which one lost them.
- **Leave relationships in prose.** Prose cross-references rot and cannot be
  validated; a broken prerequisite is the same error class as a broken id.
- **Use `related` for prerequisites.** Direction is the whole value: "see also"
  and "you cannot read this yet" are different messages.
- **A separate glossary.** Terms exiled there read as optional.
- **Render the graph as a diagram.** Forty nodes is unreadable as a picture.

### Consequences

At this granularity most entries are assessed cumulatively, and `assessed_in` is
honest about it. The real cost is on later weeks: an inconsistent guide is worse
than a uniformly coarse one, so Weeks 3–15 must follow as they are taught.

---

## ADR-019: Host the lecture decks, and publish how they were made

**Status:** Accepted

### Context

The Week 2 deck is twenty-seven animated slides generated by scripts, themselves
written by Claude Code from four prompts. Where do decks live, and what happens to
the making-of story — arguably more instructive here than the deck?

The second cuts against `prompts/` being gitignored as "drafting artifacts". This
sequence is a finished worked example of the course's central skill, including a
disagreement with the model that the instructor won.

### Decision

A **Slides** page holding each deck plus the prompt sequence that produced it.
Media is generated from committed scripts at deploy time and never committed. Two
downloads: the animated deck, and a print edition, because PowerPoint prints a
GIF's first, nearly empty frame.

### Alternatives considered

- **Commit the media.** Twenty megabytes into git history per iteration, forever,
  for pure build products.
- **Host the deck, not the prompts.** The prompts are the part that teaches the
  course's own subject.
- **One deck file.** Every student who printed the animated one would get nothing.

### Consequences

`gen_slides.py` fails loudly with the command to run if media is missing, so a
local build cannot silently produce a deckless page. The prompt sequence will
age; it records how this deck was made, not a recommendation.

---

## ADR-020: Make the browser the supported path, and the local toolchain optional

**Status:** Accepted. Supersedes
[ADR-007](#adr-007-put-students-in-version-control-on-day-two-not-at-the-project)
in part; reverses
[ADR-014](#adr-014-make-the-project-copy-with-a-command-not-a-button)

### Context

Week 1 asked students with no programming background to install Git, `gh`, Claude
Code and VS Code and push a commit, in 75 minutes, on whatever laptop they own.
Week 2 added Python and a virtual environment.

It did not work — PATH, PowerShell execution policy, `python3` versus `python`, a
missing `winget`. Those consumed the first two weeks and taught nothing about
language models, in the fortnight where students decide whether they belong here.

### Decision

**The browser is the supported path for everything the course grades.** Week 1 is
a GitHub account, a template copy, and ADR-001 committed in the web editor. Every
lab from Week 2 is a notebook opened in Colab. Labs prefer libraries to APIs, and
the local toolchain is documented in full but required by nothing.

### Alternatives considered

- **Teach the toolchain harder.** The failures are environmental. More teaching
  does not install `winget`.
- **A cloud environment we control** (Codespaces, JupyterHub). Better ergonomics,
  costly to provision, and leaves students nothing after the term.
- **Drop GitHub too, ADRs in a shared document.** Seriously considered. Version
  control is what makes a log honest: a document can be quietly backdated.
- **Delete the local instructions.** Week 13 asks whether self-hosting is worth
  it, which reads differently if nobody has run anything locally.

### Consequences

Nobody is blocked on an install, and a Chromebook is now sufficient — quietly
removing a hardware cost barrier nobody had named. Students no longer learn `git`
in Week 1: a real loss, taken deliberately.

Colab is a Google dependency we do not control, but the notebooks are plain
`.ipynb` that run in Jupyter, VS Code or Kaggle unchanged.

---

## ADR-021: Make Thursday a showcase, and put the exploration before it

**Status:** Accepted

### Context

Thursdays were guided labs, though the syllabus had already conceded the problem:
labs should *"showcase what we learned rather than following a series of steps
together as a class like robots"*.

Lockstep labs move at the speed of whoever is most stuck, and following steps
successfully shows no understanding because nobody made a decision. There is also
a rubric mismatch — labs are graded on the write-up, and thirteen people running
the same cells produce thirteen identical ones.

### Decision

Each lab has a notebook that works and is explicitly not a worksheet; every
section ends with open questions it does not answer. Thursday is ten minutes
each: a claim plus the evidence, and **a method that broke is worth more than one
that worked**. Working code is not required.

### Alternatives considered

- **Guided labs plus optional extensions.** The extensions are what the session is
  for, and anything after the required part is read as optional.
- **A specific deliverable per lab.** Recreates the worksheet, and makes the
  finding nobody predicted worth no marks.
- **Group presentations.** Thirteen slots fit the session, and a group of four
  produces one exploration rather than four.

### Consequences

Thursday preparation is now real work done alone, which students must be told
rather than discover. Labs still assign no reading, so the workload promise holds.

Every notebook must now be genuinely runnable before its session, because a
student hitting a broken cell alone at 9pm has no recourse.
