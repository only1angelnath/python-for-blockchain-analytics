# Phase 1 — Python Fundamentals

**Duration:** Weeks 2–6 | **~50 hours**

Zero to functional Python — with every concept anchored to a blockchain example.
SQL analysts will find explicit SQL parallels throughout. By the end you will have
built a simulated blockchain in pure Python and a reusable `blockchain_utils.py`
toolkit you carry into every later phase.

---

## Self-assessment — can you skip Phase 1?

Answer these before starting. If all five are solid, review quickly and jump to Phase 2.

1. What is the difference between a list and a tuple?
2. Write a function that takes a wallet address and returns whether it is valid (starts with `0x`, 42 chars).
3. Write a class `Wallet` with a `deposit()` method that validates the amount.
4. What does `defaultdict(list)` do and when would you use it over a plain dict?
5. What is `self` in a class method and why is it always the first parameter?

---

## Week-by-week contents

| Week | Folder | Topic | Files |
|------|--------|-------|-------|
| 2 | `week-02-syntax-variables` | Syntax, variables, data types | `lesson.ipynb` · `exercises.py` · `exercises_solutions.py` |
| 3 | `week-03-control-structures` | Loops and conditionals | `lesson.ipynb` · `exercises.py` · `exercises_solutions.py` |
| 4 | `week-04-data-structures` | Lists, tuples, dicts, sets | `lesson.ipynb` · `lesson_expanded.ipynb` · `lesson_advanced.ipynb` · `exercises.py` · `exercises_advanced.py` · `exercises_solutions.py` |
| 5 | `week-05-functions-modules` | Functions, modules, `blockchain_utils.py` | `lesson.ipynb` · `exercises.py` · `exercises_solutions.py` · `blockchain_utils.py` |
| 6a | `week-06a-oop-for-beginner-class-by-doabble-danny` | OOP beginner foundations | Standalone class materials |
| 6b | `week-06b-oop-advanced-class` | OOP advanced — blockchain classes | `lesson.ipynb` · `exercises.py` · `exercises_solutions.py` |

---

## Lesson format

Every week contains:
- `lesson.ipynb` — Jupyter notebook: concept explanation + runnable examples
- `exercises.py` — Practice problems (**attempt before opening solutions**)
- `exercises_solutions.py` — Full solutions in a separate file

Week 4 also has expanded notebooks for deeper study.

---

## Key artefacts you will build

| Artefact | Where | What it is |
|----------|-------|------------|
| `blockchain_utils.py` | `week-05-functions-modules/` | 30+ reusable utility functions — imported in every later phase |
| `simple-chain` | `capstone-simple-chain/` | A simulated blockchain built from scratch in pure Python |

---

## Phase 1 Capstone

📁 [`capstone-simple-chain/`](capstone-simple-chain/)

Build a working blockchain simulation using only the Python standard library:
`Transaction` → `Block` → `Blockchain`. No external libraries. Tests your mastery of
OOP, data structures, hashing, and validation all at once.

---

## Prerequisites

- Phase 0 complete (Python installed, VS Code configured, GitHub repo set up)
- No prior programming experience required

---

## What comes next

**Phase 2 — Python for Data Analysis** (`phase-2-python-for-data/`)

File handling, Pandas, NumPy, visualisation, and your first real API calls
against DefiLlama, CoinGecko, and Etherscan.
