"""Guards against the performance cliffs this library has actually had.

These assert *ratios* between two operations on the same machine, never wall-clock
absolutes, so they mean the same thing on a fast laptop and a throttled CI runner.  Each
one encodes a bug that shipped: ``grid()`` used to bottom out its recursion once per cell,
making the flagship curve's default render path ~17x slower than the power-of-two path.
"""

from __future__ import annotations

import time

import numpy as np
import pytest

import hilbertplot as hp
from hilbertplot._core import curve as curves


def _fastest(call, repeats: int = 3) -> float:
    """Return the best of ``repeats`` timings -- the least noisy estimate available."""
    call()  # warm caches so we time the work, not the memoisation
    return min(_timed(call) for _ in range(repeats))


def _timed(call) -> float:
    start = time.perf_counter()
    call()
    return time.perf_counter() - start


@pytest.mark.parametrize("order", [8, 9])
def test_arbitrary_square_fill_is_not_slower_than_the_power_of_two_path(order):
    """``grid(2**k)`` and ``points(k)`` produce the same cells; neither may be a cliff.

    The block-memoised fill is normally *faster* than the stroke construction.  A generous
    4x ceiling still catches a regression to per-cell Python recursion, which was ~17x.
    """
    curve = curves.curve(0)
    grid = _fastest(lambda: curve.grid(2**order))
    points = _fastest(lambda: curve.points(order))
    assert grid < points * 4, (
        f"grid(2**{order}) took {grid * 1e3:.1f} ms vs points({order}) {points * 1e3:.1f} ms "
        f"({grid / points:.1f}x) -- the arbitrary-square fill has regressed"
    )


def test_grid_scales_roughly_with_area():
    """Doubling the side quadruples the cells; time must not grow far faster than that."""
    curve = curves.curve(0)
    small = _fastest(lambda: curve.grid(256))
    large = _fastest(lambda: curve.grid(512))
    # 4x the work; allow 12x for constant factors and noise. Per-cell recursion blows this.
    assert large < max(small * 12, 0.5), (
        f"grid(512) took {large * 1e3:.1f} ms vs grid(256) {small * 1e3:.1f} ms "
        f"({large / small:.1f}x for 4x the cells)"
    )


def test_repeated_renders_do_not_rebuild_the_curve_from_scratch():
    """The stroke memo must survive across calls; clearing it must be the only way out.

    Asserted on the *memo counters* rather than on elapsed time: the warm path is only a
    few times faster than the cold one, which is well inside the noise of a shared runner,
    and a flaky timing assertion in a repo that squash-merges on green is worse than no
    assertion at all.  ``test_arbitrary_square_fill_...`` carries the timing signal.
    """
    curve = curves.curve(0)
    hp.config.clear_cache()
    assert hp.config.cache_info().currsize == 0

    curve.word(9)
    after_cold = hp.config.cache_info()
    assert after_cold.misses > 0, "a cold build should have missed the memo"

    curve.word(9)
    after_warm = hp.config.cache_info()
    assert after_warm.hits > after_cold.hits, "a repeat build did not hit the memo"
    assert after_warm.misses == after_cold.misses, "a repeat build recomputed something"

    hp.config.clear_cache()
    assert hp.config.cache_info().currsize == 0


def test_difference_map_stays_within_reach_of_a_single_pass():
    """It accumulates 8 neighbour offsets, so ~8 passes over the grid is the floor."""
    curve = curves.curve(0)
    order = 8
    points = curve.points(order)
    side = 2**order
    baseline = _fastest(lambda: np.abs(np.diff(points, axis=0)).sum())
    difference = _fastest(lambda: curve.difference_map(order))
    assert difference < max(baseline * 400, 0.5), (
        f"difference_map({order}) took {difference * 1e3:.1f} ms; "
        f"a single pass over {side}x{side} is {baseline * 1e3:.2f} ms"
    )


def test_single_cell_index_maths_beats_building_the_curve():
    """``encode`` is the whole reason to have index maths; it must be O(order), not O(4**order)."""
    curve = curves.curve(0)
    order = 10
    hp.config.clear_cache()
    build = _timed(lambda: curve.points(order))
    encode = _fastest(lambda: curve.encode(4**order // 2, order), repeats=5)
    assert encode * 100 < build, (
        f"encode took {encode * 1e6:.1f} us vs {build * 1e3:.1f} ms to build the curve; "
        f"it should be orders of magnitude cheaper"
    )
