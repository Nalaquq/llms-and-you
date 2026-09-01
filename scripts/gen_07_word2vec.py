"""Slides 14-16: word2vec — window, architecture, negative sampling.

w02_s14_window.gif       Sliding window emits (target, context) pairs
w02_s15_architecture.gif One-hot -> W -> hidden -> W' -> softmax;
                         then W' is discarded: the pretext-task reveal
w02_s16_negative.gif     50,000-way softmax becomes a yes/no game
"""

import matplotlib.pyplot as plt
import numpy as np
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
    blank_axes,
    chip,
    fig_to_pil,
    footer,
    hold,
    new_fig,
    save_gif,
    title_block,
    tween,
)

SENT = ["A", "cup", "of", "coffee", "is", "on", "the", "table"]
W = 0.105
GAP = 0.010
X0 = 0.5 - (len(SENT) * (W + GAP) - GAP) / 2


# ── Slide 14: sliding window ────────────────────────────────────────
def pairs_at(center):
    lo, hi = max(0, center - 2), min(len(SENT) - 1, center + 2)
    return [(SENT[center], SENT[j]) for j in range(lo, hi + 1) if j != center]


def render_window(center, n_pairs_shown, phases):
    fig = new_fig()
    title_block(
        fig,
        "Turning a corpus into a game",
        "slide a window along the text — every stop makes training "
        "examples: (word, one of its neighbours)",
        kicker="THE SLIDING WINDOW · SKIP-GRAM",
    )
    ax = blank_axes(fig, [0.03, 0.08, 0.94, 0.66])

    lo, hi = max(0, center - 2), min(len(SENT) - 1, center + 2)
    # window glow
    wx = X0 + lo * (W + GAP) - 0.012
    ww = (hi - lo + 1) * (W + GAP) - GAP + 0.024
    ax.add_patch(
        plt.Rectangle(
            (wx, 0.70),
            ww,
            0.20,
            facecolor=PURPLE,
            alpha=0.12,
            edgecolor=PURPLE,
            lw=2.0,
            transform=ax.transAxes,
        )
    )
    for i, w in enumerate(SENT):
        is_c = i == center
        in_w = lo <= i <= hi and not is_c
        chip(
            ax,
            X0 + i * (W + GAP),
            0.73,
            W,
            0.14,
            w,
            fontsize=15.5,
            face=PANEL,
            mono=True,
            edge=YELLOW if is_c else (BLUE if in_w else PANEL_EDGE),
            color=YELLOW if is_c else (BLUE if in_w else FAINT),
            lw=2.4 if is_c else 1.4,
        )
    ax.text(
        X0 + center * (W + GAP) + W / 2, 0.945, "target", ha="center", fontsize=12.5, color=YELLOW
    )
    ax.text(
        wx + ww / 2, 0.655, "context window (2 each side)", ha="center", fontsize=12, color=PURPLE
    )

    all_pairs = pairs_at(center)
    for k, (a, b) in enumerate(all_pairs[:n_pairs_shown]):
        col_x = 0.24 + (k % 2) * 0.28
        row_y = 0.42 - (k // 2) * 0.13
        chip(
            ax,
            col_x,
            row_y,
            0.24,
            0.10,
            f"({a}, {b})",
            fontsize=14.5,
            mono=True,
            face=PANEL,
            edge=GREEN,
            color=TEXT,
            lw=1.6,
        )
    if n_pairs_shown:
        ax.text(
            0.5,
            0.545,
            "training examples from this one stop:",
            ha="center",
            fontsize=13.5,
            color=SUB,
        )
    if "point" in phases:
        ax.text(
            0.5,
            0.06,
            "the window slides one word at a time over billions of words — "
            "no labels, no humans: the text teaches itself",
            ha="center",
            fontsize=15,
            color=YELLOW,
        )
    footer(fig, "study guide: sliding-window · skip-gram · cbow · corpus")
    return fig_to_pil(fig)


frames, durations = [], []
hold(frames, durations, lambda: render_window(3, 0, set()), ms=1300)
for k in range(1, 5):
    hold(frames, durations, lambda k=k: render_window(3, k, set()), ms=520)
hold(frames, durations, lambda: render_window(3, 4, set()), ms=800)
hold(frames, durations, lambda: render_window(4, 4, set()), ms=800)
hold(frames, durations, lambda: render_window(5, 4, set()), ms=800)
hold(frames, durations, lambda: render_window(5, 4, {"point"}), ms=1500)
save_gif(frames, durations, "w02_s14_window.gif")


# ── Slide 15: the architecture, and the reveal ──────────────────────
def render_arch(phases, fade_w2=0.0):
    fig = new_fig()
    title_block(
        fig,
        "word2vec: a tiny network with a secret",
        "trained to predict neighbours — but the predictions were never the point",
        kicker="WORD2VEC · THE PRETEXT TASK",
    )
    ax = blank_axes(fig, [0.03, 0.06, 0.94, 0.70])

    # input one-hot
    ax.text(0.085, 0.93, '"coffee" as one-hot', ha="center", fontsize=12.5, color=SUB)
    for i in range(7):
        v = 1 if i == 3 else 0
        chip(
            ax,
            0.055,
            0.78 - i * 0.105,
            0.06,
            0.085,
            str(v),
            fontsize=12,
            mono=True,
            face=PANEL,
            edge=YELLOW if v else PANEL_EDGE,
            color=YELLOW if v else FAINT,
            lw=2.0 if v else 1.0,
        )

    # matrix W
    if "w" in phases:
        ax.add_patch(
            plt.Rectangle(
                (0.175, 0.18),
                0.155,
                0.62,
                facecolor=PANEL,
                edgecolor=BLUE,
                lw=2.2,
                transform=ax.transAxes,
            )
        )
        ax.text(0.2525, 0.83, "matrix W", ha="center", fontsize=14, color=BLUE)
        ax.text(0.2525, 0.135, "one row per word", ha="center", fontsize=11.5, color=SUB)
        # highlight row 3
        ax.add_patch(
            plt.Rectangle(
                (0.175, 0.18 + 0.62 * (1 - 4 / 7)),
                0.155,
                0.62 / 7,
                facecolor=YELLOW,
                alpha=0.30,
                edgecolor="none",
                transform=ax.transAxes,
            )
        )
        ax.annotate(
            "",
            xy=(0.170, 0.49),
            xytext=(0.122, 0.49),
            xycoords="axes fraction",
            arrowprops=dict(arrowstyle="-|>", color=SUB, lw=2.0),
        )
        ax.text(
            0.2525,
            0.49 + 0.005,
            "row 3",
            ha="center",
            fontsize=11.5,
            color="#1b1e26",
            fontweight="bold",
        )

    # hidden vector
    if "hidden" in phases:
        ax.text(
            0.435, 0.93, "hidden layer = the embedding", ha="center", fontsize=12.5, color=YELLOW
        )
        for i, v in enumerate(["+0.62", "-0.31", "+0.85"]):
            chip(
                ax,
                0.405,
                0.62 - i * 0.115,
                0.062,
                0.09,
                v,
                fontsize=11,
                mono=True,
                face=PANEL,
                edge=YELLOW,
                color=YELLOW,
                lw=1.8,
            )
        ax.annotate(
            "",
            xy=(0.398, 0.49),
            xytext=(0.336, 0.49),
            xycoords="axes fraction",
            arrowprops=dict(arrowstyle="-|>", color=SUB, lw=2.0),
        )
        ax.text(
            0.435,
            0.30,
            "picking a one-hot row\nIS the lookup",
            ha="center",
            fontsize=11.5,
            color=SUB,
        )

    # W' and softmax output
    if "out" in phases:
        a2 = 1.0 - fade_w2
        ax.add_patch(
            plt.Rectangle(
                (0.52, 0.18),
                0.155,
                0.62,
                facecolor=PANEL,
                edgecolor=GREEN,
                lw=2.2,
                alpha=a2,
                transform=ax.transAxes,
            )
        )
        ax.text(0.5975, 0.83, "matrix W′", ha="center", fontsize=14, color=GREEN, alpha=a2)
        ax.annotate(
            "",
            xy=(0.515, 0.49),
            xytext=(0.470, 0.49),
            xycoords="axes fraction",
            arrowprops=dict(arrowstyle="-|>", color=SUB, lw=2.0, alpha=a2),
        )
        probs = [
            ("cup", 0.34),
            ("of", 0.22),
            ("is", 0.18),
            ("on", 0.11),
            ("table", 0.06),
            ("king", 0.01),
        ]
        ax.text(
            0.80,
            0.93,
            "softmax: P(neighbour | coffee)",
            ha="center",
            fontsize=12.5,
            color=SUB,
            alpha=a2,
        )
        for i, (w, pv) in enumerate(probs):
            y = 0.78 - i * 0.105
            ax.text(
                0.712,
                y + 0.035,
                w,
                fontsize=12,
                color=TEXT,
                ha="right",
                fontfamily="monospace",
                alpha=a2,
            )
            ax.add_patch(
                plt.Rectangle(
                    (0.725, y),
                    0.20 * pv * 2.4,
                    0.07,
                    facecolor=GREEN,
                    alpha=0.85 * a2,
                    edgecolor="none",
                    transform=ax.transAxes,
                )
            )
            ax.text(
                0.735 + 0.20 * pv * 2.4,
                y + 0.035,
                f"{pv:.2f}",
                fontsize=10.5,
                color=SUB,
                alpha=a2,
                va="center",
            )
        ax.annotate(
            "",
            xy=(0.705, 0.49),
            xytext=(0.680, 0.49),
            xycoords="axes fraction",
            arrowprops=dict(arrowstyle="-|>", color=SUB, lw=2.0, alpha=a2),
        )
    if fade_w2 > 0.5:
        ax.text(
            0.795,
            0.49,
            "after training:\nthrown away",
            ha="center",
            fontsize=15,
            color=RED,
            rotation=8,
        )
    if "reveal" in phases:
        chip(
            ax,
            0.13,
            0.005,
            0.72,
            0.105,
            "the prediction game was a pretext — the treasure is matrix W: "
            "one learned vector per word",
            fontsize=14.5,
            face=PANEL,
            edge=YELLOW,
            color=TEXT,
            lw=2.2,
        )
    footer(fig, "study guide: word2vec · pretext-task · neural-network-and-layers · softmax")
    return fig_to_pil(fig)


frames, durations = [], []
hold(frames, durations, lambda: render_arch(set()), ms=1100)
hold(frames, durations, lambda: render_arch({"w"}), ms=1100)
hold(frames, durations, lambda: render_arch({"w", "hidden"}), ms=1200)
hold(frames, durations, lambda: render_arch({"w", "hidden", "out"}), ms=1600)
tween(
    frames, durations, lambda t: render_arch({"w", "hidden", "out"}, fade_w2=t * 0.85), n=12, ms=60
)
hold(
    frames, durations, lambda: render_arch({"w", "hidden", "out", "reveal"}, fade_w2=0.85), ms=1600
)
save_gif(frames, durations, "w02_s15_architecture.gif")


# ── Slide 16: negative sampling ─────────────────────────────────────
def render_neg(collapse_t, phases):
    fig = new_fig()
    title_block(
        fig,
        "One cheat makes it trainable",
        "scoring all 50,000 words at every step is too slow — so change the question",
        kicker="NEGATIVE SAMPLING",
    )
    ax = blank_axes(fig, [0.03, 0.07, 0.94, 0.68])

    if collapse_t < 1:
        a = 1 - collapse_t
        ax.text(
            0.26, 0.95, "the expensive question", ha="center", fontsize=14.5, color=RED, alpha=a
        )
        ax.text(
            0.26,
            0.88,
            '"which of all 50,000 words is the neighbour?"',
            ha="center",
            fontsize=13,
            color=SUB,
            alpha=a,
        )
        rng = np.random.default_rng(5)
        heights = rng.uniform(0.02, 0.10, 60)
        heights[22] = 0.30
        for i, h in enumerate(heights):
            ax.add_patch(
                plt.Rectangle(
                    (0.045 + i * 0.0072, 0.44),
                    0.0058,
                    h,
                    facecolor=RED,
                    alpha=0.6 * a,
                    edgecolor="none",
                    transform=ax.transAxes,
                )
            )
        ax.text(
            0.26,
            0.38,
            "a full softmax over the vocabulary,\nbillions of times",
            ha="center",
            fontsize=12.5,
            color=SUB,
            alpha=a,
        )

    if collapse_t > 0:
        a = collapse_t
        ax.text(0.72, 0.95, "the cheap question", ha="center", fontsize=14.5, color=GREEN, alpha=a)
        ax.text(
            0.72,
            0.88,
            '"did these two really appear together?"',
            ha="center",
            fontsize=13,
            color=SUB,
            alpha=a,
        )
        rows = [
            ("(coffee, cup)", "yes — pull together", GREEN),
            ("(coffee, walrus)", "no — push apart", RED),
            ("(coffee, senate)", "no — push apart", RED),
            ("(coffee, kazoo)", "no — push apart", RED),
        ]
        for i, (pair, verdict, col) in enumerate(rows):
            y = 0.70 - i * 0.135
            chip(
                ax,
                0.545,
                y,
                0.185,
                0.10,
                pair,
                fontsize=13,
                mono=True,
                face=PANEL,
                edge=col,
                color=TEXT,
                lw=1.8,
                alpha=a,
            )
            ax.text(0.745, y + 0.05, verdict, fontsize=13, color=col, va="center", alpha=a)
        ax.text(
            0.72,
            0.115,
            "one real pair + a few random fakes\n(the “negative samples”)",
            ha="center",
            fontsize=12.5,
            color=SUB,
            alpha=a,
        )
    if "moral" in phases:
        fig.text(
            0.5,
            0.075,
            "the field's signature move: replace the exact, expensive thing "
            "with a cheap approximation — and it works",
            fontsize=14.5,
            color=YELLOW,
            ha="center",
        )
    footer(fig, "study guide: negative-sampling · softmax")
    return fig_to_pil(fig)


frames, durations = [], []
hold(frames, durations, lambda: render_neg(0, set()), ms=1700)
tween(frames, durations, lambda t: render_neg(t, set()), n=14, ms=60)
hold(frames, durations, lambda: render_neg(1, set()), ms=1300)
hold(frames, durations, lambda: render_neg(1, {"moral"}), ms=1500)
save_gif(frames, durations, "w02_s16_negative.gif")
