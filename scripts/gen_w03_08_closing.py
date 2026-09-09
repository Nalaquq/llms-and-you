"""Week 3, the transformer: why it won, what it does not do, and the ledger closed.

  w03_s26_parallel.gif   the reason it took over: everything at once
  w03_s27_not_expl.gif   attention weights are not explanations
  w03_s28_closing.gif    the three requirements from the review, ticked

s27 is measured, and it is the slide the Thursday lab is built to continue.
opus-mt-en-de really does translate both sentences with "sie", which is wrong
for the second one, and the cross-attention for that pronoun really does point
at "it" rather than at either noun. Reproduce in
notebooks/w03-thu-translation.ipynb, section 6.
"""

import numpy as np
from style_dark import (
    BLUE,
    FAINT,
    GREEN,
    PURPLE,
    RED,
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
)

WORDS = ["The", "animal", "didn't", "cross", "the", "street", "because", "it", "was"]


def frame(fig, kicker, title, subtitle=None):
    fig.text(0.045, 0.945, kicker, fontsize=13, color=PURPLE, fontweight="bold", va="top")
    fig.text(0.045, 0.895, title, fontsize=30, color=TEXT, fontweight="bold", va="top")
    if subtitle:
        fig.text(0.045, 0.838, subtitle, fontsize=15.5, color=SUB, va="top")


# =====================================================================
# SLIDE 26 — why it won
# =====================================================================
def make_parallel():
    def render(step, phase):
        fig = new_fig()
        frame(
            fig,
            "THE TRANSFORMER · WHY IT WON",
            "The reason it took over is not that it is cleverer",
            "It is that the whole sentence can be computed at the same time.",
        )
        ax = blank_axes(fig, [0.045, 0.195, 0.91, 0.60])
        xs = np.linspace(0.05, 0.95, len(WORDS))

        ax.text(
            0.0,
            0.93,
            "AN RNN — nine steps, in order",
            fontsize=12,
            color=RED,
            fontweight="bold",
            va="center",
        )
        for i, (x, w) in enumerate(zip(xs, WORDS, strict=True)):
            done = i <= step
            ax.text(
                x,
                0.79,
                w,
                ha="center",
                va="center",
                fontsize=12.5,
                color=TEXT if done else FAINT,
                fontweight="bold" if i == step else "normal",
            )
            ax.text(
                x,
                0.70,
                f"t{i + 1}" if done else "·",
                ha="center",
                va="center",
                fontsize=10,
                color=RED if done else FAINT,
            )

        if phase >= 1:
            ax.text(
                0.0,
                0.55,
                "A TRANSFORMER — one step, all nine at once",
                fontsize=12,
                color=GREEN,
                fontweight="bold",
                va="center",
            )
            for x, w in zip(xs, WORDS, strict=True):
                ax.text(
                    x,
                    0.41,
                    w,
                    ha="center",
                    va="center",
                    fontsize=12.5,
                    color=TEXT,
                    fontweight="bold",
                )
                ax.text(x, 0.32, "t1", ha="center", va="center", fontsize=10, color=GREEN)

        if phase >= 2:
            ax.text(
                0.0,
                0.17,
                "A GPU does thousands of things at once and nothing in order. The RNN was "
                "the wrong shape\nfor the hardware; this is the right shape.",
                fontsize=13.5,
                color=TEXT,
                va="center",
                linespacing=1.7,
            )
            ax.text(
                0.0,
                0.02,
                "That is what made training on the whole internet possible — and everything "
                "since is downstream of it.",
                fontsize=13.5,
                color=YELLOW,
                va="center",
            )

        math_strip(
            fig,
            r"$\mathrm{sequential\ operations:} \qquad \mathrm{RNN}\; O(n) "
            r"\qquad\qquad \mathrm{attention}\; O(1)$",
            note="Table 1 again — the column that mattered",
        )
        footer(fig, "study guide: recurrent-neural-network · training-and-inference")
        return fig_to_pil(fig)

    frames, durations = [], []
    for s in range(len(WORDS)):
        hold(frames, durations, lambda s=s: render(s, 0), ms=330)
    for p in (1, 2):
        hold(frames, durations, lambda p=p: render(len(WORDS) - 1, p), ms=1500)
    hold(frames, durations, lambda: render(len(WORDS) - 1, 2), ms=1200)
    save_gif(frames, durations, "w03_s26_parallel.gif")


