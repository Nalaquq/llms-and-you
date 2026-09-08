"""Week 3, the transformer: one attention head, taken apart on a real sentence.

  w03_s12_one_idea.gif    every word looks at every word, in one step
  w03_s14_question.gif    the query and the key: in plain language, then as arrows
  w03_s14b_three_views.gif one vector through three learned lenses -- q, k, v with numbers
  w03_s15_score.gif       the attention grid -- every question against every label
  w03_s16_share.gif       softmax on the grid: every row becomes shares of one
  w03_s17_blend.gif       the value is a nudge, added to the word it started as
  w03_s17b_meaning.gif    the moved vector has new neighbours; a second sentence moves it elsewhere

Built for a room with no mathematics and no programming. The mechanism is
carried by the sentence itself -- the same sentence the deck opened with --
and the formula sits in the bottom band for anyone who wants it.

s14-s17 take their pictures from 3Blue1Brown's "Attention in transformers,
step-by-step" -- the Chapter 6 video students are assigned (resource id
3blue1brown-attention; his source is github.com/3b1b/videos,
_2024/transformers/attention.py). Four of his moves are borrowed: a query and
a key as two arrows that either line up or do not; the all-pairs grid of dot
products, drawn as dots whose size is the score; softmax normalising that
grid in place; and the value as a nudge -- a vector ADDED to the embedding
the word arrived with, moving it through embedding space.

One deliberate departure. The video runs queries across the top and keys
down the side, so softmax goes down a column. Here every row is the asking
word and every column a word it looks at, so softmax goes along a row --
which is the orientation of every heatmap in Thursday's notebook and of the
mask slide (s22). Tuesday's picture and Thursday's plot should be the same
shape; a transposed grid is exactly the kind of thing this room would trip on.

Every number on s14b-s17 comes out of one TOY MODEL: a two-number embedding
per word and three 2x2 lenses (W_Q, W_K, W_V), all hand-chosen so that "it"
attends mostly to "animal". Queries, keys and values are computed from them;
every circle on the score grid is a real dot product of a query with a key;
softmax turns the rows into shares; the nudge is the share-weighted sum of
the values. The slides say it is a toy -- two numbers where the paper has 64
per head -- but the arithmetic on screen is the arithmetic, which is what
makes s15's "this circle is 0.55x1.08 + 1.89x3.30" possible. Real, messier
weights from a real model arrive on s19, and Thursday's lab is where students
meet them properly.
"""

import numpy as np
from matplotlib.patches import Circle, Rectangle
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
    grid_axes,
    grid_cell,
    grid_labels,
    grid_legend,
    grid_outline_row,
    hold,
    math_strip,
    new_fig,
    save_gif,
    tween,
)

SENT = ["The", "animal", "didn't", "cross", "the", "street", "because", "it", "was", "too", "tired"]
IT = 7  # index of "it"
ANIMAL = 1
N = len(SENT)

# The toy model. Two numbers per word (the paper has 512), placed so that
# creatures, places and states sit in different directions; and three 2x2
# lenses (the paper's are 512x64). Hand-chosen so the pictures agree with each
# other: q of "it" lines up with k of "animal", "street" second, "tired" third,
# and W_V spreads the values out so the nudge on s17 has somewhere to go.
EMB = np.array(
    [
        [0.35, 0.45],  # The
        [1.80, 1.20],  # animal
        [0.70, 0.60],  # didn't
        [1.00, -0.60],  # cross
        [0.35, 0.45],  # the
        [2.20, 0.30],  # street
        [0.80, 0.80],  # because
        [0.55, 0.30],  # it
        [0.60, 0.70],  # was
        [0.65, 0.75],  # too
        [0.30, 1.90],  # tired
    ]
)
W_Q = np.array([[1.44, -0.80], [2.56, 1.60]])
W_K = np.array([[1.20, -0.90], [0.90, 1.40]])
W_V = np.array([[1.00, 0.25], [-0.30, 1.60]])
Q = EMB @ W_Q.T  # one question per word
K = EMB @ W_K.T  # one label per word
V = EMB @ W_V.T  # one offer per word
E_IT, E_ANIMAL = EMB[IT], EMB[ANIMAL]


def softmax_rows(m):
    e = np.exp(m - m.max(axis=1, keepdims=True))
    return e / e.sum(axis=1, keepdims=True)


SCORES = Q @ K.T  # rows ask, columns answer: score(i, j) = q_i . k_j
PATTERN = softmax_rows(SCORES)  # every row sums to 1
WEIGHTS = PATTERN[IT]  # "it" attends: animal 61%, street 23%, tired 8%

KEYS = {
    1: "a creature",
    5: "a place",
    10: "a state",
    3: "an action",
}


def part_frame(fig, kicker, title, subtitle=None):
    fig.text(0.045, 0.945, kicker, fontsize=13, color=PURPLE, fontweight="bold", va="top")
    fig.text(0.045, 0.895, title, fontsize=30, color=TEXT, fontweight="bold", va="top")
    if subtitle:
        fig.text(0.045, 0.838, subtitle, fontsize=15.5, color=SUB, va="top")


def word_row(ax, y, colours=None, fontsize=15.5, weights=None, xs=None):
    """The running sentence, drawn once, with per-word colour."""
    if xs is None:
        xs = np.linspace(0.03, 0.97, len(SENT))
    for i, (x, w) in enumerate(zip(xs, SENT, strict=True)):
        col = (colours or {}).get(i, SUB)
        bold = (weights or {}).get(i, False)
        ax.text(
            x,
            y,
            w,
            ha="center",
            va="center",
            fontsize=fontsize,
            color=col,
            fontweight="bold" if bold else "normal",
        )
    return xs


def curve(ax, x0, x1, y, height, colour, lw, alpha):
    """An arc from one word to another, drawn as a parabola in axes space."""
    t = np.linspace(0, 1, 100)
    ax.plot(
        x0 + (x1 - x0) * t,
        y + height * np.sqrt(abs(x1 - x0)) * np.sin(np.pi * t),
        color=colour,
        lw=lw,
        alpha=alpha,
        solid_capstyle="round",
    )


