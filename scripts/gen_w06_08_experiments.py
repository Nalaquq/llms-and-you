"""Week 6, part 4: the mirage paper's experiments, one axis at a time.

  w06_s32_task_ladder.gif   ID, CMP, POOD, OOD -- the four task tests, on the paper's own lines
  w06_s33_collapse.gif      100% to 0%: from-scratch models and two real ones (Tables 1, 5)
  w06_s34_sft.gif           a tiny dose of the new task fixes it -- patch, or learning?
  w06_s35_length.gif        longer words, more steps: it bends the answer to the practiced size
  w06_s36_format.gif        a stray token in the prompt, and what it does
  w06_s37_unfaithful.gif    the written steps and the answer, coming apart (Table 2, App. E.1.1)
  w06_s38_robustness.gif    is it the settings? temperature, size, architecture, real models
  w06_s39_conclusions.gif   what the authors conclude -- and what they concede

Every prompt and response on these slides is either computed from
mirage_toy.py or quoted from the paper's appendix and checked there. Where a
slide quotes the authors, the quotation is exact; where it paraphrases, it
says what it is paraphrasing.
"""

from matplotlib.patches import FancyBboxPatch, Rectangle
from mirage_toy import (
    E3_MODEL,
    E3_QUERY,
    E11_MODEL,
    E11_QUERY,
    E11_TRUTH,
    E21_MODEL,
    E21_QUERY,
    E22_MODEL,
    E22_QUERY,
    WORD,
    chain,
    f1,
    f2,
)
from paper_crops import crop
from style_dark import (
    BLUE,
    FAINT,
    GREEN,
    ORANGE,
    PANEL,
    PANEL_EDGE,
    RED,
    SUB,
    TEXT,
    YELLOW,
    blank_axes,
    ease,
    fig_to_pil,
    footer,
    hold,
    kicker_title,
    new_fig,
    panel_box,
    paper_card,
    save_gif,
    token_line,
    tween,
)

FOOT = "reading (optional): Zhao et al. 2025 (cot-mirage) · "


def show_chain(ax, x, y, word, ops, fontsize=12.5, colour=TEXT, test=False):
    """One training line (prompt + response) or one test prompt, in monospace."""
    prompt, response = chain(word, ops)
    cols = [colour] * len(prompt)
    end = token_line(
        ax,
        x,
        y,
        prompt,
        [BLUE if t.startswith("[") else c for t, c in zip(prompt, cols, strict=True)],
        fontsize=fontsize,
    )
    if not test:
        token_line(ax, end, y, response, [SUB] * len(response), fontsize=fontsize)
    else:
        token_line(ax, end, y, ["?"], [YELLOW], fontsize=fontsize)


# ── s32: the task ladder ───────────────────────────────────────────────
LADDER = [
    (
        "ID",
        "in distribution",
        "tested on exactly what it practiced",
        [["F1", "F2"]],
        ["F1", "F2"],
        GREEN,
    ),
    (
        "CMP",
        "composition",
        "operations it knows, in an order it has not seen",
        [["F1", "F2"], ["F2", "F1"], ["F2", "F2"]],
        ["F1", "F1"],
        YELLOW,
    ),
    ("POOD", "partly OOD", "one operation it has never seen", [["F1", "F1"]], ["F1", "F2"], ORANGE),
    ("OOD", "out of distribution", "nothing it has seen", [["F2", "F2"]], ["F1", "F1"], RED),
]


