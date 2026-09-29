"""Week 6, part 3: the words the critique is written in.

  w06_s19_distribution.gif  training data, test data, and what a "distribution" is
  w06_s20_ood.gif           out-of-distribution, generalization, distribution shift
  w06_s21_leakage.gif       data leakage: when the test is inside the training data
  w06_s22_training.gif      pretrained, trained from scratch, fine-tuned -- and model sizes
  w06_s23_temperature.gif   temperature, reviewed, and why the paper varies it
  w06_s24_metrics.gif       exact match, edit distance, BLEU -- worked on the paper's example

The mirage paper is unreadable without about a dozen terms, and every one of
them has an everyday version: practice questions and the real exam, an answer
key that got out, marking an answer right or nearly right. Each slide starts
from that version and ends on the paper's word, so the word arrives with a
picture already attached.

The question-space plot on s19-s20 is a picture, not data: its two axes (how
many steps, how big the numbers) are chosen because a student can say where
their own homework question would sit on it.
"""

import itertools

import numpy as np
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Rectangle
from style_dark import (
    BLUE,
    FAINT,
    GREEN,
    GRID,
    ORANGE,
    PANEL,
    PANEL_EDGE,
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
    kicker_title,
    lerp,
    new_fig,
    panel_box,
    save_gif,
    tween,
)

RNG = np.random.default_rng(6)
TRAIN = RNG.normal([3.0, 40], [0.7, 14], size=(70, 2))
TEST_IN = RNG.normal([3.0, 40], [0.7, 14], size=(12, 2))
TEST_OUT = RNG.normal([7.0, 40], [0.6, 14], size=(12, 2))


def question_plane(fig, rect):
    ax = fig.add_axes(rect)
    ax.set_facecolor("none")
    ax.set_xlim(0, 9.5)
    ax.set_ylim(0, 95)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(FAINT)
    ax.set_xticks(range(1, 10))
    ax.set_yticks([0, 25, 50, 75])
    ax.tick_params(colors=SUB, labelsize=11, length=0, pad=5)
    ax.grid(True, color=GRID, lw=0.6, alpha=0.6)
    ax.set_xlabel("how many steps the problem takes", color=SUB, fontsize=12)
    ax.set_ylabel("how big its numbers are", color=SUB, fontsize=12)
    return ax


def cloud(ax, alpha):
    ax.add_patch(
        Ellipse(
            (3.0, 40), 3.6, 70, facecolor=BLUE, alpha=0.10 * alpha, edgecolor=BLUE, lw=1.5, ls="--"
        )
    )


# ── s19: distribution ───────────────────────────────────────────────────
def make_distribution():
    def render(stage):
        fig = new_fig()
        kicker_title(
            fig,
            "PART 3 · WORDS THE CRITIQUE NEEDS",
            "Practice questions, the real exam, and a “distribution”",
            "Every math word problem can be placed on this chart. Each dot is one problem.",
        )
        ax = question_plane(fig, [0.075, 0.13, 0.50, 0.63])
        if stage >= 1:
            ax.scatter(TRAIN[:, 0], TRAIN[:, 1], s=28, color=BLUE, alpha=0.85, lw=0)
        if stage >= 2:
            cloud(ax, 1)
        if stage >= 3:
            ax.scatter(TEST_IN[:, 0], TEST_IN[:, 1], s=70, color=YELLOW, marker="*", lw=0)
        rp = blank_axes(fig, [0.62, 0.12, 0.35, 0.66])
        items = [
            ("training data", BLUE, "The examples a model learns from —\nits practice questions."),
            (
                "distribution",
                BLUE,
                "The pattern those examples follow:\nwhich kinds of question, "
                "and how\noften each kind turns up. The\ndashed cloud.",
            ),
            (
                "test data",
                YELLOW,
                "Questions held back to check it. If\nthey follow the same "
                "pattern, they are\nin-distribution — a fair re-test.",
            ),
        ]
        for i, (term, colour, gloss) in enumerate(items[:stage]):
            y = 0.99 - i * 0.33
            rp.text(0.0, y, term, fontsize=16, color=colour, fontweight="bold", va="top")
            rp.text(0.0, y - 0.075, gloss, fontsize=12.5, color=TEXT, va="top", linespacing=1.4)
        footer(
            fig,
            "picture, not data · study guide: training-and-test-distributions · "
            "training-and-inference · corpus",
        )
        return fig_to_pil(fig)

    frames, durations = [], []
    for stage, ms in ((0, 1500), (1, 1800), (2, 2000), (3, 1800)):
        hold(frames, durations, lambda s=stage: render(s), ms=ms)
    hold(frames, durations, lambda: render(3), ms=1800, n=2)
    save_gif(frames, durations, "w06_s19_distribution.gif")