GRID_RECT = [0.10, 0.215, 0.36, 0.515]
SCAP = 8.0  # scores above this get the biggest circle; "animal" asking about itself is 23
WMAX = PATTERN.max()


def score_norm(r, c):
    return float(np.clip(SCORES[r, c], 0.0, SCAP) / SCAP)


# =====================================================================
# SLIDE 12 — the one idea
# =====================================================================
def make_one_idea():
    def render(phase, t=1.0):
        fig = new_fig()
        part_frame(
            fig,
            "THE TRANSFORMER · THE IDEA",
            "Let every word look at every other word. In one step.",
            "Three ways to get information from one word to another.",
        )
        ax = blank_axes(fig, [0.045, 0.20, 0.91, 0.60])

        rows = [
            ("AN RNN", "passes it along, one word at a time", RED, 0.86),
            ("A CNN", "sees a window, three words wide", ORANGE, 0.55),
            ("ATTENTION", "every word, to every word, at once", GREEN, 0.235),
        ]
        for k, (name, how, colour, y) in enumerate(rows):
            live = phase >= k
            ax.text(
                0.0,
                y + 0.10,
                name,
                fontsize=12.5,
                color=colour if live else FAINT,
                fontweight="bold",
            )
            ax.text(0.135, y + 0.10, how, fontsize=12.5, color=SUB if live else FAINT)
            xs = word_row(
                ax,
                y,
                colours={i: (TEXT if live else FAINT) for i in range(len(SENT))},
                fontsize=13.5,
            )
            if not live:
                continue
            if k == 0:  # the chain
                n = int(len(SENT) * t) if phase == 0 else len(SENT)
                for i in range(1, n):
                    curve(ax, xs[i - 1], xs[i], y + 0.045, 0.06, colour, 1.8, 0.85)
            elif k == 1:  # the window
                pos = int((len(SENT) - 3) * t) if phase == 1 else IT - 1
                for i in range(pos, min(pos + 3, len(SENT))):
                    ax.add_patch(
                        Rectangle(
                            (xs[i] - 0.036, y - 0.05),
                            0.072,
                            0.10,
                            transform=ax.transAxes,
                            facecolor="none",
                            edgecolor=colour,
                            lw=1.8,
                        )
                    )
            else:  # all of it, at once
                for j in range(len(SENT)):
                    if j == IT:
                        continue
                    a = 0.85 * t if phase == 2 else 0.85
                    curve(ax, xs[IT], xs[j], y + 0.045, 0.05, colour, 1.6, a)
                ax.text(xs[IT], y - 0.075, "▲", fontsize=11, color=colour, ha="center")

        if phase >= 3:
            ax.text(
                0.0,
                0.035,
                "Nothing is passed along and nothing is skipped. Every pair of words is "
                "one step apart,\nno matter how far apart they sit in the sentence.",
                fontsize=14,
                color=YELLOW,
                va="center",
                linespacing=1.6,
            )

        math_strip(
            fig,
            r"$\mathrm{steps\ between\ any\ two\ words:}\quad "
            r"\mathrm{RNN}\; O(n) \qquad \mathrm{CNN}\; O(\log n) "
            r"\qquad \mathrm{attention}\; O(1)$",
            note="Table 1 of the paper",
        )
        footer(fig, "study guide: recurrent-neural-network · sliding-window")
        return fig_to_pil(fig)

    frames, durations = [], []
    hold(frames, durations, lambda: render(0, 0.0), ms=500)
    tween(frames, durations, lambda t: render(0, t), n=10, ms=90)
    hold(frames, durations, lambda: render(1, 0.0), ms=400)
    tween(frames, durations, lambda t: render(1, t), n=9, ms=110)
    tween(frames, durations, lambda t: render(2, ease(t)), n=10, ms=70)
    hold(frames, durations, lambda: render(3), ms=1400, n=2)
    save_gif(frames, durations, "w03_s12_one_idea.gif")


# =====================================================================
# SLIDE 14 — the question and the label
# =====================================================================
# The arrows on the lower left. Angles are chosen so the picture agrees with
# the grid two slides on: the label that lines up best with the question is
# "animal", then "street", then "tired", and "cross" points nearly away.
# The arrows on the lower left are the toy model's own vectors: the query of
# "it" and the keys of four words, drawn as directions (lengths scaled to fit).
def _angle(v):
    return float(np.degrees(np.arctan2(v[1], v[0])))


QUERY_ANGLE = _angle(Q[IT])
_KLEN = max(np.linalg.norm(K[j]) for j in (ANIMAL, 5, 10, 3))
KEY_ARROWS = [
    (j, _angle(K[j]), 0.95 * float(np.linalg.norm(K[j]) / _KLEN), GREEN if j == ANIMAL else BLUE)
    for j in (ANIMAL, 5, 10, 3)
]


def _polar(angle, length):
    a = np.deg2rad(angle)
    return length * np.cos(a), length * np.sin(a)


