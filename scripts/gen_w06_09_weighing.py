"""Week 6, part 5: weighing both papers, the debate, and the bridge to Thursday.

  w06_s40_questions_critique.gif  questions to put to the mirage paper
  w06_s41_questions_original.gif  questions to put to Wei et al.
  w06_s42_use_now.gif             how to use chain of thought, given both
  w06_s43_debate.gif              the structured debate: sides, rules, evidence each can cite
  w06_s45_closing.gif             what you can now say -- and Thursday's lab

The reading note for the mirage paper says a student's job "is not to decide
who wins; it is to describe what would settle it". These slides keep that
promise: the observations the deck adds (the bound is uninformative at
Delta = 1; the toy removes language, which Wei's ablation suggested mattered)
are posed as questions to both papers, one slide each, and the debate slide
hands each side the evidence it can use rather than a verdict.
"""

from style_dark import (
    BLUE,
    FAINT,
    GREEN,
    ORANGE,
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
    kicker_title,
    new_fig,
    panel_box,
    save_gif,
)


def question_slide(name, kicker, title, subtitle, questions, foot, colour):
    def render(n):
        fig = new_fig()
        kicker_title(fig, kicker, title, subtitle)
        ax = blank_axes(fig, [0.045, 0.08, 0.91, 0.72])
        step = 0.95 / max(len(questions), 1)
        for i, (q, where) in enumerate(questions[:n]):
            y = 0.98 - i * step
            chip(
                ax,
                0.0,
                y - 0.085,
                0.04,
                0.085,
                str(i + 1),
                edge=colour,
                color=colour,
                fontsize=15,
                mono=True,
                bold=True,
                lw=2,
            )
            ax.text(0.06, y, q, fontsize=14, color=TEXT, va="top", linespacing=1.45)
            ax.text(1.0, y, where, fontsize=11, color=FAINT, va="top", ha="right")
        footer(fig, foot)
        return fig_to_pil(fig)

    frames, durations = [], []
    for n in range(len(questions) + 1):
        hold(frames, durations, lambda n=n: render(n), ms=2600)
    hold(frames, durations, lambda: render(len(questions)), ms=1800, n=2)
    save_gif(frames, durations, name)


CRITIQUE_QS = [
    (
        "The toy has no language. Wei's ablation found equations alone did little — the words\n"
        "mattered. Does a test with no words in it test the same thing?",
        "s14–s16 · Limitations (i)",
    ),
    (
        "The largest model trained from scratch has 3 billion parameters. Wei saw the effect "
        "appear\nnear 100 billion — and hurt small models. Do the fine-tuned 8B and 14B results "
        "close that gap?",
        "s13 · s22 · §8.2",
    ),
    (
        "In the out-of-distribution tests Δ = 1, and the theorem's ceiling sits above the worst\n"
        "possible score. What work is the theorem doing in the paper?",
        "s30",
    ),
    (
        "The theorem holds for any trained model, with or without a chain of thought. What would "
        "a\nresult about chain of thought specifically look like?",
        "backup s49",
    ),
    (
        "Would a person taught only “ROT13, then shift” manage “shift, then shift” untaught?\n"
        "What should genuine reasoning do here — and what would count as seeing it?",
        "s32",
    ),
]

ORIGINAL_QS = [
    (
        "GSM8K has been online since 2021. Could PaLM have seen the questions while training?\n"
        "How would you rule that out — and could anyone outside Google?",
        "s21",
    ),
    (
        "Wei et al. call the chain “an interpretable window”. Zhao's Table 2 shows steps and\n"
        "answers coming apart. How far should you trust the window?",
        "s07 · s37",
    ),
    (
        "Wei checked chains by reading them: 48 of 50 correct answers had sound chains. Does a\n"
        "chain that reads correctly show the model used it to get the answer?",
        "s17",
    ),
    (
        "The ablation ruled out three stories. What experiment would test the fourth — that the\n"
        "written steps cause the answer?",
        "s16",
    ),
]


def make_questions():
    question_slide(
        "w06_s40_questions_critique.gif",
        "PART 5 · WEIGHING IT",
        "Questions to put to the critique",
        "Neither paper answers these. They are yours for the debate.",
        CRITIQUE_QS,
        "reading (optional): Zhao et al. 2025 (cot-mirage) · study guide: generalization-bound · "
        "out-of-distribution-generalization",
        ORANGE,
    )
    question_slide(
        "w06_s41_questions_original.gif",
        "PART 5 · WEIGHING IT",
        "…and questions to put to the original",
        "Fair is fair. The same scrutiny, turned on Wei et al.",
        ORIGINAL_QS,
        "reading: Wei et al. 2022 (wei-2022-chain-of-thought) · study guide: data-leakage · "
        "chain-of-thought-faithfulness",
        BLUE,
    )


