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

If you were not there, use the green **Use this template** button rather than
forking — a fork stays tied to my repository, a template copy is yours. It gives
you the structure these projects turn out to need: prompts kept as versioned
files, an evaluation set, an ADR log wired to the format above, a running
`TODO.txt`, and a pre-commit hook that stops you committing an API key. It
contains no project. That part is yours.

You are not required to use it. You *are* required to end up with what it
contains, so starting somewhere else means building the same things by hand.

### Milestones

| Due | Deliverable |
|:---|:---|
| **Week 5** (Thu Sep 24) | Project proposal + **ADR-002**: technique selection and rationale |
| **Week 9** (Thu Oct 22) | **ADR-003**: how your system handles failure |
| **Week 10** (Thu Oct 29) | Working prototype + **ADR-004**: retrieval design (or why not) |
| **Week 15** (Thu Dec 3) | Final system, full ADR log, reflective introduction, presentation |

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

## Reading Responses and Burchell Reflections { #responses }

**20%**

{{ genai_banner('responses') }}

### Weekly responses

Short written responses to Tuesday readings — a few hundred words, posted
before class. Each session page lists discussion questions; answer one, or
raise something better.

These are graded lightly and quickly. The purpose is that you arrive having
thought about the reading, and that I know what the room is thinking before I
walk into it.

### The Burchell reflections

Three longer pieces, due **Weeks 2, 7, and 15**, tracking the [Burchell
arc](resources.md#the-burchell-arc) — six *Real Python* episodes with the same
guest, from July 2022 to April 2026.

The first two were recorded four and three months before ChatGPT was released.
The last, two months before this class started. Read consecutively they are a record of a
field changing under someone who was paying close attention throughout, and the
reflections ask you to track both what changed in the field and what changed in
her.

The Week 15 reflection is written in class, and asks a harder version of the
question: which of your own beliefs from Week 1 do you now think was wrong?

---

## Participation { #participation }

**10%**

Judged on the quality of what you contribute, not the frequency. A student who
speaks twice a semester and both times moves the discussion forward is doing
better than one who talks constantly.

**Attending your scheduled individual meeting counts here.** There are five
such sessions across Weeks 4, 5, and 10; see [Individual
meetings](guides/conference-weeks.md).

If speaking in class is genuinely difficult for you, come talk to me in the
first two weeks. There are other ways to demonstrate engagement and I would
rather arrange one early than grade you down for a term.
