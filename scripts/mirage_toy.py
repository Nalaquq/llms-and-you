"""DataAlchemy's two operations, and every model output the Week 6 deck quotes.

Zhao et al. build their toy world from 26 letters and two operations (§4.2):
f1 is ROT13, f2 a one-place cyclic shift. The slides compute every string
they show from these functions rather than typing it, and every model output
they quote from the paper's Appendix E is checked here against the paper's
stated ground truth on import. A deck that a room checks by hand cannot carry
a typo in a rotation.

The paper writes a composition as "f1 ∘ f2" and means *f1 first, then f2* --
the reverse of the usual mathematical convention, and the order its prompt
tokens are written in ("[F1] [F2]"). The slides avoid the ∘ and say "then".
"""


def f1(s):
    """ROT13: every letter 13 places on, wrapping (Definition 4.1, n = 13)."""
    return "".join(chr((ord(c) - 65 + 13) % 26 + 65) for c in s)


def f2(s):
    """Cyclic position shift: every letter one place left (Definition 4.2, n = 1)."""
    return s[1:] + s[:1]


OPS = {"F1": f1, "F2": f2}


def chain(word, ops):
    """The full chain of thought for `word` under `ops`, in the paper's token format.

    Returns (prompt tokens, response tokens): each intermediate result, then the
    operation still to do, then <answer> and the final result -- Appendix B.
    """
    prompt = [*word, *(f"[{o}]" for o in ops), "<think>"]
    response, cur = [], word
    for i, o in enumerate(ops):
        cur = OPS[o](cur)
        if i < len(ops) - 1:
            response += [*cur, f"[{ops[i + 1]}]"]
    return prompt, [*response, "<answer>", *cur]


WORD = "APPLE"
assert f1(WORD) == "NCCYR" and f2(WORD) == "PPLEA"  # the paper's own worked examples
assert f1(f2(WORD)) == f2(f1(WORD))  # the two commute -- Table 2 rows 3-4 turn on this

# Appendix B.2.1 uses APPL; check its training line is what chain() produces.
assert chain("APPL", ["F1", "F2"])[1] == [*"NCCY", "[F2]", "<answer>", *"CCYN"]

# Appendix E.1.1 -- trained on f1-then-f2 only, asked for f1-then-f1.
E11_QUERY, E11_MODEL = "HUSP", ("UHFC", "F2", "HFCU")
E11_TRUTH = (f1(E11_QUERY), "F1", f1(f1(E11_QUERY)))
assert E11_TRUTH == ("UHFC", "F1", "HUSP")
assert E11_MODEL[2] == f2(E11_MODEL[0])  # its answer follows from its own (wrong) step

# Appendix E.2.1 -- trained on 4-letter words, asked about a 5-letter one.
E21_QUERY, E21_MODEL = "IGLLQ", ("TYY", "TYYV")
assert (f1(E21_QUERY), f2(f1(E21_QUERY))) == ("VTYYD", "TYYDV")

# Appendix E.2.2 -- trained on two-step chains, asked for one step.
E22_QUERY, E22_MODEL = "AABD", ("NOAZNNOQ", "AABD")
assert f1(E22_QUERY) == "NNOQ"

# Appendix E.3 -- format change: one operation token deleted from the prompt.
E3_QUERY, E3_MODEL = "AAAT", "NGNGY"
assert f1(E3_QUERY) == "NNNG"
