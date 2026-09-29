"""Week 6, part 2: the evidence that chain of thought works, and its authors' caution.

  w06_s12_benchmark.gif     what a benchmark is; GSM8K; which "58%" is which
  w06_s13_emergence.gif     Wei's Table 2 redrawn: it hurts small models, helps big ones
  w06_s14_ablation_idea.gif what an ablation is -- a recipe first, then Wei's own grid
  w06_s17_caveats.gif       Section 6 and the hand-checked chains: the cautious inventors

The ablation itself (Figure 5, from the paper and redrawn) is gen_w06_04_ablation.py;
s14 exists so that students meet the *idea* of an ablation on something they
already understand -- a cake -- before they meet it on a bar chart.

Numbers: GSM8K solve rates are Wei et al. Table 2 (by model size) and Table 1
(PaLM 540B with the external calculator, 58.6). The prior best (55%) and the
self-consistency figure are from the Google Research blog post. The audit of
50 correct and 50 incorrect chains is Wei §3.2.
"""

import numpy as np
from matplotlib.patches import Rectangle
from paper_crops import crop
from style_dark import (
    BLUE,
    FAINT,
    GREEN,
    GRID,
    ORANGE,
    PANEL_EDGE,
    RED,
    SUB,
    TEXT,
    YELLOW,
    blank_axes,
    fig_to_pil,
    footer,
    hold,
    kicker_title,
    new_fig,
    panel_box,
    paper_card,
    save_gif,
    tween,
)

WEI = "reading: Wei et al. 2022 (wei-2022-chain-of-thought)"


def plain_axes(fig, rect, xlim, ylim):
    ax = fig.add_axes(rect)
    ax.set_facecolor("none")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(FAINT)
    ax.tick_params(colors=SUB, labelsize=12, length=0, pad=6)
    return ax


# ── s12: a benchmark ────────────────────────────────────────────────────
BARS = [
    ("PaLM 540B,\nstandard", 17.9, YELLOW),
    ("PaLM 540B,\nchain of thought", 56.9, ORANGE),
    ("… plus a\ncalculator", 58.6, ORANGE),
]


def make_benchmark():
    def render(n_terms, n_bars, which58):
        fig = new_fig()
        kicker_title(
            fig, "PART 2 · HOW DO YOU KNOW IT WORKS?", "A benchmark: the same exam, for every model"
        )
        ax = blank_axes(fig, [0.045, 0.10, 0.44, 0.70])
        terms = [
            (
                "benchmark",
                "A fixed set of questions with known answers.\nEveryone scores on the "
                "same set, so scores\ncan be compared.",
            ),
            (
                "GSM8K",
                "About 8,500 grade-school math word problems\n(Cobbe et al. 2021), each "
                "needing several steps.\nWei et al.'s headline test.",
            ),
            ("solve rate", "The percentage of the test problems a model\nanswers correctly."),
            (
                "state of the art",
                "The best published score so far. Before this\npaper: 55%, by "
                "a GPT-3 model trained further\nfor exactly this task.",
            ),
        ]
        for i, (term, gloss) in enumerate(terms[:n_terms]):
            y = 0.98 - i * 0.25
            ax.text(0.0, y, term, fontsize=16, color=BLUE, fontweight="bold", va="top")
            ax.text(0.0, y - 0.06, gloss, fontsize=12.5, color=TEXT, va="top", linespacing=1.4)

        if n_bars:
            bx = plain_axes(fig, [0.56, 0.27, 0.40, 0.47], (-0.6, 2.6), (0, 70))
            bx.set_xticks(range(len(BARS)))
            bx.set_xticklabels([b[0] for b in BARS], fontsize=11)
            bx.set_yticks([0, 20, 40, 60])
            bx.set_yticklabels(["0%", "20%", "40%", "60%"])
            for yv in (20, 40, 60):
                bx.axhline(yv, color=GRID, lw=0.8, zorder=0)
            bx.axhline(55, color=ORANGE, ls=(0, (4, 4)), lw=1.4, alpha=0.8)
            bx.text(
                -0.55, 56.0, "prior best 55%", fontsize=11, color=ORANGE, ha="left", va="bottom"
            )
            for i, (_, v, c) in enumerate(BARS[:n_bars]):
                bx.bar(i, v, width=0.62, color=c, alpha=0.55 if i == 2 else 1.0)
                bx.text(i, v + 1.2, f"{v}%", ha="center", fontsize=13, color=c, fontweight="bold")
            fig.text(0.56, 0.78, "GSM8K solve rate", fontsize=12, color=FAINT, fontweight="bold")
        if which58:
            fig.text(
                0.56,
                0.165,
                "Google's blog says “58%”. That is the calculator column: a program\n"
                "did the arithmetic in the model's chain (Wei Table 1). The model\n"
                "alone: 56.9%. When you cite a number, cite which one.",
                fontsize=12,
                color=TEXT,
                va="top",
                linespacing=1.45,
            )
        footer(fig, WEI + " · Tables 1–2 · Google Research blog · study guide: benchmark")
        return fig_to_pil(fig)

    frames, durations = [], []
    for n in range(1, 5):
        hold(frames, durations, lambda n=n: render(n, 0, False), ms=1700)
    for b in range(1, 4):
        hold(frames, durations, lambda b=b: render(4, b, False), ms=1300)
    hold(frames, durations, lambda: render(4, 3, True), ms=1800, n=2)
    save_gif(frames, durations, "w06_s12_benchmark.gif")


