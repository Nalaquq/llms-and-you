"""The lecture decks, in teaching order.

Filenames are stable identifiers; the teaching order lives here, once, and is
read by both ``build_deck.py`` (the PPTX) and the site's slides page (the
gallery). One entry in ``DECKS`` per deck.

Week 2 is chronological on purpose: students feel counting fail BEFORE meeting
the learned-embedding idea — the deck's flaw->fix rhythm applied to its own
biggest transition. BoW/TF-IDF produce sparse assigned vectors, not learned
embeddings, so they come first, matching the study guide's ladder.
"""

W02_ORDER = [
    "w02_s01_title.png",
    "w02_s02_text_to_numbers.gif",
    "w02_s03_tokens.gif",
    "w02_s04_onehot.gif",  # naming without meaning
    "w02_s04b_discuss_onehot.gif",  # DISCUSS: what's broken?
    "w02_s10_bag_of_words.gif",  # counting era: add the one-hots up
    "w02_s11_tfidf.gif",
    "w02_s12_preprocessing.png",
    "w02_s12b_discuss_counting.gif",  # DISCUSS: where's the wall?
    "w02_s13_ceiling.gif",  # the wall, in real data
    "w02_s09_company.gif",  # zorp: the question that gets past it
    "w02_s05_scorecard.gif",  # the learned-embedding idea
    "w02_s05b_columns.gif",  # a column, earned from co-occurrence
    "w02_s06_space.gif",  # geometry payoff
    "w02_s06b_3d.gif",
    "w02_s07_cosine.gif",
    "w02_s08_king_queen.gif",
    "w02_s14_window.gif",  # learning it at scale
    "w02_s15_architecture.gif",
    "w02_s16_negative.gif",
    "w02_s16b_discuss_word2vec.gif",  # DISCUSS: find the crack
    "w02_s17_bank.gif",
    "w02_s18_layers.gif",
    "w02_s18b_discuss_context.gif",  # DISCUSS: audit the deal
    "w02_s19_mirror.gif",
    "w02_s20_ladder.gif",
    "w02_s21_teaser.gif",
]


# Week 3: a twenty-minute review, then the transformer. Filename order is not
# teaching order at the end -- s29 (the last discussion) comes before s28 (the
# closing ledger), because the room should argue about the limits before the
# deck ties the bow. Same convention as Week 2.
W03_ORDER = [
    "w03_s01_title.png",
    "w03_s02_taxonomy.gif",  # model vs architecture vs technique
    "w03_s03_tokenization.gif",  # REVIEW: five representations, one slide each
    "w03_s04_binary.gif",
    "w03_s05_bow.gif",
    "w03_s06_tfidf.gif",
    "w03_s07_word2vec.gif",
    "w03_s08_perceptron.gif",  # REVIEW: three architectures the transformer replaced
    "w03_s09_cnn.gif",
    "w03_s10_rnn.gif",
    "w03_s11_recap.gif",  # the three problems left over -> attention
    # --- the transformer itself -------------------------------------------
    "w03_s12_one_idea.gif",
    "w03_s13_discuss_idea.gif",  # DISCUSS: what would it have to look at?
    "w03_s14_question.gif",  # one head, taken apart: query and key
    "w03_s14b_three_views.gif",  # where q, k, v come from, with numbers
    "w03_s15_score.gif",
    "w03_s16_share.gif",
    "w03_s17_blend.gif",  # ...and the formula the recap slide asked for
    "w03_s17b_meaning.gif",  # the moved vector: same word, two sentences
    "w03_s18_discuss_head.gif",  # DISCUSS: is that understanding?
    "w03_s19_heads.gif",  # eight at once, measured in Thursday's model
    "w03_s20_position.gif",  # the word-order problem, back again
    "w03_s21_discuss_heads.gif",  # DISCUSS: two design choices
    "w03_s22_mask.gif",  # writing without reading ahead
    "w03_s23_cross.gif",  # the bridge, and the crossing
    "w03_s24_discuss_bridge.gif",  # DISCUSS: did we really beat the RNN?
    "w03_s25_block.gif",  # one block, six times
    "w03_s26_parallel.gif",  # why it actually won
    "w03_s27_not_explanation.gif",  # and what it does not give you
    "w03_s29_discuss_limits.gif",  # DISCUSS: what would an explanation be?
    "w03_s28_closing.gif",  # the ledger closed -> Thursday
]


class Deck:
    """One lecture deck: its slides, its filenames, and whether the site shows it."""

    def __init__(self, prefix, stem, order, publish):
        self.prefix = prefix  # media filenames start with this
        self.stem = stem  # <stem>.pptx and <stem>_print.pptx
        self.order = order
        self.publish = publish  # does the site serve it yet?


DECKS = [
    Deck("w02", "W02_How_Text_Becomes_Numbers", W02_ORDER, publish=True),
    Deck("w03", "W03_Attention_and_the_Transformer", W03_ORDER, publish=True),
]

# Week 2's order, still importable under its old name.
ORDER = W02_ORDER
