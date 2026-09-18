# Project Context — Python for Blockchain Analytics

**Last updated:** September 2026
**Repo:** https://github.com/only1angelnath/python-for-blockchain-analytics
**Current position:** Phase 2, Week 8 (Pandas & NumPy) is next

---

## Decisions made that must not be reversed

1. **Dune API is out** — sunsetted. Use DefiLlama, CoinGecko, Etherscan, The Graph, Envio.
2. **Exercises and solutions are always separate files** — `exercises.py` has no solutions; `exercises_solutions.py` is a separate file with a warning at the top.
3. **Deliver files individually, never as zips** — Angel's stated preference.
4. **Always verify Python files run before delivering** — `python3 file.py 2>&1` must be clean.
5. **OOP week was split** — `week-06a` is external beginner class by Doabble Danny; `week-06b` is our advanced blockchain OOP lesson.
6. **Week 04 has three notebooks** — `lesson.ipynb` (intro), `lesson_expanded.ipynb` (deep dive), `lesson_advanced.ipynb` (5 applied projects).
7. **`blockchain_utils.py` travels with the course** — started in week-05, imported in all later phases.
8. **SQL parallels are mandatory** — Angel is an experienced DuneSQL analyst; every new Python concept gets a SQL equivalent.

---

## Phase completion status

| Phase | Status | Notes |
|-------|--------|-------|
| Phase 0 — Setup | ✅ Complete | env setup + GitHub workflow |
| Phase 1 — Python Fundamentals | ✅ Complete | Weeks 2–6 + capstone |
| Phase 2, Week 7 — Files & Error Handling | ✅ Complete | includes blockchain_data_tools.py |
| Phase 2, Week 8 — Pandas & NumPy | ⏳ Next | |
| Phase 2, Week 9 — Visualization | ⏳ Pending | |
| Phase 2, Week 10 — APIs & SQL | ⏳ Pending | |
| Phase 2 Capstone — defi-dashboard | ⏳ Pending | |
| Phase 3–7 | ⏳ Pending | |

---

## File inventory — what actually exists

### Root
- `README.md` — course overview with badges, target audience, structure
- `ROADMAP.md` — week-by-week checklist (updated in September tidy-up)
- `CONTRIBUTING.md` — contribution guidelines
- `LICENSE` — MIT
- `.gitignore` — Python, Jupyter, .env, logs excluded
- `.github/workflows/ci.yml` — ruff lint on push

### resources/
- `datasets.md` — free data sources (updated, Dune removed)
- `tools.md` — tools per phase (updated with Envio, Flipside, Helius etc.)
- `books.md` — reading list per phase (updated)

### phase-0-setup/
- `README.md`
- `01-environment-setup.md`
- `02-git-github-workflow.md`

### phase-1-python-fundamentals/
- `README.md` (updated in tidy-up)
- `week-02-syntax-variables/` — lesson.ipynb, exercises.py, exercises_solutions.py, README.md
- `week-03-control-structures/` — lesson.ipynb, exercises.py, README.md (solutions file missing — needs adding)
- `week-04-data-structures/` — lesson_expanded.ipynb, lesson_advanced.ipynb, exercises_advanced.py, README.md (standard lesson.ipynb and exercises.py missing — needs adding)
- `week-05-functions-modules/` — lesson.ipynb, exercises.py, exercises_solutions.py, blockchain_utils.py
- `week-06a-oop-for-beginner-class-by-doabble-danny/` — external class files, README.md
- `week-06b-oop-advanced-class/` — lesson.ipynb, exercises.py, exercises_solutions.py, README.md
- `capstone-simple-chain/` — capstone-simple-chain.py, README.md

### phase-2-python-for-data/
- `README.md`
- `week-07-files-error-handling/` — lesson.ipynb, exercises.py, exercises_solutions.py, blockchain_data_tools.py

### Phases 3–7 and final capstone
- Folder structure exists (created in initial scaffold)
- All week folders contain only `.gitkeep`
- READMEs exist for each phase

---

## Known gaps to fill (not blocking but noted)

- `week-03-control-structures/exercises_solutions.py` — missing, needs creating
- `week-04-data-structures/lesson.ipynb` — the intro-level notebook, missing
- `week-04-data-structures/exercises.py` — the standard exercises file, missing
- `week-04-data-structures/exercises_solutions.py` — missing
- `phase-2-python-for-data/week-07-files-error-handling/sample_holdings.csv` — sample data file, created during exercises but not committed

---

## Curriculum anchors — every lesson must include

1. **Deep explanation before code** — never drop syntax without context
2. **Blockchain-native example** for every concept
3. **SQL parallel** for every data manipulation concept
4. **Free data sources only** (no Dune API)
5. **Lesson summary table** + What's next + Commit instructions

---

## Phase 2 teaching plan (Weeks 8–10)

### Week 8 — Pandas & NumPy
Topics: DataFrame as a table, loading CSV/JSON, filtering (WHERE), groupby (GROUP BY),
merge (JOIN), NumPy arrays for fast computation, time series with timestamps.
Blockchain use: DEX trade analysis, wallet PnL, gas price statistics, TVL over time.
SQL parallel: heavy — Pandas syntax maps almost 1-to-1 with SQL.

### Week 9 — Data Visualization
Topics: Matplotlib (line, bar, scatter), Seaborn (heatmap, distribution), Plotly (interactive),
chart types for blockchain data (price candlesticks, TVL area, volume bars, pie for allocation).
Blockchain use: ETH price over time, gas heatmap by hour, DEX volume by protocol.

### Week 10 — APIs & SQL from Python
Topics: requests library, REST API patterns, rate limiting, pagination,
sqlite3, pandas.read_sql, building a local analytics DB.
Blockchain use: Pull from CoinGecko + DefiLlama + Etherscan, store in SQLite,
query with both SQL and Pandas.

### Phase 2 Capstone — defi-dashboard
A local multi-source DeFi analytics dashboard:
- Data from 3 sources (Etherscan, CoinGecko, DefiLlama)
- Cleaned and stored in SQLite
- Visualised with Plotly
- Runs locally, exported as a complete GitHub repo

---

## The blockchain_utils.py toolkit (current functions)

Located: `phase-1-python-fundamentals/week-05-functions-modules/blockchain_utils.py`

Categories:
- Address: `shorten_address`, `is_valid_eth_address`, `normalize_address`
- Conversions: `wei_to_eth`, `eth_to_wei`, `gwei_to_eth`, `token_amount`, `format_token`
- Gas: `gas_cost_eth`, `gas_cost_usd`, `gas_tier`
- Price/PnL: `eth_to_usd`, `usd_to_eth`, `pnl`, `price_impact`, `trade_slippage`
- DeFi: `calculate_liquidation_price`, `health_factor`, `apy_to_apr`
- Classification: `token_category`, `is_stablecoin`, `classify_wallet`
- Chain/Explorer: `chain_name`, `get_explorer_url`, `block_to_timestamp_estimate`
- Formatting: `fmt_usd`, `fmt_eth`, `fmt_pct`, `fmt_large`, `fmt_hash`

To import in any Phase 2+ notebook:
```python
import sys
sys.path.insert(0, "../../phase-1-python-fundamentals/week-05-functions-modules")
from blockchain_utils import *
```


