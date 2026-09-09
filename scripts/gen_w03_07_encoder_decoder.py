"""Week 3, the transformer: writing, the bridge between the halves, and the stack.

  w03_s22_mask.gif   the decoder cannot look at what it has not written yet
  w03_s23_cross.gif  cross-attention, read as a word alignment
  w03_s25_block.gif  one block, and the six of them

The German on both slides is what opus-mt-en-de actually produces, and the
alignment weights on s23 are measured from layer 3, head 4 of that model.
Reproduce either in notebooks/w03-thu-translation.ipynb, sections 2 and 4.

s22 is staged the way 3Blue1Brown stages masking (Chapter 6, the ShowMasking
scene): scores exist for every pair first, including the words not yet
written; those are stamped minus infinity BEFORE the softmax; and after it
they are exactly zero. The grid is the same one s15 and s16 used -- rows are
the word being written, columns the words it looks at, so the blocked
triangle is above the diagonal, as it is in both Thursday notebooks. The scores
on it are illustrative and the slide says so; the triangle is not.
"""

import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
from style_dark import (
    BLUE,
    FAINT,
    GREEN,
    PANEL,
    PANEL_EDGE,
    PURPLE,
    RED,
    SUB,
    TEXT,
    YELLOW,
    arrow,
    blank_axes,
    ease,
    fig_to_pil,
    footer,
    grid_axes,
    grid_cell,
    grid_labels,
    grid_legend,
    hold,
    math_strip,
    new_fig,
    save_gif,
    tween,
)

GERMAN = ["Das", "Tier", "ist", "nicht", "über", "die", "Straße", "gegangen"]


# Illustrative scores for the mask slide. Each word likes itself and the word
# before it, a few reach further back -- and a few of the LARGEST scores sit
# on words that have not been written yet. That is the point of the slide:
# without the mask, those would win, and the model would be copying its answer.
def _mask_scores():
    n = len(GERMAN)
    rng = np.random.default_rng(7)
    s = rng.uniform(0.3, 1.4, (n, n))
    for i in range(n):
        s[i, i] = 2.6
        if i:
            s[i, i - 1] = 2.1
    for i, j, v in [(7, 4, 2.4), (7, 1, 1.9), (6, 4, 2.3), (3, 2, 2.3)]:
        s[i, j] = v  # looking back
    for i, j, v in [(0, 1, 2.8), (1, 6, 2.5), (2, 7, 2.4), (4, 6, 2.2)]:
        s[i, j] = v  # looking ahead -- the ones the mask exists for
    return s


def _masked_softmax(s):
    future = np.triu(np.ones_like(s, dtype=bool), k=1)
    m = np.where(future, -np.inf, s)
    e = np.exp(m - m.max(axis=1, keepdims=True))
    return e / e.sum(axis=1, keepdims=True)


MASK_SCORES = _mask_scores()
MASK_WEIGHTS = _masked_softmax(MASK_SCORES)

# Measured: layer 3, head 4 of opus-mt-en-de. Note the last two -- the German
# verb complex at the end of the clause both reach back to "bought" in the
# middle of the English. That crossing is the whole argument for attention.
EN = ["I", "know", "that", "he", "bought", "a", "new", "car", "yesterday"]
DE = ["Ich", "weiß", "dass", "er", "gestern", "ein", "neues", "Auto", "gekauft", "hat"]
ALIGN = [
    (0, 0, 0.96),
    (1, 1, 0.97),
    (2, 2, 0.90),
    (3, 3, 0.87),
    (4, 8, 1.00),
    (5, 5, 0.89),
    (6, 6, 0.98),
    (7, 7, 0.74),
    (8, 4, 0.99),
    (9, 4, 0.52),
]


