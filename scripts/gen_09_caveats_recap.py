"""Slides 19-21: what the space absorbs, the ladder, and next week's teaser.

w02_s19_mirror.gif  The corpus is a mirror: bias and time-drift
w02_s20_ladder.gif  BoW -> TF-IDF -> word2vec -> BERT, each rung lighting
w02_s21_teaser.gif  The fixed-length bottleneck; attention next week
"""

from style_dark import (
    BLUE,
    FAINT,
    GREEN,
    ORANGE,
    PANEL,
    PURPLE,
    RED,
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
    save_gif,
    title_block,
    tween,
)

# ── Slide 19: the corpus is a mirror ────────────────────────────────
DRIFT = [
    ("broadcast, 1850s", "sow seeds"),
    ("broadcast, 1900s", "newspapers"),
    ("broadcast, 1990s", "radio · tv"),
]


def render_mirror(phases):
    fig = new_fig()
    title_block(
        fig,
        "The space is a mirror, not an oracle",
        "geometry records whatever the corpus reliably does — including what we'd rather it didn't",
        kicker="WHAT TRAINING ABSORBS",
    )
    ax = blank_axes(fig, [0.04, 0.07, 0.92, 0.68])

    if "bias" in phases:
        ax.text(0.25, 0.94, "bias, faithfully copied", ha="center", fontsize=15.5, color=ORANGE)
        ax.text(
            0.25,
            0.86,
            "project real embeddings on the she–he direction:",
            ha="center",
            fontsize=12,
            color=SUB,
        )
        pairs = [
            ("she →", "homemaker · nurse\nreceptionist · librarian"),
            ("he →", "maestro · skipper\nphilosopher · captain"),
        ]
        for i, (side, words) in enumerate(pairs):
            y = 0.62 - i * 0.26
            ax.text(0.115, y, side, fontsize=14, color=TEXT, ha="right", fontweight="bold")
            ax.text(0.145, y, words, fontsize=12.5, color=ORANGE, va="center")
        ax.text(
            0.25,
            0.085,
            "nobody programmed this.\nthe corpus put it there. [Bolukbasi et al., 2016]",
            ha="center",
            fontsize=11.5,
            color=SUB,
        )
    if "drift" in phases:
        ax.text(0.72, 0.94, "meaning moves with time", ha="center", fontsize=15.5, color=BLUE)
        for i, (era, near) in enumerate(DRIFT):
            chip(
                ax,
                0.565,
                0.585 - i * 0.22,
                0.16,
                0.11,
                era.split(",")[1],
                fontsize=12.5,
                face=PANEL,
                edge=BLUE,
                color=TEXT,
                lw=1.6,
            )
            ax.text(0.74, 0.64 - i * 0.22, f"nearest: {near}", fontsize=12.5, color=SUB)
            if i:
                ax.annotate(
                    "",
                    xy=(0.645, 0.585 - i * 0.22 + 0.115),
                    xytext=(0.645, 0.585 - (i - 1) * 0.22),
                    xycoords="axes fraction",
                    arrowprops=dict(arrowstyle="-|>", color=FAINT, lw=1.6),
                )
        ax.text(
            0.72,
            0.085,
            'the word "broadcast", embedded from corpora\nof three different centuries',
            ha="center",
            fontsize=11.5,
            color=SUB,
        )
    if "moral" in phases:
        fig.text(
            0.5,
            0.055,
            "when an embedding surprises you, interrogate the corpus — "
            "not the model's 'understanding'",
            fontsize=14.5,
            color=YELLOW,
            ha="center",
        )
    footer(fig, "study guide: corpus · distributional-hypothesis")
    return fig_to_pil(fig)


frames, durations = [], []
hold(frames, durations, lambda: render_mirror({"bias"}), ms=1800)
hold(frames, durations, lambda: render_mirror({"bias", "drift"}), ms=1800)
hold(frames, durations, lambda: render_mirror({"bias", "drift", "moral"}), ms=1600)
save_gif(frames, durations, "w02_s19_mirror.gif")


# ── Slide 20: the ladder ────────────────────────────────────────────
RUNGS = [
    ("bag of words", "counts words", "throws away order", BLUE),
    ("TF-IDF", "fixes importance", "still no meaning", GREEN),
    ("word2vec", "learns meaning from neighbours", "one vector per word", ORANGE),
    ("BERT & LLMs", "a vector per occurrence, in context", "the story continues…", PURPLE),
]


