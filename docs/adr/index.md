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
