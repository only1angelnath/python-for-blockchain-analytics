"""
Week 6 Exercises — Object-Oriented Programming
Python for Blockchain Analytics | Phase 1

Instructions:
- Attempt every exercise before opening exercises_solutions.py
- Each exercise builds on the last — complete them in order
- Run with: python3 exercises.py

Solutions are in: exercises_solutions.py
"""

print("=" * 60)
print("WEEK 6 EXERCISES — Object-Oriented Programming")
print("=" * 60)


# ─────────────────────────────────────────────────────────────
# EXERCISE 1 — Your first class: Block
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 1: The Block class ──")
"""
A blockchain is made of blocks. Each block has:
  - block_number  (int)
  - timestamp     (int)   — Unix timestamp
  - miner         (str)   — address that mined/validated the block
  - tx_hashes     (list)  — list of transaction hashes in this block
  - gas_used      (int)
  - gas_limit     (int)   — default: 30_000_000
  - base_fee_gwei (float)

Write a Block class with:
  1. __init__ accepting all fields (gas_limit defaults to 30_000_000)
  2. tx_count()         → number of transactions
  3. gas_utilisation()  → gas_used / gas_limit as a percentage (float)
  4. is_full()          → True if gas utilisation > 95%
  5. add_transaction(tx_hash) → appends to tx_hashes
  6. __repr__  → Block(number=19847293, txns=142, gas=87.3%)
  7. __str__   → "Block 19,847,293 | 142 txns | 87.3% gas | 18.5 Gwei"
  8. __len__   → number of transactions

Test with:
  block = Block(
      block_number  = 19_847_293,
      timestamp     = 1_714_000_000,
      miner         = "0xeBec795c9c8bBD61FFc14A6662944748F299cAec",
      tx_hashes     = ["0xaaa", "0xbbb", "0xccc"],
      gas_used      = 26_174_000,
      base_fee_gwei = 18.5,
  )
  block.add_transaction("0xddd")

Print: repr, str, tx_count(), gas_utilisation(), is_full(), len(block)
"""

# YOUR CODE HERE


# ─────────────────────────────────────────────────────────────
# EXERCISE 2 — Instance vs class attributes: TokenRegistry
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 2: TokenRegistry class ──")
"""
Build a TokenRegistry that tracks all registered tokens.

Class attributes (shared across ALL registry instances):
  - _registry: dict  — {symbol: {price, decimals}}
  - _count: int      — total tokens ever registered

Instance attributes (per registry object):
  - name: str        — name of this registry (e.g. "Mainnet")
  - created_at: str  — timestamp string when this registry was created

Methods:
  - register(symbol, price, decimals=18)
      Raises ValueError if symbol already exists. Increments _count.
  - get(symbol)
      Returns token dict or raises KeyError with a helpful message.
  - remove(symbol)
      Removes a token. Raises KeyError if not found.
  - all_symbols()
      Returns sorted list of all registered symbols.
  - count() — @classmethod returning _count
  - summary() — prints a formatted table of all tokens

Test:
  1. mainnet = TokenRegistry("Mainnet")
  2. Register ETH, BTC, USDC, UNI
  3. Try registering ETH again — catch ValueError
  4. Print mainnet.count() and mainnet.summary()
  5. testnet = TokenRegistry("Testnet"), register WETH
  6. Show _count includes both registries' tokens
"""

# YOUR CODE HERE


