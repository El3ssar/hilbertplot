"""Conversion must retain array values, masks, channel axes and spatial dimensions."""

import numpy as np
import pytest

import hilbertplot as hp


@pytest.mark.parametrize("curve", range(40))
@pytest.mark.parametrize("dtype", [np.uint8, np.int64, np.uint64, np.float32, np.complex64])
def test_exact_round_trip_preserves_values_and_dtype(curve, dtype):
    if dtype == np.uint64:
        source = np.arange(64, dtype=dtype) + 2**63
    elif dtype == np.int64:
        source = np.arange(64, dtype=dtype) + 2**60
    else:
        source = np.arange(64).astype(dtype)
    if np.issubdtype(dtype, np.complexfloating):
        source += 2j
    grid = hp.data.to_grid(source, curve=curve)
    assert type(grid) is np.ndarray
    assert grid.dtype == source.dtype
    recovered = hp.data.from_grid(grid, curve=curve)
    np.testing.assert_array_equal(recovered, source)
    assert recovered.dtype == source.dtype


@pytest.mark.parametrize("curve", [0, 3, 4, 5, 24, 29, 30, 31])
@pytest.mark.parametrize("shape", [(15, 15), (15, 16), (16, 15)])
def test_supported_shapes_use_the_same_path_as_curve_drawing(curve, shape):
    source = np.arange(np.prod(shape), dtype=np.uint64) + 2**63
    grid = hp.data.to_grid(source, curve=curve, shape=shape)
    pts = hp.curves.grid(shape, curve=curve)
    np.testing.assert_array_equal(grid[pts[:, 1], pts[:, 0]], source)
    np.testing.assert_array_equal(hp.data.from_grid(grid, curve=curve), source)


@pytest.mark.parametrize("curve", [0, 1, 12, 31, 39])
@pytest.mark.parametrize("shape", [(4, 4), (8, 8)])
@pytest.mark.parametrize("channels", [(), (3,), (4,), (2, 3)])
def test_images_and_arrays_round_trip_with_all_channels_attached(curve, shape, channels):
    shape = (*shape, *channels)
    source = np.arange(np.prod(shape), dtype=np.int64).reshape(shape) + 2**60
    samples = hp.data.from_grid(source, curve=curve)
    assert samples.shape == (source.size,)
    assert samples.dtype == source.dtype
    restored = hp.data.to_grid(samples, shape=shape, curve=curve)
    np.testing.assert_array_equal(restored, source)
    assert restored.dtype == source.dtype


@pytest.mark.parametrize("curve", [0, 12])
@pytest.mark.parametrize("shape", [(9, 20), (1, 40), (40, 1), (6, 10)])
def test_general_rectangles_are_rejected_without_a_fallback(curve, shape):
    image = np.arange(np.prod(shape)).reshape(shape)
    with pytest.raises(ValueError, match="square and quasisquare"):
        hp.data.from_grid(image, curve=curve)
    with pytest.raises(ValueError, match="square and quasisquare"):
        hp.data.to_grid(image.ravel(), shape=shape, curve=curve)
    with pytest.raises(ValueError, match="square and quasisquare"):
        hp.data.to_grid(np.zeros(image.size * 3), shape=(*shape, 3), curve=curve)


@pytest.mark.parametrize("curve", [0, 3, 4, 5, 24, 29, 30, 31])
def test_colour_images_on_supported_arbitrary_shapes_round_trip(curve):
    for shape in ((6, 6, 3), (6, 7, 4), (7, 6, 3)):
        image = np.arange(np.prod(shape), dtype=np.uint64).reshape(shape) + 2**63
        sequence = hp.data.from_grid(image, curve=curve)
        np.testing.assert_array_equal(hp.data.to_grid(sequence, shape=shape, curve=curve), image)


def test_integer_padding_uses_a_mask_and_length_keeps_legitimate_missing_values():
    values = np.array([2**63 + i for i in range(10)], dtype=np.uint64)
    grid = hp.data.to_grid(values)
    assert np.ma.isMaskedArray(grid)
    assert grid.dtype == values.dtype
    assert np.ma.getmaskarray(grid).sum() == 6
    np.testing.assert_array_equal(hp.data.from_grid(grid, length=10), values)
    floats = np.array([1, np.nan, 3], dtype=np.float32)
    restored = hp.data.from_grid(hp.data.to_grid(floats), length=3)
    np.testing.assert_array_equal(restored, floats)
    assert restored.dtype == floats.dtype
    filled = hp.data.to_grid(values, fill=0)
    assert type(filled) is np.ndarray
    assert filled.dtype == values.dtype
    assert (hp.data.from_grid(filled)[10:] == 0).all()


