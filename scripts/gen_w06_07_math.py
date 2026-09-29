"""Week 6, part 4: the mirage paper's mathematics, one term at a time.

Main flow (equations in the paper's main text):
  w06_s28_risk.gif          equations (1)-(3): loss, and risk as an average penalty
  w06_s29_tv.gif            equations (4)-(5): total variation distance, as bar charts
  w06_s30_bound.gif         equation (6), Theorem 3.1: a ceiling, and when it stops meaning anything
  w06_s31_dials.gif         equation (7): three dials -- task, length, format

Backup (after the closing slide; Appendix C, for students who want it):
  w06_s46_task_decay.gif    C.1: each new thing multiplies the chance of success
  w06_s47_length_curve.gif  C.2: the assumed shape of the length cliff, against Table 4
  w06_s48_format_cosine.gif C.3: format distance is cosine similarity -- Week 2, again
  w06_s49_proof.gif         C.4: where the theorem comes from, in two pieces

The audience has no mathematics beyond school algebra, so every equation is
shown the 3Blue1Brown way: the whole thing once, then one term lit at a time
with its meaning in words beneath it, then a worked number. Nothing is
simplified on the slide without saying so -- the symbols are the paper's.

The worked numbers on s30 (B = 1, n = 10,000, delta = 0.05, a practice
penalty of 0.02) are chosen for illustration and labeled as such; the point
the slide makes -- that the ceiling passes the worst possible score once the
distributions differ by more than about 0.48, and so says nothing at Delta = 1
-- is arithmetic on the paper's own inequality, and is posed as a question.
"""

import numpy as np
from matplotlib.patches import Wedge
from style_dark import (
    BLUE,
    FAINT,
    GREEN,
    GRID,
    ORANGE,
    PANEL_EDGE,
    PURPLE,
    RED,
    SUB,
    TEXT,
    YELLOW,
    blank_axes,
    brace_note,
    ease,
    equation,
    fig_to_pil,
    footer,
    hold,
    kicker_title,
    lerp,
    new_fig,
    save_gif,
    tween,
)

FOOT = "reading (optional): Zhao et al. 2025 (cot-mirage) · "
DIM = 0.28


def plain_axes(fig, rect, xlim, ylim):
    ax = fig.add_axes(rect)
    ax.set_facecolor("none")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(FAINT)
    ax.tick_params(colors=SUB, labelsize=11, length=0, pad=5)
    return ax


def run(frames, durations, render, stages, last_ms=1800):
    for s, ms in stages:
        hold(frames, durations, lambda s=s: render(s), ms=ms)
    hold(frames, durations, lambda: render(stages[-1][0]), ms=last_ms, n=2)


