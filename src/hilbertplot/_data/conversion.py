"""Lossless array conversion, separate from floating-point display and transforms."""

from __future__ import annotations

import warnings
from math import prod

import numpy as np

from .._core.curve import curve as lookup
from .._core.generation import check_order
from .._core.limits import check_cells
from .mapping import check_fit, check_granularity, resolve_order, square_side


def _dimensions(shape):
    """Validate and normalize a positive square/quasisquare spatial shape.

    Parameters
    ----------
    shape : tuple of int or None
        Requested spatial shape; trailing dimensions describe pixel components when supported.

    Returns
    -------
    tuple of int
        Validated row and column counts.
    """
    if not isinstance(shape, (tuple, list)) or len(shape) != 2:
        raise TypeError("shape must be a (rows, columns) pair of positive integers")
    if any(isinstance(n, bool) or not isinstance(n, (int, np.integer)) for n in shape):
        raise TypeError("shape must contain positive integers")
    rows, columns = map(int, shape)
    if rows < 1 or columns < 1:
        raise ValueError("shape dimensions must be >= 1")
    if abs(rows - columns) > 1:
        raise ValueError("only square and quasisquare shapes are supported")
    check_cells(rows * columns, f"a {rows}x{columns} grid")
    return rows, columns


def _shape_path(c, shape):
    """Resolve a connected spatial path and its row and column dimensions.

    Parameters
    ----------
    c : Curve
        Resolved internal construction used to generate the path.
    shape : tuple of int or None
        Requested spatial shape; trailing dimensions describe pixel components when supported.

    Returns
    -------
    tuple
        Ordered points followed by row and column counts.
    """
    from .._core.arbitrary import shape_points

    rows, columns = _dimensions(shape)
    return shape_points(c.index, (rows, columns)), rows, columns


def layout(n, curve, shape, order, fit):
    """Resolve the same traversal for reading and writing, without converting values.

    Parameters
    ----------
    n : int
        Number of samples, or square side in path construction as described above.
    curve : Curve or int or str
        Internal curve instance, or selector resolved by the caller.
    shape : tuple of int or None
        Requested spatial shape; trailing dimensions describe pixel components when supported.
    order : int or None
        Recursion depth for a side of 2**order; None requests automatic sizing when supported.
    fit : str
        Sizing policy already selected by the caller: pad, truncate, square or auto.

    Returns
    -------
    tuple
        Ordered points, number of rows and number of columns.
    """
    check_fit(fit)
    c = lookup(curve)
    if shape is not None:
        if order is not None:
            raise ValueError("choose either order or shape, not both")
        pts, rows, columns = _shape_path(c, shape)
        if n > rows * columns and fit != "truncate":
            raise ValueError("data does not fit in shape; choose fit='truncate' explicitly")
        return pts, rows, columns
    if order is not None:
        order = check_order(order)
        if n > 4**order and fit != "truncate":
            raise ValueError(
                f"{n} values do not fit in order {order} ({4**order} cells). "
                "Use a larger order, omit order, or choose fit='truncate' explicitly."
            )
    else:
        effective = "square" if fit == "auto" and c.generalizes else fit
        if effective == "square":
            if not c.generalizes:
                raise ValueError("fit='square' needs a generalizing curve")
            side = square_side(n)
            return c.grid(side), side, side
        order = resolve_order(n, None, "pad" if effective == "auto" else effective)
    side = 2**order
    return c.points(order), side, side


def _coarsen(values, granularity):
    """Average records in blocks, keeping channels and missing masks attached.

    Parameters
    ----------
    values : numpy.ndarray
        Sample values in traversal order, with any trailing component axes retained.
    granularity : int
        Positive number of consecutive samples per averaging block.

    Returns
    -------
    numpy.ndarray or numpy.ma.MaskedArray
        Same sample shape with repeated block means and propagated masks.
    """
    g = check_granularity(granularity)
    if g == 1:
        return values
    dtype = np.result_type(values.dtype, np.float64)
    source = np.ma.filled(values.astype(dtype), np.nan)
    result = np.empty(values.shape, dtype=dtype)
    full = len(values) // g * g
    if full:
        means = source[:full].reshape((-1, g, *values.shape[1:])).mean(axis=1)
        result[:full] = np.repeat(means, g, axis=0)
    if full < len(values):
        result[full:] = source[full:].mean(axis=0)
    if np.ma.isMaskedArray(values):
        mask = np.ma.getmaskarray(values)
        out_mask = np.empty(values.shape, dtype=bool)
        if full:
            block_mask = mask[:full].reshape((-1, g, *values.shape[1:])).any(axis=1)
            out_mask[:full] = np.repeat(block_mask, g, axis=0)
        if full < len(values):
            out_mask[full:] = mask[full:].any(axis=0)
        return np.ma.array(result, mask=out_mask)
    return result


