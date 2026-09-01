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

**Status:** Accepted, amended by [ADR-014](#adr-014-make-the-project-copy-with-a-command-not-a-button)
— the copy is made with `gh repo create`, not the web button

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

---

## ADR-014: Make the project copy with a command, not a button

**Status:** Accepted. Amends [ADR-007](#adr-007-put-students-in-version-control-on-day-two-not-at-the-project)

### Context

Since ADR-007, the Week 1 lab told students to "press the green **Use this
template** button." The instructor, reading the page, could not find a green
button.

The repository is a template — `is_template` is true, and GitHub does show the
control — but the instruction was poor regardless. It describes a button by its
colour and its position in a web UI that is restyled without notice, in a course
whose readers include people who have never used GitHub and cannot tell "I am
looking at the wrong page" from "the button moved." Colour is also the one
attribute of a control that some readers cannot perceive at all.

ADR-013 had just put the GitHub CLI in the lab, for the unrelated reason that
`gh auth login` handles push credentials. That made a better answer available
than the one already written down.

### Decision

The copy is made with one command:

```
gh repo create llms-project --template Nalaquq/llms-and-you-project --public --clone
```

It creates the repository on the student's own account from the template and
clones it, replacing two steps with one. The lab's step count drops back from
nine to eight even though ADR-013 added two.

The web route survives as a collapsed fallback, pointing at the `/generate` URL
— the form itself — rather than at a button to hunt for. It still mentions the
button's name, for a reader who would rather find it that way, but the
instruction no longer depends on locating it.

### Why not simply `git clone` the template

Asked directly, and worth writing down because it is the obvious thing to try.
A plain clone gives a working copy whose `origin` is the instructor's
repository, which students have no write access to. Everything works until the
end of the first lab, when `git push` fails — the worst possible place for this
to surface, after an hour of successful steps.

Recovering means creating a repository on GitHub and re-pointing the remote:
remotes, remote URLs, and pushing to an empty repository, all introduced at the
moment the student is stuck. `--template` avoids the situation rather than
teaching a way out of it, and gives a clean history starting at their own first
commit. A fork was rejected for a different reason: it stays tied to the
instructor's repository and is displayed by GitHub as derived from it.

### Alternatives considered

**Keep the button and describe it better** — by position, or with a screenshot.
Rejected. A screenshot is stale the next time GitHub ships a redesign, and a
description by position is what just failed.

**Link the `/generate` URL as the primary route.** This is what the fallback
does, and it is a genuine improvement on the button. Rejected as the primary
because the course is about working in a terminal, the CLI is already installed
two steps earlier, and one command that both creates and clones is less to get
wrong than a form plus a clone.

### Consequences

The lab now depends on `gh` being installed and signed in, which is step 3. If
that step failed, step 4 fails immediately and visibly rather than an hour
later, which is the right order for a failure to happen in.

Every other page that described the button — the assignments page, the guides
index, the resource note, and the template repository's own README — now names
the command instead. No page on the site refers to a control by its colour.

Nothing about the button being *correct* has changed. It exists, it works, and a
student who finds it will get the same repository. It is simply no longer what
the instructions depend on.

---

## ADR-015: Order Week 2's readings general to specific

**Status:** Accepted

### Context

Week 2 grew to seven items (ADR-010) and was ordered by accident of arrival:
the one-minute video, Alammar's *Illustrated Word2Vec*, the Hugging Face
embeddings primer, seq2seq, the transformer video, then both Burchell episodes
at the end because podcasts had been added last.

Read in that order, a student meets **word2vec before they are told what an
embedding is.** Word2Vec is one specific 2013 technique for producing one fixed
vector per word. Meeting it first invites the reasonable and wrong conclusion
that this is what embeddings *are* — which then has to be unpicked in Week 3,
when the same student meets a model that produces a different vector for the
same word in every sentence.

The reading list also had all the listening bunched at the end, so a student
pacing themselves across the week did all the reading first and all the walking
last, which is the wrong shape for the heaviest week of the term.

### Decision

The list runs general to specific, in three movements:

1. **What an embedding is.** The one-minute video, then the Hugging Face
   primer, then Burchell #119 — the classical NLP pipeline, which is the
   problem embeddings were invented to solve.
2. **One specific way of building them.** Alammar's *Illustrated Word2Vec*, now
   met as a worked example of a thing already named rather than as the
   definition.
3. **What replaced it.** Seq2seq with attention, the transformer video, and
   Burchell #121.

The session page says so — *take them in the order they are listed* — with the
reason, because a list of seven items with no stated order gets read shortest
first.

The two `assign_note`s that changed meaning were rewritten: the primer now says
it is the map and that word2vec is coming again slowly, and Alammar's says the
primer sketched this and here it is at walking pace. Without that, the overlap
reads as a duplicate and the second one gets skipped.

### Alternatives considered

**Order by length, shortest first,** to build momentum in a 241-minute week.
Rejected: it is the order a student will use anyway if we do not give them one,
and it puts the 27-minute transformer video before the 40-minute primer, which
is the same inversion in a different disguise.

**Interleave listening and reading** so each sitting has one of each. Attractive
for pacing and rejected because it cuts across the argument — the two Burchell
episodes are four years and one architecture apart, and playing them either side
of word2vec would suggest they belong together.

**Leave the order alone and explain the relationship in prose.** Rejected. The
list is what students act on; a paragraph explaining that item 2 is a special
case of item 3 is work the ordering can do for free.

### Consequences

Nothing about the workload changed — the same seven items, 105 minutes of close
reading and 241 in total, still under the exception recorded in ADR-010.

`test_foundations_week_runs_general_to_specific` pins the relationships rather
than the list: primer before word2vec, word2vec before what replaced it, the
Burchell episodes in recording order, and the one-minute video first. A reorder
that breaks the argument fails; adding an eighth reading in a sensible place
does not. The pin exists because reading order is invisible in a YAML list and
is precisely the sort of thing a later edit disturbs without noticing.

This makes reading order a thing the course has an opinion about, which is new.
Other weeks are not ordered this deliberately, and most do not need to be — Week
2 is unusual in assigning both a general account and a specific instance of the
same idea.

---

## ADR-016: Put the BoodleBox guide on every session that assigns reading

**Status:** Accepted

### Context

The college pays for BoodleBox, which puts most of the frontier models behind
one login. Before this, the site mentioned it twice: one link in the syllabus
alongside Co-Pilot, and a row in the tools table. Both are pages students read
once, in August, before they have a reading they cannot get through.

The result is predictable. Students who would benefit most from asking a model
to explain a paragraph are the ones least sure they are allowed to, in a course
that spends real time on the two ways to fail its AI policy. Ambiguity here does
not produce reckless use; it produces students quietly not using a subscription
the college has already paid for, and not saying so.

There is a genuine tension underneath. Reading responses and the Burchell
reflections are the one part of this course where GenAI is prohibited, and they
are attached to exactly the readings a student would want help with. Encouraging
model use on the reading and prohibiting it on the response are compatible
positions, but only if the boundary is stated everywhere the encouragement is.

### Decision

A guide, [Using BoodleBox to understand a
reading](../guides/boodlebox.md), linked from **every session that assigns
reading** — thirteen of them — through the `guides` mechanism from ADR-008. It
appears in the same box as *How to read a paper*, on the page a student opens
when they are stuck, rather than only where they would have to go looking.

The guide leads with the boundary rather than burying it: reading responses and
reflections are no-AI work, phrased as the syllabus already phrases it —
*asking a model to explain a passage you did not follow is fine; asking it to
write your response is not.* It carries the account-request route and Todd Pugh
as the contact, since the Computing Center administers this and the instructor
cannot fix an account.

Most of the guide is about asking a question worth answering and then checking
the reply against the reading. That last step is deliberately framed as the
skill rather than as a caution: a student who catches a hallucination in
material they half-understand has met the Week 7 subject four weeks early, on
their own terms.

### Alternatives considered

**A paragraph in the syllabus and nothing else.** What existed. It fails at the
moment of need, which is a Sunday evening in Week 6, not August.

**A line in each session's `activity` prose.** Rejected. Thirteen copies of the
same sentence, drifting apart, in a repository whose entire design is aimed at
not doing that — and prose does not render as anything a student's eye catches.

**Link it from every session, including labs.** Rejected: labs assign no
reading, so the guide has nothing to be about there, and a link that appears
everywhere stops carrying information.

**Name specific models to use for specific readings.** Rejected as advice with a
shelf life measured in months, in a guide meant to last the term.

### Consequences

Two tests hold it. `test_reading_sessions_offer_help_understanding_the_reading`
requires the link on any session with readings, so a new seminar cannot be added
without it. `test_the_boodlebox_guide_states_the_no_ai_boundary` requires the
guide to link the policy and name the prohibited work — a student arriving from
a session page may never open the syllabus, so the guide cannot rely on it
having been read.

A third test came out of building this: the guide was written, linked, and
building cleanly under `--strict` while missing from the site navigation, which
mkdocs reports only at INFO. `test_every_guide_appears_in_the_site_navigation`
now catches that for every guide.

The risk is that promoting a tool this prominently reads as encouragement to use
it on everything, which is the opposite of the policy. The mitigation is that
the boundary table is in the guide itself rather than one link away, and that
the guide's longest section is about not trusting what it tells you.

**Left undone:** the account request form's URL. The Computing Center provides
one and it is not recorded here, so the guide describes the route and names Todd
Pugh instead of linking it. That should be a link, and inventing a plausible URL
would have been worse than omitting it.

---

## ADR-017: Make course concepts data, and give them a page of their own

**Status:** Accepted

### Context

Week 1's group discussion spent most of its length on Don Norman's affordances
and constraints. It was the most useful thing that happened that day, and by the
end of it the concept existed nowhere on this site. The session's `topic` was
about attention and the paper the course is named after; its `activity` was
about the AI policy. Neither is wrong, and neither is where a student in Week 9
would look for the vocabulary they are supposed to be writing their ADRs in.

That is the general problem, not a one-off. The schedule records what a session
*was about*. It does not record what a student is *responsible for*, and those
are different lists. A topic is a heading; a concept is something a student can
be asked to define, apply, and be wrong about. The course assesses the second
list — the ADR log and the lab write-ups are graded on applying ideas — while
publishing only the first.

The gap has a predictable shape. Students revise from the reading list, which is
sixty-odd items of which most is context. They cannot tell the load-bearing
ideas from the background, so they either over-prepare on the wrong things or
ask, reasonably, what is actually going to be assessed.

### Decision

A fifth kind of course data: `data/concepts.yml`, and a [study
guide](../study-guide.md) generated from it.

A concept declares what it is (`definition`, `in_practice`), what a student must
be able to *do* with it (`mastery`), the mistake people actually make
(`pitfall`), where it was introduced (`week`/`day`), what it is reviewed with
(`resources`, by id), and — required — which graded components assess it
(`assessed_in`). The loader resolves the session, the theme, the resource ids
and the assignment ids; none of them can be a hopeful string.

Two fields are required that could reasonably have been optional. `mastery` is
required because a study guide that lists topics tells a student what to worry
about and not what to practise; if an idea cannot be written as something a
student does, it is a session summary and belongs there. `assessed_in` is
required because the page opens by promising that everything on it is
assessable, and that promise is worth more as a schema constraint than as a
sentence.

The session page that introduced a concept links to its entry, in the same
position as the guides box. This is the ADR-008 rule applied again: students
arrive through the schedule, so a page nothing points at is a page found in
December.

Concepts are filed by theme, which is deliberately allowed to disagree with the
theme of the session that taught them. Affordances arrived in a foundations
session about what an LLM is; it is a methodology idea, because it is the
vocabulary an ADR is written in. Filing it under foundations to match the
calendar would put it where nobody revising design decisions will look.

### Alternatives considered

**Put the concept in the session's `summary` or `activity`.** The cheapest
option, and it fails at the only moment that matters. Revision happens weeks
later, across sessions; nobody reopens eleven session pages to reconstruct a
list. It also buries the assessment claim in prose, where it renders as nothing
in particular.

**A glossary page written by hand.** Rejected for the reason ADR-001 rejects
hand-written session pages. A glossary duplicates titles, dates, and links that
already exist in `data/`, and the copy in the glossary is the one that goes
stale — and this copy would go stale while claiming to tell students what they
are graded on, which is worse than the usual case.

**Attach concepts to themes rather than sessions.** Tidier, and it loses the
thing students most need: when we did this, and therefore which reading it came
with and which notes to look at. The theme is kept as the filing dimension and
the session as the origin, because both questions get asked.

**Make `assessed_in` optional so anything interesting can go on the page.**
Rejected. A study guide is only useful in proportion to what it leaves out. An
idea worth mentioning but not assessing is a session's `optional` reading, which
already exists and already renders.

**Add the Norman material to Week 1's `optional` list instead.** It would put
the readings on the session page, which is something. But optional readings are
prep for one meeting, and the point of these is that they are review material a
student comes back to in November when writing an ADR about a prompt's
constraints. The study guide is where "come back to this" lives.

### Consequences

Adding a concept is a YAML entry; the study guide, its at-a-glance table, and
the link on the originating session page all follow. Six tests hold the promises
the page makes — that every concept names a real meeting and a real graded
component, that every one states something a student can do, that every one has
something to review, that the review material is free, and that the anchor a
session links to is the stable id rather than a heading slug.

The cost is a real one: the page is only as good as what gets written into it,
and it is the instructor who has to notice, that evening, that a discussion
produced a concept. Nothing in the build can detect a Week 6 idea that was never
written down. What the build can do is refuse to let a written-down one be
vague, unassessed, or unreachable, which is where the tests are aimed.

**Left undone:** the study guide launches with one concept. Week 1's discussion
of hallucinations and slop is a genuine second candidate and was left out
because the syllabus already defines both terms, and restating a definition the
site already carries is the failure mode this whole repository is built to
avoid. If those become concepts, the entry should link
[the policy](../syllabus.md#on-hallucinations-and-slop) rather than repeat it.

---

## ADR-018: Break the study guide down to the vocabulary, and record what each concept needs first

**Status:** Accepted

### Context

Week 2 is the heaviest preparation week of the term by design (ADR-010), and it
is the week the course front-loads because everything after it assumes
embeddings are understood. Reviewing its seven readings against the study guide
turned up something the page could not currently express.

The readings assume a working vocabulary the class does not have. Alammar writes
"one hidden layer" without explaining a layer. The embedding primer computes
TF-IDF without ever saying what a corpus is. Burchell's episode 119 covers
bag-of-words, stemming, lemmatization, n-grams, count vectorization and stop
words in twenty minutes, at speed, as background. This is a 200-level course
whose students arrive with no machine learning, no NLP and no LLM background at
all, and for them roughly a third of the assigned prose is terms used as though
already known.

The first draft of the Week 2 entries handled this by grouping. One entry for
"bag of words" absorbed count vectorization, stop words, stemming, lemmatization
and n-grams, on the reasoning that they are one technique and its parts. That
reasoning is sound for a reader who already knows four of the five. For this
class it puts five unfamiliar terms in one paragraph, gives the student one
place to say "I do not understand this", and offers no way to find out *which*
of the five they do not understand.

There is a second gap the schema had regardless of granularity. Concepts have
depended on each other since the page existed — cosine similarity needs the dot
product, which needs a vector — and the data recorded none of it. `related`
exists but is an undirected "see also"; it cannot say which of two entries has
to be read first. A student on the study guide in November, bouncing off an
entry, has no way to discover that the thing they are actually missing is three
entries up.

### Decision

Two changes, made together because neither is much use alone.

**Split to the level of the individual term.** The rule is: if a student can get
it wrong on its own, it is its own entry. Count vectorization can be got wrong
on its own. Stemming can be got wrong on its own, and differently from
lemmatization. Both pass, so both are entries. This takes Week 2 from a proposed
thirteen entries to forty-six, including eight that are not this week's topic
at all — corpus, vocabulary, vector, dimensionality, neural networks and layers,
parameters and weights, training and inference, softmax — and exist because the
readings use them without introduction.

**Add `builds_on` to the concept schema**: an ordered list of concept ids this
entry cannot be understood without. It is a directed prerequisite edge, and it
is deliberately not the same field as `related`. The loader refuses a
prerequisite that does not exist, refuses a self-reference, refuses an id listed
as both a prerequisite and a cross-reference, refuses a prerequisite introduced
at a *later* meeting than the concept needing it, and refuses a cycle. The last
one matters more than it sounds: two ideas taught in the same session can each
plausibly look like the other's foundation, so a cycle is reachable by accident
rather than by carelessness, and a cycle is a page that cannot be read in any
order.

The page renders the graph in three places. Each entry opens with **Understand
first**, above the definition, because a student without the prerequisites is
reading the wrong entry and the cheapest moment to say so is before they have
read a paragraph that will not land. Each entry closes with **Needed for**,
which is derived from what later entries declare rather than typed — nobody
remembers to go back and update a downward link in November. And the
at-a-glance table is now grouped by session with a prerequisite column, so the
order to learn things in is legible without reading a single definition.

### Alternatives considered

**Keep the technique-level grouping and write longer entries.** The original
plan, and the right one for a class with some background. Rejected on the
specific audience: a paragraph containing five undefined terms fails silently,
because the student cannot report which term lost them. Thirty-nine entries with
one idea each fail loudly, which is the point of a study guide that students
self-check against.

**Split, but leave the relationships in prose.** Cheapest option, and it was the
status quo. Rejected because it does not survive: prose cross-references rot,
they cannot be validated, and the failure mode is a study guide that sends a
student to an entry that has been renamed. The build already refuses a broken
resource id and a broken guide anchor; a broken prerequisite is the same class
of error and deserves the same treatment.

**Use `related` for prerequisites rather than adding a field.** Rejected because
the direction is the whole value. "See also" and "you cannot read this yet" are
different messages, and collapsing them produces a page where every entry links
to every neighbouring entry and none of it tells you where to start.

**A glossary page, separate from the study guide.** Tempting, because eight of
these entries really are vocabulary rather than course concepts. Rejected for
the reason ADR-017 rejected a hand-written glossary, and for a second one: it
would split the page's promise. The study guide says everything on it is
assessable. Terms exiled to a glossary would read as optional, and a student who
cannot define a vector cannot answer a question about cosine similarity.

**Render the prerequisite graph as a diagram.** A Mermaid dependency graph was
considered and dropped. Forty nodes is unreadable as a picture, it requires a
Markdown extension the site does not currently enable, and the thing a student
actually needs — "what do I read before this one" — is answered better by a line
of text on the entry itself than by a diagram they have to trace.

### Consequences

Week 2 has forty-six study-guide entries and the course has forty-seven. That
is a large page, and it is the correct size for the week the course front-loads
into a class with no background. The at-a-glance table absorbs the volume by
being grouped and scannable; the prerequisite column means a student can find
their own entry point rather than reading from the top.

The promise on the page needs reading with this in mind. "If it is on this page,
you can be assessed on it" remains true and remains enforced, but at this
granularity most entries are assessed cumulatively — through reading responses
and lab write-ups that use the vocabulary — rather than each being separately
examinable. `assessed_in` is honest about this: the machinery entries name
`responses`, not `midterm`.

The real cost is on later weeks. Week 2 is now decomposed to a level Weeks 3
through 15 are not, and an inconsistent study guide is worse than a uniformly
coarse one. The commitment made here is to bring the remaining weeks to this
granularity as they are taught, not to leave Week 2 as an unmatched island.
Week 3 is the immediate test: attention, self-attention, queries, keys and
values are exactly this kind of vocabulary, and this ADR is the reason they get
five entries rather than one.

`test_the_heaviest_week_is_broken_down_far_enough` names sixteen of the Week 2
sub-concepts explicitly. It is a deliberately unusual test — it asserts a
pedagogical decision rather than a structural one — and it exists so that a
future tidying pass that folds "stemming" back into "bag of words" has to argue
with this ADR rather than quietly reverse it.

---

## ADR-019: Host the lecture decks, and publish how they were made

**Status:** Accepted

### Context

The Week 2 lecture deck is twenty-seven animated slides generated entirely by
Python scripts, which were themselves written by Claude Code from four
instructor prompts. Two questions followed. Where do the decks live, so
students can get them after class? And what happens to the making-of story —
the prompt sequence — which in a prompt-engineering course is arguably more
instructive than the deck itself?

The second question cuts against an earlier default. `prompts/` is gitignored
with a note calling AI working notes "drafting artifacts, not course content."
That remains true of drafting notes in general. But this particular process is
a finished worked example of the course's central skill: a brief with real
constraints, two targeted revisions, and a structural disagreement with the
model that the instructor won. Hiding it would be teaching the course while
declining to show the course's own homework.

There is also a hosting question with a wrong answer available. The deck is
~11 MB and the GIFs ~8 MB, regenerated every time a slide is touched.
Committing them writes twenty megabytes into git history per iteration,
forever, for files that are pure build products.

### Decision

A top-level **Slides** page (`docs/slides/index.md`), holding each deck as it
is taught: the PPTX for download, and the full GIF sequence embedded in
teaching order, lazy-loaded so the page stays light.

The media is **generated at build time, never committed** — the same rule the
session pages established in ADR-001. `src/course_site/gen_slides.py` copies
the generator outputs into the site during `mkdocs build` and fails loud, with
the command to run, if they are missing. CI gained a "generate lecture media"
step and a `[slides]` dependency group. The scripts in `scripts/` are the
committed source of truth.

Teaching order lives once, in `scripts/deck_order.py`, read by both the PPTX
builder and the site's gallery macro — so the file students download and the
page they scroll cannot disagree. The same file is where the order's
*reasoning* is recorded (chronological, so counting fails before learned
embeddings appear — itself the product of the instructor's prompt 4).

The making-of is published on the Slides page itself, quoting the four real
prompts and stating the AI attribution in exactly the form the syllabus asks
of students.

### Alternatives considered

**Commit the media.** Simplest, and wrong twice: git history grows by the full
media size on every regeneration, and it breaks the repo's one rule that
generated things are not source. ADR-001 already settled this for session
pages; slides are the same case with bigger files.

**A guide (`docs/guides/making-slides-with-ai.md`).** Guides are procedures a
student follows, wired to sessions by the reachability test. This page is
primarily *hosting* with a narrative attached; filing it under guides would
bury the decks students come looking for on Thursday night. The narrative
still teaches, but it teaches from where the decks are.

**Git LFS.** Solves history bloat, adds a toolchain requirement for every
student who clones the template-adjacent repo, and still commits build
products. Rejected as complexity in the wrong place.

**Keep the making-of private, host only the decks.** The default the
`prompts/` rule would suggest. Rejected for this artifact specifically: the
course grades students on documenting their prompting decisions, and the
instructor publishing his own is the cheapest credibility the course will ever
buy. The `prompts/` default stays for genuine drafts.

### Consequences

Deploys now run matplotlib and take about a minute longer. Local
`mkdocs build` fails unless the generators have run once — loudly, with
instructions, which is the intended behaviour rather than a bug. The Slides
page must be updated as decks are added, and the making-of convention is now a
promise: future decks should arrive with their prompts, or say why not.

The subtler consequence is the precedent: course artifacts generated with AI
are published *with their provenance*, in the citation form the syllabus
demands of students. The course now models its own policy.
