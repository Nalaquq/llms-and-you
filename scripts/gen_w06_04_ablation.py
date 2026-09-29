"""Week 6: Wei et al.'s ablation, shown from the paper and then taken apart.

  w06_s15_paper_ablation.gif   Figure 5 as printed, beside the five prompts it compares
  w06_s16_ablation.gif         the same result redrawn: three stories, each ruled out

The ablation is the best piece of research design in the week's reading, and
the easiest to skim past -- it is one small figure. So it gets two slides. The
first shows the figure the students met, with the five conditions spelled out
on one worked problem (Wei's own, from Figure 1), because the figure's legend
names the conditions without showing what any of them looks like. The second
redraws the PaLM half as a sequence of suspects: a story for where chain of
thought's gain comes from, the bar that story predicts, and the verdict.

The last beat is the one the debate turns on: ruling out three explanations
does not prove the fourth. Wei et al. say as much themselves in Section 6, and
the mirage paper is an attempt at the experiment that would.

Numbers. PaLM 540B's standard (17.9) and chain-of-thought (56.9) GSM8K rates
are from the paper's Table 2. The paper does not tabulate PaLM's ablations --
Table 6 gives them for LaMDA 137B only -- so those three bars are read off
Figure 5, calibrated against the two tabulated bars (error under a point), and
the slide marks them with a ≈. Saying so on the slide is part of the lesson.
"""

from matplotlib.patches import Rectangle
from paper_crops import crop
from style_dark import (
    FAINT,
    GRID,
    ORANGE,
    PANEL,
    PANEL_EDGE,
    PURPLE,
    RED,
    SUB,
    TEXT,
    YELLOW,
    blank_axes,
    chip,
    ease,
    fig_to_pil,
    footer,
    hold,
    new_fig,
    paper_card,
    save_gif,
    tween,
)

ABLATION_GREY = "#8fa3c0"  # the three ablations: one quiet colour, as in the paper's hatching

FOOT = "reading: Wei et al. 2022 (wei-2022-chain-of-thought) · §3.3 Ablation Study · Fig. 5"

# Wei's Figure 1 problem, answered five ways. Only the text before the answer
# changes; that is the whole design.
QUESTION = (
    "Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls.\n"
    "Each can has 3 tennis balls. How many tennis balls does he have now?"
)
CONDITIONS = [
    ("Standard prompting", YELLOW, "The answer is 11.", "the baseline"),
    (
        "Equation only",
        ABLATION_GREY,
        "5 + 2 * 3 = 11. The answer is 11.",
        "keeps the math, drops the words",
    ),
    (
        "Variable compute only",
        ABLATION_GREY,
        ".............. The answer is 11.",
        "keeps the length, drops the content",
    ),
    (
        "Reasoning after answer",
        ABLATION_GREY,
        "The answer is 11. Roger started with 5 balls…",
        "keeps the words, drops the order",
    ),
    (
        "Chain-of-thought prompting",
        ORANGE,
        "Roger started with 5 balls. 2 cans of 3 is 6.\n5 + 6 = 11. The answer is 11.",
        "all of it",
    ),
]


def make_paper_slide():
    img = crop("wei_fig5_ablation")

    def render(n_rows):
        fig = new_fig()
        fig.text(
            0.045,
            0.945,
            "PART 2 · WEI ET AL. 2022, §3.3 · THE ABLATION",
            fontsize=13,
            color=PURPLE,
            fontweight="bold",
            va="top",
        )
        fig.text(
            0.045,
            0.895,
            "It works. Which part of it is doing the work?",
            fontsize=30,
            color=TEXT,
            fontweight="bold",
            va="top",
        )
        fig.text(
            0.045,
            0.838,
            "Take the prompt apart. Remove one ingredient at a time and see if the gain survives.",
            fontsize=15.5,
            color=SUB,
            va="top",
        )
        paper_card(
            fig,
            [0.057, 0.135, 0.25, 0.60],
            img,
            "Wei et al. 2022, Figure 5 — GSM8K math word problems",
        )

        ax = blank_axes(fig, [0.345, 0.085, 0.615, 0.70])
        ax.text(0.0, 0.985, QUESTION, fontsize=12.5, color=SUB, va="top", linespacing=1.45)
        ax.text(
            0.0,
            0.855,
            "…and what each prompt teaches the model to write before its answer:",
            fontsize=11.5,
            color=FAINT,
            va="top",
        )
        top, step = 0.785, 0.158
        for i, (name, colour, answer, keeps) in enumerate(CONDITIONS[:n_rows]):
            y = top - i * step
            ax.add_patch(Rectangle((0.0, y - 0.035), 0.018, 0.035, color=colour, lw=0))
            ax.text(0.03, y, name, fontsize=14, color=TEXT, fontweight="bold", va="top")
            ax.text(
                0.03,
                y - 0.048,
                "A: " + answer,
                fontsize=12,
                color=TEXT,
                va="top",
                fontfamily="monospace",
                linespacing=1.35,
            )
            ax.text(1.0, y, keeps, fontsize=12, color=colour, va="top", ha="right", style="italic")
        footer(fig, FOOT)
        return fig_to_pil(fig)

    frames, durations = [], []
    hold(frames, durations, lambda: render(0), ms=1500)
    for n in range(1, len(CONDITIONS) + 1):
        hold(frames, durations, lambda n=n: render(n), ms=1100)
    hold(frames, durations, lambda: render(len(CONDITIONS)), ms=1800, n=2)
    save_gif(frames, durations, "w06_s15_paper_ablation.gif")


