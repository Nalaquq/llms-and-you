"""Week 3 discussion interstitials — one after each part of the model.

  w03_s13_discuss_idea.gif      after the idea, before the mechanism
  w03_s18_discuss_head.gif      after one head, end to end
  w03_s21_discuss_heads.gif     after multi-head and position
  w03_s24_discuss_bridge.gif    after the mask and cross-attention
  w03_s29_discuss_limits.gif    after "attention is not an explanation"

Questions only. No hints on the slide and no answer at the bottom: what the
instructor is fishing for lives in the speaker notes, where the room cannot
read it and be steered by it.

Every set asks the same underlying thing in a different place -- how is this
different from what we did before the break? The review is still on the board
behind them, and a student with no technical background can answer all fifteen
of these from what they have watched today.
"""

from style_dark import (
    PANEL,
    PURPLE,
    SUB,
    TEXT,
    YELLOW,
    blank_axes,
    chip,
    fig_to_pil,
    footer,
    hold,
    new_fig,
    save_gif,
)

DISCUSSIONS = [
    (
        "w03_s13_discuss_idea.gif",
        "Before we open it up",
        "You have seen what attention is for. Not yet how it works.",
        [
            "Every method we reviewed had a reach: a window three words wide,\n"
            "or a memory that faded. What kind of sentence breaks both of them?",
            "If a word can look at any other word for free, what should decide\nwhere it looks?",
            "When you read a long sentence, do you go strictly left to right —\n"
            "or do you jump back? Which of this morning's methods reads like you?",
        ],
        "study guide: recurrent-neural-network · sliding-window",
    ),
    (
        "w03_s18_discuss_head.gif",
        "One head, all the way through",
        "A question, a set of labels, a score, a share, a blend.",
        [
            "word2vec gave every word one meaning for life. This gives 'it' a\n"
            "different meaning in every sentence. What can you do now that you\n"
            "could not do before the break?",
            "Nobody told the model that 'it' meant the animal. So where did\nthat come from?",
            "Has it understood the sentence — or done something that only looks\n"
            "like understanding from outside?",
        ],
        "study guide: static-vs-contextual-embeddings · polysemy",
    ),
    (
        "w03_s21_discuss_heads.gif",
        "Eight opinions, and word order again",
        "Two choices in the design that could have gone another way.",
        [
            "Eight heads read the same sentence and do different things. Is that\n"
            "a strength, or a sign that nobody quite knows what a head is for?",
            "Bag of words lost word order and it cost us everything. Attention\n"
            "lost it again — and it was handed back as an extra ingredient.\n"
            "Is that a fix, or a patch?",
            "How would you explain to a friend why 'dog bites man' and 'man bites\n"
            "dog' are hard for a computer to tell apart?",
        ],
        "study guide: bag-of-words · parameters-and-weights",
    ),
    (
        "w03_s24_discuss_bridge.gif",
        "Reading, writing, and the bridge",
        "The encoder reads all at once. The decoder writes one word at a time.",
        [
            "In the RNN, a word nine steps back had to survive nine hand-offs,\n"
            "and usually did not. Here 'gekauft' reached 'bought' in one step.\n"
            "Distance is free now — so what is the transformer paying instead?",
            "It reads the whole sentence at once but still writes one word at a\n"
            "time. Have we solved the old problem, or only half of it?",
            "Why should reading and writing get different rules at all?",
        ],
        "study guide: encoder-and-decoder · sequence-to-sequence",
    ),
    (
        "w03_s29_discuss_limits.gif",
        "So what did we actually see?",
        "Last stop before Thursday.",
        [
            "It chose what 'it' meant, got it wrong, and its attention showed no\n"
            "sign of the choice. What would count as showing you the reason?",
            "Attention pictures get used to argue that a model is fair, or safe.\n"
            "After today, how much would you trust one?",
            "Everything from this morning is still in here somewhere — counting,\n"
            "embeddings, layers. What is genuinely new, and what is old ideas\n"
            "wired together differently?",
        ],
        "study guide: static-vs-contextual-embeddings",
    ),
]


def make(name, title, subtitle, questions, sg):
    def render(n_q):
        fig = new_fig()
        fig.text(
            0.045,
            0.945,
            "DISCUSS · PAUSE HERE",
            fontsize=13,
            color=PURPLE,
            fontweight="bold",
            va="top",
        )
        fig.text(0.045, 0.895, title, fontsize=30, color=TEXT, fontweight="bold", va="top")
        fig.text(0.045, 0.838, subtitle, fontsize=15.5, color=SUB, va="top")
        ax = blank_axes(fig, [0.05, 0.09, 0.90, 0.71])
        ax.plot(
            [0.012, 0.012],
            [0.05, 0.97],
            color=PURPLE,
            lw=3,
            alpha=0.6,
            transform=ax.transAxes,
        )

        # Three questions, evenly spread over the whole panel. With the hints
        # gone there is room to set them large enough to read from the back.
        # Both the number and the text hang from the top of their slot, so a
        # three-line question does not push its own number down past line two.
        top, bottom = 0.90, 0.30
        step = (top - bottom) / max(len(questions) - 1, 1)
        for i, q in enumerate(questions[:n_q]):
            y = top - i * step
            chip(
                ax,
                0.045,
                y - 0.10,
                0.052,
                0.10,
                f"{i + 1}",
                fontsize=16,
                mono=True,
                face=PANEL,
                edge=YELLOW,
                color=YELLOW,
                lw=2.0,
                bold=True,
            )
            ax.text(
                0.135,
                y,
                q,
                fontsize=17,
                color=TEXT,
                va="top",
                linespacing=1.55,
            )

        footer(fig, sg)
        return fig_to_pil(fig)

    frames, durations = [], []
    for n in range(1, len(questions) + 1):
        hold(frames, durations, lambda n=n: render(n), ms=1200)
    hold(frames, durations, lambda: render(len(questions)), ms=1800, n=2)
    save_gif(frames, durations, name)


if __name__ == "__main__":
    for spec in DISCUSSIONS:
        make(*spec)
