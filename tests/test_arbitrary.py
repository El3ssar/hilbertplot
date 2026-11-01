"""Arbitrary-size square generation (Curve.grid) and the generalizing() group."""

import numpy as np
import pytest

import hilbertplot as hp
from hilbertplot._core import curve as curves
from hilbertplot._viz.hilbert_plot import hilbert_plot as make_plot

FEASIBLE = [0, 3, 4, 5, 24, 29, 30, 31]
INFEASIBLE = [i for i in range(40) if i not in FEASIBLE]


def _hamiltonian(cells, n):
    """The predicate these tests assert -- which is exactly the public checker."""
    return hp.curves.is_space_filling(cells, n)


# -- the group / property ---------------------------------------------------
def test_generalizing_group():
    assert [c.index for c in curves.generalizing()] == FEASIBLE
    assert len(curves.generalizing()) == 8


def test_generalizes_property():
    for i in FEASIBLE:
        assert curves.curve(i).generalizes
    for i in INFEASIBLE:
        assert not curves.curve(i).generalizes


# -- grid() correctness -----------------------------------------------------
@pytest.mark.parametrize("index", FEASIBLE)
def test_grid_is_hamiltonian(index):
    c = curves.curve(index)
    for n in [*range(1, 34), 50, 64, 100]:
        assert _hamiltonian(c.grid(n), n), f"{c.name} grid({n}) not Hamiltonian"


@pytest.mark.parametrize("index", FEASIBLE)
def test_grid_matches_points_at_powers_of_two(index):
    c = curves.curve(index)
    for k in range(1, 6):
        assert np.array_equal(c.grid(2**k), c.points(k))


# -- the construction stays a single connected path at every size ------------
@pytest.mark.parametrize("index", FEASIBLE)
def test_grid_is_connected_at_odd_sizes(index):
    """Odd sizes are what the per-curve swap rule exists for; a rewrite could break them."""
    c = curves.curve(index)
    for n in (3, 5, 7, 9, 11, 13, 15, 21, 33, 49, 65):
        cells = c.grid(n)
        steps = np.abs(np.diff(cells, axis=0)).sum(1)
        assert (steps == 1).all(), f"{c.name} grid({n}) has a discontinuity"


@pytest.mark.parametrize("index", FEASIBLE)
def test_grid_matches_points_at_larger_powers_of_two(index):
    """The block-memoised fill must stay bit-identical to the stroke-based construction."""
    c = curves.curve(index)
    for k in (6, 7):
        assert np.array_equal(c.grid(2**k), c.points(k))


# -- gating -----------------------------------------------------------------
@pytest.mark.parametrize("index", INFEASIBLE)
def test_grid_raises_for_infeasible(index):
    with pytest.raises(ValueError, match="does not tile arbitrary squares"):
        curves.curve(index).grid(10)


@pytest.mark.parametrize("index", INFEASIBLE)
def test_smallest_failure_table_is_exactly_the_smallest_failure(index):
    """The number grid() quotes must be true, and minimal.

    It is interpolated straight into a user-facing error, so a stale entry makes the
    library state a falsehood -- three entries did before this test existed.
    """
    from hilbertplot._core.arbitrary import SMALLEST_FAILURE, square_points

    claimed = SMALLEST_FAILURE[index]
    assert not _hamiltonian(square_points(index, claimed), claimed), (
        f"curve {index}: the construction actually succeeds at n={claimed}"
    )
    for smaller in range(1, claimed):
        assert _hamiltonian(square_points(index, smaller), smaller), (
            f"curve {index}: also fails at n={smaller}, so {claimed} is not the smallest"
        )


def test_smallest_failure_covers_exactly_the_infeasible_curves():
    from hilbertplot._core.arbitrary import FEASIBLE as FEASIBLE_SET
    from hilbertplot._core.arbitrary import SMALLEST_FAILURE

    assert sorted(SMALLEST_FAILURE) == INFEASIBLE
    assert set(SMALLEST_FAILURE) & FEASIBLE_SET == set()


def test_infeasible_error_names_the_size_and_points_at_the_alternative():
    with pytest.raises(ValueError, match="Moore") as exc:
        curves.curve(1).grid(10)
    message = str(exc.value)
    assert "Moore" in message
    assert "n=3" in message  # its verified smallest failure
    assert "generalizing()" in message


def test_grid_rejects_bad_n():
    with pytest.raises(ValueError, match="n must be >= 1"):
        curves.curve(0).grid(0)


# -- data mapping square-fit ------------------------------------------------
def test_square_fit_is_default_for_generalizing_curves():
    img = make_plot(0, np.arange(10000)).image()  # ceil(sqrt(10000)) = 100
    assert img.shape == (100, 100)


def test_square_fit_tight_and_padded():
    img = make_plot(0, np.arange(1000)).image()  # ceil(sqrt(1000)) = 32
    assert img.shape == (32, 32)
    assert np.isnan(img).sum() == 32 * 32 - 1000  # 24 blank cells


def test_infeasible_curve_falls_back_to_pad():
    img = make_plot(1, np.arange(1000)).image()  # Moore -> 2^k pad
    assert img.shape == (32, 32)  # order_for(1000) = 5


def test_explicit_fit_square_rejected_for_infeasible():
    with pytest.raises(ValueError, match="needs a generalizing curve"):
        make_plot(1, np.arange(100)).image(fit="square")


def test_square_fit_round_trips_through_unroll():
    data = np.arange(1, 226)  # 225 -> 15x15
    img = make_plot(0, data).image()
    assert img.shape == (15, 15)
    assert np.array_equal(curves.curve(0).unroll(img), data)


def test_order_forces_power_of_two_even_for_generalizing():
    img = make_plot(0, np.arange(100)).image(order=4)
    assert img.shape == (16, 16)
