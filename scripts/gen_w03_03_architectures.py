"""Week 3 review, part two: the three architectures the transformer replaced.

  w03_s08_perceptron.gif   one unit, pricing a house -- the arithmetic on screen
  w03_s09_cnn.gif          that unit, copied along a sentence
  w03_s10_rnn.gif          that unit, handed its own previous answer

The perceptron is taught on the classic example -- bedrooms and distance to
downtown, in, a price out -- because a room with no mathematics needs to see a
unit CALCULATE before it can see one fail. The two architectures after it are
then introduced as the same unit, rearranged: a CNN is one unit with a
three-word window copied along the sentence with identical weights; an RNN is
one unit that also reads its own output from the word before. Both of those
run on a sentence, because the sentence is where the transformer's argument
lives. (Earlier drafts ran the perceptron on "not good" and the CNN on a grid
of embedding numbers; both were judged too hard for the room.)

Perceptrons and CNNs are deliberately NOT study-guide entries -- they are here
to make the transformer's design legible, and the footer says so rather than
implying an assessment that is not coming. RNNs are assessed, and their
footer names the entries.

Numbers are computed. The house prices come out of the weights shown, and the
convolution really does peak on the window its filter was built from.
"""

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
    arrow,
    blank_axes,
    chip,
    fig_to_pil,
    footer,
    hold,
    math_strip,
    new_fig,
    pros_cons,
    save_gif,
)

PANEL_RECT = [0.045, 0.215, 0.255, 0.575]
DEMO_RECT = [0.345, 0.195, 0.615, 0.60]
BACKGROUND_FOOTER = (
    "background for the transformer — not a study-guide entry · "
    "builds on: neural-network-and-layers · parameters-and-weights"
)


def arch_frame(fig, n, title, subtitle):
    fig.text(
        0.045,
        0.945,
        f"REVIEW · ARCHITECTURE {n} OF 3",
        fontsize=13,
        color=PURPLE,
        fontweight="bold",
        va="top",
    )
    fig.text(0.045, 0.895, title, fontsize=30, color=TEXT, fontweight="bold", va="top")
    fig.text(0.045, 0.838, subtitle, fontsize=15.5, color=SUB, va="top")


# =====================================================================
# SLIDE 8 — the perceptron, pricing a house
# =====================================================================
# Thousands of dollars throughout, so the arithmetic fits on one line and
# can be checked in the room.
P_INPUTS = ["bedrooms", "miles to downtown"]
P_WEIGHTS = np.array([45.0, -12.0])
P_BIAS = 150.0
P_HOUSES = [("House A", np.array([3.0, 4.0])), ("House B", np.array([2.0, 1.0]))]


def p_price(x):
    return float(P_WEIGHTS @ x + P_BIAS)


def _k(v):
    """$237k, −$48k: money, in the units the slide uses."""
    sign = "−" if v < 0 else ""
    return f"{sign}\\${abs(v):.0f}k"


