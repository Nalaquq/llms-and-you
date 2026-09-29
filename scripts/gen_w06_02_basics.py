"""Week 6, part 1: what chain-of-thought prompting is, and how to use it.

  w06_s04_next_token.gif    how a model writes: one token at a time, reading its own output
  w06_s05_prompt_vocab.gif  prompt, exemplar, zero-shot, few-shot -- one prompt, three ways
  w06_s06_anatomy.gif       what a chain of thought is, in Wei et al.'s words
  w06_s07_four_claims.gif   the four things Wei et al. claim for it, and where each is tested
  w06_s08_zero_shot.gif     "Let's think step by step", and reasoning models
  w06_s09_variants.gif      the family: self-consistency, least-to-most, tree of thoughts
  w06_s10_how_to_use.gif    a recipe students can take away, with the evidence for each line

The audience has not programmed and has not done the reading, so the section
starts from the one mechanical fact that makes the technique make sense: a
model writes a token at a time and reads everything it has written before
writing the next. Once that is on the board, "show your working" stops being
a metaphor -- the working is literally more input. Every term after that is
introduced on a picture of a prompt, not in the abstract.

The probabilities on s04 are illustrative and the slide says so. Everything
attributed to a reading is quoted from it, and the notes say where.
"""

from matplotlib.patches import Circle, Rectangle
from style_dark import (
    BLUE,
    FAINT,
    GREEN,
    ORANGE,
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
    kicker_title,
    mono_advance,
    new_fig,
    panel_box,
    save_gif,
    tween,
)


def wrap_tokens(ax, tokens, colours, x0, y0, x1, line_h, fontsize=16):
    """Monospace tokens, wrapped at `x1`, each in its own colour. Returns the end (x, y)."""
    step = mono_advance(ax, fontsize)
    x, y = x0, y0
    for tok, colour in zip(tokens, colours, strict=True):
        w = step * len(tok)
        if x + w > x1:
            x, y = x0, y - line_h
        ax.text(x, y, tok, fontsize=fontsize, color=colour, va="center", fontfamily="monospace")
        x += w + step
    return x, y


# ── s04: one token at a time ────────────────────────────────────────────
# A sentence reads better than forty quoted words; split() is the point here.
PROMPT = (  # noqa: SIM905
    "Q: The cafeteria had 23 apples. They used 20 and bought 6 more. How many now? A:"
).split()
ANSWER = (  # noqa: SIM905
    "They used 20, so 23 − 20 = 3 . They bought 6 more, so 3 + 6 = 9 . The answer is 9 ."
).split()
# Candidate next words at the steps the slide stops on (index into ANSWER -> choices).
# Illustrative only: the point is the shape, not the numbers.
STOPS = {
    0: [("They", 0.52), ("The", 0.31), ("27", 0.06)],
    1: [("used", 0.71), ("had", 0.18), ("bought", 0.05)],
    19: [("9", 0.93), ("8", 0.03), ("29", 0.01)],
}


