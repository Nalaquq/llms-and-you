# Syllabus

**LLMs & You: Attention is All You Need**
Hampden-Sydney College · {{ semester.term }}

---

## Course information

| | |
|:---|:---|
| **Meets** | Tuesday & Thursday, 2:00–3:30 PM |
| **Location** | PRC 106 |
| **First meeting** | {{ first_meeting.long_date }} |
| **Last meeting** | {{ last_meeting.long_date }} |
| **Sessions** | {{ session_count }} across 15 weeks |
| **Prerequisites** | None |

## Instructor

**Sean Gleason**
:material-email-outline: [sgleason@hsc.edu](mailto:sgleason@hsc.edu)
:material-map-marker-outline: Pannill 100E

**Office hours:** Tuesday & Thursday 12:00–2:00 · Wednesday 9:00–12:00 · and by
appointment. Email is the fastest way to reach me, and asking for an appointment
outside these hours is normal, not an imposition.

---

## Course description

Large language models are reshaping how we write, research, and solve problems.
This course introduces the principles and practice of prompt engineering: the
craft of communicating effectively with AI systems to produce reliable,
high-quality outputs.

Using **Python (no experience required)**, **VS Code**, and **Anthropic's
Claude**, we begin by building a theoretical foundation in neural networks,
transformer architectures, and natural language processing. From there we
develop techniques for crafting prompts that account for hallucination, bias,
and context constraints; learn to evaluate model outputs against evidence you
construct yourself; and apply structured prompting strategies including
chain-of-thought reasoning, retrieval-augmented generation, agents and tool use,
and system-level prompt design.

Particular attention is given to **what changes when a system has to run for
other people** — API integration, token accounting, cost management, and
responsible use in production. Throughout the semester you will apply these
skills in an individual project, building a proof-of-concept application that
demonstrates both technical proficiency and ethical awareness.

Two things distinguish this course from a tutorial. You will read the
literature, **including the parts that contradict each other** — chain-of-thought
prompting alongside the paper arguing it is an illusion; a hallucination
benchmark alongside the critique saying it measures the wrong thing. And you
will **document your decisions as you make them**, in a log that is graded as a
primary artifact.

The course is named after Vaswani et al.'s 2017 paper. We read it in Week 3.

!!! info "No prerequisites — and that is not a formality"

    No programming, no statistics, no linear algebra. We install the tools
    together in class — Claude Code and the desktop app in week one, Python the
    week after — and nobody leaves those rooms without a working setup. Where a
    paper contains mathematics you have not seen, you are told which sections
    to skip.

## Learning objectives

By the end of the term you should be able to:

1. **Explain** what a transformer-based language model does when it generates
   text, in terms a non-specialist can follow — tokens, embeddings, attention,
   and the limits each imposes.
2. **Apply** named prompting techniques deliberately, and justify why you chose
   one over the alternatives rather than defending what happened to work.
3. **Evaluate** a prompted system against evidence you constructed, and state
   honestly what your evaluation does and does not measure.
4. **Assess** claims made about these systems — in papers, in marketing, and in
   journalism — including claims made in this course.
5. **Document** design decisions as you make them, in a form another person
   could audit.

---

## Required texts

**There are none to buy. Every reading in this course is free.**

