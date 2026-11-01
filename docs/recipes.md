# Complete usage example

This script exercises the main plotting and conversion operations. Plotting calls
return figures; save or close them with Matplotlib. Detailed mathematical definitions
are in the individual analysis chapters.

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import hilbertplot as hp

# Data plotting: choose a curve by index, label or symbol.
values = np.sin(np.arange(4096) / 20)
fig = hp.plot(values, curve=12, cmap="RdBu_r", vmin=-1, vmax=1)
fig.savefig("data.png", dpi=180)
fig = hp.plot(values, curve="Moore", granularity=4, cmap="RdBu_r")
fig = hp.plot(values, curve="12H", cmap=["navy", "white", "firebrick"])

# Curve geometry, with no measurement data.
fig = hp.plot_curve(0, order=3, color="steelblue")
fig = hp.plot_curve(3, shape=(15, 16), color="darkorchid")
fig = hp.gallery(hp.curves.proper(), order=3, color="steelblue")

# Raw array conversions retain exact integer values and masks.
source = np.arange(100, dtype=np.uint64) + 2**63
grid = hp.data.to_grid(source, curve=12)
recovered = hp.data.from_grid(grid, curve=12, length=source.size)
np.testing.assert_array_equal(recovered, source)

# Read RGB pixels in curve order; retain the full shape to reconstruct.
image = np.arange(16 * 16 * 3, dtype=np.uint16).reshape(16, 16, 3)
sequence = hp.data.from_grid(image, curve=12)
restored = hp.data.to_grid(sequence, curve=12, shape=image.shape)
np.testing.assert_array_equal(restored, image)

# Numerical transforms, with or without rendering.
coarse = hp.data.granulate(values, 4)
spectrum = hp.data.fourier(values, curve=0, window=True)
fig = hp.plot(values, fourier=True, window=True, cmap="magma")
field = hp.curves.difference_map(0, order=6)
fig = hp.plot(values, difference=True, cmap="inferno",
              norm=LogNorm(vmin=1, vmax=field.max()))

# Metadata, direct indexing, and resource controls.
metadata = hp.curves.info(12)
xy = hp.curves.index_to_xy(10**18, order=40, curve=12)
assert hp.curves.xy_to_index(*xy, order=40, curve=12) == 10**18
stats = hp.config.cache_info()
hp.config.clear_cache()
plt.close("all")
```

For examples where the transforms reveal a specific input structure, see
[Thue–Morse Fourier maps](guides/fourier.md) and
[periodic-region granularity](guides/granularity.md).
