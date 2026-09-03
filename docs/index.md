---
hide:
  - navigation
---

# LLMs & You
## *Attention is All You Need*

**Hampden-Sydney College · Fall 2026**

Large language models are reshaping how we write, research, and solve problems.
This course is about the principles and practice of prompt engineering — how to
build systems that work, and how to tell the difference between one that works
and one that only appears to. The hands-on work runs in your browser, in
notebooks built on **scikit-learn**, **Hugging Face**, and the rest of the
ordinary Python toolkit.

We will read the 2017 paper this course is named after. We will also read the 2025 paper
arguing that the field's most celebrated technique is an illusion. You will learn by doing, and you will be doing some serious learning. Enjoy!

---

## The essentials

| | |
|:---|:---|
| **Meets** | Tuesday & Thursday, 2:00–3:30 PM |
| **Location** | PRC 106 |
| **Term** | {{ semester.term }} — {{ session_count }} sessions across 15 weeks |
| **Instructor** | Sean Gleason |
| **Email** | [sgleason@hsc.edu](mailto:sgleason@hsc.edu) |
| **Office** | Pannill 100E |
| **Office hours** | T/TH 12:00–2:00 · W 9:00–12:00 · and by appointment |

[Read the syllabus](syllabus.md){ .md-button .md-button--primary }
[See the schedule](schedule.md){ .md-button }
[Start your project](https://github.com/Nalaquq/llms-and-you-project){ .md-button }

---

## What you will do

<div class="grid cards" markdown>

-   :material-book-open-page-variant:{ .lg .middle } **Read the field, including where it disagrees with itself**

    ---

    Vaswani's transformer paper alongside Alammar's illustrated walkthrough.
    TruthfulQA alongside the benchmark critique that says TruthfulQA is
    miscategorised. Chain-of-thought alongside the paper calling it a mirage.

-   :material-flask-outline:{ .lg .middle } **Run things on Thursdays, then show what you found**

    ---

    Ten hands-on labs, each a notebook that opens in your browser with nothing
    installed. We will break a tokenizer. We will watch counting words run out
    of road, and see what word vectors do about it. We will build an evaluation
    set, give a model a tool, measure what a system costs per user, and run an
    open-weight model on a free GPU to ask whether self-hosting wins.

    You explore beforehand; Thursday is you showing the room one thing you
    found. Preferably one that broke.

-   :material-file-document-edit-outline:{ .lg .middle } **Document every decision as you make it**

    ---

    You will keep an Architectural Decision Record log all semester. This is a living document. It is graded as a primary form of assessment to justify your decisions across the semester.

-   :material-shield-search:{ .lg .middle } **Attack a system, then defend it**

    ---

    The midterm is a red-teaming exercise using HackAPrompt. You find the
    attack that works, explain why it works, and design the defence.

</div>

---

## Free & Open Everything

Every reading in this course is free and open access.

**There is also nothing to install.** The labs run in Google Colab, on a Google
login, from any machine including a Chromebook or a library computer. If you
would rather build a local toolchain, the guide covers that too and I will sit
with you while you do it — but it is an option, never a requirement.

When a paper contains mathematics you do not understand, you will be told which
sections to skip and what to take from the rest. Learning to read a paper you
cannot fully understand is itself one of the skills this course teaches.

[Set up your tools](guides/setup.md){ .md-button }
[Working in Colab](guides/colab.md){ .md-button }

---

## A note on using AI in a course about AI

You will use these tools constantly — that is the point — and the college
provides them through [Microsoft Co-Pilot](https://m365.cloud.microsoft/) and
[BoodleBox](https://boodlebox.ai/).

**You may use Generative AI unless an assignment says otherwise, and you must
cite it when you do.** When AI is not
permitted, the page says so in red.

Two things will fail an assignment. Submitting **hallucinations or slop** — even
where AI was allowed, because permission to use a tool is not permission to skip
reading what it produced. And using AI where it was **prohibited**, which also
goes to the Honor Court.

Read the [full policy](syllabus.md#using-ai). We discuss it at length in Week 1.

---

<small>
This site is generated from structured course data — every date, reading, and
session page is derived from the YAML files in `data/`, validated on every
build. The
[repository]({{ config.repo_url }}) is meant to be read as an example of the
documentation practice the course teaches.
</small>