- **[Prompt Engineering](https://www.gptaiflow.com/assets/files/2025-01-18-pdf-1-TechAI-Goolge-whitepaper_Prompt%20Engineering_v4-af36dcc7a49bb7269a58b1c9b89a8ae1.pdf)** — Lee Boonstra (Google, 2025). 68pp, assigned in sections. The applied text.
- **[Auditing AI](https://mitpress.mit.edu/9780262051729/auditing-ai/)** — The Marquand House Collective (MIT Press, 2026). Open access.
- **[Neural Networks](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi)** — 3Blue1Brown. The foundations spine, chapters 1–3.

Everything else is a linked paper, podcast, or article. This site links out and
hosts nothing.

!!! success "Zero-cost reading list"

    A required text you cannot afford is a barrier disguised as a syllabus. So
    there is no book to buy, no course pack, and no reading behind a paywall or
    a library login — a test in this site's repository fails the build if a
    gated reading is ever added.

    If you hit anything you cannot open, tell me. That is a bug, not your
    problem to work around.

The full library is on the [Readings](resources.md) page.

---

## How the week works

**Tuesday carries the reading.** One or two substantial items, typically 45–75
minutes of preparation, plus discussion questions posted on the session page in
advance. Come able to answer them.

**Thursday is hands-on and assigns no new reading.** This is deliberate. Labs
are for building, breaking, and writing up what happened. Your total preparation
load is therefore roughly one reading per week, not one per meeting.

**Five sessions are individual meetings rather than a group class.** See
[individual meetings](#individual-meetings) below.

---

## Assessment

{{ grading_table() }}

Details, deliverables, and rubrics are on the [Assignments](assignments.md) page.

### On the decision log

The single thread running through this course is that you write down why you
did things, while you are doing them. You will keep a log of [Architectural
Decision Records](guides/writing-adrs.md) — a lightweight format borrowed from
software engineering — recording the choices you make on your project: which
model, which technique, whether to use retrieval, how to handle failure.

Four are due at checkpoints during the term. The full log is submitted with the
final project and is graded as a primary artifact.

A log that records a decision you later regretted, with the reasoning that led
there, is worth more than one that is quietly correct throughout. I am grading
the thinking, and thinking that never went wrong usually means the record was
written afterwards.

---

## Individual meetings

Five sessions this term are **individual meetings** rather than a group class.
Each student gets a scheduled 15-minute slot, and that week's work is
self-paced.

{{ conference_table() }}

The sign-up sheet goes out the Thursday before. Attending counts toward
participation exactly as attending class does.

Both project milestones fall in these weeks by design: your proposal (Week 5)
and your prototype (Week 10) are the two points where individual feedback is
worth most, and each meeting ends with a written goal for the next stretch.

What to bring, week by week: [Individual meetings](guides/conference-weeks.md).

---

## Using AI { #using-ai }

We will use generative Artificial intelligence as part of this course, and
subscriptions to GenAI platforms are available from the college through
[Microsoft Co-Pilot](https://m365.cloud.microsoft/) and
[BoodleBox](https://boodlebox.ai/). Often we use these subscriptions to test a
model's limitations and reflect on how we interact with such technologies.

For these reasons, each assignment will note specifically if Generative AI is
**not** allowed. For all other assignments you are free to use Generative AI,
but you must acknowledge use with citations. But, with great power comes great
responsibility: **if an assignment you submit includes AI hallucinations or AI
Slop, I will fail the assignment** regardless of whether such technology was
allowed. We will discuss this policy extensively during the first week of class.

If you are caught using Generative AI during such a non-generative
AI-approved assignment, you will fail the assignment and I will submit your
response to the honor court.

!!! danger "The two ways to fail on this policy"

    **Hallucinations or slop in submitted work** — fails the assignment even
    where AI was permitted. Permission to use a tool is not permission to skip
    reading what it produced.

    **AI on an assignment marked no-AI** — fails the assignment and goes to the
    [Honor Court](https://www.hsc.edu/student-life/honor-and-conduct).

### Where restrictions appear

Every assignment and session page states its position explicitly. Where
Generative AI is not permitted you will see a red **No generative AI on this
work** banner at the top of the page, with the reason. If there is no banner,
AI is permitted and must be cited.

You are never expected to infer a restriction. If a page is ambiguous, that is
my error — tell me and I will fix it.

### Acknowledging use

Cite it as you would any source. At minimum, state the tool, what you asked it
to do, and what you did with the output:

> Drafted the evaluation rubric with Claude (Anthropic), prompted with the task
> description and three example items; I rewrote criteria 2 and 4 after testing
> them against my own scored examples.

Your decision log is usually the right place for this on project work. A single
line is enough. What is not enough is "AI was used."

### On hallucinations and slop

Both terms get defined properly in Week 7, when we read TruthfulQA and build
evaluations — and there is a real distinction the literature argues about, which
is part of the point.

For grading purposes the working definitions are simpler. A **hallucination** is
a confident false statement: a citation to a paper that does not exist, a
statistic with no source, a quotation nobody said. **Slop** is text that has been
generated but not thought about — padded, genericised, technically on-topic and
substantively empty.

Both are detectable by reading, which is how I will detect them. The defence
against both is the same and is not complicated: read what you submit, and check
the claims it makes.

---

## Policies

### Attendance

Come to class. Discussion is a substantial part of what the course is, and it
does not work if the room is thin. If you must miss a session, the session page
carries the readings and the activity, but it cannot carry the conversation.

Attending your scheduled individual meeting during a conference week counts
the same as attending class.

### Late work

Talk to me before the deadline and we will almost always work something out.
Talk to me after and it becomes harder, though not impossible. Work submitted
without any conversation loses a letter grade per day.

Project milestones are the exception: because each one feeds the next, they
cannot slide far without cascading. If you are stuck on one, that is precisely
what the conferences are for.

### Academic integrity

The [Hampden-Sydney Honor Code](https://www.hsc.edu/student-life/honor-and-conduct)
applies in full. In this course the operative question is always the same: can
you account for the work you submitted? Collaboration is encouraged on labs and
expected in discussion; the project and its decision log are yours.

### Accessibility

If you have a documented disability, or think you may have an undocumented one,
contact the Office of Disability Services and come talk to me. Accommodations
are straightforward to arrange and I would rather set them up in Week 1 than in
Week 10.

---

<small>
This syllabus is generated from the course data files in the
[repository]({{ config.repo_url }}). Dates come from the
[Hampden-Sydney academic calendar](https://www.hsc.edu/calendars/academic-calendar).
Changes made during the term will appear here and are announced in class.
</small>
