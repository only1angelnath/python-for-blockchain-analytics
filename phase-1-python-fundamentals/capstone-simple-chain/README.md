# Phase 1 Capstone — simple-chain

**A simulated blockchain in pure Python**

---

## What this is

A working blockchain simulation built using only the Python standard library —
no external packages allowed. This capstone tests everything from Phase 1:

- **OOP** (Week 6b) — three classes that model the blockchain
- **Data structures** (Week 4) — lists, dicts for the chain and transaction pool
- **Functions** (Week 5) — clean, validated, documented methods
- **Control structures** (Week 3) — validation loops, chain traversal
- **Type casting** (Week 2) — consistent data types throughout

---

## Architecture

```
Blockchain
  └── chain: list[Block]
        └── transactions: list[Transaction]
```

### `Transaction`
Models a transfer of value between two addresses.
- Stores `from_addr`, `to_addr`, `amount`, `timestamp`
- `tx_hash` property — deterministic SHA-256 hash of all fields

### `Block`
Groups transactions and links to the previous block.
- Stores `index`, `previous_hash`, `transactions`, `timestamp`
- `block_hash` property — SHA-256 of block contents
- `is_valid()` — checks hash starts with `"00"` (simplified proof-of-work)

### `Blockchain`
Manages the chain, pending pool, and analytics.
- `add_transaction()` — adds to pending pool
- `mine_block()` — creates a new block from pending transactions
- `is_valid_chain()` — verifies every block links correctly to the previous
- `get_balance(address)` — computes net balance from all mined transactions

---

## Files

| File | Description |
|------|-------------|
| `capstone-simple-chain.py` | Full implementation — run with `python3 capstone-simple-chain.py` |

---

## Running it

```bash
cd phase-1-python-fundamentals/capstone-simple-chain
python3 capstone-simple-chain.py
```

Expected output:
```
Blockchain: 3 blocks | valid: True
Block #0 | 0 txns | hash: 0000...
Block #1 | 2 txns | hash: 00ab...
  0xAlice → 0xBob | 5.0 ETH
  0xBob → 0xCarol | 2.0 ETH
Block #2 | 2 txns | hash: 00cd...
  0xCarol → 0xAlice | 1.0 ETH
  0xAlice → 0xDave | 0.5 ETH

Balance 0xAlice: -4.5 ETH
Balance 0xBob: 3.0 ETH
Balance 0xCarol: 1.0 ETH
Balance 0xDave: 0.5 ETH
```

---

## Extension ideas

Once the basic version works, try:
- Add a `difficulty` parameter that controls how many leading zeros the hash needs
- Add a `miner_reward` — credit the miner's address with a reward per block
- Add transaction fees — sender pays a small fee per transaction
- Add `verify_transaction(tx)` — check the sender has sufficient balance before adding to pending

---

## What comes next

Phase 2 — Python for Data Analysis. You will load real blockchain data from
CSVs and APIs, manipulate it with Pandas, and visualise it with Matplotlib and Plotly.
