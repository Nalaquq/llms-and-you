"""Slides 17-18: polysemy, and how modern models fix it with layers.

w02_s17_bank.gif    One dot for "bank" strains between river and money
w02_s18_layers.gif  Same input vector, different sentence, diverging as
                    it climbs the stack: static below, contextual above
"""

import matplotlib.pyplot as plt
from style_dark import (
    BLUE,
    FAINT,
    GREEN,
    PANEL,
    PANEL_EDGE,
    PURPLE,
    SUB,
    TEXT,
    YELLOW,
    blank_axes,
    chip,
    ease,
    fig_to_pil,
    footer,
    hold,
    lerp,
    new_fig,
    plane,
    save_gif,
    title_block,
    tween,
)

# ── Slide 17: the bank problem ──────────────────────────────────────
RIVER = [("river", 1.6, 4.6), ("water", 1.1, 3.8), ("shore", 2.3, 4.1), ("boat", 1.9, 3.3)]
MONEY = [("money", 7.0, 1.7), ("loan", 7.6, 2.4), ("cash", 6.4, 1.2), ("teller", 7.3, 1.0)]
MID = (4.45, 2.85)


def render_bank(split_t, phases):
    fig = new_fig()
    title_block(
        fig,
        "The flaw: one word, one vector",
        "word2vec must give ‘bank’ a single point — an average of every sense it ever had",
        kicker="POLYSEMY",
    )
    ax = plane(fig, [0.06, 0.09, 0.56, 0.68], xlim=(0, 9), ylim=(0, 6), grid=False)
    for w, x, y in RIVER:
        ax.plot(x, y, "o", ms=8, color=BLUE)
        ax.text(x + 0.12, y + 0.08, w, fontsize=12.5, color=BLUE)
    for w, x, y in MONEY:
        ax.plot(x, y, "o", ms=8, color=GREEN)
        ax.text(x + 0.12, y + 0.08, w, fontsize=12.5, color=GREEN)

    if split_t == 0:
        ax.plot(*MID, "o", ms=13, color=YELLOW)
        ax.text(MID[0] + 0.15, MID[1] + 0.12, "bank", fontsize=15, color=YELLOW, fontweight="bold")
        ax.annotate(
            "",
            xy=(1.9, 4.0),
            xytext=MID,
            arrowprops=dict(arrowstyle="-", color=FAINT, lw=1.2, linestyle=":"),
        )
        ax.annotate(
            "",
            xy=(6.9, 1.7),
            xytext=MID,
            arrowprops=dict(arrowstyle="-", color=FAINT, lw=1.2, linestyle=":"),
        )
        ax.text(
            4.45,
            1.15,
            "not near the rivers.\nnot near the money.\nwrong about both.",
            ha="center",
            fontsize=12.5,
            color=YELLOW,
        )
    else:
        e = ease(split_t)
        b1 = (lerp(MID[0], 2.35, e), lerp(MID[1], 3.55, e))
        b2 = (lerp(MID[0], 6.35, e), lerp(MID[1], 2.15, e))
        for (bx, by), lbl in [(b1, "bank₁"), (b2, "bank₂")]:
            ax.plot(bx, by, "o", ms=11, color=YELLOW)
            ax.text(bx + 0.14, by + 0.10, lbl, fontsize=13.5, color=YELLOW)

    tx = 0.665
    fig.text(tx, 0.66, "“I sat on the river bank.”", fontsize=15, color=BLUE)
    fig.text(tx, 0.60, "“I robbed a bank.”", fontsize=15, color=GREEN)
    if split_t == 0:
        fig.text(
            tx,
            0.50,
            "word2vec: same vector for both.\nthe sentence cannot change it.",
            fontsize=14.5,
            color=SUB,
        )
    if "want" in phases:
        fig.text(
            tx,
            0.50,
            "what we want: a vector computed\nper sentence, not per word —\na contextual embedding",
            fontsize=14.5,
            color=GREEN,
        )
    if "static" in phases:
        chip(
            blank_axes(fig, [0, 0, 1, 1]),
            tx - 0.005,
            0.14,
            0.30,
            0.22,
            "static: one vector per word,\nfixed at training time (word2vec)\n\n"
            "contextual: one vector per\noccurrence, computed on the fly\n"
            "(BERT, GPT, every modern LLM)",
            fontsize=13,
            face=PANEL,
            edge=PURPLE,
            color=TEXT,
            lw=2.0,
        )
    footer(fig, "study guide: polysemy · static-vs-contextual-embeddings")
    return fig_to_pil(fig)