# ── The redraw ─────────────────────────────────────────────────────────
STANDARD, COT = 17.9, 56.9
# (story, what it would predict, the bar Figure 5 shows, the verdict)
SUSPECTS = [
    ("Equation only", "It just writes down the sum.", 22.0),
    ("Variable compute only", "It just gets more tokens to think with.", 18.0),
    ("Reasoning after answer", "The steps just wake up what it already knows.", 18.0),
]
BAR_X = [0, 1.25, 2.25, 3.25, 4.5]  # standard, three ablations, chain of thought
BAR_W = 0.8


def make_redraw():
    def render(std_t=0.0, cot_t=0.0, gap_t=0.0, suspects=(), closing=0.0):
        """`suspects`: one (grow, verdict) pair of 0..1 values per suspect shown."""
        fig = new_fig()
        fig.text(
            0.045,
            0.945,
            "PART 2 · WEI ET AL. 2022, FIGURE 5, REDRAWN",
            fontsize=13,
            color=PURPLE,
            fontweight="bold",
            va="top",
        )
        fig.text(
            0.045,
            0.895,
            "Three stories for the gain, and what happened to each",
            fontsize=30,
            color=TEXT,
            fontweight="bold",
            va="top",
        )
        fig.text(
            0.045,
            0.838,
            "PaLM 540B on GSM8K: the share of math word problems solved.",
            fontsize=15.5,
            color=SUB,
            va="top",
        )

        # Bars. A plain axes rather than a plane(): the y scale is data here.
        ax = fig.add_axes([0.075, 0.215, 0.41, 0.545])
        ax.set_facecolor("none")
        ax.set_xlim(-0.6, 5.1)
        ax.set_ylim(0, 64)
        for s in ("top", "right", "bottom"):
            ax.spines[s].set_visible(False)
        ax.spines["left"].set_color(FAINT)
        ax.set_yticks([0, 20, 40, 60])
        ax.set_yticklabels(["0%", "20%", "40%", "60%"], color=SUB, fontsize=12)
        ax.tick_params(axis="y", length=0, pad=8)
        ax.set_xticks([])
        for yv in (20, 40, 60):
            ax.axhline(yv, color=GRID, lw=0.8, zorder=0)
        ax.axhline(0, color=FAINT, lw=1.2)

        def bar(x, h, colour, label, value_text, alpha=1.0):
            ax.add_patch(
                Rectangle((x - BAR_W / 2, 0), BAR_W, h, color=colour, alpha=alpha, lw=0, zorder=2)
            )
            ax.text(x, -2.5, label, ha="center", va="top", fontsize=11, color=SUB, linespacing=1.25)
            if value_text:
                ax.text(
                    x,
                    h + 1.2,
                    value_text,
                    ha="center",
                    va="bottom",
                    fontsize=13,
                    color=colour,
                    fontweight="bold",
                    alpha=alpha,
                )

        if std_t:
            h = STANDARD * ease(std_t)
            bar(BAR_X[0], h, YELLOW, "standard", f"{h:.1f}" if std_t >= 1 else "")
        if cot_t:
            h = COT * ease(cot_t)
            bar(BAR_X[4], h, ORANGE, "chain of\nthought", f"{h:.1f}" if cot_t >= 1 else "")

        # The gap: a dashed baseline across, and a bracket on the right.
        if gap_t:
            ax.plot(
                [BAR_X[0] - BAR_W / 2, BAR_X[4] + BAR_W / 2],
                [STANDARD, STANDARD],
                ls=(0, (4, 4)),
                color=YELLOW,
                lw=1.3,
                alpha=0.7 * gap_t,
                zorder=3,
            )
            top = STANDARD + (COT - STANDARD) * ease(gap_t)
            bx = BAR_X[4] + BAR_W / 2 + 0.18
            ax.plot([bx, bx], [STANDARD, top], color=ORANGE, lw=2.2, clip_on=False)
            for yy in (STANDARD, top):
                ax.plot([bx - 0.08, bx], [yy, yy], color=ORANGE, lw=2.2, clip_on=False)
            ax.text(
                bx + 0.12,
                (STANDARD + COT) / 2,
                "+39\npoints",
                fontsize=14,
                color=ORANGE,
                fontweight="bold",
                va="center",
                alpha=gap_t,
                clip_on=False,
            )

        for i, (grow, verdict) in enumerate(suspects):
            name, _, value = SUSPECTS[i]
            h = value * ease(grow)
            short = name.replace(" only", "\nonly").replace(" after", "\nafter")
            bar(
                BAR_X[1 + i],
                h,
                ABLATION_GREY,
                short.lower(),
                f"≈{value:.0f}" if grow >= 1 else "",
                alpha=1.0 - 0.45 * verdict,
            )

        # Suspects panel.
        rp = blank_axes(fig, [0.555, 0.17, 0.40, 0.60])
        if gap_t >= 1:
            rp.text(
                0.0,
                0.99,
                "Where do the 39 points come from?",
                fontsize=16,
                color=TEXT,
                fontweight="bold",
                va="top",
            )
        for i, (_grow, verdict) in enumerate(suspects):
            name, story, value = SUSPECTS[i]
            y = 0.80 - i * 0.215
            dim = 1.0 - 0.55 * verdict
            chip(
                rp,
                0.012,
                y - 0.075,
                0.07,
                0.10,
                f"{i + 1}",
                face=PANEL,
                edge=ABLATION_GREY,
                color=ABLATION_GREY,
                fontsize=15,
                mono=True,
                bold=True,
                alpha=dim,
            )
            rp.text(0.115, y, f"“{story}”", fontsize=14.5, color=TEXT, va="top", alpha=dim)
            rp.text(
                0.115,
                y - 0.068,
                f"test it: {name.lower()}",
                fontsize=12,
                color=SUB,
                va="top",
                alpha=dim,
            )
            if verdict:
                rp.text(
                    0.115,
                    y - 0.125,
                    f"✗  ≈{value:.0f}% — back at the baseline"
                    if value < 20
                    else f"✗  ≈{value:.0f}% — barely off the baseline",
                    fontsize=12.5,
                    color=RED,
                    fontweight="bold",
                    va="top",
                    alpha=verdict,
                )
        if closing:
            rp.add_patch(
                Rectangle(
                    (0.0, 0.0),
                    1.0,
                    0.14,
                    facecolor=PANEL,
                    edgecolor=PANEL_EDGE,
                    lw=1.4,
                    alpha=closing,
                    transform=rp.transAxes,
                )
            )
            rp.text(
                0.03,
                0.105,
                "Left standing: the steps, in words, before the answer.",
                fontsize=13.5,
                color=ORANGE,
                fontweight="bold",
                va="top",
                alpha=closing,
            )
            rp.text(
                0.03,
                0.045,
                "Ruling out three stories is not the same as proving a fourth.",
                fontsize=12.5,
                color=TEXT,
                va="top",
                alpha=closing,
            )

        fig.text(
            0.075,
            0.098,
            "Standard and chain of thought: Table 2.  ≈ ablation bars read off Figure 5 — "
            "the paper tabulates ablations for LaMDA 137B only (Table 6).",
            fontsize=10.5,
            color=FAINT,
            va="top",
        )
        footer(fig, FOOT)
        return fig_to_pil(fig)

    frames, durations = [], []
    hold(frames, durations, lambda: render(), ms=900)
    tween(frames, durations, lambda t: render(std_t=t), n=14)
    hold(frames, durations, lambda: render(std_t=1), ms=900)
    tween(frames, durations, lambda t: render(std_t=1, cot_t=t), n=18)
    hold(frames, durations, lambda: render(std_t=1, cot_t=1), ms=700)
    tween(frames, durations, lambda t: render(std_t=1, cot_t=1, gap_t=t), n=12)
    hold(frames, durations, lambda: render(std_t=1, cot_t=1, gap_t=1), ms=2200)

    done = []
    base = {"std_t": 1, "cot_t": 1, "gap_t": 1}
    for _ in SUSPECTS:
        # The story first, with no bar: the room should guess before it grows.
        hold(
            frames,
            durations,
            lambda d=tuple(done): render(**base, suspects=(*d, (0.0, 0.0))),
            ms=2600,
        )
        tween(
            frames,
            durations,
            lambda t, d=tuple(done): render(**base, suspects=(*d, (t, 0.0))),
            n=12,
        )
        hold(
            frames,
            durations,
            lambda d=tuple(done): render(**base, suspects=(*d, (1.0, 0.0))),
            ms=900,
        )
        tween(
            frames,
            durations,
            lambda t, d=tuple(done): render(**base, suspects=(*d, (1.0, t))),
            n=8,
        )
        done.append((1.0, 1.0))
        hold(frames, durations, lambda d=tuple(done): render(**base, suspects=d), ms=1400)

    tween(frames, durations, lambda t: render(**base, suspects=tuple(done), closing=t), n=10)
    hold(frames, durations, lambda: render(**base, suspects=tuple(done), closing=1.0), ms=1800, n=2)
    save_gif(frames, durations, "w06_s16_ablation.gif")


if __name__ == "__main__":
    make_paper_slide()
    make_redraw()
