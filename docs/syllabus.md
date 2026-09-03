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
appointment. Email or texting are the fastest ways to reach me, and asking for an appointment outside these hours is normal, not an imposition.

---

## Course description

Large language models are reshaping how we write, research, and solve problems.
This course introduces the principles and practice of prompt engineering: the
craft of communicating effectively with AI systems to produce reliable,
high-quality outputs.

We will begin by building a theoretical foundation in neural networks,
transformer architectures, and natural language processing. From there we
will develop techniques for crafting prompts that account for hallucination, bias,
and context constraints; learn to evaluate model outputs against evidence you
construct yourself; and apply structured prompting strategies including
chain-of-thought reasoning, retrieval-augmented generation, agents and tool use,
and system-level prompt design.

Particular attention is given to **what changes when a system has to run for
other people.** For this reason, we will pay specific attention to API integration, token accounting, cost management, and responsible use in production. Throughout the semester you will apply these skills in an individual project, building a proof-of-concept application that demonstrates both technical proficiency and an awareness of the limits of generative AI.

LLMs, NLP, and Generative AI are massive topics, and it is impossible to cover everything in 15 weeks. For this reason, I've chosen select topics and canonical literature that I feel best captures our current moment. But, as with any burgeoning technology, there is a lot to learn and not everyone agrees. For these reasons, we will cover contradictory approaches, ideas, and literature. For instance, we will cover chain-of-thought prompting alongside the paper arguing it is an illusion; and introduce a hallucination (truthfulQA)
benchmark alongside the critique saying it measures the wrong thing. And you
will **document your decisions as you make them** — in an ADR log recording what
you chose and why you chose it over the alternative, and a changelog recording
what actually changed and when. Both are graded as primary forms of assessment.
They answer different questions, which is why you keep both.

The course is named after Vaswani et al.'s 2017 paper. We read it in Week 3.

!!! info "No prerequisites"

    You do not need prior experience with coding, Machine Learning, or AI. We
    will cover the math at a high level so it is digestible, but also accessible
    for those in the class that have not taken linear algebra, algorithms, or
    differential equations. When we cover technical reports and white papers
    containing model architectures and math, I will tell you which sections to
    focus on.

    **You also do not need to install anything.** Everything hands-on in this
    course runs in a browser tab: the lab notebooks in
    [Google Colab](guides/colab.md), your project repository on
    [GitHub](guides/setup.md#week-1-your-repository-in-the-browser), and the
    college's own chat tools. If you would rather work locally — Python, an
    editor, a terminal — that route is written up in full and I will help you
    set it up, but nothing is graded on it.

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

## Required Content

**All content assigned in this course is free.**

- **[Prompt Engineering](https://www.gptaiflow.com/assets/files/2025-01-18-pdf-1-TechAI-Goolge-whitepaper_Prompt%20Engineering_v4-af36dcc7a49bb7269a58b1c9b89a8ae1.pdf)** — Lee Boonstra (Google, 2025). 68pp, assigned in sections. The applied text.
- **[Auditing AI](https://mitpress.mit.edu/9780262051729/auditing-ai/)** — The Marquand House Collective (MIT Press, 2026). Open access.
- **Deep Learning, Chapters 5 & 6** — 3Blue1Brown. An excellent video resource
  for all things mathematical, and the visual spine of Weeks 2 and 3:
  [Transformers, the tech behind LLMs](https://www.youtube.com/watch?v=wjZofJX0v4M)
  and [Attention in transformers, step-by-step](https://www.youtube.com/watch?v=eMlx5fFNoYc).

Everything else is a linked paper, podcast, or article. This site links out and
hosts nothing.

!!! success "Zero-cost reading list"

    A required text you cannot afford is a barrier disguised as a syllabus. So
    there is no book to buy, no course pack, and no reading behind a paywall or
    a library login. Moreover, a test in this site's repository fails the build if a
    gated reading is ever added.

    If you hit anything you cannot open, tell me. That is a bug, not your
    problem to work around.

The full library is on the [Readings](resources.md) page.

---

## How the week works

**Tuesdays cover a new idea or concept.** I will assign one or two substantial items, typically 45–75 minutes of preparation, plus discussion questions posted on the session page in advance. Come able to answer them, and come with questions. 

**Thursdays are lab days, and they are yours.** Each lab has a
[notebook](guides/colab.md) that opens in your browser. Explore it beforehand at
whatever depth interests you — change the inputs, break things, follow the
question you actually find interesting rather than the one I wrote down.

Then **Thursday is you showing what you found.** Ten minutes each, informally,
laptop open. We are not working through steps together as a class like robots;
we are comparing what happened when thirteen people poked at the same thing.

A method that broke is worth more than one that worked, and these labs are
graded on the write-up rather than the result. You also do not need working code
to have something to show — a table, a screenshot, or a confusion you can state
precisely all count.

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

**Use them to understand the reading.** A model that explains a paragraph back
to you in different words is doing something a classmate would do, and you are
entitled to it. [Using BoodleBox to understand a
reading](guides/boodlebox.md) walks through getting an account, asking a
question worth answering, and — the part that matters — checking what it told
you. Every session with reading links it.

Accounts are free through the Computing Center. Request one in the first week;
they take a few days.

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