# ── s42: using it, given both ──────────────────────────────────────────
ADVICE = [
    (
        "Both papers agree it works on problems like the ones the model has seen a lot of.",
        "Use it there: multi-step problems of familiar kinds.",
        GREEN,
    ),
    (
        "The chain is text the model wrote, not a record of how it got the answer.",
        "Check the answer on its own. Treat the chain as a draft, not an audit trail.",
        ORANGE,
    ),
    (
        "Failures cluster where a question is unlike the practice.",
        "Test your oddest cases: unusual formats, longer problems, new kinds of task.",
        RED,
    ),
    (
        "A fluent wrong chain is more convincing than a bare wrong answer.",
        "Where it matters — medicine, money, law — someone who knows the field checks.",
        YELLOW,
    ),
    (
        "You will be asked why you chose it.",
        "Say in your ADR which evidence you relied on, and which you set aside.",
        BLUE,
    ),
]


def make_use_now():
    def render(n):
        fig = new_fig()
        kicker_title(
            fig,
            "PART 5 · WEIGHING IT",
            "So how should you use it, given both papers?",
            "Whatever the debate decides, these follow from evidence both sides accept.",
        )
        ax = blank_axes(fig, [0.045, 0.08, 0.91, 0.72])
        for i, (fact, do, colour) in enumerate(ADVICE[:n]):
            y = 0.98 - i * 0.195
            ax.plot([0, 0], [y - 0.13, y], color=colour, lw=3, alpha=0.8)
            ax.text(0.02, y, fact, fontsize=13, color=SUB, va="top")
            ax.text(0.02, y - 0.06, do, fontsize=15, color=TEXT, va="top", fontweight="bold")
        footer(
            fig,
            "readings: Wei et al. 2022 · Zhao et al. 2025, Appendix G · AWS · IBM · "
            "study guide: chain-of-thought-prompting",
        )
        return fig_to_pil(fig)

    frames, durations = [], []
    for n in range(len(ADVICE) + 1):
        hold(frames, durations, lambda n=n: render(n), ms=2200)
    hold(frames, durations, lambda: render(len(ADVICE)), ms=1800, n=2)
    save_gif(frames, durations, "w06_s42_use_now.gif")


# ── s43: the debate ────────────────────────────────────────────────────
SIDE_A = [
    ("Only words, before the answer, move the score", "ablation · s16"),
    ("Robust to who writes the exemplars", "Wei §3.4"),
    ("48 of 50 correct answers had sound chains", "s17"),
    ("A new operation learned from a handful of examples", "s34"),
    ("The toy has no language in it", "s39 · Limitations (i)"),
]
SIDE_B = [
    ("100% on the practiced task, ~0% one step away", "s33"),
    ("Right steps with wrong answers, and the reverse", "s37"),
    ("Pads answers to the length it practiced", "s35–s36"),
    ("Small models: “fluent but illogical chains”", "Wei §3.2 · s13"),
    ("Wei et al. leave reasoning “an open question”", "Wei §6 · s17"),
]