# ── s28: loss and risk ─────────────────────────────────────────────────
def make_risk():
    marks = [("Q1", True), ("Q2", True), ("Q3", False), ("Q4", True)]

    def render(stage):
        fig = new_fig()
        kicker_title(
            fig,
            "PART 4 · THE MATH, TERM BY TERM · 1 OF 4",
            "Loss and risk: marking the practice, and the exam",
            "Equations (1)–(3). First without symbols: four practice questions.",
        )
        ex = blank_axes(fig, [0.045, 0.69, 0.91, 0.10])
        for i, (q, ok) in enumerate(marks):
            x = i * 0.12
            ex.text(x, 0.75, q, fontsize=13, color=SUB, va="center")
            ex.text(
                x + 0.045,
                0.75,
                "✓" if ok else "✗",
                fontsize=16,
                color=GREEN if ok else RED,
                va="center",
            )
            ex.text(x, 0.20, f"penalty {0 if ok else 1}", fontsize=12, color=TEXT, va="center")
        ex.text(
            0.50,
            0.75,
            "loss = the penalty for one answer (0 if right)",
            fontsize=13,
            color=RED,
            va="center",
        )
        ex.text(
            0.50,
            0.20,
            "risk = the average loss:  (0 + 0 + 1 + 0) ÷ 4 = 0.25",
            fontsize=13,
            color=BLUE,
            va="center",
        )

        if stage >= 1:
            a = [
                1.0 if stage in (1, 2) else DIM,
                1.0,
                1.0 if stage in (1, 3) else DIM,
                1.0 if stage in (1, 4) else DIM,
                1.0 if stage in (1, 5) else DIM,
            ]
            if stage >= 9:
                a = [1.0] * 5
            boxes = equation(
                fig,
                [
                    (r"\hat{R}_{\mathrm{train}}(f_\theta)", BLUE, a[0]),
                    ("=", TEXT, a[1]),
                    (r"\frac{1}{n}\sum_{i=1}^{n}", YELLOW, a[2]),
                    (r"\ell", RED, a[3]),
                    (r"\left(f_\theta(x_i),\ y_i\right)", GREEN, a[4]),
                ],
                y=0.555,
                fontsize=32,
            )
            fig.text(0.955, 0.555, "(1)", fontsize=13, color=FAINT, ha="right")
            notes = {
                2: (
                    0,
                    "the practice risk: average penalty on the\ntraining questions. The "
                    "hat (^) means\n“measured on a sample”.",
                    BLUE,
                ),
                3: (
                    2,
                    "add up over all n practice\nquestions, then divide by n:\nan average",
                    YELLOW,
                ),
                4: (3, "the loss: the penalty\nfor one answer", RED),
                5: (
                    4,
                    "the model's answer to question i\n(f is the model, θ its weights)\n"
                    "and the right answer, yᵢ",
                    GREEN,
                ),
            }
            if stage in notes:
                k, text, colour = notes[stage]
                brace_note(fig, boxes[k], text, colour, dy=0.03)
        if stage >= 6:
            b = [1.0 if stage in (6, 7) else DIM, 1.0, 1.0 if stage in (6, 8) else DIM, 1.0]
            if stage >= 9:
                b = [1.0] * 4
            boxes = equation(
                fig,
                [
                    (r"R_{\mathrm{test}}(f_\theta)", ORANGE, b[0]),
                    ("=", TEXT, b[1]),
                    (r"\mathbb{E}_{(x,y)\sim\mathcal{D}_{\mathrm{test}}}", YELLOW, b[2]),
                    (r"\left[\ell\left(f_\theta(x),\ y\right)\right]", TEXT, b[3]),
                ],
                y=0.265,
                fontsize=32,
            )
            fig.text(0.955, 0.265, "(3)", fontsize=13, color=FAINT, ha="right")
            if stage == 7:
                brace_note(
                    fig,
                    boxes[0],
                    "the test risk: the average penalty\non the real "
                    "exam. No hat — this is the\ntrue average, not a sample's",
                    ORANGE,
                    dy=0.03,
                )
            if stage == 8:
                brace_note(
                    fig,
                    boxes[2],
                    "𝔼 = “expected value”: the average over every\n"
                    "question the test distribution could produce.\n∼ means “drawn "
                    "from”; $\\mathcal{D}$ is a distribution",
                    YELLOW,
                    dy=0.03,
                )
            if stage >= 9:
                fig.text(
                    0.5,
                    0.13,
                    "Equation (2) is the same average over the training "
                    "distribution, $\\mathcal{D}_{\\mathrm{train}}$. "
                    "The whole paper asks:\nhow far can the exam "
                    "penalty (3) climb above the practice penalty (1)?",
                    fontsize=14,
                    color=TEXT,
                    ha="center",
                    va="top",
                    linespacing=1.5,
                )
        footer(fig, FOOT + "§3, equations (1)–(3) · study guide: loss-and-risk")
        return fig_to_pil(fig)

    frames, durations = [], []
    run(
        frames,
        durations,
        render,
        [
            (0, 2600),
            (1, 1800),
            (2, 2600),
            (3, 2400),
            (4, 2000),
            (5, 2600),
            (6, 1800),
            (7, 2600),
            (8, 2800),
            (9, 1800),
        ],
    )
    save_gif(frames, durations, "w06_s28_risk.gif")


# ── s29: total variation distance ──────────────────────────────────────
KINDS = ["f1 then f1", "f1 then f2", "f2 then f1", "f2 then f2"]
P_MILD = np.array([0.4, 0.3, 0.2, 0.1])
Q_MILD = np.array([0.1, 0.2, 0.3, 0.4])
P_CMP = np.array([1 / 3, 1 / 3, 1 / 3, 0.0])
Q_CMP = np.array([0.0, 0.0, 0.0, 1.0])


