"""Slides 04-05: one-hot encoding, then the hand-built feature scorecard.

w02_s04_onehot.gif     One-hot vectors; every pair equally far apart
w02_s05_scorecard.gif  Cornell-style feature table: an embedding is a
                       scorecard — but nobody writes it by hand
"""

from style_dark import (
    BLUE,
    FAINT,
    GREEN,
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
    fig_to_pil,
    footer,
    hold,
    new_fig,
    save_gif,
    title_block,
    tween,
)

# ── Slide 4: one-hot ────────────────────────────────────────────────
VOCAB = ["a", "are", "cat", "coffee", "dog", "king", "not", "queen", "the", "…"]


def render_onehot(hot_words, dot_t, phases):
    fig = new_fig()
    title_block(
        fig,
        "The obvious first try: one-hot encoding",
        "one slot per vocabulary word — put a 1 in your word's slot, 0 everywhere else",
        kicker="ONE-HOT · SPARSE VECTORS",
    )
    ax = blank_axes(fig, [0.03, 0.06, 0.94, 0.70])

    # vocabulary rail on the left
    ax.text(0.09, 0.97, "vocabulary", ha="center", fontsize=13, color=SUB)
    for i, w in enumerate(VOCAB):
        ax.text(
            0.09,
            0.88 - i * 0.088,
            w,
            ha="center",
            fontsize=14.5,
            color=TEXT if w != "…" else FAINT,
            fontfamily="monospace",
        )

    # one-hot columns for cat and dog
    cols = [("cat", 2, BLUE, 0.30), ("dog", 4, GREEN, 0.46)]
    for name, hot_i, col, x in cols:
        if name not in hot_words:
            continue
        ax.text(x, 0.97, f'"{name}"', ha="center", fontsize=15, color=col, fontweight="bold")
        for i in range(len(VOCAB)):
            v = 1 if i == hot_i else 0
            chip(
                ax,
                x - 0.033,
                0.855 - i * 0.088,
                0.066,
                0.072,
                str(v),
                fontsize=13,
                mono=True,
                face=PANEL,
                edge=col if v else PANEL_EDGE,
                color=col if v else FAINT,
                lw=2.0 if v else 1.0,
            )

    if dot_t > 0:
        y0 = 0.62
        ax.text(
            0.75,
            y0 + 0.16,
            "how similar are cat and dog?",
            ha="center",
            fontsize=16,
            color=TEXT,
            alpha=dot_t,
        )
        ax.text(
            0.75,
            y0,
            r"$\vec{cat}\cdot\vec{dog} \;=\; 0\!\cdot\!0 + 0\!\cdot\!0 + "
            r"1\!\cdot\!0 + 0\!\cdot\!0 + 0\!\cdot\!1 + \ldots \;=\; 0$",
            ha="center",
            fontsize=17,
            color=YELLOW,
            alpha=dot_t,
        )
        ax.text(
            0.75,
            y0 - 0.14,
            "zero.  and cat · the = 0,  cat · queen = 0 …",
            ha="center",
            fontsize=14.5,
            color=SUB,
            alpha=dot_t,
        )
    if "verdict" in phases:
        chip(
            ax,
            0.565,
            0.13,
            0.37,
            0.20,
            "every pair of words is exactly\nas unrelated as every other —\n"
            "identity, but no meaning",
            fontsize=14.5,
            face=PANEL,
            edge=RED,
            color=TEXT,
            lw=2.0,
        )
        ax.text(
            0.75,
            0.05,
            "and each vector is 50,000 slots of almost all zeros",
            ha="center",
            fontsize=13,
            color=RED,
        )
    footer(fig, "study guide: one-hot-encoding · sparse-and-dense-vectors")
    return fig_to_pil(fig)


frames, durations = [], []
hold(frames, durations, lambda: render_onehot(set(), 0, set()), ms=1100)
hold(frames, durations, lambda: render_onehot({"cat"}, 0, set()), ms=900)
hold(frames, durations, lambda: render_onehot({"cat", "dog"}, 0, set()), ms=900)
tween(frames, durations, lambda t: render_onehot({"cat", "dog"}, t, set()), n=10, ms=55)
hold(frames, durations, lambda: render_onehot({"cat", "dog"}, 1, set()), ms=1100)
hold(frames, durations, lambda: render_onehot({"cat", "dog"}, 1, {"verdict"}), ms=1300)
save_gif(frames, durations, "w02_s04_onehot.gif")


