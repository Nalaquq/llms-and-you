# Decision log

This course website keeps the same kind of decision log it asks students to
keep. Every significant choice — technical and pedagogical — is recorded here
with its reasoning and its alternatives.

It is public for two reasons. It is the clearest available example of the
format applied to real decisions, and several of these decisions are debatable,
which makes them better examples than clean ones would be.

See [Writing ADRs](../guides/writing-adrs.md) for the template.

---

## ADR-001: Generate the site from structured data rather than writing pages

**Status:** Accepted

### Context

A 15-week course site contains the same facts in many places. A reading appears
on the schedule, on a session page, and in the readings list. A date appears on
the schedule, in the syllabus, and in an assignment description. Written by
hand, these drift — and the first time a student is sent to a session page
listing a reading that was dropped three weeks ago, the site stops being
trusted.

### Decision

All course facts live in four YAML files (`semester.yml`, `themes.yml`,
`resources.yml`, `schedule.yml`), validated by Pydantic models, and every page
is derived from them. Session pages are generated at build time and are not
committed to the repository.

### Alternatives considered

**Write 28 session pages by hand.** Faster to start, and it is what most course
sites do. Rejected because the drift problem is not hypothetical — it is the
normal end state of a hand-maintained course site by about Week 9.

**Keep readings only in the syllabus,** as CMU's 17-630 does, with a bare topic
schedule. Rejected because the explicit goal was a clickable schedule where each
session carries its own readings.

**A database.** Rejected as absurd overhead for 28 sessions and 62 resources,
and it would make the course content unreviewable in a diff.

### Consequences

Changing a reading is a one-line edit that propagates everywhere. A typo in a
resource id fails the build rather than rendering an empty list. The cost is
that adding a session means editing YAML rather than writing Markdown, and
anyone maintaining this later needs to understand that the `docs/sessions/`
directory is generated and must not be edited.

---

## ADR-002: Derive dates and modality; never write them by hand

**Status:** Accepted

### Context

The Fall 2026 term has two holidays that remove class meetings, and three
windows where sessions run as individual meetings rather than a group class.
Five of 28 sessions are affected. Encoding this by hand means 28 opportunities
to get a date wrong, and a recurring error mode where the schedule says one
thing and a session page says another.

### Decision

`data/semester.yml` holds only term bounds, holiday dates, and individual-meeting
date ranges. `calendar.py` derives every meeting date, assigns it to a course
week, and sets the session's modality from whether it falls inside one of those
windows. No session declares its own date or modality.

### Alternatives considered

**Tag each session with a date and a boolean flag.** Rejected: it is five
hand-maintained flags that can silently disagree with the date ranges they are
supposed to reflect.

**Treat those dates as cancellations.** Rejected because they are not
cancellations. The session happens — as fifteen minutes with each student rather
than seventy-five with all of them. Modelling them as holidays would have shown
students five cancelled sessions, which is both wrong and worse.

### Consequences

Adding a window is a three-line edit and every affected session reflags itself. Scheduling a session on a date the class does not meet raises a
build error naming the holiday. The trade-off is indirection: you cannot read a
session's date off `schedule.yml`, you have to run the code or read the built
site.

---

## ADR-003: Assign chain-of-thought and its refutation in the same week

**Status:** Accepted

### Context