def make_task_ladder():
    def render(n):
        fig = new_fig()
        kicker_title(
            fig,
            "PART 4 · §5.1 · THE TASK AXIS",
            "Four tests, each a step further from the practice",
            "The paper's own training and test lines (Appendix B.2.1), for the word "
            "APPL. Blue tokens name the operations.",
        )
        ax = blank_axes(fig, [0.045, 0.08, 0.91, 0.72])
        y = 0.97
        for name, long, gloss, trains, test, colour in LADDER[:n]:
            ax.text(0.0, y, name, fontsize=17, color=colour, fontweight="bold", va="top")
            ax.text(0.0, y - 0.055, long, fontsize=10.5, color=SUB, va="top")
            ax.text(0.73, y, gloss, fontsize=12.5, color=colour, va="top")
            yy = y - 0.02
            for ops in trains:
                ax.text(0.115, yy, "practiced", fontsize=10, color=FAINT, va="center")
                show_chain(ax, 0.20, yy, "APPL", ops, fontsize=12)
                yy -= 0.052
            ax.text(0.115, yy, "tested", fontsize=10, color=colour, va="center", fontweight="bold")
            show_chain(ax, 0.20, yy, "APPL", test, fontsize=12, test=True)
            y = yy - 0.085
        footer(
            fig, FOOT + "§5.1 · Appendix B.2.1 · study guide: out-of-distribution-generalization"
        )
        return fig_to_pil(fig)

    frames, durations = [], []
    for n in range(1, len(LADDER) + 1):
        hold(frames, durations, lambda n=n: render(n), ms=2600)
    hold(frames, durations, lambda: render(len(LADDER)), ms=1800, n=2)
    save_gif(frames, durations, "w06_s32_task_ladder.gif")


# ── s33: the collapse ──────────────────────────────────────────────────
SCENARIOS = [
    ("ID", "tested on exactly what it trained on", "f1∘f1  →  f1∘f1"),
    ("CMP", "a new combination of two verbs it knows", "{f1∘f1, f1∘f2, f2∘f1}  →  f2∘f2"),
    ("POOD", "one verb it has never seen", "f1∘f1  →  f1∘f2"),
    ("OOD", "nothing it has seen", "f1∘f1  →  f2∘f2"),
]
# Exact match (%) on the full chain, per scenario, in SCENARIOS order.
SERIES = [
    ("trained from scratch", BLUE, [100.00, 0.01, 0.00, 0.00]),
    ("LLaMA3-8B, fine-tuned", ORANGE, [100.00, 8.52, 0.00, 0.00]),
    ("Qwen3-14B, fine-tuned", GREEN, [100.00, 0.01, 0.00, 0.00]),
]