# =====================================================================
# SLIDE 27 — attention is not an explanation
# =====================================================================
# The Winograd pair. English tokens, the German opus-mt-en-de writes for each,
# the noun a reader resolves "it" to, and where the model's cross-attention
# went when it wrote the pronoun (measured; w03-thu-translation.ipynb, section 6).
_EN = ["The", "trophy", "would", "not", "fit", "in", "the", "suitcase"]
_EN += ["because", "it", "was", "too"]
EN_A = [*_EN, "big"]
EN_B = [*_EN, "small"]
_DE = ["Die", "Trophäe", "passte", "nicht", "in", "den", "Koffer,", "weil", "sie", "zu"]
DE_A = [*_DE, "groß", "war."]
DE_B = [*_DE, "klein", "war."]
IT_EN, TROPHY, SUITCASE = 9, 1, 7
SIE = 8
CASES = [
    # english, german, noun 'it' means, weight sie->it, verdict lines, correct?
    (EN_A, DE_A, TROPHY, 0.58, True),
    (EN_B, DE_B, SUITCASE, 0.61, False),
]


def make_not_explanation():
    def render(phase):
        fig = new_fig()
        frame(
            fig,
            "THE TRANSFORMER · WHAT ATTENTION IS NOT",
            "An attention weight is not a reason",
            "German pronouns have a gender, so translating 'it' forces the model to decide "
            "which noun it means.",
        )
        ax = blank_axes(fig, [0.045, 0.195, 0.91, 0.60])

        for k, (en, de, noun, weight, correct) in enumerate(CASES):
            y_en = 0.84 - k * 0.44
            y_de = y_en - 0.18
            ex = np.linspace(0.01, 0.63, len(en))
            dx = np.linspace(0.02, 0.62, len(de))
            for i, (x, w) in enumerate(zip(ex, en, strict=True)):
                lit = i == IT_EN or (phase >= 1 and i == noun)
                ax.text(
                    x,
                    y_en,
                    w,
                    ha="center",
                    va="center",
                    fontsize=11,
                    color=(YELLOW if i == IT_EN else BLUE) if lit else SUB,
                    fontweight="bold" if lit else "normal",
                )
            if phase >= 1:
                # What any reader knows: an arc from 'it' to the noun it means.
                t = np.linspace(0, 1, 80)
                x0, x1 = ex[IT_EN], ex[noun]
                ax.plot(
                    x0 + (x1 - x0) * t,
                    y_en + 0.035 + 0.06 * np.sin(np.pi * t),
                    color=BLUE,
                    lw=1.8,
                    alpha=0.9,
                )
                ax.text(
                    (x0 + x1) / 2,
                    y_en + 0.10,
                    f"a reader: 'it' is the {en[noun]}",
                    fontsize=10.5,
                    color=BLUE,
                    ha="center",
                    va="bottom",
                )
            if phase >= 2:
                for i, (x, w) in enumerate(zip(dx, de, strict=True)):
                    ax.text(
                        x,
                        y_de,
                        w,
                        ha="center",
                        va="center",
                        fontsize=11,
                        color=(GREEN if correct else RED) if i == SIE else SUB,
                        fontweight="bold" if i == SIE else "normal",
                    )
                colour = GREEN if correct else RED
                ax.text(
                    0.67,
                    y_en - 0.02,
                    "the model wrote  sie  ('she')",
                    fontsize=12,
                    color=TEXT,
                    va="center",
                )
                ax.text(
                    0.67,
                    y_en - 0.085,
                    "= die Trophäe, the trophy" + ("   ✓ right" if correct else "   ✗ wrong"),
                    fontsize=12,
                    color=colour,
                    va="center",
                    fontweight="bold",
                )
                if not correct:
                    ax.text(
                        0.67,
                        y_en - 0.145,
                        "the suitcase is der Koffer — 'he' — so it\nshould have written  er",
                        fontsize=10.5,
                        color=SUB,
                        va="center",
                        linespacing=1.4,
                    )
            if phase >= 3:
                # Where the model looked while writing 'sie': at 'it', not a noun.
                ax.plot(
                    [dx[SIE], ex[IT_EN]],
                    [y_de + 0.035, y_en - 0.035],
                    color=YELLOW,
                    lw=2.8,
                    alpha=0.95,
                    solid_capstyle="round",
                )
                ax.text(
                    (dx[SIE] + ex[IT_EN]) / 2 + 0.035,
                    (y_de + y_en) / 2,
                    f"{weight:.2f}",
                    fontsize=11,
                    color=YELLOW,
                    va="center",
                    fontfamily="monospace",
                )
                for j in (TROPHY, SUITCASE):
                    ax.plot(
                        [dx[SIE], ex[j]],
                        [y_de + 0.035, y_en - 0.035],
                        color=RED,
                        lw=1.0,
                        alpha=0.5,
                        ls=(0, (3, 3)),
                    )
                    ax.text(
                        ex[j] + (0.02 if j == TROPHY else -0.02),
                        y_en - 0.06,
                        "≈ 0",
                        fontsize=9.5,
                        color=RED,
                        ha="left" if j == TROPHY else "right",
                        va="top",
                        alpha=0.8,
                        fontfamily="monospace",
                    )
        if phase >= 3:
            ax.text(
                0.67,
                0.66,
                "yellow: where it looked while writing 'sie'",
                fontsize=10.5,
                color=YELLOW,
                fontweight="bold",
                va="center",
            )

        if phase >= 4:
            ax.text(
                0.0,
                0.115,
                "Right answer or wrong one, the attention looks the same: it points at "
                "'it', never at a noun.\nWhatever chose the gender, it is not in these "
                "weights.",
                fontsize=12.5,
                color=TEXT,
                va="center",
                linespacing=1.55,
            )
            ax.text(
                0.0,
                0.015,
                "Attention tells you where information was read from. It does not tell you "
                "what was done with it.",
                fontsize=14,
                color=YELLOW,
                va="center",
                fontweight="bold",
            )

        footer(
            fig,
            "study guide: static-vs-contextual-embeddings · polysemy · measured: "
            "opus-mt-en-de, translation notebook section 6",
        )
        return fig_to_pil(fig)

    frames, durations = [], []
    for p in (0, 1, 2, 3, 4):
        hold(frames, durations, lambda p=p: render(p), ms=1500)
    hold(frames, durations, lambda: render(4), ms=1500)
    save_gif(frames, durations, "w03_s27_not_explanation.gif")


