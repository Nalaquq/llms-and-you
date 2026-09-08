"""Week 3 review, part one: five ways to turn text into numbers, one slide each.

  w03_s03_tokenization.gif   tokens, stems, lemmas
  w03_s04_binary.gif         one-hot / binary vectorization
  w03_s05_bow.gif            bag of words
  w03_s06_tfidf.gif          TF-IDF
  w03_s07_word2vec.gif       word2vec (skip-gram / CBOW) and cosine

Week 2 spent a session on these; this is the compression. Each slide is the
same three things -- the technique running, the deal it strikes, and the
formula along the bottom -- so the room can see the ladder in five minutes
without being taught it twice.

Every number on these slides is computed here, not typed in. The TF-IDF
weights in particular are the real ones for the corpus below, which is how
"the" is allowed to land on exactly zero.
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
    blank_axes,
    chip,
    fig_to_pil,
    footer,
    hold,
    math_strip,
    new_fig,
    pros_cons,
    save_gif,
)

PANEL_RECT = [0.045, 0.215, 0.255, 0.575]
DEMO_RECT = [0.345, 0.195, 0.615, 0.60]


def review_frame(fig, n, title, subtitle):
    """Shared furniture: which rung of the ladder this is, and what it is called."""
    fig.text(
        0.045,
        0.945,
        f"REVIEW · REPRESENTATION {n} OF 5",
        fontsize=13,
        color=PURPLE,
        fontweight="bold",
        va="top",
    )
    fig.text(0.045, 0.895, title, fontsize=30, color=TEXT, fontweight="bold", va="top")
    fig.text(0.045, 0.838, subtitle, fontsize=15.5, color=SUB, va="top")


# =====================================================================
# SLIDE 3 — tokenization, stemming, lemmatization
# =====================================================================
RAW = "The models were learning quickly."
TOKENS = ["The", "models", "were", "learning", "quickly", "."]
SUBWORD = ("tokenization", ["token", "##ization"])
NORMAL = [
    ("models", "model", "model"),
    ("were", "were", "be"),
    ("learning", "learn", "learn"),
    ("quickly", "quickli", "quickly"),
]


def make_tokenization():
    def render(phase):
        fig = new_fig()
        review_frame(
            fig,
            1,
            "Tokenization, stemming, lemmatization",
            "Before any arithmetic: cut the string up, and "
            "decide which forms count as the same word.",
        )
        pros_cons(
            fig,
            PANEL_RECT,
            [
                "A fixed, finite vocabulary\nout of infinite text.",
                "Subwords mean no word is\never unknown.",
                "Cheap, deterministic, and\nthe same every run.",
            ],
            [
                "A token is not a word. The\nletters are gone "
                "— which is\nwhy 'how many r's' is hard.",
                "Stems are often not words:\nquickly → quickli.",
                "Lemmatizing needs a\ndictionary and the part of\nspeech, per language.",
            ],
        )
        ax = blank_axes(fig, DEMO_RECT)

        ax.text(0.0, 0.99, "the string", fontsize=10.5, color=FAINT, fontweight="bold", va="top")
        ax.text(0.0, 0.90, f'"{RAW}"', fontsize=16, color=TEXT, va="top", fontfamily="monospace")

        if phase >= 1:
            ax.text(0.0, 0.735, "tokens", fontsize=10.5, color=FAINT, fontweight="bold", va="top")
            x = 0.0
            for tok in TOKENS:
                w = 0.018 + 0.026 * len(tok)
                chip(ax, x, 0.575, w, 0.095, tok, fontsize=12.5, mono=True, edge=BLUE, color=BLUE)
                x += w + 0.012

        if phase >= 2:
            ax.text(
                0.0,
                0.47,
                "a rare word splits into subwords",
                fontsize=10.5,
                color=FAINT,
                fontweight="bold",
                va="top",
            )
            word, pieces = SUBWORD
            x = 0.0
            ax.text(x, 0.355, word, fontsize=13, color=SUB, va="center", fontfamily="monospace")
            x += 0.021 * len(word) + 0.02
            ax.text(x, 0.355, "→", fontsize=13, color=FAINT, va="center")
            x += 0.045
            for piece in pieces:
                w = 0.018 + 0.024 * len(piece)
                chip(ax, x, 0.31, w, 0.09, piece, fontsize=12, mono=True, edge=YELLOW, color=YELLOW)
                x += w + 0.012
            ax.text(
                x + 0.02,
                0.355,
                "## = a continued token",
                fontsize=11.5,
                color=FAINT,
                va="center",
            )

        if phase >= 3:
            ax.text(
                0.0,
                0.20,
                "and which forms count as the same word",
                fontsize=10.5,
                color=FAINT,
                fontweight="bold",
                va="top",
            )
            rows = (
                ("token", [n[0] for n in NORMAL], TEXT),
                ("stem", [n[1] for n in NORMAL], ORANGE),
                ("lemma", [n[2] for n in NORMAL], GREEN),
            )
            for r, (label, values, colour) in enumerate(rows):
                y = 0.10 - r * 0.062
                ax.text(0.0, y, label, fontsize=11.5, color=SUB, va="center")
                for c, val in enumerate(values):
                    ax.text(
                        0.13 + c * 0.20,
                        y,
                        val,
                        fontsize=12.5,
                        color=colour,
                        va="center",
                        fontfamily="monospace",
                    )

        math_strip(
            fig,
            r"$T(\mathrm{text}) \rightarrow (t_1, t_2, \ldots, t_n), \quad "
            r"t_i \in V, \quad |V| \approx 30{,}000$",
            note="every model you use starts here",
        )
        footer(
            fig,
            "study guide: token-and-tokenization · vocabulary "
            "· stemming · lemmatization · stop-words",
        )
        return fig_to_pil(fig)

    frames, durations = [], []
    for p in range(4):
        hold(frames, durations, lambda p=p: render(p), ms=1000)
    hold(frames, durations, lambda: render(3), ms=1000)
    save_gif(frames, durations, "w03_s03_tokenization.gif")


# =====================================================================
# SLIDE 4 — binary vectorization (one-hot)
# =====================================================================
VOCAB = ["a", "cat", "dog", "king", "sat", "the"]
ONEHOT_WORDS = ["cat", "dog", "king"]


def make_binary():
    def render(phase):
        fig = new_fig()
        review_frame(
            fig,
            2,
            "Binary vectorization",
            "One slot per vocabulary word. Turn on the slot that is the word, and nothing else.",
        )
        pros_cons(
            fig,
            PANEL_RECT,
            [
                "Exact and lossless: every\nword stays distinguishable.",
                "No training, no corpus\nstatistics, no choices.",
                "Still the format every\nmodel's output layer uses.",
            ],
            [
                "One word costs |V| numbers,\n49,999 of them zero.",
                "Every pair of words is\nequally dissimilar.",
                "Nothing about a word's\nmeaning is anywhere in it.",
            ],
        )
        ax = blank_axes(fig, DEMO_RECT)

        ax.text(0.0, 0.97, "vocabulary", fontsize=10.5, color=FAINT, fontweight="bold", va="top")
        for i, v in enumerate(VOCAB):
            ax.text(
                0.0,
                0.86 - i * 0.115,
                v,
                fontsize=13.5,
                color=SUB,
                va="center",
                fontfamily="monospace",
            )

        shown = min(phase, len(ONEHOT_WORDS))
        for c, word in enumerate(ONEHOT_WORDS[:shown]):
            x = 0.18 + c * 0.135
            ax.text(
                x + 0.045,
                0.965,
                word,
                fontsize=13.5,
                color=BLUE,
                ha="center",
                va="top",
                fontfamily="monospace",
                fontweight="bold",
            )
            for i, v in enumerate(VOCAB):
                on = v == word
                chip(
                    ax,
                    x,
                    0.815 - i * 0.115,
                    0.09,
                    0.085,
                    "1" if on else "0",
                    fontsize=13,
                    mono=True,
                    face=PANEL if not on else "#2b3446",
                    edge=BLUE if on else PANEL_EDGE,
                    color=BLUE if on else FAINT,
                    lw=2.0 if on else 1.2,
                )

        if phase >= 4:
            ax.text(0.60, 0.72, "so how similar are they?", fontsize=13.5, color=TEXT, va="top")
            pairs = [("cat", "dog", 0), ("cat", "king", 0), ("dog", "king", 0)]
            for i, (a, b, dot) in enumerate(pairs):
                ax.text(
                    0.60,
                    0.60 - i * 0.10,
                    f"{a} · {b}  =  {dot}",
                    fontsize=15,
                    color=RED,
                    va="top",
                    fontfamily="monospace",
                )
            ax.text(
                0.60,
                0.26,
                "Every pair. Always zero.\nThe vectors are orthogonal\nby "
                "construction — cat is no\ncloser to dog than to king.",
                fontsize=13,
                color=SUB,
                va="top",
                linespacing=1.5,
            )

        math_strip(
            fig,
            [
                r"$x_w \in \{0,1\}^{|V|}, \qquad x_w[i] = 1 \;\; \mathrm{if} \;\; w = v_i, "
                r"\;\; \mathrm{else} \;\; 0$",
                r"$x_a \cdot x_b = 0 \quad \mathrm{for\ every\ pair} \quad a \neq b$",
            ],
        )
        footer(fig, "study guide: one-hot-encoding · sparse-and-dense-vectors · dot-product")
        return fig_to_pil(fig)

    frames, durations = [], []
    for p in range(5):
        hold(frames, durations, lambda p=p: render(p), ms=900)
    hold(frames, durations, lambda: render(4), ms=1000)
    save_gif(frames, durations, "w03_s04_binary.gif")


# =====================================================================
# SLIDE 5 — bag of words
# =====================================================================
BOW_DOCS = ["the dog bites the man", "the man bites the dog"]
BOW_VOCAB = ["bites", "dog", "man", "the"]


def _counts(doc):
    return [doc.split().count(v) for v in BOW_VOCAB]


def make_bow():
    def render(phase):
        fig = new_fig()
        review_frame(
            fig,
            3,
            "Bag of words",
            "Add the one-hot vectors up. A whole document "
            "becomes one fixed-length vector of counts.",
        )
        pros_cons(
            fig,
            PANEL_RECT,
            [
                "A document of any length\nbecomes one fixed vector.",
                "Similarity is finally non-zero:\nshared words show up.",
                "Still a serious baseline for\nclassification and search.",
            ],
            [
                "Word order is gone. Not\nweakened — gone.",
                "Still |V| dimensions, still\nalmost all zeros.",
                "'the' counts as loudly as\nthe word that matters.",
                "Synonyms share nothing:\ncar and automobile are\nas unrelated as cat and if.",
            ],
        )
        ax = blank_axes(fig, DEMO_RECT)

        for i, v in enumerate(BOW_VOCAB):
            ax.text(
                0.0,
                0.72 - i * 0.115,
                v,
                fontsize=13.5,
                color=SUB,
                va="center",
                fontfamily="monospace",
            )

        for c, doc in enumerate(BOW_DOCS[: min(phase, 2)]):
            x = 0.20 + c * 0.145
            ax.text(
                x + 0.045,
                0.93,
                f"d{c + 1}",
                fontsize=13.5,
                color=BLUE,
                ha="center",
                va="center",
                fontfamily="monospace",
                fontweight="bold",
            )
            ax.text(0.20, 0.84 - c * 0.0, "", fontsize=1)
            for i, n in enumerate(_counts(doc)):
                chip(
                    ax,
                    x,
                    0.675 - i * 0.115,
                    0.09,
                    0.085,
                    str(n),
                    fontsize=13,
                    mono=True,
                    face="#2b3446" if n else PANEL,
                    edge=BLUE if n else PANEL_EDGE,
                    color=BLUE if n else FAINT,
                    lw=2.0 if n else 1.2,
                )

        for c, doc in enumerate(BOW_DOCS[: min(phase, 2)]):
            ax.text(
                0.52,
                0.72 - c * 0.115,
                f'd{c + 1}:  "{doc}"',
                fontsize=13.5,
                color=TEXT,
                va="center",
                fontfamily="monospace",
            )

        if phase >= 3:
            ax.text(
                0.52,
                0.44,
                "Two opposite claims about who\nbit whom. Identical vectors.",
                fontsize=14,
                color=RED,
                va="top",
                linespacing=1.5,
            )
            ax.text(
                0.52,
                0.22,
                "Any method built only on counts\ncannot tell "
                "these apart — and\nmost of language is word order.",
                fontsize=13,
                color=SUB,
                va="top",
                linespacing=1.5,
            )

        math_strip(
            fig,
            r"$x_d[j] \;=\; \sum_{i=1}^{n} 1[\, t_i = v_j \,] "
            r"\qquad\mathrm{that\ is,}\qquad x_d = \sum_{i=1}^{n} x_{t_i}$",
            note="the document is the sum of its one-hots",
        )
        footer(fig, "study guide: bag-of-words · count-vectorization · n-grams")
        return fig_to_pil(fig)

    frames, durations = [], []
    for p in range(4):
        hold(frames, durations, lambda p=p: render(p), ms=1000)
    hold(frames, durations, lambda: render(3), ms=1000)
    save_gif(frames, durations, "w03_s05_bow.gif")


# =====================================================================
# SLIDE 6 — TF-IDF  (weights computed, not asserted)
# =====================================================================
CORPUS = [
    "the leaf uses light to make sugar",
    "the plant stores sugar in the root",
    "photosynthesis happens in the chloroplast",
    "the chloroplast holds chlorophyll",
    "chlorophyll gives the leaf its colour",
]
TFIDF_DOC = 1  # "the plant stores sugar in the root" -- has a repeated 'the'


def tfidf_table():
    """Real TF-IDF for one document of CORPUS. 'the' lands on zero on its own."""
    n_docs = len(CORPUS)
    doc = CORPUS[TFIDF_DOC].split()
    rows = []
    for term in dict.fromkeys(doc):
        tf = doc.count(term)
        df = sum(1 for d in CORPUS if term in d.split())
        idf = float(np.log(n_docs / df))
        rows.append((term, tf, df, tf * idf))
    return sorted(rows, key=lambda r: -r[3])


def make_tfidf():
    rows = tfidf_table()
    top = max(r[3] for r in rows)

    def render(phase):
        fig = new_fig()
        review_frame(
            fig,
            4,
            "TF-IDF",
            "Same counts, reweighted: a word matters here only if it does not appear everywhere.",
        )
        pros_cons(
            fig,
            PANEL_RECT,
            [
                "Ubiquitous words fall out on\ntheir own — "
                "no stop list to\nmaintain or argue about.",
                "The words that identify a\ndocument rise to the top.",
                "Cheap, interpretable, and it\nran web search for 20 years.",
            ],
            [
                "Word order is still gone.",
                "Still sparse, still |V| wide.",
                "Synonyms still share nothing.",
                "The weights belong to the\ncorpus you happened to have,\nnot to the language.",
            ],
        )
        ax = blank_axes(fig, DEMO_RECT)

        ax.text(
            0.0,
            0.99,
            "a five-document corpus",
            fontsize=10.5,
            color=FAINT,
            fontweight="bold",
            va="top",
        )
        for i, d in enumerate(CORPUS):
            hit = i == TFIDF_DOC
            ax.text(
                0.0,
                0.90 - i * 0.058,
                f"d{i + 1}   {d}",
                fontsize=11.5,
                color=YELLOW if hit else FAINT,
                va="top",
                fontfamily="monospace",
                fontweight="bold" if hit else "normal",
            )

        if phase >= 1:
            ax.text(
                0.0, 0.505, "scoring d2", fontsize=10.5, color=FAINT, fontweight="bold", va="top"
            )
            ax.text(0.155, 0.505, "count in d2", fontsize=10.5, color=BLUE, va="top")
            ax.text(0.32, 0.505, "docs it appears in", fontsize=10.5, color=SUB, va="top")
            ax.text(0.56, 0.505, "tf-idf", fontsize=10.5, color=ORANGE, va="top")

            shown = rows if phase >= 2 else rows[:0]
            for i, (term, tf, df, score) in enumerate(rows):
                y = 0.425 - i * 0.068
                dead = score == 0
                ax.text(
                    0.0,
                    y,
                    term,
                    fontsize=12.5,
                    color=RED if dead else TEXT,
                    va="center",
                    fontfamily="monospace",
                )
                ax.text(
                    0.185,
                    y,
                    str(tf),
                    fontsize=12.5,
                    color=BLUE,
                    va="center",
                    fontfamily="monospace",
                )
                ax.text(
                    0.40,
                    y,
                    f"{df} of 5",
                    fontsize=12.5,
                    color=SUB,
                    va="center",
                    fontfamily="monospace",
                )
                if (term, tf, df, score) in shown:
                    ax.barh(
                        y,
                        0.30 * score / top,
                        height=0.045,
                        left=0.56,
                        color=RED if dead else ORANGE,
                        alpha=0.85,
                    )
                    ax.text(
                        0.88,
                        y,
                        f"{score:.2f}",
                        fontsize=12.5,
                        color=RED if dead else ORANGE,
                        va="center",
                        fontfamily="monospace",
                    )

        if phase >= 3:
            ax.text(
                0.0,
                0.012,
                "'the' is in all five documents: log(5/5) = 0. It scores nothing, and "
                "nobody had to put it on a list.",
                fontsize=12.5,
                color=YELLOW,
                va="center",
            )

        math_strip(
            fig,
            r"$\mathrm{tfidf}(t, d) \;=\; \mathrm{tf}(t, d) \cdot "
            r"\log \frac{N}{\mathrm{df}(t)}$",
            note="N = documents in the corpus,  df = how many contain t",
        )
        footer(
            fig,
            "study guide: term-frequency · inverse-document-frequency · tf-idf · stop-words",
        )
        return fig_to_pil(fig)

    frames, durations = [], []
    for p in range(4):
        hold(frames, durations, lambda p=p: render(p), ms=1050)
    hold(frames, durations, lambda: render(3), ms=1000)
    save_gif(frames, durations, "w03_s06_tfidf.gif")


# =====================================================================
# SLIDE 7 — word2vec
# =====================================================================
W2V_SENT = ["the", "cat", "sat", "on", "the", "warm", "mat"]
W2V_CENTRE = 2  # "sat"
W2V_WINDOW = 2
# Illustrative vectors -- 4 of the 300 dimensions. The cosines below are
# computed from exactly these numbers, so what is on the slide is consistent.
W2V_VECS = {
    "cat": np.array([0.71, -0.22, 0.35, 0.09]),
    "dog": np.array([0.66, -0.17, 0.41, 0.12]),
    "king": np.array([-0.28, 0.64, 0.11, -0.53]),
}


def cosine(a, b):
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


def make_word2vec():
    def render(phase):
        fig = new_fig()
        review_frame(
            fig,
            5,
            "word2vec",
            "Stop assigning the numbers. Learn them, from which words keep company with which.",
        )
        pros_cons(
            fig,
            PANEL_RECT,
            [
                "Dense: 300 numbers, not\n50,000 — and every one\nof them is used.",
                "Similarity is graded, and\nlearned from "
                "raw text with\nno labels and no annotators.",
                "Free at use time: the vector\nis a lookup.",
            ],
            [
                "One vector per word, forever.\n'bank' gets exactly one.",
                "Needs a large corpus, and\ninherits whatever is in it.",
                "Still no word order — the\nvector for a word is the same\nin every sentence.",
            ],
        )
        ax = blank_axes(fig, DEMO_RECT)

        ax.text(
            0.0,
            0.99,
            "slide a window along the corpus",
            fontsize=10.5,
            color=FAINT,
            fontweight="bold",
            va="top",
        )
        xs = np.linspace(0.03, 0.72, len(W2V_SENT))
        for i, (x, word) in enumerate(zip(xs, W2V_SENT, strict=True)):
            centre = i == W2V_CENTRE
            ctx = 0 < abs(i - W2V_CENTRE) <= W2V_WINDOW
            ax.text(
                x,
                0.86,
                word,
                fontsize=15,
                ha="center",
                va="center",
                color=YELLOW if centre else (BLUE if ctx else FAINT),
                fontweight="bold" if centre or ctx else "normal",
                fontfamily="monospace",
            )
        ax.text(
            0.0,
            0.755,
            "yellow = the centre word     blue = the context it must predict  (window ±2)",
            fontsize=10.5,
            color=BLUE,
            va="center",
        )

        if phase >= 1:
            for label, arrow_text, colour, y in (
                ("skip-gram", "centre  →  predict its context", YELLOW, 0.655),
                ("CBOW", "context  →  predict the centre", BLUE, 0.575),
            ):
                ax.text(0.0, y, label, fontsize=12.5, color=colour, va="center", fontweight="bold")
                ax.text(0.19, y, arrow_text, fontsize=12.5, color=SUB, va="center")
            ax.text(
                0.0,
                0.505,
                "Nobody labelled anything. The corpus is its own answer key —\n"
                "and the weights we wanted are what is left after training.",
                fontsize=12,
                color=FAINT,
                va="top",
                linespacing=1.5,
            )

        if phase >= 2:
            ax.text(
                0.0,
                0.365,
                "what training leaves behind",
                fontsize=10.5,
                color=FAINT,
                fontweight="bold",
                va="top",
            )
            for c, (word, vec) in enumerate(W2V_VECS.items()):
                x = 0.0 + c * 0.20
                ax.text(
                    x + 0.055,
                    0.292,
                    word,
                    fontsize=13,
                    color=BLUE,
                    ha="center",
                    fontfamily="monospace",
                    fontweight="bold",
                )
                for i, val in enumerate(vec):
                    ax.text(
                        x + 0.055,
                        0.212 - i * 0.053,
                        f"{val:+.2f}",
                        fontsize=12,
                        color=TEXT,
                        ha="center",
                        fontfamily="monospace",
                    )
                ax.text(
                    x + 0.055, 0.212 - len(vec) * 0.053, "⋮", fontsize=12, color=FAINT, ha="center"
                )

        if phase >= 3:
            ax.text(
                0.66,
                0.292,
                "cosine similarity",
                fontsize=10.5,
                color=FAINT,
                fontweight="bold",
                va="center",
            )
            pairs = [("cat", "dog"), ("cat", "king")]
            for i, (a, b) in enumerate(pairs):
                val = cosine(W2V_VECS[a], W2V_VECS[b])
                ax.text(
                    0.66,
                    0.20 - i * 0.072,
                    f"{a} · {b}   {val:+.2f}",
                    fontsize=14,
                    color=GREEN if val > 0.5 else ORANGE,
                    va="center",
                    fontfamily="monospace",
                )
            ax.text(0.66, 0.03, "graded, at last.", fontsize=12.5, color=SUB, va="center")

        math_strip(
            fig,
            [
                r"$\max \; \sum_{t} \sum_{-c \leq j \leq c,\; j \neq 0} "
                r"\log p(w_{t+j} \mid w_t)$"
                r"$\qquad p(o \mid c) = \frac{\exp(u_o^{\top} v_c)}"
                r"{\sum_{w} \exp(u_w^{\top} v_c)}$",
                r"$\cos(a, b) = \frac{a \cdot b}{\|a\| \, \|b\|}$",
            ],
        )
        footer(
            fig,
            "study guide: word2vec · skip-gram · cbow · negative-sampling · cosine-similarity",
        )
        return fig_to_pil(fig)

    frames, durations = [], []
    for p in range(4):
        hold(frames, durations, lambda p=p: render(p), ms=1050)
    hold(frames, durations, lambda: render(3), ms=1000)
    save_gif(frames, durations, "w03_s07_word2vec.gif")


if __name__ == "__main__":
    make_tokenization()
    make_binary()
    make_bow()
    make_tfidf()
    make_word2vec()