def make_question():
    def render(phase, t=1.0):
        fig = new_fig()
        part_frame(
            fig,
            "THE TRANSFORMER · QUERY AND KEY",
            "Every word asks a question. Every word wears a label.",
            "Attention is those two things being matched up. That is the whole mechanism.",
        )
        ax = blank_axes(fig, [0.045, 0.195, 0.91, 0.60])
        # Narrower than the default row: these words carry chips under them, and
        # the last one ran off the slide at full width.
        xs = word_row(
            ax,
            0.745,
            colours={i: (YELLOW if i == IT else TEXT) for i in range(len(SENT))},
            weights={IT: True},
            xs=np.linspace(0.075, 0.905, len(SENT)),
        )

        if phase >= 1:
            ax.text(
                0.0,
                0.985,
                "THE QUERY — what this word wants to know",
                fontsize=11,
                color=YELLOW,
                fontweight="bold",
                va="center",
            )
            chip(
                ax,
                min(xs[IT] - 0.155, 0.99 - 0.31),
                0.85,
                0.31,
                0.10,
                "which thing am I standing in for?",
                fontsize=13,
                face=PANEL,
                edge=YELLOW,
                color=YELLOW,
            )
            ax.plot([xs[IT], xs[IT]], [0.79, 0.845], color=YELLOW, lw=1.6)

        if phase >= 2:
            ax.text(
                0.0,
                0.655,
                "THE KEYS — what each word advertises about itself",
                fontsize=11,
                color=BLUE,
                fontweight="bold",
                va="center",
            )
            for j, label in KEYS.items():
                cx = min(max(xs[j] - 0.062, 0.0), 1.0 - 0.124)
                chip(
                    ax,
                    cx,
                    0.505,
                    0.124,
                    0.08,
                    label,
                    fontsize=11.5,
                    face=PANEL,
                    edge=BLUE,
                    color=BLUE,
                )
                ax.plot([xs[j], xs[j]], [0.59, 0.70], color=BLUE, lw=1.2, alpha=0.6)

        if phase >= 3:
            # 3b1b's picture: both the question and the label are vectors, and a
            # label answers a question when the two arrows line up.
            ax.text(
                0.0,
                0.415,
                "INSIDE THE MODEL — both are arrows",
                fontsize=11,
                color=FAINT,
                fontweight="bold",
                va="center",
            )
            pax = fig.add_axes([0.045, 0.20, 0.34, 0.225])
            pax.set_aspect("equal")
            pax.set_anchor("SW")
            pax.set_xlim(-1.35, 1.35)
            pax.set_ylim(-0.12, 1.12)
            pax.axis("off")
            pax.plot([-1.3, 1.3], [0, 0], color=PANEL_EDGE, lw=1.0)
            pax.plot([0, 0], [-0.1, 1.1], color=PANEL_EDGE, lw=1.0)
            qx, qy = _polar(QUERY_ANGLE, 1.0)
            arrow(pax, (0, 0), (qx, qy), color=YELLOW, lw=3.0, mutation=18)
            pax.text(
                qx - 0.06,
                qy + 0.02,
                "what 'it' is asking",
                fontsize=10.5,
                color=YELLOW,
                va="bottom",
                ha="right",
                linespacing=1.3,
            )
            for j, angle, length, colour in KEY_ARROWS:
                a = -8.0 + (angle + 8.0) * ease(t)  # keys swing in from flat
                kx, ky = _polar(a, length)
                arrow(pax, (0, 0), (kx, ky), color=colour, lw=2.2, alpha=0.9, mutation=15)
                if t >= 1.0:
                    dx = 0.05 if kx >= 0 else -0.05
                    pax.text(
                        kx + dx,
                        ky + 0.03,
                        SENT[j],
                        fontsize=10.5,
                        color=colour,
                        ha="left" if kx >= 0 else "right",
                        va="bottom",
                    )
            ax.text(
                0.42,
                0.37,
                "A label answers a question when the two arrows line up.\n"
                "'animal' lines up best with what 'it' is asking; 'cross' lines up worst.",
                fontsize=13,
                color=TEXT,
                va="top",
                linespacing=1.6,
            )
            ax.text(
                0.42,
                0.20,
                "Nobody wrote those questions or those labels. Each word's vector is "
                "multiplied by three\nlearned matrices to make three versions of itself — "
                "a question, a label, and something to give.",
                fontsize=12,
                color=SUB,
                va="top",
                linespacing=1.6,
            )

        if phase >= 4:
            ax.text(
                0.42,
                0.035,
                "Same word, three jobs. That is the only new machinery in the whole paper.",
                fontsize=13.5,
                color=YELLOW,
                va="center",
            )

        math_strip(
            fig,
            r"$q_i = W_Q x_i \qquad k_j = W_K x_j \qquad v_j = W_V x_j$",
            note="query, key, value — three learned views of one word",
        )
        footer(fig, "study guide: parameters-and-weights · vector · dot-product")
        return fig_to_pil(fig)

    frames, durations = [], []
    for p in range(3):
        hold(frames, durations, lambda p=p: render(p), ms=1200)
    hold(frames, durations, lambda: render(3, 0.0), ms=700)
    tween(frames, durations, lambda t: render(3, t), n=14, ms=70)
    hold(frames, durations, lambda: render(3, 1.0), ms=1400)
    hold(frames, durations, lambda: render(4), ms=1200, n=2)
    save_gif(frames, durations, "w03_s14_question.gif")


