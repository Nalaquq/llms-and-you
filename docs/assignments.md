# Assignments

{{ grading_table() }}

---

## Semester Project and ADR Log { #project }

**35% · Due {{ last_meeting.long_date }}**

{{ genai_banner('project') }}

A prompt-engineering system of your own design, built across the term and
submitted with the decision log you kept while building it.

The system can be almost anything that involves directing a language model
deliberately: a retrieval-augmented assistant over a corpus you care about, an
evaluation harness for a task nobody has benchmarked well, a workflow that
decomposes a hard problem across several prompts, a tool-using agent, a
red-teaming study of a specific failure mode. The requirement is not scale. It
is that the thing does something you can evaluate, and that you made real
choices building it.

### Starting it

You already have it. Your copy of
**[Nalaquq/llms-and-you-project](https://github.com/Nalaquq/llms-and-you-project)**
was made and cloned in the Week 1 lab; the project goes in that folder.

If you were not there, one command makes your copy and clones it:
`gh repo create llms-project --template Nalaquq/llms-and-you-project --public
--clone`. Not a fork — a fork stays tied to my repository, and a template copy
is yours. The [setup guide](guides/setup.md#your-own-copy-of-the-project-template)
has the website route too. It gives
you the structure these projects turn out to need: prompts kept as versioned
files, an evaluation set, an ADR log wired to the format above, a running
`TODO.txt`, and a pre-commit hook that stops you committing an API key. It
contains no project. That part is yours.

You are not required to use it. You *are* required to end up with what it
contains, so starting somewhere else means building the same things by hand.

### Milestones

{{ milestone_table() }}

Weeks 5 and 10 are individual-meeting weeks, so both milestones are discussed
one-to-one rather than in class. Each ends with a written goal for the next
stretch of work.

### What is graded

- **The system** — does it work, and can you show that it works?
- **The decision log** — four required ADRs plus whatever else you recorded.
  Graded on the quality of reasoning, not the correctness of the outcome.
- **The changelog** — what changed and when, kept alongside the ADRs. The two
  answer different questions: an ADR says why you chose something over the
  alternative, a changelog says what actually moved and in what order. Keep
  both. Neither substitutes for the other.
- **The reflective introduction** — 1,000 words at the front of the log,
  written last: what you set out to build, what you actually built, and which
  recorded decision you now think was wrong.

!!! tip "On writing the log honestly"

    A log containing a decision you later regretted, with the reasoning that
    led you there, is worth more than one that is quietly correct throughout.
    I am grading the thinking. Thinking that never went wrong usually means the
    record was written afterwards, and it reads that way.

---

## HackAPrompt Red-Team Midterm { #midterm }

**15% · Opens Week 8 (Thu Oct 15) · Due Week 9 (Thu Oct 22)**

{{ genai_banner('midterm') }}

Adversarial prompting against the [HackAPrompt](https://www.hackaprompt.com/)
environment, submitted as a write-up rather than a score.

Fall Break removes Week 8's Tuesday, so the unit opens with a full working lab
that needs no advance reading — the format and the calendar happen to suit each
other here.

### Deliverable

A short paper, roughly 1,500 words:

1. **The attack.** What you got the system to do that it was built not to do.
   Include the exact prompt.
2. **Why it worked.** Mechanism, not narrative. Connect it to something from
   Themes 1–3: what about how these models process instructions made this
   possible?
3. **The defence.** What you would build to stop it, and — importantly — what
   your defence would cost in capability or user experience.
4. **What it generalises to.** Is this specific to one system, or a class of
   failure?

### Why this is assigned

Making a system fail on purpose requires understanding it better than using it
successfully does. It is also, deliberately, an assignment a model cannot
complete on your behalf.

We do this in a sandboxed competition environment, against systems built to be
attacked. The rules of engagement are covered in the Week 8 lab, and they matter.

---

## Thursday Labs { #labs }

**20% · Twelve sessions across the term**

{{ genai_banner('labs') }}

Hands-on work, graded on the write-up rather than the result.

Labs assign no advance reading — that is the whole point of the Tuesday/Thursday
split, and it is why your weekly preparation load is one reading, not two. Bring
what you built in the previous session.

Each lab is submitted as a short write-up: what you did, what happened, what you
expected instead, and what you would try next. **A lab that failed and was
documented honestly scores better than one that worked and was not.** This is
not a generous gesture; failed experiments that are well described are more
useful than successful ones that are not.

The lowest two lab grades are dropped. Things happen.

---

## Concept Checks at Individual Meetings { #concept-checks }

**20%**

{{ genai_banner('concept-checks') }}

At each [individual meeting](guides/conference-weeks.md) you are asked about
concepts from the [study guide](study-guide.md) — everything the course has
covered up to that week. Out loud, in your own words, across a desk.

**The study guide is the whole of what can be asked.** Nothing outside that page
appears, and each entry already tells you what you are expected to be able to
*do* with the idea: the **You should be able to** lines are the questions. A
concept you can only recite in the words it was defined in is one you cannot yet
apply, and applying it is what is being graded.

The [Burchell arc](resources.md#the-burchell-arc) is fair game at the same
meetings, as far as it has run by then. Not the episode summaries — what has
changed across them, and what has changed in her.

### How it is graded

Roughly ten minutes of the fifteen. You are not being caught out: if you cannot
get to an answer, we work toward it together and that is worth something.
Fluency in the vocabulary is worth less than knowing when an idea applies and
when it does not.

Three meetings, in Weeks 4, 5, and 10. Later meetings cover more ground, because
more has been taught.

---

## Oral Progress Reports { #progress-reports }

**10%**

{{ genai_banner('progress-reports') }}

The other half of each meeting. Five minutes on where your project stands: what
you built since we last met, what broke, what you decided and why, and what you
intend next.

**Graded on whether you can say plainly where you are.** A project that stalled
and is described accurately scores better than one described vaguely. This is
the spoken version of what your [decision log](guides/writing-adrs.md) does in
writing, and the two should agree — if the log says one thing and you say
another in the room, that gap is the interesting part.

Each report ends with a **written goal** for the next stretch, agreed between
us. The following meeting starts by checking it.

Attending your scheduled meeting is how both of these components are earned.
There is no separate participation grade; if something makes a slot impossible,
email me and we find another time. The one thing that does not work is silence.
