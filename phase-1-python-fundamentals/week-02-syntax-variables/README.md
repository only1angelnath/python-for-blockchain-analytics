# Week 2 — Syntax, Variables & Data Types

**Phase 1 · Week 2 of 6 · ~8 hours**

---

## What you will learn

- How Python reads and executes code (indentation, statements, comments)
- Variables — naming, assignment, reassignment
- The four core types: `int`, `float`, `str`, `bool`
- Type casting — converting between types (critical for API responses)
- f-strings — clean, readable output formatting
- How all of this maps to real blockchain data

## SQL analyst parallel

Variables are like `SELECT`ing a value and giving it an alias:
```sql
SELECT 1000 AS balance
```
The difference is Python keeps it in memory so you can use it again and again.

---

## Files

| File | Purpose |
|------|---------|
| `lesson.ipynb` | Full lesson — 8 sections, all runnable |
| `exercises.py` | 7 exercises + 1 challenge — attempt before opening solutions |
| `exercises_solutions.py` | Full solutions — open only after attempting |

---

## Key concepts

| Concept | Blockchain example |
|---------|-------------------|
| `int` | Block number, nonce, Wei amounts |
| `float` | Token prices, APY percentages |
| `str` | Wallet addresses, tx hashes, token symbols |
| `bool` | Is contract verified? Is wallet flagged? |
| Type casting | Every Etherscan API response returns strings — cast before arithmetic |
| f-strings | Format receipts, addresses, portfolio summaries |

---

## Mini-project

**Transaction Receipt Formatter** — take raw Etherscan API data (all strings),
cast each field to the correct type, compute gas costs, and display a clean receipt.

---

## Before moving to Week 3

- [ ] All 7 exercises attempted without looking at solutions first
- [ ] Mini-project receipt formatter working and displaying correctly
- [ ] Committed and pushed:
  ```bash
  git add phase-1-python-fundamentals/week-02-syntax-variables/
  git commit -m "phase-1/week-02: syntax and variables complete"
  git push
  ```