# =====================================================================
# SLIDE 15 — the score, as a grid
# =====================================================================
def make_score():
    # Two cells worked on screen: the best match and the worst.
    ex_hi, ex_lo = ANIMAL, 3

    def render(phase, t=1.0):
        fig = new_fig()
        part_frame(
            fig,
            "THE TRANSFORMER · THE SCORE",
            "Every circle is one dot product: a question times a label",
            "The numbers from the last slide, multiplied pair by pair and added. One "
            "circle for every pair of words.",
        )
        gax = grid_axes(fig, GRID_RECT, N)
        grid_labels(
            gax,
            N,
            SENT,
            row_colours={IT: YELLOW},
            col_colours={ex_hi: GREEN, ex_lo: BLUE} if phase <= 2 else {ANIMAL: GREEN},
        )
        grid_legend(
            gax, "rows ask · columns answer · a bigger circle is a bigger score · red: below zero"
        )

        # The "it" row builds left to right; the other ten rows arrive together.
        n_it = N if phase >= 2 else (int(N * t) if phase == 1 else 0)
        others = 1.0 if phase >= 4 else (t if phase == 3 else 0.0)
        for r in range(N):
            for c in range(N):
                neg = SCORES[r, c] < 0
                if r == IT:
                    if c < n_it:
                        grid_cell(gax, N, r, c, score_norm(r, c), 0, 0.0, dot_colour=TEXT)
                elif others > 0:
                    grid_cell(
                        gax,
                        N,
                        r,
                        c,
                        score_norm(r, c),
                        0,
                        0.0,
                        alpha=others,
                        dot_colour=RED if neg else SUB,
                    )
        grid_outline_row(gax, N, IT)
        if phase <= 2:
            for c, colour in ((ex_hi, GREEN), (ex_lo, BLUE)):
                gax.add_patch(
                    Rectangle(
                        (c + 0.02, N - 1 - IT + 0.02),
                        0.96,
                        0.96,
                        facecolor="none",
                        edgecolor=colour,
                        lw=2.0,
                    )
                )

        # The right-hand panel has square units, so the circles it draws are the
        # grid's circles at the grid's size.
        pax = fig.add_axes([0.55, 0.215, 0.40, 0.52])
        pax.set_aspect("equal")
        pax.set_anchor("SW")
        pax.set_xlim(0, 13.67)
        pax.set_ylim(0, 10)
        pax.axis("off")
        q = Q[IT]

        def worked(y, j, colour):
            k = K[j]
            score = SCORES[IT, j]
            for row, (qv, kv) in enumerate(zip(q, k, strict=True)):
                yy = y - row * 1.0
                pax.add_patch(
                    Rectangle((0.3, yy - 0.42), 1.3, 0.84, facecolor=PANEL, edgecolor=YELLOW)
                )
                pax.text(
                    0.95,
                    yy,
                    f"{qv:.2f}",
                    ha="center",
                    va="center",
                    fontsize=11.5,
                    color=YELLOW,
                    fontfamily="monospace",
                )
                pax.add_patch(
                    Rectangle((2.3, yy - 0.42), 1.3, 0.84, facecolor=PANEL, edgecolor=colour)
                )
                pax.text(
                    2.95,
                    yy,
                    f"{kv:.2f}",
                    ha="center",
                    va="center",
                    fontsize=11.5,
                    color=colour,
                    fontfamily="monospace",
                )
                pax.text(
                    4.1,
                    yy,
                    f"{qv:.2f} × {kv:.2f}  =  {qv * kv:.2f}",
                    va="center",
                    fontsize=11.5,
                    color=TEXT,
                    fontfamily="monospace",
                )
            pax.text(1.95, y - 0.5, "·", ha="center", va="center", fontsize=22, color=TEXT)
            pax.text(
                0.95, y - 1.75, "q of 'it'", ha="center", va="center", fontsize=9.5, color=YELLOW
            )
            pax.text(
                2.95,
                y - 1.75,
                f"k of '{SENT[j]}'",
                ha="center",
                va="center",
                fontsize=9.5,
                color=colour,
            )
            terms = " + ".join(f"{a:.2f}" for a in q * k)
            pax.text(
                4.1,
                y - 1.75,
                f"add them:  {terms}  =  {score:.2f}",
                va="center",
                fontsize=11.5,
                color=colour,
                fontfamily="monospace",
                fontweight="bold",
            )
            r = (0.07 + 0.38 * float(np.clip(score, 0, SCAP) / SCAP)) * 41 / 47
            pax.add_patch(Circle((12.6, y - 0.5), r, facecolor=colour, edgecolor="none"))

        pax.text(
            0,
            9.75,
            "EACH CIRCLE — the row's question · the column's label",
            fontsize=10.5,
            color=FAINT,
            fontweight="bold",
            va="center",
        )
        worked(8.8, ex_hi, GREEN)
        if phase >= 1:
            worked(5.6, ex_lo, BLUE)
        if phase >= 2:
            pax.text(
                0,
                2.75,
                "'animal' scores highest. Not because anyone said so —\nbecause its label "
                "and the question of 'it' point the same way,\nso the products are big and "
                "so is their sum.",
                fontsize=11.5,
                color=TEXT,
                va="top",
                linespacing=1.55,
            )
        if phase >= 3:
            pax.text(
                0,
                1.0,
                "Every other word does the same, at the same time:\n121 dot products in one "
                "step. That is 'every word looks at every word'.",
                fontsize=11.5,
                color=YELLOW,
                va="top",
                linespacing=1.55,
                alpha=others,
            )
        if phase >= 4:
            pax.text(
                0,
                -0.45,
                "a two-number toy — each head in the paper does this with 64; real weights "
                "arrive in four slides",
                fontsize=9.5,
                color=FAINT,
                va="top",
            )

        math_strip(
            fig,
            r"$\mathrm{score}(i, j) \;=\; q_i \cdot k_j \;=\; \sum_d q_{i,d}\, k_{j,d}$",
            note="the paper also divides by √d_k; the toy skips it",
        )
        footer(fig, "study guide: dot-product · cosine-similarity")
        return fig_to_pil(fig)

    frames, durations = [], []
    hold(frames, durations, lambda: render(0), ms=1800)
    hold(frames, durations, lambda: render(1, 0.0), ms=1400)
    tween(frames, durations, lambda t: render(1, t), n=11, ms=140)
    hold(frames, durations, lambda: render(2), ms=1600)
    tween(frames, durations, lambda t: render(3, ease(t)), n=10, ms=70)
    hold(frames, durations, lambda: render(3), ms=1100)
    hold(frames, durations, lambda: render(4), ms=1600, n=2)
    save_gif(frames, durations, "w03_s15_score.gif")


