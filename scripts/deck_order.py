"""The Week 2 deck, in teaching order.

Filenames are stable identifiers; the teaching order lives here, once, and is
read by both ``build_deck.py`` (the PPTX) and the site's slides page (the
gallery). Chronological on purpose: students feel counting fail BEFORE meeting
the learned-embedding idea — the deck's flaw->fix rhythm applied to its own
biggest transition. BoW/TF-IDF produce sparse assigned vectors, not learned
embeddings, so they come first, matching the study guide's ladder.
"""

ORDER = [
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
