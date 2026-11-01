"""Mapping 1-D data onto 2-D through a Hilbert curve, and the granularity transform.

This implements the *Hilbert plot* of Estevez-Rams et al., "Visualizing long vectors
of measurements by use of the Hilbert curve", Comput. Phys. Commun. 197 (2015) 118:
the chosen curve is walked and value ``data[i]`` is placed at the ``i``-th cell it
visits, so every one of the forty curves induces its own data-to-image mapping.  The
*l-granularity* transform (eqs. 1-3) coarsens the data by replacing each block of ``l``
values with ``l`` copies of the block mean.

Everything here is curve-agnostic (functions take a plain point array), which keeps it
reusable for the coming arbitrary-square generalisation.  Fitting a sequence whose
length is not a power of four is an explicit choice, see :func:`resolve_order` /
:func:`scatter`.
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "FITS",
    "check_fit",
    "check_granularity",
    "difference_map",
    "fourier_spectrum",
    "gather",
    "granulate",
    "label_map",
    "order_floor",
    "order_for",
    "resolve_order",
    "scatter",
    "square_side",
]


def order_for(n: int) -> int:
    """Smallest order ``k`` whose ``2**k`` by ``2**k`` grid holds ``n`` values.

    ``ceil(log4(n))`` -- the order the paper uses for a length-``n`` sequence.

    >>> order_for(1024), order_for(1000), order_for(1025)
    (5, 5, 6)

    Parameters
    ----------
    n : int
        Number of samples, or square side in path construction as described above.

    Returns
    -------
    int
        Smallest recursion depth that holds all requested samples.
    """
    if n < 1:
        raise ValueError(f"need at least one value, got n={n}")
    k = 0
    while 4**k < n:
        k += 1
    return k


def order_floor(n: int) -> int:
    """Largest order ``k`` whose grid fits *inside* ``n`` values (``floor(log4(n))``).

    >>> order_floor(1024), order_floor(1000), order_floor(15)
    (5, 4, 1)

    Parameters
    ----------
    n : int
        Number of samples, or square side in path construction as described above.

    Returns
    -------
    int
        Largest recursion depth fitting inside the sample count.
    """
    if n < 1:
        raise ValueError(f"need at least one value, got n={n}")
    k = 0
    while 4 ** (k + 1) <= n:
        k += 1
    return k


#: Every legal value of the ``fit`` argument, in the order the docs present them.
FITS: tuple[str, ...] = ("auto", "square", "pad", "truncate")


def check_fit(fit: str) -> str:
    """Return ``fit`` if it is one of :data:`FITS`, else raise a listing every legal value.

    Called before anything else looks at ``fit``, so an invalid mode is rejected even when
    an explicit ``order`` would have made it moot -- otherwise a typo passes silently.

    >>> check_fit("square")
    'square'

    Parameters
    ----------
    fit : str
        Sizing policy already selected by the caller: pad, truncate, square or auto.

    Returns
    -------
    str
        The validated fitting policy.
    """
    if fit not in FITS:
        legal = ", ".join(repr(name) for name in FITS)
        raise ValueError(f"fit must be one of {legal}, got {fit!r}")
    return fit


def resolve_order(n: int, order: int | None, fit: str) -> int:
    """Pick the grid order for ``n`` values given an explicit ``order`` or a ``fit`` mode.

    ``fit="pad"`` uses the smallest enclosing grid (``order_for``); ``fit="truncate"``
    uses the largest grid that fits inside the data (``order_floor``).  An explicit
    ``order`` overrides both.

    Parameters
    ----------
    n : int
        Number of samples, or square side in path construction as described above.
    order : int or None
        Recursion depth for a side of 2**order; None requests automatic sizing when supported.
    fit : str
        Sizing policy already selected by the caller: pad, truncate, square or auto.

    Returns
    -------
    int
        Resolved power-of-two recursion depth.
    """
    if order is not None:
        if order < 0:
            raise ValueError(f"order must be non-negative, got {order}")
        return order
    if fit == "pad":
        return order_for(n)
    if fit == "truncate":
        return order_floor(n)
    raise ValueError(f"fit must be 'pad' or 'truncate' here, got {fit!r}")


def check_granularity(granularity: int) -> int:
    """Return ``granularity`` if it is a usable block length, else raise.

    Split out of :func:`granulate` so a caller can validate without paying for the copy
    ``granulate`` makes -- at granularity 1 the transform is the identity, and the render
    path resolves it on every call.

    >>> check_granularity(4)
    4

    Parameters
    ----------
    granularity : int
        Positive number of consecutive samples per averaging block.

    Returns
    -------
    int
        Validated positive block length.
    """
    if isinstance(granularity, bool) or not isinstance(granularity, (int, np.integer)):
        raise TypeError(f"granularity must be an int, got {type(granularity).__name__}")
    granularity = int(granularity)
    if granularity < 1:
        raise ValueError(f"granularity must be >= 1, got {granularity}")
    return granularity


def granulate(data, granularity: int) -> np.ndarray:
    """Replace each consecutive block by repeated copies of its arithmetic mean.

    Parameters
    ----------
    data : array_like
        Real numeric input, flattened to one dimension and converted to float64.
        Non-finite values propagate through their block means; no values are
        omitted automatically. Use data.to_grid for mask-aware conversion.
    granularity : int
        Positive block length. One returns a float64 copy of the flattened
        input. A final short block is averaged over its available values.

    Returns
    -------
    coarse : numpy.ndarray of float64, shape (data.size,)
        Same number of values, with one mean repeated across each block.

    Raises
    ------
    TypeError
        Block length is not an integer or is bool.
    ValueError
        Block length is less than one.

    See Also
    --------
    hilbertplot.plot : Use granularity to coarsen while plotting.

    Notes
    -----
    This is not decimation: sequence length stays fixed. Averaging is lossy
    and happens in sequence order before mapping to pixels. For a block B,
    every output position in B receives sum(data[B]) / len(B). The standalone
    helper converts via numpy.asarray; masked arrays should be handled with
    explicit missing-value policy or the mask-aware to_grid pipeline.

    Examples
    --------
    >>> import hilbertplot as hp
    >>> hp.data.granulate([0, 2, 10, 14, 7], 2).tolist()
    [1.0, 1.0, 12.0, 12.0, 7.0]
    """
    granularity = check_granularity(granularity)
    data = np.asarray(data, dtype=float).ravel()
    if granularity == 1:
        return data.copy()
    n = data.size
    out = np.empty(n, dtype=float)
    full = (n // granularity) * granularity
    if full:
        block_means = data[:full].reshape(-1, granularity).mean(axis=1)
        out[:full] = np.repeat(block_means, granularity)
    if full < n:  # trailing partial block
        out[full:] = data[full:].mean()
    return out


def square_side(n: int) -> int:
    """Smallest square side holding ``n`` values: ``ceil(sqrt(n))``.

    >>> square_side(10000), square_side(1000)
    (100, 32)

    Parameters
    ----------
    n : int
        Number of samples, or square side in path construction as described above.

    Returns
    -------
    int
        Smallest side whose square contains n samples.
    """
    if n < 1:
        raise ValueError(f"need at least one value, got n={n}")
    s = int(n**0.5)
    while s * s < n:
        s += 1
    while (s - 1) * (s - 1) >= n:
        s -= 1
    return s


def scatter(points: np.ndarray, values: np.ndarray, side: int, fill: float = np.nan) -> np.ndarray:
    """Place ``values`` onto a ``side x side`` grid along a curve's ``points`` path.

    ``values[i]`` is written to ``points[i]``.  If there are more values than cells
    they are truncated to fit; if fewer, the remaining cells keep ``fill``.  Returned
    array is indexed ``image[y, x]`` (for ``origin="lower"`` display).

    Parameters
    ----------
    points : numpy.ndarray
        Ordered integer (x, y) cells with shape (N, 2).
    values : numpy.ndarray
        Sample values in traversal order, with any trailing component axes retained.
    side : int or None
        Square side in cells, or None when an order determines it.
    fill : numeric scalar
        Value assigned to cells without samples.

    Returns
    -------
    numpy.ndarray of float64
        Square image indexed [y, x], padded or truncated to capacity.
    """
    cap = side * side
    values = np.asarray(values, dtype=float).ravel()
    if values.size > cap:
        values = values[:cap]
    n = values.size
    image = np.full((side, side), fill, dtype=float)
    sel = points[:n]
    image[sel[:, 1], sel[:, 0]] = values
    return image


def gather(points: np.ndarray, array: np.ndarray) -> np.ndarray:
    """Read a 2-D ``array`` along a curve's ``points`` path -> 1-D (inverse of :func:`scatter`).

    Parameters
    ----------
    points : numpy.ndarray
        The ordered ``(N, 2)`` ``(x, y)`` cells the curve visits.
    array : numpy.ndarray
        A 2-D array indexed ``array[y, x]`` covering those cells.

    Returns
    -------
    numpy.ndarray
        ``array`` values in visit order, i.e. ``array[points[i, 1], points[i, 0]]``.
    """
    return array[points[:, 1], points[:, 0]]


def fourier_spectrum(
    image: np.ndarray, *, log: bool = True, window: bool = False, remove_dc: bool = True
) -> np.ndarray:
    """Return the centred 2-D FFT magnitude of a Hilbert-plot image.

    The magnitude of the (fft-shifted) 2-D Fourier transform: hidden periodicities and
    symmetries in the data show up as bright peaks and structured patterns, exactly the
    "Fourier map" companion to the Hilbert plot of Estevez-Rams et al. (2015).

    Parameters
    ----------
    image : numpy.ndarray
        A 2-D array (a data image from :meth:`hilbertplot.HilbertPlot.image`).  ``NaN`` cells
        (padding) are replaced by the finite mean before transforming.
    log : bool, default True
        Return ``log(1 + |F|)`` (compresses the huge dynamic range so faint structure is
        visible); otherwise the raw magnitude.
    window : bool, default False
        Multiply by a 2-D Hann window first, to suppress the cross-shaped artifact from
        the image's hard edges.
    remove_dc : bool, default True
        Subtract the mean before transforming, so the enormous DC (mean-brightness) spike
        at the centre does not wash out the pattern.

    Returns
    -------
    numpy.ndarray
        A real ``image.shape`` array, the centred spectrum (indexed ``[y, x]``).
    """
    img = np.asarray(image, dtype=float)
    if np.isinf(img).any():
        raise ValueError("Fourier map requires finite values or NaN for missing cells")
    if not np.isfinite(img).any():
        raise ValueError("Fourier map needs at least one finite value")
    if np.isnan(img).any():
        img = np.where(np.isnan(img), np.nanmean(img), img)
    if remove_dc:
        img = img - img.mean()
    if window:
        img = img * np.outer(np.hanning(img.shape[0]), np.hanning(img.shape[1]))
    mag = np.abs(np.fft.fftshift(np.fft.fft2(img)))
    return np.log1p(mag) if log else mag


def label_map(points: np.ndarray, side: int) -> np.ndarray:
    """Return the ``(side, side)`` grid of visit-order indices (labels) for a curve.

    ``label_map[y, x]`` is the step ``i`` at which the curve reaches cell ``(x, y)`` --
    the inverse of ``points``.

    Parameters
    ----------
    points : numpy.ndarray
        The ordered ``(side*side, 2)`` cells the curve visits.
    side : int
        Grid side length (``2**order``).

    Returns
    -------
    numpy.ndarray
        An ``(side, side)`` integer array of labels, indexed ``[y, x]``.
    """
    labels = np.empty((side, side), dtype=np.int64)
    labels[points[:, 1], points[:, 0]] = np.arange(points.shape[0])
    return labels


def _neighbour_counts(side: int) -> np.ndarray:
    """Return each cell's number of 8-neighbours: 8 inside, 5 on an edge, 3 at a corner.

    Parameters
    ----------
    side : int or None
        Square side in cells, or None when an order determines it.

    Returns
    -------
    numpy.ndarray of float64
        Square count array for side >= 2; single-cell handling is in difference_map.
    """
    counts = np.full((side, side), 8.0)
    counts[0, :] = counts[-1, :] = 5.0
    counts[:, 0] = counts[:, -1] = 5.0
    counts[0, 0] = counts[0, -1] = counts[-1, 0] = counts[-1, -1] = 3.0
    return counts


def difference_map(points: np.ndarray, side: int) -> np.ndarray:
    """Return the *difference map*: mean 8-neighbour label distance at every cell.

    At each cell the value is the mean of ``|label - neighbour_label|`` over its up-to-8
    nearest (Moore) neighbours.  Large values mark sites where cells that are close on
    the plane are far apart along the curve -- i.e. where locality is broken (Estevez-Rams
    et al., "Locality preserving homogeneous Hilbert curves by use of arbitrary kernels",
    *Appl. Math. Comput.* **234** (2014) 531).

    Each of the eight neighbour offsets is accumulated over the overlapping sub-rectangle
    where it is in bounds, and divided by the closed-form neighbour count
    (:func:`_neighbour_counts`).  That avoids the NaN-padded scratch grid and per-offset
    masking an in-bounds test would need, and is about 2.5x faster at order 10.

    Parameters
    ----------
    points : numpy.ndarray
        The ordered ``(side*side, 2)`` cells the curve visits.
    side : int
        Grid side length (``2**order``, or any ``n`` for an arbitrary square).

    Returns
    -------
    numpy.ndarray
        An ``(side, side)`` float array of mean neighbour label differences, ``[y, x]``.
        A ``1 x 1`` grid has no neighbours at all, and is reported as ``0.0``.
    """
    if side == 1:  # a lone cell has no neighbours; the mean is vacuous, report zero
        return np.zeros((1, 1))
    labels = label_map(points, side).astype(np.float64)
    total = np.zeros((side, side))
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            # The cells that have a neighbour at this offset, and that neighbour's slice.
            y_start, y_stop = max(0, dy), side + min(0, dy)
            x_start, x_stop = max(0, dx), side + min(0, dx)
            here = labels[y_start:y_stop, x_start:x_stop]
            there = labels[y_start - dy : y_stop - dy, x_start - dx : x_stop - dx]
            total[y_start:y_stop, x_start:x_stop] += np.abs(here - there)
    return total / _neighbour_counts(side)
