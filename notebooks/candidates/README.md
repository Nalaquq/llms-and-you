# Candidate notebooks

Notebooks being evaluated, not yet taught. Nothing in this directory is wired to
a session: `notebooks.py` globs `notebooks/*.ipynb` and does not recurse, so a
file in here is invisible to the loader, to the site, and to
`test_every_notebook_belongs_to_a_session`. That is the point — a candidate can
sit alongside the notebook it might replace without either one pretending to be
the other.

To promote one: move it to `notebooks/`, point the session's `notebook` field at
its stem, flip `metadata.course.status` to `complete`, and run `pytest`.

Open a candidate in Colab by pasting its GitHub path into
<https://colab.research.google.com/github/Nalaquq/llms-and-you>, or by editing
a normal notebook's Colab URL to include `candidates/`.

---

## `w03-thu-english.ipynb`

An English-only alternative to `w03-thu.ipynb`, written because the German one
asks students to read a language they do not have. The German lab depends on
knowing German twice over: the cross-attention section turns on German putting
the verb at the end of a clause, and the closing section turns on German
pronouns carrying a gender, which is what forces the model to commit to a
referent.

| | `w03-thu.ipynb` (taught) | `w03-thu-english.ipynb` (candidate) |
|:---|:---|:---|
| Model | opus-mt-en-de, 74M | flan-t5-base, 248M |
| Task | English to German | English question answering |
| Download | ~300 MB | ~1 GB |
| Encoder / decoder layers | 6 / 6, 8 heads | 12 / 12, 12 heads |
| All three attention types | yes | yes |
| Needs German | yes | no |

Both are encoder-decoder models, which is the reason for either choice: an
encoder-only model like BERT shows one of the paper's three attention blocks and
a decoder-only model like GPT-2 shows one.

**What the English version does differently.** The German notebook ends on a
model that gets a Winograd sentence wrong while its attention points nowhere
useful. The English one ends on a control experiment instead, which is a sharper
version of the same lesson:

- The model answers *both* halves of the pair correctly, in English the student
  can read: "The trophy" and then "the suitcase".
- Scoring all 144 encoder heads turns up several whose `it` row peaks on a noun,
  the strongest at 0.85 on `trophy`. It looks exactly like a coreference head.
- Changing one word so the referent flips leaves that head still pointing at
  `trophy`, in the sentence where the model correctly answers `suitcase`.

So the student finds a convincing explanation and then watches it fail a control
they ran themselves. That is a better ending than "the model got it wrong", and
it needs no German.

**The cost, if this replaces the taught notebook.** The Week 3 deck quotes
numbers measured from opus-mt and tells students they reproduce in this lab —
the coreference head at 0.87, the alignment head at layer 3 head 4, and the
cross-attention weights of 0.58 and 0.61 on slide 27. Those are opus-mt facts.
Switching the lab means re-measuring them against flan-t5-base and re-rendering
three slides, or accepting that Tuesday and Thursday no longer show the same
model.

**Status.** Draft. Every code cell has been run end to end on CPU and the prose
matches what came out, but it has not been opened in Colab, and the numbers it
describes are from one machine on one library version.