def make_next_token():
    def render(n_written, bars=None, bar_t=1.0, closing=False):
        fig = new_fig()
        kicker_title(
            fig,
            "PART 1 · HOW A MODEL WRITES",
            "One token at a time — and it reads its own writing",
            "Words stand in for tokens here. The model predicts the next one, adds it, "
            "and starts again.",
        )
        top = blank_axes(fig, [0.045, 0.53, 0.91, 0.25])
        panel_box(top, 0, 0, 1, 1)
        top.text(
            0.015,
            0.90,
            "WHAT THE MODEL READS",
            fontsize=10,
            color=FAINT,
            fontweight="bold",
            va="center",
        )
        toks = PROMPT + ANSWER[:n_written]
        cols = [SUB] * len(PROMPT) + [YELLOW] * n_written
        wrap_tokens(top, toks, cols, 0.015, 0.70, 0.985, 0.21, fontsize=16)
        if n_written:
            top.text(
                0.985,
                0.08,
                "yellow: written by the model",
                fontsize=10.5,
                color=YELLOW,
                ha="right",
                va="bottom",
                alpha=0.8,
            )

        low = blank_axes(fig, [0.045, 0.12, 0.91, 0.36])
        chip(
            low,
            0.0,
            0.34,
            0.19,
            0.32,
            "the model",
            edge=BLUE,
            color=TEXT,
            fontsize=16,
            bold=True,
            lw=2,
        )
        low.annotate(
            "",
            xy=(0.095, 0.68),
            xytext=(0.095, 1.02),
            arrowprops=dict(arrowstyle="-|>", color=FAINT, lw=1.8),
        )
        low.annotate(
            "",
            xy=(0.27, 0.50),
            xytext=(0.195, 0.50),
            arrowprops=dict(arrowstyle="-|>", color=FAINT, lw=1.8),
        )
        if bars:
            low.text(
                0.28,
                0.93,
                "how likely each next word is",
                fontsize=11,
                color=FAINT,
                fontweight="bold",
                va="center",
            )
            for i, (word, p) in enumerate(bars):
                y = 0.72 - i * 0.24
                low.text(
                    0.28,
                    y,
                    word,
                    fontsize=16,
                    color=TEXT,
                    va="center",
                    fontfamily="monospace",
                    ha="left",
                )
                low.add_patch(
                    Rectangle(
                        (0.37, y - 0.07),
                        0.30 * p * ease(bar_t),
                        0.14,
                        color=GREEN if i == 0 else PANEL_EDGE,
                        lw=0,
                    )
                )
                if bar_t >= 1:
                    low.text(0.38 + 0.30 * p, y, f"{p:.2f}", fontsize=12, color=SUB, va="center")
            low.text(0.28, 0.02, "illustrative numbers", fontsize=10, color=FAINT, style="italic")
        low.text(
            0.74,
            0.95,
            "It takes the likeliest word,\nadds it to the end,\nand reads everything\nagain "
            "before the next one.",
            fontsize=14,
            color=TEXT,
            va="top",
            linespacing=1.5,
        )
        if closing:
            low.text(
                0.74,
                0.30,
                "So by the time it writes “9”,\n“3 + 6 =” is already there\nfor it to read.",
                fontsize=14,
                color=ORANGE,
                va="top",
                linespacing=1.5,
                fontweight="bold",
            )
        if closing:
            fig.text(
                0.5,
                0.075,
                "A chain of thought is text the model writes for itself — and then reads.",
                fontsize=16,
                color=TEXT,
                ha="center",
                fontweight="bold",
            )
        footer(fig, "study guide: token-and-tokenization · training-and-inference · softmax")
        return fig_to_pil(fig)

    frames, durations = [], []
    hold(frames, durations, lambda: render(0), ms=1800)
    for i in range(len(ANSWER)):
        if i in STOPS:
            tween(frames, durations, lambda t, i=i: render(i, STOPS[i], t), n=8)
            hold(frames, durations, lambda i=i: render(i, STOPS[i]), ms=1800)
            hold(frames, durations, lambda i=i: render(i + 1, STOPS[i]), ms=900)
        else:
            hold(frames, durations, lambda i=i: render(i + 1), ms=160)
    hold(frames, durations, lambda: render(len(ANSWER), STOPS[19], closing=True), ms=1800, n=2)
    save_gif(frames, durations, "w06_s04_next_token.gif")


# ── s05: prompt vocabulary ──────────────────────────────────────────────
Q_ROGER = "Q: Roger has 5 tennis balls. He buys 2\n   more cans of 3 balls. How many now?"
Q_APPLES = "Q: The cafeteria had 23 apples. They\n   used 20, then bought 6. How many now?"
COLUMNS = [
    (
        "Zero-shot",
        BLUE,
        None,
        None,
        "No worked examples. Just the\nquestion — the model answers\ncold.",
    ),
    (
        "Few-shot",
        YELLOW,
        "A: The answer is 11.",
        None,
        "One or more worked examples\n(“shots”) first. Each is an\nexemplar. The model copies\n"
        "their pattern.",
    ),
    (
        "Few-shot chain of thought",
        GREEN,
        "A: Roger started with 5. 2 cans\n   of 3 is 6. 5 + 6 = 11.\n   The answer is 11.",
        True,
        "The same — but the exemplars\nshow their working. Now the\npattern it copies is:\n"
        "working first, then answer.",
    ),
]


