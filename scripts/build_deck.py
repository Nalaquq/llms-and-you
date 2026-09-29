"""Assemble the lecture decks from scripts/demo_photos/.

Run every gen_*.py first, then:  python build_deck.py
One PPTX per entry in ``deck_order.DECKS``, plus a print edition of each.

Slides are 16:9, dark (#1b1e26) to match the GIF backgrounds and the course
site's slate theme. GIFs animate in slideshow mode. Each slide carries speaker
notes naming the study-guide concepts it teaches, so the deck and
docs/study-guide.md stay in step.
"""

import glob
import os
import sys

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from deck_order import DECKS  # noqa: E402

PHOTOS = os.path.join(SCRIPT_DIR, "demo_photos")
BG = RGBColor(0x1B, 0x1E, 0x26)


# Speaker notes, keyed by slide file prefix. First line = the beat to hit;
# "SG:" names the study-guide entries; "Ask:" is a question to throw out.
NOTES = {
    "w02_s01": (
        "Cold open: this map is real — every dot is a word placed by arithmetic. "
        "By the end of today they can read this picture.\n"
        "Session: How Text Becomes Numbers (w02-tue)."
    ),
    "w02_s02": (
        "The entire lecture is the ? box. Models never see letters — only numbers.\n"
        "SG: vector · embedding.\n"
        "Ask: what do YOU think is in the box?"
    ),
    "w02_s03": (
        "Tokens are not words. The primer's own example — 'coders' becomes "
        "cod+ers. Strawberry lands here: it's not that models can't count, "
        "they never saw the letters.\n"
        "SG: token-and-tokenization · vocabulary.\n"
        "Thursday's lab: we call the real token counter on their own text."
    ),
    "w02_s04": (
        "First honest attempt. Let them compute cat·dog aloud — it's zero, and "
        "zero for EVERY pair. Identity without meaning, 50k slots of zeros.\n"
        "SG: one-hot-encoding · sparse-and-dense-vectors · dot-product (preview)."
    ),
    "w02_s04b": (
        "DISCUSSION (3-5 min). Fish for: (1) similarity should be graded, "
        "not binary — they'll invent cosine before meeting it; (2) nobody "
        "hand-decides — it has to come from data, cheaply, at scale; "
        "(3) far fewer slots, densely used — they'll invent dimensionality.\n"
        "Don't resolve the questions. The field didn't either: next comes "
        "what everyone did first — count. Their answers get delivered at "
        "the scorecard, after counting hits its ceiling."
    ),
    "w02_s05": (
        "The bridge intuition (from Cornell's CS4782 deck): an embedding is a "
        "scorecard. Similar words = similar rows. Then the twist: nobody writes "
        "it — training fills it in, axes unlabelled, ~1,000 columns.\n"
        "SG: embedding · dimensionality.\n"
        "Ask: what would a 'verb-ness' column score for 'run'?"
    ),
    "w02_s05b": (
        "The scorecard, earned. Derive ONE column live: count how often each "
        "word appears near feline company (purr, fur, claws), rescale, and a "
        "column materialises. king scores low — no cat-words in his company.\n"
        "SG: embedding · distributional-hypothesis · corpus.\n"
        "Key line: training runs this for hundreds of columns at once and "
        "never names any of them — which is why axes are unlabelled."
    ),
    "w02_s06": (
        "Watch meaning become geometry. Neighbour list on the right is how anyone "
        "actually inspects a space.\n"
        "SG: embedding-space · nearest-neighbours.\n"
        "Caveat now, not later: good/bad are neighbours — similar ≠ synonym."
    ),
    "w02_s06b": (
        "Flatland escape. The opening frame IS the 2-D plot they've been "
        "looking at — top-down. Tilt: a third axis was always there, and king/"
        "coffee, near-neighbours in 2-D, fly apart. Let the rotation run.\n"
        "Then the jump: GPT-2 768 dims, DeepSeek-R1 7,168.\n"
        "SG: dimensionality · embedding-space · dimensionality-reduction.\n"
        "Pros/cons: room for distinctions vs memory+compute, overfitting, "
        "and unviewability — every plot from here on is a projection.\n"
        "Ask: why not just use 10 dimensions? why not a million?"
    ),
    "w02_s07": (
        "The angle IS the similarity. Watch the meter as the arrow swings. "
        "Length changes nothing — that's the whole point of cosine over dot.\n"
        "SG: dot-product · cosine-similarity.\n"
        "This number runs every retrieval system they'll build in Week 10."
    ),
    "w02_s08": (
        "The famous demo, then its cracks. Run it live in the projector "
        "(projector.tensorflow.org) right after this slide.\n"
        "SG: vector-arithmetic-and-its-limits.\n"
        "In-class activity: find one analogy that works and one that fails."
    ),
    "w02_s09": (
        "THE PIVOT. Counting just hit its wall; this is the question that "
        "gets past it. 'zorp': they infer a drink from three sentences — they just "
        "ran the distributional hypothesis themselves. Firth quote lands here.\n"
        "SG: distributional-hypothesis · corpus.\n"
        "This is the hinge of the whole week — everything learned rests on it."
    ),
    "w02_s10": (
        "Rung 1. Order dies in the bag: dog-bites-man == man-bites-dog, and no "
        "setting fixes it — the method is working as designed.\n"
        "SG: bag-of-words · count-vectorization.\n"
        "Still the backbone of keyword search everywhere."
    ),
    "w02_s11": (
        "Rung 2. TF x IDF; 'the' is deleted by arithmetic, not by a list. "
        "Fully interpretable — every score explainable. Worth admiring.\n"
        "SG: term-frequency · inverse-document-frequency · tf-idf · stop-words."
    ),
    "w02_s12": (
        "Fast tour, 90 seconds. The trap to name: stop-word removal deletes "
        "'not' — negation lives in stop words.\n"
        "SG: stemming · lemmatization · stop-words · n-grams.\n"
        "Each knob is an ADR-sized decision, not a default."
    ),
    "w02_s12b": (
        "DISCUSSION (3-5 min). Fish for: (1) no — counters can't see "
        "similarity, only co-occurrence in documents; (2) nothing returned — "
        "the synonym gap, this is why search moved to embeddings; (3) the "
        "bag is identical, bigrams patch it locally and explode the "
        "vocabulary.\n"
        "Next slide is the blob: counting's ceiling in real data. Then "
        "zorp — the question that escapes it — so question 1 gets its "
        "answer two slides from now. Don't give it away here."
    ),
    "w02_s13": (
        "The ceiling. Real TF-IDF spaces collapse into a blob (the HF primer "
        "shows this with PCA). Counting cannot learn cat≈kitten. A different "
        "QUESTION was needed — that pivot is the next slide.\n"
        "SG: tf-idf (pitfall) · dimensionality-reduction."
    ),
    "w02_s14": (
        "The new question: predict your neighbours. Window slides, pairs fall "
        "out — billions of free training examples, no human labels.\n"
        "SG: sliding-window · skip-gram · cbow.\n"
        "Skip-gram: word→context. CBOW: context→word. Both same bet."
    ),
    "w02_s15": (
        "word2vec's secret: the network is a pretext. After training, throw the "
        "output layer away — matrix W (one row per word) was the treasure.\n"
        "SG: word2vec · pretext-task · neural-network-and-layers · "
        "parameters-and-weights · softmax.\n"
        "Same trick later: BERT's masking, GPT's next-token."
    ),
    "w02_s16": (
        "Full softmax over 50k words per step = untrainable. Negative sampling "
        "changes the question to yes/no with a few random fakes.\n"
        "SG: negative-sampling · softmax · training-and-inference.\n"
        "Name the pattern: cheap approximation beats exact computation."
    ),
    "w02_s16b": (
        "DISCUSSION (3-5 min). Fish for: (1) an average of every sense — "
        "a point between rivers and money, wrong about both; (2) long-range "
        "reference (the trophy/suitcase 'it') — windows can't reach it; "
        "(3) averaging word vectors = a bag of vectors — they just "
        "reinvented bag-of-words one level up. Enjoy that landing.\n"
        "Next slide is the bank crime scene they just predicted."
    ),
    "w02_s17": (
        "The flaw that ends the word2vec era: 'bank' gets ONE vector, wrong "
        "about both senses. Static vs contextual is discussion question 3.\n"
        "SG: polysemy · static-vs-contextual-embeddings."
    ),
    "w02_s18": (
        "The fix, honestly told: an LLM's embedding layer is STILL a lookup "
        "table. Context is added by the layers above — watch the two 'bank's "
        "diverge on the way up. The mixing machinery is attention = Week 3.\n"
        "SG: static-vs-contextual-embeddings · bert · encoder-and-decoder · "
        "masked-language-modelling."
    ),
    "w02_s18b": (
        "DISCUSSION (3-5 min). Fish for: (1) no more precomputed "
        "dictionary — every representation needs a forward pass: compute, "
        "cost, latency (Week 11 territory); (2) which words to listen to "
        "is exactly attention — question 2 IS next week's paper title; "
        "(3) bias, staleness, corpus-bounds — the mirror slide lands in "
        "two slides and they'll have predicted it.\n"
        "The arc closes here: every method today existed to fix the one "
        "before it — say that out loud before the recap."
    ),
    "w02_s19": (
        "Two receipts that the space mirrors its corpus: Bolukbasi's she–he "
        "occupations, and 'broadcast' drifting across centuries.\n"
        "SG: corpus · distributional-hypothesis (pitfall).\n"
        "Moral: interrogate the corpus, not the model's 'understanding'."
    ),
    "w02_s20": (
        "The whole week in one picture. Each rung fixed the last one's flaw and "
        "exposed its own. Reading responses can ask for any rung's ✓ and ✗.\n"
        "SG: bag-of-words · tf-idf · word2vec · bert (the ladder)."
    ),
    "w02_s21": (
        "Cliffhanger. Seq2seq squeezes a sentence through one fixed vector; "
        "long sentences die. The 2017 fix is attention — the paper this course "
        "is named after. Read Alammar's seq2seq post before Tuesday.\n"
        "SG: sequence-to-sequence · hidden-state · fixed-length-bottleneck · "
        "recurrent-neural-network."
    ),
    # ---- Week 3: the review that opens the transformer session -------------
    # Twenty minutes, hard stop. These notes carry a running clock because the
    # review is the part that always overruns, and the paper is the lecture.
    "w03_s01": (
        "Cold open. Ask the room which word 'it' refers to, and how they know. "
        "Nobody can say WHY they know -- that is the session.\n"
        "Then: twenty minutes of review, and hold yourself to it. The paper is "
        "the lecture; this is the runway.\n"
        "Session: Attention and the Transformer (w03-tue)."
    ),
    "w03_s02": (
        "0:00-0:02. The three words get used interchangeably all term and they "
        "are not the same. Make them place a name in the right column out loud: "
        "BERT, TF-IDF, transformer.\n"
        "SG: parameters-and-weights · training-and-inference.\n"
        "Ask: is word2vec an architecture or a model? (Both names get used for "
        "it -- skip-gram is the architecture, the trained vectors are the model. "
        "That confusion is the point.)"
    ),
    "w03_s03": (
        "0:02-0:05. One slide for all of Week 2's preprocessing. Land one thing: "
        "the model never sees letters, only token ids -- which is why counting "
        "the r's in strawberry is hard and not a sign of stupidity.\n"
        "SG: token-and-tokenization · vocabulary · stemming · lemmatization."
    ),
    "w03_s04": (
        "0:05-0:07. Have them compute cat · dog aloud. Zero. Every pair, zero. "
        "That is the flaw the entire rest of the ladder is fixing.\n"
        "SG: one-hot-encoding · sparse-and-dense-vectors · dot-product."
    ),
    "w03_s05": (
        "0:07-0:09. Bag of words IS the sum of the one-hots -- say that, it is "
        "the line that makes the ladder feel inevitable. Then the punchline: "
        "'dog bites man' and 'man bites dog' are the same vector.\n"
        "SG: bag-of-words · count-vectorization.\n"
        "Ask: name a sentence pair where losing order changes everything."
    ),
    "w03_s06": (
        "0:09-0:11. The weights on this slide are computed from the five-document "
        "corpus shown, not typed in: 'the' really does score 0.00, because "
        "log(5/5) = 0. Point at it. Nobody wrote a stop list.\n"
        "SG: term-frequency · inverse-document-frequency · tf-idf · stop-words."
    ),
    "w03_s07": (
        "0:11-0:14. The turn from assigned numbers to learned ones. Two beats: "
        "the corpus is its own answer key (no labels, no annotators), and the "
        "vectors are what is LEFT OVER after training a throwaway task.\n"
        "SG: word2vec · skip-gram · cbow · negative-sampling · cosine-similarity.\n"
        "Carry the flaw forward: one vector per word, so 'bank' gets one."
    ),
    "w03_s08": (
        "0:14-0:16. NOT a study-guide entry -- say so, they will ask. It is here "
        "so 'the transformer is a stack of these' means something.\n"
        "The classic example, on purpose: bedrooms and miles to downtown in, a "
        "price out. Let the arithmetic build and read it aloud: 3 times 45k, 4 "
        "times minus 12k, plus the 150k bias, 237k. Then House B, faster. Every "
        "number on screen is one of the two weights or the bias -- point at them.\n"
        "Learning = choosing those three numbers from houses that sold. Say it once.\n"
        "The flaw: it is a straight line. A bedroom is worth the same 45k downtown "
        "or forty miles out, because the inputs never interact. Hold that -- 'not' "
        "and 'good' is the same failure, and the next two slides are this unit, "
        "rearranged."
    ),
    "w03_s09": (
        "0:16-0:18. Also background, not assessed. The bridge is the point: THIS "
        "IS THE SAME UNIT. Three weighted edges into a sum, exactly as on the last "
        "slide -- only now the inputs are three word-vectors and the unit is copied "
        "along the sentence with the same weights. Watch it slide.\n"
        "The filter here IS the phrase 'not very good', which is what a learned "
        "filter means.\n"
        "The cost is the point: three words wide. 'The animal ... it' is thirteen "
        "apart, and no amount of pooling helps."
    ),
    "w03_s10": (
        "0:18-0:20. This one IS assessed, and it is the direct ancestor of "
        "today's paper. Same unit a third time: every box is slide 8's sum, with "
        "one extra input -- its own answer from the word before. That arrow between "
        "the boxes is the whole idea.\n"
        "Two costs, both fatal: strictly sequential (t5 waits for t4, so the GPU "
        "idles), and the early words fade.\n"
        "SG: recurrent-neural-network · hidden-state · sequence-to-sequence · "
        "fixed-length-bottleneck.\n"
        "Ask: what would you have to change to read the whole sentence at once?"
    ),
    "w03_s11": (
        "0:20. Review ends here. The three requirements on this slide are the "
        "paper's abstract, restated as demands the room generated itself -- read "
        "them back as 'you just asked for attention'.\n"
        "Leave the Attention(Q, K, V) = ? on screen while the transformer half "
        "begins.\n"
        "SG: static-vs-contextual-embeddings · sequence-to-sequence · "
        "fixed-length-bottleneck."
    ),
    # ---- Week 3: the transformer -------------------------------------------
    "w03_s12": (
        "0:20. The whole paper in one sentence, and they have already asked for it. "
        "Walk down the three rows: passed along, a window, all at once.\n"
        "The bottom row is the paper. Everything after this is detail.\n"
        "Ask: how far apart are 'animal' and 'it'? Now how many steps?"
    ),
    "w03_s13": (
        "DISCUSSION (4-5 min). They know what attention is FOR, not how it works.\n"
        "Q1 -- fish for a long-range dependency: a pronoun far from its noun, a "
        "verb far from its subject. Our own title slide is one.\n"
        "Q2 -- fish for 'the other words', not 'the programmer'. This is the "
        "answer the next four slides spell out, so let them half-invent it.\n"
        "Q3 -- everyone jumps back. Nobody reads like an RNN. That is the point."
    ),
    "w03_s14": (
        "0:26. THE hard slide. Go slowly. Query = the question this word is asking. "
        "Key = the label each word wears. Value = what it hands over.\n"
        "Say 'same word, three jobs' out loud; that sentence is the whole of 3.2.\n"
        "Then the arrows -- 3b1b's picture. A question and a label are both vectors, "
        "and a label answers a question when the two line up. Let the keys swing in: "
        "'animal' lands nearly on top of the question, 'cross' points the other way. "
        "That IS the dot product; the next slide only writes the number down.\n"
        "Nobody wrote the questions -- W_Q, W_K, W_V are learned. If they ask what "
        "the question 'really' says: nothing in English. That is the honest answer."
    ),
    "w03_s14b": (
        "0:29. Where the three things COME FROM. One word's vector -- two numbers "
        "here, 512 in the paper -- goes through three lenses and comes out as a "
        "question, a label, and an offer. Read one product from the strip aloud: "
        "it is the perceptron again, a weighted sum per output number.\n"
        "Then 'it' through the same lenses. The same three matrices for every "
        "word and every sentence; they are the only thing attention learns.\n"
        "Land it: q of 'it' and k of 'animal' line up -- the arrows from the last "
        "slide, with numbers. The grid on the next slide does this for all 121 pairs."
    ),
    "w03_s15": (
        "0:30. The grid -- the same shape as every heatmap on Thursday: rows ask, "
        "columns answer -- and EVERY circle is a dot product of the numbers from the "
        "last slide. Read the worked one aloud: 0.55 times 1.08, 1.89 times 3.30, add "
        "them, 6.83, a big circle. Then 'cross': 1.07, a small one. That is the whole "
        "calculation, and it is Week 2's similarity arithmetic.\n"
        "Let the 'it' row build, then the other ten rows -- 121 dot products in one "
        "step. THAT is 'every word looks at every word', as a picture.\n"
        "If someone asks why 'animal' and 'street' light up their whole rows: long "
        "vectors make big products everywhere, which is exactly what the paper's "
        "divide-by-root-d_k is for. A two-number toy; the real ones are four slides away."
    ),
    "w03_s16": (
        "0:32. Softmax again -- third time this course -- but now on the grid, row by "
        "row. Watch the 'it' row: dots become shares, and the numbers in the cells "
        "add to 100 -- animal 61, street 23, tired 8. Then every row at once, and the "
        "'= 1' down the right.\n"
        "The line that matters: attention is a BUDGET. Total is always 1, so "
        "looking hard at one word means looking less hard at everything else. "
        "That is why a head with nothing to say still dumps weight somewhere, "
        "which they will see for real on Thursday.\n"
        "Last line plants the mask: nothing goes to zero here. s22 is where something does."
    ),
    "w03_s17": (
        "0:35. The payoff, and the value finally has a job: each word OFFERS "
        "something, and 'it' adds those offers in its attention's proportions. Call "
        "it the nudge. Then the arrow on the right: 'it' arrived short and generic, "
        "the nudge is ADDED to it, and it swings to point where 'animal' points -- a "
        "vector that exists only in this sentence.\n"
        "Say 'added, not written over'. That is the residual; s25's 'add + "
        "normalise' will mean exactly this.\n"
        "Then land the callback hard: this is what word2vec could NOT do. Bank on "
        "a river and bank in a city, Week 2, one vector for life.\n"
        "The formula in the band is the one s11 left as a question mark. Point at it.\n"
        "SG: static-vs-contextual-embeddings · polysemy."
    ),
    "w03_s17b": (
        "0:38. The slide the whole morning was for. Same word, same question, two "
        "sentences that differ in their last word. In one, 'animal' wins and the "
        "vector lands among creatures; in the other, 'street' wins and it lands "
        "among roads. Read the neighbour lists aloud -- that is the Week 2 test "
        "for what a vector means, applied to a vector that moved.\n"
        "Say it plainly: nothing about 'it' was looked up. Its meaning is where "
        "the vector ended up, and the words around it put it there. That is what "
        "'contextual embedding' means and nothing more.\n"
        "Illustrative and the slide says so.\n"
        "SG: static-vs-contextual-embeddings · polysemy · nearest-neighbours."
    ),
    "w03_s18": (
        "DISCUSSION (5 min). The mechanism is complete; now make them own it.\n"
        "Q1 -- fish for anything context-dependent: bank, pitch, sarcasm, "
        "pronouns. Week 2 could not tell any of them apart.\n"
        "Q2 -- the corpus. Same trick as word2vec: predict text, keep the "
        "weights. If nobody gets there, ask who wrote the labels.\n"
        "Q3 is the semester's argument and does not resolve today. Let it run "
        "for two minutes, then say so plainly and move."
    ),
    "w03_s19": (
        "0:42. All four heads are MEASURED, in the model they open on Thursday. "
        "Say that -- it is why the lab exists.\n"
        "5-0 does the coreference our title slide asked about, at 0.87. 3-1 does "
        "nothing but look left. Two useful, two plumbing.\n"
        "Reproduce: notebooks/w03-thu-translation.ipynb section 5 -- the optional\n"
        "deep dive, not the main lab. Say so if anyone asks."
    ),
    "w03_s20": (
        "0:46. The trap: if everything sees everything at once, order is gone -- "
        "attention only scores PAIRS of words, so 'dog bites man' and 'man bites "
        "dog' would give the identical grid. Let them feel the Week 2 regression "
        "before the fix.\n"
        "Fix: a stamp per position, ADDED to the word before attention sees it. "
        "The table is the stamp itself -- six of the 512 numbers, computed from "
        "the paper's sinusoids (Section 3.5), one column under each word. Point at "
        "two columns: no two alike, so 'dog' at 2 and 'dog' at 5 are now different "
        "vectors. That is the whole fix.\n"
        "SG: bag-of-words (callback)."
    ),
    "w03_s21": (
        "DISCUSSION (4 min). Two design choices, both arguable.\n"
        "Q1 -- there is no agreed answer. Interpretability research has been "
        "trying to name heads for years. Say that; it licenses uncertainty.\n"
        "Q2 -- 'patch' is a defensible answer and later models did change it. "
        "Reward whoever argues it, do not correct them.\n"
        "Q3 is the check on the whole morning: if they can explain word order "
        "to a friend, Week 2 and Week 3 have connected."
    ),
    "w03_s22": (
        "0:52. Three beats, staged the way 3b1b stages it. One: scores exist for "
        "every pair, including words not yet written -- and some of the biggest sit "
        "there, which is the whole problem. Two: stamp minus infinity on those "
        "BEFORE the softmax. Three: after it they are exactly zero. Not small. Zero.\n"
        "It is s15's grid again -- rows are the word being written -- so the "
        "triangle is above the diagonal, as it is in both Thursday notebooks.\n"
        "Why: without it the model reads the answer while learning to write it, "
        "and learns nothing."
    ),
    "w03_s23": (
        "0:56. The bridge, and the best picture in the deck. Follow the two yellow "
        "lines: German puts the verb at the end, so 'gekauft hat' reaches back "
        "nine words to 'bought', in one step.\n"
        "That distance is exactly what the RNN could not carry.\n"
        "Measured, layer 3 head 4. SG: encoder-and-decoder · sequence-to-sequence."
    ),
    "w03_s24": (
        "DISCUSSION (5 min). The best set in the deck.\n"
        "Q1 -- distance costs the transformer NOTHING in steps, but it pays in "
        "compute: every pair of words is scored, so a sentence twice as long costs "
        "four times as much. That is the trade the paper made, and the reason "
        "context windows have a size.\n"
        "Q2 is the prize and nobody sees it coming -- training is parallel, "
        "GENERATION is not. It still writes one token at a time, which is why "
        "every chatbot they have used types at them word by word.\n"
        "Q3 -- when reading, the whole input already exists."
    ),
    "w03_s25": (
        "1:03. Deflate it: four steps, stacked six times, and that is the model.\n"
        "'Add + normalise' in plain terms -- keep the original, add what was just "
        "learned. Nothing is ever fully overwritten, which is why you can stack "
        "six of them without the signal dying."
    ),
    "w03_s26": (
        "1:07. The honest answer to 'why did this win'. Not cleverness -- shape. "
        "A GPU does thousands of things at once and nothing in order.\n"
        "Everything since 2017 is downstream of this one column of Table 1."
    ),
    "w03_s27": (
        "1:11. The slide to be strict about. Four beats, in order.\n"
        "One: two sentences that differ in one word, and every reader resolves "
        "'it' differently -- trophy in the first, suitcase in the second. The blue "
        "arcs are the room, not the model.\n"
        "Two: German makes the model commit. Trophy is die (she), suitcase is der "
        "(he). It wrote 'sie' both times: right, then WRONG.\n"
        "Three: the yellow lines. While writing 'sie' the cross-attention pointed "
        "at 'it' -- 0.58 and 0.61 -- and at neither noun, in either sentence.\n"
        "Four: so the attention picture is the same for the right answer and the "
        "wrong one. Whatever decided the gender is not in these weights.\n"
        "Both numbers reproduce in notebooks/w03-thu-translation.ipynb, section 6."
    ),
    "w03_s29": (
        "DISCUSSION (5 min). Last stop.\n"
        "Q1 is an open research question. Say so -- they should leave knowing "
        "the field does not have this one either.\n"
        "Q2 has teeth: they have just watched an attention picture fail to "
        "explain a wrong answer. Push for a specific answer, not 'less'.\n"
        "Q3 is the closer. Genuinely new: every word reaching every word at "
        "once. Old and rewired: embeddings, softmax, layers, the dot product. "
        "If they can sort that list, the whole day has landed."
    ),
    "w03_s28": (
        "1:16. Close the ledger they opened at s11: all three ticked, each by a "
        "slide they can name.\n"
        "Last line: Thursday they open this model themselves and find their own "
        "version of s27. Tell them to come with one thing.\n"
        "SG: encoder-and-decoder · static-vs-contextual-embeddings."
    ),
    # Week 6 -- for students with no programming or math background. Every
    # term gets its own slide before it is used; the Appendix C math is backup
    # after the close (s46-s49). Numbers in these notes are the papers'.
    "w06_s01": (
        "Cold open is the next slide. One line here: this technique is in every "
        "prompting guide, and today we read the people who sell it, the people who "
        "invented it, and the people who doubt it.\n"
        "Session: Chain-of-Thought -- and Whether It Is Real (w06-tue)."
    ),
    "w06_s02": (
        "Let them read Figure 1 before you say anything. Then: same model, same "
        "question; the ONLY difference is one worked example in the prompt.\n"
        "Land the third note -- it is the whole day's question.\n"
        "Ask: who has typed 'show your working' into a chatbot? Did it help?"
    ),
    "w06_s03": (
        "Five parts. Part 3 exists because the critique is unreadable without "
        "about a dozen words; nobody is expected to know them yet.\n"
        "The 'reasoning' box: ask them to jot, as they go, each time a slide or a "
        "reading uses the word, and whether anyone defines it. They will need the "
        "list for the debate."
    ),
    "w06_s04": (
        "The one mechanical fact the whole technique rests on. A model writes one "
        "token at a time and re-reads EVERYTHING before the next -- including what "
        "it just wrote. So 'show your working' is not a metaphor: the working is "
        "more input.\n"
        "The bars are illustrative (the slide says so). The point is the last "
        "stop: with '3 + 6 =' already written, '9' is an easy next word.\n"
        "SG: token-and-tokenization · training-and-inference · softmax (Week 2 review)."
    ),
    "w06_s05": (
        "Vocabulary on one prompt. A 'shot' is one worked example; each is an "
        "exemplar. Few-shot CoT = the exemplars show their working.\n"
        "The Roger / cafeteria pair is Wei's own Figure 1.\n"
        "SG: few-shot-prompting · chain-of-thought-prompting."
    ),
    "w06_s06": (
        "Wei's definition, verbatim (§2). Two things to stress: (1) the whole "
        "technique is eight hand-written exemplars (Appendix Table 20) -- no "
        "retraining; (2) the chain comes BEFORE the answer, which is why they did "
        "not call it an explanation (§2: explanations 'typically come after').\n"
        "SG: chain-of-thought-prompting."
    ),
    "w06_s07": (
        "Wei §2's four 'attractive properties', quoted. Point at the hedges: "
        "'in principle', 'at least in principle', 'sufficiently large', and "
        "claim 2's own parenthesis that characterizing the computation 'remains "
        "an open question'.\n"
        "Claim 1 is tested by Wei's ablation (Part 2); claim 2 by Zhao (Part 4).\n"
        "Ask: which of these would a vendor page leave the hedge off?"
    ),
    "w06_s08": (
        "Zero-shot CoT: Kojima et al. 2022 ('Let's think step by step'), cited in "
        "Zhao §2.1. AWS and IBM both list zero-shot CoT; the quoted instructions "
        "are theirs.\n"
        "Reasoning models (the o-series, DeepSeek-R1 and kin): the chain is now "
        "trained in, so students meet CoT whether or not they ask for it.\n"
        "SG: chain-of-thought-prompting · few-shot-prompting."
    ),
    "w06_s09": (
        "One slide, not a lecture: each variant keeps the chain and changes how "
        "many or what shape. Self-consistency's 74% is from the Google blog "
        "('follow-up work on self-consistency'). Least-to-most is on the AWS "
        "page; tree of thoughts in Zhao §2.1 and IBM's navigation.\n"
        "Don't linger -- none of these is tested today."
    ),
    "w06_s10": (
        "The take-home recipe. Every line has a source: one-step problems gained "
        "little (Wei Table 3, SingleOp); CoT made every model under ~10B worse "
        "(Table 2); cost (IBM, AWS). The 'Check' line previews Part 4.\n"
        "The banana prompt is the AWS reading's own example; the chain in yellow "
        "is worked by hand, not a model output.\n"
        "Ask: what's a problem from another class where you'd use this?"
    ),
    "w06_s11": (
        "DISCUSSION (4-5 min). Q1: incentives -- a vendor sells capability; a "
        "paper is judged on what it can defend. Q2: fish for 'you can see where "
        "it went wrong' -- then ask whether seeing the chain shows you the cause "
        "(Part 4 will). Q3: IBM repeats 'think out loud' and 'emergent'; the "
        "hedges ('open question', 'in principle') are gone.\n"
        "Don't resolve Q2. It comes back at s37."
    ),
    "w06_s12": (
        "Benchmark vocabulary. GSM8K: ~8,500 grade-school problems (Cobbe et al. "
        "2021).\n"
        "The 58% lesson: Google's blog figure uses an external calculator (the "
        "blog says so: 'for a fair comparison against fine-tuned GPT-3 "
        "baselines'). Model alone: 56.9 (Table 2); with calculator 58.6 (Table 1).\n"
        "SG: benchmark."
    ),
    "w06_s13": (
        "Wei Table 2, GSM8K, redrawn. Below ~10B parameters CoT made EVERY model "
        "worse (GPT 350M: 2.2 -> 0.5; PaLM 8B: 4.9 -> 4.1; LaMDA the same). Above "
        "~100B it pays hugely.\n"
        "'Emergent' = absent, then present, above some size. Wei §3.2: smaller "
        "models 'produced fluent but illogical chains of thought' -- worth "
        "flagging; Side B will use it.\n"
        "SG: emergent-abilities · parameters-and-weights."
    ),
    "w06_s14": (
        "Ablation, first on a cake. The rule: change one thing at a time against "
        "a control. Then the same grid for Wei's five prompts.\n"
        "Reading of the grid: no single ingredient does it -- equations, words "
        "and length-before-answer only work together.\n"
        "SG: ablation-study."
    ),
    "w06_s15": (
        "Hold the figure up before explaining it: this is the one they skimmed. "
        "Walk the five prompts down the right. Only the text before 'The answer "
        "is 11' changes -- that is the whole design.\n"
        "Reading: Wei §3.3, Figure 5. The worked problem is theirs (Figure 1); "
        "the five answer lines illustrate each condition.\n"
        "Ask: which of these do you expect to work?"
    ),
    "w06_s16": (
        "Each story appears with no bar. PAUSE and let the room guess before it "
        "grows. Equation only: ~22 vs 17.9. Dots: flat. Reasoning after the "
        "answer: flat -- so the chain has to come BEFORE the answer to help.\n"
        "The ≈ bars are read off Figure 5; the paper tabulates ablations for "
        "LaMDA only (Table 6: 6.5 / 5.4 / 6.4 / 6.1 / 14.3). Say so -- reading a "
        "figure is legitimate if you admit it.\n"
        "Land the last line: three stories ruled out is not the fourth proved."
    ),
    "w06_s17": (
        "§6, quoted. The inventors decline to say 'reasoning'. The hand check "
        "(§3.2): of 50 correct LaMDA 137B answers, 48 chains sound, 2 right by "
        "coincidence. Of 50 WRONG answers, 46% of chains were almost right, 54% "
        "had major errors.\n"
        "Note for later: reading a chain and finding it sound is not the same "
        "as showing the model used it (s41 Q3).\n"
        "SG: chain-of-thought-prompting."
    ),
    "w06_s18": (
        "DISCUSSION (5 min) -- the session's own questions 2 and 3. Q1: push for "
        "something observable, not a definition. Q3 is the intervention idea: "
        "corrupt a middle step and see if the answer follows. Zhao §2.2 cites "
        "work doing exactly this (Lanham et al. 2023) that found answers often "
        "do NOT change -- don't reveal it; let them propose it.\n"
        "Transition: to test any of this you need Part 3's words."
    ),
    "w06_s19": (
        "The question-space picture is a picture, not data (footer says so). "
        "Axes chosen so a student can place their own homework problem.\n"
        "Distribution = what kinds of example, how often. Test data drawn from "
        "the same cloud = in-distribution.\n"
        "SG: training-and-test-distributions · corpus."
    ),
    "w06_s20": (
        "Watch the test cloud slide away: that movement is 'distribution shift'. "
        "Red stars: out-of-distribution.\n"
        "The key distinction: generalizing to new questions of the SAME kind is "
        "expected; to new KINDS is the contested case, and today's argument.\n"
        "The three shifts are Zhao's axes, in homework terms. They come back as "
        "the three dials (s31).\n"
        "SG: out-of-distribution-generalization."
    ),
    "w06_s21": (
        "Data leakage / benchmark contamination. The exam-posted-online analogy "
        "does the work.\n"
        "Be even-handed: this is why Zhao build their own data (§1: pretrained "
        "models 'suffer from data leakage'), and it is an open question -- not "
        "an accusation -- for Wei's GSM8K results.\n"
        "SG: data-leakage · benchmark."
    ),
    "w06_s22": (
        "Three ways to meet a task, then the size strip. Zhao's from-scratch "
        "models: 62K-3B (Table 8), GPT- and LLaMA-style; real-model check: "
        "LLaMA3-8B and Qwen3-14B-Instruct, fine-tuned on DataAlchemy (§8.2). "
        "Wei: up to PaLM 540B.\n"
        "The x180 gap is the heart of Side A's size objection; the fine-tuned "
        "8B/14B results are Zhao's answer to it.\n"
        "SG: pretraining-and-fine-tuning · parameters-and-weights."
    ),
    "w06_s23": (
        "Week 2 review: logits, divided by T, then softmax. Watch the bars "
        "sharpen (cold) and flatten (hot).\n"
        "Why it's here: Zhao run at T = 1e-5 (F.1) and re-ran from 1e-5 to 10 "
        "(D.5) to rule out 'it's just the decoding setting' -- a control, like "
        "Wei's ablation. Same pattern up to T = 1; at 10 'essentially uniform "
        "sampling'.\n"
        "SG: temperature · softmax · logits."
    ),
    "w06_s24": (
        "The answer is real: Appendix E.1.1, truth HUSP, model HFCU.\n"
        "Exact match: all or nothing. Edit distance (Levenshtein): 3 changes "
        "(F->U, C->S, U->P); the paper reports it scaled 0-1. BLEU: shared short "
        "runs, from machine translation; don't compute it, just the idea.\n"
        "The paper scores reasoning, answer and full chain separately -- that "
        "split is what makes s37 possible.\n"
        "SG: exact-match-and-edit-distance."
    ),
    "w06_s25": (
        "The hypothesis (§3), verbatim, then glossed phrase by phrase. 'Inductive "
        "bias' = a learned lean. The one-sentence version is the thing to "
        "remember.\n"
        "Note the parenthesis in the paper: effectiveness is governed by "
        "distribution discrepancy 'rather than by model architecture or scale' "
        "-- a strong claim, and the one s22/s38 bear on."
    ),
    "w06_s26": (
        "Why a toy: you cannot test 'outside the training data' on a model whose "
        "training data is secret. So build the data.\n"
        "Don't read Figure 2 panel by panel -- the next slide runs it.\n"
        "Ask: what do you give up by using letters instead of language?"
    ),
    "w06_s27": (
        "APPLE is the paper's example. ROT13: count 13 on from A, land on N. "
        "Shift: the A wraps round. Then the CoT format exactly as trained: the "
        "middle step, the operation still to do, the answer.\n"
        "Here every step has one right answer -- fully checkable, which Wei's "
        "math problems could not give.\n"
        "Notation warning for keen readers: the paper's 'f1 ∘ f2' means f1 "
        "FIRST, the reverse of the usual convention."
    ),
    "w06_s28": (
        "Equations (1)-(3). Start with the four practice questions; the math is "
        "just that average, written generally. Walk each coloured term.\n"
        "Hat = measured on a sample. 𝔼 = the true average over the whole "
        "distribution. The paper's question in one line at the end.\n"
        "Cross-entropy (the paper's example loss) need not be named.\n"
        "SG: loss-and-risk."
    ),
    "w06_s29": (
        "TV distance with bars. Mild example first: TV = 0.4. Show the 'sup' "
        "reading with A = first two kinds: 0.7 vs 0.3.\n"
        "Then morph to the composition test (train on three kinds, test only on "
        "the fourth): TV = 1, the maximum. Tell them to remember the number -- "
        "the next slide needs it.\n"
        "SG: total-variation-distance."
    ),
    "w06_s30": (
        "Theorem 3.1, term by term. It is a CEILING ('at most'), not a "
        "prediction.\n"
        "The numbers are illustrative (B=1, n=10,000, delta=0.05, practice "
        "penalty 0.02; sampling term 0.012). Past Δ ≈ 0.48 the ceiling exceeds "
        "the worst possible penalty, so it rules nothing out; at Δ = 1 -- the "
        "OOD tests -- it is 2.03.\n"
        "Pose it as a question, not a gotcha: the theorem motivates the lens; "
        "the experiments carry the evidence. This is s40 Q3.\n"
        "SG: generalization-bound."
    ),
    "w06_s31": (
        "Equation (7): three dials combined by some increasing function Φ. The "
        "paper never picks Φ -- it only requires 'turning any dial up never "
        "turns the total down'.\n"
        "Each dial gets its own measure in Appendix C: backup slides s46-s48. "
        "Skip them unless asked.\n"
        "SG: out-of-distribution-generalization."
    ),
    "w06_s32": (
        "The four task tests on the paper's own lines (Appendix B.2.1), for APPL. "
        "Let them predict each before the next slide.\n"
        "CMP = operations it knows in a new order; POOD = one never-seen "
        "operation; OOD = nothing seen.\n"
        "Ask: which would YOU get right, given only the practice lines?"
    ),
    "w06_s33": (
        "Let each row grow before reading it. ID perfect; CMP 0.01% (LLaMA3-8B "
        "manages 8.52%); POOD and OOD zero for all.\n"
        "Pre-empt 'tiny models': Table 5 is two real pretrained models, "
        "fine-tuned, on the same cliff. But the task is still letters, not "
        "language (Limitations (i)) -- and Wei's ablation said words mattered.\n"
        "Reading: §5.1 Table 1; Appendix D.7 Table 5."
    ),
    "w06_s34": (
        "Figure 4: mix a tiny share of the new task into fine-tuning. By ~4e-4 "
        "(four in ten thousand) every curve is near the top; CMP recovers first, "
        "OOD last.\n"
        "Interpolation vs extrapolation: define both, they return in s38.\n"
        "Two readings, genuinely open: 'a patch, not a panacea' (App. G) vs "
        "'that is what learning looks like'. Don't pick one."
    ),
    "w06_s35": (
        "Length, two ways. Text length (Table 4): 100% at the trained length 4, "
        "0% at 2, 3, 5 and 6. The IGLLQ example (E.2.1) squeezes five letters "
        "into four.\n"
        "Steps (Figure 6, E.2.2): trained on two-step chains, asked for one, it "
        "pads the chain back to two -- and so gets AABD, not NNOQ.\n"
        "Both examples are quoted from Appendix E and checked by script."
    ),
    "w06_s36": (
        "Format: insert / delete / modify one token (Appendix B.4). Figure 7: "
        "insertion hurts most; noise in the letters and operations matters, noise "
        "elsewhere less.\n"
        "E.3: one operation deleted from the prompt, and the model pads its "
        "answer to the practiced length (NGNGY for NNNG).\n"
        "Ask: what's the everyday version -- a typo in your prompt?"
    ),
    "w06_s37": (
        "The finding the debate can use. The HUSP output is quoted from E.1.1. "
        "First step right; then it writes [F2] because f2 always came second in "
        "training, and does f2. Its answer follows from its own wrong step.\n"
        "Table 2: rows 1-2 every step right, answer wrong; rows 3-4 steps wrong, "
        "answer right -- possible only because f1 and f2 commute (APPLE both "
        "ways, on the slide).\n"
        "Tie back to s07 claim 2 and s11 Q2: how much is the window worth?\n"
        "SG: chain-of-thought-faithfulness."
    ),
    "w06_s38": (
        "Zhao's controls -- the same logic as Wei's ablation, aimed at the "
        "failure. Temperature (D.5), size and architecture (§8.1, Table 8), real "
        "models (§8.2, Table 5).\n"
        "The D.5 quote is their own summary on scale: bigger models interpolate "
        "faster, not extrapolate further. Side B's best line on size."
    ),
    "w06_s39": (
        "Their verdict (App. G), verbatim, and their implications -- 'fluent "
        "nonsense' is worth repeating.\n"
        "Then their own first limitation, verbatim.\n"
        "Last line is a question, not a verdict: the experiments show fragility "
        "under shift; the conclusion says what CoT 'is not'. Let the room decide "
        "whether the second follows from the first."
    ),
    "w06_s40": (
        "Questions for the critique -- none has an agreed answer. Q1 and Q2 are "
        "Side A's; Q3-Q4 are about what the theorem can carry (s30, backup s49); "
        "Q5 asks what 'genuine reasoning' would even do in the toy.\n"
        "Don't answer them. They're debate material."
    ),
    "w06_s41": (
        "Same scrutiny for Wei. Q1 leakage (s21). Q2 the window (s37). Q3: a "
        "chain that READS correctly vs one the model USED. Q4: the intervention "
        "experiment -- if nobody proposed it at s18, give them the Lanham et al. "
        "2023 result here (Zhao §2.2: answers often unchanged when steps are "
        "corrupted)."
    ),
    "w06_s42": (
        "Practical synthesis both sides accept. Each line maps to evidence: "
        "familiar problems (both papers), chain is not an audit trail (s37), "
        "test odd cases (Zhao App. G 'Prioritize OOD testing'), expert checks "
        "(App. G), and the ADR habit from the project.\n"
        "SG: chain-of-thought-prompting."
    ),
    "w06_s43": (
        "STRUCTURED DEBATE (~20 min). Split the room. Suggested: 4 min prep, 2 "
        "min opening each, 8 min open floor, 1 min closing each.\n"
        "Enforce the two rules: every claim cites a slide or section; each side "
        "concedes one point. Anyone who says 'reasoning' defines it first -- "
        "that rule alone is most of the lesson.\n"
        "Wei §6 is enough to argue from; the mirage paper was optional."
    ),
    "w06_s44": (
        "DISCUSSION (5 min) -- session question 4 plus two. Q2 is the deepest: "
        "if people also generalize from what they have practiced, is the "
        "dichotomy real? Q3: have them write it down -- Thursday's lab asks for "
        "it before they run anything."
    ),
    "w06_s45": (
        "Close the ledger: every term on the left had its own slide. Thursday: "
        "the lab builds the experiment -- tasks inside and outside the "
        "distribution, CoT vs direct, a prediction written first. Read out the "
        "one-finding template.\n"
        "Backup slides follow; stop here unless someone asks about Appendix C."
    ),
    "w06_s46": (
        "BACKUP -- Appendix C.1. The counting in eq. (14), then eq. (18): each "
        "novelty multiplies success by a fraction rho. Halving is the "
        "illustration.\n"
        "Honest notes: the multiplicative, independent-failure model is ASSUMED; "
        "the rho values are never measured. And the 'threshold' tau = ln(pi_0)/"
        "kappa is never positive (pi_0 <= 1), so eq. (17) holds for every task -- "
        "the threshold is trivially met."
    ),
    "w06_s47": (
        "BACKUP -- Appendix C.2, eq. (22). The paper calls it 'a modeling "
        "ansatz': an assumed shape with sigma fitted, not derived (their "
        "heuristic derivation follows it).\n"
        "Against Table 4: exact match is a cliff (fit needs a tiny sigma); edit "
        "distance rises gently. Which shape you see depends on the metric."
    ),
    "w06_s48": (
        "BACKUP -- Appendix C.3. Format distance is 1 minus the cosine similarity "
        "to the nearest training prompt's embedding -- Week 2's cosine, reused. "
        "Appendix C.3 does not name the embedding function eta.\n"
        "SG: cosine-similarity · embedding."
    ),
    "w06_s49": (
        "BACKUP -- Appendix C.4. Split the gap into (i) a shift term, bounded by "
        "TV (their 2B is a loose constant), and (ii) a sampling term, bounded by "
        "Hoeffding -- shown as coin flips settling inside a narrowing band.\n"
        "The point for s40 Q4: nothing here mentions chains of thought; it is a "
        "standard result that holds for any model on any task.\n"
        "SG: generalization-bound."
    ),
}