def make_collapse():
    img = crop("mirage_tab1_collapse")

    def render(rows):
        """`rows`: a 0..1 grow value per scenario shown."""
        fig = new_fig()
        kicker_title(
            fig,
            "PART 4 · §5.1 · TASK GENERALIZATION",
            "Perfect on what it practiced. Nothing past it.",
            "Exact match on the whole chain: every written step and the answer right.",
        )
        ax = blank_axes(fig, [0.045, 0.10, 0.60, 0.68])
        ax.text(0.0, 0.985, "train  →  test", fontsize=11, color=FAINT, fontweight="bold", va="top")
        ax.text(
            0.47,
            0.985,
            "exact match, 0–100%",
            fontsize=11,
            color=FAINT,
            fontweight="bold",
            va="top",
        )
        bar_x, bar_w = 0.47, 0.50
        row_h = 0.215
        for r, grow in enumerate(rows):
            name, gloss, notation = SCENARIOS[r]
            top = 0.90 - r * row_h
            ax.text(0.0, top, name, fontsize=17, color=TEXT, fontweight="bold", va="top")
            ax.text(0.10, top - 0.004, gloss, fontsize=12.5, color=SUB, va="top")
            ax.text(
                0.0,
                top - 0.07,
                notation,
                fontsize=12.5,
                color=TEXT,
                va="top",
                fontfamily="monospace",
            )
            ax.add_patch(
                Rectangle(
                    (bar_x, top - 0.165),
                    bar_w,
                    0.165,
                    facecolor="none",
                    edgecolor=PANEL_EDGE,
                    lw=1.0,
                )
            )
            for s, (_, colour, vals) in enumerate(SERIES):
                v = vals[r]
                y = top - 0.035 - s * 0.048
                w = bar_w * v / 100 * ease(grow)
                ax.add_patch(Rectangle((bar_x, y - 0.03), max(w, 0.002), 0.03, color=colour, lw=0))
                if grow >= 1:
                    ax.text(
                        bar_x + max(w, 0.002) + 0.008,
                        y - 0.015,
                        f"{v:.2f}".rstrip("0").rstrip(".") + "%",
                        fontsize=11,
                        color=colour,
                        va="center",
                        fontweight="bold",
                    )
        # legend
        for s, (label, colour, _) in enumerate(SERIES):
            ax.add_patch(Rectangle((0.0 + s * 0.34, 0.02), 0.018, 0.03, color=colour, lw=0))
            ax.text(0.025 + s * 0.34, 0.035, label, fontsize=11, color=SUB, va="center")

        paper_card(
            fig, [0.69, 0.50, 0.265, 0.24], img, "Zhao et al. 2025, Table 1\n(trained from scratch)"
        )
        if len(rows) == len(SCENARIOS) and rows[-1] >= 1:
            box = blank_axes(fig, [0.675, 0.14, 0.29, 0.25])
            box.add_patch(
                FancyBboxPatch(
                    (0, 0),
                    1,
                    1,
                    boxstyle="round,pad=0,rounding_size=0.04",
                    facecolor=PANEL,
                    edgecolor=PANEL_EDGE,
                    lw=1.4,
                )
            )
            box.text(
                0.06,
                0.85,
                "Not only a toy-model result",
                fontsize=13.5,
                color=ORANGE,
                fontweight="bold",
                va="top",
            )
            box.text(
                0.06,
                0.62,
                "Two real pretrained models, fine-tuned\non the same tasks, "
                "fall off the same cliff.\nThe paper's own caveat: the tasks are\n"
                "still letters, not language.",
                fontsize=12,
                color=TEXT,
                va="top",
                linespacing=1.45,
            )
        footer(fig, FOOT + "§5.1 · Table 1 · Appendix D.7, Table 5")
        return fig_to_pil(fig)

    frames, durations = [], []
    hold(frames, durations, lambda: render([]), ms=1400)
    done = []
    for _ in SCENARIOS:
        hold(frames, durations, lambda d=tuple(done): render([*d, 0.0]), ms=1700)
        tween(frames, durations, lambda t, d=tuple(done): render([*d, t]), n=12)
        done.append(1.0)
        hold(frames, durations, lambda d=tuple(done): render(list(d)), ms=1200)
    hold(frames, durations, lambda: render(done), ms=1800, n=2)
    save_gif(frames, durations, "w06_s33_collapse.gif")


