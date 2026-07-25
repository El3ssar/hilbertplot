"""The morphisms must match the paper's letter tables exactly, and D4 must be a group."""

import itertools

import pytest

from hilbertplot._core.symmetry import (
    DIRECTIONS,
    IDENTITY,
    MORPHISMS,
    Symmetry,
    apply_morphism,
    reverse_word,
)

# The morphism letter tables printed in sections V and VII of the paper.
PAPER_TABLES = {
    "o": {"u": "r", "r": "u", "d": "l", "l": "d"},
    "a": {"u": "l", "r": "d", "d": "r", "l": "u"},
    "g": {"u": "l", "r": "u", "d": "r", "l": "d"},
    "x": {"u": "r", "r": "d", "d": "l", "l": "u"},
    "f": {"u": "d", "r": "l", "d": "u", "l": "r"},
    "m": {"u": "d", "r": "r", "d": "u", "l": "l"},
    "y": {"u": "u", "r": "l", "d": "d", "l": "r"},
}


@pytest.mark.parametrize("code,table", PAPER_TABLES.items())
def test_morphism_matches_paper(code, table):
    sym = MORPHISMS[code]
    for letter, expected in table.items():
        assert sym.apply_letter(letter) == expected


def test_identity_is_noop():
    for letter in DIRECTIONS:
        assert IDENTITY.apply_letter(letter) == letter


def test_d4_has_eight_distinct_elements():
    mats = {s.matrix for s in MORPHISMS.values()}
    assert len(mats) == 8


def test_d4_closed_under_composition():
    elements = list(MORPHISMS.values())
    mats = {s.matrix for s in elements}
    for a, b in itertools.product(elements, repeat=2):
        assert a.compose(b).matrix in mats


def test_every_morphism_is_a_bijection_on_letters():
    for sym in MORPHISMS.values():
        images = {sym.apply_letter(d) for d in DIRECTIONS}
        assert images == set(DIRECTIONS)


def test_reversion_example_from_paper():
    # The worked example on page 15.
    assert reverse_word("ruluurdrurddldr") == "luruuldlulddrdl"


def test_reversion_is_an_involution():
    for word in ("urd", "ruluurdrurddldr", "uu", ""):
        assert reverse_word(reverse_word(word)) == word


def test_reversion_equals_reverse_then_rot180():
    word = "ruluurdrurddldr"
    manual = MORPHISMS["f"].apply_word(word)[::-1]
    assert reverse_word(word) == manual


def test_apply_morphism_helper():
    assert apply_morphism("f", "ur") == "dl"


def test_composition_order():
    # s.compose(t) means "t after s" acting on vectors.
    s, t = MORPHISMS["g"], MORPHISMS["g"]
    v = (1, 0)
    assert s.compose(t).apply_vector(v) == t.apply_vector(s.apply_vector(v))
    # g composed with itself is a 180-degree rotation.
    assert s.compose(t).matrix == MORPHISMS["f"].matrix
