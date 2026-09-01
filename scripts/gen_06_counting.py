"""Slides 10-13: the counting era — bag of words, TF-IDF, and the ceiling.

w02_s10_bag_of_words.gif  Words fall into a bag; order dies; the bite demo
w02_s11_tfidf.gif         TF bars, then IDF dims the everywhere-words
w02_s12_preprocessing.png Stemming / lemmatization / stop words / n-grams
w02_s13_ceiling.gif       Counting has no meaning: the blob
"""

import matplotlib.pyplot as plt
import numpy as np
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
    plane,
    save_gif,
    save_png,
    title_block,
    tween,
)

rng = np.random.default_rng(3)

# ── Slide 10: bag of words ──────────────────────────────────────────
S1 = ["the", "dog", "bit", "the", "man"]
S2 = ["the", "man", "bit", "the", "dog"]
COUNTS = [("the", 2), ("dog", 1), ("bit", 1), ("man", 1)]


def render_bag(drop_t, phases):
    fig = new_fig()
    title_block(
        fig,
        "The counting era: bag of words",
        "count what occurs, throw away the order — that trade is the whole method",
        kicker="BAG OF WORDS · COUNT VECTORIZATION",
    )
    ax = blank_axes(fig, [0.03, 0.06, 0.94, 0.70])

    ax.text(
        0.24,
        0.96,
        '"the dog bit the man"',
        ha="center",
        fontsize=18,
        color=TEXT,
        fontfamily="monospace",
    )
    # bag silhouette
    bx, by = 0.24, 0.30
    bag = plt.Polygon(
        [
            [bx - 0.10, by + 0.18],
            [bx + 0.10, by + 0.18],
            [bx + 0.13, by - 0.16],
            [bx - 0.13, by - 0.16],
        ],
        closed=True,
        facecolor=PANEL,
        edgecolor=PURPLE,
        lw=2.5,
        transform=ax.transAxes,
    )
    ax.add_patch(bag)
    ax.text(bx, by - 0.235, "order is not stored in here", ha="center", fontsize=12.5, color=SUB)

    # words tumble in
    for i, w in enumerate(S1):
        t_i = np.clip(drop_t * len(S1) - i, 0, 1)
        if t_i <= 0:
            ax.text(
                0.10 + i * 0.07,
                0.87,
                w,
                ha="center",
                fontsize=15,
                color=TEXT,
                fontfamily="monospace",
            )
            continue
        x0, y0 = 0.10 + i * 0.07, 0.87
        jx = bx + [-0.05, 0.03, -0.01, 0.06, -0.06][i]
        jy = by + [0.05, -0.05, 0.08, 0.00, -0.08][i]
        x, y = lerp(x0, jx, t_i), lerp(y0, jy, t_i)
        rot = int(t_i * [20, -30, 12, -15, 25][i])
        ax.text(x, y, w, ha="center", fontsize=15, color=TEXT, fontfamily="monospace", rotation=rot)

    if "counts" in phases:
        ax.text(0.56, 0.86, "count", ha="left", fontsize=13, color=SUB)
        for i, (w, c) in enumerate(COUNTS):
            y = 0.76 - i * 0.115
            ax.text(0.56, y, w, fontsize=15.5, color=TEXT, fontfamily="monospace")
            chip(
                ax,
                0.65,
                y - 0.03,
                0.055,
                0.085,
                str(c),
                fontsize=14,
                mono=True,
                face=PANEL,
                edge=BLUE,
                color=BLUE,
            )
            ax.annotate(
                "",
                xy=(0.54, y + 0.02),
                xytext=(bx + 0.14, by),
                xycoords="axes fraction",
                arrowprops=dict(arrowstyle="-", color=FAINT, lw=0.8, alpha=0.4),
            )
        ax.text(
            0.62,
            0.28,
            "= the document's vector\n(one slot per vocabulary word,\nalmost all zeros)",
            fontsize=13.5,
            color=SUB,
            ha="center",
        )
    if "bite" in phases:
        chip(
            ax,
            0.76,
            0.42,
            0.215,
            0.34,
            '"the dog bit the man"\n"the man bit the dog"\n\n'
            "same bag. identical vector.\nno setting fixes this —\n"
            "order was thrown away\non purpose",
            fontsize=13.5,
            face=PANEL,
            edge=RED,
            color=TEXT,
            lw=2.0,
        )
    footer(fig, "study guide: bag-of-words · count-vectorization")
    return fig_to_pil(fig)


