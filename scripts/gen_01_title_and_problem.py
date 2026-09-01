"""Slides 01-02: title card, and the problem of the day (text -> numbers).

w02_s01_title.png            Title card with faint embedded-word starfield
w02_s02_text_to_numbers.gif  "cat" morphs into a vector; the day's question
"""

import matplotlib.pyplot as plt
import numpy as np
from style_dark import (
    BLUE,
    FAINT,
    PANEL,
    PANEL_EDGE,
    PURPLE,
    RED,
    SUB,
    TEXT,
    YELLOW,
    blank_axes,
    chip,
    fig_to_pil,
    hold,
    lerp,
    new_fig,
    save_gif,
    save_png,
    title_block,
    tween,
)

rng = np.random.default_rng(7)

# ── Slide 1: title ───────────────────────────────────────────────────
WORDS = [
    "cat",
    "dog",
    "kitten",
    "coffee",
    "cup",
    "king",
    "queen",
    "river",
    "bank",
    "money",
    "run",
    "running",
    "Monday",
    "Tuesday",
    "vector",
    "token",
    "puppy",
    "tea",
    "castle",
    "crown",
    "water",
    "boat",
    "France",
    "Paris",
    "walk",
    "walked",
    "apple",
    "orange",
    "seven",
    "eight",
]

fig = new_fig()
ax = blank_axes(fig, [0, 0, 1, 1])
# a quiet constellation of words with faint links: an embedding space at rest
pts = {}
clusters = {
    (-0.28, 0.10): WORDS[:6],
    (0.30, 0.22): WORDS[6:12],
    (0.05, -0.25): WORDS[12:18],
    (-0.32, -0.22): WORDS[18:24],
    (0.33, -0.12): WORDS[24:30],
}


def far_enough(x, y):
    return all((x - px) ** 2 + (y - py) ** 2 > 0.0035 for px, py in pts.values())


for (cx, cy), ws in clusters.items():
    for w in ws:
        for _ in range(60):
            x = 0.5 + cx + rng.normal(0, 0.07)
            y = 0.52 + cy + rng.normal(0, 0.055)
            if far_enough(x, y):
                break
        pts[w] = (x, y)
        ax.plot(x, y, "o", ms=4, color=BLUE, alpha=0.5)
        ax.text(x + 0.008, y, w, fontsize=10.5, color=SUB, alpha=0.55, va="center")
words = list(pts)
for _ in range(26):
    a, b = rng.choice(words, 2, replace=False)
    (x0, y0), (x1, y1) = pts[a], pts[b]
    if (x0 - x1) ** 2 + (y0 - y1) ** 2 < 0.03:
        ax.plot([x0, x1], [y0, y1], color=BLUE, lw=0.7, alpha=0.18)

fig.text(
    0.5, 0.60, "How Text Becomes Numbers", fontsize=46, color=TEXT, fontweight="bold", ha="center"
)
fig.text(
    0.5,
    0.52,
    "tokens, embeddings, and why the map above exists",
    fontsize=19,
    color=SUB,
    ha="center",
)
fig.text(
    0.5,
    0.115,
    "LLMs & You  ·  Week 2  ·  attention is all you need",
    fontsize=13,
    color=FAINT,
    ha="center",
)
save_png(fig, "w02_s01_title.png")
plt.close(fig)


# ── Slide 2: the problem ─────────────────────────────────────────────
VEC = [0.62, -0.31, 0.85, -0.07, 0.44]


def render(morph_t, phases):
    fig = new_fig()
    title_block(
        fig,
        "Computers only do arithmetic",
        "so before a model can read anything, every word must become numbers",
        kicker="THE PROBLEM OF THE DAY",
    )
    ax = blank_axes(fig, [0.05, 0.10, 0.90, 0.66])

    # left: the word
    chip(
        ax, 0.06, 0.52, 0.16, 0.16, "cat", fontsize=34, bold=True, face=PANEL, edge=BLUE, color=TEXT
    )
    ax.text(0.14, 0.44, "what you type", ha="center", fontsize=13, color=SUB)

    # arrow with the mystery box
    if "arrow" in phases:
        chip(
            ax,
            0.335,
            0.53,
            0.13,
            0.14,
            "?",
            fontsize=30,
            bold=True,
            face=PANEL,
            edge=PURPLE,
            color=PURPLE,
        )
        ax.annotate(
            "",
            xy=(0.325, 0.60),
            xytext=(0.235, 0.60),
            xycoords="axes fraction",
            arrowprops=dict(arrowstyle="-|>", color=SUB, lw=2.4),
        )
        ax.annotate(
            "",
            xy=(0.565, 0.60),
            xytext=(0.475, 0.60),
            xycoords="axes fraction",
            arrowprops=dict(arrowstyle="-|>", color=SUB, lw=2.4),
        )
        ax.text(0.40, 0.44, "today's whole lecture", ha="center", fontsize=13, color=PURPLE)

    # right: the vector, digits sliding in
    if morph_t > 0:
        x0 = 0.60
        for i, v in enumerate(VEC):
            t_i = np.clip(morph_t * 5 - i, 0, 1)
            if t_i <= 0:
                continue
            y = lerp(0.85, 0.53 + 0.0, t_i)  # drop in from above
            col = BLUE if v >= 0 else RED
            chip(
                ax,
                x0 + i * 0.068,
                y,
                0.062,
                0.14,
                f"{v:+.2f}",
                fontsize=13.5,
                mono=True,
                face=PANEL,
                edge=PANEL_EDGE,
                color=col,
                alpha=t_i,
            )
        ax.text(
            0.60 + 2.5 * 0.068,
            0.44,
            "what the model sees",
            ha="center",
            fontsize=13,
            color=SUB,
            alpha=morph_t,
        )

    if "vocab" in phases:
        fig.text(
            0.5,
            0.155,
            "a list of numbers is called a $\\bf{vector}$ — and every idea today "
            "is about which numbers to pick",
            fontsize=16,
            color=YELLOW,
            ha="center",
        )
    return fig_to_pil(fig)


frames, durations = [], []
hold(frames, durations, lambda: render(0, set()), ms=1100)
hold(frames, durations, lambda: render(0, {"arrow"}), ms=1100)
tween(frames, durations, lambda t: render(t, {"arrow"}), n=18, ms=55)
hold(frames, durations, lambda: render(1, {"arrow"}), ms=900)
hold(frames, durations, lambda: render(1, {"arrow", "vocab"}), ms=1200)
save_gif(frames, durations, "w02_s02_text_to_numbers.gif")