def frame(fig, kicker, title, subtitle):
    fig.text(0.045, 0.945, kicker, fontsize=13, color=PURPLE, fontweight="bold", va="top")
    fig.text(0.045, 0.895, title, fontsize=30, color=TEXT, fontweight="bold", va="top")
    fig.text(0.045, 0.838, subtitle, fontsize=15.5, color=SUB, va="top")


# =====================================================================
# SLIDE 22 — the mask
# =====================================================================
def make_mask():
    n = len(GERMAN)
    smin, smax = MASK_SCORES.min(), MASK_SCORES.max()
    wmax = MASK_WEIGHTS.max()

    def render(phase, t=1.0):
        fig = new_fig()
        frame(
            fig,
            "THE TRANSFORMER · THE MASK",
            "While it writes, it is not allowed to read ahead",
            "The decoder writes one word at a time, and each word may look only at the "
            "words already written.",
        )
        gax = grid_axes(fig, [0.10, 0.215, 0.36, 0.515], n)
        grid_labels(gax, n, GERMAN, fontsize=11.5)
        grid_legend(gax, "rows: the word being written · columns: the words it looks at")

        t_mask = 1.0 if phase >= 2 else (t if phase == 1 else 0.0)
        t_soft = 1.0 if phase >= 3 else (t if phase == 2 else 0.0)
        for r in range(n):
            for c in range(n):
                norm = (MASK_SCORES[r, c] - smin) / (smax - smin)
                x, y = c, n - 1 - r
                if c <= r:
                    grid_cell(gax, n, r, c, norm, MASK_WEIGHTS[r, c], t_soft, wmax=wmax)
                    continue
                # Not written yet: the score is there, then it is struck out.
                gax.add_patch(
                    Rectangle(
                        (x + 0.04, y + 0.04),
                        0.92,
                        0.92,
                        facecolor="#241d24" if t_mask > 0 else "none",
                        alpha=min(1.0, t_mask * 2),
                        edgecolor=RED if 0 < t_mask < 1 else PANEL_EDGE,
                        lw=1.4 if 0 < t_mask < 1 else 0.7,
                    )
                )
                if t_mask < 1.0:
                    gax.add_patch(
                        Circle(
                            (x + 0.5, y + 0.5),
                            (0.07 + 0.38 * norm) * (1.0 - t_mask),
                            facecolor=SUB,
                            edgecolor="none",
                            alpha=0.9,
                        )
                    )
                if t_mask > 0:
                    gax.text(
                        x + 0.5,
                        y + 0.5,
                        "−∞" if t_soft < 0.5 else "0",
                        ha="center",
                        va="center",
                        fontsize=11 if t_soft < 0.5 else 10,
                        color=RED,
                        alpha=t_mask * (0.9 if t_soft < 0.5 else 0.55),
                        fontweight="bold",
                    )

        x0 = 0.55
        fig.text(
            x0,
            0.755,
            "Before the mask, every word has a score for every word —\n"
            "including the words after it, which have not been written yet.",
            fontsize=12.5,
            color=TEXT,
            va="top",
            linespacing=1.6,
        )
        if phase >= 1:
            fig.text(
                x0,
                0.635,
                "So, before the softmax, set every one of those to minus infinity.",
                fontsize=12.5,
                color=RED,
                va="top",
                alpha=min(1.0, t_mask * 2),
            )
        if phase >= 2:
            fig.text(
                x0,
                0.555,
                "After the softmax they are exactly zero. Not small. Zero.\n"
                "The words already written share the whole budget between them.",
                fontsize=12.5,
                color=TEXT,
                va="top",
                linespacing=1.6,
                alpha=min(1.0, t_soft * 2),
            )
            fig.text(x0, 0.44, "allowed", fontsize=11.5, color=GREEN, va="top", alpha=t_soft)
            fig.text(
                x0 + 0.09,
                0.44,
                "blocked — has not been written yet",
                fontsize=11.5,
                color=RED,
                va="top",
                alpha=t_soft,
            )
        if phase >= 3:
            fig.text(
                x0,
                0.365,
                "Without it the model could read the answer while learning\n"
                "to write it, and would learn nothing.",
                fontsize=13,
                color=YELLOW,
                va="top",
                linespacing=1.6,
            )
            fig.text(
                x0,
                0.255,
                "The triangle is what both Thursday notebooks check, in section 2.",
                fontsize=11.5,
                color=SUB,
                va="top",
            )
            fig.text(
                x0,
                0.215,
                "illustrative scores — the triangle is not",
                fontsize=10.5,
                color=FAINT,
                va="top",
            )

        math_strip(
            fig,
            r"$\mathrm{score}(i,j) \;=\; -\infty \quad \mathrm{when} \;\; j > i "
            r"\qquad\Rightarrow\qquad \alpha_{ij} = 0$",
            note="set before the softmax",
        )
        footer(fig, "study guide: softmax · encoder-and-decoder")
        return fig_to_pil(fig)

    frames, durations = [], []
    hold(frames, durations, lambda: render(0), ms=1300)
    hold(frames, durations, lambda: render(1, 0.0), ms=400)
    tween(frames, durations, lambda t: render(1, ease(t)), n=12, ms=70)
    hold(frames, durations, lambda: render(1), ms=1300)
    tween(frames, durations, lambda t: render(2, ease(t)), n=12, ms=70)
    hold(frames, durations, lambda: render(2), ms=1300)
    hold(frames, durations, lambda: render(3), ms=1700, n=2)
    save_gif(frames, durations, "w03_s22_mask.gif")


