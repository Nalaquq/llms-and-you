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
    "w03_s19_heads.gif",  # eight at once, measured in the translation notebook
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


# Week 6: chain-of-thought, for students with no programming or mathematics
# beyond school algebra. Five parts: what it is and how to use it (s01-s11),
# the evidence (s12-s18), the words the critique needs (s19-s24), the critique
# in full with its equations (s25-s39), and weighing both papers (s40-s45).
# Every term gets a slide before it is used. The Appendix C mathematics comes
# AFTER the closing slide (s46-s49): backup for the room, or for students who
# ask -- the main flow keeps the equations in the paper's main text.
# Research-design sections are shown from the paper first, then redrawn.
W06_ORDER = [
    "w06_s01_title.png",
    "w06_s02_cold_open.gif",  # Wei Fig. 1: same model, 27 or 9
    "w06_s03_roadmap.gif",
    # --- part 1: what it is, how to use it ----------------------------------
    "w06_s04_next_token.gif",  # one token at a time; it reads its own writing
    "w06_s05_prompt_vocab.gif",  # zero-shot, few-shot, exemplar
    "w06_s06_anatomy.gif",  # Wei's definition, drawn
    "w06_s07_four_claims.gif",  # and where each claim gets tested
    "w06_s08_zero_shot.gif",  # "Let's think step by step"; reasoning models
    "w06_s09_variants.gif",  # self-consistency, least-to-most, tree of thoughts
    "w06_s10_how_to_use.gif",  # a recipe, with evidence per line
    "w06_s11_discuss_vendors.gif",  # DISCUSS: sellers vs inventors
    # --- part 2: the evidence ------------------------------------------------
    "w06_s12_benchmark.gif",  # GSM8K; which 58% is which
    "w06_s13_emergence.gif",  # hurts small models, helps big ones
    "w06_s14_ablation_idea.gif",  # a cake, then Wei's ingredient grid
    "w06_s15_paper_ablation.gif",  # Figure 5 as printed
    "w06_s16_ablation.gif",  # redrawn: three stories ruled out
    "w06_s17_caveats.gif",  # §6: the cautious inventors
    "w06_s18_discuss_answer.gif",  # DISCUSS: what would an answer look like?
    # --- part 3: words the critique needs ------------------------------------
    "w06_s19_distribution.gif",
    "w06_s20_ood.gif",
    "w06_s21_leakage.gif",
    "w06_s22_training.gif",  # scratch vs fine-tuned; model sizes
    "w06_s23_temperature.gif",
    "w06_s24_metrics.gif",  # exact match, edit distance, BLEU
    # --- part 4: the critique ------------------------------------------------
    "w06_s25_hypothesis.gif",
    "w06_s26_paper_dataalchemy.gif",  # Figure 2 as printed: why a toy
    "w06_s27_dataalchemy.gif",  # the toy running
    "w06_s28_risk.gif",  # eq. (1)-(3)
    "w06_s29_tv.gif",  # eq. (4)-(5)
    "w06_s30_bound.gif",  # eq. (6), Theorem 3.1
    "w06_s31_dials.gif",  # eq. (7)
    "w06_s32_task_ladder.gif",  # ID / CMP / POOD / OOD
    "w06_s33_collapse.gif",  # Tables 1 and 5
    "w06_s34_sft.gif",  # Figure 4: the patch
    "w06_s35_length.gif",
    "w06_s36_format.gif",
    "w06_s37_unfaithful.gif",  # Table 2, App. E.1.1
    "w06_s38_robustness.gif",  # temperature, size, architecture, real models
    "w06_s39_conclusions.gif",  # what they conclude, what they concede
    # --- part 5: weighing it -------------------------------------------------
    "w06_s40_questions_critique.gif",
    "w06_s41_questions_original.gif",
    "w06_s42_use_now.gif",
    "w06_s43_debate.gif",
    "w06_s44_discuss_session.gif",  # DISCUSS: after the debate
    "w06_s45_closing.gif",  # -> Thursday's lab
    # --- backup: Appendix C mathematics ---------------------------------------
    "w06_s46_task_decay.gif",
    "w06_s47_length_curve.gif",
    "w06_s48_format_cosine.gif",
    "w06_s49_proof.gif",
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
    Deck("w06", "W06_Chain_of_Thought", W06_ORDER, publish=True),
]

# Week 2's order, still importable under its old name.
ORDER = W02_ORDER
