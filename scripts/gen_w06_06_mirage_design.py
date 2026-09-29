"""Week 6, part 4: the mirage paper's claim, and the toy world it built to test it.

  w06_s25_hypothesis.gif        the hypothesis, one phrase at a time, in plain words
  w06_s26_paper_dataalchemy.gif Figure 2 as printed, and why anyone would build a toy
  w06_s27_dataalchemy.gif       the toy, running: ROT13, a shift, and a written step

Zhao et al.'s argument is hard going on the page because the notation arrives
before the reason for it. These slides reverse that. First the claim, glossed
phrase by phrase. Then the reason for the toy: "outside the training data"
cannot be tested on a model whose training data is secret, so they build the
data. Then the toy itself, with the paper's own example word (APPLE) put
through each operation on screen.

Every string is computed from mirage_toy.py, not typed.
"""

from mirage_toy import WORD, f1, f2
from paper_crops import crop
from style_dark import (
    BLUE,
    FAINT,
    GREEN,
    ORANGE,
    PANEL,
    PANEL_EDGE,
    SUB,
    TEXT,
    YELLOW,
    blank_axes,
    chip,
    ease,
    fig_to_pil,
    footer,
    hold,
    kicker_title,
    lerp,
    new_fig,
    panel_box,
    paper_card,
    save_gif,
    tween,
)

FOOT = "reading (optional): Zhao et al. 2025 (cot-mirage) · "


# ── s25: the hypothesis, in plain words ────────────────────────────────
GLOSS = [
    (
        "“a structured inductive bias”",
        "a learned lean — a habit of producing\nanswers of a particular shape",
        YELLOW,
    ),
    (
        "“learned from in-distribution data”",
        "picked up from the kind of examples it\npracticed on",
        BLUE,
    ),
    ("“conditionally generate”", "write, depending on the question in front\nof it,", GREEN),
    (
        "“reasoning trajectories that approximate\nthose observed during training”",
        "chains of steps that resemble the\nchains it saw in training",
        ORANGE,
    ),
]


def make_hypothesis():
    def render(n, closing):
        fig = new_fig()
        kicker_title(
            fig, "PART 4 · ZHAO ET AL. 2025, §3 · THE CLAIM", "The hypothesis, one phrase at a time"
        )
        fig.text(
            0.045,
            0.83,
            "“We hypothesize that CoT reasoning reflects a structured inductive bias learned "
            "from in-distribution data,\nenabling models to conditionally generate reasoning "
            "trajectories that approximate those observed during training.”",
            fontsize=14,
            color=SUB,
            va="top",
            style="italic",
            linespacing=1.5,
        )
        ax = blank_axes(fig, [0.045, 0.27, 0.91, 0.47])
        for i, (phrase, plain, colour) in enumerate(GLOSS[:n]):
            y = 0.97 - i * 0.25
            ax.text(
                0.0,
                y,
                phrase,
                fontsize=14.5,
                color=colour,
                va="top",
                style="italic",
                linespacing=1.3,
            )
            ax.text(0.47, y - 0.01, "→", fontsize=18, color=FAINT, va="top")
            ax.text(0.52, y, plain, fontsize=14.5, color=TEXT, va="top", linespacing=1.3)
        if closing:
            lo = blank_axes(fig, [0.045, 0.08, 0.91, 0.17])
            panel_box(lo, 0, 0, 1, 1, edge=ORANGE)
            lo.text(
                0.02,
                0.75,
                "In one sentence: the model writes steps that look like steps it has seen.",
                fontsize=16,
                color=ORANGE,
                fontweight="bold",
                va="center",
            )
            lo.text(
                0.02,
                0.32,
                "The prediction: chain of thought works when a question "
                "resembles the practice, and fails as it moves away —\nwhatever the size "
                "of the model. A “mirage”: from a distance it looks like reasoning.",
                fontsize=13,
                color=TEXT,
                va="center",
                linespacing=1.45,
            )
        footer(fig, FOOT + "§3 · study guide: out-of-distribution-generalization")
        return fig_to_pil(fig)

    frames, durations = [], []
    for n in range(len(GLOSS) + 1):
        hold(frames, durations, lambda n=n: render(n, False), ms=2200)
    hold(frames, durations, lambda: render(len(GLOSS), True), ms=1800, n=2)
    save_gif(frames, durations, "w06_s25_hypothesis.gif")