def make_tv():
    def render(stage, morph=0.0):
        fig = new_fig()
        kicker_title(
            fig,
            "PART 4 · THE MATH, TERM BY TERM · 2 OF 4",
            "Total variation: how different are two distributions?",
            "Equations (4)–(5). Four kinds of question; how often each turns up in "
            "training (blue) and in the test (yellow).",
        )
        p = P_MILD + (P_CMP - P_MILD) * ease(morph)
        q = Q_MILD + (Q_CMP - Q_MILD) * ease(morph)
        ax = plain_axes(fig, [0.07, 0.40, 0.50, 0.36], (-0.6, 3.6), (0, 1.08))
        ax.set_xticks(range(4))
        ax.set_xticklabels(KINDS, fontsize=12)
        ax.set_yticks([0, 0.5, 1.0])
        ax.set_yticklabels(["0", "½", "1"])
        for yv in (0.5, 1.0):
            ax.axhline(yv, color=GRID, lw=0.7, zorder=0)
        w = 0.36
        ax.bar(np.arange(4) - w / 2, p, width=w, color=BLUE)
        if stage >= 1:
            ax.bar(np.arange(4) + w / 2, q, width=w, color=YELLOW)
        if stage >= 2:
            for i in range(4):
                d = abs(p[i] - q[i])
                ax.plot([i - w, i + w], [max(p[i], q[i]) + 0.05] * 2, color=RED, lw=1.2)
                ax.text(
                    i, max(p[i], q[i]) + 0.07, f"gap {d:.2f}", ha="center", fontsize=11.5, color=RED
                )
        tv = 0.5 * np.abs(p - q).sum()
        rp = blank_axes(fig, [0.62, 0.40, 0.35, 0.36])
        if stage >= 3:
            rp.text(0.0, 0.95, "Add the gaps, halve the total:", fontsize=14, color=TEXT, va="top")
            gaps = " + ".join(f"{abs(a - b):.2f}" for a, b in zip(p, q, strict=True))
            rp.text(
                0.0, 0.78, f"½ × ({gaps})", fontsize=13, color=RED, va="top", fontfamily="monospace"
            )
            rp.text(
                0.0, 0.58, f"TV = {tv:.2f}", fontsize=26, color=ORANGE, fontweight="bold", va="top"
            )
            rp.text(
                0.0,
                0.30,
                "0 = the same pattern exactly\n1 = no overlap at all",
                fontsize=13,
                color=SUB,
                va="top",
                linespacing=1.5,
            )
        if stage >= 4:
            a = [
                1.0,
                1.0,
                1.0 if stage in (5, 7) else DIM if stage > 5 else 1.0,
                1.0,
                1.0 if stage in (6, 7) else DIM if stage > 5 else 1.0,
            ]
            boxes = equation(
                fig,
                [
                    (r"\Delta\;=\;\mathrm{TV}(P,Q)", ORANGE, a[0]),
                    ("=", TEXT, a[1]),
                    (r"\sup_{A}\ |P(A)-Q(A)|", BLUE, a[2]),
                    ("=", TEXT, a[3]),
                    (r"\frac{1}{2}\int|dP-dQ|", RED, a[4]),
                ],
                y=0.25,
                fontsize=30,
            )
            if stage == 5:
                brace_note(
                    fig,
                    boxes[2],
                    "the biggest disagreement about the chance of any "
                    "group of questions A.\nTry A = the first two kinds: 0.70 vs 0.30 "
                    "→ 0.40. Same answer.",
                    BLUE,
                    dy=0.03,
                )
            if stage == 6:
                brace_note(
                    fig,
                    boxes[4],
                    "half the total gap, bar by bar —\n∫ is adding up, for smooth charts",
                    RED,
                    dy=0.03,
                )
            if stage == 4:
                brace_note(
                    fig,
                    boxes[0],
                    "Δ (“delta”): the paper's name for it —\n“distribution discrepancy”",
                    ORANGE,
                    dy=0.03,
                )
        if stage >= 7:
            fig.text(
                0.62,
                0.36,
                "Zhao's “composition” test: train on three kinds,\ntest only "
                "on the fourth. TV = 1. Remember this.",
                fontsize=13,
                color=ORANGE,
                va="top",
                fontweight="bold",
                linespacing=1.4,
            )
        footer(fig, FOOT + "§3, equations (4)–(5) · study guide: total-variation-distance")
        return fig_to_pil(fig)

    frames, durations = [], []
    run(
        frames,
        durations,
        render,
        [(0, 1600), (1, 1600), (2, 2200), (3, 2400), (4, 2400), (5, 3000), (6, 2400)],
        last_ms=900,
    )
    tween(frames, durations, lambda t: render(6, t), n=18, ms=70)
    hold(frames, durations, lambda: render(7, 1.0), ms=1800, n=2)
    save_gif(frames, durations, "w06_s29_tv.gif")


# ── s30: the bound ─────────────────────────────────────────────────────
B, R_HAT, N, DELTA_CONF = 1.0, 0.02, 10_000, 0.05
SAMPLING = B * np.sqrt(np.log(1 / DELTA_CONF) / (2 * N))
BREAK_EVEN = (B - R_HAT - SAMPLING) / (2 * B)
assert abs(SAMPLING - 0.0122) < 5e-4 and abs(BREAK_EVEN - 0.484) < 1e-3


