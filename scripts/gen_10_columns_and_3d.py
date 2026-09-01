"""Slides 05b-06b: where scorecard columns come from, and escaping flatland.

w02_s05b_columns.gif  A column is derived: count the company a word keeps
w02_s06b_3d.gif       Top-down '2D' view tilts into 3D and rotates;
                      then the jump to 768-7,168 dims, pros and cons
"""

import matplotlib.pyplot as plt
from style_dark import (
    BG,
    BLUE,
    FAINT,
    GREEN,
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
    fig_to_pil,
    footer,
    hold,
    new_fig,
    save_gif,
    title_block,
    tween,
)

# ── Slide 5b: how a column gets its values ──────────────────────────
SENTS = [
    (
        "the ",
        "cat",
        " purred and licked its ",
        ["purred", "fur"],
        BLUE,
        "the cat purred and licked its fur",
    ),
    (
        "a ",
        "kitten",
        " chased yarn, claws out, purring",
        ["claws", "purring"],
        BLUE,
        "a kitten chased yarn, claws out, purring",
    ),
    (
        "the ",
        "king",
        " wore his crown to the throne",
        [],
        PURPLE,
        "the king wore his crown to the throne",
    ),
]
TALLY = [("cat", 41, +0.9, BLUE), ("kitten", 38, +0.8, BLUE), ("king", 2, -0.4, PURPLE)]


def render_columns(n_sent, count_t, phases):
    fig = new_fig()
    title_block(
        fig,
        "Where does a column come from?",
        "nobody types the scores in — count the company each word keeps, and a column appears",
        kicker="THE SCORECARD, EARNED",
    )
    ax = blank_axes(fig, [0.04, 0.08, 0.92, 0.66])

    # left: the corpus snippets, feline-company words lighting up
    ax.text(0.21, 0.97, "a tiny corpus", ha="center", fontsize=13, color=SUB)
    plain = [
        ("the cat purred and licked its fur", 0),
        ("a kitten chased yarn, claws out, purring", 1),
        ("the king wore his crown to the throne", 2),
    ]
    hots = [["purred", "fur"], ["claws,", "purring"], []]
    heads = ["cat", "kitten", "king"]
    for i, (sent, _) in enumerate(plain[:n_sent]):
        y = 0.86 - i * 0.16
        x = 0.035
        for word in sent.split(" "):
            bare = word.strip(",")
            if bare in heads:
                col, w8 = (BLUE if bare != "king" else PURPLE), "bold"
            elif word in hots[i] and "lit" in phases:
                col, w8 = YELLOW, "bold"
            else:
                col, w8 = SUB, "normal"
            ax.text(x, y, word, fontsize=14.5, color=col, fontweight=w8, fontfamily="monospace")
            x += 0.0089 * (len(word) + 1)
    if "lit" in phases:
        ax.text(
            0.21,
            0.335,
            "yellow = feline company\n(purr, fur, claws…)",
            ha="center",
            fontsize=12.5,
            color=YELLOW,
        )

    # right: tallies become a column
    if count_t > 0:
        ax.text(
            0.685,
            0.97,
            "times seen near feline words\n(per 1,000 uses, whole corpus)",
            ha="center",
            fontsize=12.5,
            color=SUB,
        )
        for i, (w, n, _score, col) in enumerate(TALLY):
            y = 0.72 - i * 0.17
            ax.text(0.545, y + 0.045, w, fontsize=14.5, color=col, ha="right", fontweight="bold")
            shown = round(n * min(count_t, 1))
            bw = 0.26 * shown / 45
            ax.add_patch(
                plt.Rectangle(
                    (0.565, y),
                    bw,
                    0.075,
                    facecolor=col,
                    alpha=0.8,
                    edgecolor="none",
                    transform=ax.transAxes,
                )
            )
            ax.text(
                0.575 + bw,
                y + 0.038,
                str(shown),
                fontsize=12.5,
                color=SUB,
                va="center",
                fontfamily="monospace",
            )
        if "column" in phases:
            ax.text(0.905, 0.86, "rescale ↓", ha="center", fontsize=12, color=SUB)
            ax.text(0.905, 0.80, '"feline?"', ha="center", fontsize=13, color=YELLOW)
            for i, (_w, _n, score, _col) in enumerate(TALLY):
                chip(
                    ax,
                    0.86,
                    0.585 - i * 0.17,
                    0.09,
                    0.10,
                    f"{score:+.1f}",
                    fontsize=13.5,
                    mono=True,
                    face=PANEL,
                    edge=BLUE if score > 0 else RED,
                    color=TEXT,
                    lw=2.0,
                )
            ax.text(
                0.905,
                0.145,
                "= one column of\nthe scorecard",
                ha="center",
                fontsize=12.5,
                color=YELLOW,
            )
    if "takeaway" in phases:
        fig.text(
            0.5,
            0.075,
            "training runs this game for hundreds of columns at once, "
            "over billions of sentences — and never names any of them",
            fontsize=15,
            color=YELLOW,
            ha="center",
        )
    footer(fig, "study guide: embedding · distributional-hypothesis · corpus")
    return fig_to_pil(fig)


