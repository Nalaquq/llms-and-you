"""Week 6 opening: the title, the trick in one picture, and the road through the day.

  w06_s01_title.png       the chain the whole session is about, and its question mark
  w06_s02_cold_open.gif   Wei et al.'s Figure 1: same model, same question, 27 or 9
  w06_s03_roadmap.gif     five parts, and the one word the day argues about

The cold open is the paper's own first figure because it is the fastest honest
demonstration there is: nothing about the model changes between the two
columns except one example in the prompt. Students who have not done the
reading see the effect before they see a single term, which is the order the
rest of the deck keeps -- the thing first, then the word for it.
"""

from paper_crops import crop
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
    paper_card,
    save_gif,
    save_png,
)

FOOT = "study guide: chain-of-thought-prompting"


def make_title():
    fig = new_fig()
    fig.text(0.06, 0.80, "WEEK 6 · TUESDAY", fontsize=13, color=PURPLE, fontweight="bold")
    fig.text(0.06, 0.715, "Chain of Thought", fontsize=44, color=TEXT, fontweight="bold")
    fig.text(0.06, 0.645, "— and whether it is real", fontsize=30, color=SUB)

    # The chain the cold open will produce, drawn as the deck's emblem: four
    # links and a question mark hanging off the arrow that joins them.
    ax = blank_axes(fig, [0.06, 0.33, 0.88, 0.22])
    links = ["23 apples", "23 − 20 = 3", "3 + 6 = 9", "the answer is 9"]
    colours = [SUB, YELLOW, YELLOW, GREEN]
    for i, (text, colour) in enumerate(zip(links, colours, strict=True)):
        x = 0.01 + i * 0.25
        chip(ax, x, 0.30, 0.19, 0.40, text, edge=colour, color=TEXT, fontsize=16, lw=2.0)
        if i < len(links) - 1:
            ax.annotate(
                "",
                xy=(x + 0.247, 0.50),
                xytext=(x + 0.197, 0.50),
                arrowprops=dict(arrowstyle="-|>", color=FAINT, lw=2),
            )
    ax.text(0.5, 0.92, "reasoning?", fontsize=20, color=ORANGE, ha="center", style="italic")

    fig.text(
        0.06,
        0.26,
        "Ask a model to show its working and it gets more math problems right.\n"
        "Today: what the trick is, how to use it — and a 2025 paper arguing\n"
        "that the working it shows is a mirage.",
        fontsize=16,
        color=SUB,
        va="top",
        linespacing=1.6,
    )
    fig.text(
        0.06,
        0.08,
        "Readings: AWS · IBM · Google Research · Wei et al. 2022 · (optional) Zhao et al. 2025",
        fontsize=12.5,
        color=FAINT,
    )
    save_png(fig, "w06_s01_title.png")


def make_cold_open():
    img = crop("wei_fig1_prompts")

    def render(stage):
        fig = new_fig()
        kicker_title(
            fig,
            "COLD OPEN · WEI ET AL. 2022, FIGURE 1",
            "Same model. Same question. 27 or 9.",
            "The only thing that changed is the example the model was shown first.",
        )
        paper_card(fig, [0.057, 0.14, 0.60, 0.585], img, "Wei et al. 2022, Figure 1")
        ax = blank_axes(fig, [0.70, 0.12, 0.27, 0.66])
        notes = [
            (
                "Left",
                "The example shows only an answer.\nThe model copies that habit:\n"
                "answer at once. Wrong.",
                RED,
            ),
            (
                "Right",
                "The example shows the working.\nThe model copies that habit:\n"
                "working first, then answer. Right.",
                GREEN,
            ),
            (
                "The question for today",
                "Is the working on the right how\nthe model got to 9 — "
                "or just\nwhat working looks like?",
                ORANGE,
            ),
        ]
        for i, (head, body, colour) in enumerate(notes[:stage]):
            y = 0.97 - i * 0.34
            ax.plot([0, 0], [y - 0.26, y], color=colour, lw=3, alpha=0.8)
            ax.text(0.05, y, head, fontsize=15, color=colour, fontweight="bold", va="top")
            ax.text(0.05, y - 0.07, body, fontsize=13, color=TEXT, va="top", linespacing=1.45)
        footer(fig, FOOT)
        return fig_to_pil(fig)

    frames, durations = [], []
    for stage, ms in ((0, 2600), (1, 2200), (2, 2200), (3, 1800)):
        hold(frames, durations, lambda s=stage: render(s), ms=ms)
    hold(frames, durations, lambda: render(3), ms=1800, n=2)
    save_gif(frames, durations, "w06_s02_cold_open.gif")


PARTS = [
    ("1", "What it is, and how to use it", "prompt · few-shot · exemplar · zero-shot", BLUE),
    ("2", "The evidence it works", "benchmark · emergence · ablation", YELLOW),
    (
        "3",
        "Words the critique needs",
        "distribution · out-of-distribution · data leakage ·\n"
        "temperature · exact match · edit distance",
        GREEN,
    ),
    ("4", "The critique, in full", "a toy language · risk · total variation · a bound", ORANGE),
    ("5", "Weighing it — then the debate", "what each side can and cannot claim", PURPLE),
]


def make_roadmap():
    def render(n, word):
        fig = new_fig()
        kicker_title(fig, "TODAY", "Five parts, and one word we will argue about")
        ax = blank_axes(fig, [0.045, 0.14, 0.58, 0.68])
        for i, (num, head, terms, colour) in enumerate(PARTS[:n]):
            y = 0.96 - i * 0.195
            chip(
                ax,
                0.0,
                y - 0.11,
                0.06,
                0.11,
                num,
                edge=colour,
                color=colour,
                fontsize=17,
                mono=True,
                bold=True,
                lw=2.0,
            )
            ax.text(0.10, y - 0.005, head, fontsize=17, color=TEXT, fontweight="bold", va="top")
            ax.text(0.10, y - 0.065, terms, fontsize=12, color=SUB, va="top", linespacing=1.35)
        if word:
            rp = blank_axes(fig, [0.66, 0.30, 0.30, 0.40])
            panel_box(rp, 0, 0, 1, 1, edge=ORANGE, lw=2, rounding=0.05)
            rp.text(
                0.5,
                0.72,
                "“reasoning”",
                fontsize=30,
                color=ORANGE,
                ha="center",
                fontweight="bold",
                va="center",
            )
            rp.text(
                0.5,
                0.36,
                "Every reading uses it.\nWatch whether anyone defines it —\n"
                "and note who uses it how.",
                fontsize=13.5,
                color=TEXT,
                ha="center",
                va="center",
                linespacing=1.5,
            )
        footer(fig, "session: Chain-of-Thought — and Whether It Is Real (w06-tue)")
        return fig_to_pil(fig)

    frames, durations = [], []
    for n in range(len(PARTS) + 1):
        hold(frames, durations, lambda n=n: render(n, False), ms=1300)
    hold(frames, durations, lambda: render(len(PARTS), True), ms=1800, n=2)
    save_gif(frames, durations, "w06_s03_roadmap.gif")


if __name__ == "__main__":
    make_title()
    make_cold_open()
    make_roadmap()