def make_bound():
    def render(stage, d=0.1):
        fig = new_fig()
        kicker_title(
            fig,
            "PART 4 · THE MATH, TERM BY TERM · 3 OF 4",
            "Theorem 3.1: a ceiling on the exam penalty",
            "Equation (6). It holds “with probability at least 1 − δ” — almost "
            "always, for small δ.",
        )
        hi = {1: 0, 2: 1, 3: 2, 4: 4, 5: 6}
        a = [1.0] * 7 if stage in (0, 6, 7, 8) else [DIM] * 7
        if stage in hi:
            a[hi[stage]] = 1.0
        boxes = equation(
            fig,
            [
                (r"R_{\mathrm{test}}", ORANGE, a[0]),
                (r"\leq", TEXT, a[1]),
                (r"\hat{R}_{\mathrm{train}}", BLUE, a[2]),
                ("+", TEXT, a[3]),
                (
                    r"2B\,\Delta(\mathcal{D}_{\mathrm{train}},\mathcal{D}_{\mathrm{test}})",
                    RED,
                    a[4],
                ),
                ("+", TEXT, a[5]),
                (r"B\sqrt{\frac{\log(1/\delta)}{2n}}", GREEN, a[6]),
            ],
            y=0.66,
            fontsize=34,
        )
        notes = {
            1: (0, "the exam penalty", ORANGE),
            2: (1, "is at most: a ceiling,\nnot a prediction", TEXT),
            3: (2, "the practice penalty", BLUE),
            4: (
                4,
                "cost of the exam being different.\nB = the worst penalty one answer can "
                "get;\nΔ = total variation, from the last slide",
                RED,
            ),
            5: (
                6,
                "cost of practicing on only n questions.\nShrinks as n grows. δ = the "
                "small chance\nthe guarantee fails (say 5%)",
                GREEN,
            ),
        }
        if stage in notes:
            k, text, colour = notes[stage]
            brace_note(fig, boxes[k], text, colour, dy=0.03)
        if stage == 6:
            fig.text(
                0.5,
                0.50,
                "In words: exam penalty ≤ practice penalty + a charge for "
                "difference + a charge for too little practice.",
                fontsize=15,
                color=TEXT,
                ha="center",
                va="top",
            )
        if stage >= 7:
            ceiling = R_HAT + 2 * B * d + SAMPLING
            ax = plain_axes(fig, [0.10, 0.12, 0.40, 0.40], (-0.02, 1.02), (0, 2.2))
            ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
            ax.set_yticks([0, 1, 2])
            ax.set_xlabel("Δ — how different the exam is", color=SUB, fontsize=12)
            ax.set_ylabel("the ceiling", color=SUB, fontsize=12)
            xs = np.linspace(0, 1, 50)
            ax.plot(xs, R_HAT + 2 * B * xs + SAMPLING, color=RED, lw=2.4)
            ax.axhline(B, color=YELLOW, ls=(0, (4, 4)), lw=1.5)
            ax.text(0.02, B + 0.05, "worst possible penalty, B = 1", fontsize=11, color=YELLOW)
            ax.scatter([d], [ceiling], s=80, color=ORANGE, zorder=3)
            if stage >= 8:
                ax.axvspan(BREAK_EVEN, 1.02, color=RED, alpha=0.08, lw=0)
            rp = blank_axes(fig, [0.55, 0.10, 0.42, 0.44])
            rp.text(
                0.0,
                0.98,
                "Try numbers (illustrative): B = 1, practice penalty 0.02,\n"
                "n = 10,000 questions, δ = 0.05",
                fontsize=12.5,
                color=SUB,
                va="top",
                linespacing=1.4,
            )
            rp.text(
                0.0,
                0.76,
                f"ceiling = 0.02 + 2 × {d:.2f} + {SAMPLING:.3f} = {ceiling:.2f}",
                fontsize=15,
                color=ORANGE,
                va="top",
                fontfamily="monospace",
            )
            if stage >= 8:
                rp.text(
                    0.0,
                    0.58,
                    f"Past Δ ≈ {BREAK_EVEN:.2f} the ceiling is above the worst\npenalty "
                    "possible. It rules nothing out.",
                    fontsize=13.5,
                    color=RED,
                    va="top",
                    linespacing=1.4,
                    fontweight="bold",
                )
                rp.text(
                    0.0,
                    0.33,
                    "Question for Part 5: the out-of-distribution tests\n"
                    "have Δ = 1. What does the theorem tell us there?",
                    fontsize=13.5,
                    color=TEXT,
                    va="top",
                    linespacing=1.4,
                )
        footer(
            fig,
            FOOT + "§3, Theorem 3.1 · study guide: generalization-bound · total-variation-distance",
        )
        return fig_to_pil(fig)

    frames, durations = [], []
    for s, ms in ((0, 2200), (1, 1600), (2, 2000), (3, 1600), (4, 3200), (5, 3200), (6, 2600)):
        hold(frames, durations, lambda s=s: render(s), ms=ms)
    hold(frames, durations, lambda: render(7, 0.0), ms=1600)
    tween(frames, durations, lambda t: render(7, t), n=30, ms=80)
    hold(frames, durations, lambda: render(8, 1.0), ms=1800, n=2)
    save_gif(frames, durations, "w06_s30_bound.gif")


# ── s31: three dials ───────────────────────────────────────────────────
DIALS = [
    ("task", "new operations, new letters,\nnew combinations", BLUE),
    ("length", "longer or shorter words;\nmore or fewer steps", GREEN),
    ("format", "prompt tokens inserted,\ndeleted or changed", YELLOW),
]


