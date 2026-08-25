# Writing Architectural Decision Records

An ADR is a short document recording one decision: what you decided, why, what
you gave up, and what you rejected.

The format comes from software engineering — Michael Nygard's 2011 post
popularised it, and it is now standard practice at AWS, Azure, and IBM. You will
use it for prompt design decisions, which is a slightly unusual application and
a natural one: prompt engineering is full of choices that look arbitrary six
weeks later unless you wrote down why you made them.

**Reference:** [adr.github.io](https://adr.github.io/) ·
[Templates](https://adr.github.io/adr-templates/)

---

## The template

Use this unless you have a reason not to.

```markdown
# ADR-00N: <the decision, stated as a title>

## Status
Proposed | Accepted | Superseded by ADR-00M

## Context
What situation forces a decision here? What constraints are real?
Written so someone who has not been in your head can follow.

## Decision
What you decided. Active voice: "We will use..." not "It was decided..."

## Alternatives considered
What else you could have done, and why you did not.
This section is the point of the document.

## Consequences
What becomes easier. What becomes harder. What you will have to
watch out for later.
```

Half a page to a page. If yours runs to three pages, you are documenting several
decisions and should split them.

---

## The four required ADRs

| | Due | Decision |
|:---|:---|:---|
| **ADR-001** | Week 1 (Thu Aug 27) | Any decision you made setting up Claude Code |
| **ADR-002** | Week 5 (Thu Sep 24) | Technique selection for your project |
| **ADR-003** | Week 9 (Thu Oct 22) | How your system handles failure |
| **ADR-004** | Week 10 (Thu Oct 29) | Retrieval design — or why you are not using retrieval |

ADR-001 is due in the first week, before you have anything complicated to
decide. That is deliberate: the format is easier to learn on a simple decision
than on a hard one, and the Week 1 lab manufactures a handful of small ones by
having you install something.

Write others whenever you make a choice you might question later. The full log
is submitted with the final project.

!!! tip "Write it while you decide, not after"

    The Week 1 lab has you do both, back to back, so you can feel the
    difference. Reconstructing three decisions you already made is easy and
    produces tidy records. Writing one *as you decide* is slower, more
    uncomfortable, and contains doubt.

    The second kind is worth having. The first kind is a description of a
    conclusion.

---

## What separates a good ADR from a bad one

**The alternatives section is where the value is.** An ADR that records what you
chose is a note. An ADR that records what you rejected, and why, is a decision
record. When you reread it in November wondering why you did not use retrieval,
the answer needs to be in there.

**Write it when you decide, not afterwards.** Retroactive ADRs read as
justification rather than reasoning, and they are easy to spot — they never
contain doubt, and real decisions almost always do.

**Record the constraint honestly.** "We chose this because the alternative
required a GPU I do not have" is a legitimate and useful entry. "We chose this
for optimal performance characteristics" when the real reason was time is not.

**Supersede rather than edit.** If you change your mind, write a new ADR that
supersedes the old one and mark the old one's status. The trail of changed minds
is the most interesting part of a mature log.

---

## Why this course grades them

Prompt engineering has a specific failure mode: something works, you do not know
why, and you cannot tell later whether it still works or whether you have been
carrying a superstition for six weeks. Half the techniques in the [Prompt
Report](https://arxiv.org/abs/2406.06608) were discovered by people noticing
something worked and not initially knowing why.

Writing decisions down as you make them is the cheapest available defence
against that. It is also, not incidentally, what makes work auditable — which
is the subject of Week 14, and the connection is not accidental.

---

!!! note "This site keeps its own log"

    The [decision log](../adr/index.md) for this course website is public,
    including the decisions about how the course itself is structured. It is
    worth skimming as an example of the format applied to real choices, some of
    which are debatable.