# ─────────────────────────────────────────────────────────────
# EXERCISE 3 — Dunder methods: LiquidityPool
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 3: LiquidityPool with dunders ──")
"""
Write a LiquidityPool class:

  Attributes:
    - token0 (str)     — first token symbol
    - token1 (str)     — second token symbol
    - reserve0 (float) — amount of token0 in pool
    - reserve1 (float) — amount of token1 in pool
    - fee_tier (int)   — in basis points (500 = 0.05%)

  Properties (@property):
    - price      → reserve1 / reserve0
    - pair_name  → "token0/token1"
    - fee_pct    → fee_tier / 10_000  (as a decimal, e.g. 0.0005)

  Regular method:
    - calculate_tvl(price0_usd, price1_usd)
        → reserve0 * price0_usd + reserve1 * price1_usd

  Dunder methods:
    - __repr__ → LiquidityPool('USDC/ETH', fee=0.05%, price=3247.85)
    - __str__  → "USDC/ETH | Price: 3,247.85 | Fee: 0.05%"
    - __eq__   → equal if same pair regardless of order (USDC/ETH == ETH/USDC)
    - __gt__   → pool A > pool B if pool A has higher reserve0
    - __lt__   → pool A < pool B if pool A has lower reserve0

Test:
  pool1 = LiquidityPool("USDC", "ETH",  1_000_000, 308.0, fee_tier=500)
  pool2 = LiquidityPool("USDC", "ETH",  500_000,   154.0, fee_tier=3000)
  pool3 = LiquidityPool("ETH",  "USDC", 308.0,     1_000_000, fee_tier=500)

  Print pool1.price, pool1.pair_name, pool1.calculate_tvl(1.0, 3247.85)
  Test: pool1 == pool3, pool1 > pool2, sorted([pool2, pool1])
"""

# YOUR CODE HERE


# ─────────────────────────────────────────────────────────────
# EXERCISE 4 — Inheritance: DeFi Protocol hierarchy
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 4: Protocol inheritance hierarchy ──")
"""
Protocol (parent)
  - name, chain, tvl_usd
  - tvl_formatted() → "$5.20B" / "$420.00M" / "$12.50K"
  - info() → basic one-line description

DEX(Protocol)
  - volume_24h, fee_tier (decimal, e.g. 0.003)
  - fees_24h (@property) → volume_24h * fee_tier
  - apr_estimate (@property) → fees_24h * 365 / tvl_usd * 100
  - Override info() to include volume and APR
  - is_high_yield(threshold=20.0) → True if apr > threshold

LendingProtocol(Protocol)
  - total_borrowed
  - utilisation (@property) → total_borrowed / tvl_usd * 100
  - Override info() to include utilisation
  - borrow_apr(base_rate=2.0) → base_rate * (1 + utilisation/100)

Test:
  uniswap = DEX("Uniswap V3", "ethereum", 5_200_000_000, 1_800_000_000, 0.003)
  gmx     = DEX("GMX", "arbitrum", 680_000_000, 310_000_000, 0.001)
  aave    = LendingProtocol("Aave V3", "ethereum", 12_800_000_000, 8_200_000_000)

  for p in [uniswap, gmx, aave]:
      print(p.info())

  isinstance checks, is_high_yield(), borrow_apr()
  sorted by tvl_usd descending
"""

# YOUR CODE HERE


# ─────────────────────────────────────────────────────────────
# EXERCISE 5 — @property: PriceOracle
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 5: PriceOracle with @property ──")
"""
Write a PriceOracle class:

  Attributes:
    - symbol (str)
    - _price (float)         — private, exposed via @property
    - _price_history (list)  — past prices, most recent last
    - decimals (int, default 18)

  Properties:
    - price (getter) → return _price
    - price (setter) → validate > 0, save old price to history, update _price
    - change_24h → (current - first_in_history) / first_in_history * 100
                   Return 0.0 if history has fewer than 1 entry
    - high  → max of all prices including current
    - low   → min of all prices including current
    - all_prices → _price_history + [_price]

  Dunder methods:
    - __repr__ → PriceOracle('ETH', price=3247.85, history=5)
    - __str__  → "ETH: $3,247.85 | 24h: +2.40% | High: $3,400.00 | Low: $3,050.00"

Test:
  oracle = PriceOracle("ETH", 3050.0)
  for price in [3120.0, 3247.85, 3310.0, 3290.0, 3350.0, 3247.85]:
      oracle.price = price

  print(oracle)
  print("High:", oracle.high)
  print("Low:", oracle.low)
  print("All prices:", oracle.all_prices)

  try:
      oracle.price = -100
  except ValueError as e:
      print("Error:", e)
"""

# YOUR CODE HERE