def dial(ax, cx, cy, r, value, colour, label):
    ax.add_patch(Wedge((cx, cy), r, 0, 180, width=r * 0.18, facecolor=PANEL_EDGE, edgecolor="none"))
    ax.add_patch(
        Wedge(
            (cx, cy), r, 180 - 180 * value, 180, width=r * 0.18, facecolor=colour, edgecolor="none"
        )
    )
    ang = np.pi * (1 - value)
    ax.plot([cx, cx + 0.8 * r * np.cos(ang)], [cy, cy + 0.8 * r * np.sin(ang)], color=TEXT, lw=2.5)
    ax.text(
        cx,
        cy - 0.22 * r,
        label,
        ha="center",
        va="top",
        fontsize=15,
        color=colour,
        fontweight="bold",
    )


def make_dials():
    def render(stage, t=0.0):
        fig = new_fig()
        kicker_title(
            fig,
            "PART 4 · THE MATH, TERM BY TERM · 4 OF 4",
            "Three dials, one total",
            "Equation (7). How different the exam is, split into the three ways it can differ.",
        )
        boxes = equation(
            fig,
            [
                (r"\Delta", ORANGE, 1.0),
                ("=", TEXT, 1.0),
                (r"\Phi", PURPLE, 1.0),
                (
                    r"(\Delta_{\mathrm{task}},\ \Delta_{\mathrm{length}},\ "
                    r"\Delta_{\mathrm{format}})",
                    TEXT,
                    1.0,
                ),
            ],
            y=0.71,
            fontsize=32,
        )
        if stage >= 1:
            brace_note(
                fig,
                boxes[2],
                "Φ (“phi”): some way of combining the three.\nThe "
                "paper only requires that turning any dial up\nnever turns the total "
                "down — “monotonically increasing”.",
                PURPLE,
                dy=0.03,
                x=0.30,
            )
        ax = fig.add_axes([0.045, 0.08, 0.91, 0.40])
        ax.set_xlim(0, 16)
        ax.set_ylim(0, 4)
        ax.set_aspect("equal")
        ax.axis("off")
        if stage >= 2:
            vals = [
                0.15 + 0.7 * ease(min(1, t * 3)),
                0.1 + 0.5 * ease(min(1, max(0, t * 3 - 1))),
                0.05 + 0.4 * ease(min(1, max(0, t * 3 - 2))),
            ]
            for i, ((name, what, colour), v) in enumerate(zip(DIALS, vals, strict=True)):
                cx = 1.8 + i * 3.6
                dial(ax, cx, 1.6, 1.3, v, colour, name)
                ax.text(
                    cx, 0.35, what, ha="center", va="top", fontsize=11, color=SUB, linespacing=1.3
                )
            total = min(1.0, max(vals) + 0.25 * sum(vals))
            ax.text(10.75, 1.9, "→", fontsize=30, color=FAINT, ha="center", va="center")
            dial(ax, 13.6, 1.6, 1.6, total, ORANGE, "Δ, total")
        if stage >= 3:
            fig.text(
                0.5,
                0.47,
                "Appendix C measures each dial separately — backup slides at the end of the deck.",
                fontsize=13,
                color=SUB,
                ha="center",
            )
        footer(fig, FOOT + "§3, equation (7) · study guide: out-of-distribution-generalization")
        return fig_to_pil(fig)

    frames, durations = [], []
    hold(frames, durations, lambda: render(0), ms=1800)
    hold(frames, durations, lambda: render(1), ms=3000)
    tween(frames, durations, lambda t: render(2, t), n=30, ms=70)
    hold(frames, durations, lambda: render(3, 1.0), ms=1800, n=2)
    save_gif(frames, durations, "w06_s31_dials.gif")


