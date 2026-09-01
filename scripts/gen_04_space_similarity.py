"""Slides 06-08: embedding space, cosine similarity, vector arithmetic.

w02_s06_space.gif      Scattered words drift into semantic clusters
w02_s07_cosine.gif     Two arrows; the angle IS the similarity
w02_s08_king_queen.gif king - man + woman walks to queen; then a failure
"""

import numpy as np
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
    arrow,
    blank_axes,
    chip,
    ease,
    fig_to_pil,
    footer,
    hold,
    new_fig,
    plane,
    save_gif,
    title_block,
    tween,
)

rng = np.random.default_rng(11)

# ── Slide 6: the space organises itself ─────────────────────────────
GROUPS = {
    BLUE: [("cat", 1.6, 4.9), ("kitten", 2.3, 5.4), ("dog", 1.2, 5.6), ("puppy", 2.0, 6.1)],
    GREEN: [("coffee", 6.8, 5.3), ("tea", 7.5, 5.8), ("cup", 6.3, 6.0)],
    PURPLE: [("king", 6.7, 1.3), ("queen", 7.4, 1.8), ("crown", 6.2, 2.1)],
    ORANGE: [("Monday", 1.5, 1.4), ("Tuesday", 2.2, 1.1), ("Friday", 1.1, 2.0)],
}
START = {
    w: (rng.uniform(0.5, 8.0), rng.uniform(0.5, 6.4))
    for _, ws in GROUPS.items()
    for (w, _, _) in ws
}


def render_space(t, phases):
    fig = new_fig()
    title_block(
        fig,
        "Meaning becomes geometry",
        "train well, and 'similar meaning' turns into 'close together' — distance you can measure",
        kicker="EMBEDDING SPACE",
    )
    ax = plane(fig, [0.07, 0.09, 0.60, 0.68], xlim=(0, 9), ylim=(0, 7))
    e = ease(t)
    for col, ws in GROUPS.items():
        for w, gx, gy in ws:
            sx, sy = START[w]
            x, y = sx + (gx - sx) * e, sy + (gy - sy) * e
            ax.plot(x, y, "o", ms=9, color=col, alpha=0.95)
            ax.text(x + 0.13, y + 0.10, w, fontsize=13, color=TEXT)

    tx = 0.70
    fig.text(tx, 0.66, "each word = one point", fontsize=15.5, color=TEXT)
    if t >= 1:
        fig.text(tx, 0.575, "nearest neighbours of cat:", fontsize=15.5, color=BLUE)
        for i, (w, s) in enumerate(
            [("kitten", 0.94), ("dog", 0.91), ("puppy", 0.88), ("coffee", 0.12)]
        ):
            c = TEXT if s > 0.5 else FAINT
            fig.text(
                tx + 0.02,
                0.515 - i * 0.052,
                f"{w:<8} {s:.2f}",
                fontsize=14,
                color=c,
                fontfamily="monospace",
            )
    if "caveat" in phases:
        chip(
            blank_axes(fig, [0, 0, 1, 1]),
            0.675,
            0.13,
            0.28,
            0.145,
            'careful: "close" means keeps the\nsame company — good and bad\nare neighbours too',
            fontsize=13.5,
            face=PANEL,
            edge=ORANGE,
            color=TEXT,
            lw=2.0,
        )
    footer(fig, "study guide: embedding-space · nearest-neighbours")
    return fig_to_pil(fig)


frames, durations = [], []
hold(frames, durations, lambda: render_space(0, set()), ms=1200)
tween(frames, durations, lambda t: render_space(t, set()), n=24, ms=55)
hold(frames, durations, lambda: render_space(1, set()), ms=1400)
hold(frames, durations, lambda: render_space(1, {"caveat"}), ms=1300)
save_gif(frames, durations, "w02_s06_space.gif")


# ── Slide 7: cosine similarity ──────────────────────────────────────
def render_cosine(ang_deg, show_len=False):
    fig = new_fig()
    title_block(
        fig,
        "How close is close? Measure the angle",
        "cosine similarity compares direction and ignores length — "
        "+1 same way, 0 unrelated, −1 opposite",
        kicker="DOT PRODUCT · COSINE",
    )
    ax = plane(fig, [0.06, 0.08, 0.52, 0.70], xlim=(-4.6, 4.6), ylim=(-0.8, 4.4))
    ax.axhline(0, color=FAINT, lw=1.0)
    ax.axvline(0, color=FAINT, lw=1.0)

    a = np.deg2rad(28)
    b = np.deg2rad(28 + ang_deg)
    r1, r2 = 3.6, (2.4 if show_len else 3.6)
    v1 = (r1 * np.cos(a), r1 * np.sin(a))
    v2 = (r2 * np.cos(b), r2 * np.sin(b))
    arrow(ax, (0, 0), v1, color=BLUE, lw=4)
    arrow(ax, (0, 0), v2, color=YELLOW, lw=4)
    ax.text(*(1.06 * np.array(v1)), r"$\vec{cat}$", fontsize=17, color=BLUE)
    ax.text(*(1.10 * np.array(v2)), r"$\vec{dog}$", fontsize=17, color=YELLOW)
    th = np.linspace(a, b, 40)
    ax.plot(1.1 * np.cos(th), 1.1 * np.sin(th), color=SUB, lw=1.6)
    ax.text(
        1.55 * np.cos((a + b) / 2), 1.55 * np.sin((a + b) / 2), r"$\theta$", fontsize=16, color=SUB
    )

    cos = np.cos(b - a)
    fig.text(0.665, 0.60, "cosine similarity", fontsize=16, color=SUB)
    fig.text(
        0.665,
        0.50,
        f"cos θ = {cos:+.2f}",
        fontsize=30,
        color=YELLOW,
        fontfamily="monospace",
        fontweight="bold",
    )
    # live meter
    mx0, mw = 0.665, 0.27
    axm = blank_axes(fig, [0, 0, 1, 1])
    axm.plot([mx0, mx0 + mw], [0.42, 0.42], color=PANEL_EDGE, lw=7, solid_capstyle="round")
    axm.plot(mx0 + mw * (cos + 1) / 2, 0.42, "o", ms=13, color=YELLOW)
    fig.text(mx0, 0.375, "−1", fontsize=12, color=SUB, ha="center")
    fig.text(mx0 + mw / 2, 0.375, "0", fontsize=12, color=SUB, ha="center")
    fig.text(mx0 + mw, 0.375, "+1", fontsize=12, color=SUB, ha="center")
    if show_len:
        fig.text(
            0.665,
            0.27,
            "shrinking a vector changes nothing:\ndirection is what carries meaning",
            fontsize=14.5,
            color=GREEN,
        )
    fig.text(
        0.665,
        0.155,
        r"built from the dot product:  cos θ = $\frac{\vec{a}\,\cdot\,\vec{b}}"
        r"{|\vec{a}|\,|\vec{b}|}$",
        fontsize=15,
        color=SUB,
    )
    footer(fig, "study guide: dot-product · cosine-similarity")
    return fig_to_pil(fig)