def make_perceptron():
    def render(house, n_terms, flaw=False):
        """house: index of the house being priced (None before any); n_terms: how
        much of its arithmetic is on screen, 0..4 (two products, the bias, the
        total)."""
        fig = new_fig()
        arch_frame(
            fig,
            1,
            "The perceptron",
            "One unit: multiply each input by a weight, add them up, and answer. "
            "Every network here is made of these.",
        )
        pros_cons(
            fig,
            PANEL_RECT,
            [
                "The smallest thing that\nlearns from examples: the\nweights come from past sales.",
                "The weights are readable —\n$45k a bedroom is a number\nyou can argue with.",
                "Stack them and you have\nevery network in this deck.",
            ],
            [
                "It can only add. A bedroom is\nworth the same $45k downtown\nor "
                "forty miles out — the two\ninputs never interact.",
                "The inputs must be a fixed\nlist of numbers. For text,\nthat means "
                "flattening the\nsentence before it arrives.",
            ],
        )
        ax = blank_axes(fig, DEMO_RECT)
        x = P_HOUSES[house][1] if house is not None else None

        # The unit: two inputs, two weighted edges, a sum, a price.
        ys = [0.86, 0.66]
        for i, (name, w, y) in enumerate(zip(P_INPUTS, P_WEIGHTS, ys, strict=True)):
            live = x is not None
            chip(
                ax,
                0.0,
                y - 0.055,
                0.12,
                0.11,
                f"{x[i]:.0f}" if live else "?",
                fontsize=17,
                mono=True,
                face="#2b3446" if live else PANEL,
                edge=YELLOW if live else PANEL_EDGE,
                color=YELLOW if live else FAINT,
                bold=live,
            )
            ax.text(0.135, y, name, fontsize=12, color=SUB, va="center")
            ax.plot(
                [0.31, 0.46],
                [y, 0.76],
                color=GREEN if w > 0 else RED,
                lw=2.2,
                alpha=0.8,
                transform=ax.transAxes,
            )
            ax.text(
                0.385,
                y + (0.76 - y) * 0.5 + (0.035 if y > 0.76 else -0.04),
                f"× {_k(w)}",
                fontsize=11.5,
                color=GREEN if w > 0 else RED,
                ha="center",
                va="center",
                fontfamily="monospace",
            )
        chip(ax, 0.46, 0.695, 0.10, 0.13, "Σ", fontsize=20, edge=BLUE, color=BLUE)
        ax.text(0.51, 0.62, f"+ {_k(P_BIAS)}", fontsize=11, color=FAINT, ha="center")
        ax.text(0.51, 0.575, "the bias", fontsize=9.5, color=FAINT, ha="center")
        arrow(ax, (0.565, 0.76), (0.64, 0.76), color=FAINT, lw=2.0)
        done = house is not None and n_terms >= 4
        chip(
            ax,
            0.645,
            0.695,
            0.20,
            0.13,
            _k(p_price(x)) if done else "price",
            fontsize=17 if done else 13,
            mono=done,
            face="#2b3446" if done else PANEL,
            edge=GREEN if done else PANEL_EDGE,
            color=GREEN if done else SUB,
            bold=done,
        )

        # The arithmetic, one term at a time, for each house priced so far.
        for h, (label, xv) in enumerate(P_HOUSES):
            if house is None or h > house:
                break
            n = n_terms if h == house else 4
            y = 0.44 - h * 0.17
            ax.text(
                0.0,
                y,
                f"{label}:  {xv[0]:.0f} bedrooms, {xv[1]:.0f} mile{'s' if xv[1] != 1 else ''} "
                f"from downtown",
                fontsize=13,
                color=TEXT if h == house else SUB,
                va="center",
            )
            parts = [
                f"{xv[0]:.0f} × {_k(P_WEIGHTS[0])}",
                f"{xv[1]:.0f} × {_k(P_WEIGHTS[1])}",
                _k(P_BIAS),
            ]
            shown = "  +  ".join(parts[: min(n, 3)])
            if n >= 4:
                shown += f"   =   {_k(p_price(xv))}"
            ax.text(
                0.0,
                y - 0.065,
                shown,
                fontsize=12.5,
                color=SUB,
                va="center",
                fontfamily="monospace",
            )
            if n >= 4:
                worked = "  +  ".join(_k(v) for v in [*(P_WEIGHTS * xv), P_BIAS])
                ax.text(
                    0.0,
                    y - 0.115,
                    f"= {worked}",
                    fontsize=11,
                    color=FAINT,
                    va="center",
                    fontfamily="monospace",
                )

        if flaw:
            ax.text(
                0.0,
                0.04,
                "It is a straight line. Every bedroom adds exactly $45k whether the house is "
                "downtown or forty\nmiles out — and real prices are not like that. Neither is "
                "language: 'not' and 'good' interact.",
                fontsize=12,
                color=YELLOW,
                va="center",
                linespacing=1.6,
            )

        math_strip(
            fig,
            r"$\hat{y} \;=\; w_1 x_1 + w_2 x_2 + b$",
            note="w = (45, −12), b = 150, in \\$k — learned from sales",
        )
        footer(fig, BACKGROUND_FOOTER)
        return fig_to_pil(fig)

    frames, durations = [], []
    hold(frames, durations, lambda: render(None, 0), ms=1100)
    for n in range(5):
        hold(frames, durations, lambda n=n: render(0, n), ms=900 if n < 4 else 1500)
    for n in (1, 2, 3, 4):
        hold(frames, durations, lambda n=n: render(1, n), ms=550 if n < 4 else 1300)
    hold(frames, durations, lambda: render(1, 4, flaw=True), ms=1600, n=2)
    save_gif(frames, durations, "w03_s08_perceptron.gif")