def render_ladder(n, phases):
    fig = new_fig()
    title_block(
        fig,
        "Four rungs, one ladder",
        "each method fixes its predecessor's flaw — and exposes its own",
        kicker="WEEK 2, IN ONE PICTURE",
    )
    ax = blank_axes(fig, [0.05, 0.06, 0.90, 0.70])
    for i, (name, fixes, flaw, col) in enumerate(RUNGS[:n]):
        y = 0.06 + i * 0.235
        x = 0.06 + i * 0.115
        chip(
            ax,
            x,
            y,
            0.30,
            0.16,
            name,
            fontsize=17,
            face=PANEL,
            edge=col,
            color=col,
            lw=2.4,
            bold=True,
        )
        ax.text(x + 0.325, y + 0.115, f"✓ {fixes}", fontsize=13.5, color=GREEN, va="center")
        flaw_col = RED if i < 3 else SUB
        mark = "✗" if i < 3 else "→"
        ax.text(x + 0.325, y + 0.045, f"{mark} {flaw}", fontsize=13.5, color=flaw_col, va="center")
        if i:
            ax.annotate(
                "",
                xy=(x + 0.10, y - 0.008),
                xytext=(x - 0.045, y - 0.075),
                xycoords="axes fraction",
                arrowprops=dict(arrowstyle="-|>", color=FAINT, lw=2.0),
            )
    if "moral" in phases:
        fig.text(
            0.76,
            0.155,
            "every flaw on this ladder is a fact\n"
            "about your tools — retrieval, search,\n"
            "and prompting all inherit them",
            fontsize=14,
            color=YELLOW,
            ha="center",
        )
    footer(fig, "study guide: bag-of-words · tf-idf · word2vec · bert")
    return fig_to_pil(fig)


frames, durations = [], []
for k in range(1, 5):
    hold(frames, durations, lambda k=k: render_ladder(k, set()), ms=950)
hold(frames, durations, lambda: render_ladder(4, {"moral"}), ms=1700)
save_gif(frames, durations, "w02_s20_ladder.gif")


# ── Slide 21: bottleneck teaser ─────────────────────────────────────
SENT = [
    "The",
    "cat",
    "that",
    "my",
    "neighbour",
    "adopted",
    "last",
    "spring",
    "finally",
    "sat",
    "down",
]


def render_teaser(squeeze_t, phases):
    fig = new_fig()
    title_block(
        fig,
        "Next week: a bottleneck, and the fix",
        "early translation models squeezed a whole sentence through one fixed-size vector",
        kicker="WEEK 3 TEASER · SEQ2SEQ",
    )
    ax = blank_axes(fig, [0.04, 0.08, 0.92, 0.64])

    # funnel: converging lines in, diverging lines out
    fx = 0.475
    for x0, y0, x1, y1 in [
        (0.10, 0.86, fx - 0.01, 0.60),
        (0.10, 0.12, fx - 0.01, 0.38),
        (fx + 0.062, 0.60, 0.92, 0.86),
        (fx + 0.062, 0.38, 0.92, 0.12),
    ]:
        ax.plot([x0, x1], [y0, y1], color=SUB, lw=2.0, transform=ax.transAxes)
    chip(
        ax,
        fx - 0.002,
        0.415,
        0.054,
        0.145,
        "ctx",
        fontsize=12,
        mono=True,
        face=PANEL,
        edge=YELLOW,
        color=YELLOW,
        lw=2.2,
    )
    ax.text(
        fx + 0.026,
        0.30,
        "one fixed-size vector,\nno matter the sentence",
        ha="center",
        fontsize=11.5,
        color=SUB,
    )
    ax.text(0.80, 0.49, "…the translation\ncomes out here", ha="center", fontsize=11.5, color=FAINT)

    # words crowd toward the funnel mouth
    e = ease(squeeze_t)
    for i, w in enumerate(SENT):
        col0 = 0.045
        row = i % 4
        coln = i // 4
        x0 = col0 + coln * 0.105
        y0 = 0.78 - row * 0.17
        x = lerp(x0, 0.40, e)
        y = lerp(y0, 0.49, e)
        a = 1.0 - 0.92 * e  # crushed words all but vanish into the funnel
        ax.text(
            x,
            y,
            w,
            fontsize=12.5,
            color=TEXT,
            alpha=max(a, 0.08),
            fontfamily="monospace",
            ha="center",
        )
    if squeeze_t >= 1:
        ax.text(
            0.20, 0.49, "eleven words in,\nmost of them lost", ha="center", fontsize=13, color=RED
        )
        ax.text(
            0.72,
            0.76,
            "the longer the sentence,\nthe worse it gets",
            ha="center",
            fontsize=13,
            color=SUB,
        )
    if "fix" in phases:
        fig.text(
            0.5,
            0.135,
            "the 2017 fix: stop squeezing — let the model look back at "
            "every word and choose. it's called attention,",
            fontsize=15,
            color=YELLOW,
            ha="center",
        )
        fig.text(
            0.5,
            0.085,
            "and the paper that named this course says it is all you need.",
            fontsize=15,
            color=YELLOW,
            ha="center",
            style="italic",
        )
    footer(fig, "study guide: sequence-to-sequence · hidden-state · fixed-length-bottleneck")
    return fig_to_pil(fig)


frames, durations = [], []
hold(frames, durations, lambda: render_teaser(0, set()), ms=1500)
tween(frames, durations, lambda t: render_teaser(t, set()), n=20, ms=65)
hold(frames, durations, lambda: render_teaser(1, set()), ms=1300)
hold(frames, durations, lambda: render_teaser(1, {"fix"}), ms=1800)
save_gif(frames, durations, "w02_s21_teaser.gif")