frames, durations = [], []
hold(frames, durations, lambda: render_bank(0, set()), ms=2000)
hold(frames, durations, lambda: render_bank(0, {"want"}), ms=1400)
tween(frames, durations, lambda t: render_bank(t, {"want"}), n=18, ms=60)
hold(frames, durations, lambda: render_bank(1, {"want", "static"}), ms=1700)
save_gif(frames, durations, "w02_s17_bank.gif")


# ── Slide 18: layers add the context ────────────────────────────────
N_LAYERS = 5


def render_layers(rise_t, phases):
    fig = new_fig()
    title_block(
        fig,
        "How LLMs fix it: context is added by layers",
        "the embedding layer is still a lookup table — ‘bank’ enters "
        "both sentences as the identical vector",
        kicker="STATIC BELOW, CONTEXTUAL ABOVE",
    )
    ax = blank_axes(fig, [0.05, 0.06, 0.90, 0.70])

    # the two sentences at the bottom
    ax.text(0.28, 0.045, "“…river bank…”", ha="center", fontsize=13.5, color=BLUE)
    ax.text(0.72, 0.045, "“…robbed a bank…”", ha="center", fontsize=13.5, color=GREEN)

    # layer stack
    for i in range(N_LAYERS):
        y = 0.16 + i * 0.14
        col = PANEL_EDGE if i else YELLOW
        label = "embedding layer (lookup table — static)" if i == 0 else f"attention layer {i}"
        ax.add_patch(
            plt.Rectangle(
                (0.14, y),
                0.72,
                0.085,
                facecolor=PANEL,
                edgecolor=col,
                lw=1.8,
                transform=ax.transAxes,
            )
        )
        ax.text(
            0.5,
            y + 0.042,
            label,
            ha="center",
            fontsize=12,
            color=YELLOW if i == 0 else SUB,
            va="center",
        )

    # the two copies of "bank" climbing and diverging
    top = min(rise_t, 1.0)
    y_now = 0.145 + ease(top) * (0.16 + (N_LAYERS - 1) * 0.14 + 0.10 - 0.145)
    spread = ease(top) * 0.26
    for sgn, col in ((-1, BLUE), (1, GREEN)):
        x = 0.5 + sgn * (0.02 + spread)
        ax.plot(x, y_now, "o", ms=12, color=col, zorder=5, transform=ax.transAxes)
        ax.text(
            x + 0.015 * sgn,
            y_now + 0.03,
            "bank",
            ha="center",
            fontsize=11.5,
            color=col,
            transform=ax.transAxes,
        )
    if rise_t == 0:
        ax.text(0.5, 0.115, "identical vectors in", ha="center", fontsize=12, color=YELLOW)
    if "done" in phases:
        ax.text(
            0.5,
            0.965,
            "two different vectors out — each shaped by its whole sentence",
            ha="center",
            fontsize=14.5,
            color=TEXT,
        )
        ax.text(
            0.5,
            0.915,
            "the mixing machinery is attention — that story is Week 3",
            ha="center",
            fontsize=13.5,
            color=PURPLE,
        )
    footer(fig, "study guide: static-vs-contextual-embeddings · bert · encoder-and-decoder")
    return fig_to_pil(fig)


frames, durations = [], []
hold(frames, durations, lambda: render_layers(0, set()), ms=1800)
tween(frames, durations, lambda t: render_layers(t, set()), n=24, ms=70)
hold(frames, durations, lambda: render_layers(1, {"done"}), ms=1800)
save_gif(frames, durations, "w02_s18_layers.gif")
