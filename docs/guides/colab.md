# Working in Google Colab

Every Thursday notebook opens in Colab: Python running on Google's machines,
driven from a browser tab. Nothing is installed on your laptop, nothing costs
anything, and it works the same on Windows, macOS, a Chromebook, and a library
computer.

!!! success "What you need"

    A Google account. That is the whole list.

    If you would rather run the notebooks on your own machine, you can — see
    [Python on your own machine](setup.md#week-2-python-on-your-own-machine-optional).
    It is an option, not the path, and nothing this semester requires it.

---

## Opening a notebook { #opening-a-notebook }

Every lab session page has a button that opens that week's notebook directly.
Press it. Colab will ask you to sign in to Google, then the notebook appears.

The first time, you will see a warning that the notebook was not authored by
Google. That is expected — it is telling you the file came from GitHub, which is
where I put it. **Run anyway.**

---

## Running cells { #running-cells }

A notebook is a column of **cells**. Grey cells are code; the rest is writing.

| | |
|:---|:---|
| Run the cell you are in | ++shift+enter++ |
| Run everything, top to bottom | **Runtime → Run all** |
| Stop something that is taking too long | the ⏹ square, or **Runtime → Interrupt** |

**Order matters.** A cell that uses `corpus` fails if you have not run the cell
that defines `corpus`. This is the single most common confusion: a notebook is
not a document you read top to bottom, it is a machine with a memory, and that
memory only contains what you have actually run.

If things stop making sense, **Runtime → Restart session and run all** puts you
back at a known state. Do it early rather than debugging a mystery.

---

## Make your own copy before you change anything { #make-your-own-copy }

Opening a notebook from GitHub gives you a **read-only view**. You can run it and
edit it in the tab, but your changes go nowhere and are gone when you close it.

Since the point of these notebooks is changing things, save a copy first:

**File → Save a copy in Drive**

That puts a private copy in your own Google Drive, which is where your work
should live. The tab switches to your copy automatically. Do this before you
start exploring, not after you have spent an hour on something good.

!!! warning "The runtime forgets everything"

    Close the tab, or leave it idle for a while, and Google reclaims the machine.
    Your **code** is saved in Drive; the **variables and installed packages are
    not**, along with any file the notebook downloaded.

    So when you come back tomorrow, run the setup cell again. Nothing is broken —
    this is how Colab works, and it is the price of not installing anything.

---

## Downloading a file you made { #downloading-a-file }

Charts, tables, and anything you saved live on Google's machine, not yours. The
folder icon in the left sidebar shows them; the ⋮ next to a file downloads it.

To get a plot out for a slide, right-click the image in the output and **Save
image as**. That is usually all anybody needs.

---

## The free GPU { #the-free-gpu }

**Runtime → Change runtime type → T4 GPU**, then **Save**.

You do not need this before Week 13, and turning it on for a notebook that does
not use one just makes the session shorter — Google limits free GPU time and
takes it back when you are idle. Leave it off until a notebook says otherwise.

---

## API keys, when a notebook needs one { #api-keys }

Most notebooks in this course need no key at all: scikit-learn, gensim and
Hugging Face tokenizers all run locally on the Colab machine, free and
anonymously. A few later labs talk to a commercial model, and those need a key.

**Never paste a key into a cell.** A notebook is a file you will share, publish,
and screenshot, and a key in a cell is a key in all three.

Colab has a place for them: the **🔑 key icon** in the left sidebar. Add the key
there once, name it, and switch on *Notebook access*. Then the notebook reads it
without it ever appearing in the file:

```python
from google.colab import userdata

api_key = userdata.get("ANTHROPIC_API_KEY")
```

The secret belongs to your Google account, not to the notebook, so it survives
being copied and does not travel when you share the file.

---

## You do not have to write code { #you-do-not-have-to-write-code }

This is a course about language models, and using one to work through a notebook
is using the tool the course is about. It is explicitly allowed here.

Things that are fine, and that I would rather you did than stall:

- Pasting a cell into [BoodleBox](https://boodlebox.ai/) or
  [Co-Pilot](https://m365.cloud.microsoft/) and asking what it does
- Pasting an **error message** in and asking what it means — do this, errors are
  not shameful and reading them is a skill
- Asking for the code to answer a question the notebook raised but did not answer
- Asking it to explain an output you do not believe

The one thing that does not work is pasting a cell in, getting an answer, and
bringing that answer to Thursday as a finding. You have to have run something.
The difference is visible immediately and it is the whole point of the session.

!!! info "Where the line is"

    Reading responses and the Burchell reflections are **no-AI work** — see the
    [AI policy](../syllabus.md#using-ai). Lab notebooks are not: use whatever
    helps, and say what you used when you show it. Citing a model you leaned on
    is normal practice here, not a confession.

---

## When something breaks { #when-something-breaks }

| What you see | What it means |
|:---|:---|
| `NameError: name 'corpus' is not defined` | You skipped a cell above. **Runtime → Run all** |
| `ModuleNotFoundError` | The setup cell has not run in this session. Run it |
| A numpy or gensim error on import | **Runtime → Restart session**, then run the setup cell again. Common and not your fault |
| Cell has been running for minutes | Downloading a model, probably. Give it two minutes; then **Runtime → Interrupt** |
| "Notebook was not authored by Google" | Expected. It came from GitHub. Run anyway |
| Your edits vanished | You were in the read-only view. **File → Save a copy in Drive** first |
| `RuntimeError: cannot connect to GPU` | Free GPU quota is used up. Switch back to CPU; nothing before Week 13 needs one |

Still stuck? Bring the **exact error text** — screenshot the whole cell, not just
the last line. Email me or come to office hours, and if a notebook is broken for
you it is probably broken for other people, so telling me is a favour.
