# Week 8 — Pandas & NumPy

**Phase 2: Python for Data Analysis**

Run the SQL you already know, locally, on any data source. This week maps every core
`dex.trades`-style query to Pandas, then goes one layer down to NumPy for fast maths,
percentiles, and time series.

## Files

| File | Purpose |
|------|---------|
| `lesson.ipynb` | The lesson: concepts, SQL parallels, blockchain examples, mini project |
| `exercises.py` | 15 exercises + 1 challenge. Self-checking (✅ / ❌ / ⬜). **No solutions.** |
| `exercises_solutions.py` | Full solutions. ⚠️ Only open after attempting `exercises.py` |
| `sample_data.py` | Deterministic offline datasets (DEX trades, gas, TVL, dimension tables) |

## Requirements

```bash
pip install "pandas>=2.2" numpy
```

Imports `blockchain_utils.py` from `../../phase-1-python-fundamentals/week-05-functions-modules/`.

## Topics

- DataFrame as a table, `.info()` / `.describe()` / null checks
- Loading CSV / JSON / API-style data, `parse_dates`
- Selecting (`SELECT`), filtering (`WHERE`, `IN`, `LIKE`, `BETWEEN`, `IS NULL`)
- Computed columns, `np.where` / `np.select` (`CASE WHEN`), sorting, `nlargest`
- `groupby` / `agg` / `pivot_table` / `transform` (`GROUP BY`, window functions)
- `merge` with `validate=` (`JOIN`), anti-joins, `concat` (`UNION ALL`)
- NumPy: vectorisation, broadcasting, percentiles, log returns, the **Wei / int64 overflow trap**
- Time series: `resample` (`date_trunc`), `rolling`, `shift` / `pct_change` (`LAG`), drawdown

## How to work through it

1. Read `lesson.ipynb` top to bottom, running every cell
2. Work through `exercises.py` in order; run `python3 exercises.py` as you go
3. Compare with `exercises_solutions.py` only after attempting everything

## Next

Week 9: Data Visualization (Matplotlib, Seaborn, Plotly)