# ── s13: emergence ──────────────────────────────────────────────────────
# GSM8K solve rate (%), Wei et al. Table 2: (billions of parameters, standard, CoT).
GPT = [(0.35, 2.2, 0.5), (1.3, 2.4, 0.5), (6.7, 4.0, 2.4), (175, 15.6, 46.9)]
PALM = [(8, 4.9, 4.1), (62, 9.6, 29.9), (540, 17.9, 56.9)]


def make_emergence():
    img = crop("wei_fig4_scale")

    def render(t, notes):
        fig = new_fig()
        kicker_title(
            fig,
            "PART 2 · WEI ET AL. 2022, FIGURE 4 / TABLE 2",
            "It only works on big models — and hurts small ones",
            "Parameters are the numbers inside a model that training sets. Their "
            "count is the model's size.",
        )
        ax = plain_axes(fig, [0.075, 0.17, 0.50, 0.56], (0.25, 900), (0, 62))
        ax.set_xscale("log")
        ax.set_xticks([0.35, 1, 10, 100, 540])
        ax.set_xticklabels(["0.35B", "1B", "10B", "100B", "540B"])
        ax.set_yticks([0, 20, 40, 60])
        ax.set_yticklabels(["0%", "20%", "40%", "60%"])
        for yv in (20, 40, 60):
            ax.axhline(yv, color=GRID, lw=0.8, zorder=0)
        ax.set_xlabel("model size (parameters, log scale)", color=SUB, fontsize=12)
        ax.set_ylabel("GSM8K solve rate", color=SUB, fontsize=12)
        # Reveal the curves left to right, as model size grows.
        xmax = np.exp(np.log(0.3) + (np.log(900) - np.log(0.3)) * t)
        for series, mark, name in ((GPT, "o", "GPT"), (PALM, "s", "PaLM")):
            pts = [p for p in series if p[0] <= xmax]
            if not pts:
                continue
            xs = [p[0] for p in pts]
            ax.plot(xs, [p[1] for p in pts], color=YELLOW, marker=mark, lw=2, ms=7)
            ax.plot(xs, [p[2] for p in pts], color=ORANGE, marker=mark, lw=2.4, ms=7)
            if pts[-1] == series[-1]:
                ax.text(xs[-1] * 1.15, pts[-1][2], name, color=ORANGE, fontsize=12, va="center")
        ax.text(0.3, 58, "— chain of thought", color=ORANGE, fontsize=12)
        ax.text(0.3, 53, "— standard", color=YELLOW, fontsize=12)
        if notes >= 1:
            ax.axvspan(0.25, 10, color=RED, alpha=0.07, lw=0)
            ax.text(
                0.4,
                22,
                "below ~10B: every model\ndid worse with a chain",
                fontsize=12,
                color=RED,
                linespacing=1.35,
            )
        if notes >= 2:
            paper_card(fig, [0.63, 0.47, 0.33, 0.26], img, "Wei et al. 2022, Figure 4 (GSM8K row)")
            rp = blank_axes(fig, [0.62, 0.10, 0.35, 0.30])
            rp.text(
                0.0,
                0.95,
                "an emergent ability",
                fontsize=15,
                color=BLUE,
                fontweight="bold",
                va="top",
            )
            rp.text(
                0.0,
                0.77,
                "one that is absent in small models\nand appears above some size, "
                "rather\nthan improving gradually.",
                fontsize=12.5,
                color=TEXT,
                va="top",
                linespacing=1.4,
            )
            rp.text(
                0.0,
                0.33,
                "Smaller models “produced fluent but\nillogical chains of thought” — Wei §3.2",
                fontsize=12,
                color=ORANGE,
                va="top",
                style="italic",
                linespacing=1.4,
            )
        footer(fig, WEI + " · Table 2 · study guide: emergent-abilities · parameters-and-weights")
        return fig_to_pil(fig)

    frames, durations = [], []
    hold(frames, durations, lambda: render(0.0, 0), ms=1400)
    tween(frames, durations, lambda t: render(t, 0), n=24, ms=70)
    hold(frames, durations, lambda: render(1.0, 0), ms=1400)
    hold(frames, durations, lambda: render(1.0, 1), ms=2200)
    hold(frames, durations, lambda: render(1.0, 2), ms=1800, n=2)
    save_gif(frames, durations, "w06_s13_emergence.gif")