# ── s37: the steps and the answer, coming apart ────────────────────────
def make_unfaithful():
    img = crop("mirage_tab2_unfaithful")
    mid, op, ans = E11_MODEL
    tmid, top_, tans = E11_TRUTH

    def render(stage):
        fig = new_fig()
        kicker_title(
            fig,
            "PART 4 · §5.1 & APPENDIX E.1.1",
            "It wrote the steps it had practiced",
            "Trained only on f1-then-f2. Asked for f1-then-f1.",
        )
        ax = blank_axes(fig, [0.045, 0.46, 0.91, 0.31])

        def line(y, label, toks, colours, alpha=1.0):
            ax.text(
                0.0, y, label, fontsize=12, color=FAINT, fontweight="bold", va="center", alpha=alpha
            )
            x = 0.16
            for tok, col in zip(toks, colours, strict=True):
                ax.text(
                    x,
                    y,
                    tok,
                    fontsize=20,
                    color=col,
                    va="center",
                    fontfamily="monospace",
                    alpha=alpha,
                    fontweight="bold" if col in (RED, GREEN) else "normal",
                )
                x += 0.01148 * (len(tok) + 1)  # one monospace cell at 20pt

        line(0.86, "prompt", [" ".join(E11_QUERY), "[F1] [F1]", "<think>"], [BLUE, BLUE, SUB])
        if stage >= 1:
            line(
                0.58,
                "model wrote",
                [" ".join(mid), f"[{op}]", "<answer>", " ".join(ans)],
                [TEXT, RED, SUB, RED],
            )
        if stage >= 2:
            line(
                0.32,
                "should be",
                [" ".join(tmid), f"[{top_}]", "<answer>", " ".join(tans)],
                [TEXT, GREEN, SUB, GREEN],
            )
        if stage >= 3:
            ax.text(
                0.16,
                0.08,
                "The first step is right. Then it names f2 — the step it always took "
                "second in training — and does f2.",
                fontsize=13.5,
                color=TEXT,
                va="center",
            )

        if stage >= 4:
            paper_card(fig, [0.057, 0.10, 0.42, 0.26], img, "Zhao et al. 2025, Table 2")
            rp = blank_axes(fig, [0.53, 0.09, 0.43, 0.32])
            rp.text(
                0.0,
                0.97,
                "Rows 1–2: right steps, wrong answer",
                fontsize=14,
                color=YELLOW,
                fontweight="bold",
                va="top",
            )
            rp.text(0.0, 0.83, "reasoning 100%, answer 0.01%", fontsize=12.5, color=SUB, va="top")
            rp.text(
                0.0,
                0.64,
                "Rows 3–4: wrong steps, right answer",
                fontsize=14,
                color=YELLOW,
                fontweight="bold",
                va="top",
            )
            rp.text(
                0.0,
                0.50,
                f"f1 and f2 commute: {WORD} → {f1(WORD)} → {f2(f1(WORD))}\n"
                f"and {WORD} → {f2(WORD)} → {f1(f2(WORD))}. Same answer, other path.",
                fontsize=12.5,
                color=SUB,
                va="top",
                linespacing=1.45,
                fontfamily="monospace",
            )
        if stage >= 5:
            fig.text(
                0.53,
                0.165,
                "The written chain and the answer can come apart —\nin both directions.",
                fontsize=13.5,
                color=ORANGE,
                fontweight="bold",
                va="top",
            )
        footer(fig, FOOT + "§5.1 · Table 2 · Appendix E.1.1 (the model output is quoted)")
        return fig_to_pil(fig)

    frames, durations = [], []
    for stage, ms in ((0, 1800), (1, 2200), (2, 2200), (3, 2400), (4, 2400), (5, 1800)):
        hold(frames, durations, lambda s=stage: render(s), ms=ms)
    hold(frames, durations, lambda: render(5), ms=1800, n=2)
    save_gif(frames, durations, "w06_s37_unfaithful.gif")


