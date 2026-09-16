# Week 6b — OOP Advanced: Blockchain Classes

**Phase 1 · Week 6b of 6 · ~10 hours**

**Prerequisite:** Complete `week-06a-oop-for-beginner-class-by-doabble-danny/` first.

---

## What you will learn

- `__init__` — setting up an object's initial state with validation
- Instance methods — behaviour that uses `self`
- Class attributes vs instance attributes — when to use each
- `@classmethod` and `@staticmethod` — factory methods and utilities
- `@property` — computed attributes accessed without parentheses
- Dunder (magic) methods — `__repr__`, `__str__`, `__eq__`, `__lt__`, `__len__`, `__contains__`
- Inheritance — building `Token → ERC20Token → StableToken` hierarchies
- `super()` — extending parent behaviour without rewriting it
- When to use OOP vs plain functions

---

## Files

| File | Purpose |
|------|---------|
| `lesson.ipynb` | Full lesson — 8 sections, deeply explained |
| `exercises.py` | 6 exercises + Phase 1 capstone challenge — no solutions |
| `exercises_solutions.py` | Full solutions — open only after attempting |

---

## Classes you will build

| Class | What it models | New OOP concepts introduced |
|-------|---------------|----------------------------|
| `Block` | Ethereum block | `__init__`, methods, dunders |
| `TokenRegistry` | Shared token database | Class attributes, `@classmethod` |
| `LiquidityPool` | Uniswap-style pool | `@property`, `__eq__` with order-independence |
| `Protocol → DEX → LendingProtocol` | DeFi protocols | Inheritance, `super()`, method overriding |
| `PriceOracle` | Price tracker | `@property` getter + setter with validation |
| `Transaction` | Ethereum transaction | All dunders together, `@property` for derived fields |

---

## Challenge — Phase 1 Capstone

Build a simulated blockchain using three classes:

```
ChainTransaction → ChainBlock → Blockchain
```

Uses: `hashlib.sha256`, OOP, data structures, and everything from Phase 1.
See [`capstone-simple-chain/`](../capstone-simple-chain/) for the standalone version.

---

## Key OOP decision guide

| Use a class when | Use a function when |
|-----------------|---------------------|
| Data + behaviour belong together | Pure transformation (input → output) |
| Multiple instances with shared structure | No persistent state needed |
| Need inheritance | Simple utility |
| State changes over time | One-off calculation |

---

## Before moving to Phase 2

- [ ] All 6 exercises attempted without peeking at solutions
- [ ] Capstone blockchain simulation running correctly
- [ ] `blockchain_utils.py` from Week 5 is committed and working
- [ ] Committed and pushed:
  ```bash
  git add phase-1-python-fundamentals/week-06b-oop-advanced-class/
  git commit -m "phase-1/week-06b: advanced OOP complete"
  git push
  ```
