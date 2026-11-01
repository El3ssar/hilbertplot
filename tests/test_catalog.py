"""The headline correctness theorem, plus catalogue metadata and lookups.

Proving two things about the whole catalogue -- that every curve is space-filling and
that the forty are pairwise distinct up to symmetry and reversion -- together with the
paper's completeness result (exactly forty exist) means the set we built is exactly
the complete set of two-dimensional Hilbert curves.
"""

import numpy as np
import pytest

from hilbertplot._core import curve as curves
from hilbertplot._core.geometry import canonical_form, is_space_filling


# --------------------------------------------------------------------------
# Completeness / correctness
# --------------------------------------------------------------------------
def test_catalog_has_forty_curves():
    assert len(curves.catalog()) == 40
    assert [c.index for c in curves.catalog()] == list(range(40))


@pytest.mark.parametrize("order", [1, 2, 3, 4, 5, 6])
def test_every_curve_is_space_filling(order):
    for c in curves.catalog():
        assert is_space_filling(c.points(order), 2**order), (
            f"{c.name} not space-filling at order {order}"
        )


@pytest.mark.parametrize("order", [3, 4, 5])
def test_all_forty_curves_are_pairwise_distinct(order):
    forms = {canonical_form(c.points(order)) for c in curves.catalog()}
    assert len(forms) == 40


# --------------------------------------------------------------------------
# Families / kernels (the homogeneous vs inhomogeneous split)
# --------------------------------------------------------------------------
def test_family_counts():
    assert len(curves.homogeneous()) == 12
    assert len(curves.inhomogeneous()) == 28
    assert len(curves.proper()) == 6
    assert len(curves.improper()) == 6


def test_homogeneity_follows_from_kernels():
    for c in curves.catalog():
        assert c.is_homogeneous == (len(c.kernels) == 1)


def test_proper_curves_use_hilbert_kernel_only():
    for c in curves.proper():
        assert c.kernels == {0}


def test_improper_curves_use_liu4_kernel_only():
    for c in curves.improper():
        assert c.kernels == {5}


def test_curve2_is_never_a_kernel():
    # Liu1 (2) has both endpoints interior; it cannot connect quadrants, so it is
    # never used as a building block.
    used = set().union(*(c.kernels for c in curves.catalog()))
    assert 2 not in used
    assert used == {0, 1, 3, 4, 5}


def test_inhomogeneous_groupings_match_paper():
    groups: dict[str, list[int]] = {}
    for c in curves.inhomogeneous():
        groups.setdefault(c.combination, []).append(c.index)
    counts = {k: len(v) for k, v in groups.items()}
    assert counts == {"3H+5H": 6, "0H+4H": 14, "1H+5H": 6, "1H+3H+5H": 2}


def test_named_proper_curves():
    names = [curves.curve(i).name for i in range(6)]
    assert names == ["Hilbert", "Moore", "Liu1", "Liu2", "Liu3", "Liu4"]


# --------------------------------------------------------------------------
# Closed curves (Table 3)
# --------------------------------------------------------------------------
@pytest.mark.parametrize("index", [1, 2, 6, 9])
def test_closed_curves_have_adjacent_endpoints(index):
    c = curves.curve(index)
    assert c.is_closed
    pts = c.points(5)
    assert int(np.abs(pts[0] - pts[-1]).sum()) == 1


def test_exactly_four_closed_curves():
    assert {c.index for c in curves.closed()} == {1, 2, 6, 9}


# --------------------------------------------------------------------------
# Entry/exit point geometry (Table 3) -- an independent check on the
# homogeneous curves, orthogonal to the space-filling property.
# --------------------------------------------------------------------------
_TABLE3_ENDPOINTS = {
    0: ("corner", "corner"),
    1: ("edge", "edge"),
    2: ("interior", "interior"),
    3: ("edge", "edge"),
    4: ("corner", "interior"),
    5: ("edge", "edge"),
    6: ("interior", "interior"),
    7: ("interior", "edge"),
    8: ("edge", "edge"),
    9: ("interior", "interior"),
    10: ("edge", "edge"),
    11: ("edge", "interior"),
}


def _endpoint_type(cell, side):
    x, y = int(cell[0]), int(cell[1])
    on = (x in (0, side - 1)) + (y in (0, side - 1))
    return ("interior", "edge", "corner")[on]


@pytest.mark.parametrize(("index", "expected"), _TABLE3_ENDPOINTS.items())
def test_entry_exit_types_match_table3(index, expected):
    order = 4
    side = 2**order
    pts = curves.curve(index).points(order)
    got = sorted((_endpoint_type(pts[0], side), _endpoint_type(pts[-1], side)))
    assert got == sorted(expected)


# --------------------------------------------------------------------------
# Lookups / API surface
# --------------------------------------------------------------------------
def test_get_by_index_and_name():
    assert curves.curve(0).name == "Hilbert"
    assert curves.curve("moore").index == 1
    assert curves.curve("Hilbert") is curves.curve(0)


def test_get_invalid():
    with pytest.raises(IndexError):
        curves.curve(40)
    with pytest.raises(KeyError):
        curves.curve("nope")


def test_by_kernels_filter():
    assert {c.index for c in curves.by_kernels(3, 5)} == {12, 13, 14, 15, 16, 17}
    assert {c.index for c in curves.by_kernels(0)} == {0, 1, 2, 3, 4, 5}


def test_curve_word_and_points():
    assert curves.curve(0).word(2) == "ruluurdrurddldr"
    assert curves.curve("moore").points(3).shape == (64, 2)


def test_curve_is_hashable_and_equatable():
    assert curves.curve(0) == curves.curve(0)
    assert curves.curve(0) != curves.curve(1)
    assert len({curves.curve(0), curves.curve(0), curves.curve(1)}) == 2


def test_rule_smoke():
    assert "12h(k)" in curves.curve(12).rule
    assert curves.curve(0).rule.startswith("0h(k) =")


# --------------------------------------------------------------------------
# Presentation: name-only repr and CurveList table
# --------------------------------------------------------------------------
def test_curve_str_is_the_name_and_repr_is_unambiguous():
    # str() stays friendly for f-strings and print(); repr() identifies the curve fully.
    assert str(curves.curve(0)) == "Hilbert"
    assert str(curves.curve(1)) == "Moore"
    assert str(curves.curve(12)) == "Liu2+Liu4 #1"
    assert repr(curves.curve(0)) == "<Curve 0H Hilbert (proper)>"
    assert repr(curves.curve(12)) == "<Curve 12H Liu2+Liu4 #1 (inhomogeneous)>"


def test_curvelist_is_a_list_that_prints_as_a_table():
    group = curves.proper()
    assert isinstance(group, list)  # still a real list
    assert group[0] == curves.curve(0)
    text = repr(group)
    for heading in ("name", "kind", "closed"):
        assert heading in text
    for name in ("Hilbert", "Moore"):
        assert name in text
    # closed flag shows for Moore (closed) but not Hilbert
    assert "yes" in text


def test_empty_curvelist_repr():
    assert repr(curves.by_kernels(2)) == "CurveList([])"  # kernel 2 is never used