# ── s46 (backup): task novelty ─────────────────────────────────────────
def make_task_decay():
    def render(stage):
        fig = new_fig()
        kicker_title(
            fig,
            "BACKUP · APPENDIX C.1 · THE TASK DIAL",
            "Each new thing multiplies the chance of success",
            "Equations (14), (17), (18), simplified to their counting. The symbols are "
            "the paper's.",
        )
        boxes = equation(
            fig,
            [
                (r"\mathcal{T}(C)", BLUE, 1.0),
                ("=", TEXT, 1.0),
                (r"\alpha\sum_i \mathbb{1}[a_i\ \mathrm{new}]", TEXT, 1.0),
                ("+", TEXT, 1.0),
                (r"\beta\sum_j \mathbb{1}[f_j\ \mathrm{new}]", TEXT, 1.0),
                ("+", TEXT, 1.0),
                (r"\gamma\,\mathbb{1}[f_S\ \mathrm{new}]", TEXT, 1.0),
            ],
            y=0.72,
            fontsize=28,
        )
        if stage >= 1:
            brace_note(
                fig,
                boxes[2],
                "𝟙[·] is 1 if true, 0 if not —\nso this counts new letters",
                SUB,
                dy=0.025,
                fontsize=11.5,
            )
            brace_note(fig, boxes[4], "…new operations", SUB, dy=0.025, fontsize=11.5)
            brace_note(
                fig,
                boxes[6],
                "…a new combination.\nα, β, γ: how much each counts",
                SUB,
                dy=0.025,
                fontsize=11.5,
            )
        if stage >= 2:
            equation(
                fig,
                [
                    (r"\pi(C)", GREEN, 1.0),
                    ("=", TEXT, 1.0),
                    (
                        r"\pi_0\ \cdot\ \rho_a^{\#\,\mathrm{new\ letters}}\ \cdot\ "
                        r"\rho_f^{\#\,\mathrm{new\ ops}}\ \cdot\ \rho_c^{[\mathrm{new\ combo}]}",
                        TEXT,
                        1.0,
                    ),
                ],
                y=0.47,
                fontsize=26,
            )
            fig.text(
                0.5,
                0.425,
                "π: the chance the whole chain is right. π₀: its chance on "
                "familiar questions.\nEach ρ (“rho”) is a fraction below 1 — so every new "
                "thing multiplies the chance down.",
                fontsize=12.5,
                color=SUB,
                ha="center",
                va="top",
                linespacing=1.45,
            )
        if stage >= 3:
            ax = plain_axes(fig, [0.10, 0.10, 0.36, 0.22], (-0.4, 4.4), (0, 1.1))
            ks = np.arange(5)
            ax.bar(ks, 0.5**ks, color=GREEN, width=0.6)
            for k in ks:
                ax.text(k, 0.5**k + 0.04, f"{0.5**k:g}", ha="center", fontsize=11, color=GREEN)
            ax.set_xticks(ks)
            ax.set_xlabel("how many new things", color=SUB, fontsize=11)
            ax.set_yticks([0, 1])
            rp = blank_axes(fig, [0.52, 0.08, 0.45, 0.26])
            rp.text(
                0.0,
                0.95,
                "With π₀ = 1 and every ρ = ½ (illustrative):\nhalve, halve, "
                "halve. That is exponential decay —\nequation (17): "
                "$\\pi \\leq \\exp(-\\kappa(\\mathcal{T} - \\tau))$.",
                fontsize=12.5,
                color=TEXT,
                va="top",
                linespacing=1.45,
            )
            rp.text(
                0.0,
                0.30,
                "A model of failure the authors assume — each\nnovelty costs a "
                "fixed fraction, independently.\nThe ρ values are not measured.",
                fontsize=12.5,
                color=ORANGE,
                va="top",
                linespacing=1.45,
            )
        footer(fig, FOOT + "Appendix C.1 · study guide: out-of-distribution-generalization")
        return fig_to_pil(fig)

    frames, durations = [], []
    run(frames, durations, render, [(0, 2000), (1, 3000), (2, 3000), (3, 2000)])
    save_gif(frames, durations, "w06_s46_task_decay.gif")


# ── s47 (backup): the length curve ─────────────────────────────────────
# Table 4, trained on length 4: full-chain exact match and edit distance by test length.
T4_LEN = [2, 3, 4, 5, 6]
T4_EM = [0.0, 0.0, 100.0, 0.0, 0.0]
T4_ED = [0.3772, 0.2221, 0.0, 0.1818, 0.3294]


def eps(length, e0, sigma, ltrain=4):
    return e0 + (1 - e0) * (1 - np.exp(-((length - ltrain) ** 2) / (2 * sigma**2)))