# ── s14: what an ablation is ────────────────────────────────────────────
CAKE_COLS = ["baking powder", "eggs", "hot oven"]
CAKE_ROWS = [
    ("the full recipe", (1, 1, 1), "rises", GREEN),
    ("no baking powder", (0, 1, 1), "flat", RED),
    ("no eggs", (1, 0, 1), "rises", GREEN),
    ("cool oven", (1, 1, 0), "flat", RED),
]
WEI_COLS = ["equations", "words", "extra length\nbefore the answer"]
WEI_ROWS = [
    ("standard prompting", (0, 0, 0), "17.9%", YELLOW),
    ("equation only", (1, 0, 1), "≈22%", SUB),
    ("variable compute only", (0, 0, 1), "≈18%", SUB),
    ("reasoning after answer", (1, 1, 0), "≈18%", SUB),
    ("chain of thought", (1, 1, 1), "56.9%", ORANGE),
]


def grid(ax, cols, rows, n_rows, result_head, y0=0.84, row_h=0.13, reveal_result=True):
    for j, c in enumerate(cols):
        ax.text(
            0.38 + j * 0.16,
            y0 + 0.08,
            c,
            fontsize=12,
            color=SUB,
            ha="center",
            va="bottom",
            linespacing=1.2,
        )
    ax.text(0.90, y0 + 0.08, result_head, fontsize=12, color=SUB, ha="center", va="bottom")
    for i, (name, marks, result, colour) in enumerate(rows[:n_rows]):
        y = y0 - i * row_h
        ax.text(0.0, y, name, fontsize=14, color=TEXT, va="center")
        for j, m in enumerate(marks):
            ax.text(
                0.38 + j * 0.16,
                y,
                "✓" if m else "✗",
                fontsize=17,
                ha="center",
                va="center",
                color=GREEN if m else RED,
            )
        if reveal_result:
            ax.text(
                0.90,
                y,
                result,
                fontsize=15,
                ha="center",
                va="center",
                color=colour,
                fontweight="bold",
            )
    ax.plot([0, 1], [y0 + 0.05, y0 + 0.05], color=PANEL_EDGE, lw=1)


def make_ablation_idea():
    def render(stage):
        fig = new_fig()
        if stage < 6:
            kicker_title(
                fig,
                "PART 2 · A WORD YOU NEED: ABLATION",
                "Take one ingredient out at a time",
                "Why did the cake rise? Bake it again with one thing missing, keep "
                "everything else the same, and compare.",
            )
            ax = blank_axes(fig, [0.045, 0.30, 0.60, 0.48])
            grid(ax, CAKE_COLS, CAKE_ROWS, min(stage, 4), "result", y0=0.80, row_h=0.18)
            if stage >= 5:
                rp = blank_axes(fig, [0.68, 0.30, 0.28, 0.48])
                for i, (term, gloss) in enumerate(
                    [
                        ("control", "the full recipe — what\neverything is compared to"),
                        ("ablation", "a copy with one part\nremoved or replaced"),
                        (
                            "the rule",
                            "change one thing at a\ntime, or you cannot tell\nwhich one mattered",
                        ),
                    ]
                ):
                    y = 0.98 - i * 0.34
                    rp.text(0.0, y, term, fontsize=15, color=BLUE, fontweight="bold", va="top")
                    rp.text(
                        0.0, y - 0.09, gloss, fontsize=12.5, color=TEXT, va="top", linespacing=1.4
                    )
                fig.text(
                    0.045,
                    0.21,
                    "Verdict: baking powder and heat matter; the eggs were not why it rose.",
                    fontsize=15,
                    color=TEXT,
                    fontweight="bold",
                )
        else:
            kicker_title(
                fig,
                "PART 2 · THE SAME IDEA, ON A PROMPT",
                "Wei et al.'s ablation, as an ingredient grid",
                "Each prompt keeps some parts of a chain of thought and drops others. "
                "GSM8K, PaLM 540B.",
            )
            ax = blank_axes(fig, [0.045, 0.14, 0.70, 0.60])
            grid(
                ax,
                WEI_COLS,
                WEI_ROWS,
                len(WEI_ROWS),
                "solve rate",
                y0=0.80,
                row_h=0.15,
                reveal_result=stage >= 7,
            )
            if stage >= 8:
                rp = blank_axes(fig, [0.77, 0.20, 0.20, 0.52])
                rp.text(
                    0.0,
                    0.95,
                    "No single\ningredient\ndoes it.",
                    fontsize=16,
                    color=ORANGE,
                    fontweight="bold",
                    va="top",
                    linespacing=1.3,
                )
                rp.text(
                    0.0,
                    0.50,
                    "Only the full\ncombination —\nequations in words,\nbefore "
                    "the answer —\nmoves the score.",
                    fontsize=13,
                    color=TEXT,
                    va="top",
                    linespacing=1.4,
                )
            fig.text(
                0.045,
                0.085,
                "≈ read off Figure 5; the paper tables these for LaMDA "
                "only. Next: the figure itself.",
                fontsize=11,
                color=FAINT,
            )
        footer(fig, WEI + " · §3.3 · study guide: ablation-study")
        return fig_to_pil(fig)

    frames, durations = [], []
    for stage, ms in (
        (0, 1500),
        (1, 1200),
        (2, 1400),
        (3, 1400),
        (4, 1400),
        (5, 2400),
        (6, 2600),
        (7, 1800),
        (8, 1800),
    ):
        hold(frames, durations, lambda s=stage: render(s), ms=ms)
    hold(frames, durations, lambda: render(8), ms=1800, n=2)
    save_gif(frames, durations, "w06_s14_ablation_idea.gif")


