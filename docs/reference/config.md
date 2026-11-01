# Resource controls

Normal plotting needs no configuration. Curve generation memoises stroke data;
coordinate and derived image arrays may still be allocated again on later calls.

An order-k path contains 4**k cells. Coordinates alone cost 16 bytes per cell;
images, masks, FFTs and intermediate arrays add to peak memory. The default cell
limit is a guard against accidental huge allocations, not a reserved memory budget.

```python
import hilbertplot as hp

previous = hp.config.set_cell_limit(4**10)
try:
    # work within the temporary limit
    pass
finally:
    hp.config.set_cell_limit(previous)
hp.config.clear_cache()
```

```{eval-rst}
.. autofunction:: hilbertplot.config.cache_info
```

```{eval-rst}
.. autofunction:: hilbertplot.config.clear_cache
```

```{eval-rst}
.. autofunction:: hilbertplot.config.cell_limit
```

```{eval-rst}
.. autofunction:: hilbertplot.config.set_cell_limit
```