def make_length_curve():
    def render(stage, sigma=2.0):
        fig = new_fig()
        kicker_title(
            fig,
            "BACKUP · APPENDIX C.2 · THE LENGTH DIAL",
            "An assumed shape for the length cliff",
            "Equation (22). The authors call it “a modeling ansatz” — a shape chosen "
            "to fit, not derived.",
        )
        a = [1.0] * 4 if stage < 1 or stage > 4 else [DIM] * 4
        if 1 <= stage <= 4:
            a[stage - 1] = 1.0
        boxes = equation(
            fig,
            [
                (r"\varepsilon(L)=", TEXT, 1.0),
                (r"\varepsilon_0", BLUE, a[0]),
                (r"+\ (1-\varepsilon_0)\,", TEXT, a[1]),
                (
                    r"\left(1-\exp\left(-\frac{(L-L_{\mathrm{train}})^2}{2\sigma^2}\right)\right)",
                    RED,
                    a[2],
                ),
            ],
            y=0.70,
            fontsize=30,
        )
        notes = {
            1: (1, "the error at the length it trained on", BLUE),
            3: (
                3,
                "0 at the trained length, rising to 1 far from it.\nSquared: too long "
                "and too short count the same.\nσ (“sigma”): how forgiving — the width",
                RED,
            ),
        }
        if stage in notes:
            k, text, colour = notes[stage]
            brace_note(fig, boxes[k], text, colour, dy=0.03)
        if stage >= 4:
            ax = plain_axes(fig, [0.10, 0.12, 0.45, 0.40], (1.5, 6.5), (-0.05, 1.12))
            ax.set_xticks(T4_LEN)
            ax.set_yticks([0, 0.5, 1])
            ax.set_xlabel("test word length (trained on 4)", color=SUB, fontsize=12)
            ax.set_ylabel("error", color=SUB, fontsize=12)
            xs = np.linspace(1.5, 6.5, 200)
            ax.plot(xs, eps(xs, 0.0, sigma), color=RED, lw=2.4)
            ax.scatter(
                T4_LEN,
                [1 - e / 100 for e in T4_EM],
                s=90,
                color=ORANGE,
                zorder=3,
                label="1 − exact match",
            )
            ax.scatter(T4_LEN, T4_ED, s=70, color=BLUE, marker="s", zorder=3, label="edit distance")
            ax.legend(loc="lower right", frameon=False, labelcolor=SUB, fontsize=11)
            ax.text(1.6, 1.06, f"curve: ε₀ = 0, σ = {sigma:.2f}", color=RED, fontsize=11.5)
            rp = blank_axes(fig, [0.60, 0.12, 0.37, 0.40])
            rp.text(
                0.0,
                0.95,
                "The data (Table 4)",
                fontsize=14.5,
                color=TEXT,
                fontweight="bold",
                va="top",
            )
            rp.text(
                0.0,
                0.80,
                "Exact match is a cliff: 100% at\nlength 4, 0% one letter either "
                "side.\nEdit distance rises more gently.",
                fontsize=12.5,
                color=SUB,
                va="top",
                linespacing=1.45,
            )
            rp.text(
                0.0,
                0.42,
                "Which shape you see depends on\nhow you mark. The curve is fitted\nby choosing σ.",
                fontsize=12.5,
                color=ORANGE,
                va="top",
                linespacing=1.45,
            )
        footer(fig, FOOT + "Appendix C.2 · Table 4 · study guide: exact-match-and-edit-distance")
        return fig_to_pil(fig)

    frames, durations = [], []
    for s, ms in ((0, 2200), (1, 2400), (3, 3200)):
        hold(frames, durations, lambda s=s: render(s), ms=ms)
    hold(frames, durations, lambda: render(5, 2.0), ms=1600)
    tween(frames, durations, lambda t: render(5, lerp(2.0, 0.35, t)), n=24, ms=80)
    hold(frames, durations, lambda: render(5, 0.35), ms=1800, n=2)
    save_gif(frames, durations, "w06_s47_length_curve.gif")


# ── s48 (backup): format distance is cosine similarity ─────────────────
def make_format_cosine():
    train_angles = [20, 32, 44]

    def render(stage, drift=0.0):
        fig = new_fig()
        kicker_title(
            fig,
            "BACKUP · APPENDIX C.3 · THE FORMAT DIAL",
            "Format distance is cosine similarity — Week 2, again",
            "Definition C.1, equations (26)–(27).",
        )
        boxes = equation(
            fig,
            [
                (r"S(p_{\mathrm{test}})", YELLOW, 1.0),
                ("=", TEXT, 1.0),
                (r"\max_{p\,\in\,\Pi_{\mathrm{train}}}", BLUE, 1.0),
                (r"\cos\left(\eta(p),\ \eta(p_{\mathrm{test}})\right)", GREEN, 1.0),
            ],
            y=0.72,
            fontsize=30,
        )
        fig.text(
            0.5,
            0.47,
            r"$\Delta_{\mathrm{format}} = 1 - S(p_{\mathrm{test}})$",
            fontsize=24,
            color=ORANGE,
            ha="center",
        )
        if stage >= 1:
            brace_note(
                fig,
                boxes[2],
                "compare with the most\nsimilar training prompt",
                BLUE,
                dy=0.045,
                x=0.26,
            )
            brace_note(
                fig,
                boxes[3],
                "η (“eta”) turns a prompt into a vector —\nan embedding. "
                "cos: the angle between two",
                GREEN,
                dy=0.045,
                x=0.74,
            )
        if stage >= 2:
            ax = fig.add_axes([0.10, 0.06, 0.30, 0.36])
            ax.set_xlim(-0.1, 1.1)
            ax.set_ylim(-0.1, 1.1)
            ax.set_aspect("equal")
            ax.axis("off")
            for a in train_angles:
                r = np.radians(a)
                ax.annotate(
                    "",
                    xy=(np.cos(r), np.sin(r)),
                    xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2),
                )
            ta = 50 + 35 * ease(drift)
            r = np.radians(ta)
            ax.annotate(
                "",
                xy=(np.cos(r), np.sin(r)),
                xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=YELLOW, lw=2.6),
            )
            s = np.cos(np.radians(ta - max(train_angles)))
            rp = blank_axes(fig, [0.50, 0.08, 0.47, 0.32])
            rp.text(
                0.0,
                0.95,
                "blue: training prompts   yellow: the test prompt",
                fontsize=12,
                color=SUB,
                va="top",
            )
            rp.text(
                0.0,
                0.72,
                f"S = {s:.2f}     Δ_format = {1 - s:.2f}",
                fontsize=18,
                color=ORANGE,
                va="top",
                fontfamily="monospace",
            )
            rp.text(
                0.0,
                0.45,
                "Insert a stray token, delete one, change one:\nthe test prompt's "
                "vector swings away from every\ntraining prompt, S falls, the dial rises.",
                fontsize=12.5,
                color=TEXT,
                va="top",
                linespacing=1.45,
            )
        footer(fig, FOOT + "Appendix C.3 · study guide: cosine-similarity · embedding")
        return fig_to_pil(fig)

    frames, durations = [], []
    hold(frames, durations, lambda: render(0), ms=2000)
    hold(frames, durations, lambda: render(1), ms=3000)
    hold(frames, durations, lambda: render(2, 0.0), ms=1600)
    tween(frames, durations, lambda t: render(2, t), n=24, ms=80)
    hold(frames, durations, lambda: render(2, 1.0), ms=1800, n=2)
    save_gif(frames, durations, "w06_s48_format_cosine.gif")