def make_debate():
    def render(stage):
        fig = new_fig()
        kicker_title(
            fig,
            "PART 5 · STRUCTURED DEBATE",
            "Is chain of thought reasoning?",
            "Half the room argues each side. Evidence only — name the slide or the section.",
        )
        for c, (head, colour, items) in enumerate(
            [
                ("A · It is reasoning — or close enough to matter", GREEN, SIDE_A),
                ("B · It is pattern-matching over the training data", RED, SIDE_B),
            ]
        ):
            if stage < c + 1:
                continue
            ax = blank_axes(fig, [0.045 + c * 0.46, 0.22, 0.445, 0.58])
            panel_box(ax, 0, 0, 1, 1, edge=colour)
            ax.text(0.04, 0.94, head, fontsize=14.5, color=colour, fontweight="bold", va="top")
            ax.text(
                0.04,
                0.84,
                "evidence you can cite",
                fontsize=10.5,
                color=FAINT,
                va="top",
                fontweight="bold",
            )
            for i, (claim, where) in enumerate(items):
                y = 0.74 - i * 0.145
                ax.text(0.04, y, claim, fontsize=12.5, color=TEXT, va="top")
                ax.text(0.96, y - 0.055, where, fontsize=10.5, color=SUB, va="top", ha="right")
        if stage >= 3:
            lo = blank_axes(fig, [0.045, 0.07, 0.91, 0.12])
            lo.text(0.0, 0.85, "Rules", fontsize=13, color=PURPLE, fontweight="bold", va="top")
            lo.text(
                0.08,
                0.85,
                "Each side concedes one point the other side gets right.   "
                "Nobody may use “reasoning” without saying what they mean by it.",
                fontsize=12.5,
                color=TEXT,
                va="top",
            )
            lo.text(
                0.08,
                0.35,
                "Wei §6 is enough to argue from. The mirage paper is the "
                "strongest ammunition either side can bring.",
                fontsize=12.5,
                color=SUB,
                va="top",
            )
        footer(
            fig,
            "session activity (w06-tue) · study guide: chain-of-thought-faithfulness · "
            "out-of-distribution-generalization",
        )
        return fig_to_pil(fig)

    frames, durations = [], []
    for stage, ms in ((0, 1600), (1, 2600), (2, 2600), (3, 1800)):
        hold(frames, durations, lambda s=stage: render(s), ms=ms)
    hold(frames, durations, lambda: render(3), ms=1800, n=2)
    save_gif(frames, durations, "w06_s43_debate.gif")


# ── s45: closing ───────────────────────────────────────────────────────
LEDGER = [
    ("chain of thought", "steps written before the answer"),
    ("zero-shot · few-shot · exemplar", "how a prompt is built"),
    ("benchmark · emergence · ablation", "how the effect was shown"),
    ("distribution · OOD · data leakage", "what the critique turns on"),
    ("exact match · edit distance · BLEU", "how answers were marked"),
    ("risk · total variation · a bound", "the math of the critique"),
]


def make_closing():
    def render(stage):
        fig = new_fig()
        kicker_title(fig, "CLOSE · THURSDAY'S LAB", "Testing the Mirage")
        ax = blank_axes(fig, [0.045, 0.12, 0.44, 0.68])
        ax.text(
            0.0, 0.99, "What you can now say", fontsize=14, color=FAINT, fontweight="bold", va="top"
        )
        for i, (terms, what) in enumerate(LEDGER):
            y = 0.88 - i * 0.14
            ax.text(0.0, y, "✓", fontsize=15, color=GREEN, va="top")
            ax.text(0.06, y, terms, fontsize=13.5, color=TEXT, va="top", fontweight="bold")
            ax.text(0.06, y - 0.055, what, fontsize=11.5, color=SUB, va="top")
        if stage >= 1:
            rp = blank_axes(fig, [0.52, 0.16, 0.44, 0.64])
            panel_box(rp, 0, 0, 1, 1, edge=YELLOW)
            rp.text(
                0.05,
                0.93,
                "Thursday: test it, big and small",
                fontsize=15,
                color=YELLOW,
                fontweight="bold",
                va="top",
            )
            steps = [
                "In BoodleBox: catch a model hallucinating,\nthen try the same prompt on the "
                "others.",
                "Add “Let's think step by step.” Fixed,\nflagged, unchanged — or worse?",
                "In Colab: the Week 3 and 4 models, with\nand without chain of thought.",
            ]
            for i, s in enumerate(steps):
                y = 0.78 - i * 0.20
                rp.text(0.05, y, f"{i + 1}", fontsize=15, color=YELLOW, fontweight="bold", va="top")
                rp.text(0.12, y, s, fontsize=12.5, color=TEXT, va="top", linespacing=1.4)
            rp.text(
                0.05,
                0.14,
                "Bring one finding: “I expected X. I ran Y. I got Z,\nwhich "
                "surprised me because …”",
                fontsize=12,
                color=ORANGE,
                va="top",
                linespacing=1.4,
                style="italic",
            )
        footer(fig, "next session: Lab — Testing the Mirage (w06-thu)")
        return fig_to_pil(fig)

    frames, durations = [], []
    hold(frames, durations, lambda: render(0), ms=2600)
    hold(frames, durations, lambda: render(1), ms=1800, n=3)
    save_gif(frames, durations, "w06_s45_closing.gif")


if __name__ == "__main__":
    make_questions()
    make_use_now()
    make_debate()
    make_closing()