# =====================================================================
# SLIDE 16 — the share, as a grid
# =====================================================================
def make_share():
    top3 = np.argsort(WEIGHTS)[::-1][:3]

    def render(phase, t=1.0):
        fig = new_fig()
        part_frame(
            fig,
            "THE TRANSFORMER · THE SHARE",
            "Turn every row of scores into shares that add up to one",
            "Softmax. The same step that turned a model's guesses into probabilities in Week 2.",
        )
        gax = grid_axes(fig, GRID_RECT, N)
        grid_labels(gax, N, SENT, row_colours={IT: YELLOW}, col_colours={ANIMAL: GREEN})
        grid_legend(gax, "rows ask · columns answer · a brighter cell is a bigger share")

        t_it = 1.0 if phase >= 2 else (t if phase == 1 else 0.0)
        t_all = 1.0 if phase >= 3 else (t if phase == 2 else 0.0)
        for r in range(N):
            for c in range(N):
                if r == IT:
                    grid_cell(
                        gax,
                        N,
                        r,
                        c,
                        score_norm(r, c),
                        PATTERN[r, c],
                        t_it,
                        wmax=WMAX,
                        dot_colour=TEXT,
                        label=f"{PATTERN[r, c] * 100:.0f}",
                    )
                else:
                    grid_cell(gax, N, r, c, score_norm(r, c), PATTERN[r, c], t_all, wmax=WMAX)
            if t_all > 0 or (r == IT and t_it > 0):
                a = t_it if r == IT else t_all
                gax.text(
                    N + 0.35,
                    N - 0.5 - r,
                    "= 1",
                    fontsize=10,
                    color=GREEN if r == IT else FAINT,
                    va="center",
                    alpha=a,
                    fontfamily="monospace",
                    clip_on=False,
                )
        grid_outline_row(gax, N, IT)

        x = 0.55
        fig.text(
            x, 0.755, "a score", fontsize=12, color=SUB if t_it < 0.5 else FAINT, fontweight="bold"
        )
        fig.text(
            x + 0.10,
            0.755,
            "→   a share of attention",
            fontsize=12,
            color=FAINT if t_it < 0.5 else GREEN,
            fontweight="bold",
        )
        for k, j in enumerate(top3):
            if t_it < 0.5:
                label = f"{SENT[j]:<8}{SCORES[IT, j]:>5.1f}"
                colour = SUB
            else:
                label = f"{SENT[j]:<8}{PATTERN[IT, j]:>5.0%}"
                colour = GREEN if j == ANIMAL else SUB
            fig.text(
                x + 0.02,
                0.70 - k * 0.042,
                label,
                fontsize=13,
                color=colour,
                va="center",
                fontfamily="monospace",
            )
        if phase >= 2:
            fig.text(
                x,
                0.555,
                "Every share is positive, and the eleven in a row add\nto exactly 100%. "
                "Then the same, for every row at once.",
                fontsize=12.5,
                color=TEXT,
                va="top",
                linespacing=1.6,
            )
        if phase >= 3:
            fig.text(
                x,
                0.44,
                "So attention is a budget. A word cannot look hard at\none thing "
                "without looking less hard at everything else —\nwhich is why a head "
                "with nothing to say still has to\nput its weight somewhere.",
                fontsize=12.5,
                color=SUB,
                va="top",
                linespacing=1.6,
            )
            fig.text(
                x,
                0.235,
                "Nothing goes all the way to zero. Keep that in mind\nfor the mask.",
                fontsize=12,
                color=YELLOW,
                va="top",
                linespacing=1.6,
            )

        math_strip(
            fig,
            r"$\alpha_{ij} \;=\; \frac{e^{\,\mathrm{score}(i,j)}}"
            r"{\sum_{j'} e^{\,\mathrm{score}(i,j')}} "
            r"\qquad \sum_j \alpha_{ij} = 1$",
            note="softmax: bigger scores win, but nothing goes to zero",
        )
        footer(fig, "study guide: softmax · logits")
        return fig_to_pil(fig)

    frames, durations = [], []
    hold(frames, durations, lambda: render(0), ms=1000)
    tween(frames, durations, lambda t: render(1, ease(t)), n=12, ms=80)
    hold(frames, durations, lambda: render(1), ms=1300)
    tween(frames, durations, lambda t: render(2, ease(t)), n=12, ms=70)
    hold(frames, durations, lambda: render(2), ms=1100)
    hold(frames, durations, lambda: render(3), ms=1600, n=2)
    save_gif(frames, durations, "w03_s16_share.gif")


# =====================================================================
# SLIDE 17 — the blend, as a nudge
# =====================================================================
# Embedding-space arrows for the plane on the right. Two dimensions of the
# 512 -- a projection, like every embedding picture in Week 2. "it" arrives
# short and generic (a pronoun's vector says almost nothing); the words that
# win its attention each offer a value, and the weighted sum of those is the
# nudge that gets ADDED to it.
LENSES = [
    ("W_Q", W_Q, "q", "the question it asks", YELLOW),
    ("W_K", W_K, "k", "the label it wears", BLUE),
    ("W_V", W_V, "v", "what it offers, if a question picks it", GREEN),
]
# The three words "it" attends to most, their values, and the nudge: the
# share-weighted sum of EVERY word's value, not just these three.
RECIPE = [int(j) for j in np.argsort(WEIGHTS)[::-1][:3]]
VALUES = {j: (V[j], GREEN if j == ANIMAL else BLUE) for j in RECIPE}
NUDGE = WEIGHTS @ V


