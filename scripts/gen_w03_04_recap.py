"""Week 3 review, closing slide: the ladder, and the three problems left on it.

  w03_s11_recap.gif

Week 2 ended on a ladder of representations; this one carries the
architectures up it too, and lands on the three requirements the transformer
paper is an answer to. It is the last slide of the review -- the deck's
transformer half begins after it, so this slide asks the question and
deliberately does not answer it.
"""

from matplotlib.patches import FancyBboxPatch
from style_dark import (
    BLUE,
    FAINT,
    GREEN,
    PANEL,
    PANEL_EDGE,
    PURPLE,
    RED,
    TEXT,
    YELLOW,
    blank_axes,
    fig_to_pil,
    footer,
    hold,
    math_strip,
    new_fig,
    save_gif,
)

# Each rung fixed the one below it and broke something new. That rhythm is the
# argument of the whole review, so it is the only thing on the closing slide.
LADDER = [
    ("binary vectorization", "words became numbers", "no similarity, at all"),
    ("bag of words", "documents became comparable", "word order gone entirely"),
    ("TF-IDF", "common words stopped shouting", "still no meaning, only counts"),
    ("word2vec", "meaning, learned and graded", "one vector per word, forever"),
    ("CNN", "local phrases, learned not listed", "a window three words wide"),
    ("RNN", "order and memory, any length", "sequential, and the start fades"),
]

REQUIREMENTS = [
    "A word's meaning has to come from its whole sentence — not from a fixed window.",
    "Any word must be able to look at any other word, however far away it is.",
    "And it has to be parallel, or we cannot train it on anything the size of the internet.",
]


def make_recap():
    def render(n_rows, n_reqs, closer):
        fig = new_fig()
        fig.text(
            0.045,
            0.945,
            "REVIEW · WHERE THAT LEAVES US",
            fontsize=13,
            color=PURPLE,
            fontweight="bold",
            va="top",
        )
        fig.text(
            0.045,
            0.895,
            "Every rung fixed the last one, and broke something new",
            fontsize=30,
            color=TEXT,
            fontweight="bold",
            va="top",
        )
        ax = blank_axes(fig, [0.045, 0.215, 0.91, 0.615])

        ax.text(
            0.0, 0.985, "the technique", fontsize=10.5, color=FAINT, fontweight="bold", va="top"
        )
        ax.text(
            0.235, 0.985, "what it fixed", fontsize=10.5, color=GREEN, fontweight="bold", va="top"
        )
        ax.text(
            0.60,
            0.985,
            "what it could not do",
            fontsize=10.5,
            color=RED,
            fontweight="bold",
            va="top",
        )

        for i, (name, fixed, broke) in enumerate(LADDER[:n_rows]):
            y = 0.90 - i * 0.078
            ax.text(0.0, y, name, fontsize=13, color=TEXT, va="center", fontfamily="monospace")
            ax.text(0.235, y, fixed, fontsize=13, color=GREEN, va="center", alpha=0.9)
            ax.text(0.60, y, broke, fontsize=13, color=RED, va="center", alpha=0.9)

        if n_reqs:
            box = FancyBboxPatch(
                (-0.012, 0.055),
                1.024,
                0.34,
                boxstyle="round,pad=0.012,rounding_size=0.03",
                facecolor=PANEL,
                edgecolor=PANEL_EDGE,
                linewidth=1.6,
                transform=ax.transAxes,
            )
            ax.add_patch(box)
            ax.text(
                0.015,
                0.355,
                "SO WHAT WOULD ACTUALLY WORK?",
                fontsize=10.5,
                color=FAINT,
                fontweight="bold",
                va="top",
            )
            for i, req in enumerate(REQUIREMENTS[:n_reqs]):
                y = 0.265 - i * 0.078
                ax.text(
                    0.015, y, f"{i + 1}", fontsize=13, color=BLUE, fontweight="bold", va="center"
                )
                ax.text(0.055, y, req, fontsize=13.5, color=TEXT, va="center")

        if closer:
            ax.text(
                0.0,
                -0.022,
                "One idea, published in 2017, does all three at once. That is the rest of today.",
                fontsize=14.5,
                color=YELLOW,
                va="center",
                style="italic",
            )

        math_strip(
            fig,
            r"$\mathrm{Attention}(Q, K, V) \;=\; \; ?$",
            note="the paper you read for today",
        )
        footer(
            fig,
            "study guide: static-vs-contextual-embeddings · sequence-to-sequence · "
            "fixed-length-bottleneck",
        )
        return fig_to_pil(fig)

    frames, durations = [], []
    for n in range(1, len(LADDER) + 1):
        hold(frames, durations, lambda n=n: render(n, 0, False), ms=520)
    for r in range(1, len(REQUIREMENTS) + 1):
        hold(frames, durations, lambda r=r: render(len(LADDER), r, False), ms=1000)
    hold(frames, durations, lambda: render(len(LADDER), len(REQUIREMENTS), True), ms=1400, n=2)
    save_gif(frames, durations, "w03_s11_recap.gif")


if __name__ == "__main__":
    make_recap()
