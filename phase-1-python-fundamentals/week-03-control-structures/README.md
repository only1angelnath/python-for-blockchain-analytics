# Week 3 — Control Structures: Loops & Conditionals

**Phase 1 · Week 3 of 6 · ~8 hours**

---

## What you will learn

- `if / elif / else` — making decisions based on on-chain data
- Comparison operators (`==`, `!=`, `>`, `<`, `>=`, `<=`)
- Logical operators (`and`, `or`, `not`, `in`)
- `for` loops — processing lists of transactions or wallets
- `while` loops — polling until a block confirms, retry logic
- `break` and `continue` — controlling loop flow
- `range()` — scanning block ranges
- Nesting — loops inside loops, conditions inside loops

## SQL analyst parallel

| Python | SQL equivalent |
|--------|---------------|
| `if/elif/else` | `CASE WHEN ... THEN ... ELSE ... END` |
| `for tx in transactions` | Iterating over result rows |
| `continue` on failed txns | `WHERE status = 'success'` |
| Accumulating `total_volume` | `SUM(value_eth)` |

---

## Files

| File | Purpose |
|------|---------|
| `lesson.ipynb` | Full lesson — 8 sections, all runnable |
| `exercises.py` | 7 exercises + 1 challenge — attempt before opening solutions |
| `exercises_solutions.py` | Full solutions — open only after attempting |

---

## Key concepts

| Concept | Blockchain use |
|---------|---------------|
| `if/elif/else` | Token tier labelling, gas price classification |
| `and / or / not` | Multi-condition token safety checks |
| `in` | Membership checks against stablecoin lists, blacklists |
| `for` loop | Batch processing trades, wallet lists |
| `break` | Stop scanning once first whale transaction is found |
| `continue` | Skip failed transactions in a batch |
| `while` | Poll for block confirmation, API retry loop |

---

## Mini-project

**Wallet Activity Classifier** — given a list of transactions, aggregate stats
(volume, success rate, gas average, type breakdown) and classify the wallet.

---

## Before moving to Week 4

- [ ] All 7 exercises attempted independently
- [ ] Wallet classifier producing correct output
- [ ] Committed and pushed:
  ```bash
  git add phase-1-python-fundamentals/week-03-control-structures/
  git commit -m "phase-1/week-03: control structures complete"
  git push
  ```
