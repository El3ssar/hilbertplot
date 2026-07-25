"""Word generation: known landmark words, lengths, and the memoisation cache."""

import pytest

import hilbertplot as hp
from hilbertplot._core.geometry import word_to_codes
from hilbertplot._core.generation import clear_cache, curve_codes, curve_word, word_length


def test_hilbert_order_2_matches_paper():
    # The canonical Hilbert curve word quoted in the paper (0H2).
    assert curve_word(0, 2) == "ruluurdrurddldr"


def test_hilbert_order_1():
    assert curve_word(0, 1) == "urd"


def test_order_zero_is_empty_for_all_curves():
    for c in hp.catalog():
        assert c.word(0) == ""


@pytest.mark.parametrize("order", range(0, 8))
def test_word_length_invariant(order):
    for c in hp.catalog():
        assert len(c.word(order)) == word_length(order) == 4**order - 1


def test_words_only_use_four_letters():
    for c in hp.catalog():
        assert set(c.word(4)) <= set("udlr")


def test_negative_order_rejected():
    with pytest.raises(ValueError):
        curve_word(0, -1)
    with pytest.raises(ValueError):
        word_length(-1)
    with pytest.raises(ValueError):
        curve_codes(0, -1)


@pytest.mark.parametrize("index", [0, 5, 12, 39])
def test_codes_agree_with_word(index):
    # The fast numpy-code path must produce exactly the same strokes as the word.
    for order in range(0, 6):
        codes = curve_codes(index, order)
        assert list(codes) == list(word_to_codes(curve_word(index, order)))


def test_high_order_generation(index=0):
    # Exercise the fast path at scale: a million-stroke curve stays space-filling.
    from hilbertplot._core.geometry import is_space_filling

    pts = hp.curve(0).points(10)
    assert pts.shape == (4**10, 2)
    assert is_space_filling(pts, 10)


def test_cache_clear_is_safe():
    curve_word(5, 6)
    clear_cache()
    # still correct after clearing
    assert curve_word(0, 2) == "ruluurdrurddldr"