# ── s26: the figure, and why build a toy at all ────────────────────────
def make_paper_slide():
    img = crop("mirage_fig2_framework")
    points = [
        (
            "Why a toy?",
            "“Outside the training data” cannot be tested on a model whose\n"
            "training data is secret. So build the data, train the model on\n"
            "it from nothing, and know exactly what it has seen.",
            YELLOW,
        ),
        (
            "Three ways to step outside",
            "task — a new combination of operations\n"
            "length — longer or shorter words, more or fewer steps\n"
            "format — the prompt's own tokens inserted, deleted, changed",
            BLUE,
        ),
    ]

    def render(n):
        fig = new_fig()
        kicker_title(
            fig,
            "PART 4 · ZHAO ET AL. 2025, §4 · THE DESIGN",
            "A language with no internet in it",
            "DataAlchemy: 26 letters, two operations, and models trained from scratch.",
        )
        paper_card(
            fig,
            [0.057, 0.375, 0.886, 0.355],
            img,
            "Zhao et al. 2025, Figure 2 — the framework of DataAlchemy",
        )
        ax = blank_axes(fig, [0.045, 0.075, 0.91, 0.215])
        for i, (head, body, colour) in enumerate(points[:n]):
            x = 0.012 + i * 0.51
            ax.plot([x, x], [0.08, 0.98], color=colour, lw=3, alpha=0.7)
            ax.text(x + 0.02, 0.98, head, fontsize=15, color=colour, fontweight="bold", va="top")
            ax.text(x + 0.02, 0.77, body, fontsize=13, color=TEXT, va="top", linespacing=1.5)
        footer(fig, FOOT + "§4 · Fig. 2")
        return fig_to_pil(fig)

    frames, durations = [], []
    for n in range(len(points) + 1):
        hold(frames, durations, lambda n=n: render(n), ms=1500)
    hold(frames, durations, lambda: render(len(points)), ms=1800, n=2)
    save_gif(frames, durations, "w06_s26_paper_dataalchemy.gif")


# ── s27: the toy, running ──────────────────────────────────────────────
CELL, GAP = 0.045, 0.02


def letter_row(ax, x0, y, letters, colour=BLUE, face=PANEL, alpha=1.0, xs=None, ys=None):
    """A word as a row of letter tiles; `xs`/`ys` override single tile positions."""
    for i, c in enumerate(letters):
        x = x0 + i * (CELL + GAP) if xs is None else xs[i]
        yy = y if ys is None else ys[i]
        chip(
            ax,
            x,
            yy,
            CELL,
            0.12,
            c,
            face=face,
            edge=colour,
            color=TEXT,
            fontsize=19,
            mono=True,
            bold=True,
            lw=2.0,
            alpha=alpha,
        )


