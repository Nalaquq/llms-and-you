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
| **Week 1, Thursday** | [GitHub, your project repository, Claude Code, and VS Code](#week-1-your-repository-and-your-tools) — the folder you work in all term |
| **Week 2, Thursday** | [Python and a virtual environment](#week-2-python-and-vs-code) |

---

## Week 1: Your repository and your tools { #week-1-your-repository-and-your-tools }

By the end of this lab you have a GitHub account, your own copy of the project
template cloned onto your machine, and two tools that can read it. Everything
after Week 1 happens inside that folder.

### A GitHub account

**[github.com](https://github.com/)** — free. Pick a username you would be
willing to put on a CV; this account will outlive the course.

If you want it written down rather than demonstrated,
[Hello World](https://docs.github.com/en/get-started/using-github/hello-world)
covers repositories, branches, and commits in about twenty minutes.

### Your own copy of the project template

Open **[Nalaquq/llms-and-you-project](https://github.com/Nalaquq/llms-and-you-project)**
and press the green **Use this template** button.

**Not fork.** A fork stays tied to my repository; a template copy is yours. Make
it public and give it a name that says what it is.

### Clone it

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-PROJECT.git
cd YOUR-PROJECT
```

Put it somewhere you will find it again — Desktop is fine, Downloads is not.

Then turn on the credential guard. Once per clone:

```bash
git config core.hooksPath .githooks
```

It refuses any commit containing something shaped like an API key. See
[Never put an API key in your code](#model-access) below for why that matters
more than it sounds like it does.

### Claude Code — the CLI we use all term

**[claude.com/claude-code](https://claude.com/claude-code)** — per-platform
install instructions are in the
[setup docs](https://docs.claude.com/en/docs/claude-code/setup).

This is Claude in your terminal, and the difference that matters is that **it
can see and change files in a folder.** A chat window only knows what you paste
into it; Claude Code can read a directory, open the files in it, and edit them.

Start it inside your clone:

```bash
claude
```

Then just talk to it:

```
what is in this repository, and what is each folder for?
```

### VS Code

Install **[Visual Studio Code](https://code.visualstudio.com/)** and open your
cloned folder in it — **File → Open Folder**, not open-a-file. Run `claude`
again from VS Code's built-in terminal so the editor and the model are looking
at the same directory.

The Python extension comes next week. Today VS Code is somewhere to see the
files while Claude Code changes them.

### What is in the folder

You did not build this layout, so none of it is obvious. We walk it together in
class; this is the version to come back to.

| Path | What it is for |
|:---|:---|
| `TODO.txt` | What the next version of your prompt needs to do |
| `PROMPTING.md` | The practices this course grades. Read this one first |
| `prompts/` | Your prompts, as versioned files — one file per prompt |
| `src/project/` | Your code. `client.py` is written for you; the rest is yours |
| `evals/` | Your test set. Started in week one, not the week before it is due |
| `docs/adr/` | Your decision log — why you chose things. Graded |
| `CHANGELOG.md` | What changed and when. Graded alongside the ADRs |
| `tests/` | Ordinary tests, for the parts that are ordinary code |

`TODO.txt` is the one to start using today. It is a running list of what the
next draft of your prompt has to do, in sections by where each item ends up —
in the prompt itself, in `evals/`, in an ADR, or in a question for me. Write the
line the moment you have the thought. An hour later you no longer have it.

### The desktop app — optional

[claude.ai/download](https://claude.ai/download), macOS and Windows. A
comfortable surface for long conversations. Install it if you want it; nothing
in the course requires it.

### The decisions you just made without noticing

Which install method. What you named the repository. Where you put the folder.
Whether you took the first suggestion Claude Code offered or pushed back.

None of those felt like decisions at the time, which is exactly why they are
good practice material. **ADR-001** asks you to write one of them up properly —
context, decision, alternatives, consequences — and the part that is graded is
whether your alternatives section contains a real alternative.

---

## Week 2: Python and a virtual environment { #week-2-python-and-vs-code }

Week 2's lab needs a toolchain of your own, so we build one.

### Python

Install **Python 3.11 or newer** from
[python.org](https://www.python.org/downloads/).

On Windows, tick **"Add Python to PATH"** during installation — it is easy to
miss and causes most of the problems we see.

```bash
python3 --version
```

### The Python extension for VS Code

VS Code itself went on in Week 1. Add the **Python extension** now: Extensions
panel, ++ctrl+shift+x++, search "Python", install the Microsoft one.

If you missed Week 1, install [VS Code](https://code.visualstudio.com/) first.
You do not need to know it well. We use a small fraction of it.

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

You already made your copy in [Week 1](#week-1-your-repository-and-your-tools).
Do not start the semester project from an empty folder — work in that clone. Its
README covers the environment and API key steps again in the order you will
actually need them, and the structure it sets up is the structure you are graded
on.

---

## When something breaks

Errors are information, not failure. The common ones:

| What you see | What it means |
|:---|:---|
| `command not found: git` | Git is not installed. macOS: run `git --version` and accept the prompt. Windows: install [Git for Windows](https://git-scm.com/download/win) |
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