frames, durations = [], []
hold(frames, durations, lambda: render_cosine(12), ms=1200)
tween(frames, durations, lambda t: render_cosine(12 + t * 120), n=26, ms=60)
hold(frames, durations, lambda: render_cosine(132), ms=1000)
tween(frames, durations, lambda t: render_cosine(132 - t * 120), n=26, ms=60)
hold(frames, durations, lambda: render_cosine(12, show_len=True), ms=1500)
save_gif(frames, durations, "w02_s07_cosine.gif")


# ── Slide 8: king − man + woman ─────────────────────────────────────
P = {
    "king": (5.6, 1.6),
    "man": (4.4, 1.1),
    "woman": (4.15, 3.4),
    "queen": (5.45, 3.95),
    "actual": (5.30, 3.80),
}


def render_kq(walk_t, phases):
    fig = new_fig()
    title_block(
        fig,
        "You can do algebra on meaning",
        "the gap between king and man is a direction — add it to woman and see where you land",
        kicker="VECTOR ARITHMETIC",
    )
    ax = plane(fig, [0.06, 0.08, 0.58, 0.70], xlim=(3.4, 6.6), ylim=(0.4, 4.8))
    for w, (x, y) in P.items():
        if w == "actual":
            continue
        col = {"king": PURPLE, "man": BLUE, "woman": BLUE, "queen": PURPLE}[w]
        ax.plot(x, y, "o", ms=9, color=col)
        dy = -0.28 if w in ("king", "man") else 0.16
        ax.text(x + 0.06, y + dy, w, fontsize=15, color=col)

    k, m, wm = (np.array(P[w]) for w in ("king", "man", "woman"))
    d = m - k  # subtract this
    if walk_t > 0:
        e = ease(min(walk_t * 2, 1))
        arrow(ax, tuple(k), tuple(k + d * e), color=RED, lw=3.5)
        ax.text(*(k + d * 0.5 + [0.14, -0.10]), "− man", fontsize=13, color=RED)
    if walk_t > 0.5:
        e = ease((walk_t - 0.5) * 2)
        start = wm
        tip = start - d * e
        arrow(ax, tuple(start), tuple(tip), color=GREEN, lw=3.5)
        ax.text(*(start - d * 0.5 + [-0.62, -0.30]), "+ (king − man)", fontsize=13, color=GREEN)
    if "land" in phases:
        ax.plot(*P["actual"], "*", ms=22, color=YELLOW)
        ax.plot(*P["queen"], "o", ms=26, mfc="none", mec=YELLOW, mew=2)
        ax.text(4.62, 4.35, "lands here — nearest word: queen", fontsize=13.5, color=YELLOW)

    tx = 0.68
    fig.text(
        tx,
        0.66,
        r"$\vec{king} - \vec{man} + \vec{woman} \approx \vec{queen}$",
        fontsize=17,
        color=TEXT,
    )
    if "land" in phases:
        fig.text(
            tx,
            0.56,
            "nobody programmed a royalty direction.\nit fell out of the training data.",
            fontsize=14.5,
            color=SUB,
        )
    if "fail" in phases:
        chip(
            blank_axes(fig, [0, 0, 1, 1]),
            tx - 0.005,
            0.13,
            0.30,
            0.30,
            "but try it yourself and watch it miss:\n\n"
            "  doctor − man + woman → nurse\n"
            "  cup − coffee + tea   → ??\n\n"
            "hits and misses have the same cause:\n"
            "corpus statistics, not understanding",
            fontsize=13.5,
            face=PANEL,
            edge=RED,
            color=TEXT,
            lw=2.0,
        )
    footer(fig, "study guide: vector-arithmetic-and-its-limits")
    return fig_to_pil(fig)


frames, durations = [], []
hold(frames, durations, lambda: render_kq(0, set()), ms=1300)
tween(frames, durations, lambda t: render_kq(t, set()), n=26, ms=60)
hold(frames, durations, lambda: render_kq(1, {"land"}), ms=1600)
hold(frames, durations, lambda: render_kq(1, {"land", "fail"}), ms=1500)
save_gif(frames, durations, "w02_s08_king_queen.gif")