def make_machinery():
    rot_out = f1(WORD)
    chain_mid, chain_out = f1(WORD), f2(f1(WORD))
    query = f"{' '.join(WORD)} [F1] [F2] <think>"
    response_tokens = [*chain_mid, "[F2]", "<answer>", *chain_out]

    def render(rot=0.0, shift=0.0, chain=0.0, typed=0):
        fig = new_fig()
        kicker_title(
            fig,
            "PART 4 · §4 · THE TOY, RUNNING",
            "Two verbs, and a place to write the steps down",
            "The paper's own word, put through each operation it defines.",
        )
        ax = blank_axes(fig, [0.045, 0.10, 0.91, 0.72])
        x_in, x_out = 0.26, 0.66

        # Row 1: f1, ROT13. Each tile turns over to its partner 13 letters on,
        # left to right, like a counter ticking.
        y1 = 0.80
        ax.text(
            0.0, y1 + 0.09, "f1 · ROT13", fontsize=17, color=YELLOW, fontweight="bold", va="center"
        )
        ax.text(
            0.0,
            y1 + 0.02,
            "every letter moves 13 places on\nthe alphabet, wrapping round",
            fontsize=12,
            color=SUB,
            va="center",
            linespacing=1.4,
        )
        if rot:
            letter_row(ax, x_in, y1, WORD)
            ax.annotate(
                "",
                xy=(x_out - 0.02, y1 + 0.06),
                xytext=(x_in + 5 * (CELL + GAP) + 0.005, y1 + 0.06),
                arrowprops=dict(arrowstyle="-|>", color=YELLOW, lw=2.2),
            )
            for i, c in enumerate(WORD):
                t = min(1.0, max(0.0, rot * 6 - i))  # staggered
                shown = rot_out[i] if t >= 0.5 else c
                chip(
                    ax,
                    x_out + i * (CELL + GAP),
                    y1,
                    CELL,
                    0.12,
                    shown,
                    face=PANEL,
                    edge=YELLOW if t >= 0.5 else PANEL_EDGE,
                    color=TEXT,
                    fontsize=19,
                    mono=True,
                    bold=True,
                    lw=2.0,
                    alpha=0.35 + 0.65 * abs(2 * t - 1),
                )
                if 0 < t < 1:
                    ax.text(
                        x_out + i * (CELL + GAP) + CELL / 2,
                        y1 + 0.15,
                        "+13",
                        ha="center",
                        fontsize=11,
                        color=YELLOW,
                        alpha=1 - abs(2 * t - 1),
                    )

        # Row 2: f2, the shift. The tiles slide left one place and the first
        # one arcs over the top to the end -- motion, not a relabelling.
        y2 = 0.50
        ax.text(
            0.0,
            y2 + 0.09,
            "f2 · cyclic shift",
            fontsize=17,
            color=BLUE,
            fontweight="bold",
            va="center",
        )
        ax.text(
            0.0,
            y2 + 0.02,
            "every letter moves one place\nleft; the first goes to the end",
            fontsize=12,
            color=SUB,
            va="center",
            linespacing=1.4,
        )
        if shift:
            letter_row(ax, x_in, y2, WORD, alpha=1.0)
            ax.annotate(
                "",
                xy=(x_out - 0.02, y2 + 0.06),
                xytext=(x_in + 5 * (CELL + GAP) + 0.005, y2 + 0.06),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.2),
            )
            step = CELL + GAP
            xs, ys = [], []
            for i in range(len(WORD)):
                start = x_out + i * step
                if i == 0:
                    end = x_out + (len(WORD) - 1) * step
                    xs.append(lerp(start, end, shift))
                    ys.append(y2 + 0.16 * (1 - (2 * ease(shift) - 1) ** 2))
                else:
                    xs.append(lerp(start, start - step, shift))
                    ys.append(y2)
            letter_row(ax, 0, y2, WORD, xs=xs, ys=ys)

        # Row 3: both, with the step written down. This is the paper's CoT format.
        y3 = 0.17
        if chain:
            ax.text(
                0.0,
                y3 + 0.13,
                "Chain them — and write the middle step down. That is the chain of thought here:",
                fontsize=15,
                color=TEXT,
                va="center",
                alpha=chain,
            )
            ax.text(
                0.0,
                y3 + 0.02,
                "prompt",
                fontsize=11.5,
                color=FAINT,
                va="center",
                fontweight="bold",
                alpha=chain,
            )
            ax.text(
                0.10,
                y3 + 0.02,
                query,
                fontsize=17,
                color=BLUE,
                va="center",
                fontfamily="monospace",
                alpha=chain,
            )
            ax.text(
                0.0,
                y3 - 0.08,
                "model",
                fontsize=11.5,
                color=FAINT,
                va="center",
                fontweight="bold",
                alpha=chain,
            )
            x = 0.10
            for j, tok in enumerate(response_tokens[:typed]):
                colour = (
                    YELLOW if j < len(chain_mid) else (SUB if tok.startswith(("[", "<")) else GREEN)
                )
                ax.text(
                    x,
                    y3 - 0.08,
                    tok,
                    fontsize=17,
                    color=colour,
                    va="center",
                    fontfamily="monospace",
                    fontweight="bold" if colour == GREEN else "normal",
                )
                x += 0.00975 * (len(tok) + 1)  # one monospace cell at 17pt
            if typed >= len(response_tokens):
                ax.text(
                    0.10,
                    y3 - 0.16,
                    "the step (f1 applied)  ·  what is left to do  ·  "
                    "the answer (f2 applied to the step)",
                    fontsize=11.5,
                    color=SUB,
                    va="center",
                    style="italic",
                )

        footer(fig, FOOT + "§4.2 Definitions 4.1–4.3 · CoT format from Appendix E")
        return fig_to_pil(fig)

    frames, durations = [], []
    hold(frames, durations, lambda: render(), ms=1000)
    tween(frames, durations, lambda t: render(rot=t), n=24, ms=55)
    hold(frames, durations, lambda: render(rot=1), ms=1600)
    tween(frames, durations, lambda t: render(rot=1, shift=t), n=18, ms=55)
    hold(frames, durations, lambda: render(rot=1, shift=1), ms=1600)
    tween(frames, durations, lambda t: render(rot=1, shift=1, chain=t), n=8)
    for k in range(1, 5 + 2 + 5 + 1):
        hold(frames, durations, lambda k=k: render(rot=1, shift=1, chain=1, typed=k), ms=220)
    hold(frames, durations, lambda: render(rot=1, shift=1, chain=1, typed=99), ms=1800, n=2)
    save_gif(frames, durations, "w06_s27_dataalchemy.gif")


if __name__ == "__main__":
    make_hypothesis()
    make_paper_slide()
    make_machinery()
