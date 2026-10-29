# Week 10 — APIs & SQL from Python

**Phase 2: Python for Data Analysis**

Pull real data from CoinGecko, DefiLlama and Etherscan; store it in your own SQLite warehouse;
query it with SQL *and* Pandas; and wrap it all in a re-runnable pipeline. This is the engine
of the Phase 2 capstone (`defi-dashboard`).

**Offline-first:** every notebook and exercise runs with **no internet and no API keys**, using
`fixtures.py`. A single flag switches the same code to the live APIs.

## Files

| File | Purpose |
|------|---------|
| `lesson.ipynb` | **Part 1: APIs.** HTTP anatomy, JSON→DataFrame, auth & secrets, error handling, retries/backoff, rate limits, pagination & generators, caching |
| `lesson_expanded.ipynb` | **Part 2: SQLite.** Connections & transactions, type quirks (wei!), injection, constraints, indexes, upserts, window functions, Pandas bridge |
| `lesson_advanced.ipynb` | **Part 3: Pipeline.** ETL design, idempotency, incremental loads, logging, quality checks, CLI, analytics on your warehouse |
| `exercises.py` | 16 exercises + 1 challenge. Self-checking (✅ / ❌ with hints / ⬜). **No solutions.** |
| `exercises_solutions.py` | Full solutions. ⚠️ Only open after attempting `exercises.py` |
| `api_clients.py` | Reusable toolkit: `request_json` (retries/backoff), `RateLimiter`, CoinGecko / DefiLlama / Etherscan V2 clients |
| `db_tools.py` | Schema + safe connection + idempotent upserts |
| `pipeline.py` | The ETL pipeline + quality checks + CLI |
| `fixtures.py` | Offline stand-in for the three APIs (same response *shapes*, simulated numbers) |
| `live_smoke_test.py` | Verifies your keys and each live endpoint, with hints. **Run this first when going live** |
| `RESOURCES.md` | Curated docs, videos, free PDFs, with verification status for every link |

(Naming note: the three lesson notebooks follow the course's `lesson` / `lesson_expanded` / `lesson_advanced`
convention, but here they are three *parts* in sequence rather than three depths of one topic.)

## Requirements

```bash
pip install pandas numpy requests matplotlib
```

Uses `blockchain_utils.py` (Week 5) and `sample_data.py` (Week 8) via relative paths.

## Quick start

```bash
python3 exercises.py                  # see where you are (all ⬜ at first)
python3 pipeline.py                   # run the pipeline offline -> chainlens.db
python3 live_smoke_test.py --offline  # proves the smoke test works
```

### Going live (optional, after the lessons)

```bash
export ETHERSCAN_API_KEY=...          # free: etherscan.io/apis
export COINGECKO_DEMO_API_KEY=...     # free Demo plan (recommended)
python3 live_smoke_test.py            # check every source first
python3 pipeline.py --live
```

Put keys in a `.env` that is in `.gitignore`. **Never commit a key.** Also add `*.db`, `raw/`, `.cache/`.

## Topics

- HTTP request/response, query params, status codes, JSON ↔ Python
- Three JSON shapes → DataFrame; epoch seconds vs milliseconds
- API keys, env vars, `.env`, redaction; why Etherscan hides errors inside HTTP 200
- Retries with exponential backoff and `Retry-After`; client-side rate limiting
- Pagination: page-number, capped offset, block-cursor; **generators** (`yield`, `islice`)
- SQLite: transactions, types (int64 vs wei), placeholders, constraints, indexes, upsert, `to_sql` traps
- SQL: CTEs, window functions, date functions; DuneSQL ↔ SQLite differences
- ETL: idempotent, incremental, observable; quality checks; `argparse` CLI; scheduling concepts

## How to work through it

Follow the study order in `RESOURCES.md` §7: lesson → exercises for that part → next lesson.
Compare with `exercises_solutions.py` only after attempting everything.

## Honest limits

The live-API path was written from the providers' documentation but **could not be run against the real
APIs** in the environment where this week was built. Fixture numbers are simulated. If a live call fails,
`live_smoke_test.py` tells you which source and why; the provider's current docs win over this course.

## Next

**Phase 2 Capstone: `defi-dashboard`**: extend this pipeline with your own sources and questions, add the Plotly dashboard, publish.
