# Week 4 — Data Structures: Lists, Tuples, Dictionaries & Sets

**Phase 1 · Week 4 of 6 · ~10 hours (expanded)**

This is the longest week in Phase 1 — data structures are the foundation of
every analytics pipeline. Take your time. The expanded materials reward the effort.

---

## What you will learn

- **Lists** — ordered, mutable sequences; price history, transaction batches
- **Tuples** — immutable records; swap events, function return values
- **Dictionaries** — the most important structure in blockchain analytics; every API response
- **Sets** — unique collections; token holders, deduplication, set math
- **Nesting** — dicts of lists, lists of dicts (real API shapes)
- **namedtuple** — readable immutable records
- **defaultdict + Counter** — power tools for aggregation

## SQL analyst parallel

| Python | SQL equivalent |
|--------|---------------|
| `list` of values | Single-column `SELECT` result |
| `list` of `dict` | Multi-column `SELECT *` result set |
| `dict` | One row |
| `set` | `SELECT DISTINCT` |
| Dict comprehension with filter | `SELECT ... WHERE ...` |
| Aggregating in a loop | `SUM()`, `COUNT()`, `AVG()` with `GROUP BY` |

---

## Files — three levels of depth

| File | Level | Purpose |
|------|-------|---------|
| `lesson.ipynb` | Intro | Core concepts with blockchain examples |
| `lesson_expanded.ipynb` | Deep dive | All methods, copying, sorting, namedtuples, defaultdict, Counter, nesting |
| `lesson_advanced.ipynb` | Applied | 5 complete projects: multi-chain registry, wallet clustering, DEX pool analyser, block scanner, protocol dashboard |
| `exercises.py` | Practice | 7 intro exercises — attempt before solutions |
| `exercises_advanced.py` | Challenge | 8 harder problems combining all structures |
| `exercises_solutions.py` | Reference | Solutions to `exercises.py` |

> `exercises_advanced.py` solutions are embedded as comments at the bottom of each exercise — scroll down only after attempting.

---

## Key concepts

| Structure | Key methods / operations | Blockchain use |
|-----------|--------------------------|----------------|
| `list` | `.append()`, `.sort(key=)`, `sorted()`, slicing, comprehensions | Price history, tx batches |
| `tuple` | unpacking, `namedtuple` | Swap event records, function returns |
| `dict` | `.get()`, `.items()`, `defaultdict`, `Counter`, merge with `\|` | API responses, aggregations |
| `set` | `&`, `\|`, `-`, `^`, `frozenset` | Holder sets, blacklists, set math |

---

## Mini-project

**On-Chain Portfolio Tracker** — takes a list of buy records, aggregates holdings
per token, calculates P&L, sorts by value, analyses diversification using set operations.

---

## Before moving to Week 5

- [ ] All intro exercises attempted independently
- [ ] At least 4 of 8 advanced exercises attempted
- [ ] Portfolio tracker producing correct output
- [ ] Committed and pushed:
  ```bash
  git add phase-1-python-fundamentals/week-04-data-structures/
  git commit -m "phase-1/week-04: data structures complete"
  git push
  ```