def _layout_notes_page(notes_slide, note_text):
    """Write the note, pinning the font size and touching nothing else.

    Hard-won constraint: Microsoft PowerPoint drops the slide image from a
    notes page if the sldImg placeholder carries a local <a:xfrm> it did not
    write itself — schema-legal, verified empirically. So geometry is left to
    inherit from the notes master, exactly as PowerPoint expects; the only
    intervention is an explicit 12pt run size so text renders predictably.
    The blank-slide-when-printing problem is solved by the print edition
    (final frames as stills), not by touching this layout.
    """
    notes_slide.notes_text_frame.text = note_text
    for para in notes_slide.notes_text_frame.paragraphs:
        for run in para.runs:
            run.font.size = Pt(12)


def _build(files, out_path, print_edition=False):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    for path in files:
        if print_edition and path.endswith(".gif"):
            path = path.replace(".gif", "_final.png")
        slide = prs.slides.add_slide(blank)
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = BG
        slide.shapes.add_picture(path, 0, 0, width=prs.slide_width, height=prs.slide_height)
        key = "_".join(os.path.basename(path).split("_")[:2])
        note = NOTES.get(key)
        if note:
            _layout_notes_page(slide.notes_slide, note)

    prs.save(out_path)
    print(f"saved {out_path} ({len(files)} slides, {os.path.getsize(out_path) / 1e6:.1f} MB)")


def main():
    for deck in DECKS:
        ordered = [os.path.join(PHOTOS, f) for f in deck.order]
        finals = [f.replace(".gif", "_final.png") for f in ordered if f.endswith(".gif")]
        missing = [f for f in [*ordered, *finals] if not os.path.exists(f)]
        if missing:
            raise SystemExit(
                "missing media (run the gen scripts first): "
                + ", ".join(os.path.basename(f) for f in missing)
            )
        extra = sorted(
            os.path.basename(f)
            for f in glob.glob(os.path.join(PHOTOS, f"{deck.prefix}_s*.*"))
            if not f.endswith(("_final.png", "_preview.png"))
            and os.path.basename(f) not in deck.order
        )
        if extra:
            raise SystemExit(f"media not listed in {deck.prefix.upper()}_ORDER (add them): {extra}")

        # Animated deck for presenting; print edition (final frames as stills)
        # for Notes Page printing and handouts, where GIFs show their first,
        # nearly-empty frame.
        _build(ordered, os.path.join(SCRIPT_DIR, f"{deck.stem}.pptx"))
        _build(ordered, os.path.join(SCRIPT_DIR, f"{deck.stem}_print.pptx"), print_edition=True)


if __name__ == "__main__":
    main()
