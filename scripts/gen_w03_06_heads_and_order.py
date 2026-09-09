"""Week 3, the transformer: eight heads at once, and putting word order back.

  w03_s19_heads.gif     multi-head attention, with real measured heads
  w03_s20_position.gif  positional encoding, and why it is needed at all

s20 shows the stamp itself -- six numbers per position, computed from the
paper's sinusoids, under the word they get added to -- rather than the usual
heatmap of all 512 dimensions, which reads as wallpaper from the back of a
room. The point the slide has to land is that the same word at two positions
becomes two different vectors, and a table under the words shows that.

The four heads on s19 are MEASURED, not invented -- from
Helsinki-NLP/opus-mt-en-de, the model students open in the optional Week 3
deep dive. Any of them can be reproduced there. See
notebooks/w03-thu-translation.ipynb, sections 3 and 5.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
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
    fig_to_pil,
    footer,
    hold,
    math_strip,
    new_fig,
    save_gif,
)

SENT = ["The", "animal", "didn't", "cross", "the", "street", "because", "it", "was", "too", "tired"]
IT = 7

# (layer, head, plain-language job, source word index, target index, weight, colour)
# Measured here. Reproduce with notebooks/w03-thu-translation.ipynb.
HEADS = [
    (5, 0, "finds the noun the pronoun stands for", IT, 1, 0.87, GREEN),
    (1, 7, "looks at the word straight after", IT, 8, 1.00, BLUE),
    (3, 1, "always looks at the word before", None, None, 0.99, ORANGE),
    (4, 0, "looks only at itself", None, None, 0.78, PURPLE),
]


def frame(fig, kicker, title, subtitle):
    fig.text(0.045, 0.945, kicker, fontsize=13, color=PURPLE, fontweight="bold", va="top")
    fig.text(0.045, 0.895, title, fontsize=30, color=TEXT, fontweight="bold", va="top")
    fig.text(0.045, 0.838, subtitle, fontsize=15.5, color=SUB, va="top")


def curve(ax, x0, x1, y, height, colour, lw, alpha=0.9):
    t = np.linspace(0, 1, 80)
    ax.plot(
        x0 + (x1 - x0) * t,
        y + height * np.sqrt(abs(x1 - x0)) * np.sin(np.pi * t),
        color=colour,
        lw=lw,
        alpha=alpha,
        solid_capstyle="round",
    )


# =====================================================================
# SLIDE 19 — multi-head
# =====================================================================
def make_heads():
    def render(n):
        fig = new_fig()
        frame(
            fig,
            "THE TRANSFORMER · MULTI-HEAD ATTENTION",
            "Eight of those, side by side, asking different questions",
            "One head can only ask one thing at a time. So the model runs eight, and glues "
            "the answers together.",
        )
        ax = blank_axes(fig, [0.045, 0.195, 0.91, 0.60])

        for k, (layer, head, job, src, dst, weight, colour) in enumerate(HEADS[:n]):
            y = 0.85 - k * 0.235
            ax.text(
                0.0,
                y + 0.095,
                f"layer {layer}, head {head}",
                fontsize=11.5,
                color=colour,
                fontweight="bold",
            )
            ax.text(0.145, y + 0.095, job, fontsize=12.5, color=TEXT)
            ax.text(
                0.99,
                y + 0.095,
                f"{weight:.2f}",
                fontsize=12.5,
                color=colour,
                ha="right",
                fontfamily="monospace",
            )
            xs = np.linspace(0.03, 0.93, len(SENT))
            lit = {src, dst} if src is not None else set()
            for i, (x, w) in enumerate(zip(xs, SENT, strict=True)):
                ax.text(
                    x,
                    y,
                    w,
                    ha="center",
                    va="center",
                    fontsize=12,
                    color=colour if i in lit else FAINT,
                    fontweight="bold" if i in lit else "normal",
                )
            if src is not None:
                curve(ax, xs[src], xs[dst], y + 0.032, 0.055, colour, 2.6)
            elif head == 1:  # every word to the one before it
                for i in range(1, len(SENT)):
                    curve(ax, xs[i], xs[i - 1], y + 0.032, 0.04, colour, 1.5, 0.75)
            else:  # every word to itself
                for x in xs:
                    ax.plot([x, x], [y + 0.032, y + 0.075], color=colour, lw=1.5, alpha=0.75)

        if n >= len(HEADS):
            ax.text(
                0.0,
                0.03,
                "Two of these are useful, two are plumbing — and all eight run at the same "
                "time, on the same sentence.",
                fontsize=13.5,
                color=YELLOW,
                va="center",
            )

        math_strip(
            fig,
            r"$\mathrm{MultiHead}(Q,K,V) = \mathrm{Concat}(\mathrm{head}_1, \ldots, "
            r"\mathrm{head}_h)\, W^O$",
            note="h = 8 heads · measured in opus-mt-en-de",
        )
        footer(fig, "study guide: parameters-and-weights · neural-network-and-layers")
        return fig_to_pil(fig)

    frames, durations = [], []
    for n in range(1, len(HEADS) + 1):
        hold(frames, durations, lambda n=n: render(n), ms=1100)
    hold(frames, durations, lambda: render(len(HEADS)), ms=1600, n=2)
    save_gif(frames, durations, "w03_s19_heads.gif")


# =====================================================================
# SLIDE 20 — positional encoding
# =====================================================================
BITE_A = ["the", "dog", "bites", "the", "man"]
BITE_B = ["the", "man", "bites", "the", "dog"]


def positional_encoding(n_pos=40, d=32):
    """The paper's sinusoids, computed. This is Section 3.5, drawn."""
    pos = np.arange(n_pos)[:, None]
    i = np.arange(d)[None, :]
    angle = pos / np.power(10000, (2 * (i // 2)) / d)
    pe = np.where(i % 2 == 0, np.sin(angle), np.cos(angle))
    return pe


POS_DIMS = 6  # how many of the 512 numbers the slide shows per position


def make_position():
    # Positions 1..5 of the sentence, the first six numbers of each stamp.
    pe = positional_encoding(n_pos=len(BITE_A), d=32)[:, :POS_DIMS]
    cmap = plt.get_cmap("RdYlBu")
    chip_x = [0.02 + i * 0.105 for i in range(len(BITE_A))]

    def render(phase):
        fig = new_fig()
        frame(
            fig,
            "THE TRANSFORMER · POSITION",
            "Careful — we have just thrown away word order again",
            "If every word looks at every word at once, nothing in the machine knows which "
            "came first.",
        )
        ax = blank_axes(fig, [0.045, 0.195, 0.91, 0.60])

        for k, words in enumerate((BITE_A, BITE_B)):
            y = 0.94 - k * 0.105
            for x, w in zip(chip_x, words, strict=True):
                chip(
                    ax,
                    x,
                    y - 0.042,
                    0.092,
                    0.084,
                    w,
                    fontsize=12.5,
                    mono=True,
                    edge=PANEL_EDGE,
                    color=TEXT,
                )
        if phase >= 1:
            ax.text(
                0.58,
                0.90,
                "Same five words. Attention only scores pairs of\nwords, so the grid on the "
                "score slide would come\nout identical for these two.",
                fontsize=12.5,
                color=RED,
                va="center",
                linespacing=1.55,
            )
            ax.text(
                0.58,
                0.775,
                "This is the bag-of-words problem, back again.",
                fontsize=12,
                color=SUB,
                va="center",
            )

        if phase >= 2:
            ax.text(
                0.0,
                0.665,
                "THE FIX — stamp every word with where it sits, before attention sees it",
                fontsize=11.5,
                color=GREEN,
                fontweight="bold",
                va="center",
            )
            # The same first sentence, each word now carrying its position.
            for i, (x, w) in enumerate(zip(chip_x, BITE_A, strict=True)):
                chip(ax, x, 0.535, 0.092, 0.105, "", edge=GREEN, lw=1.6)
                ax.text(
                    x + 0.046,
                    0.615,
                    w,
                    fontsize=12.5,
                    color=TEXT,
                    ha="center",
                    va="center",
                    fontfamily="monospace",
                )
                ax.text(
                    x + 0.046,
                    0.565,
                    f"+ position {i + 1}",
                    fontsize=8.5,
                    color=GREEN,
                    ha="center",
                    va="center",
                )
            ax.text(
                0.0,
                0.485,
                "the stamp: six of the 512 numbers added to the word at that position — "
                "computed from a formula, never learned",
                fontsize=10,
                color=FAINT,
                va="center",
            )
            cell_h = 0.062
            for i, x in enumerate(chip_x):
                for d in range(POS_DIMS):
                    v = pe[i, d]
                    ax.add_patch(
                        Rectangle(
                            (x, 0.45 - (d + 1) * cell_h),
                            0.092,
                            cell_h - 0.006,
                            transform=ax.transAxes,
                            facecolor=cmap((v + 1) / 2),
                            edgecolor="none",
                            alpha=0.9,
                        )
                    )
                    ax.text(
                        x + 0.046,
                        0.45 - (d + 0.5) * cell_h,
                        f"{v:+.2f}",
                        fontsize=9.5,
                        color="#1b1e26",
                        ha="center",
                        va="center",
                        fontfamily="monospace",
                    )

        if phase >= 3:
            ax.text(
                0.58,
                0.60,
                "No two columns are alike. 'dog' at position 2 and\n'dog' at position 5 "
                "now carry different numbers,\nso the two sentences are different inputs "
                "again.",
                fontsize=12.5,
                color=TEXT,
                va="center",
                linespacing=1.55,
            )
            ax.text(
                0.58,
                0.40,
                "Position 500 gets a stamp made the same way as\nposition 5, so nothing "
                "had to be memorised.",
                fontsize=11.5,
                color=SUB,
                va="center",
                linespacing=1.55,
            )
            ax.text(
                0.58,
                0.22,
                "Order is not built into the machine. It is added\nto the input, like "
                "everything else.",
                fontsize=13,
                color=YELLOW,
                va="center",
                linespacing=1.55,
            )

        math_strip(
            fig,
            [
                r"$PE_{(pos,\,2i)} = \sin\!\left(pos / 10000^{2i/d}\right)$"
                r"$\qquad PE_{(pos,\,2i+1)} = \cos\!\left(pos / 10000^{2i/d}\right)$",
                r"$x_{\mathrm{input}} = x_{\mathrm{word}} + PE_{pos}$",
            ],
        )
        footer(fig, "study guide: bag-of-words · vector · embedding")
        return fig_to_pil(fig)

    frames, durations = [], []
    for p in range(4):
        hold(frames, durations, lambda p=p: render(p), ms=1300)
    hold(frames, durations, lambda: render(3), ms=1600)
    save_gif(frames, durations, "w03_s20_position.gif")


if __name__ == "__main__":
    make_heads()
    make_position()
