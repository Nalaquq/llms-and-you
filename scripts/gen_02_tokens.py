"""Slide 03: tokenization — the text is chopped before anything numeric.

w02_s03_tokens.gif  Sentence chopped into subword tokens with ids;
                    ends on the strawberry lesson.
"""

from style_dark import (
    BLUE,
    ORANGE,
    PANEL,
    PANEL_EDGE,
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

# the primer's own example — token boundaries fall inside "coders"
TOKENS = [
    ("HTML", 5835),
    ("␣cod", 20329),
    ("ers", 388),
    ("␣are", 525),
    ("␣not", 537),
    ("␣considered", 6509),
    ("␣programmers", 54846),
]
SENT = "HTML coders are not considered programmers"

W = 0.118
GAP = 0.008
X0 = 0.5 - (len(TOKENS) * (W + GAP) - GAP) / 2


def render(n_cut, id_t, phases):
    fig = new_fig()
    title_block(
        fig,
        "First, the text is chopped into tokens",
        "a token is not a word — it is a chunk from a fixed menu the model chose before training",
        kicker="TOKENS & TOKENIZATION",
    )
    ax = blank_axes(fig, [0.03, 0.10, 0.94, 0.64])

    # the raw sentence
    ax.text(
        0.5,
        0.90,
        SENT,
        ha="center",
        fontsize=22,
        color=TEXT,
        fontfamily="monospace",
        alpha=0.35 if n_cut >= len(TOKENS) else 1.0,
    )

    # tokens drop out of it one at a time
    for i, (tok, tid) in enumerate(TOKENS[:n_cut]):
        x = X0 + i * (W + GAP)
        hot = i in (1, 2)  # the split word
        chip(
            ax,
            x,
            0.55,
            W,
            0.15,
            tok,
            fontsize=15.5,
            mono=True,
            face=PANEL,
            edge=YELLOW if hot else PANEL_EDGE,
            color=YELLOW if hot else TEXT,
            lw=2.2 if hot else 1.4,
        )
        if id_t > 0:
            ax.text(
                x + W / 2,
                0.47,
                f"{tid}",
                ha="center",
                fontsize=12.5,
                color=BLUE,
                fontfamily="monospace",
                alpha=id_t,
            )

    if id_t > 0:
        ax.text(
            0.5,
            0.38,
            "each token is just an id — a row number in the model's vocabulary",
            ha="center",
            fontsize=14.5,
            color=SUB,
            alpha=id_t,
        )

    if "split" in phases:
        ax.annotate(
            '"coders" was never seen — the model got two pieces',
            xy=(X0 + 1.5 * (W + GAP) + W / 2, 0.55),
            xytext=(0.5, 0.24),
            xycoords="axes fraction",
            ha="center",
            fontsize=15,
            color=YELLOW,
            arrowprops=dict(
                arrowstyle="-|>", color=YELLOW, lw=1.8, connectionstyle="arc3,rad=0.15"
            ),
        )
    if "strawberry" in phases:
        ax.text(
            0.5,
            0.08,
            'this is why counting the r\'s in "strawberry" fails: '
            "you are asking about letters it was never shown",
            ha="center",
            fontsize=15.5,
            color=ORANGE,
        )
    footer(fig, "study guide: tokens-and-tokenization · vocabulary")
    return fig_to_pil(fig)


frames, durations = [], []
hold(frames, durations, lambda: render(0, 0, set()), ms=1300)
for k in range(1, len(TOKENS) + 1):
    hold(frames, durations, lambda k=k: render(k, 0, set()), ms=420)
tween(frames, durations, lambda t: render(len(TOKENS), t, set()), n=10, ms=55)
hold(frames, durations, lambda: render(len(TOKENS), 1, {"split"}), ms=1400)
hold(frames, durations, lambda: render(len(TOKENS), 1, {"split", "strawberry"}), ms=1200)
save_gif(frames, durations, "w02_s03_tokens.gif")