def make_blend():
    def render(phase, t=1.0):
        fig = new_fig()
        part_frame(
            fig,
            "THE TRANSFORMER · THE BLEND",
            "Add what the words offer, in those proportions, to 'it'",
            "What comes out is a new version of 'it' — one that only exists in this sentence.",
        )
        ax = blank_axes(fig, [0.045, 0.195, 0.44, 0.60])

        ax.text(
            0.0,
            0.965,
            "WHAT EACH WORD OFFERS — its value — weighted by 'it''s attention",
            fontsize=11,
            color=FAINT,
            fontweight="bold",
            va="center",
        )
        n_lines = min(phase, len(RECIPE))
        for k, j in enumerate(RECIPE[:n_lines]):
            y = 0.87 - k * 0.125
            colour = VALUES[j][1]
            ax.text(
                0.0,
                y,
                f"{WEIGHTS[j]:>3.0%}",
                fontsize=15,
                color=GREEN if j == ANIMAL else SUB,
                va="center",
                fontfamily="monospace",
            )
            ax.text(0.16, y, "×", fontsize=15, color=FAINT, va="center")
            chip(
                ax,
                0.22,
                y - 0.045,
                0.34,
                0.09,
                f"what '{SENT[j]}' offers   ({VALUES[j][0][0]:.1f}, {VALUES[j][0][1]:.1f})",
                fontsize=11.5,
                face=PANEL,
                edge=colour,
                color=colour,
            )
            if k:
                ax.text(0.60, y + 0.0625, "+", fontsize=15, color=FAINT, va="center")
        if n_lines >= len(RECIPE):
            ax.text(0.0, 0.50, "+   the rest", fontsize=12.5, color=FAINT, va="center")

        if phase >= 4:
            ax.plot([0.0, 0.62], [0.445, 0.445], color=PANEL_EDGE, lw=1.2)
            ax.text(
                0.0,
                0.385,
                "=  the nudge for 'it'",
                fontsize=14,
                color=YELLOW,
                va="center",
                fontweight="bold",
            )
            ax.text(
                0.0,
                0.30,
                "what 'it' becomes  =  what 'it' was  +  the nudge",
                fontsize=13,
                color=TEXT,
                va="center",
            )
            new = E_IT + NUDGE
            ax.text(
                0.0,
                0.245,
                f"({new[0]:.2f}, {new[1]:.2f})  =  ({E_IT[0]:.2f}, {E_IT[1]:.2f})  +  "
                f"({NUDGE[0]:.2f}, {NUDGE[1]:.2f})",
                fontsize=12,
                color=YELLOW,
                va="center",
                fontfamily="monospace",
            )
            ax.text(
                0.0,
                0.19,
                "Added, not written over. 'it' keeps what it arrived with and gains what "
                "the sentence says.",
                fontsize=11.5,
                color=SUB,
                va="center",
            )

        if phase >= 5:
            ax.text(
                0.0,
                0.11,
                "This is the thing word2vec could not do.",
                fontsize=14.5,
                color=YELLOW,
                va="center",
                fontweight="bold",
            )
            ax.text(
                0.0,
                0.035,
                "In Week 2 every word had one vector for life, so 'bank' was the same "
                "vector on a river and\nin a city. Here a word's vector is moved, by its "
                "sentence, every time it appears.",
                fontsize=11.5,
                color=SUB,
                va="center",
                linespacing=1.55,
            )

        # The plane: a corner of embedding space, and the arrow that moves.
        pax = fig.add_axes([0.52, 0.205, 0.435, 0.59])
        pax.set_aspect("equal")
        pax.set_anchor("SW")
        x_hi, y_hi, y_lo = 3.4, 3.4, -0.45
        pax.set_xlim(-0.3, x_hi)
        pax.set_ylim(y_lo, y_hi)
        pax.axis("off")
        for g in np.arange(0, x_hi, 0.5):
            pax.plot([g, g], [y_lo + 0.05, y_hi - 0.1], color=PANEL_EDGE, lw=0.6, alpha=0.6)
        for g in np.arange(0, y_hi - 0.1, 0.5):
            pax.plot([-0.25, x_hi - 0.05], [g, g], color=PANEL_EDGE, lw=0.6, alpha=0.6)
        pax.text(
            -0.25,
            y_hi - 0.08,
            "EMBEDDING SPACE — two of the 512 directions",
            fontsize=10,
            color=FAINT,
            fontweight="bold",
            va="bottom",
        )

        arrow(pax, (0, 0), tuple(E_IT), color=SUB, lw=2.4, mutation=16)
        pax.text(
            E_IT[0] + 0.06,
            E_IT[1] - 0.02,
            "'it', as it arrived",
            fontsize=10.5,
            color=SUB,
            va="top",
        )
        for j in RECIPE[:n_lines]:
            v, colour = VALUES[j]
            arrow(
                pax,
                (0, 0),
                tuple(v),
                color=colour,
                lw=2.0,
                alpha=0.9 if j == ANIMAL else 0.45,
                mutation=15,
            )
            pax.text(
                v[0] + 0.05,
                v[1] + 0.06,
                SENT[j],
                fontsize=11,
                color=colour,
                alpha=1.0 if j == ANIMAL else 0.7,
                va="bottom",
            )

        if phase >= 4:
            tt = ease(t) if phase == 4 else 1.0
            tip = E_IT + NUDGE * tt
            if tt > 0.02:
                pax.plot(
                    [E_IT[0], tip[0]],
                    [E_IT[1], tip[1]],
                    color=YELLOW,
                    lw=1.6,
                    ls=(0, (4, 3)),
                    alpha=0.8,
                )
                arrow(pax, (0, 0), tuple(tip), color=YELLOW, lw=3.2, mutation=19)
            if tt >= 1.0:
                pax.text(
                    (E_IT[0] + tip[0]) / 2 + 0.08,
                    (E_IT[1] + tip[1]) / 2 - 0.06,
                    "the nudge",
                    fontsize=10.5,
                    color=YELLOW,
                    va="top",
                )
                pax.text(
                    tip[0] + 0.08,
                    tip[1] - 0.02,
                    "'it', in this sentence",
                    fontsize=11.5,
                    color=YELLOW,
                    va="top",
                    fontweight="bold",
                )
        if phase >= 5:
            pax.text(
                -0.25,
                y_lo + 0.02,
                "'it' now points where 'animal' points — a vector built out of this sentence.",
                fontsize=11,
                color=TEXT,
                va="top",
            )

        math_strip(
            fig,
            [
                r"$x_i' \;=\; x_i \;+\; \sum_j \alpha_{ij}\, v_j$",
                r"$\mathrm{Attention}(Q, K, V) \;=\; \mathrm{softmax}"
                r"\!\left(\frac{Q K^{\top}}{\sqrt{d_k}}\right) V$",
            ],
            note="the answer to the slide that asked",
        )
        footer(fig, "study guide: static-vs-contextual-embeddings · polysemy · embedding")
        return fig_to_pil(fig)

    frames, durations = [], []
    for p in (0, 1, 2, 3):
        hold(frames, durations, lambda p=p: render(p), ms=850)
    hold(frames, durations, lambda: render(4, 0.0), ms=700)
    tween(frames, durations, lambda t: render(4, t), n=16, ms=70)
    hold(frames, durations, lambda: render(4, 1.0), ms=1200)
    hold(frames, durations, lambda: render(5), ms=1600, n=2)
    save_gif(frames, durations, "w03_s17_blend.gif")


# =====================================================================
# SLIDE 14b — three lenses on one vector
# =====================================================================
# Where q, k and v come from: one word's vector, multiplied by three learned
# matrices. Two dimensions instead of 512 so every number fits on the slide,
# and the arithmetic in the strip is the perceptron's -- each output number is
# a weighted sum of the input numbers.
def _vec(v):
    return f"({v[0]:.2f}, {v[1]:.2f})"