# ── s34: supervised fine-tuning, a little ──────────────────────────────
def make_sft():
    img = crop("mirage_fig4_sft")

    def render(stage):
        fig = new_fig()
        kicker_title(
            fig,
            "PART 4 · §5.1 · A DOSE OF THE NEW TASK",
            "Mix in a few examples of the new task, and it recovers",
            "Supervised fine-tuning with a tiny share of the unseen kind of question.",
        )
        paper_card(fig, [0.057, 0.30, 0.38, 0.43], img, "Zhao et al. 2025, Figure 4")
        rp = blank_axes(fig, [0.49, 0.10, 0.48, 0.70])
        rp.text(0.0, 0.99, "Read the x-axis", fontsize=15, color=BLUE, fontweight="bold", va="top")
        rp.text(
            0.0,
            0.92,
            "“SFT data ratio (1e−4)”: the share of the fine-tuning\nexamples "
            "that are the new kind. By 4 × 10⁻⁴ — four in every\nten thousand — every curve is "
            "near the top; the smaller the shift, the sooner.",
            fontsize=12.5,
            color=TEXT,
            va="top",
            linespacing=1.45,
        )
        if stage >= 1:
            rp.text(
                0.0,
                0.66,
                "Two words you need",
                fontsize=15,
                color=BLUE,
                fontweight="bold",
                va="top",
            )
            rp.text(
                0.0,
                0.59,
                "interpolation — filling in between examples you have seen.\n"
                "extrapolation — going beyond them.",
                fontsize=12.5,
                color=TEXT,
                va="top",
                linespacing=1.45,
            )
        if stage >= 2:
            panel_box(rp, 0, 0.0, 1, 0.42, edge=ORANGE)
            rp.text(
                0.04,
                0.38,
                "Two readings — you decide",
                fontsize=14,
                color=ORANGE,
                fontweight="bold",
                va="top",
            )
            rp.text(
                0.04,
                0.29,
                "The authors: “a patch, not a panacea” — it “simply\nexpands the "
                "model's ‘in-distribution’ bubble slightly”.",
                fontsize=12,
                color=TEXT,
                va="top",
                linespacing=1.4,
            )
            rp.text(
                0.04,
                0.13,
                "Or: picking up a new operation from a handful of\nexamples is "
                "what we would call learning, in a person.",
                fontsize=12,
                color=TEXT,
                va="top",
                linespacing=1.4,
            )
        fig.text(
            0.057,
            0.2,
            "Bigger models climb faster, “but exhibit the same OOD collapse\n"
            "… once the SFT support is exhausted” (Appendix D.5).",
            fontsize=12,
            color=SUB,
            va="top",
            linespacing=1.4,
        )
        footer(
            fig,
            FOOT + "§5.1 · Appendix D.5, G · study guide: pretraining-and-fine-tuning · "
            "out-of-distribution-generalization",
        )
        return fig_to_pil(fig)

    frames, durations = [], []
    for stage, ms in ((0, 2600), (1, 2400), (2, 1800)):
        hold(frames, durations, lambda s=stage: render(s), ms=ms)
    hold(frames, durations, lambda: render(2), ms=1800, n=2)
    save_gif(frames, durations, "w06_s34_sft.gif")


# ── s35: length ────────────────────────────────────────────────────────
T4 = [(2, 0.0), (3, 0.0), (4, 100.0), (5, 0.0), (6, 0.0)]  # Table 4, full-chain exact match


def spaced(s):
    return list(s)


