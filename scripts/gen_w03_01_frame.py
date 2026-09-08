"""Week 3 opening: the deck's title, and the vocabulary the review needs.

  w03_s01_title.png      cold open — the sentence attention is famous for
  w03_s02_taxonomy.gif   model vs architecture vs technique

The taxonomy slide comes first on purpose. Everything in the twenty-minute
review that follows is one of those three things, and students who cannot
tell them apart hear "word2vec", "BERT" and "tokenization" as one
undifferentiated list of names.
"""

import numpy as np
from matplotlib.patches import FancyBboxPatch
from style_dark import (
    BLUE,
    FAINT,
    GREEN,
    PANEL,
    PURPLE,
    SUB,
    TEXT,
    YELLOW,
    blank_axes,
    fig_to_pil,
    footer,
    hold,
    math_strip,
    new_fig,
    save_gif,
    save_png,
)

# =====================================================================
# SLIDE 1 — PNG: title
# =====================================================================
SENTENCE = ["The", "animal", "didn't", "cross", "the", "street", "because", "it", "was", "tired"]


def make_title():
    fig = new_fig()
    ax = blank_axes(fig, [0.06, 0.30, 0.88, 0.34])

    # The sentence, laid out with the arcs that give the deck its name. Drawn
    # faint: this is a promise about the next 75 minutes, not a claim yet.
    xs = np.linspace(0.03, 0.97, len(SENTENCE))
    for x, word in zip(xs, SENTENCE, strict=True):
        lit = word in ("it", "animal")
        ax.text(
            x,
            0.30,
            word,
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=19,
            color=YELLOW if lit else SUB,
            fontweight="bold" if lit else "normal",
        )

    src = xs[SENTENCE.index("it")]
    for target, weight in (("animal", 1.0), ("street", 0.45), ("tired", 0.3)):
        dst = xs[SENTENCE.index(target)]
        t = np.linspace(0, 1, 120)
        x = src + (dst - src) * t
        y = 0.42 + 0.42 * np.sqrt(abs(dst - src)) * np.sin(np.pi * t)
        ax.plot(
            x,
            y,
            transform=ax.transAxes,
            color=BLUE,
            lw=1.0 + 3.0 * weight,
            alpha=0.20 + 0.55 * weight,
            solid_capstyle="round",
        )

    fig.text(0.06, 0.80, "WEEK 3 · TUESDAY", fontsize=13, color=PURPLE, fontweight="bold")
    fig.text(
        0.06, 0.715, "Attention and the Transformer", fontsize=44, color=TEXT, fontweight="bold"
    )
    fig.text(
        0.06,
        0.235,
        "Which word does 'it' mean? Every architecture before 2017 had to answer\n"
        "that by remembering, or by looking nearby. Neither worked well enough.",
        fontsize=16,
        color=SUB,
        va="top",
        linespacing=1.6,
    )
    fig.text(0.06, 0.10, "First: twenty minutes on how we got here.", fontsize=14, color=FAINT)
    save_png(fig, "w03_s01_title.png")


# =====================================================================
# SLIDE 2 — GIF: model vs architecture vs technique
# =====================================================================
COLUMNS = [
    (
        "ARCHITECTURE",
        BLUE,
        "The shape of the machine.",
        "What is wired to what, and\nin which order — written down\nbefore anything is trained.",
        ["perceptron", "CNN", "RNN", "transformer"],
    ),
    (
        "MODEL",
        GREEN,
        "An architecture, trained.",
        "The same wiring with every\nweight filled in by running "
        "a\ncorpus through it. Weights are\nthe whole difference.",
        ["word2vec", "BERT", "GPT-5", "Claude"],
    ),
    (
        "TECHNIQUE",
        YELLOW,
        "A way of using or preparing.",
        "A procedure with no weights\nof its own. It can be applied\nto any model, or to none.",
        ["tokenization", "TF-IDF", "few-shot", "RAG"],
    ),
]


def make_taxonomy():
    def render(n_cols, show_line):
        fig = new_fig()
        fig.text(
            0.045,
            0.945,
            "REVIEW · THE VOCABULARY",
            fontsize=13,
            color=PURPLE,
            fontweight="bold",
            va="top",
        )
        fig.text(
            0.045,
            0.895,
            "Three words that are not synonyms",
            fontsize=30,
            color=TEXT,
            fontweight="bold",
            va="top",
        )
        fig.text(
            0.045,
            0.838,
            "Everything in this review is exactly one of these. Say which, every time.",
            fontsize=15.5,
            color=SUB,
            va="top",
        )
        ax = blank_axes(fig, [0.045, 0.245, 0.91, 0.555])

        for i, (name, colour, tagline, body, examples) in enumerate(COLUMNS[:n_cols]):
            x = 0.02 + i * 0.335
            w = 0.30
            box = FancyBboxPatch(
                (x, 0.0),
                w,
                1.0,
                boxstyle="round,pad=0.012,rounding_size=0.04",
                facecolor=PANEL,
                edgecolor=colour,
                linewidth=1.8,
                alpha=0.95,
                transform=ax.transAxes,
            )
            ax.add_patch(box)
            ax.text(x + 0.03, 0.925, name, fontsize=15, color=colour, fontweight="bold", va="top")
            ax.text(
                x + 0.03, 0.845, tagline, fontsize=14.5, color=TEXT, va="top", fontweight="bold"
            )
            ax.text(x + 0.03, 0.745, body, fontsize=12.5, color=SUB, va="top", linespacing=1.5)
            ax.text(
                x + 0.03, 0.47, "for example", fontsize=10, color=FAINT, va="top", fontweight="bold"
            )
            for j, ex in enumerate(examples):
                ax.text(
                    x + 0.03,
                    0.385 - j * 0.082,
                    f"· {ex}",
                    fontsize=12.5,
                    color=TEXT,
                    va="top",
                    fontfamily="monospace",
                )

        if show_line:
            ax.text(
                0.5,
                -0.115,
                "A blueprint is not a house, and neither one is a way of living in it.",
                fontsize=15,
                color=YELLOW,
                ha="center",
                va="top",
                style="italic",
            )
        math_strip(
            fig,
            r"$\mathrm{model} \;=\; \mathrm{architecture} \;+\; \theta$",
            note="θ = the weights, learned from a corpus",
        )
        footer(fig, "study guide: parameters-and-weights · training-and-inference")
        return fig_to_pil(fig)

    frames, durations = [], []
    for n in (1, 2, 3):
        hold(frames, durations, lambda n=n: render(n, False), ms=1100)
    hold(frames, durations, lambda: render(3, True), ms=1200, n=2)
    save_gif(frames, durations, "w03_s02_taxonomy.gif")


if __name__ == "__main__":
    make_title()
    make_taxonomy()