def _wsum(row, e):
    """'1.2(1.8) - 0.9(1.2)': one output number of a matrix product, written out."""
    a, b = row
    sign = "-" if b < 0 else "+"
    return f"{a:.2g}({e[0]:.2g}) {sign} {abs(b):.2g}({e[1]:.2g})"


def make_three_views():
    rows = [("animal", E_ANIMAL, 0.80), ("it", E_IT, 0.36)]

    def render(phase):
        fig = new_fig()
        part_frame(
            fig,
            "THE TRANSFORMER · QUERY, KEY, VALUE",
            "One vector in, three vectors out",
            "Every word is pushed through the same three learned lenses. That is where "
            "the question, the label and the offer come from.",
        )
        ax = blank_axes(fig, [0.045, 0.195, 0.91, 0.60])

        for r, (word, e, yc) in enumerate(rows):
            if r == 1 and phase < 4:
                break
            n_lens = 3 if r == 1 or phase >= 3 else phase
            chip(
                ax,
                0.0,
                yc - 0.05,
                0.10,
                0.10,
                word,
                fontsize=14,
                mono=True,
                edge=YELLOW if word == "it" else PANEL_EDGE,
                color=YELLOW if word == "it" else TEXT,
            )
            chip(
                ax,
                0.12,
                yc - 0.05,
                0.14,
                0.10,
                _vec(e),
                fontsize=12.5,
                mono=True,
                edge=PANEL_EDGE,
                color=TEXT,
            )
            ax.text(
                0.19,
                yc - 0.085,
                "its vector, from Week 2 + the position stamp",
                fontsize=8.5,
                color=FAINT,
                ha="center",
                va="center",
            )
            for k, (name, w, out, caption, colour) in enumerate(LENSES[:n_lens]):
                y = yc + (1 - k) * 0.13
                ax.plot(
                    [0.265, 0.31], [yc, y], color=colour, lw=1.6, alpha=0.8, transform=ax.transAxes
                )
                chip(
                    ax,
                    0.31,
                    y - 0.04,
                    0.10,
                    0.08,
                    name,
                    fontsize=12.5,
                    mono=True,
                    face=PANEL,
                    edge=colour,
                    color=colour,
                    bold=True,
                )
                arrow(ax, (0.415, y), (0.45, y), color=colour, lw=1.8, mutation=12)
                v = w @ e
                chip(
                    ax,
                    0.455,
                    y - 0.04,
                    0.20,
                    0.08,
                    f"{out} = {_vec(v)}",
                    fontsize=12,
                    mono=True,
                    face="#2b3446",
                    edge=colour,
                    color=colour,
                )
                ax.text(0.675, y, caption, fontsize=12, color=colour, va="center")

        if phase >= 4:
            ax.text(
                0.0,
                0.09,
                "Same three lenses for every word in the sentence, and for every sentence. "
                "Nobody designed them — they are learned,\nlike the perceptron's weights, "
                "from predicting text. They are the only thing attention has to learn.",
                fontsize=12,
                color=SUB,
                va="center",
                linespacing=1.6,
            )
        if phase >= 5:
            ax.text(
                0.0,
                0.0,
                "The question of 'it' and the label of 'animal' line up — that is the "
                "arrow picture from the last slide, now with numbers under it.",
                fontsize=12.5,
                color=YELLOW,
                va="center",
            )

        k_an = W_K @ E_ANIMAL
        math_strip(
            fig,
            [
                r"$q = W_Q\,x \qquad k = W_K\,x \qquad v = W_V\,x$",
                rf"$k_{{\mathrm{{animal}}}} = W_K\,x_{{\mathrm{{animal}}}}:\quad "
                rf"{_wsum(W_K[0], E_ANIMAL)} = {k_an[0]:.2f}, \quad "
                rf"{_wsum(W_K[1], E_ANIMAL)} = {k_an[1]:.2f}$",
            ],
            note="each W is 512×64 in the paper, 2×2 here · each output number is a "
            "weighted sum, a perceptron",
        )
        footer(fig, "study guide: parameters-and-weights · vector · neural-network-and-layers")
        return fig_to_pil(fig)

    frames, durations = [], []
    for p in range(6):
        hold(frames, durations, lambda p=p: render(p), ms=1100 if p < 4 else 1500)
    hold(frames, durations, lambda: render(5), ms=1500)
    save_gif(frames, durations, "w03_s14b_three_views.gif")


# =====================================================================
# SLIDE 17b — the moved vector has new neighbours
# =====================================================================
# Illustrative neighbourhoods on the same plane as s17. The second sentence
# swaps the last word so 'it' must mean the street, and the same arithmetic
# moves the vector somewhere else.
IT_TIRED = E_IT + NUDGE  # sentence 1, computed on s17
# Sentence 2 is illustrative: by a later layer "street" has absorbed "wide" and
# wears a label that wins, so its value dominates the nudge instead.
IT_WIDE = E_IT + 0.62 * V[5] + 0.20 * V[ANIMAL] + 0.06 * V[10]
CLUSTERS = [
    ("he", np.array([0.30, 0.62])),
    ("this", np.array([1.15, 0.05])),
    ("that", np.array([0.50, 0.90])),
    ("she", np.array([0.05, 0.80])),
    ("creature", IT_TIRED + np.array([-0.35, 0.55])),
    ("dog", IT_TIRED + np.array([0.45, 0.35])),
    ("beast", IT_TIRED + np.array([0.15, -0.35])),
    ("animal", IT_TIRED + np.array([-0.40, 0.05])),
    ("road", IT_WIDE + np.array([0.25, -0.20])),
    ("lane", IT_WIDE + np.array([-0.10, -0.50])),
    ("street", IT_WIDE + np.array([-0.45, -0.20])),
    ("crossing", IT_WIDE + np.array([0.45, 0.35])),
]
NEIGHBOURS = {
    "before": ("he · this · that", SUB),
    "tired": ("animal · creature · beast", YELLOW),
    "wide": ("street · road · lane", ORANGE),
}