def make_prompt_vocab():
    def render(n_cols, show_terms):
        fig = new_fig()
        kicker_title(
            fig,
            "PART 1 · THE WORDS FOR A PROMPT",
            "Zero-shot, few-shot, and few-shot chain of thought",
            "A prompt is everything you send the model. Here is one question, prompted three ways.",
        )
        for i, (head, colour, example, is_cot, gloss) in enumerate(COLUMNS[:n_cols]):
            ax = blank_axes(fig, [0.045 + i * 0.31, 0.10, 0.29, 0.70])
            ax.text(0.0, 0.98, head, fontsize=17, color=colour, fontweight="bold", va="top")
            panel_box(ax, 0, 0.33, 1, 0.58, edge=colour)
            y = 0.87
            if example:
                ax.text(
                    0.04,
                    y,
                    Q_ROGER,
                    fontsize=12,
                    color=SUB,
                    va="top",
                    fontfamily="monospace",
                    linespacing=1.3,
                )
                ax.text(
                    0.04,
                    y - 0.115,
                    example,
                    fontsize=12,
                    color=GREEN if is_cot else SUB,
                    va="top",
                    fontfamily="monospace",
                    linespacing=1.3,
                )
                if show_terms:
                    h = 0.115 + 0.055 * example.count("\n") + 0.045
                    ax.plot(
                        [0.975, 0.99, 0.99, 0.975],
                        [y + 0.005, y + 0.005, y - h, y - h],
                        color=colour,
                        lw=1.5,
                    )
                    ax.text(
                        0.97,
                        y - h - 0.02,
                        "← exemplar",
                        fontsize=11,
                        color=colour,
                        ha="right",
                        va="top",
                        fontweight="bold",
                    )
                y -= 0.115 + 0.055 * example.count("\n") + 0.14
            ax.text(
                0.04,
                y,
                Q_APPLES + "\nA:",
                fontsize=12,
                color=TEXT,
                va="top",
                fontfamily="monospace",
                linespacing=1.3,
            )
            if show_terms:
                ax.text(0.0, 0.29, gloss, fontsize=13, color=TEXT, va="top", linespacing=1.45)
        footer(fig, "study guide: few-shot-prompting · chain-of-thought-prompting")
        return fig_to_pil(fig)

    frames, durations = [], []
    for n in range(1, 4):
        hold(frames, durations, lambda n=n: render(n, False), ms=1500)
    hold(frames, durations, lambda: render(3, True), ms=1800, n=2)
    save_gif(frames, durations, "w06_s05_prompt_vocab.gif")


