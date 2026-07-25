"""Arbitrary-size square generation (Curve.grid) and the generalizing() group."""

import numpy as np
import pytest

import hilbertplot as hp

FEASIBLE = [0, 3, 4, 5, 24, 29, 30, 31]
INFEASIBLE = [i for i in range(40) if i not in FEASIBLE]


def _hamiltonian(cells, n):
    if cells.shape != (n * n, 2):
        return False
    if len({tuple(c) for c in cells}) != n * n:
        return False
    if cells[:, 0].min() or cells[:, 1].min():
        return False
    if cells[:, 0].max() != n - 1 or cells[:, 1].max() != n - 1:
        return False
    return bool((np.abs(np.diff(cells, axis=0)).sum(1) == 1).all())


# -- the group / property ---------------------------------------------------
def test_generalizing_group():
    assert [c.index for c in hp.generalizing()] == FEASIBLE
    assert len(hp.generalizing()) == 8


def test_generalizes_property():
    for i in FEASIBLE:
        assert hp.curve(i).generalizes
    for i in INFEASIBLE:
        assert not hp.curve(i).generalizes


# -- grid() correctness -----------------------------------------------------
@pytest.mark.parametrize("index", FEASIBLE)
def test_grid_is_hamiltonian(index):
    c = hp.curve(index)
    for n in list(range(1, 34)) + [50, 64, 100]:
        assert _hamiltonian(c.grid(n), n), f"{c.name} grid({n}) not Hamiltonian"


@pytest.mark.parametrize("index", FEASIBLE)
def test_grid_matches_points_at_powers_of_two(index):
    c = hp.curve(index)
    for k in range(1, 6):
        assert np.array_equal(c.grid(2**k), c.points(k))


# -- gating -----------------------------------------------------------------
@pytest.mark.parametrize("index", INFEASIBLE)
def test_grid_raises_for_infeasible(index):
    with pytest.raises(ValueError):
        hp.curve(index).grid(10)


def test_grid_rejects_bad_n():
    with pytest.raises(ValueError):
        hp.curve(0).grid(0)


# -- data mapping square-fit ------------------------------------------------
def test_square_fit_is_default_for_generalizing_curves():
    img = hp.hilbert_plot(0, np.arange(10000)).image()  # ceil(sqrt(10000)) = 100
    assert img.shape == (100, 100)


def test_square_fit_tight_and_padded():
    img = hp.hilbert_plot(0, np.arange(1000)).image()  # ceil(sqrt(1000)) = 32
    assert img.shape == (32, 32)
    assert np.isnan(img).sum() == 32 * 32 - 1000  # 24 blank cells


def test_infeasible_curve_falls_back_to_pad():
    img = hp.hilbert_plot(1, np.arange(1000)).image()  # Moore -> 2^k pad
    assert img.shape == (32, 32)  # order_for(1000) = 5


def test_explicit_fit_square_rejected_for_infeasible():
    with pytest.raises(ValueError):
        hp.hilbert_plot(1, np.arange(100)).image(fit="square")


def test_square_fit_round_trips_through_unroll():
    data = np.arange(1, 226)  # 225 -> 15x15
    img = hp.hilbert_plot(0, data).image()
    assert img.shape == (15, 15)
    assert np.array_equal(hp.curve(0).unroll(img), data)


def test_order_forces_power_of_two_even_for_generalizing():
    img = hp.hilbert_plot(0, np.arange(100)).image(order=4)
    assert img.shape == (16, 16)