frames, durations = [], []
hold(frames, durations, lambda: render_bag(0, set()), ms=1200)
tween(frames, durations, lambda t: render_bag(t, set()), n=20, ms=60)
hold(frames, durations, lambda: render_bag(1, {"counts"}), ms=1500)
hold(frames, durations, lambda: render_bag(1, {"counts", "bite"}), ms=1500)
save_gif(frames, durations, "w02_s10_bag_of_words.gif")


# ── Slide 11: TF-IDF ────────────────────────────────────────────────
TERMS = [
    ("the", 0.95, 1.00),
    ("cat", 0.30, 0.08),
    ("harbour", 0.22, 0.02),
    ("is", 0.80, 0.98),
    ("tide", 0.25, 0.03),
    ("of", 0.85, 0.99),
]
# (term, tf, doc-frequency-share). idf ~ log(1/df)


def render_tfidf(idf_t, phases):
    fig = new_fig()
    title_block(
        fig,
        "TF-IDF: frequent here, rare everywhere",
        "term frequency × inverse document frequency — importance "
        "without a hand-made stop-word list",
        kicker="TF · IDF · TF-IDF",
    )
    ax = blank_axes(fig, [0.06, 0.10, 0.88, 0.62])

    x0, bw = 0.10, 0.105
    base = 0.30
    ax.text(x0, 0.99, "raw term frequency  →  after the IDF penalty", fontsize=14.5, color=SUB)
    for i, (w, tf, df) in enumerate(TERMS):
        idf = np.log(1 / max(df, 0.01)) / np.log(100)  # 0..1 scale
        post = min(tf * idf * 2.4, 1.0)  # rescaled so real words stay tall
        h_now = tf * (1 - idf_t) + post * idf_t
        x = x0 + i * (bw + 0.038)
        everywhere = df > 0.5
        col = FAINT if (everywhere and idf_t > 0.5) else (YELLOW if not everywhere else BLUE)
        ax.add_patch(
            plt.Rectangle(
                (x, base),
                bw,
                0.60 * max(h_now, 0.012),
                facecolor=col,
                edgecolor="none",
                alpha=0.9,
                transform=ax.transAxes,
            )
        )
        ax.text(
            x + bw / 2,
            base - 0.075,
            w,
            ha="center",
            fontsize=14.5,
            color=TEXT,
            fontfamily="monospace",
        )
        if idf_t > 0.5 and everywhere:
            ax.text(
                x + bw / 2,
                base + 0.60 * h_now + 0.035,
                "appears in\nevery doc → ≈ 0",
                ha="center",
                fontsize=10.5,
                color=FAINT,
            )

    if "formula" in phases:
        fig.text(
            0.5,
            0.165,
            r"tf-idf $= \frac{\mathrm{count\ in\ this\ doc}}{\mathrm{words\ in\ this\ doc}}"
            r"\times \log\frac{\mathrm{total\ docs}}{\mathrm{docs\ containing\ it}}$",
            fontsize=17,
            color=TEXT,
            ha="center",
        )
        fig.text(
            0.5,
            0.085,
            '"the" appears in every document → its score is exactly zero. '
            "no stop-word list needed — arithmetic deleted it.",
            fontsize=14,
            color=GREEN,
            ha="center",
        )
    footer(fig, "study guide: term-frequency · inverse-document-frequency · tf-idf · stop-words")
    return fig_to_pil(fig)


frames, durations = [], []
hold(frames, durations, lambda: render_tfidf(0, set()), ms=1500)
tween(frames, durations, lambda t: render_tfidf(t, set()), n=20, ms=60)
hold(frames, durations, lambda: render_tfidf(1, set()), ms=900)
hold(frames, durations, lambda: render_tfidf(1, {"formula"}), ms=1600)
save_gif(frames, durations, "w02_s11_tfidf.gif")