# ── s06: anatomy of a chain ─────────────────────────────────────────────
def make_anatomy():
    steps = ["They had 23 apples.", "They used 20:\n23 − 20 = 3.", "They bought 6:\n3 + 6 = 9."]

    def render(stage):
        fig = new_fig()
        kicker_title(
            fig,
            "PART 1 · WHAT A CHAIN OF THOUGHT IS",
            "A series of steps, written before the answer",
        )
        fig.text(
            0.045,
            0.82,
            "“a coherent series of intermediate reasoning steps that lead to the final "
            "answer for a problem”",
            fontsize=16,
            color=YELLOW,
            va="top",
            style="italic",
        )
        fig.text(0.045, 0.775, "— Wei et al. 2022, §2", fontsize=12, color=SUB, va="top")
        ax = blank_axes(fig, [0.045, 0.38, 0.91, 0.33])
        chip(ax, 0.0, 0.35, 0.15, 0.30, "the question", edge=BLUE, color=TEXT, fontsize=14)
        for i, s in enumerate(steps[: max(0, stage)]):
            x = 0.19 + i * 0.20
            chip(ax, x, 0.30, 0.17, 0.40, s, edge=YELLOW, color=TEXT, fontsize=13)
            ax.annotate(
                "",
                xy=(x - 0.003, 0.5),
                xytext=(x - 0.037, 0.5),
                arrowprops=dict(arrowstyle="-|>", color=FAINT, lw=1.6),
            )
        if stage >= 4:
            ax.annotate(
                "",
                xy=(0.787, 0.5),
                xytext=(0.753, 0.5),
                arrowprops=dict(arrowstyle="-|>", color=FAINT, lw=1.6),
            )
            chip(
                ax,
                0.79,
                0.35,
                0.20,
                0.30,
                "The answer is 9.",
                edge=GREEN,
                color=TEXT,
                fontsize=14,
                bold=True,
            )
            ax.plot([0.19, 0.19, 0.75, 0.75], [0.20, 0.14, 0.14, 0.20], color=YELLOW, lw=1.8)
            ax.text(
                0.47,
                0.08,
                "intermediate steps — the “chain”",
                fontsize=13,
                color=YELLOW,
                ha="center",
                va="top",
            )
            ax.plot([0.79, 0.79, 0.99, 0.99], [0.26, 0.20, 0.20, 0.26], color=GREEN, lw=1.8)
            ax.text(0.89, 0.13, "final answer", fontsize=13, color=GREEN, ha="center", va="top")
        if stage >= 5:
            notes = blank_axes(fig, [0.045, 0.09, 0.91, 0.24])
            notes.text(
                0.0,
                0.95,
                "That is the whole technique.",
                fontsize=16,
                color=TEXT,
                fontweight="bold",
                va="top",
            )
            notes.text(
                0.0,
                0.72,
                "Wei et al. wrote eight worked examples like this by hand (Appendix, "
                "Table 20) and put them in the prompt.\nNo retraining, no new model. "
                "They chose the name on purpose: it “mimics a step-by-step thought\n"
                "process for arriving at the answer” — and it comes before the answer, "
                "where an explanation would come after.",
                fontsize=13.5,
                color=SUB,
                va="top",
                linespacing=1.5,
            )
        footer(fig, "study guide: chain-of-thought-prompting · few-shot-prompting")
        return fig_to_pil(fig)

    frames, durations = [], []
    for stage, ms in ((0, 1600), (1, 900), (2, 900), (3, 900), (4, 1800), (5, 1800)):
        hold(frames, durations, lambda s=stage: render(s), ms=ms)
    hold(frames, durations, lambda: render(5), ms=1800, n=2)
    save_gif(frames, durations, "w06_s06_anatomy.gif")


# ── s07: Wei's four claims ──────────────────────────────────────────────
CLAIMS = [
    (
        "More steps, more computation",
        "“additional computation can be allocated to problems\nthat require more reasoning steps”",
        "tested by Wei et al.'s own ablation · Part 2",
        YELLOW,
    ),
    (
        "A window into the model",
        "“an interpretable window into the behavior of the model” — though “fully\ncharacterizing "
        "a model's computations … remains an open question”",
        "tested by Zhao et al. · Part 4",
        ORANGE,
    ),
    (
        "Works for many kinds of task",
        "“potentially applicable (at least in principle) to any task\nthat humans can solve via "
        "language”",
        "math, common sense, symbol puzzles in the paper",
        BLUE,
    ),
    (
        "Cheap to use",
        "“readily elicited in sufficiently large off-the-shelf language\nmodels simply by "
        "including examples”",
        "note “sufficiently large” · Part 2",
        GREEN,
    ),
]


def make_four_claims():
    def render(n):
        fig = new_fig()
        kicker_title(
            fig,
            "PART 1 · WEI ET AL. 2022, §2",
            "What the inventors claim for it — four things",
            "Read the hedges as closely as the claims. The authors put them there.",
        )
        ax = blank_axes(fig, [0.045, 0.09, 0.91, 0.71])
        for i, (head, quote, test, colour) in enumerate(CLAIMS[:n]):
            y = 0.97 - i * 0.25
            chip(
                ax,
                0.0,
                y - 0.10,
                0.045,
                0.10,
                str(i + 1),
                edge=colour,
                color=colour,
                fontsize=16,
                mono=True,
                bold=True,
                lw=2,
            )
            ax.text(0.065, y, head, fontsize=16.5, color=TEXT, fontweight="bold", va="top")
            ax.text(
                0.065,
                y - 0.065,
                quote,
                fontsize=12.5,
                color=SUB,
                va="top",
                style="italic",
                linespacing=1.4,
            )
            ax.text(1.0, y, test, fontsize=12, color=colour, va="top", ha="right")
        footer(
            fig,
            "reading: Wei et al. 2022 (wei-2022-chain-of-thought) · §2 · "
            "study guide: chain-of-thought-prompting",
        )
        return fig_to_pil(fig)

    frames, durations = [], []
    for n in range(len(CLAIMS) + 1):
        hold(frames, durations, lambda n=n: render(n), ms=1700)
    hold(frames, durations, lambda: render(len(CLAIMS)), ms=1800, n=2)
    save_gif(frames, durations, "w06_s07_four_claims.gif")