def make_meaning():
    def render(phase, t=1.0):
        fig = new_fig()
        part_frame(
            fig,
            "THE TRANSFORMER · MEANING",
            "Same word, two sentences, two vectors",
            "Change the vector and you have changed the meaning. That is all 'contextual' means.",
        )
        pax = fig.add_axes([0.045, 0.205, 0.50, 0.59])
        pax.set_aspect("equal")
        pax.set_anchor("SW")
        pax.set_xlim(-0.2, 3.5)
        pax.set_ylim(-0.4, 2.5)
        pax.axis("off")
        for g in np.arange(0, 3.5, 0.5):
            pax.plot([g, g], [-0.35, 2.45], color=PANEL_EDGE, lw=0.6, alpha=0.6)
        for g in np.arange(0, 2.5, 0.5):
            pax.plot([-0.15, 3.45], [g, g], color=PANEL_EDGE, lw=0.6, alpha=0.6)
        for word, (x, y) in CLUSTERS:
            pax.plot(x, y, "o", color=FAINT, ms=5)
            pax.text(x + 0.05, y + 0.04, word, fontsize=10, color=SUB, va="bottom")

        arrow(pax, (0, 0), tuple(E_IT), color=SUB, lw=2.2, mutation=14)
        pax.text(E_IT[0] - 0.05, E_IT[1] + 0.04, "'it', Week 2", fontsize=10, color=SUB, ha="right")
        if phase >= 1:
            tt = ease(t) if phase == 1 else 1.0
            tip = E_IT + (IT_TIRED - E_IT) * tt
            arrow(pax, (0, 0), tuple(tip), color=YELLOW, lw=3.0, mutation=18)
            if tt >= 1.0:
                pax.text(
                    tip[0] + 0.08,
                    tip[1] + 0.02,
                    "'it' … too tired",
                    fontsize=11,
                    color=YELLOW,
                    ha="left",
                    va="bottom",
                    fontweight="bold",
                )
        if phase >= 2:
            tt = ease(t) if phase == 2 else 1.0
            tip = E_IT + (IT_WIDE - E_IT) * tt
            arrow(pax, (0, 0), tuple(tip), color=ORANGE, lw=3.0, mutation=18)
            if tt >= 1.0:
                pax.text(
                    tip[0] + 0.08,
                    tip[1] + 0.02,
                    "'it' … too wide",
                    fontsize=11,
                    color=ORANGE,
                    ha="left",
                    va="bottom",
                    fontweight="bold",
                )

        x = 0.59
        prefix = "The animal didn't cross the street because it was too "
        pt = 10.5
        # +1: matplotlib trims the trailing space when it measures the prefix.
        join = (len(prefix) + 1) * pt / 72 * 100 * 0.6021 / 1600
        fig.text(
            x,
            0.77,
            "NEAREST WORDS TO 'it' — illustrative",
            fontsize=11,
            color=FAINT,
            fontweight="bold",
            va="center",
        )
        fig.text(x, 0.725, "on its own, as in Week 2", fontsize=11.5, color=SUB, va="center")
        fig.text(
            x + 0.02,
            0.685,
            NEIGHBOURS["before"][0],
            fontsize=13,
            color=SUB,
            va="center",
            fontfamily="monospace",
        )
        if phase >= 1:
            fig.text(x, 0.615, prefix, fontsize=pt, color=TEXT, va="center", fontfamily="monospace")
            fig.text(
                x + join,
                0.615,
                "tired.",
                fontsize=pt,
                color=YELLOW,
                va="center",
                fontweight="bold",
                fontfamily="monospace",
            )
            fig.text(
                x + 0.02,
                0.573,
                NEIGHBOURS["tired"][0],
                fontsize=13,
                color=YELLOW,
                va="center",
                fontfamily="monospace",
            )
        if phase >= 2:
            fig.text(x, 0.50, prefix, fontsize=pt, color=TEXT, va="center", fontfamily="monospace")
            fig.text(
                x + join,
                0.50,
                "wide.",
                fontsize=pt,
                color=ORANGE,
                va="center",
                fontweight="bold",
                fontfamily="monospace",
            )
            fig.text(
                x + 0.02,
                0.458,
                NEIGHBOURS["wide"][0],
                fontsize=13,
                color=ORANGE,
                va="center",
                fontfamily="monospace",
            )
        if phase >= 3:
            fig.text(
                x,
                0.395,
                "One word changed at the end of the sentence. A layer\nlater, 'street' has "
                "absorbed 'wide' and wears a different\nlabel; 'it' asks the same question, "
                "'street' wins it, a\ndifferent value is added, and the vector lands elsewhere.",
                fontsize=12,
                color=TEXT,
                va="top",
                linespacing=1.6,
            )
            fig.text(
                x,
                0.26,
                "Nothing about 'it' was looked up. Its meaning IS\nwhere its vector "
                "ended up — and the words around it\ndecided that.",
                fontsize=12.5,
                color=YELLOW,
                va="top",
                linespacing=1.6,
            )

        math_strip(
            fig,
            r"$x_{it}' \;=\; x_{it} \;+\; \sum_j \alpha_{ij}\, v_j$",
            note="same arithmetic, two sentences, two answers",
        )
        footer(fig, "study guide: static-vs-contextual-embeddings · polysemy · nearest-neighbours")
        return fig_to_pil(fig)

    frames, durations = [], []
    hold(frames, durations, lambda: render(0), ms=1300)
    tween(frames, durations, lambda t: render(1, t), n=14, ms=70)
    hold(frames, durations, lambda: render(1), ms=1300)
    tween(frames, durations, lambda t: render(2, t), n=14, ms=70)
    hold(frames, durations, lambda: render(2), ms=1200)
    hold(frames, durations, lambda: render(3), ms=1600, n=2)
    save_gif(frames, durations, "w03_s17b_meaning.gif")


if __name__ == "__main__":
    make_one_idea()
    make_question()
    make_three_views()
    make_score()
    make_share()
    make_blend()
    make_meaning()
