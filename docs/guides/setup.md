# Setting up your tools

We install everything together in class. This page is the reference and the
fallback, not homework.

!!! success "No programming experience required"

    That is not a formality. This course assumes you have never installed
    Python and never opened a terminal. Every setup step is done together, in
    class, on whatever machine you brought.

    If something here does not work on your machine, that is normal and it is
    my problem to solve, not yours. Email me or come to office hours.

There are two setup sessions, a week apart, and they are deliberately separate:

| | |
|:---|:---|
| **Week 1, Thursday** | [Claude Code](#week-1-claude-code-and-the-desktop-app) — installed as material for the decision-record lab |
| **Week 2, Thursday** | [Python and VS Code](#week-2-python-and-vs-code) |

---

## Week 1: Claude Code { #week-1-claude-code-and-the-desktop-app }

The Week 1 lab is really about [decision
records](writing-adrs.md) — installing Claude Code is how we manufacture
some decisions worth recording. Do the install; the lab is what you do next.

### Claude Code — the one we use

**[claude.com/claude-code](https://claude.com/claude-code)** — per-platform
install instructions are in the
[setup docs](https://docs.claude.com/en/docs/claude-code/setup).

This is Claude in your terminal, and the difference that matters is that **it
can see and change files in a folder.** A chat window only knows what you paste
into it; Claude Code can read a directory, open the files in it, and edit them.

Start it by opening a terminal, moving to a folder, and running:

```bash
claude
```

Then just talk to it:

```
what files are in this folder?
```

### The desktop app — optional

[claude.ai/download](https://claude.ai/download), macOS and Windows. A
comfortable surface for long conversations. Install it if you want it; nothing
in the course requires it.

### The decisions you just made without noticing

Which install method. Where you put your project folder. Whether you took the
first suggestion Claude Code offered or pushed back. Whether you bothered with
the desktop app at all.

None of those felt like decisions at the time, which is exactly why they are
good practice material. **ADR-001** asks you to write one of them up properly —
context, decision, alternatives, consequences — and the part that is graded is
whether your alternatives section contains a real alternative.

---

## Week 2: Python and VS Code { #week-2-python-and-vs-code }

Week 2's lab needs a toolchain of your own, so we build one.

### Python

Install **Python 3.11 or newer** from
[python.org](https://www.python.org/downloads/).

On Windows, tick **"Add Python to PATH"** during installation — it is easy to
miss and causes most of the problems we see.

```bash
python3 --version
```

### VS Code

Install [Visual Studio Code](https://code.visualstudio.com/), then add the
**Python extension** (Extensions panel, ++ctrl+shift+x++, search "Python",
install the Microsoft one).

You do not need to know VS Code well. We use a small fraction of it.

### A virtual environment

Keeps this course's packages separate from anything else on your machine:

=== "macOS / Linux"

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install anthropic
    ```

=== "Windows"

    ```powershell
    python -m venv .venv
    .venv\Scripts\activate
    pip install anthropic
    ```

When it is active your prompt starts with `(.venv)`. If you close the terminal,
run `activate` again — forgetting this is the single most common source of "it
worked yesterday".

---

## Model access

Three things, for three purposes. They are not interchangeable.

| For | Use | Cost to you |
|:---|:---|:---|
| Everyday chat and coursework | [Microsoft Co-Pilot](https://m365.cloud.microsoft/) · [BoodleBox](https://boodlebox.ai/) | Free — provided by the college |
| Working with files and folders | Claude Code, desktop app | Sign-in required |
| Scripts and your project | An **API key** | Arranged at the start of term |

An API key is not the same as a chat login. It is how a Python script talks to
the model, and it is billed per token. **Do not buy credits on your own before
we have talked** — access is handled for you.

!!! warning "Never put an API key in your code"

    Keys go in an environment variable, never in a file you might share or
    commit. Once `ANTHROPIC_API_KEY` is set, the library finds it:

    ```python
    import anthropic

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment
    ```

    A key pasted into a script and pushed to GitHub is scraped within minutes.
    This is not hypothetical — it is the most common way students lose access.

---

## Your project starts from a template

When you begin the semester project, do not start from an empty folder. Start
from **[Nalaquq/llms-and-you-project](https://github.com/Nalaquq/llms-and-you-project)**
and use the green **Use this template** button — not fork. It sets up the
structure you are graded on, and its README covers the environment and API key
steps again in the order you will actually need them.

---

## When something breaks

Errors are information, not failure. The common ones:

| What you see | What it means |
|:---|:---|
| `command not found: claude` | Claude Code is not installed, or the terminal needs restarting after install |
| `command not found: python3` | Python not installed, or not on PATH (Windows: reinstall and tick the box) |
| `ModuleNotFoundError: No module named 'anthropic'` | Virtual environment not active, or `pip install anthropic` not run |
| `AuthenticationError` | `ANTHROPIC_API_KEY` is not set in this terminal |
| `RateLimitError` (429) | Too many requests too fast. Wait and retry — handled properly in Week 13 |
| `BadRequestError` (400) | The request is malformed. Read the message; it usually names the field |

Bring the **exact error text** to class or office hours. "It didn't work" is
hard to help with; a pasted traceback is usually solved in under a minute.

---

## A note on following tutorials

There is a great deal of Claude and OpenAI tutorial material online, and much of
it is out of date in ways that will not be obvious to you.

The clearest example, which you meet in the Week 4 lab: nearly every prompt
engineering tutorial tells you to adjust `temperature` to control randomness. On
current frontier models that parameter has been **removed** — sending it returns
an error — and replaced by an `effort` setting. The tutorials have not caught
up.

When sources contradict, the [API reference](https://docs.claude.com/en/api/overview)
wins. Worth internalising early: in a field moving this fast, knowing *where the
authoritative answer lives* is more durable than knowing the answer.