# ── s08: zero-shot chain of thought ─────────────────────────────────────
def make_zero_shot():
    def render(stage):
        fig = new_fig()
        kicker_title(
            fig,
            "PART 1 · NO EXAMPLES NEEDED",
            "Zero-shot chain of thought: just ask for the steps",
            "Writing worked examples is work. A single sentence turns out to do much "
            "of the same job.",
        )
        ax = blank_axes(fig, [0.045, 0.36, 0.44, 0.42])
        panel_box(ax, 0, 0, 1, 0.86, edge=GREEN)
        ax.text(
            0.0, 0.97, "the whole prompt", fontsize=11, color=FAINT, fontweight="bold", va="top"
        )
        ax.text(
            0.04,
            0.76,
            Q_APPLES,
            fontsize=13,
            color=TEXT,
            va="top",
            fontfamily="monospace",
            linespacing=1.35,
        )
        ax.text(
            0.04,
            0.42,
            "A: Let's think step by step.",
            fontsize=15,
            color=GREEN,
            va="top",
            fontfamily="monospace",
            fontweight="bold",
        )
        ax.text(
            0.04,
            0.20,
            "Kojima et al. 2022, cited in Zhao et al.\n§2.1. IBM and AWS call it zero-shot CoT.",
            fontsize=11.5,
            color=SUB,
            va="top",
            linespacing=1.35,
        )

        rp = blank_axes(fig, [0.53, 0.36, 0.43, 0.42])
        if stage >= 1:
            rp.text(
                0.0,
                0.97,
                "The readings' versions",
                fontsize=15,
                color=TEXT,
                fontweight="bold",
                va="top",
            )
            quotes = [
                (
                    "IBM",
                    "users add “describe your reasoning steps”\nor “explain your answer "
                    "step-by-step.”",
                ),
                ("AWS", "“Solve the following math word problems\nstep by step. …”"),
                (
                    "AWS",
                    "“Instruct the LLM to explain its thought\nprocess before reaching a "
                    "conclusion.”",
                ),
            ]
            for i, (who, q) in enumerate(quotes):
                y = 0.80 - i * 0.26
                rp.text(0.0, y, who, fontsize=12, color=BLUE, fontweight="bold", va="top")
                rp.text(0.12, y, q, fontsize=12.5, color=SUB, va="top", linespacing=1.4)
        if stage >= 2:
            lo = blank_axes(fig, [0.045, 0.09, 0.91, 0.22])
            panel_box(lo, 0, 0, 1, 1, edge=PURPLE)
            lo.text(
                0.02,
                0.80,
                "Now built in: “reasoning models”",
                fontsize=15,
                color=PURPLE,
                fontweight="bold",
                va="top",
            )
            lo.text(
                0.02,
                0.50,
                "Newer models are trained to write a long chain of thought before every "
                "answer, unasked —\nZhao et al. §2.1 calls it embedding “long-form CoT "
                "directly into inference”. Same idea, no prompt needed.",
                fontsize=13,
                color=TEXT,
                va="top",
                linespacing=1.5,
            )
        footer(fig, "study guide: chain-of-thought-prompting · few-shot-prompting")
        return fig_to_pil(fig)

    frames, durations = [], []
    for stage, ms in ((0, 2200), (1, 2200), (2, 1800)):
        hold(frames, durations, lambda s=stage: render(s), ms=ms)
    hold(frames, durations, lambda: render(2), ms=1800, n=2)
    save_gif(frames, durations, "w06_s08_zero_shot.gif")


# ── s09: the family ─────────────────────────────────────────────────────
def _dot(ax, x, y, colour, r=0.018):
    ax.add_patch(Circle((x, y), r, facecolor=colour, edgecolor="none", transform=ax.transAxes))


