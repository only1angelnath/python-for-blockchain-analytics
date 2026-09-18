# CLAUDE.md — Instructions for Claude Code in this repo

This file tells Claude Code how to work in the
`python-for-blockchain-analytics` repository.

---

## What this repo is

A complete, beginner-friendly public course:
**Python → Blockchain Data Engineer → ML Engineer**

Learner: Angel (only1angelnath), Lagos. Experienced DuneSQL analyst, blockchain native.
Goal: Blockchain Data Engineer / ML Engineer role within 6 months.

---

## Repo structure

```
phase-0-setup/                         Week 1
phase-1-python-fundamentals/           Weeks 2–6   ← COMPLETE
phase-2-python-for-data/               Weeks 7–10  ← IN PROGRESS (Week 7 done)
phase-3-blockchain-analytics/          Weeks 11–14
phase-4-advanced-python/               Weeks 15–19
phase-5-data-engineering/              Weeks 20–25
phase-6-system-design/                 Weeks 26–29
phase-7-ml-engineering/               Weeks 30–35
final-capstone-chainlens/              Week 36
resources/                             datasets.md, tools.md, books.md
```

---

## File conventions — follow these exactly

| File | Purpose |
|------|---------|
| `lesson.ipynb` | Main lesson notebook |
| `lesson_expanded.ipynb` | Deep-dive version (optional) |
| `lesson_advanced.ipynb` | Applied projects version (optional) |
| `exercises.py` | Exercises ONLY — no solutions embedded |
| `exercises_solutions.py` | Solutions ONLY — separate file with warning header |
| `blockchain_utils.py` | Reusable toolkit (Phase 1 Week 5+) |
| `blockchain_data_tools.py` | Tools reference (Phase 2 Week 7+) |
| `README.md` | Every folder must have one |

---

## Standards for every lesson

### Notebooks
- Explain concepts DEEPLY in markdown before any code cell
- Blockchain-native example for every concept
- SQL parallel for every data manipulation concept
- Structure: numbered sections (`## 1. Title`)
- End with: Summary table → What's next → Commit instructions

### Exercise files
- Problem as docstring above each exercise
- `# YOUR CODE HERE` placeholder
- No solutions — solutions go in `exercises_solutions.py`
- SQL parallels in exercise prompts where applicable

### Solutions files
- Warning at top: "Only open after attempting exercises.py"
- Full working solutions with docstrings
- Must run clean: `python3 exercises_solutions.py`

---

## Data sources — free only (Dune API is sunsetted)

| Use case | Tool | Key? |
|----------|------|------|
| Token prices | CoinGecko | No |
| Protocol TVL | DefiLlama | No |
| On-chain txns | Etherscan | Free signup |
| Contract reads | web3.py + Ankr RPC | No |
| DeFi events | The Graph | No |
| Custom indexer | Envio / HyperIndex | Free tier |
| Solana | Helius | Free signup |
| SQL analytics | Flipside | Free tier |

**Never reference Dune SIM API** — it has been sunsetted.

---

## blockchain_utils.py

Lives at: `phase-1-python-fundamentals/week-05-functions-modules/blockchain_utils.py`

Import in Phase 2+ notebooks:
```python
import sys
sys.path.insert(0, "../../phase-1-python-fundamentals/week-05-functions-modules")
from blockchain_utils import *
```

Do NOT duplicate functions from this file. Import and extend it.

---

## Git commit message format

```
phase-N/week-NN: short description
phase-N/capstone: short description
tidy: what was fixed
fix: what was corrected
```

Examples:
- `phase-2/week-08: pandas and numpy — lesson + exercises`
- `phase-1/week-06b: OOP advanced complete`
- `tidy: Phase 1 READMEs and ROADMAP updated`

---

## What NOT to do

- Never reference Dune Analytics API (sunsetted)
- Never embed solutions in exercises.py
- Never deliver files as zip archives
- Never skip the SQL parallel for data manipulation concepts
- Never use generic examples — always blockchain context
- Never assume Angel needs DeFi explained — he's a blockchain native