frames, durations = [], []
hold(frames, durations, lambda: render_columns(1, 0, set()), ms=1100)
hold(frames, durations, lambda: render_columns(2, 0, set()), ms=900)
hold(frames, durations, lambda: render_columns(3, 0, set()), ms=900)
hold(frames, durations, lambda: render_columns(3, 0, {"lit"}), ms=1300)
tween(frames, durations, lambda t: render_columns(3, t, {"lit"}), n=14, ms=60)
hold(frames, durations, lambda: render_columns(3, 1, {"lit", "column"}), ms=1500)
hold(frames, durations, lambda: render_columns(3, 1, {"lit", "column", "takeaway"}), ms=1600)
save_gif(frames, durations, "w02_s05b_columns.gif")


# ── Slide 6b: flatland escape — 2D was a shadow of 3D ───────────────
CLUSTERS_3D = {
    BLUE: [("cat", 1.1, 4.1, 3.6), ("kitten", 2.1, 5.1, 4.3), ("dog", 1.1, 5.4, 3.4)],
    PURPLE: [("king", 5.0, 3.0, 0.6), ("queen", 5.6, 3.5, 1.1)],
    GREEN: [("coffee", 5.2, 3.2, 4.6), ("tea", 5.9, 3.7, 5.0)],
    ORANGE: [("Monday", 2.0, 1.2, 1.0), ("Friday", 1.4, 1.7, 1.5)],
}


def render_3d(elev, azim, phases):
    fig = new_fig()
    title_block(
        fig,
        "The space was never a flat page",
        "two dimensions is only what fits on a slide — the real thing has room to spare",
        kicker="DIMENSIONALITY",
    )
    ax = fig.add_axes([0.01, 0.02, 0.62, 0.80], projection="3d")
    ax.set_facecolor(BG)
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 6.5)
    ax.set_zlim(0, 5.5)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_facecolor(BG)
        axis.pane.set_edgecolor(GRID)
        axis._axinfo["grid"]["color"] = GRID
        axis._axinfo["grid"]["linewidth"] = 0.5
        axis.set_ticklabels([])
        axis.line.set_color(FAINT)
    ax.set_xlabel("dim 1", color=SUB, fontsize=10)
    ax.set_ylabel("dim 2", color=SUB, fontsize=10)
    ax.set_zlabel("dim 3" if elev < 60 else "", color=YELLOW, fontsize=10)
    ax.view_init(elev=elev, azim=azim)

    flat = elev > 60
    for col, ws in CLUSTERS_3D.items():
        for w, x, y, z in ws:
            zz = 0 if flat else z
            ax.plot([0, x], [0, y], [0, zz], color=col, lw=1.5, alpha=0.45)
            ax.scatter([x], [y], [zz], color=col, s=45, depthshade=False)
            ax.text(x, y, zz + 0.15, w, color=TEXT, fontsize=10.5)

    tx = 0.655
    if flat:
        fig.text(
            tx,
            0.62,
            "the picture so far — seen from\ndirectly above, it looks 2-D",
            fontsize=15,
            color=TEXT,
        )
        fig.text(
            tx,
            0.50,
            "…and king and coffee look like\nneighbours. do they deserve to be?",
            fontsize=14,
            color=RED,
        )
    elif "spin" in phases and "dims" not in phases:
        fig.text(
            tx,
            0.62,
            "tilt the camera: a third axis\nwas there all along",
            fontsize=15,
            color=YELLOW,
        )
        fig.text(
            tx,
            0.50,
            "king and coffee were far apart —\nthe flat view had squashed them\nonto each other",
            fontsize=14,
            color=GREEN,
        )
    if "dims" in phases:
        fig.text(tx, 0.67, "now keep adding axes:", fontsize=15, color=TEXT)
        fig.text(
            tx,
            0.61,
            "GPT-2:  768 dimensions\nDeepSeek-R1:  7,168",
            fontsize=14.5,
            color=YELLOW,
            fontfamily="monospace",
        )
        axp = blank_axes(fig, [0, 0, 1, 1])
        chip(
            axp,
            tx - 0.005,
            0.30,
            0.325,
            0.255,
            "✓ room for many distinctions at once\n"
            "   (feline, royal, plural, tense, tone…)\n"
            "✗ every column costs memory + compute\n"
            "✗ too many columns for the data\n"
            "   → the model memorizes noise\n"
            "✗ nobody can see it — every picture\n"
            "   you'll ever meet is a projection",
            fontsize=12.5,
            face=PANEL,
            edge=PANEL_EDGE,
            color=TEXT,
            lw=1.6,
        )
        fig.text(
            tx,
            0.245,
            "choosing the width is a real design\ndecision — there is no free lunch",
            fontsize=13,
            color=SUB,
        )
    footer(fig, "study guide: dimensionality · embedding-space · dimensionality-reduction")
    return fig_to_pil(fig)


frames, durations = [], []
hold(frames, durations, lambda: render_3d(90, -90, set()), ms=2000)
tween(frames, durations, lambda t: render_3d(90 - 68 * t, -90 + 25 * t, {"spin"}), n=16, ms=70)
tween(frames, durations, lambda t: render_3d(22, -65 + 360 * t, {"spin"}), n=36, ms=80)
hold(frames, durations, lambda: render_3d(22, -65, {"spin"}), ms=1200)
hold(frames, durations, lambda: render_3d(22, -65, {"spin", "dims"}), ms=1800)
save_gif(frames, durations, "w02_s06b_3d.gif")
