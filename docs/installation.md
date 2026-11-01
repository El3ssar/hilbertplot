# Installation

Python 3.10 or newer is required.

```bash
pip install hilbertplot
```

This installs NumPy and Matplotlib together with the library. Plotting and numerical
operations are available from the same installation; no extra is needed.

To update an existing installation:

```bash
pip install --upgrade hilbertplot
```

## Verify the installation

```python
import hilbertplot as hp

print(hp.__version__)
print(hp.curves.info("Moore")["index"])  # 1
```

## Work from source

```bash
git clone https://github.com/El3ssar/hilbertplot.git
cd hilbertplot
uv sync --extra dev
uv run python examples/try_api.py
```

`examples/try_api.py` makes separate figures and exercises the numerical operations.
Add `--save-only` with `MPLBACKEND=Agg` to run without opening windows.