# ── s20: out of distribution ────────────────────────────────────────────
SHIFTS = [
    ("task", "a new kind of question", "practiced adding and taking away;\nasked to multiply"),
    (
        "length",
        "longer or shorter than practiced",
        "practiced 3-step problems;\nasked a 6-step one",
    ),
    (
        "format",
        "the same question, set out differently",
        "practiced tidy questions;\nasked one with a stray word in it",
    ),
]


def make_ood():
    def render(shift_t, stage):
        fig = new_fig()
        kicker_title(
            fig,
            "PART 3 · WORDS THE CRITIQUE NEEDS",
            "Out of distribution: questions unlike the practice",
            "Move the exam away from the practice questions and watch what the words mean.",
        )
        ax = question_plane(fig, [0.075, 0.13, 0.46, 0.63])
        ax.scatter(TRAIN[:, 0], TRAIN[:, 1], s=22, color=BLUE, alpha=0.6, lw=0)
        cloud(ax, 1)
        pts = TEST_IN + (TEST_OUT - TEST_IN) * ease(shift_t)
        inside = ((pts[:, 0] - 3.0) / 1.8) ** 2 + ((pts[:, 1] - 40) / 35) ** 2 <= 1
        ax.scatter(pts[inside, 0], pts[inside, 1], s=80, color=YELLOW, marker="*", lw=0)
        ax.scatter(pts[~inside, 0], pts[~inside, 1], s=80, color=RED, marker="*", lw=0)
        if shift_t > 0.05:
            ax.annotate(
                "",
                xy=(3.0 + 4.0 * ease(shift_t), 88),
                xytext=(3.0, 88),
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=2),
            )
            ax.text(3.0, 91, "distribution shift", color=ORANGE, fontsize=12)

        rp = blank_axes(fig, [0.58, 0.10, 0.39, 0.68])
        terms = [
            (
                "out-of-distribution (OOD)",
                RED,
                "Test questions outside the pattern of the\ntraining data. Red stars.",
            ),
            (
                "generalization",
                GREEN,
                "Doing well on questions you did not\npractice. On new "
                "questions of the same kind:\nexpected. On OOD questions: the hard,\ncontested "
                "case — and today's argument.",
            ),
        ]
        for i, (term, colour, gloss) in enumerate(terms[: min(stage, 2)]):
            y = 0.99 - i * 0.24
            rp.text(0.0, y, term, fontsize=15.5, color=colour, fontweight="bold", va="top")
            rp.text(0.0, y - 0.065, gloss, fontsize=12.5, color=TEXT, va="top", linespacing=1.4)
        if stage >= 3:
            rp.text(
                0.0,
                0.46,
                "Three ways to step outside — Zhao et al.'s axes:",
                fontsize=13,
                color=ORANGE,
                fontweight="bold",
                va="top",
            )
            for i, (axis, what, eg) in enumerate(SHIFTS):
                y = 0.37 - i * 0.135
                rp.text(0.0, y, axis, fontsize=13.5, color=ORANGE, fontweight="bold", va="top")
                rp.text(0.17, y, what, fontsize=12, color=TEXT, va="top")
                rp.text(0.17, y - 0.045, eg, fontsize=10.5, color=SUB, va="top", linespacing=1.3)
        footer(
            fig,
            "picture, not data · study guide: out-of-distribution-generalization · "
            "training-and-test-distributions",
        )
        return fig_to_pil(fig)

    frames, durations = [], []
    hold(frames, durations, lambda: render(0.0, 0), ms=1600)
    tween(frames, durations, lambda t: render(t, 0), n=20, ms=60)
    hold(frames, durations, lambda: render(1.0, 1), ms=2000)
    hold(frames, durations, lambda: render(1.0, 2), ms=2200)
    hold(frames, durations, lambda: render(1.0, 3), ms=1800, n=2)
    save_gif(frames, durations, "w06_s20_ood.gif")