# =====================================================================
# SLIDE 9 — the CNN: the same unit, copied along the sentence
# =====================================================================
C_SENT = ["the", "film", "was", "not", "very", "good"]
C_DIM = 4
C_K = 3
_rng = np.random.default_rng(19)
C_EMB = np.round(_rng.normal(0, 0.55, size=(len(C_SENT), C_DIM)), 2)
# A learned filter is a pattern the training data made worth detecting. Here
# it IS the "not very good" window, which is what "learned to detect that
# phrase" means -- and it makes the peak on the slide a real computation.
C_FILTER = C_EMB[3:6].copy()


def c_featuremap():
    return np.array(
        [float((C_EMB[i : i + C_K] * C_FILTER).sum()) for i in range(len(C_SENT) - C_K + 1)]
    )


def make_cnn():
    fmap = c_featuremap()
    best = int(np.argmax(fmap))
    word_x = [0.09 + i * 0.16 for i in range(len(C_SENT))]

    def render(pos, phase):
        fig = new_fig()
        arch_frame(
            fig,
            2,
            "The convolutional network",
            "Take that unit, give it a three-word window, and copy it along the "
            "sentence with the same weights.",
        )
        pros_cons(
            fig,
            PANEL_RECT,
            [
                "Learns which local phrases\nmatter — nobody lists them.",
                "The same unit fires wherever\nthe phrase appears in the\nsentence.",
                "Every window is computed at\nonce: fast, and parallel.",
            ],
            [
                "The window is fixed. 'The\nanimal … it' is "
                "thirteen words\napart and simply invisible.",
                "Pooling keeps whether the\nphrase occurred, not where.",
                "Seeing further means stacking\nmore layers, "
                "which costs depth\nand still has a horizon.",
            ],
        )
        ax = blank_axes(fig, DEMO_RECT)

        ax.text(
            0.0,
            0.99,
            "the sentence — each word is its vector from Week 2, so the unit's inputs are numbers",
            fontsize=10.5,
            color=FAINT,
            fontweight="bold",
            va="top",
        )
        for i, (word, cx) in enumerate(zip(C_SENT, word_x, strict=True)):
            inside = pos is not None and pos <= i < pos + C_K
            chip(
                ax,
                cx - 0.07,
                0.78,
                0.14,
                0.10,
                word,
                fontsize=13,
                mono=True,
                face="#2b3446" if inside else PANEL,
                edge=YELLOW if inside else PANEL_EDGE,
                color=YELLOW if inside else SUB,
                bold=inside,
            )

        if pos is not None:
            # The unit, drawn exactly as it was on the perceptron slide: three
            # weighted edges into a sum. Only its position changes.
            cx = word_x[pos + 1]
            for k in range(C_K):
                sx = word_x[pos + k]
                ax.plot(
                    [sx, cx],
                    [0.775, 0.635],
                    color=BLUE,
                    lw=2.0,
                    alpha=0.85,
                    transform=ax.transAxes,
                )
                ax.text(
                    sx + (cx - sx) * 0.42 + (0.0 if k == 1 else (-0.03 if k == 0 else 0.03)),
                    0.775 + (0.635 - 0.775) * 0.42,
                    f"w{k + 1}",
                    fontsize=9.5,
                    color=BLUE,
                    ha="center",
                    va="center",
                    fontfamily="monospace",
                )
            chip(ax, cx - 0.05, 0.505, 0.10, 0.13, "Σ", fontsize=20, edge=BLUE, color=BLUE)
            ax.text(
                cx,
                0.475,
                "the same unit,\nthe same weights",
                fontsize=9.5,
                color=BLUE,
                ha="center",
                va="top",
                linespacing=1.3,
            )
            arrow(ax, (cx, 0.50), (cx, 0.40), color=FAINT, lw=1.6, mutation=12)

        if phase >= 1:
            ax.text(
                0.0,
                0.375,
                "one number per window",
                fontsize=10.5,
                color=FAINT,
                fontweight="bold",
                va="center",
            )
            shown = len(fmap) if phase >= 2 else (pos + 1 if pos is not None else 0)
            for i, val in enumerate(fmap[:shown]):
                top_hit = phase >= 2 and i == best
                ax.text(
                    word_x[i + 1],
                    0.31,
                    f"{val:+.2f}",
                    fontsize=13,
                    ha="center",
                    va="center",
                    color=GREEN if top_hit else SUB,
                    fontfamily="monospace",
                    fontweight="bold" if top_hit else "normal",
                )

        if phase >= 2:
            ax.text(
                0.0,
                0.21,
                f"keep the biggest  →  {fmap[best]:+.2f}   on the window "
                f'"{" ".join(C_SENT[best : best + C_K])}"',
                fontsize=13.5,
                color=GREEN,
                va="center",
            )
            ax.text(
                0.0,
                0.135,
                "This unit's weights learned one phrase. It found it, and it would find it "
                "anywhere in the sentence.",
                fontsize=12,
                color=SUB,
                va="center",
            )

        if phase >= 3:
            ax.text(
                0.0,
                0.03,
                "But it can only ever see three words at a time — and that is the whole problem.",
                fontsize=12.5,
                color=YELLOW,
                va="center",
            )

        math_strip(
            fig,
            r"$c_i \;=\; f\left(W \cdot x_{i:i+k-1} + b\right), "
            r"\qquad \hat{c} \;=\; \max_i \; c_i$",
            note="k = the window; the same W at every position",
        )
        footer(
            fig,
            "background for the transformer — not a study-guide entry · "
            "builds on: sliding-window · neural-network-and-layers",
        )
        return fig_to_pil(fig)

    frames, durations = [], []
    hold(frames, durations, lambda: render(None, 0), ms=900)
    for pos in range(len(fmap)):
        hold(frames, durations, lambda pos=pos: render(pos, 1), ms=800)
    for phase in (2, 3):
        hold(frames, durations, lambda phase=phase: render(best, phase), ms=1200)
    hold(frames, durations, lambda: render(best, 3), ms=1000)
    save_gif(frames, durations, "w03_s09_cnn.gif")