# =====================================================================
# SLIDE 23 — cross-attention
# =====================================================================
def make_cross():
    def render(n_shown, note):
        fig = new_fig()
        frame(
            fig,
            "THE TRANSFORMER · CROSS-ATTENTION",
            "The bridge: every German word may look at every English word",
            "Same mechanism, one change — the question comes from the German side, the "
            "labels from the English.",
        )
        ax = blank_axes(fig, [0.045, 0.195, 0.91, 0.60])

        ex = np.linspace(0.06, 0.94, len(EN))
        dx = np.linspace(0.04, 0.96, len(DE))
        ax.text(
            0.0,
            0.93,
            "ENGLISH — what it read",
            fontsize=11,
            color=BLUE,
            fontweight="bold",
            va="center",
        )
        ax.text(
            0.0,
            0.20,
            "GERMAN — what it wrote",
            fontsize=11,
            color=GREEN,
            fontweight="bold",
            va="center",
        )

        shown = ALIGN[:n_shown]
        lit_en = {e for _, e, _ in shown}
        for i, (x, w) in enumerate(zip(ex, EN, strict=True)):
            ax.text(
                x,
                0.82,
                w,
                ha="center",
                va="center",
                fontsize=13.5,
                color=TEXT if i in lit_en else FAINT,
                fontweight="bold" if i in lit_en else "normal",
            )
        for i, (x, w) in enumerate(zip(dx, DE, strict=True)):
            ax.text(
                x,
                0.31,
                w,
                ha="center",
                va="center",
                fontsize=13.5,
                color=TEXT if i < n_shown else FAINT,
                fontweight="bold" if i < n_shown else "normal",
            )

        for d, e, weight in shown:
            far = abs(dx[d] - ex[e]) > 0.22
            ax.plot(
                [dx[d], ex[e]],
                [0.365, 0.775],
                color=YELLOW if far else GREEN,
                lw=0.8 + 2.6 * weight,
                alpha=0.85 if far else 0.55,
                solid_capstyle="round",
            )

        if note:
            ax.text(
                0.0,
                0.09,
                "Look at the two yellow lines. German sends the verb to the end of the "
                "clause, so 'gekauft hat'\nsits nine words away from 'bought' — and reaches "
                "it in one step. An RNN had to carry that\ndistance in a single vector, and "
                "this is what it could not do.",
                fontsize=13,
                color=YELLOW,
                va="center",
                linespacing=1.7,
            )

        math_strip(
            fig,
            r"$Q \;\mathrm{from\ the\ decoder}, \qquad K, V \;\mathrm{from\ the\ encoder}$",
            note="measured: layer 3, head 4 of opus-mt-en-de",
        )
        footer(fig, "study guide: encoder-and-decoder · sequence-to-sequence")
        return fig_to_pil(fig)

    frames, durations = [], []
    for n in (2, 4, 6, 8, 10):
        hold(frames, durations, lambda n=n: render(n, False), ms=620)
    hold(frames, durations, lambda: render(10, True), ms=1800, n=2)
    save_gif(frames, durations, "w03_s23_cross.gif")


