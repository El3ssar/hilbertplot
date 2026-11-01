# Plotting

Every plotting function returns a standard Matplotlib `Figure`. It draws immediately,
without opening a window or closing the figure. Use `fig.savefig(...)`, `plt.show()`,
and `plt.close(fig)` as needed. `ax=` places the drawing on your own axes.

```{eval-rst}
.. autofunction:: hilbertplot.plot
```

```{eval-rst}
.. autofunction:: hilbertplot.plot_curve
```

```{eval-rst}
.. autofunction:: hilbertplot.gallery
```