# =====================================================================
# SLIDE 10 — the RNN: the same unit, handed its own last answer
# =====================================================================
R_SENT = ["the", "film", "was", "not", "very", "good"]


def make_rnn():
    def render(step, phase):
        fig = new_fig()
        arch_frame(
            fig,
            3,
            "The recurrent network",
            "The same unit once more, with one extra input: its own answer from the word before.",
        )
        pros_cons(
            fig,
            PANEL_RECT,
            [
                "Any length of input, with no\npadding and no fixed window.",
                "Word order finally matters:\n'not good' "
                "and 'good not'\nare different computations.",
                "The hidden state is memory —\nthe first architecture here\nthat has any.",
            ],
            [
                "Strictly sequential. Word 40\nwaits for word "
                "39, so training\ncannot be parallelised.",
                "Early words fade. By the end\nof a long sentence the start\nhas washed out.",
                "In seq2seq the whole input\nmust fit through one fixed\nvector — the bottleneck.",
            ],
        )
        ax = blank_axes(fig, DEMO_RECT)

        xs = np.linspace(0.02, 0.80, len(R_SENT))
        ax.text(
            0.0,
            0.99,
            "one word at a time, left to right",
            fontsize=10.5,
            color=FAINT,
            fontweight="bold",
            va="top",
        )
        for i, (x, word) in enumerate(zip(xs, R_SENT, strict=True)):
            done = i <= step
            ax.text(
                x + 0.06,
                0.86,
                word,
                fontsize=12.5,
                ha="center",
                va="center",
                color=TEXT if done else FAINT,
                fontfamily="monospace",
                fontweight="bold" if i == step else "normal",
            )
            if done:
                arrow(ax, (x + 0.06, 0.805), (x + 0.06, 0.735), color=BLUE, lw=1.8, mutation=14)
            chip(
                ax,
                x,
                0.60,
                0.12,
                0.125,
                "Σ",
                fontsize=17,
                face="#2b3446" if done else PANEL,
                edge=BLUE if done else PANEL_EDGE,
                color=BLUE if done else FAINT,
                lw=2.0 if done else 1.2,
            )
            ax.text(
                x + 0.06,
                0.555,
                f"h{i + 1}",
                fontsize=10.5,
                color=BLUE if done else FAINT,
                ha="center",
                fontfamily="monospace",
            )
            if i:
                # The recurrence itself: the arrow that makes it an RNN.
                arrow(
                    ax,
                    (xs[i - 1] + 0.12, 0.6625),
                    (x, 0.6625),
                    color=BLUE if done else PANEL_EDGE,
                    lw=2.0 if done else 1.2,
                    mutation=12,
                )
        ax.text(
            0.0,
            0.50,
            "INSIDE EVERY BOX — slide 8's unit, with two inputs: this word and the box before it",
            fontsize=10.5,
            color=FAINT,
            fontweight="bold",
            va="top",
        )
        ax.text(
            0.0,
            0.435,
            "h_now  =  Σ( w × this word  +  u × h_before  +  b )   — the same w, u, b "
            "at every step",
            fontsize=12,
            color=TEXT,
            va="top",
            fontfamily="monospace",
        )
        ax.text(
            0.0,
            0.375,
            "so each h is a summary of the whole sentence so far, in one vector",
            fontsize=11,
            color=SUB,
            va="top",
        )

        if phase >= 1:
            arrow(ax, (0.935, 0.6625), (0.995, 0.6625), color=GREEN, lw=2.2, mutation=16)
            ax.text(
                0.985,
                0.535,
                "the decision is read\noff the last box alone",
                fontsize=10.5,
                color=GREEN,
                va="top",
                ha="right",
                linespacing=1.4,
            )

        if phase >= 2:
            ax.text(
                0.0,
                0.28,
                "two costs it never paid off",
                fontsize=10.5,
                color=FAINT,
                fontweight="bold",
                va="top",
            )
            ax.text(0.0, 0.20, "1", fontsize=13, color=RED, fontweight="bold", va="center")
            ax.text(
                0.045,
                0.20,
                "Sequential by construction — h5 cannot start until h4 exists. A GPU sits idle.",
                fontsize=12.5,
                color=SUB,
                va="center",
            )

        if phase >= 3:
            ax.text(0.0, 0.07, "2", fontsize=13, color=RED, fontweight="bold", va="center")
            ax.text(
                0.045,
                0.07,
                "Everything must survive the squeeze through one fixed-size vector, "
                "and the\nearly words do not. Long sentences degrade — the "
                "fixed-length bottleneck.",
                fontsize=12.5,
                color=SUB,
                va="center",
                linespacing=1.6,
            )

        math_strip(
            fig,
            r"$h_t \;=\; \tanh\left(W_h \, h_{t-1} + W_x \, x_t + b\right), "
            r"\qquad \hat{y} \;=\; \mathrm{softmax}(W_y \, h_T)$",
            note="the same W at every step",
        )
        footer(
            fig,
            "study guide: recurrent-neural-network · hidden-state · sequence-to-sequence · "
            "fixed-length-bottleneck",
        )
        return fig_to_pil(fig)

    frames, durations = [], []
    for step in range(len(R_SENT)):
        hold(frames, durations, lambda step=step: render(step, 0), ms=600)
    last = len(R_SENT) - 1
    for phase in (1, 2, 3):
        hold(frames, durations, lambda phase=phase: render(last, phase), ms=1300)
    hold(frames, durations, lambda: render(last, 3), ms=1000)
    save_gif(frames, durations, "w03_s10_rnn.gif")


if __name__ == "__main__":
    make_perceptron()
    make_cnn()
    make_rnn()