# ── s21: data leakage ───────────────────────────────────────────────────
def make_leakage():
    def render(t, stage):
        fig = new_fig()
        kicker_title(
            fig,
            "PART 3 · WORDS THE CRITIQUE NEEDS",
            "Data leakage: the answer key got out",
            "If the exam was posted online last week, a perfect score tells you nothing "
            "about the student.",
        )
        ax = blank_axes(fig, [0.045, 0.12, 0.50, 0.66])
        ax.set_aspect("auto")
        ax.add_patch(
            Circle(
                (0.42, 0.50),
                0.36,
                facecolor=BLUE,
                alpha=0.10,
                edgecolor=BLUE,
                lw=2,
                transform=ax.transAxes,
            )
        )
        ax.text(
            0.42,
            0.80,
            "what the model was\ntrained on:\na large slice of the web",
            ha="center",
            va="center",
            fontsize=12.5,
            color=BLUE,
            linespacing=1.35,
        )
        x = lerp(0.80, 0.34, t)
        ax.add_patch(
            FancyBboxPatch(
                (x, 0.33),
                0.17,
                0.16,
                boxstyle="round,pad=0.01",
                facecolor=PANEL,
                edgecolor=YELLOW,
                lw=2,
                transform=ax.transAxes,
            )
        )
        ax.text(
            x + 0.085,
            0.41,
            "the test\n(GSM8K,\nonline since 2021)",
            ha="center",
            va="center",
            fontsize=10.5,
            color=YELLOW,
            linespacing=1.25,
        )
        rp = blank_axes(fig, [0.58, 0.12, 0.39, 0.66])
        blocks = [
            (
                "data leakage",
                RED,
                "Test questions, or their answers, turn\nup in the training "
                "data. Also called\nbenchmark contamination.",
            ),
            (
                "why it matters here",
                ORANGE,
                "A model that has seen the answer can\nscore well by "
                "remembering. You can no\nlonger tell memory from method — which\nis exactly the "
                "question about CoT.",
            ),
            (
                "Zhao et al.'s fix",
                GREEN,
                "Invent brand-new data, and train a\nmodel on it from "
                "nothing. Then nothing\ncan have leaked, because nothing else\nwas ever there.",
            ),
        ]
        for i, (term, colour, gloss) in enumerate(blocks[:stage]):
            y = 0.99 - i * 0.34
            rp.text(0.0, y, term, fontsize=15.5, color=colour, fontweight="bold", va="top")
            rp.text(0.0, y - 0.07, gloss, fontsize=12.5, color=TEXT, va="top", linespacing=1.4)
        if stage >= 3:
            fig.text(
                0.045,
                0.085,
                "An open question, not an accusation: nobody outside Google "
                "can check what PaLM was trained on.",
                fontsize=12.5,
                color=SUB,
            )
        footer(
            fig,
            "reading (optional): Zhao et al. 2025 (cot-mirage) · §1 · study guide: "
            "data-leakage · benchmark",
        )
        return fig_to_pil(fig)

    frames, durations = [], []
    hold(frames, durations, lambda: render(0.0, 0), ms=1500)
    tween(frames, durations, lambda t: render(t, 0), n=16, ms=60)
    for stage in (1, 2, 3):
        hold(frames, durations, lambda s=stage: render(1.0, s), ms=2200)
    hold(frames, durations, lambda: render(1.0, 3), ms=1800, n=2)
    save_gif(frames, durations, "w06_s21_leakage.gif")


# ── s22: how the models were trained, and how big they are ─────────────
SIZES = [  # (label, parameters, colour, row)
    ("Zhao: trained from scratch, 62K – 3B", (6.2e4, 3e9), BLUE, 0),
    ("Zhao: LLaMA3-8B, fine-tuned", (8e9,), GREEN, 1),
    ("Zhao: Qwen3-14B, fine-tuned", (14e9,), GREEN, 1),
    ("Wei: GPT-3 175B", (175e9,), ORANGE, 2),
    ("Wei: PaLM 540B", (540e9,), ORANGE, 2),
]