def test_masks_are_preserved_per_channel_and_conversion_never_aliases_input():
    values = np.ma.array(np.arange(18).reshape(6, 3), mask=False)
    values.mask[2, 1] = True
    grid = hp.data.to_grid(values, shape=(2, 3))
    result = hp.data.from_grid(grid)
    assert result.dtype == values.dtype
    np.testing.assert_array_equal(result.mask, values.mask.ravel())
    np.testing.assert_array_equal(result.compressed(), values.compressed())
    result.data[0] = -999
    assert values[0, 0] == 0
    assert grid.min() >= 0


def test_granularity_averages_samples_without_mixing_channels():
    values = np.array([[0, 100], [2, 104], [10, 200], [14, 208], [20, 300]])
    expected = np.array([[1, 102], [1, 102], [12, 204], [12, 204], [20, 300]])
    grid = hp.data.to_grid(values, granularity=2)
    np.testing.assert_array_equal(hp.data.from_grid(grid, length=10).reshape(5, 2), expected)
    masked = np.ma.array(values, mask=False)
    masked.mask[1, 0] = True
    result = hp.data.from_grid(hp.data.to_grid(masked, granularity=2), length=10).reshape(5, 2)
    assert result.mask[:2, 0].all()
    assert not result.mask[:, 1].any()
    np.testing.assert_array_equal(result[:, 1], expected[:, 1])


def test_curve_switching_on_a_colour_square_is_reversible():
    image = np.arange(8 * 8 * 3, dtype=np.uint64).reshape(8, 8, 3) + 2**63
    samples = hp.data.from_grid(image, curve=0)
    switched = hp.data.to_grid(samples, shape=image.shape, curve=12)
    reversed_samples = hp.data.from_grid(switched, curve=12)
    np.testing.assert_array_equal(hp.data.to_grid(reversed_samples, shape=image.shape), image)


def test_colour_channels_follow_pixel_order_in_a_flat_sequence():
    image = np.arange(12, dtype=np.uint8).reshape(2, 2, 3)
    np.testing.assert_array_equal(hp.data.from_grid(image), [0, 1, 2, 6, 7, 8, 9, 10, 11, 3, 4, 5])


def test_strided_and_fortran_order_images_round_trip():
    source = np.arange(8 * 16 * 3).reshape(8, 16, 3)
    for image in (source[::-1, ::2, ::-1], np.asfortranarray(source[:, :8]).transpose(1, 0, 2)):
        sequence = hp.data.from_grid(image, curve=12)
        assert sequence.ndim == 1
        np.testing.assert_array_equal(hp.data.to_grid(sequence, curve=12, shape=image.shape), image)


def test_explicit_shape_length_and_fill_validation():
    with pytest.raises(ValueError, match="either order or shape"):
        hp.data.to_grid(range(4), shape=(2, 2), order=1)
    with pytest.raises(ValueError, match="does not fit"):
        hp.data.to_grid(range(10), shape=(2, 2))
    np.testing.assert_array_equal(
        hp.data.from_grid(hp.data.to_grid(range(10), shape=(2, 2), fit="truncate")), range(4)
    )
    for length in (-1, 5):
        with pytest.raises(ValueError, match="length"):
            hp.data.from_grid(np.zeros((2, 2)), length=length)
    for length in (True, 1.5):
        with pytest.raises(TypeError, match="length"):
            hp.data.from_grid(np.zeros((2, 2)), length=length)
    assert hp.data.from_grid(np.zeros((2, 2)), length=0).shape == (0,)
    with pytest.raises(ValueError, match="represented"):
        hp.data.to_grid(np.arange(3, dtype=np.uint8), fill=999)
    with pytest.raises(ValueError, match="represented"):
        hp.data.to_grid(np.arange(3, dtype=np.int64), fill=0.5)


def test_non_generalizing_curves_reject_unsupported_square_sizes():
    with pytest.raises(ValueError, match="power-of-two squares only"):
        hp.data.from_grid(np.zeros((6, 6)), curve=12)
    with pytest.raises(ValueError, match="power-of-two squares only"):
        hp.data.to_grid(np.zeros(36), shape=(6, 6), curve=12)
