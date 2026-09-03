# Setting up your tools

We do all of this together in class. This page is the reference and the
fallback, not homework.

!!! success "No programming experience required"

    That is not a formality. This course assumes you have never installed
    Python and never opened a terminal.

    If something here does not work on your machine, that is normal and it is
    my problem to solve, not yours. Email me or come to office hours.

## The short version

**You need a browser and two free accounts.** That is the whole requirement for
the entire semester.

| | |
|:---|:---|
| **Week 1, Thursday** | [A GitHub account and your project repository](#week-1-your-repository-in-the-browser) — all in the browser |
| **Week 2, Thursday** | [Notebooks in Colab](#week-2-notebooks-in-your-browser) — a Google login, nothing installed |

Everything below those two sections is **optional**. Installing Python, Git, and
a local editor is genuinely worth doing if you are interested, and it is better
once you are past the first month — but nothing this semester requires it, and
choosing not to costs you no marks.

!!! info "Commands come in two flavours — pick your platform once"

    Where this page does show a terminal command, it is given twice: **macOS /
    Linux** for the Unix shells (bash and zsh), and **Windows (PowerShell)** for
    the terminal that opens by default on Windows.

    Pick your platform once and the rest of the site follows you.
    **Both tabs are always there**, including where the two halves are
    character-for-character the same. You should never have to work out whether
    a command applies to you.

---

## Week 1: Your repository, in the browser { #week-1-your-repository-in-the-browser }

By the end of this lab you have a GitHub account, your own copy of the project
template, and one commit in it. No installs, no terminal.

### A GitHub account

**[github.com](https://github.com/)** — free. Pick a username you would be
willing to put on a CV; this account will outlive the course.

Use an email address you will still have after you graduate.

!!! warning "Your email address will be public"

    Every commit carries the address on your account, permanently and visibly.
    If you would rather not publish yours, GitHub gives you a private one —
    **Settings → Emails → *Keep my email address private*** — which looks like
    `12345678+username@users.noreply.github.com`. Turn that on now, before your
    first commit, and GitHub uses it automatically.

If you want the concepts written down rather than demonstrated,
[Hello World](https://docs.github.com/en/get-started/using-github/hello-world)
covers repositories, branches, and commits in about twenty minutes.

### Your own copy of the project template { #your-own-copy-of-the-project-template }

Open [the project
template](https://github.com/Nalaquq/llms-and-you-project) and press the green
**Use this template** button, then **Create a new repository**.

Name it whatever you like. Set it **Public**. Press **Create repository**.

That is it — you now have a repository on your own account, with a clean history
that starts at your first commit.

!!! question "Why not fork it?"

    A fork stays tied to mine. GitHub presents it as a contribution to my
    project rather than a project of your own, it carries my entire history, and
    it behaves oddly when you later want to change its structure.

    A template copy is a genuine start. It is yours in every sense that matters,
    and nothing about it points back at me.

### What is in the folder

You did not build this layout, so none of it is obvious. We walk it together in
class; this is the version to come back to.

| Path | What it is for |
|:---|:---|
| `TODO.txt` | What the next version of your prompt needs to do |
| `PROMPTING.md` | The practices this course grades. Read this one first |
| `prompts/` | Your prompts, as versioned files — one file per prompt |
| `src/project/` | Your code, when you get to it |
| `evals/` | Your test set. Started in week one, not the week before it is due |
| `docs/adr/` | Your decision log — why you chose things. Graded |
| `CHANGELOG.md` | What changed and when. Graded alongside the ADRs |
| `tests/` | Ordinary tests, for the parts that are ordinary code |

`TODO.txt` is the one to start using today. It is a running list of what the
next draft of your prompt has to do, in sections by where each item ends up —
in the prompt itself, in `evals/`, in an ADR, or in a question for me. Write the
line the moment you have the thought. An hour later you no longer have it.

### Editing and committing in the browser { #editing-and-committing-in-the-browser }

This is the whole Git workflow, and every part of it is a button.

1. Click the file you want to change — say `docs/adr/ADR-001.md`.
2. Press the **pencil icon** at the top right of the file view.
3. Type.
4. Scroll to the bottom. Put a real sentence in the **commit message** box.
5. Press **Commit changes**.

You have just made a commit: a saved, dated, described version of your work that
you can return to and that nobody can quietly overwrite.

**That button does exactly what `git commit` does.** People who use the terminal
are not doing something more real than you; they are doing the same thing with
fewer clicks and more options. Nothing in this course needs the extra options.

!!! tip "Write commit messages you would want to read in November"

    `Update ADR-001.md` tells you nothing. `ADR-001: chose a public repo, noted
    the privacy trade-off` tells you what happened.

    This costs eight seconds and is the difference between a decision log that is
    useful in December and one that is archaeology. It is also graded.

### The decisions you just made without noticing

What you named the repository. Whether you made it public. Whether you turned on
the private email address. Whether you are going to work in the browser or set
up a local toolchain later.

None of those felt like decisions at the time, which is exactly why they are good
practice material. **ADR-001** asks you to write one of them up properly —
context, decision, alternatives, consequences — and what is graded is whether
your alternatives section contains a real alternative.

See [Writing Architectural Decision Records](writing-adrs.md).

---

## Week 2: Notebooks in your browser { #week-2-notebooks-in-your-browser }

Every Thursday lab from Week 2 onward is a **notebook** — Python you run a cell
at a time, with the output right underneath it. They run in Google Colab, on
Google's machines, from a browser tab.

**You need a Google account. Nothing else.** No Python, no terminal, no
installs, no payment. The session page for each lab has a button that opens that
week's notebook directly.

[:material-compass-outline: **Working in Google Colab**](colab.md) covers running
cells, saving your own copy, what to do when the runtime forgets everything, and
the errors you will actually hit. Read it once, in Week 2.

!!! success "You do not have to write code"

    Pasting a cell into a chatbot and asking what it does — or what an error
    means — is a legitimate way to work through these notebooks, and it is
    explicitly allowed. See [that section of the Colab
    guide](colab.md#you-do-not-have-to-write-code) for where the line is.

---

## Week 2: Python on your own machine — optional { #week-2-python-on-your-own-machine-optional }

Everything below here is for people who want it. **Skip this section entirely
and you will not miss a single graded thing.**

It is worth doing if you want your work to outlive a browser tab, if you want to
use an editor properly, or if you are considering more programming after this
course. Come to office hours and I will sit with you while you do it.

### Install Python

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

Install **[Visual Studio Code](https://code.visualstudio.com/)**, then add the
**Python extension**: Extensions panel, ++ctrl+shift+x++, search "Python",
install the Microsoft one.

VS Code opens `.ipynb` notebooks natively, so a course notebook downloaded from
GitHub works there the same way it does in Colab.

You do not need to know VS Code well. We use a small fraction of it.

### A virtual environment

Keeps this course's packages separate from anything else on your machine:

=== "macOS / Linux"

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

=== "Windows (PowerShell)"

    ```powershell
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    ```

When it is active your prompt starts with `(.venv)`. If you close the terminal,
activate it again — forgetting this is the single most common source of "it
worked yesterday".

!!! warning "Windows: `running scripts is disabled on this system`"

    PowerShell blocks scripts by default, and the activate script is one. Run
    this once, in the same window, then activate again:

    ```powershell
    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
    ```

    `CurrentUser` matters — it changes the policy for your account only, not
    the machine.

### Running a course notebook locally

Download the notebook from the link on the session page, then install what it
uses and open it:

=== "macOS / Linux"

    ```bash
    pip install jupyterlab scikit-learn pandas matplotlib gensim transformers nltk
    jupyter lab
    ```

=== "Windows (PowerShell)"

    ```powershell
    pip install jupyterlab scikit-learn pandas matplotlib gensim transformers nltk
    jupyter lab
    ```

The notebooks are written so the same cells run in both places. The only
difference is the `%pip install` cell at the top, which you can skip locally
because you just did it by hand.

!!! tip "If a library refuses to install"

    `gensim` in particular needs a Python version it has a prebuilt package for,
    and the newest Python is often too new. If it fails, use Python 3.12 — or
    just use Colab for that notebook, which is what Colab is for.

---

## The command-line route — optional { #the-command-line-route-optional }

Also optional, also genuinely worth learning, and also not required at any point
this semester.

The browser workflow in Week 1 does everything this course asks for. This route
gets you branching, history, offline work, and the ability to run things across
many files at once — which starts to matter around the time your project gets
real.

### Install Git

Git runs on your machine; GitHub is the website that stores a copy. They are
different things and you need both.

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
    it and wait; it is a few minutes.

=== "Windows (PowerShell)"

    ```powershell
    winget install --id Git.Git -e --source winget
    ```

    Then **close PowerShell and open a new window.** The installer adds Git to
    your PATH, and a window opened before that happened will not see it.

    If `winget` is not recognised, download the installer from
    [git-scm.com/download/win](https://git-scm.com/download/win) and accept
    every default.

### Tell Git who you are

Git stamps every commit with a name and an email, and refuses to commit until
you have set them. Once per machine, not once per project. Use the email on your
GitHub account — or the private forwarding address, if you turned that on.

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

### Install the GitHub CLI — `gh` — and sign in { #install-the-github-cli-and-sign-in }

GitHub stopped accepting passwords for pushing in 2021. `gh` handles the
credential so you do not have to make an access token by hand.

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
authenticate Git with your GitHub credentials. That last answer is what makes
`git push` work later without asking for anything.

### Clone the repository you already made { #clone-it }

You made it in Week 1 through the browser. This brings it down to your machine:

=== "macOS / Linux"

    ```bash
    gh repo clone YOUR-USERNAME/YOUR-PROJECT
    cd YOUR-PROJECT
    git config core.hooksPath .githooks
    ```

=== "Windows (PowerShell)"

    ```powershell
    gh repo clone YOUR-USERNAME/YOUR-PROJECT
    cd YOUR-PROJECT
    git config core.hooksPath .githooks
    ```

Run it from wherever you want the folder to live — your Desktop is fine,
Downloads is not.

That last line turns on the **credential guard**: it refuses any commit
containing something shaped like an API key. Once per clone, and worth it.

### Claude Code — optional, and not required by anything

**[claude.com/claude-code](https://claude.com/claude-code)** — install
instructions in the [setup
docs](https://docs.claude.com/en/docs/claude-code/setup).

This is a model in your terminal that **can see and change files in a folder**,
which a chat window cannot. Some of you will like it a great deal. It is not
used in any lab and no assignment assumes it.

Start it inside your clone:

=== "macOS / Linux"

    ```bash
    claude
    ```

=== "Windows (PowerShell)"

    ```powershell
    claude
    ```

Then talk to it:

```
what is in this repository, and what is each folder for?
```

---

## Model access

The college pays for model access. Use that rather than a personal subscription.

| For | Use | Cost to you |
|:---|:---|:---|
| Everyday chat, and working through a notebook | [Microsoft Co-Pilot](https://m365.cloud.microsoft/) · [BoodleBox](https://boodlebox.ai/) | Free — provided by the college |
| The Week 2–3 notebooks | Nothing. scikit-learn, gensim and Hugging Face tokenizers run locally and anonymously | Free |
| A few later labs, and your project | An **API key** | Arranged at the start of term |

**Do not buy credits on your own before we have talked.** Access is handled for
you, and paying for it yourself is both unnecessary and hard to reverse.

!!! warning "Never put an API key in a notebook cell"

    A notebook is a file you will share, publish, and screenshot. A key in a cell
    is a key in all three, and a key pushed to GitHub is scraped within minutes.
    This is not hypothetical — it is the most common way students lose access.

    In Colab, keys go in the **🔑 panel** in the left sidebar. See
    [API keys in the Colab guide](colab.md#api-keys).

If you are running locally, use an environment variable instead. This is the one
place where the two platforms look nothing alike:

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

---

## When something breaks

Errors are information, not failure.

**In a notebook**, the common ones and what they mean are in the [Colab
guide](colab.md#when-something-breaks). Nine times in ten the answer is
**Runtime → Run all**.

**Everywhere else:**

PowerShell words the first few differently from bash. `command not found: x`
and `The term 'x' is not recognized...` are the same error.

| What you see | What it means |
|:---|:---|
| The **Use this template** button is missing | You are not signed in to GitHub, or you are looking at a fork rather than the template |
| Your edit on github.com did not save | You did not press **Commit changes** at the bottom of the page |
| `command not found: git`<br>`The term 'git' is not recognized` | Git is not installed, or the terminal predates the install — see [Install Git](#install-git) and open a new window |
| `*** Please tell me who you are` | Git has no name and email yet. See [Tell Git who you are](#tell-git-who-you-are) |
| `Authentication failed` / `could not read Username` on push | GitHub does not accept passwords. Run `gh auth login` — see [Install the GitHub CLI](#install-the-github-cli-and-sign-in) |
| `Permission denied` / `403` on push | Signed in as the wrong account, or pushing to my repository rather than your copy. Check `git remote -v` names *your* username |
| `repository not found` on clone | The URL has a typo, or the repository is private and you are not signed in |
| `command not found: python3`<br>`The term 'python3' is not recognized` | On Windows the command is `python`, not `python3`. Otherwise: not installed, or not on PATH — reinstall and tick the box |
| `running scripts is disabled on this system` | Windows only. PowerShell is blocking the venv activate script — see [A virtual environment](#a-virtual-environment) |
| `ModuleNotFoundError` | Virtual environment not active, or the package is not installed in it |
| `AuthenticationError` | The API key is not set in this terminal. Setting it in another window does not count |
| `RateLimitError` (429) | Too many requests too fast. Wait and retry — handled properly in Week 13 |

Bring the **exact error text** to class or office hours. "It didn't work" is
hard to help with; a pasted traceback is usually solved in under a minute.

---

## A note on following tutorials

There is a great deal of tutorial material online, and much of it is out of date
in ways that will not be obvious to you.

The clearest example, which you meet in the Week 4 lab: nearly every prompt
engineering tutorial tells you to adjust `temperature` to control randomness. On
current frontier models that parameter has been **removed** — sending it returns
an error — and replaced by an `effort` setting. The tutorials have not caught up.

The same thing happens in the libraries you will use here. Most word2vec
tutorials online are written against gensim 3, whose API changed in gensim 4:
`model.wv.vocab` became `model.wv.key_to_index`, and `size=` became
`vector_size=`. Code copied from a 2019 blog post fails with an error that
does not explain itself.

When sources contradict, the official documentation wins —
[scikit-learn](https://scikit-learn.org/stable/),
[gensim](https://radimrehurek.com/gensim/),
[Hugging Face](https://huggingface.co/docs), or the
[API reference](https://docs.claude.com/en/api/overview). Worth internalising
early: in a field moving this fast, knowing *where the authoritative answer
lives* is more durable than knowing the answer.