# ── Slide 5: the scorecard (hand-built embedding) ───────────────────
FEATS = ["living being", "feline", "human", "royalty", "verb", "plural"]
ROWS = [
    ("cat", [0.9, 0.9, 0.1, -0.7, -0.3, -0.2], BLUE),
    ("kitten", [0.8, 0.8, -0.1, -0.6, -0.5, -0.1], BLUE),
    ("houses", [-0.8, -0.4, -0.5, -0.9, 0.3, 0.8], GREEN),
    ("king", [0.5, -0.4, 0.7, 0.9, -0.7, -0.6], PURPLE),
    ("queen", [0.8, -0.1, 0.8, 0.8, -0.5, -0.9], PURPLE),
]


def render_scorecard(n_rows, n_cols, phases):
    fig = new_fig()
    title_block(
        fig,
        "An embedding is a scorecard",
        "give every word a score along a handful of traits — similar words get similar rows",
        kicker="EMBEDDINGS · DIMENSIONALITY",
    )
    ax = blank_axes(fig, [0.03, 0.06, 0.94, 0.70])

    x0, y0, cw, rh = 0.175, 0.80, 0.099, 0.112
    # feature headers, slanted feel
    for j, f in enumerate(FEATS[:n_cols]):
        ax.text(
            x0 + j * cw + cw / 2,
            y0 + 0.11,
            f,
            ha="center",
            fontsize=12.5,
            color=YELLOW,
            rotation=18,
        )
    for i, (w, vals, col) in enumerate(ROWS[:n_rows]):
        ax.text(
            x0 - 0.035,
            y0 - i * rh - 0.035,
            w,
            ha="right",
            fontsize=15.5,
            color=col,
            fontweight="bold",
        )
        for j, v in enumerate(vals[:n_cols]):
            a = abs(v)
            face = PANEL
            edge = BLUE if v > 0 else RED
            chip(
                ax,
                x0 + j * cw + 0.006,
                y0 - i * rh - 0.075,
                cw - 0.012,
                0.082,
                f"{v:+.1f}",
                fontsize=12.5,
                mono=True,
                face=face,
                edge=edge,
                color=TEXT,
                lw=0.8 + 1.8 * a,
            )

    if "similar" in phases:
        ax.annotate(
            "cat and kitten:\nnearly the same row,\nnearly the same vector",
            xy=(x0 + 5.9 * cw, y0 - 0.6 * rh),
            xytext=(0.895, 0.55),
            xycoords="axes fraction",
            ha="center",
            fontsize=14,
            color=GREEN,
            arrowprops=dict(
                arrowstyle="-|>", color=GREEN, lw=1.8, connectionstyle="arc3,rad=-0.25"
            ),
        )
    if "twist" in phases:
        chip(
            ax,
            0.09,
            0.02,
            0.55,
            0.155,
            "the twist: nobody writes this table. training fills it in,\n"
            "the traits are not labelled, and there are ~1,000 columns —\n"
            "the number of columns is the embedding's dimensionality",
            fontsize=14,
            face=PANEL,
            edge=ORANGE,
            color=TEXT,
            lw=2.0,
        )
    footer(fig, "study guide: embedding · dimensionality")
    return fig_to_pil(fig)


frames, durations = [], []
hold(frames, durations, lambda: render_scorecard(1, 6, set()), ms=1000)
for r in range(2, len(ROWS) + 1):
    hold(frames, durations, lambda r=r: render_scorecard(r, 6, set()), ms=520)
hold(frames, durations, lambda: render_scorecard(len(ROWS), 6, {"similar"}), ms=1400)
hold(frames, durations, lambda: render_scorecard(len(ROWS), 6, {"similar", "twist"}), ms=1400)
save_gif(frames, durations, "w02_s05_scorecard.gif")