def make_length():
    img = crop("mirage_fig6_steps")
    q_mid, q_ans = f1(E21_QUERY), f2(f1(E21_QUERY))
    m_mid, m_ans = E21_MODEL
    s_steps, s_ans = E22_MODEL

    def render(stage):
        fig = new_fig()
        kicker_title(
            fig,
            "PART 4 · §6 · THE LENGTH AXIS",
            "It bends the answer to the size it practiced",
            "Left: word length. Right: number of steps. Both examples are the "
            "paper's, from Appendix E.2.",
        )
        lp = blank_axes(fig, [0.045, 0.10, 0.44, 0.70])
        lp.text(
            0.0,
            0.99,
            "Trained only on 4-letter words",
            fontsize=15,
            color=TEXT,
            fontweight="bold",
            va="top",
        )
        for i, (length, em) in enumerate(T4):
            x = 0.02 + i * 0.19
            h = 0.28 * em / 100
            lp.add_patch(
                Rectangle((x, 0.55), 0.12, max(h, 0.004), color=GREEN if em else RED, lw=0)
            )
            lp.text(
                x + 0.06, 0.53, f"{length} letters", ha="center", va="top", fontsize=11, color=SUB
            )
            lp.text(
                x + 0.06,
                0.57 + h,
                f"{em:.0f}%",
                ha="center",
                va="bottom",
                fontsize=12,
                color=GREEN if em else RED,
                fontweight="bold",
            )
        lp.text(0.0, 0.92, "full-chain exact match (Table 4)", fontsize=10.5, color=FAINT, va="top")
        if stage >= 1:
            lp.text(0.0, 0.40, "asked", fontsize=10.5, color=FAINT, va="center")
            token_line(
                lp, 0.15, 0.40, [*E21_QUERY, "[F1]", "[F2]"], [TEXT] * 5 + [BLUE] * 2, fontsize=13
            )
            lp.text(0.0, 0.29, "wrote", fontsize=10.5, color=FAINT, va="center")
            token_line(
                lp,
                0.15,
                0.29,
                [*m_mid, "[F2]", "<answer>", *m_ans],
                [RED] * 3 + [SUB, SUB] + [RED] * 4,
                fontsize=13,
            )
            lp.text(0.0, 0.18, "should", fontsize=10.5, color=FAINT, va="center")
            token_line(
                lp,
                0.15,
                0.18,
                [*q_mid, "[F2]", "<answer>", *q_ans],
                [GREEN] * 5 + [SUB, SUB] + [GREEN] * 5,
                fontsize=13,
            )
            lp.text(
                0.0,
                0.06,
                "A five-letter word, squeezed into four letters.",
                fontsize=12.5,
                color=ORANGE,
                va="center",
            )
        if stage >= 2:
            paper_card(
                fig,
                [0.53, 0.47, 0.43, 0.27],
                img,
                "Figure 6 — change the mix of 1-, 2- and 3-step training chains",
            )
            rp = blank_axes(fig, [0.52, 0.10, 0.45, 0.28])
            rp.text(
                0.0,
                0.95,
                "Trained on two-step chains; asked for one step:",
                fontsize=12.5,
                color=TEXT,
                va="top",
            )
            token_line(
                rp,
                0.0,
                0.68,
                [*E22_QUERY, "[F1]", "→", *s_steps[:4], *s_steps[4:], "[F1]", "<answer>", *s_ans],
                [TEXT] * 4 + [BLUE, FAINT] + [RED] * 8 + [SUB, SUB] + [RED] * 4,
                fontsize=12,
            )
            rp.text(
                0.0,
                0.42,
                f"The answer should be {f1(E22_QUERY)} — one step. It padded "
                "the chain\nout to the two steps it practiced.",
                fontsize=12.5,
                color=ORANGE,
                va="top",
                linespacing=1.4,
            )
        footer(
            fig,
            FOOT + "§6 · Table 4 · Figure 6 · Appendix E.2 · study guide: "
            "out-of-distribution-generalization",
        )
        return fig_to_pil(fig)

    frames, durations = [], []
    for stage, ms in ((0, 2200), (1, 3000), (2, 1800)):
        hold(frames, durations, lambda s=stage: render(s), ms=ms)
    hold(frames, durations, lambda: render(2), ms=1800, n=2)
    save_gif(frames, durations, "w06_s35_length.gif")