Chain-of-thought is the most-cited prompting technique in the field and a
required part of any serious course on the subject. It is also the subject of
[a 2025 paper](https://arxiv.org/abs/2508.01191) arguing it is a mirage — that
apparent reasoning is pattern-matching over the training distribution.

The conventional approach teaches the technique in the techniques unit and
saves the critique for a critical-perspectives unit at the end of the term, if
there is time. There usually is not.

### Decision

Both are assigned in Week 6, in person, with a structured debate as the session
activity. The lab that Thursday has students construct tasks inside and outside
the plausible training distribution and test the disagreement themselves.

### Alternatives considered

**Teach CoT in Week 5, critique it in Week 15.** The standard structure.
Rejected because ten weeks of using a technique as though it were settled makes
the later critique feel like a footnote rather than a live question.

**Teach only the technique.** Defensible for a purely applied course. Rejected
because it would misrepresent the state of the field to students who cannot yet
tell that it is being misrepresented.

### Consequences

Students learn a technique and its strongest objection simultaneously, which is
harder and more honest. The risk is that some come away thinking
chain-of-thought does not work, which is not what the paper claims — so the
session questions explicitly separate what the paper claims from what it does
not.

This also forces a scheduling constraint: Week 6 must be in person. It is.

---

## ADR-004: Replace the group class with individual meetings on five dates

**Status:** Accepted

### Context

Five sessions across Weeks 4, 5, and 10 cannot run as a group class. Something
has to happen in them, and the default options are all bad.

### Decision

Those sessions become **individual meetings**: each student gets a scheduled
15-minute slot, and the week's work is self-paced. Both project milestones — the
proposal and the prototype — are scheduled into these weeks, and each meeting
ends with a written goal for the next stretch. Discussion-dependent material is
scheduled into weeks that meet as a group.

The session's topic on the schedule simply reads *"Individual Meetings: …"*.
That is what the session is; no further explanation is offered.

### Alternatives considered

**Run the class over video.** Rejected. A seminar with twenty-five students over
video is worse than the same seminar in a room, everyone knows it, and
pretending otherwise wastes an hour of everyone's time. The material originally
scheduled for Week 5 was the chain-of-thought debate — the most
discussion-dependent session in the course. It moved to Week 6.

**Cancel and redistribute.** Rejected: five sessions is too much content to
absorb, and it would leave students without contact during the stretch that
includes their project proposal.

**Record lectures.** Rejected as strictly worse than one-to-one time. Fifteen
minutes of individual attention on a student's own project beats seventy-five
minutes of recorded talk, and it is only possible because the class is small.

### Consequences

Every student gets guaranteed one-to-one time at the two points where their
project most needs it, and project feedback moves out of the classroom, where it
never belonged. The goal-setting close gives each meeting a checkable output.

The costs are real. The RAG unit gets one week rather than two and is introduced
without a group session, which is thin for a technical topic students have not
seen before — Berryman & Ziegler's chapters carry more weight there than they
should have to. That is the part of the schedule most worth revisiting after the
first offering.

**One privacy consequence, deliberately designed in:** the schema records only
the dates and a label. There is no field for *why* a week runs this way, and
`test_conference_windows_record_no_reason` fails if someone adds one. This
repository is public; a reason that does not exist cannot leak.

## ADR-005: Make the AI-use policy a field, not a sentence

**Status:** Accepted

### Context

The course policy is permissive by default: students may use Generative AI
unless an assignment says otherwise, and must cite it when they do. Using AI
where it is prohibited fails the assignment and goes to the Honor Court.

That policy makes a promise — *"each assignment will note specifically if
Generative AI is not allowed."* A promise of that kind, backed by an Honor Court
referral, cannot depend on somebody remembering to write a sentence on the right
page. If a restriction exists but is not visible where the student is working,
the referral is not defensible.

### Decision

`genai` is a field on both `Assignment` and `Session`, defaulting to `allowed`.
A prohibition is invalid without an accompanying `genai_note` — the Pydantic
model refuses to construct one, so the build fails rather than rendering a
silent restriction.

Prohibitions render as a red banner at the top of the page they apply to.
Permitted work renders a short reminder that citation is required. The grading
table carries a GenAI column so the whole policy is visible at a glance.

### Alternatives considered

**State the policy once in the syllabus and rely on prose elsewhere.** The
normal approach. Rejected because it inverts the burden: a student would have to
notice the *absence* of a permission rather than the presence of a restriction,
and the failure mode is a student penalised for a rule they were never shown.

**Prohibit AI by default and mark exceptions.** Rejected because it contradicts
the actual policy and would misrepresent a course whose subject is these tools.

**A boolean.** Rejected in favour of an enum with a required justification. The
question "why is this one different?" always has an answer worth writing down,
and requiring it prevents restrictions accumulating without reasons.

### Consequences

Every restriction is guaranteed visible and guaranteed explained. Adding one is
a two-line YAML edit that cannot be done carelessly. Tests assert that
prohibitions carry reasons, that the default stays permissive, and that the
Week 1 session still covers the policy — so a future edit that quietly inverts
the default will fail rather than surprise a student.

The cost is that a genuinely ad-hoc restriction ("not on this one thing, for
this one reason") now requires touching the data model rather than typing a
sentence. That friction is intentional.

**Currently prohibited:** reading responses and Burchell reflections, and the
in-class Week 15 reflection. Everything else permits AI with citation. Those
choices are the instructor's and are the most likely part of this ADR to change
after the policy discussion in Week 1.

---

## ADR-006: Enter the foundations theme at the embedding matrix, not at gradient descent

**Status:** Accepted

### Context

The foundations spine was 3Blue1Brown's *Neural Networks* series, chapters 1-3:
what a neural network computes, gradient descent, and backpropagation. It is an
outstanding series and it was the right choice for a course starting from
nothing.

It is the wrong choice for *these* students. The same material is already taught
in the instructor's remote sensing and computer vision courses, and taught more
thoroughly there. Worse, it is taught **pixel-forward** — the worked examples are
images, the intuitions are convolutional, and a student arriving from those
courses meets gradient descent for the second time in a form that points away
from language rather than toward it.

There is also a scope question underneath. Spending the opening weeks on how
neural networks came to work implies that the history of AI/ML is part of what
this course covers. It is not. This course starts at the point where text
becomes numbers and moves forward from there.

### Decision

Drop the *Neural Networks* series. Enter the theme at the embedding matrix
instead, using two later videos from the same author and one more in Week 3:

- **Week 2** — *How word vectors encode meaning* (1 min) and *Transformers, the
  tech behind LLMs* (Chapter 5, 27 min). Chapter 5 opens on tokens and
  embeddings, which is exactly where Week 2 opens, and reaches a working
  Transformer without requiring backpropagation.
- **Week 3** — *Attention in transformers, step-by-step* (Chapter 6, 26 min),
  placed between Alammar and Vaswani. It constructs query, key, and value on
  screen, which is the notation Section 3 of the paper introduces without
  explanation.

Gradient descent is now assumed, not taught. Where a paper depends on it,
Prince's *Understanding Deep Learning* remains optional depth.

### Alternatives considered

**Keep chapters 1-3 and accept the duplication.** Rejected. Reteaching material
students already have is not free — it costs the two weeks this course most
needs, and it teaches students that the reading list is not written for them
specifically.

**Keep them as optional rather than required.** Tempting, and rejected for a
narrower reason: the optional list is where a student goes when they want more,
and its value depends on everything there being genuinely worth the time *for
this course*. A prerequisite that most of the room already has does not qualify.

**Replace with a language-first introduction to neural networks from another
author.** Rejected because it solves the pixel-forward problem while leaving the
scope problem untouched. The issue is not which examples the video uses. It is
that the course does not need the unit.

### Consequences

Week 2 now runs 143 minutes of preparation against 180 before, and the close
reading within it is unchanged at 65 minutes — the reduction is entirely
listening. Week 3 gains 26 minutes and still sits at 95 minutes of close
reading, under the 120-minute cap asserted by
`test_weekly_reading_load_stays_reasonable`.

The risk is a student who has *not* taken remote sensing or computer vision and
has never seen a neural network. Chapter 5 was chosen partly because it is
self-contained enough to absorb that student, but this assumption should be
checked in Week 1 rather than discovered in Week 3. If the room turns out to be
mostly new to the material, the honest fix is to restore chapters 1-2 as
optional depth, not to reverse this decision.

---

## ADR-007: Put students in version control on day two, not at the project

**Status:** Accepted

### Context

The Week 1 lab installed Claude Code, and nothing else. GitHub, the project
template, and VS Code arrived later — the template was mentioned on the
assignments page, and students met it when they started the project around
Week 5.

That ordering had three costs. Students spent the first month working in
whatever folder they happened to create, so the first four ADRs lived somewhere
that was not under version control and in several cases not backed up at all.
The template's structure — `prompts/`, `evals/`, `docs/adr/` — encodes the three
practices the project is graded on, and meeting it in Week 5 means meeting it
after the habits it is meant to shape have already formed. And the Week 1 lab
manufactured decisions to record from a single install, which is thin material.

The course also asks students to keep prompts as versioned files. A student
without a repository cannot do that, so the practice was being taught weeks
before it was possible to follow.

### Decision

The Week 1 Thursday lab now runs the full setup: a GitHub account, a copy of
the project template taken with **Use this template**, a clone onto the
student's machine, the credential guard turned on, the Claude Code CLI, VS Code,
and a walk through the directory structure. The decision-record exercise stays
where it was, at the end, and now has six or seven real decisions behind it
rather than one.

The template gains a `TODO.txt` — a running list of what the next draft of a
prompt has to do, sectioned by where each item ends up: the prompt, `evals/`,
an ADR, or a question for the instructor. Students start using it in the lab.
This repository keeps the same file at its root, for the same reason it keeps
an ADR log.

### Alternatives considered

**Leave the template at Week 5 and add only GitHub to Week 1.** Rejected. An
account without a repository to put in it is a form students fill in and forget.
The account is only useful on the day it holds something.

**Split it: GitHub and the clone in Week 1, VS Code and the walkthrough in
Week 2.** The genuinely tempting option, because Week 1 is now full. Rejected
because the walkthrough is what makes the clone mean anything — a folder you
cannot read is not a folder you will work in — and because Week 2's lab already
carries Python, a virtual environment, and the tokenizer exercise.

**Have students start from an empty repository and build the structure
themselves over the term.** Pedagogically defensible, and it is what a
professional would do. Rejected because the structure is not what the course is
teaching; the practices it holds are. Twelve weeks of unstructured folders would
produce twelve weeks of arguing about folders.

### Consequences

Week 1 Thursday is now the densest session of the term, and it is a session
where any student can be blocked by an unfamiliar machine. The lab is written to
be run as seven numbered steps for exactly that reason, and steps 1 to 6 are
done together at one pace. If it overruns, the ADR exercise is the part that
moves to homework — it is the only part that does not need the room.

Every ADR from ADR-001 onward is committed and pushed, which means the decision
log is reviewable during term rather than at the end of it. Week 2's lab is
unchanged: it still installs Python and a virtual environment, and VS Code
appears there now as the Python extension plus a fallback for anyone who missed
Week 1. The duplication is deliberate.

The risk is a student who joins the course in Week 2 and has no repository. The
setup guide is written so that the Week 1 section can be worked through alone,
which is the same fallback that already existed for the Claude Code install.

---

## ADR-008: Make "link the guide" a field with a test, not a habit

**Status:** Accepted

### Context

The site has four written guides — setup, reading papers, writing ADRs, and
individual meetings — and until now **no session linked to any of them.** They
were reachable from the Guides index and from the top navigation, and nowhere
else.

That is the wrong place for them. Students do not browse this site. They open
the session they are stuck on, usually the night before, and read that one page.
A guide written for exactly that moment, linked from a page they were not on,
is a guide that does not get read. The Week 1 lab was the clearest case: seven
steps, every one of them written up in `setup.md`, and not one link.

The obvious fix — remember to paste the links in — is the fix that fails. It is
the same failure mode ADR-005 identified for the AI policy: a rule that lives in
someone's memory is a rule that holds until the week it does not.

### Decision

`Session` gains a `guides` field: a list of `slug` or `slug#anchor` references
into `docs/guides/`. Guides are read out of their own Markdown files by
`guides.py`, which takes the title from the H1 and maps every anchor to the
heading it names, so nothing is authored twice. References are validated at load
time against both the file and the heading. They render as an admonition above
the reading list, naming the specific section where one is given.

Three tests hold the rule up:

- `test_every_guide_is_reachable_from_a_session` — if we wrote a guide, some
  session names it. This is the rule itself.
- `test_setup_sessions_point_at_the_setup_guide` and
  `test_individual_meeting_sessions_explain_themselves` — the two cases where a
  missing link strands a student with no way forward.
- `test_guide_links_written_into_prose_still_resolve` — session prose also links
  to guide sections inline, step by step. Those are plain text and would rot
  silently, so they are checked by the same rule.

### Alternatives considered

**Paste the links into the session prose and stop there.** What was asked for,
and it is half the answer — the inline per-step links are genuinely the useful
ones, and they stayed. Rejected on its own because it fixes the four sessions
someone thought about and leaves the next guide unlinked, which is how this
happened in the first place.

**A `guides.yml` data file.** Rejected. The guide's title and its headings
already exist in the guide, and a second copy in YAML is a second thing to
update when a heading is reworded — the exact drift this repository is built to
prevent. Reading the Markdown is more code and less duplication, and it is the
right trade at four files.

**Auto-link by theme or keyword** — infer that a session mentioning `pip` wants
the setup guide. Rejected as too clever. Which guide helps is a judgement about
where students get stuck, and it should be written down as a judgement.

**Validate anchors by building the site and checking the HTML.** Rejected as too
slow for a test suite that runs on every edit. `guides.py` mirrors the toc
extension's slugify instead, and `test_guide_anchors_match_what_markdown_will_generate`
compares the two directly, so drift in the upstream slug rules fails here rather
than in a student's browser.

### Consequences

Adding a guide to `docs/guides/` now fails the test suite until some session
points at it. That is the intended cost: it forces the question "who is stuck,
and where?" at the moment the guide is written rather than never.

Renaming a heading in a guide also fails, naming the sessions that pointed at
it. This is the same bargain as resource ids, and it is worth the same price.

The `{ #anchor }` convention matters more than it did. A heading with an
explicit anchor is stable under rewording; one without changes its anchor when
the words change. Guides whose sections are linked from sessions should carry
explicit anchors, and `setup.md`'s two week headings already do.

---

## ADR-009: Give every shell command a PowerShell half

**Status:** Accepted, amended by [ADR-012](#adr-012-tab-every-shell-command-including-the-identical-ones)
— the decision to leave identical commands untabbed was reversed

### Context

Every command on this site was written for a Unix shell. The one exception was
the virtual environment block in the setup guide, which had a Windows tab
because that is where the difference is impossible to miss.

The rest silently assumed macOS or Linux: `python3` where Windows wants
`python`, `export` where Windows wants `$env:`, `source .venv/bin/activate`
where Windows wants `.venv\Scripts\Activate.ps1`. Students bring whatever laptop
they own, and a meaningful share of the room brings Windows.

For a student with no prior terminal experience — which this course explicitly
assumes — this is not a small inconvenience. `export: command not recognized`
carries no information about what the command should have been. The student
cannot tell whether they typed it wrong, installed something wrong, or are
reading instructions written for a machine they do not have. The most likely
outcome is that they conclude the problem is them.

There was also a subtler failure. A Windows student who works out `$env:` on
their own then finds the next page assumes bash again, and the one after that.
The cost is not one lookup; it is a running tax on every page, paid only by the
students least equipped to pay it.

### Decision

Every command that differs between shells is shown for both, in linked content
tabs labelled exactly **macOS / Linux** and **Windows (PowerShell)**. Material's
`content.tabs.link` is enabled, so choosing a platform once follows the reader
across every tab set on the site.

Commands that are identical — `git clone`, `git config`, `claude`,
`python -m project.main` — are deliberately **not** tabbed. Wrapping an
identical command in two tabs implies a difference that is not there, and
teaches students to stop reading the labels.

The setup guide states the convention before using it, and the Week 1 lab says
plainly that everything in that session is the same on all three platforms and
that the divergence starts in Week 2.

Windows also gets the two things bash users never see: the
`Set-ExecutionPolicy` incantation that PowerShell requires before a venv will
activate, and the fact that `SetEnvironmentVariable` does not affect the window
you typed it in. The troubleshooting table now carries PowerShell's wording of
each error next to bash's, because `The term 'python3' is not recognized` and
`command not found: python3` are the same problem and do not look like it.

`tests/test_platform_parity.py` enforces this. A shell block containing a
divergent construct outside a platform tab set fails; a tab set covering only
one platform fails; an off-convention tab label fails.

### Alternatives considered

**A `# Windows: ...` comment on the bash line.** What the project template did,
and it is why this was easy to miss — it looks like the problem is handled. It
fails for the case that matters: a comment cannot be copied and run, it puts the
Windows student's instructions in a place they must mentally edit, and it does
not survive a command longer than one line.

**Write for WSL and tell Windows students to install it.** Rejected. It is the
answer a developer gives, and it is wrong for this room: it adds an install, a
second filesystem, and a class of path confusion to the machine of the student
who is already least sure of themselves — to save the instructor writing a
second line.

**Pick one shell and require it.** Rejected for the same reason the course does
not require a particular laptop. The point of the first lab is that everyone
leaves it with a working setup on the machine they actually own.

**Detect the platform and show only the matching half.** Rejected as fragile and
worse for the room: in class we project one screen, and an instructor demoing on
macOS should still be able to point at what the Windows half says.

### Consequences

Both halves must now be kept correct, and the wrong half of a tab set is a bug
that only affects students the author does not share a platform with. That is
exactly the drift the parity tests exist to catch, and it is why they check the
shape of the page rather than trusting review.

Pages are longer. A tab set occupies more vertical space than a code block, and
the setup guide grew by roughly a third. Accepted: the page is a reference read
under pressure, not an essay.

The project template repository is covered by the same decision but not by the
same mechanism — GitHub renders README files as plain Markdown and does not
support content tabs. There the halves are bold-labelled blocks instead, and
`test_platform_specific_commands_live_in_tabs` accepts that form for `README.md`
so the rule still holds where tabs cannot.

The `.githooks/pre-commit` hook in the template also prints both forms now. A
credential-blocking hook whose remedy only works on one platform sends half the
students who trip it looking for a second problem.

---

## ADR-010: Let Week 2 run over the reading cap, and say so on the page

**Status:** Accepted

### Context

`test_weekly_reading_load_stays_reasonable` caps a session at 120 minutes of
close reading and 200 minutes in total. Those numbers are the course's workload
promise made concrete, and ADR-006 treated them as the constraint that keeps the
promise honest.

Week 2 is the foundations week. Everything after it — attention in Week 3, the
whole of the transformer, retrieval in Week 10 — assumes a student knows what a
vector of numbers is doing in place of a word. Two additions were wanted:
Burchell's *Real Python* #119, the classical NLP pipeline recorded before any of
this was called an LLM, and Hugging Face's visual embeddings primer, which
covers contextual embeddings inside a running model. Alammar does not cover
that, because it did not exist when he wrote.

With both, Week 2 comes to 241 minutes. The obvious fixes were considered and
declined: moving Burchell #121 to Week 3, or demoting it to optional. The
instructor's judgement is that the week is worth the weight.

### Decision

Week 2 Tuesday runs at 241 minutes, recorded as an explicit exception rather
than by relaxing the cap.

`HEAVY_SESSIONS` in the test file maps a session slug to the exact ceiling it
may not exceed. Exact, because the point is not to create room — it is to make
the next addition to that week a decision someone has to take again.

Three things hold the exception honest:

- The **close-reading cap is not exceptioned and never will be.** Week 2 sits at
  105 of 120 minutes there. All 41 minutes of overrun are listening. ADR-006's
  own reasoning is the justification: an hour of paper is an hour at a desk, an
  hour of podcast is a walk across campus, which is why the two cap separately.
- `test_heavy_sessions_are_actually_heavy` fails if the week slims back under
  200, so the exception cannot outlive the reason for it.
- `test_overloaded_sessions_warn_students` fails unless the session page says it
  is a heavy week. A promise made to students cannot be excepted only in a test
  file they never open, so Week 2's summary now says it is the heaviest week of
  the term, why, that most of it is listening, and to start on the weekend.

### Alternatives considered

**Raise the global cap to 245.** Rejected outright. It converts one deliberate
week into a permanent licence for every week, and quietly retires the promise
instead of making an exception to it.

**Move Burchell #121 to Week 3.** Genuinely attractive: #121 is titled *Moving
NLP Forward With Transformer Models and Attention*, which is Week 3's topic
almost word for word, and it would have brought Week 2 to 191 with Week 3 at
171. Rejected because #119 and #121 were recorded two weeks apart in the last
summer before ChatGPT, and hearing them back to back is the point — the pair is
the evidence, not either one alone.

**Demote #121 to optional.** Same arithmetic, and it shrinks the Burchell arc
from six required episodes to five, weakening the Week 15 reflection that asks
students to trace the whole thing.

**Add the primer as optional.** Rejected: contextual embeddings are the part of
Week 2 with no other source on the list, and optional readings are not read.

### Consequences

Week 2 is 241 minutes against a term norm of about 140, and it lands in the
second week, when students are least practised at pacing themselves. The
mitigation is that they are told, on the page, before it starts. If the week
proves too much in practice, the honest response is to move #121 to Week 3 as
above — the option is costed and still there.

The exception mechanism is now available and will be attractive. It should stay
rare: every entry in `HEAVY_SESSIONS` is a week where the course asked for more
than it promised, and the count of them is a fair measure of how well the
promise is being kept.

### A correction that came with it

Adding #119 required renumbering the arc, which surfaced that episodes 188 and
232 were numbered in the wrong order — 232 was labelled episode 2 and 188
episode 3, though 188 aired in January 2024 and 232 the following December. The
arc is now in the order it happened.

The table on the Readings page is generated from `resources.yml` rather than
written, after three of six episode titles were typed in from memory and three
of those were wrong. That is the repository's one rule working exactly as
intended: the data was right and the memory was not.

---

## ADR-011: Make the required ADRs data, so the session pages announce them

**Status:** Accepted

### Context

The project is graded on four decision records due at checkpoints. Which four,
and when, was written down three times: a table in the ADR guide, a milestone
table on the assignments page, and — for some of them — the `due` field of the
session they fall on.

Two of the three did not agree. **ADR-001 and ADR-003 were in both Markdown
tables and in neither session's `due` field.** The consequence is invisible
until it is expensive: `due` is what renders the red *Due today* banner on the
session page and the flag on the schedule, so a student who worked from the
schedule — which is how the site is designed to be used, and what every session
guide link now points them at — saw two of their four graded ADRs announced
nowhere at all.

ADR-001 was worse than an omission. The Week 1 lab said "**ADR-001 is due**" in
its activity prose, in bold, which reads as handled and is not. That is exactly
the failure ADR-005 named for the AI policy: a fact stated only in prose does
not render as a banner, and a deadline a student cannot see is not one you can
hold them to.

### Decision

The four required ADRs move into `data/assignments.yml` as a `RequiredADR` list
on the project assignment: id, the meeting they are due at as (week, day), and
the decision each one records. No dates, per ADR-002 — `calendar.py` supplies
those.

Everything that shows them now derives from that list. The guide's table and the
milestone table are macros. The session `due` fields were corrected, and the
loader refuses to build if a required ADR's session does not name it, so the
banner and the tables cannot drift apart again.

The milestone table is derived from the sessions' own `due` fields rather than
from a separate list, which makes that table and the *Due today* banner the same
fact rendered in two places instead of two facts that agree by luck.

### Alternatives considered

**Add the two missing `due:` lines and stop.** What was asked for, and it fixes
today's bug in two lines. Rejected as the whole answer because the bug was not
the two lines — it was that the same fact lived in three hand-maintained places
with nothing checking them against each other. That arrangement produced this
error and would produce the next one.

**Keep the tables written by hand and add only the test.** Rejected: a test that
compares two hand-written tables tells you they disagree without saying which is
right. Deriving both from one list means there is nothing to disagree.

**Put the ADR list in its own `data/adrs.yml`.** Rejected as a fifth data file
for four rows of something that belongs to one assignment. It hangs off the
project, which is what it is graded as part of.

### Consequences

Adding a fifth required ADR is now one entry in `assignments.yml` plus the `due`
text on its session, and the build tells you if you forget the second half. The
guide's table, the milestone table, the session banner, and the schedule flag
all follow.

The date shown for each ADR is now derived, so moving a session moves its
deadline everywhere — including on the guide page, which previously carried
hand-typed dates that a schedule change would have silently falsified.

`due` strings are prose and stay prose: they are what the banner says, and
"HackAPrompt midterm write-up, and ADR-003 (how your system handles failure)"
reads better on the day than any structure would. The loader only checks that
the ADR's id appears in it.

---

## ADR-012: Tab every shell command, including the identical ones

**Status:** Accepted. Amends [ADR-009](#adr-009-give-every-shell-command-a-powershell-half)

### Context

ADR-009 gave every *divergent* command a PowerShell half and deliberately left
identical ones — `git clone`, `git config`, `claude` — as plain single blocks.
The reasoning was that wrapping an identical command in two tabs implies a
difference that is not there, and teaches students to stop reading the labels.

Reviewing the site afterwards, the instructor found the result inconsistent: a
page moves between tabbed and untabbed blocks with no visible rule, and five
shell blocks — three in the setup guide, two in the Week 1 lab — had no Windows
half at all.

The argument in ADR-009 assumed a reader who notices that an untabbed block is
untabbed and infers "this must be the same everywhere." That is a reasonable
inference and the wrong one to require. This course assumes a student who has
never opened a terminal. Presented with a plain `bash`-labelled block after two
tabbed ones, the available readings are "this works everywhere", "this is the
Mac one and mine is missing", and "I scrolled past a tab". Only one is right,
and nothing on the page distinguishes them — least of all the word `bash` in the
corner, which to a Windows student names a shell they do not have.

The cost of the alternative is small and lands in the right place. A duplicated
tab costs a reader one glance. A missing one costs them the evening.

### Decision

Every shell code block on the site sits in a tab set with both halves, whether
or not the two are identical. The setup guide states this outright — *both tabs
are always there, including where the two are character-for-character the same*
— so an identical pair reads as the convention rather than as an error.

Non-shell blocks are untouched: Python, the ADR template, sample output and the
text you type at Claude Code's own prompt have no PowerShell half, and inventing
one would be the noise ADR-009 was worried about.

`test_every_shell_command_is_given_for_both_platforms` now applies to every
shell block rather than only the divergent ones.

### Alternatives considered

**Keep ADR-009 and add a note explaining the untabbed blocks.** Rejected: it
asks the reader to learn a rule in order to read a page, which is more work than
the duplication it saves.

**Mark identical blocks with a third tab label such as "Any platform".** A
genuine option, and rejected because it adds a third thing to understand and
breaks tab linking — a reader who has chosen Windows would still land on a tab
set where their choice does not appear.

### Consequences

The rule is now blanket, which makes it checkable without judgement: any shell
block outside a tab set fails, with no divergence heuristic deciding whether it
should have been exempt. That is a better test than the one it replaces, because
it has no false negatives to reason about.

Duplication introduces a failure the old rule could not have: two halves that
drift, or a bash command pasted under the Windows tab. `test_each_tab_holds_the_right_platform`
covers it, rejecting Unix-only syntax under a Windows tab, PowerShell-only
syntax under a Unix tab, and a block whose language tag disagrees with its tab.

Pages get longer again. The setup guide and the Week 1 lab each gain several tab
sets whose halves say the same thing. That is the accepted cost, and it is paid
by the reader who already knows what they are doing.

---

## ADR-013: Authenticate GitHub with `gh`, and install the tools before using them

**Status:** Accepted

### Context

The Week 1 setup guide had students run `git clone`, `git config`, and later
`git push`, and never installed Git. The only mention of installing it was a row
in the troubleshooting table — which is where a student looks *after* something
has already failed, having first concluded the problem is them.

Two further prerequisites were missing from the same chain. Git refuses to
commit without a `user.name` and `user.email`, and the lab ends by having
students commit and push ADR-001. And GitHub removed password authentication for
Git operations in August 2021, so a student who got that far would meet
`Support for password authentication was removed` at the last step of their
first lab.

Each of these is invisible to anyone who set their machine up years ago, which
is everyone who writes course material.

### Decision

The Week 1 guide and the Week 1 lab now install Git, set the Git identity, and
install and sign into the GitHub CLI, in that order, before anything is cloned.
Each step is executable on a machine with nothing on it.

**Push authentication is handled by `gh auth login`.** It opens a browser, takes
a one-time code, and — when answered *yes* to authenticating Git — writes a
credential helper that makes `git push` work silently from then on.

### Alternatives considered

**A personal access token.** The path GitHub's own documentation leads with, and
rejected for a first lab: it means a settings page with a dozen scope
checkboxes, a decision about expiry, and a secret the student must paste
somewhere and then keep. Handing a beginner a long-lived credential in week one
also cuts against a course that spends the term telling them not to paste keys
into things.

**SSH keys.** Better long-term hygiene and the wrong week for it. `ssh-keygen`,
an agent, a passphrase decision, and a public key pasted into a settings page
is more new concepts than the rest of the lab combined, all before the student
has done anything.

**GitHub Desktop.** Genuinely easier, and rejected because the course is about
working in a terminal alongside a model that reads your files. A GUI that hides
what a commit is would work against Week 1's actual subject.

**Say nothing and let students hit the error.** This was the status quo, not a
choice anyone made. Worth naming: the error is legible to someone who knows what
it means and opaque to everyone else, and "it didn't work" is what arrives at
office hours.

### Consequences

Week 1 Thursday grows from seven steps to nine, in a session that was already
the densest of the term. The ordering is the mitigation — every step now
succeeds if the one above it did, so the failure modes are sequential and
diagnosable rather than mysterious.

`test_labs_do_not_use_a_tool_the_guide_never_installs` checks the class of bug
rather than this instance: every command a lab tells students to run, other than
those the OS provides, must be named in an *Install* heading in the setup guide.
It matches whole words, because `git` is a substring of `github` and a looser
check let an uninstalled Git ride along on the GitHub CLI's heading — the first
version of this test passed while the bug was still present.

That is also why the CLI's heading now names the command: **Install the GitHub
CLI — `gh` — and sign in**, with an explicit `{ #anchor }` so the wording can
change again without breaking the links into it.

The troubleshooting table gained the errors this chain actually produces —
`Please tell me who you are`, `Authentication failed`, `Permission denied` on
push — each pointing at the section that prevents it rather than describing a
fix in place.