# ─────────────────────────────────────────────────────────────
# EXERCISE 6 — Full class: Transaction
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 6: Full Transaction class ──")
"""
Build a complete Transaction class:

  Attributes:
    - tx_hash, from_address, to_address
    - value_wei (int), gas_used (int), gas_price_gwei (float)
    - block_number (int)
    - status (str)   — "success" or "failed"
    - tx_type (str)  — "transfer", "swap", "contract_call", etc.

  Properties:
    - value_eth        → value_wei / 1e18
    - gas_cost_eth     → gas_used * gas_price_gwei * 1e9 / 1e18
    - total_cost_eth   → value_eth + gas_cost_eth
    - is_success       → status == "success"

  Methods:
    - receipt(eth_price=3247.85) → formatted multi-line string
    - summary() → one-line string

  Dunder methods:
    - __repr__ → Transaction('0xabc...', 1.5 ETH, success)
    - __str__  → "✅ 0xabc...xyz | 1.5000 ETH | 21,000 gas @ 20 Gwei"
    - __eq__   → same tx_hash (case-insensitive)
    - __lt__   → sort by value_eth ascending

Test:
  tx1 = Transaction(
      "0x5c504ed432cb51138bcf09aa5e8a410dd4a1e204ef84bfed1be16dfba1b22060",
      "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
      "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
      value_wei=1_500_000_000_000_000_000,
      gas_used=21_000, gas_price_gwei=20,
      block_number=19_847_293, status="success", tx_type="transfer")

  tx2 = Transaction(
      "0xabc123def456abc123def456abc123def456abc123def456abc123def456abc1",
      "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
      "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
      value_wei=500_000_000_000_000_000,
      gas_used=148_320, gas_price_gwei=25,
      block_number=19_847_294, status="success", tx_type="swap")

  Print: repr, str, value_eth, gas_cost_eth, receipt() for tx1
  Print: summary() for both
  Test: tx1 == tx2, sorted([tx2, tx1])
"""

# YOUR CODE HERE


# ─────────────────────────────────────────────────────────────
# CHALLENGE — Phase 1 Capstone: simple_chain.py
# ─────────────────────────────────────────────────────────────
print("\n── Challenge: simple_chain — Simulated blockchain ──")
"""
Build a minimal blockchain in pure Python using three classes.

1. Transaction
   - from_addr, to_addr, amount, timestamp
   - tx_hash property: built by hashing a string of the four fields
     Hint: import hashlib; hashlib.sha256(string.encode()).hexdigest()
   - __str__ → "0xAlice → 0xBob | 1.5 ETH"

2. Block
   - index, previous_hash, transactions (list), timestamp
   - block_hash property → sha256 of index + previous_hash + all tx hashes + timestamp
   - is_valid() → True if block_hash starts with "00" (simplified PoW)
   - __str__ → "Block #3 | 2 txns | hash: 00ab1234..."

3. Blockchain
   - chain (list of Block)
   - __init__ creates the genesis block (index=0, previous_hash="0"*64, no txns)
   - pending_transactions (list)
   - add_transaction(from_addr, to_addr, amount) → adds to pending
   - mine_block() → creates Block from pending, clears pending
   - is_valid_chain() → every block's previous_hash matches prior block's hash
   - get_balance(address) → sum of received - sum of sent across all mined txns
   - __len__ → number of blocks
   - __str__ → "Blockchain: 4 blocks | valid: True"

Demo:
  bc = Blockchain()
  bc.add_transaction("0xAlice", "0xBob",   5.0)
  bc.add_transaction("0xBob",   "0xCarol", 2.0)
  bc.mine_block()

  bc.add_transaction("0xCarol", "0xAlice", 1.0)
  bc.add_transaction("0xAlice", "0xDave",  0.5)
  bc.mine_block()

  print(bc)
  print("Chain valid:", bc.is_valid_chain())
  for block in bc.chain:
      print(block)
  print("Bob's balance:", bc.get_balance("0xBob"))
"""

# YOUR CODE HERE


print("\n" + "=" * 60)
print("Done! Check exercises_solutions.py to compare.")
print("Phase 1 complete — 6 weeks of Python foundations!")
print("=" * 60)