def make_training():
    def render(stage):
        fig = new_fig()
        kicker_title(
            fig,
            "PART 3 · WORDS THE CRITIQUE NEEDS",
            "Three ways a model can meet a task",
            "The two papers test very different models. Know which is which before "
            "comparing their results.",
        )
        cards = [
            (
                "pretrained",
                ORANGE,
                "Trained on an enormous amount of\ntext first. Wei's models: "
                "PaLM,\nGPT-3, LaMDA. Nobody outside the\ncompany knows exactly what text.",
            ),
            (
                "trained from scratch",
                BLUE,
                "Starts as random numbers and learns\nonly what you "
                "give it. Zhao's main\nmodels: they saw DataAlchemy and\nnothing else.",
            ),
            (
                "fine-tuned",
                GREEN,
                "A pretrained model trained a little\nmore on new examples "
                "with correct\nanswers — “supervised fine-tuning”,\nSFT. Zhao's check on real "
                "models.",
            ),
        ]
        for i, (head, colour, body) in enumerate(cards[:stage]):
            ax = blank_axes(fig, [0.045 + i * 0.31, 0.44, 0.29, 0.33])
            panel_box(ax, 0, 0, 1, 1, edge=colour)
            ax.text(0.06, 0.88, head, fontsize=16, color=colour, fontweight="bold", va="top")
            ax.text(0.06, 0.66, body, fontsize=12.5, color=TEXT, va="top", linespacing=1.4)
        if stage >= 4:
            ax = fig.add_axes([0.20, 0.13, 0.75, 0.22])
            ax.set_facecolor("none")
            ax.set_xscale("log")
            ax.set_xlim(3e4, 2e12)
            ax.set_ylim(-0.6, 2.6)
            ax.set_yticks([])
            for s in ("top", "right", "left"):
                ax.spines[s].set_visible(False)
            ax.spines["bottom"].set_color(FAINT)
            ax.set_xticks([1e5, 1e6, 1e7, 1e8, 1e9, 1e10, 1e11, 1e12])
            ax.set_xticklabels(["100K", "1M", "10M", "100M", "1B", "10B", "100B", "1T"])
            ax.tick_params(colors=SUB, labelsize=11, length=0)
            ax.set_xlabel(
                "parameters (log scale — each step is ten times bigger)", color=SUB, fontsize=11
            )
            rows = {0: "Zhao, from scratch", 1: "Zhao, fine-tuned", 2: "Wei"}
            for r, name in rows.items():
                fig.text(
                    0.19,
                    0.13 + 0.22 * (r + 0.6) / 3.2,
                    name,
                    fontsize=12,
                    ha="right",
                    va="center",
                    color=[BLUE, GREEN, ORANGE][r],
                )
            for label, vals, colour, row in SIZES:
                if len(vals) == 2:
                    ax.plot(vals, [row, row], color=colour, lw=8, solid_capstyle="round")
                else:
                    ax.scatter(vals, [row], s=110, color=colour, zorder=3)
                    left = label.startswith(("Zhao: LLaMA", "Wei: GPT"))
                    ax.text(
                        vals[0] * (0.8 if left else 1.25),
                        row + 0.38,
                        label.split(": ")[1],
                        fontsize=10.5,
                        color=colour,
                        ha="right" if left else "left",
                    )
            ax.annotate(
                "",
                xy=(540e9, -0.35),
                xytext=(3e9, -0.35),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=1.5),
            )
            ax.text(
                4e10,
                -0.25,
                "×180",
                fontsize=12,
                color=RED,
                ha="center",
                va="bottom",
                fontweight="bold",
            )
        footer(
            fig,
            "Zhao et al. §4.3 and Table 8 · Wei et al. Table 2 · study guide: "
            "pretraining-and-fine-tuning · parameters-and-weights",
        )
        return fig_to_pil(fig)

    frames, durations = [], []
    for stage in range(5):
        hold(frames, durations, lambda s=stage: render(s), ms=2000)
    hold(frames, durations, lambda: render(4), ms=1800, n=2)
    save_gif(frames, durations, "w06_s22_training.gif")