# ── Slide 12: preprocessing zoo (static) ────────────────────────────
fig = new_fig()
title_block(
    fig,
    "Four knobs on the counting pipeline",
    "each one trades information for a smaller, cleaner vocabulary — and each can backfire",
    kicker="PREPROCESSING",
)
panels = [
    (
        "stemming",
        BLUE,
        "chop endings by rule\n\nrunning → run\nstudies → studi\n\n"
        "fast, no dictionary,\nresult may not be a word",
    ),
    (
        "lemmatization",
        GREEN,
        "look up the dictionary form\n\nran → run\nbetter → good\n\n"
        "accurate, slower, needs to\nknow noun vs verb",
    ),
    (
        "stop words",
        ORANGE,
        'delete "the, a, is, of"\n\nbut careful:\n"not effective" → "effective"\n\n'
        "negation lives in\nstop words",
    ),
    (
        "n-grams",
        PURPLE,
        'count word pairs too\n\n"not good" becomes a unit\n\n'
        "vocabulary explodes as\nn grows — trigrams, then stop",
    ),
]
axp = blank_axes(fig, [0.03, 0.07, 0.94, 0.70])
for i, (name, col, body) in enumerate(panels):
    x = 0.012 + i * 0.25
    chip(axp, x, 0.16, 0.222, 0.62, "", face=PANEL, edge=col, lw=2.0)
    axp.text(x + 0.111, 0.71, name, ha="center", fontsize=17, color=col, fontweight="bold")
    axp.text(x + 0.111, 0.43, body, ha="center", fontsize=12.3, color=TEXT, va="center")
footer(fig, "study guide: stemming · lemmatization · stop-words · n-grams")
save_png(fig, "w02_s12_preprocessing.png")
plt.close(fig)


# ── Slide 13: the ceiling — counting has no geometry of meaning ─────
BLOB_WORDS = [
    "the",
    "cat",
    "dog",
    "is",
    "tide",
    "harbour",
    "run",
    "of",
    "seven",
    "king",
    "tea",
    "walk",
    "and",
    "boat",
    "queen",
]
BLOB = {w: (rng.normal(0, 0.55), rng.normal(0, 0.45)) for w in BLOB_WORDS}
SEM = {
    "cat": (-2.6, 1.5),
    "dog": (-2.2, 1.9),
    "king": (2.4, 1.6),
    "queen": (2.8, 1.9),
    "tea": (0.2, -1.8),
    "the": (-3.0, -1.9),
    "is": (-2.5, -2.2),
    "of": (-2.0, -2.5),
}


def render_ceiling(spread_t, phases):
    fig = new_fig()
    title_block(
        fig,
        "The ceiling: counting is not meaning",
        "plot a TF-IDF space and almost every word collapses into one "
        "blob — synonyms that never co-occur look unrelated",
        kicker="WHY COUNTING WASN'T ENOUGH",
    )
    ax = plane(fig, [0.055, 0.08, 0.55, 0.68], xlim=(-4, 4), ylim=(-3, 3), grid=False)
    e = ease(spread_t)
    labelled_in_blob = {"cat", "king", "the", "tea", "dog", "of"}
    for w, (bx, by) in BLOB.items():
        tx, ty = SEM.get(w, (bx * 2.2, by * 2.2))
        x, y = bx + (tx - bx) * e, by + (ty - by) * e
        in_sem = w in SEM
        col = BLUE if spread_t < 0.5 else (YELLOW if in_sem else FAINT)
        ax.plot(x, y, "o", ms=6, color=col, alpha=0.85 if (in_sem or spread_t < 0.5) else 0.35)
        show = (w in labelled_in_blob) if spread_t < 0.5 else in_sem
        if show:
            ax.text(x + 0.09, y + 0.05, w, fontsize=11.5, color=SUB)

    tx0 = 0.655
    if spread_t < 0.5:
        fig.text(
            tx0,
            0.60,
            "a real TF-IDF space (via PCA):\none blob. distance ≈ nothing.",
            fontsize=15,
            color=TEXT,
        )
    else:
        fig.text(
            tx0,
            0.60,
            "what we actually want:\nneighbourhoods that mean something",
            fontsize=15,
            color=TEXT,
        )
    if "verdict" in phases:
        chip(
            blank_axes(fig, [0, 0, 1, 1]),
            tx0 - 0.005,
            0.17,
            0.30,
            0.28,
            "TF-IDF only knows which documents\na word appeared in.\n\n"
            "it cannot learn that cat ≈ kitten\nfrom counts alone.\n\n"
            "a different question was needed —\nask about the neighbours",
            fontsize=13.5,
            face=PANEL,
            edge=ORANGE,
            color=TEXT,
            lw=2.0,
        )
    footer(fig, "study guide: tf-idf · sparse-and-dense-vectors · dimensionality-reduction")
    return fig_to_pil(fig)


frames, durations = [], []
hold(frames, durations, lambda: render_ceiling(0, set()), ms=1700)
tween(frames, durations, lambda t: render_ceiling(t, set()), n=20, ms=60)
hold(frames, durations, lambda: render_ceiling(1, set()), ms=1100)
hold(frames, durations, lambda: render_ceiling(1, {"verdict"}), ms=1600)
save_gif(frames, durations, "w02_s13_ceiling.gif")