def to_grid(data, *, curve, shape, order, fit, fill, granularity):
    """Arrange numeric sample records along a supported path without lossy dtype conversion.

    Parameters
    ----------
    data : array_like
        Numeric sample sequence supplied by the caller.
    curve : Curve or int or str
        Internal curve instance, or selector resolved by the caller.
    shape : tuple of int or None
        Requested spatial shape; trailing dimensions describe pixel components when supported.
    order : int or None
        Recursion depth for a side of 2**order; None requests automatic sizing when supported.
    fit : str
        Sizing policy already selected by the caller: pad, truncate, square or auto.
    fill : numeric scalar
        Value assigned to cells without samples.
    granularity : int
        Positive number of consecutive samples per averaging block.

    Returns
    -------
    numpy.ndarray or numpy.ma.MaskedArray
        Grid with trailing sample axes; padding and input masks are preserved.
    """
    values = np.asanyarray(data)
    if values.ndim < 1 or len(values) == 0:
        raise ValueError("data is empty or scalar; provide at least one sample")
    if values.dtype.kind not in "biufc":
        raise TypeError("data must be a numeric array")
    if any(n == 0 for n in values.shape[1:]):
        raise ValueError("samples must have at least one channel/value")
    if shape is not None and isinstance(shape, (tuple, list)) and len(shape) > 2:
        spatial = _dimensions(shape[:2])
        channels = shape[2:]
        if any(isinstance(n, bool) or not isinstance(n, (int, np.integer)) for n in channels):
            raise TypeError("shape must contain positive integers")
        channels = tuple(map(int, channels))
        if any(n < 1 for n in channels):
            raise ValueError("shape dimensions must be >= 1")
        if values.ndim == 1:
            width = prod(channels)
            if len(values) % width:
                raise ValueError("sequence length must be divisible by the channel dimensions")
            values = values.reshape((-1, *channels))
        elif values.shape[1:] != channels:
            raise ValueError("sample channel dimensions do not match shape")
        shape = spatial
    values = _coarsen(values, granularity)
    pts, rows, columns = layout(len(values), curve, shape, order, fit)
    count = min(len(values), rows * columns)
    padded = count < rows * columns
    target_shape = (rows, columns, *values.shape[1:])
    fill_array = np.asarray(fill)
    if fill_array.ndim != 0 or fill_array.dtype.kind not in "biufc":
        raise TypeError("fill must be a numeric scalar")
    missing_fill = bool(np.isnan(fill_array))
    masked_padding = padded and missing_fill and values.dtype.kind not in "fc"
    masked = np.ma.isMaskedArray(values) or masked_padding
    if not padded:
        result = np.empty(target_shape, dtype=values.dtype)
    elif masked_padding:
        result = np.zeros(target_shape, dtype=values.dtype)
    else:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("error")
                cast_fill = fill_array.astype(values.dtype).item()
            if values.dtype.kind in "biu" and cast_fill != fill_array.item():
                raise ValueError("fill would lose precision")
            result = np.full(target_shape, cast_fill, dtype=values.dtype)
        except (ValueError, TypeError, OverflowError, Warning) as exc:
            raise ValueError(f"fill cannot be represented by dtype {values.dtype}") from exc
    if masked:
        mask = np.full(target_shape, padded and missing_fill, dtype=bool)
        result = np.ma.array(result, mask=mask)
    selected = pts[:count]
    result[selected[:, 1], selected[:, 0]] = values[:count]
    return result


def from_grid(array, *, curve, length):
    """Gather spatial pixels and flatten their components, retaining dtype and masks.

    Parameters
    ----------
    array : numpy.ndarray
        Array indexed by spatial row then column; trailing axes hold pixel components.
    curve : Curve or int or str
        Internal curve instance, or selector resolved by the caller.
    length : int or None
        Requested number of flattened output values; None retains all values.

    Returns
    -------
    numpy.ndarray or numpy.ma.MaskedArray
        One-dimensional curve-ordered values, optionally limited to length.
    """
    values = np.asanyarray(array)
    if values.ndim < 2:
        raise ValueError("expected an array with at least two spatial dimensions")
    if any(n == 0 for n in values.shape[2:]):
        raise ValueError("pixels must have at least one channel/value")
    shape = _dimensions(list(values.shape[:2]))
    pts, _, _ = _shape_path(lookup(curve), shape)
    result = values[pts[:, 1], pts[:, 0]].reshape(-1)
    if length is not None:
        if isinstance(length, bool) or not isinstance(length, (int, np.integer)):
            raise TypeError("length must be an integer")
        if not 0 <= length <= len(result):
            raise ValueError(f"length must be between 0 and {len(result)}")
        result = result[:length]
    return result