# ── s17: the cautious inventors ─────────────────────────────────────────
CAVEATS = [
    (
        "“this does not answer whether the neural network is actually\n‘reasoning,’ which we "
        "leave as an open question.”",
        ORANGE,
    ),
    (
        "“there is no guarantee of correct reasoning paths, which can\nlead to both correct and "
        "incorrect answers”",
        ORANGE,
    ),
    (
        "“the emergence of chain-of-thought reasoning only at large model\nscales makes it costly "
        "to serve in real-world applications”",
        SUB,
    ),
    (
        "writing chains by hand is cheap for eight examples, but “could be\nprohibitive for "
        "finetuning”",
        SUB,
    ),
]


def make_caveats():
    def render(n, audit):
        fig = new_fig()
        kicker_title(
            fig,
            "PART 2 · WEI ET AL. 2022, §6 “DISCUSSION”",
            "The inventors are the cautious ones",
            "The vendor pages say the model “reasons”. The people who invented the "
            "technique would not.",
        )
        ax = blank_axes(fig, [0.045, 0.10, 0.56, 0.68])
        ax.text(
            0.0,
            0.99,
            "Their own four limitations",
            fontsize=14,
            color=FAINT,
            fontweight="bold",
            va="top",
        )
        for i, (q, colour) in enumerate(CAVEATS[:n]):
            y = 0.89 - i * 0.22
            ax.plot([0, 0], [y - 0.13, y], color=colour, lw=3, alpha=0.8)
            ax.text(
                0.025,
                y,
                q,
                fontsize=13,
                color=TEXT if colour == ORANGE else SUB,
                va="top",
                linespacing=1.45,
                style="italic",
            )
        if audit:
            rp = blank_axes(fig, [0.64, 0.14, 0.32, 0.62])
            panel_box(rp, 0, 0, 1, 1, edge=BLUE)
            rp.text(
                0.06,
                0.93,
                "They also checked by hand",
                fontsize=14,
                color=BLUE,
                fontweight="bold",
                va="top",
            )
            rp.text(
                0.06,
                0.80,
                "50 chains where LaMDA 137B\ngot the answer right:",
                fontsize=12.5,
                color=TEXT,
                va="top",
                linespacing=1.4,
            )
            for k in range(50):
                r, c = divmod(k, 10)
                colour = RED if k >= 48 else GREEN
                rp.add_patch(
                    Rectangle((0.08 + c * 0.085, 0.50 - r * 0.06), 0.065, 0.045, color=colour, lw=0)
                )
            rp.text(
                0.06,
                0.20,
                "48 sound chains. 2 reached the\nright answer by coincidence.",
                fontsize=12.5,
                color=TEXT,
                va="top",
                linespacing=1.4,
            )
            rp.text(0.06, 0.07, "Wei §3.2", fontsize=11, color=FAINT, va="top")
        footer(fig, WEI + " · §3.2, §6 · study guide: chain-of-thought-prompting")
        return fig_to_pil(fig)

    frames, durations = [], []
    for n in range(len(CAVEATS) + 1):
        hold(frames, durations, lambda n=n: render(n, False), ms=2000)
    hold(frames, durations, lambda: render(len(CAVEATS), True), ms=1800, n=2)
    save_gif(frames, durations, "w06_s17_caveats.gif")


if __name__ == "__main__":
    make_benchmark()
    make_emergence()
    make_ablation_idea()
    make_caveats()