# ── s36: format ────────────────────────────────────────────────────────
def make_format():
    img = crop("mirage_fig7_format")
    base = [*"APPL", "[F2]", "[F2]"]
    variants = [
        ("practiced", base, None),
        ("insert", ["A", "P", "<noise>", "P", "L", "[F2]", "[F2]"], 2),
        ("delete", ["A", "P", "L", "[F2]", "[F2]"], None),
        ("modify", ["A", "<noise>", "P", "L", "[F2]", "[F2]"], 1),
    ]
    assert chain("APPL", ["F2", "F2"])[1][-4:] == list(f2(f2("APPL")))

    def render(stage):
        fig = new_fig()
        kicker_title(
            fig,
            "PART 4 · §7 · THE FORMAT AXIS",
            "One stray token in the prompt",
            "Same question, set out slightly differently. The paper's own examples (Appendix B.4).",
        )
        lp = blank_axes(fig, [0.045, 0.40, 0.40, 0.40])
        for i, (name, toks, noise_at) in enumerate(variants[: stage + 1]):
            y = 0.92 - i * 0.24
            lp.text(
                0.0,
                y,
                name,
                fontsize=13,
                color=BLUE if i == 0 else ORANGE,
                fontweight="bold",
                va="center",
            )
            cols = [
                RED
                if (noise_at is not None and k == noise_at)
                else (BLUE if t.startswith("[") else TEXT)
                for k, t in enumerate(toks)
            ]
            token_line(lp, 0.22, y, toks, cols, fontsize=14)
        if stage >= 3:
            lp.text(0.0, 0.03, "“delete” dropped one P.", fontsize=11.5, color=SUB, va="top")
        if stage >= 4:
            paper_card(fig, [0.50, 0.44, 0.46, 0.29], img, "Zhao et al. 2025, Figure 7")
            lo = blank_axes(fig, [0.045, 0.08, 0.91, 0.26])
            lo.text(
                0.0,
                0.95,
                "Finding: “insertion makes the greatest difference”; changes to "
                "the letters and the operations matter,\n“whereas the changes to other "
                "tokens have a lesser effect on the results”.",
                fontsize=12.5,
                color=TEXT,
                va="top",
                linespacing=1.45,
            )
            lo.text(
                0.0,
                0.50,
                "Appendix E.3 — one operation deleted from the prompt:",
                fontsize=12,
                color=SUB,
                va="top",
            )
            token_line(
                lo,
                0.0,
                0.26,
                [*E3_QUERY, "[F1]", "→", *E3_MODEL],
                [TEXT] * 4 + [BLUE, FAINT] + [RED] * 5,
                fontsize=14,
            )
            lo.text(
                0.37,
                0.26,
                f"should be {' '.join(f1(E3_QUERY))} — it padded to the length it practiced.",
                fontsize=12.5,
                color=ORANGE,
                va="center",
            )
        footer(
            fig,
            FOOT + "§7 · Figure 7 · Appendix B.4, E.3 · study guide: "
            "out-of-distribution-generalization",
        )
        return fig_to_pil(fig)

    frames, durations = [], []
    for stage, ms in ((0, 1600), (1, 1600), (2, 1600), (3, 1800), (4, 1800)):
        hold(frames, durations, lambda s=stage: render(s), ms=ms)
    hold(frames, durations, lambda: render(4), ms=1800, n=2)
    save_gif(frames, durations, "w06_s36_format.gif")


# ── s38: is it the settings? ───────────────────────────────────────────
CHECKS = [
    (
        "temperature",
        "0.00001 up to 10. Same pattern up to 1;\nat 10 the output is near random.",
        "Appendix D.5",
        YELLOW,
    ),
    (
        "model size",
        "62 thousand to 3 billion parameters,\ntrained from scratch. Same pattern.",
        "§8.1 · Figure 8",
        BLUE,
    ),
    (
        "architecture",
        "Two designs, GPT-style and LLaMA-style.\nSame pattern.",
        "§8.1 · Table 8",
        BLUE,
    ),
    (
        "real models",
        "LLaMA3-8B and Qwen3-14B, fine-tuned\non the toy. Same cliff.",
        "§8.2 · Table 5",
        GREEN,
    ),
]


def make_robustness():
    def render(n, closing):
        fig = new_fig()
        kicker_title(
            fig,
            "PART 4 · §8 · CONTROLS",
            "Is it the settings? Four checks",
            "Like Wei's ablation, these rule out boring explanations — here, for the failure.",
        )
        for i, (head, body, src, colour) in enumerate(CHECKS[:n]):
            r, c = divmod(i, 2)
            ax = blank_axes(fig, [0.045 + c * 0.46, 0.50 - r * 0.21, 0.445, 0.19])
            panel_box(ax, 0, 0, 1, 1, edge=colour)
            ax.text(0.04, 0.84, head, fontsize=15, color=colour, fontweight="bold", va="top")
            ax.text(0.04, 0.56, body, fontsize=12.5, color=TEXT, va="top", linespacing=1.4)
            ax.text(0.96, 0.84, src, fontsize=10.5, color=FAINT, va="top", ha="right")
        if closing:
            fig.text(
                0.045,
                0.19,
                "On size, their summary: bigger models “reach near-perfect "
                "ID accuracy more quickly”, but scale “accelerates\ninterpolation within "
                "the … training distribution rather than enabling extrapolation beyond "
                "it” (Appendix D.5).",
                fontsize=13,
                color=ORANGE,
                va="top",
                linespacing=1.5,
            )
        footer(
            fig,
            FOOT + "§8 · Appendix D.5–D.7 · study guide: temperature · "
            "out-of-distribution-generalization",
        )
        return fig_to_pil(fig)

    frames, durations = [], []
    for n in range(len(CHECKS) + 1):
        hold(frames, durations, lambda n=n: render(n, False), ms=1800)
    hold(frames, durations, lambda: render(len(CHECKS), True), ms=1800, n=2)
    save_gif(frames, durations, "w06_s38_robustness.gif")


