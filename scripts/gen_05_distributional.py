"""Slide 09: the distributional hypothesis, taught by a mystery word.

w02_s09_company.gif  You've never seen "zorp" — context tells you anyway.
"""

from style_dark import (
    GREEN,
    PANEL,
    PURPLE,
    SUB,
    TEXT,
    YELLOW,
    blank_axes,
    chip,
    fig_to_pil,
    footer,
    hold,
    new_fig,
    save_gif,
    title_block,
)

SENTS = [
    ("I love drinking ", "zorp", " after a big meal."),
    ("A cold glass of ", "zorp", " on a hot day is perfect."),
    ("Two bottles of ", "zorp", " made me quite dizzy."),
]
CLUES = ["drinking", "cold glass", "bottles · dizzy"]


def render(n_sent, phases):
    fig = new_fig()
    title_block(
        fig,
        "What does “zorp” mean?",
        "you have never seen this word — read anyway",
        kicker="THE DISTRIBUTIONAL HYPOTHESIS",
    )
    ax = blank_axes(fig, [0.05, 0.10, 0.90, 0.64])

    for i, (pre, w, post) in enumerate(SENTS[:n_sent]):
        y = 0.88 - i * 0.16
        highlight = "clues" in phases
        ax.text(0.07, y, pre, fontsize=18, color=TEXT, ha="left")
        # measure-free layout: place word after fixed offsets per row
        off = [0.245, 0.235, 0.225][i]
        ax.text(0.07 + off, y, w, fontsize=18, color=PURPLE, fontweight="bold", ha="left")
        ax.text(
            0.07 + off + 0.075, y, post, fontsize=18, color=YELLOW if highlight else TEXT, ha="left"
        )
        if highlight:
            ax.text(0.78, y, f"clue: {CLUES[i]}", fontsize=13.5, color=YELLOW, ha="left")

    if "guess" in phases:
        chip(
            ax,
            0.07,
            0.135,
            0.42,
            0.17,
            "some kind of drink — probably alcoholic.\n"
            "you inferred that from the company\n"
            "the word keeps. so can a computer.",
            fontsize=14.5,
            face=PANEL,
            edge=GREEN,
            color=TEXT,
            lw=2.0,
        )
    if "hypothesis" in phases:
        fig.text(
            0.545,
            0.235,
            "“You shall know a word by the company it keeps.”",
            fontsize=17,
            color=TEXT,
            style="italic",
        )
        fig.text(
            0.545,
            0.185,
            "— J.R. Firth, 1957 · the bet every learned embedding rests on",
            fontsize=13,
            color=SUB,
        )
    footer(fig, "study guide: distributional-hypothesis · corpus")
    return fig_to_pil(fig)


frames, durations = [], []
hold(frames, durations, lambda: render(1, set()), ms=1500)
hold(frames, durations, lambda: render(2, set()), ms=1300)
hold(frames, durations, lambda: render(3, set()), ms=1300)
hold(frames, durations, lambda: render(3, {"clues"}), ms=1500)
hold(frames, durations, lambda: render(3, {"clues", "guess"}), ms=1500)
hold(frames, durations, lambda: render(3, {"clues", "guess", "hypothesis"}), ms=1500)
save_gif(frames, durations, "w02_s09_company.gif")
