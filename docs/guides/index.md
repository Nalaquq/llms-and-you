# Guides

Practical references for working in this course. None of these are graded; all
of them are things students ask about.

<div class="grid cards" markdown>

-   :material-notebook-outline:{ .lg .middle } **[Working in Google Colab](colab.md)**

    ---

    Where every Thursday notebook runs, on a Google login and nothing else.
    Running cells, saving your own copy, why the runtime forgets everything
    overnight, and the errors you will actually hit. Also: why working through
    a notebook with a chatbot is allowed here, and where that line sits.

-   :material-console:{ .lg .middle } **[Setting up your tools](setup.md)**

    ---

    A GitHub account and your project repository in Week 1 — all in the browser,
    nothing installed. Then, entirely optionally, Python and a local toolchain
    for anyone who wants one. Assumes you have never opened a terminal and never
    asks you to.

-   :material-robot-outline:{ .lg .middle } **[Using BoodleBox to understand a reading](boodlebox.md)**

    ---

    The college pays for a platform with most of the frontier models behind one
    login. How to get an account, how to ask it about a paragraph that will not
    go in, how to check what it said — and exactly where the line is in this
    course.

-   :material-file-document-outline:{ .lg .middle } **[How to read a paper you cannot fully understand](reading-papers.md)**

    ---

    This course has no prerequisites and assigns research papers. Here is how
    those two facts coexist: a three-pass method, what to do at a wall, and
    what you are actually assessed on.

-   :material-clipboard-text-outline:{ .lg .middle } **[Writing Architectural Decision Records](writing-adrs.md)**

    ---

    The template, the four required ADRs and when they are due, and what
    separates a decision record from a note.

-   :material-source-repository:{ .lg .middle } **[The project template](https://github.com/Nalaquq/llms-and-you-project)**

    ---

    Where your semester project starts, and what you clone in the Week 1 lab.
    Prompts kept as versioned files, an evaluation set, both logs you are
    graded on, a running `TODO.txt`, and a hook that stops you committing an
    API key. `gh repo create --template` makes your copy — do not fork.

-   :material-account-clock-outline:{ .lg .middle } **[Individual meetings](conference-weeks.md)**

    ---

    Five sessions are individual 15-minute meetings rather than a group class.
    How to book your slot, what to bring to each one, and why both project
    milestones land there.

</div>

---

## Tools you will need

All free. The required ones need a browser and nothing else.

**Required — two free accounts, both in a browser:**

| Tool | Used for |
|:---|:---|
| [GitHub](https://github.com/) | Your account and your project repository. Set up Week 1, in the browser |
| [Google Colab](https://colab.research.google.com/) | Every Thursday notebook. A Google login; nothing installed |
| [Microsoft Co-Pilot](https://m365.cloud.microsoft/) · [BoodleBox](https://boodlebox.ai/) | College-provided chat access — use these, not a personal subscription |
| [HackAPrompt](https://www.hackaprompt.com/) | Red-teaming midterm, Weeks 8–9 |
| [Project template](https://github.com/Nalaquq/llms-and-you-project) | The starting point for your semester project |

**Used inside the notebooks.** Nothing to install — Colab has them, or the
setup cell adds them:

| Library | Used for |
|:---|:---|
| [scikit-learn](https://scikit-learn.org/stable/) | Bag of words, TF-IDF, cosine similarity, PCA. Week 2 onward |
| [Hugging Face](https://huggingface.co/docs) | Tokenizers, open-weight models, datasets, the `evaluate` library |
| [gensim](https://radimrehurek.com/gensim/) | word2vec — pretrained vectors, and training your own. Week 2 |
| [NLTK](https://www.nltk.org/) | Stemming and lemmatization. Week 2 |

**Optional, for anyone who wants a local toolchain.** None of this is graded and
no lab requires it:

| Tool | Used for |
|:---|:---|
| [Python](https://www.python.org/downloads/) + [VS Code](https://code.visualstudio.com/) | Running the notebooks on your own machine |
| [Git](https://git-scm.com/downloads) + [GitHub CLI](https://cli.github.com/) | The command-line route to the same repository |
| [Claude Code](https://claude.com/claude-code) · [desktop app](https://claude.ai/download) | A model that can read and edit a folder. Nothing assumes it |
| [Claude API](https://docs.claude.com/en/api/overview) | A few later labs and, if you want it, your project |

If cost is ever a barrier to any of these, tell me early. It is a solvable
problem and not one you should be quietly working around.