# ── s23: temperature ────────────────────────────────────────────────────
CANDIDATES = ["9", "8", "27", "10"]
LOGITS = np.array([4.0, 1.6, 1.0, 0.6])


def softmax(z, t):
    e = np.exp((z - z.max()) / t)
    return e / e.sum()


def make_temperature():
    # The dial's path: normal, cold, very hot, back to normal.
    path = [1.0, 0.25, 0.25, 4.0, 4.0, 1.0]

    def render(temp, stage):
        fig = new_fig()
        kicker_title(
            fig,
            "PART 3 · A WORD YOU HAVE MET: TEMPERATURE",
            "Temperature: how adventurous the next word is",
            "Review from Week 2. The model scores every candidate; softmax turns the "
            "scores into chances.",
        )
        ax = blank_axes(fig, [0.045, 0.20, 0.50, 0.56])
        ax.text(
            0.0,
            0.99,
            "…so 3 + 6 = 9. The answer is",
            fontsize=15,
            color=SUB,
            va="top",
            fontfamily="monospace",
        )
        p = softmax(LOGITS, temp)
        for i, (c, pi) in enumerate(zip(CANDIDATES, p, strict=True)):
            y = 0.78 - i * 0.18
            ax.text(0.02, y, c, fontsize=18, color=TEXT, va="center", fontfamily="monospace")
            ax.add_patch(
                Rectangle(
                    (0.12, y - 0.05), 0.70 * pi, 0.10, color=GREEN if i == 0 else PANEL_EDGE, lw=0
                )
            )
            ax.text(0.13 + 0.70 * pi, y, f"{pi:.2f}", fontsize=12, color=SUB, va="center")
        ax.text(
            0.0, 0.02, f"temperature T = {temp:.2f}", fontsize=17, color=ORANGE, fontweight="bold"
        )
        ax.text(0.55, 0.02, "illustrative scores", fontsize=10.5, color=FAINT, style="italic")

        rp = blank_axes(fig, [0.60, 0.12, 0.37, 0.64])
        rp.text(
            0.0,
            0.99,
            "low T: piles the chance onto the top\nword — the same answer every time.",
            fontsize=13,
            color=TEXT,
            va="top",
            linespacing=1.4,
        )
        rp.text(
            0.0,
            0.84,
            "high T: flattens it — unlikely words\nget picked; near random.",
            fontsize=13,
            color=TEXT,
            va="top",
            linespacing=1.4,
        )
        if stage >= 1:
            panel_box(rp, 0, 0.0, 1, 0.62, edge=ORANGE)
            rp.text(
                0.05,
                0.57,
                "Why the mirage paper cares",
                fontsize=14.5,
                color=ORANGE,
                fontweight="bold",
                va="top",
            )
            rp.text(
                0.05,
                0.47,
                "Their runs use T = 0.00001 — always the\ntop word. A critic could say the "
                "failures\nare an artifact of that setting. So they\nre-ran from 0.00001 to "
                "10: the same\npattern held up to T = 1. At 10 the\noutput is “essentially "
                "uniform sampling”.",
                fontsize=12,
                color=TEXT,
                va="top",
                linespacing=1.4,
            )
            rp.text(0.05, 0.05, "Zhao et al. Appendix D.5 · F.1", fontsize=10.5, color=FAINT)
        footer(fig, "study guide: temperature · softmax · logits")
        return fig_to_pil(fig)

    frames, durations = [], []
    hold(frames, durations, lambda: render(1.0, 0), ms=1800)
    for a, b in itertools.pairwise(path):
        if a == b:
            hold(frames, durations, lambda a=a: render(a, 0), ms=1400)
        else:
            tween(
                frames,
                durations,
                lambda t, a=a, b=b: render(float(np.exp(lerp(np.log(a), np.log(b), t))), 0),
                n=16,
                ms=60,
            )
    hold(frames, durations, lambda: render(1.0, 1), ms=1800, n=2)
    save_gif(frames, durations, "w06_s23_temperature.gif")


# ── s24: how answers are scored ─────────────────────────────────────────
TRUTH, MODEL = "HUSP", "HFCU"  # the paper's Appendix E.1.1 answer and ground truth