def make_variants():
    def panel(fig, rect, head, colour, body, source, draw):
        ax = blank_axes(fig, rect)
        panel_box(ax, 0, 0, 1, 1)
        ax.text(0.04, 0.93, head, fontsize=15, color=colour, fontweight="bold", va="top")
        draw(ax)
        ax.text(0.04, 0.30, body, fontsize=12, color=TEXT, va="top", linespacing=1.4)
        ax.text(0.04, 0.05, source, fontsize=10.5, color=FAINT, va="bottom")

    def chain(ax, y, xs, colour, end=None):
        ax.plot(xs, [y] * len(xs), color=colour, lw=1.5, alpha=0.7, transform=ax.transAxes)
        for x in xs:
            _dot(ax, x, y, colour)
        if end:
            ax.text(xs[-1] + 0.03, y, end, fontsize=11, color=colour, va="center")

    def d_chain(ax):
        chain(ax, 0.55, [0.08, 0.28, 0.48, 0.68], YELLOW, "answer")

    def d_vote(ax):
        answers = ["9", "9", "8", "9", "9"]
        for i, a in enumerate(answers):
            y = 0.76 - i * 0.075
            chain(ax, y, [0.08, 0.22, 0.36, 0.50], GREEN if a == "9" else RED)
            ax.text(0.54, y, a, fontsize=11, color=GREEN if a == "9" else RED, va="center")
        ax.text(0.66, 0.60, "vote → 9", fontsize=14, color=GREEN, va="center", fontweight="bold")

    def d_ltm(ax):
        for i, s in enumerate(["sub-question 1", "sub-question 2", "the question"]):
            chip(ax, 0.06 + i * 0.31, 0.46, 0.27, 0.18, s, edge=BLUE, color=TEXT, fontsize=10.5)

    def d_tree(ax):
        root = (0.10, 0.58)
        kids = [(0.35, 0.74), (0.35, 0.58), (0.35, 0.42)]
        grand = [(0.60, 0.80), (0.60, 0.68), (0.60, 0.48)]
        for k in kids:
            ax.plot([root[0], k[0]], [root[1], k[1]], color=FAINT, transform=ax.transAxes)
        for g, k in zip(grand, (kids[0], kids[0], kids[2]), strict=True):
            ax.plot([k[0], g[0]], [k[1], g[1]], color=FAINT, transform=ax.transAxes)
        for p in [root, *kids, *grand]:
            _dot(ax, *p, ORANGE)
        ax.text(0.37, 0.58, "  ✗ dead end", fontsize=10.5, color=RED, va="center")
        ax.text(0.63, 0.80, "  ✓", fontsize=12, color=GREEN, va="center")

    specs = [
        (
            "Chain of thought",
            YELLOW,
            "One chain, one answer. What we have\nseen so far.",
            "Wei et al. 2022",
            d_chain,
        ),
        (
            "Self-consistency",
            GREEN,
            "Sample several chains; take the\nmajority answer. Lifted GSM8K to 74%.",
            "Google Research blog (follow-up work)",
            d_vote,
        ),
        (
            "Least-to-most",
            BLUE,
            "Break the problem into smaller\nquestions first; solve them in order.",
            "AWS",
            d_ltm,
        ),
        (
            "Tree of thoughts",
            ORANGE,
            "Branch, explore several paths,\nabandon dead ends.",
            "Zhao et al. §2.1 · IBM",
            d_tree,
        ),
    ]

    def render(n):
        fig = new_fig()
        kicker_title(
            fig,
            "PART 1 · THE FAMILY",
            "Variations on writing the steps down",
            "The vendor pages list these. Each keeps the chain and changes how many, "
            "or in what shape.",
        )
        for i, (head, colour, body, src, draw) in enumerate(specs[:n]):
            r, c = divmod(i, 2)
            panel(
                fig, [0.045 + c * 0.46, 0.44 - r * 0.33, 0.445, 0.31], head, colour, body, src, draw
            )
        footer(
            fig,
            "study guide: chain-of-thought-prompting · also on the vendor pages: "
            "auto-CoT (the model writes its own exemplars), multimodal CoT",
        )
        return fig_to_pil(fig)

    frames, durations = [], []
    for n in range(1, len(specs) + 1):
        hold(frames, durations, lambda n=n: render(n), ms=1800)
    hold(frames, durations, lambda: render(len(specs)), ms=1800, n=2)
    save_gif(frames, durations, "w06_s09_variants.gif")


