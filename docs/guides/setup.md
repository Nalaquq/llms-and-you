# Setting up your tools

We install everything together in class. This page is the reference and the
fallback, not homework.

!!! success "No programming experience required"

    That is not a formality. This course assumes you have never installed
    Python and never opened a terminal. Every setup step is done together, in
    class, on whatever machine you brought.

    If something here does not work on your machine, that is normal and it is
    my problem to solve, not yours. Email me or come to office hours.

!!! info "Commands come in two flavours — pick your platform once"

    Every command on this site is given twice: **macOS / Linux** for the Unix
    shells (bash and zsh), and **Windows (PowerShell)** for the terminal that
    opens by default on Windows.

    Pick your tab once and the rest of the site follows you, on this page and
    every other one. **Both tabs are always there**, including where the two
    are character-for-character the same — `git` and `claude` mostly are. You
    should never have to work out whether a command applies to you.

There are two setup sessions, a week apart, and they are deliberately separate:

| | |
|:---|:---|
| **Week 1, Thursday** | [GitHub, your project repository, Claude Code, and VS Code](#week-1-your-repository-and-your-tools) — the folder you work in all term |
| **Week 2, Thursday** | [Python and a virtual environment](#week-2-python-and-vs-code) |

---

## Week 1: Your repository and your tools { #week-1-your-repository-and-your-tools }

By the end of this lab you have a GitHub account, Git installed and able to
push to it, your own copy of the project template cloned onto your machine, and
two tools that can read it. Everything after Week 1 happens inside that folder.

Work down this page in order. Each step assumes the one above it worked.

### A GitHub account

**[github.com](https://github.com/)** — free. Pick a username you would be
willing to put on a CV; this account will outlive the course.

If you want it written down rather than demonstrated,
[Hello World](https://docs.github.com/en/get-started/using-github/hello-world)
covers repositories, branches, and commits in about twenty minutes.

### Install Git

Git is the thing that does the cloning, committing, and pushing. It is separate
from GitHub: Git runs on your machine, GitHub is the website that stores a copy.
You need both.

=== "macOS / Linux"

    ```bash
    # macOS: this prints a version, or offers to install the tools that provide it.
    git --version

    # Debian / Ubuntu, if the above says it is missing
    sudo apt update && sudo apt install git

    # Fedora
    sudo dnf install git
    ```

    On macOS the prompt that appears says *Command Line Developer Tools*. Accept
    it and wait; it is a few minutes and it installs Git among other things.

=== "Windows (PowerShell)"

    ```powershell
    winget install --id Git.Git -e --source winget
    ```

    Then **close PowerShell and open a new window.** The installer adds Git to
    your PATH, and a window opened before that happened will not see it.

    If `winget` is not recognised, download the installer from
    [git-scm.com/download/win](https://git-scm.com/download/win) and accept
    every default.

Check it worked. This is the same command on both:

=== "macOS / Linux"

    ```bash
    git --version
    ```

=== "Windows (PowerShell)"

    ```powershell
    git --version
    ```

Any version number from 2.30 upwards is fine.

### Tell Git who you are

Git stamps every commit with a name and an email, and it refuses to commit until
you have set them. Do this once per machine, not once per project.

Use the email attached to your GitHub account, or commits will not link to your
profile. It is fine for this to be your college address.

=== "macOS / Linux"

    ```bash
    git config --global user.name "Your Name"
    git config --global user.email "you@example.com"
    ```

=== "Windows (PowerShell)"

    ```powershell
    git config --global user.name "Your Name"
    git config --global user.email "you@example.com"
    ```

!!! warning "This is public"

    Every commit you push carries that name and email, permanently and visibly.
    If you would rather not publish your address, GitHub can give you a private
    one — Settings → Emails → *Keep my email address private* — and it looks
    like `12345678+username@users.noreply.github.com`. Use that instead.

### Install the GitHub CLI — `gh` — and sign in { #install-the-github-cli-and-sign-in }

You will push work to GitHub, and GitHub stopped accepting passwords for that in
2021. The short way past this is `gh`, which handles the credential for you.

=== "macOS / Linux"

    ```bash
    # macOS, with Homebrew
    brew install gh

    # Debian / Ubuntu
    sudo apt install gh

    # Fedora
    sudo dnf install gh
    ```

=== "Windows (PowerShell)"

    ```powershell
    winget install --id GitHub.cli -e --source winget
    ```

If you have no Homebrew and no `apt`, the per-platform instructions are at
[cli.github.com](https://cli.github.com/).

Then sign in. It opens a browser, gives you an eight-character code to paste,
and is done in under a minute:

=== "macOS / Linux"

    ```bash
    gh auth login
    ```

=== "Windows (PowerShell)"

    ```powershell
    gh auth login
    ```

Choose **GitHub.com**, then **HTTPS**, then **yes** when it offers to
authenticate Git with your GitHub credentials. That last answer is the one that
makes `git push` work later without asking for anything.

### Make your own copy, and clone it { #your-own-copy-of-the-project-template }

One command. It creates a repository on your GitHub account from the course
template, then clones it to the folder you are standing in. Replace
`llms-project` with whatever you want yours called:

=== "macOS / Linux"

    ```bash
    gh repo create llms-project \
      --template Nalaquq/llms-and-you-project \
      --public --clone
    cd llms-project
    ```

=== "Windows (PowerShell)"

    ```powershell
    gh repo create llms-project `
      --template Nalaquq/llms-and-you-project `
      --public --clone
    cd llms-project
    ```

Run it from wherever you want the folder to live — your Desktop is fine,
Downloads is not.

!!! question "Why not just `git clone` my repository?"

    Because you could not push to it. A plain clone points at *my* repository,
    which you do not have write access to, so the commit at the end of today
    would have nowhere to go.

    `--template` makes a repository that is **yours**, with a clean history
    starting at your first commit. It is not a fork either — a fork stays tied
    to mine and shows up on GitHub as derived from it.

??? note "If you would rather do it on the website"

    Open
    [github.com/Nalaquq/llms-and-you-project/generate](https://github.com/Nalaquq/llms-and-you-project/generate),
    which is the *Create a new repository from a template* form. Name it, set it
    **Public**, and press **Create repository**.

    That page is the same thing the **Use this template** button on the
    repository opens, if you would rather find it that way.

    Then clone what you just made:

    === "macOS / Linux"

        ```bash
        git clone https://github.com/YOUR-USERNAME/YOUR-PROJECT.git
        cd YOUR-PROJECT
        ```

    === "Windows (PowerShell)"

        ```powershell
        git clone https://github.com/YOUR-USERNAME/YOUR-PROJECT.git
        cd YOUR-PROJECT
        ```

### Turn on the credential guard { #clone-it }

Once per clone:

=== "macOS / Linux"

    ```bash
    git config core.hooksPath .githooks
    ```

=== "Windows (PowerShell)"

    ```powershell
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

=== "macOS / Linux"

    ```bash
    claude
    ```

=== "Windows (PowerShell)"

    ```powershell
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

=== "macOS / Linux"

    ```bash
    python3 --version
    ```

=== "Windows (PowerShell)"

    ```powershell
    python --version
    ```

That difference persists: **`python3` on macOS and Linux, `python` on
Windows.** Everywhere this page shows one, the other tab shows the other.

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

=== "Windows (PowerShell)"

    ```powershell
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install anthropic
    ```

When it is active your prompt starts with `(.venv)`. If you close the terminal,
activate it again — forgetting this is the single most common source of "it
worked yesterday":

=== "macOS / Linux"

    ```bash
    source .venv/bin/activate
    ```

=== "Windows (PowerShell)"

    ```powershell
    .venv\Scripts\Activate.ps1
    ```

!!! warning "Windows: `running scripts is disabled on this system`"

    PowerShell blocks scripts by default, and the activate script is one. Run
    this once, in the same window, then activate again:

    ```powershell
    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
    ```

    `CurrentUser` matters — it changes the policy for your account only, not
    the machine.

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
    commit. A key pasted into a script and pushed to GitHub is scraped within
    minutes. This is not hypothetical — it is the most common way students lose
    access.

Setting it is the one place where the two platforms look nothing alike:

=== "macOS / Linux"

    ```bash
    export ANTHROPIC_API_KEY='sk-ant-...'
    ```

    Lasts until you close the terminal. To make it permanent, add that line to
    `~/.zshrc` (macOS) or `~/.bashrc` (most Linux), then open a new terminal.

=== "Windows (PowerShell)"

    ```powershell
    $env:ANTHROPIC_API_KEY = 'sk-ant-...'
    ```

    Lasts until you close the window. To make it permanent:

    ```powershell
    [Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY', 'sk-ant-...', 'User')
    ```

    Then **open a new terminal** — the window you typed it in will not see it.

Once it is set, the library finds it on its own. This is the same on both:

```python
import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment
```

Check it is set in *this* terminal before you go looking for other problems:

=== "macOS / Linux"

    ```bash
    echo $ANTHROPIC_API_KEY
    ```

=== "Windows (PowerShell)"

    ```powershell
    echo $env:ANTHROPIC_API_KEY
    ```

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

PowerShell words the first three differently from bash. `command not found: x`
and `The term 'x' is not recognized...` are the same error.

| What you see | What it means |
|:---|:---|
| `command not found: git`<br>`The term 'git' is not recognized` | Git is not installed, or the terminal predates the install — see [Install Git](#install-git) and open a new window |
| `*** Please tell me who you are` | Git has no name and email yet. See [Tell Git who you are](#tell-git-who-you-are) |
| `Authentication failed` / `could not read Username` on push | GitHub does not accept passwords. Run `gh auth login` — see [Install the GitHub CLI](#install-the-github-cli-and-sign-in) |
| `Support for password authentication was removed` | Same thing, said differently. `gh auth login` |
| `Permission denied` / `403` on push | You are signed in as the wrong account, or pushing to my repository rather than your copy. Check `git remote -v` names *your* username |
| `repository not found` on clone | The URL has a typo, or the repository is private and you are not signed in |
| `command not found: claude`<br>`The term 'claude' is not recognized` | Claude Code is not installed, or the terminal needs restarting after install |
| `command not found: python3`<br>`The term 'python3' is not recognized` | On Windows the command is `python`, not `python3`. Otherwise: Python not installed, or not on PATH — reinstall and tick the box |
| `running scripts is disabled on this system` | Windows only. PowerShell is blocking the venv activate script — see [A virtual environment](#a-virtual-environment) |
| `ModuleNotFoundError: No module named 'anthropic'` | Virtual environment not active, or `pip install anthropic` not run |
| `AuthenticationError` | `ANTHROPIC_API_KEY` is not set in this terminal. Setting it in another window does not count |
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
