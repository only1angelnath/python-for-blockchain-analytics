# Week 9 — Data Visualization

**Phase 2: Python for Data Analysis**

On Dune you click "Add visualization". This week you learn what's behind that button, and
how to build charts you fully control, from quick exploratory plots to interactive HTML
you can publish.

## Files

| File | Purpose |
|------|---------|
| `lesson.ipynb` | The lesson: chart selection, Matplotlib, Seaborn, Plotly, design checklist, dashboard mini project |
| `exercises.py` | 12 exercises + 1 challenge. Self-checking (✅ / ❌ with reasons / ⬜). **No solutions.** |
| `exercises_solutions.py` | Full solutions. ⚠️ Only open after attempting `exercises.py` |
| `viz_data.py` | Deterministic offline data: ETH OHLC, allocation, plus the Week 8 datasets |

## Requirements

```bash
pip install matplotlib seaborn plotly pandas numpy
```

Imports `blockchain_utils.py` from Week 5 and `sample_data.py` from Week 8 (via `viz_data.py`).

## Topics

- Choosing the chart from the question; Dune chart types mapped to Python
- Matplotlib anatomy (Figure / Axes), formatters, annotation, `savefig`
- Line, bar (grouped/stacked/horizontal), scatter (log scales), area (stacked / 100%), pie vs bar
- Subplots with shared axes; candlesticks built from scratch
- Seaborn: histograms, box plots, heatmaps (gas by weekday x hour), correlation matrix
- Plotly Express + Graph Objects: hover, candlestick + volume, `write_html`
- A chart-quality checklist and common pitfalls

## How to work through it

1. Run `lesson.ipynb` top to bottom (it writes charts into `charts/`)
2. Work through `exercises.py`; run `python3 exercises.py --save` and **open the PNGs**.
   The checker verifies structure; judging whether a chart is clear is your job.
3. Compare with `exercises_solutions.py` only after attempting everything

## Next

Week 10: APIs & SQL from Python (CoinGecko, DefiLlama, Etherscan, SQLite)