# =====================================================================
# SLIDE 28 — the ledger, closed
# =====================================================================
LEDGER = [
    (
        "A word's meaning has to come from its whole sentence.",
        "every word attends to every word — s17",
    ),
    (
        "Any word must reach any other word, however far away.",
        "one step, at any distance — s12, s23",
    ),
    (
        "And it has to be parallel, or we cannot train it at scale.",
        "no recurrence left to wait for — s26",
    ),
]


def make_closing():
    def render(n, closer):
        fig = new_fig()
        frame(
            fig,
            "THE TRANSFORMER · WHERE THAT LEAVES US",
            "The three things we asked for, before the break",
        )
        ax = blank_axes(fig, [0.045, 0.215, 0.91, 0.60])

        for i, (want, got) in enumerate(LEDGER[:n]):
            y = 0.88 - i * 0.20
            ax.text(0.0, y, "✓", fontsize=20, color=GREEN, va="center", fontweight="bold")
            ax.text(0.05, y, want, fontsize=16, color=TEXT, va="center")
            ax.text(0.05, y - 0.082, got, fontsize=12.5, color=GREEN, va="center")

        if n >= len(LEDGER):
            ax.text(
                0.0,
                0.245,
                "One mechanism, and the same one every time: a question, a set of labels, a "
                "weighted blend.",
                fontsize=13.5,
                color=SUB,
                va="center",
            )

        if closer:
            ax.text(
                0.0,
                0.10,
                "Thursday you open one and look at the weights yourself — the same model, "
                "the same sentences.",
                fontsize=15,
                color=YELLOW,
                va="center",
                style="italic",
            )

        math_strip(
            fig,
            r"$\mathrm{Attention}(Q, K, V) \;=\; \mathrm{softmax}"
            r"\!\left(\frac{Q K^{\top}}{\sqrt{d_k}}\right) V$",
            note="that is the paper",
        )
        footer(fig, "study guide: encoder-and-decoder · static-vs-contextual-embeddings")
        return fig_to_pil(fig)

    frames, durations = [], []
    for n in range(1, len(LEDGER) + 1):
        hold(frames, durations, lambda n=n: render(n, False), ms=950)
    hold(frames, durations, lambda: render(len(LEDGER), True), ms=1800, n=2)
    save_gif(frames, durations, "w03_s28_closing.gif")


if __name__ == "__main__":
    make_parallel()
    make_not_explanation()
    make_closing()