# =====================================================================
# SLIDE 25 — the block
# =====================================================================
BLOCK = [
    ("attention", "let the words look at each other", GREEN),
    ("add + normalise", "keep the original, add what was learned", FAINT),
    ("feed-forward", "now think about each word on its own", BLUE),
    ("add + normalise", "keep the original, add what was learned", FAINT),
]


def make_block():
    def render(n, stacked):
        fig = new_fig()
        frame(
            fig,
            "THE TRANSFORMER · THE BLOCK",
            "Four steps, stacked six times. That is the whole model.",
            "Everything you have seen today is one block. The architecture is that block, "
            "repeated.",
        )
        ax = blank_axes(fig, [0.045, 0.195, 0.91, 0.60])

        for i, (name, what, colour) in enumerate(BLOCK[:n]):
            y = 0.80 - i * 0.175
            box = FancyBboxPatch(
                (0.02, y - 0.06),
                0.29,
                0.12,
                boxstyle="round,pad=0.008,rounding_size=0.02",
                facecolor=PANEL,
                edgecolor=colour,
                lw=1.8,
                transform=ax.transAxes,
            )
            ax.add_patch(box)
            ax.text(
                0.165,
                y,
                name,
                fontsize=14,
                color=colour,
                ha="center",
                va="center",
                fontweight="bold",
            )
            ax.text(0.34, y, what, fontsize=13, color=TEXT, va="center")
            if i:
                arrow(ax, (0.165, y + 0.115), (0.165, y + 0.065), color=FAINT, lw=1.6, mutation=14)

        if stacked:
            for k in range(6):
                x = 0.745 + k * 0.043
                ax.add_patch(
                    FancyBboxPatch(
                        (x, 0.12),
                        0.034,
                        0.30,
                        boxstyle="round,pad=0.004,rounding_size=0.012",
                        facecolor=PANEL,
                        edgecolor=PURPLE,
                        lw=1.4,
                        alpha=0.9,
                        transform=ax.transAxes,
                    )
                )
                ax.text(
                    x + 0.017, 0.27, str(k + 1), fontsize=11, color=PURPLE, ha="center", va="center"
                )
            ax.text(
                0.745,
                0.475,
                "six of them, one after another",
                fontsize=12.5,
                color=PURPLE,
                va="center",
                fontweight="bold",
            )
            ax.text(
                0.72,
                0.05,
                "Each layer's output is the next one's input.",
                fontsize=12,
                color=SUB,
                va="center",
            )

        math_strip(
            fig,
            r"$\mathrm{LayerNorm}\left(x + \mathrm{Sublayer}(x)\right)$",
            note="the '+ x' is the residual: nothing is ever fully overwritten",
        )
        footer(fig, "study guide: neural-network-and-layers · parameters-and-weights")
        return fig_to_pil(fig)

    frames, durations = [], []
    for n in range(1, len(BLOCK) + 1):
        hold(frames, durations, lambda n=n: render(n, False), ms=850)
    hold(frames, durations, lambda: render(4, True), ms=1700, n=2)
    save_gif(frames, durations, "w03_s25_block.gif")


if __name__ == "__main__":
    make_mask()
    make_cross()
    make_block()