# ── s49 (backup): where the theorem comes from ─────────────────────────
def make_proof():
    rng = np.random.default_rng(3)
    flips = rng.integers(0, 2, size=4000)
    running = np.cumsum(flips) / np.arange(1, len(flips) + 1)

    def render(stage, upto=4000):
        fig = new_fig()
        kicker_title(
            fig,
            "BACKUP · APPENDIX C.4 · THE PROOF, IN TWO PIECES",
            "Where Theorem 3.1 comes from",
            "Equation (28): split the gap between exam and practice into two gaps.",
        )
        boxes = equation(
            fig,
            [
                (r"R_{\mathrm{test}}-\hat{R}_{\mathrm{train}}", TEXT, 1.0),
                ("=", TEXT, 1.0),
                (r"[R_{\mathrm{test}}-R_{\mathrm{train}}]", RED, 1.0),
                ("+", TEXT, 1.0),
                (r"[R_{\mathrm{train}}-\hat{R}_{\mathrm{train}}]", GREEN, 1.0),
            ],
            y=0.73,
            fontsize=30,
        )
        if stage >= 1:
            brace_note(
                fig,
                boxes[2],
                "(i) the exam is a different pattern.\nNo question costs "
                "more than B, so this\ngap is at most 2B × TV",
                RED,
                dy=0.045,
                x=0.40,
            )
        if stage >= 2:
            brace_note(
                fig,
                boxes[4],
                "(ii) practice was only a sample.\nHoeffding's "
                "inequality: averages of\nmany bounded numbers rarely stray far",
                GREEN,
                dy=0.045,
                x=0.80,
            )
        if stage >= 3:
            ax = plain_axes(fig, [0.10, 0.15, 0.45, 0.26], (1, 4000), (0.2, 0.8))
            ax.set_xscale("log")
            ax.set_xticks([1, 10, 100, 1000])
            ax.set_xticklabels(["1", "10", "100", "1,000"])
            ns = np.arange(1, upto + 1)
            band = np.sqrt(np.log(1 / 0.05) / (2 * ns))
            ax.fill_between(ns, 0.5 - band, 0.5 + band, color=GREEN, alpha=0.15, lw=0)
            ax.plot(ns, running[:upto], color=YELLOW, lw=1.6)
            ax.axhline(0.5, color=FAINT, lw=1)
            ax.set_xlabel("coin flips so far (n)", color=SUB, fontsize=11)
            ax.set_ylabel("share heads", color=SUB, fontsize=11)
            rp = blank_axes(fig, [0.60, 0.10, 0.37, 0.32])
            rp.text(
                0.0,
                0.95,
                "(ii) as coins: the share of heads\nsettles toward ½, inside a "
                "band\nthat narrows like 1/√n.",
                fontsize=12.5,
                color=TEXT,
                va="top",
                linespacing=1.45,
            )
            if stage >= 4:
                rp.text(
                    0.0,
                    0.42,
                    "Nothing in this proof mentions chains\nof thought. It "
                    "holds for any model on\nany task — a standard result.",
                    fontsize=12.5,
                    color=ORANGE,
                    va="top",
                    linespacing=1.45,
                    fontweight="bold",
                )
        footer(fig, FOOT + "Appendix C.4 · study guide: generalization-bound")
        return fig_to_pil(fig)

    frames, durations = [], []
    run(frames, durations, render, [(0, 2000), (1, 3000), (2, 3000)], last_ms=600)
    tween(frames, durations, lambda t: render(3, max(2, int(4000**t))), n=30, ms=80)
    hold(frames, durations, lambda: render(4), ms=1800, n=2)
    save_gif(frames, durations, "w06_s49_proof.gif")


if __name__ == "__main__":
    make_risk()
    make_tv()
    make_bound()
    make_dials()
    make_task_decay()
    make_length_curve()
    make_format_cosine()
    make_proof()
