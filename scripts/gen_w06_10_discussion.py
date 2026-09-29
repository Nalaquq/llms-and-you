"""Week 6 discussion interstitials -- one at the end of each argument.

  w06_s11_discuss_vendors.gif   after part 1: the sellers and the inventors
  w06_s18_discuss_answer.gif    after part 2: what would an answer even look like?
  w06_s44_discuss_session.gif   after the debate: does it change how you use it?

Same furniture as Week 3's (gen_w03_09_discussion.make): questions only, no
hints on the slide, what the instructor is fishing for in the speaker notes.
The questions are the session's own (data/schedule.yml, w06-tue), plus the
ones the slides before each pause set up.
"""

from gen_w03_09_discussion import make

DISCUSSIONS = [
    (
        "w06_s11_discuss_vendors.gif",
        "The sellers and the inventors",
        "Same technique. Read how each describes it.",
        [
            "IBM: chain of thought “simulates human-like reasoning processes”. Wei et al.:\n"
            "their work “does not answer whether the neural network is actually\n"
            "‘reasoning’”. Why would the two describe the same result so differently?",
            "AWS calls it “more accurate and debuggable than standard prompting”.\n"
            "What would “debuggable” have to mean for that to be true?",
            "Which of Wei's four claims do the vendor pages repeat — and which of\n"
            "the hedges do they drop?",
        ],
        "readings: AWS · IBM · Wei et al. 2022 §2, §6 · study guide: chain-of-thought-prompting",
    ),
    (
        "w06_s18_discuss_answer.gif",
        "What would an answer even look like?",
        "Wei et al. leave the question open. Could you close it?",
        [
            "Wei et al. leave “whether the neural network is actually reasoning” as an\n"
            "open question. What would an answer even look like?",
            "What experiment would settle it? Could you run it — with what you\nhave, this week?",
            "Suppose you changed a step in the middle of the chain and the answer did\n"
            "not change. What would that tell you?",
        ],
        "reading: Wei et al. 2022 §6 · study guide: ablation-study · chain-of-thought-faithfulness",
    ),
    (
        "w06_s44_discuss_session.gif",
        "After the debate",
        "Last stop before Thursday.",
        [
            "If chain of thought works, but not for the reasons people say, does that\n"
            "change how you should use it?",
            "Is “pattern-matching” the opposite of reasoning — or a description of how\n"
            "people reason too?",
            "Name one result, from either paper or from Thursday's lab, that would\n"
            "change your mind. Write it down now.",
        ],
        "session: Chain-of-Thought — and Whether It Is Real (w06-tue) · study guide: "
        "out-of-distribution-generalization",
    ),
]


if __name__ == "__main__":
    for spec in DISCUSSIONS:
        make(*spec)