def levenshtein(a, b):
    d = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        prev, d[0] = d[0], i
        for j, cb in enumerate(b, 1):
            prev, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, prev + (ca != cb))
    return d[-1]


assert levenshtein(MODEL, TRUTH) == 3


def make_metrics():
    def render(stage, fixed):
        fig = new_fig()
        kicker_title(
            fig,
            "PART 3 · HOW THE PAPER MARKS AN ANSWER",
            "Exact match, edit distance, BLEU",
            "One real answer from the paper, marked three ways. Right answer: HUSP. "
            "The model wrote: HFCU.",
        )
        ax = blank_axes(fig, [0.045, 0.52, 0.91, 0.24])
        ax.text(0.0, 0.75, "should be", fontsize=12, color=FAINT, fontweight="bold", va="center")
        ax.text(0.0, 0.28, "model wrote", fontsize=12, color=FAINT, fontweight="bold", va="center")
        for i, (t, m) in enumerate(zip(TRUTH, MODEL, strict=True)):
            x = 0.16 + i * 0.075
            chip(
                ax,
                x,
                0.60,
                0.055,
                0.30,
                t,
                edge=GREEN,
                color=TEXT,
                fontsize=20,
                mono=True,
                bold=True,
            )
            same = t == m
            shown = t if (fixed > i and not same) else m
            edge = GREEN if (same or fixed > i) else RED
            chip(
                ax,
                x,
                0.13,
                0.055,
                0.30,
                shown,
                edge=edge,
                color=TEXT,
                fontsize=20,
                mono=True,
                bold=True,
            )
            if stage >= 2 and not same and fixed > i:
                ax.text(
                    x + 0.0275, 0.05, "edit", fontsize=10.5, color=ORANGE, ha="center", va="center"
                )
        blocks = [
            (
                "exact match",
                RED,
                "Right only if every letter is right.\nHere: 0. All or nothing "
                "— the paper's\n“hard” metric.",
                "0",
            ),
            (
                "edit distance",
                ORANGE,
                "The fewest single-letter changes that\nturn one into the "
                "other. Here: 3 of 4\nletters. Reported scaled from 0 (same)\nto 1. Lower is "
                "better.",
                "3 / 4 = 0.75",
            ),
            (
                "BLEU",
                BLUE,
                "Counts how many short runs of letters\nthe two share. 1 means "
                "identical, 0\nnothing shared. Higher is better.\n"
                "Borrowed from machine translation.",
                "low",
            ),
        ]
        lo = blank_axes(fig, [0.045, 0.10, 0.91, 0.38])
        for i, (term, colour, gloss, val) in enumerate(blocks[: max(0, stage)]):
            x = i * 0.34
            lo.text(x, 0.98, term, fontsize=16, color=colour, fontweight="bold", va="top")
            lo.text(
                x + 0.30,
                0.98,
                val,
                fontsize=15,
                color=colour,
                va="top",
                ha="right",
                fontfamily="monospace",
            )
            lo.text(x, 0.80, gloss, fontsize=12, color=TEXT, va="top", linespacing=1.4)
        if stage >= 4:
            lo.text(
                0.0,
                0.10,
                "Each is scored three times: on the written steps, on the "
                "final answer, and on the whole chain.",
                fontsize=13,
                color=YELLOW,
                va="bottom",
            )
        footer(
            fig, "Zhao et al. §4.3 · Appendix E.1.1 · study guide: exact-match-and-edit-distance"
        )
        return fig_to_pil(fig)

    frames, durations = [], []
    hold(frames, durations, lambda: render(0, 0), ms=1800)
    hold(frames, durations, lambda: render(1, 0), ms=2200)
    for k in range(1, 5):
        hold(frames, durations, lambda k=k: render(2, k), ms=700)
    hold(frames, durations, lambda: render(2, 4), ms=1600)
    hold(frames, durations, lambda: render(3, 0), ms=2200)
    hold(frames, durations, lambda: render(4, 0), ms=1800, n=2)
    save_gif(frames, durations, "w06_s24_metrics.gif")


if __name__ == "__main__":
    make_distribution()
    make_ood()
    make_leakage()
    make_training()
    make_temperature()
    make_metrics()