# ── s39: the authors' conclusions ──────────────────────────────────────
def make_conclusions():
    implications = [
        (
            "Guard against over-reliance",
            "“fluent nonsense” — plausible but flawed chains — “can "
            "be more\ndeceptive and damaging than an outright incorrect answer”",
        ),
        (
            "Prioritize OOD testing",
            "a test set that mirrors the training set cannot tell you how\nrobust a system is",
        ),
        (
            "Fine-tuning is “a patch, not a panacea”",
            "it fixes the case you trained for, not the next one",
        ),
    ]

    def render(stage):
        fig = new_fig()
        kicker_title(
            fig,
            "PART 4 · APPENDIX G · THE AUTHORS' VERDICT",
            "What Zhao et al. conclude — and what they concede",
        )
        fig.text(
            0.045,
            0.82,
            "“CoT is not a mechanism for genuine logical inference but "
            "rather a sophisticated form of structured\npattern matching, fundamentally "
            "bounded by the data distribution seen during training.”",
            fontsize=15,
            color=ORANGE,
            va="top",
            style="italic",
            linespacing=1.45,
        )
        ax = blank_axes(fig, [0.045, 0.30, 0.55, 0.40])
        if stage >= 1:
            ax.text(
                0.0,
                0.99,
                "For anyone using it",
                fontsize=14,
                color=FAINT,
                fontweight="bold",
                va="top",
            )
            for i, (head, body) in enumerate(implications):
                y = 0.84 - i * 0.30
                ax.text(0.0, y, head, fontsize=14.5, color=TEXT, fontweight="bold", va="top")
                ax.text(0.0, y - 0.10, body, fontsize=12, color=SUB, va="top", linespacing=1.4)
        if stage >= 2:
            rp = blank_axes(fig, [0.63, 0.30, 0.33, 0.40])
            panel_box(rp, 0, 0, 1, 1, edge=BLUE)
            rp.text(
                0.05,
                0.92,
                "Their own first limitation",
                fontsize=14,
                color=BLUE,
                fontweight="bold",
                va="top",
            )
            rp.text(
                0.05,
                0.76,
                "The toy “may inevitably not fully\ncapture the semantic "
                "richness,\nambiguity, and compositional\ndiversity present in natural\n"
                "language.”",
                fontsize=12.5,
                color=TEXT,
                va="top",
                linespacing=1.45,
                style="italic",
            )
            rp.text(0.05, 0.08, "Limitations (i)", fontsize=10.5, color=FAINT)
        if stage >= 3:
            fig.text(
                0.045,
                0.21,
                "Notice the jump in wording: the experiments show fragility "
                "under distribution shift;\nthe conclusion says what CoT “is not”. Which "
                "claim do the experiments support?",
                fontsize=14,
                color=TEXT,
                va="top",
                linespacing=1.5,
                fontweight="bold",
            )
        footer(fig, FOOT + "Appendix G · Limitations · study guide: chain-of-thought-faithfulness")
        return fig_to_pil(fig)

    frames, durations = [], []
    for stage, ms in ((0, 2600), (1, 2600), (2, 2600), (3, 1800)):
        hold(frames, durations, lambda s=stage: render(s), ms=ms)
    hold(frames, durations, lambda: render(3), ms=1800, n=2)
    save_gif(frames, durations, "w06_s39_conclusions.gif")


if __name__ == "__main__":
    make_task_ladder()
    make_collapse()
    make_sft()
    make_length()
    make_format()
    make_unfaithful()
    make_robustness()
    make_conclusions()
