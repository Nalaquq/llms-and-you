"""Discussion-prompt interstitials at the deck's four critical junctures.

Each sits right before the slide that exposes the current approach's flaw,
so students predict the failure before it is revealed. Questions appear one
at a time — hold the slide and let them argue.

  w02_s04b_discuss_onehot.gif    after one-hot, before the scorecard
  w02_s12b_discuss_counting.gif  after TF-IDF/preprocessing, before the blob
  w02_s16b_discuss_word2vec.gif  after word2vec, before "bank"
  w02_s18b_discuss_context.gif   after contextual layers, before the recap
"""

from style_dark import (
    ORANGE,
    PANEL,
    PURPLE,
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
)


def make_discussion(name, title, subtitle, questions, closer, sg):
    """One interstitial: numbered questions phased in, then the closer."""

    def render(n_q, show_closer):
        fig = new_fig()
        title_block(fig, title, subtitle, kicker="DISCUSS · PAUSE HERE")
        ax = blank_axes(fig, [0.05, 0.10, 0.90, 0.64])
        # quiet accent rule down the left
        ax.plot([0.012, 0.012], [0.06, 0.97], color=PURPLE, lw=3, alpha=0.6, transform=ax.transAxes)

        top, bottom = 0.88, 0.16
        step = (top - bottom) / max(len(questions) - 1, 1)
        for i, (q, hint) in enumerate(questions[:n_q]):
            y = top - i * step
            chip(
                ax,
                0.045,
                y - 0.065,
                0.055,
                0.115,
                f"{i + 1}",
                fontsize=16,
                mono=True,
                face=PANEL,
                edge=YELLOW,
                color=YELLOW,
                lw=2.0,
                bold=True,
            )
            ax.text(0.135, y + 0.012, q, fontsize=17, color=TEXT, va="center", linespacing=1.45)
            if hint:
                dy = 0.105 if "\n" in q else 0.062
                ax.text(0.135, y - dy, hint, fontsize=13, color=SUB, va="center")
        if show_closer:
            fig.text(0.5, 0.075, closer, fontsize=15, color=ORANGE, ha="center", style="italic")
        footer(fig, sg)
        return fig_to_pil(fig)

    frames, durations = [], []
    hold(frames, durations, lambda: render(0, False), ms=900)
    for k in range(1, len(questions) + 1):
        hold(frames, durations, lambda k=k: render(k, False), ms=1400)
    hold(frames, durations, lambda: render(len(questions), True), ms=1600)
    save_gif(frames, durations, name)


make_discussion(
    "w02_s04b_discuss_onehot.gif",
    "Before we fix it — what's actually broken?",
    "one-hot gave every word a name. talk through what it didn't give us",
    [
        (
            "cat · dog = 0.  Is zero wrong? What number do you want there — and why that one?",
            "zero says 'no relationship at all'. is that ever true of two words?",
        ),
        (
            "Wherever the right numbers come from, who decides that cat is like kitten?",
            "a linguist? a dictionary? a vote? something cheaper?",
        ),
        (
            "Each one-hot vector has 50,000 slots and uses one. How many does a word really need?",
            "what would you spend 300 slots on?",
        ),
    ],
    "hold your answers — the field took thirty years to build them. first, everyone counted.",
    "before: one-hot-encoding · ahead: embedding · dimensionality",
)

make_discussion(
    "w02_s12b_discuss_counting.gif",
    "Counting has taken us far. Where's the wall?",
    "bag of words, TF-IDF, four preprocessing knobs — now find their ceiling",
    [
        (
            'TF-IDF knows "harbour" matters to this document. Does it know harbour ≈ port?',
            "what would it take for two words to look similar to a counter?",
        ),
        (
            'You search "car"; the document only says "automobile".\nWhat do these methods return?',
            "nothing matched. should it have?",
        ),
        (
            '"great, not boring" vs "boring, not great" — what does the bag see?',
            "which knob from the last slide helps, and how far does it get you?",
        ),
    ],
    "next: watch counting hit this wall in real data — then the question that gets past it",
    "before: tf-idf · n-grams · ahead: the ceiling, then word2vec",
)

make_discussion(
    "w02_s16b_discuss_word2vec.gif",
    "word2vec looks like the winner. Find the crack.",
    "meaning from neighbours, one learned vector per word — stress-test it",
    [
        (
            '"I deposited money at the bank" / "we fished from the bank."\n'
            "word2vec hands back ONE vector. A vector of what?",
            "if it must average, what is it averaging?",
        ),
        (
            "Training saw a window of ±2 words. What meaning lives farther away than that?",
            'try: "the trophy didn\'t fit in the suitcase because it was too big"',
        ),
        (
            "Word vectors are solved. What's your plan for a whole\n"
            "sentence — and what breaks if you just average them?",
            "does averaging remind you of anything from earlier today?",
        ),
    ],
    "keep your bank answer — the next slide is that crime scene",
    "before: word2vec · ahead: polysemy · static-vs-contextual-embeddings",
)

make_discussion(
    "w02_s18b_discuss_context.gif",
    "Context solved it, then. What did it cost?",
    "one vector per occurrence, computed through the layers — audit the deal",
    [
        (
            "A contextual vector can't be precomputed into a dictionary.\n"
            "What did we give up, and when will we pay for it?",
            "think: speed, cost, and 'let me just look that word up'",
        ),
        (
            'Each layer mixes in "the rest of the sentence." Which words\n'
            "should a layer listen to most — and who decides?",
            "in the trophy sentence, what should 'it' attend to?",
        ),
        (
            "Everything is still learned from a corpus.\n"
            "Which of today's problems did context NOT fix?",
            "the mirror slide is two slides away — predict it",
        ),
    ],
    "question 2 is the title of next week's paper",
    "before: static-vs-contextual · ahead: corpus (the mirror) · attention (W3)",
)