# ── s10: how to use it ──────────────────────────────────────────────────
RECIPE = [
    (
        "Use it for",
        "problems with several steps: arithmetic, logic, plans\nwith constraints, "
        "anything you would work on paper.",
        GREEN,
    ),
    (
        "Skip it for",
        "one-step questions (little or no gain, Wei Table 3) and\nsmall models — it "
        "made models under ~10B worse (Table 2).",
        RED,
    ),
    (
        "Ask for",
        "the final answer on its own line. Easy to find,\neasy to check against the steps.",
        BLUE,
    ),
    (
        "Check",
        "the answer separately. A tidy chain is not proof the\nanswer is right — or that "
        "the chain produced it (Part 4).",
        ORANGE,
    ),
    (
        "Budget",
        "more words out means more time and more tokens\n(IBM and AWS both say so).",
        YELLOW,
    ),
]


def make_how_to_use():
    def render(n):
        fig = new_fig()
        kicker_title(fig, "PART 1 · USING IT YOURSELF", "A recipe, with the evidence for each line")
        ax = blank_axes(fig, [0.045, 0.12, 0.40, 0.68])
        ax.text(0.0, 0.99, "before", fontsize=11, color=FAINT, fontweight="bold", va="top")
        panel_box(ax, 0, 0.66, 1, 0.28)
        ax.text(
            0.03,
            0.90,
            "If you have 7 bananas and give 4 to\nyour friend, then receive 5 "
            "more and\nthrow out 3 rotten ones, how many\ndo you have left?",
            fontsize=11.5,
            color=SUB,
            va="top",
            fontfamily="monospace",
            linespacing=1.3,
        )
        ax.text(
            0.0,
            0.60,
            "after — the AWS reading's own example",
            fontsize=11,
            color=FAINT,
            fontweight="bold",
            va="top",
        )
        panel_box(ax, 0, 0.17, 1, 0.38, edge=GREEN)
        ax.text(
            0.03,
            0.51,
            "Solve the following math word\nproblems step by step.",
            fontsize=11.5,
            color=GREEN,
            va="top",
            fontfamily="monospace",
            linespacing=1.3,
            fontweight="bold",
        )
        ax.text(
            0.03,
            0.39,
            "If you have 7 bananas … how many\ndo you have left?\n"
            "Put the final answer on its own line.",
            fontsize=11.5,
            color=SUB,
            va="top",
            fontfamily="monospace",
            linespacing=1.3,
        )
        ax.text(
            0.0,
            0.11,
            "a chain for it: 7 − 4 = 3 · 3 + 5 = 8 · 8 − 3 = 5",
            fontsize=12,
            color=YELLOW,
            va="top",
        )

        rp = blank_axes(fig, [0.49, 0.10, 0.47, 0.70])
        for i, (head, body, colour) in enumerate(RECIPE[:n]):
            y = 0.98 - i * 0.20
            rp.text(0.0, y, head, fontsize=15, color=colour, fontweight="bold", va="top")
            rp.text(0.0, y - 0.055, body, fontsize=12.5, color=TEXT, va="top", linespacing=1.4)
        footer(
            fig,
            "readings: AWS · IBM · Wei et al. 2022 Tables 2–3 · study guide: "
            "chain-of-thought-prompting",
        )
        return fig_to_pil(fig)

    frames, durations = [], []
    for n in range(len(RECIPE) + 1):
        hold(frames, durations, lambda n=n: render(n), ms=1700)
    hold(frames, durations, lambda: render(len(RECIPE)), ms=1800, n=2)
    save_gif(frames, durations, "w06_s10_how_to_use.gif")


if __name__ == "__main__":
    make_next_token()
    make_prompt_vocab()
    make_anatomy()
    make_four_claims()
    make_zero_shot()
    make_variants()
    make_how_to_use()
