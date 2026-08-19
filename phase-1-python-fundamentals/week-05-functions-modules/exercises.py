"""
Week 5 Exercises — Functions & Modules
Python for Blockchain Analytics | Phase 1

Instructions:
- Attempt EVERY exercise before checking exercises_solutions.py
- Write your solution where you see # YOUR CODE HERE
- Run with: python3 exercises.py
- Check your output makes sense before peeking at solutions

Solutions are in: exercises_solutions.py
"""

print("=" * 60)
print("WEEK 5 EXERCISES — Functions & Modules")
print("=" * 60)


# ─────────────────────────────────────────────────────────────
# EXERCISE 1 — Basic functions: Gas fee calculator
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 1: Gas fee calculator ──")
"""
Write a function gas_fee_usd(gas_used, gas_price_gwei, eth_price_usd)
that returns the total gas fee in USD.

Formula: gas_fee_usd = (gas_used * gas_price_gwei * 1e9 / 1e18) * eth_price_usd

Then test it with these scenarios:
  a. Simple ETH transfer:  gas_used=21_000,  gas_price=20 gwei, eth=$3247.85
  b. Uniswap swap:         gas_used=150_000, gas_price=25 gwei, eth=$3247.85
  c. Contract deployment:  gas_used=800_000, gas_price=18 gwei, eth=$3247.85

Print each result as: "Transfer:    $X.XXXX"
"""

# YOUR CODE HERE



# ─────────────────────────────────────────────────────────────
# EXERCISE 2 — Default arguments: Token formatter
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 2: Token amount formatter ──")
"""
Write a function format_amount(raw_amount, symbol, decimals=18, precision=4)
that converts a raw token integer to a human-readable string.

Examples:
  format_amount(1_500_000_000_000_000_000, "ETH")
    → "1.5000 ETH"
  format_amount(1_500_000, "USDC", decimals=6)
    → "1.5000 USDC"
  format_amount(1_500_000, "USDC", decimals=6, precision=2)
    → "1.50 USDC"
  format_amount(1_284_000_000_000_000_000, "UNI", precision=2)
    → "1.28 UNI"

Test all four examples above and print the results.
"""

# YOUR CODE HERE


# ─────────────────────────────────────────────────────────────
# EXERCISE 3 — Return multiple values: Position health checker
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 3: Position health checker ──")
"""
Write a function check_position(collateral_eth, debt_usd, eth_price, threshold=0.825)
that returns a TUPLE of four values:
  (collateral_value_usd, health_factor, liquidation_price, status)

Formulas:
  collateral_value_usd = collateral_eth * eth_price
  health_factor        = (collateral_value_usd * threshold) / debt_usd
  liquidation_price    = debt_usd / (collateral_eth * threshold)
  status               = "✅ Safe"    if health_factor >= 1.5
                         "⚠️  Warning" if 1.0 <= health_factor < 1.5
                         "🚨 At Risk"  if health_factor < 1.0

Test with these three positions:
  a. collateral=10 ETH, debt=$20,000, eth_price=$3,247.85
  b. collateral=5  ETH, debt=$12,000, eth_price=$3,247.85
  c. collateral=3  ETH, debt=$10,500, eth_price=$3,247.85

For each position print:
  "Collateral: $X | HF: X.XX | Liq: $X | Status: ..."
"""

# YOUR CODE HERE


# ─────────────────────────────────────────────────────────────
# EXERCISE 4 — *args: Multi-wallet volume aggregator
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 4: Multi-wallet volume aggregator ──")
"""
Write a function total_volume(*wallet_volumes) that:
  - Accepts any number of positional float arguments (each is a wallet's volume in ETH)
  - Returns a dict with keys:
      "count"   → number of wallets
      "total"   → sum of all volumes
      "average" → average volume
      "max"     → highest single wallet volume
      "min"     → lowest single wallet volume

Test with:
  a. 3 wallets:  total_volume(5.2, 18.7, 0.3)
  b. 5 wallets:  total_volume(250.0, 12.5, 0.8, 45.3, 3.1)
  c. 1 wallet:   total_volume(100.0)

Print results for each call in a readable format.
"""

# YOUR CODE HERE


# ─────────────────────────────────────────────────────────────
# EXERCISE 5 — **kwargs: API request builder
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 5: Etherscan API request builder ──")
"""
Write a function build_etherscan_url(action, api_key="demo", **params)
that builds a full Etherscan API URL.

Base URL: "https://api.etherscan.io/api"
Always include: module="account", action=action, apikey=api_key
Add any extra **params to the query string.

Test with these calls:
  a. build_etherscan_url("txlist", address="0xd8dA...6045", startblock=0, endblock=99999999)
  b. build_etherscan_url("tokentx", address="0xd8dA...6045", contractaddress="0xA0b8...eB48")
  c. build_etherscan_url("balance", api_key="MYKEY123", address="0xd8dA...6045", tag="latest")

Print each URL. It should look like:
  https://api.etherscan.io/api?module=account&action=txlist&apikey=demo&address=...&startblock=0&...
"""

# YOUR CODE HERE


# ─────────────────────────────────────────────────────────────
# EXERCISE 6 — Lambda: Token list sorter
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 6: Token list sorter ──")
"""
Given the tokens list below, use lambda functions with sorted() to produce:
  1. Sorted by price ascending
  2. Sorted by market_cap descending
  3. Sorted by 24h_change descending (best performers first)
  4. Sorted by name alphabetically
  5. Sorted by volume/market_cap ratio descending (capital efficiency)

For each sort, print: "Rank. SYMBOL ($price) — sort_value"

tokens = [
    {"symbol":"ETH",  "name":"Ethereum",   "price":3247.85, "market_cap":390e9, "volume_24h":15.8e9, "change_24h":2.4},
    {"symbol":"BTC",  "name":"Bitcoin",    "price":67412.0, "market_cap":1320e9,"volume_24h":32.0e9, "change_24h":-0.8},
    {"symbol":"UNI",  "name":"Uniswap",    "price":12.84,   "market_cap":9.7e9, "volume_24h":180e6,  "change_24h":-1.2},
    {"symbol":"AAVE", "name":"Aave",       "price":98.50,   "market_cap":1.47e9,"volume_24h":95e6,   "change_24h":3.1},
    {"symbol":"ARB",  "name":"Arbitrum",   "price":1.24,    "market_cap":1.57e9,"volume_24h":420e6,  "change_24h":-0.5},
    {"symbol":"CRV",  "name":"Curve DAO",  "price":0.48,    "market_cap":630e6, "volume_24h":130e6,  "change_24h":1.8},
]
"""

# YOUR CODE HERE
tokens = [
    {"symbol":"ETH",  "name":"Ethereum",   "price":3247.85, "market_cap":390e9, "volume_24h":15.8e9, "change_24h":2.4},
    {"symbol":"BTC",  "name":"Bitcoin",    "price":67412.0, "market_cap":1320e9,"volume_24h":32.0e9, "change_24h":-0.8},
    {"symbol":"UNI",  "name":"Uniswap",    "price":12.84,   "market_cap":9.7e9, "volume_24h":180e6,  "change_24h":-1.2},
    {"symbol":"AAVE", "name":"Aave",       "price":98.50,   "market_cap":1.47e9,"volume_24h":95e6,   "change_24h":3.1},
    {"symbol":"ARB",  "name":"Arbitrum",   "price":1.24,    "market_cap":1.57e9,"volume_24h":420e6,  "change_24h":-0.5},
    {"symbol":"CRV",  "name":"Curve DAO",  "price":0.48,    "market_cap":630e6, "volume_24h":130e6,  "change_24h":1.8},
]


# ─────────────────────────────────────────────────────────────
# EXERCISE 7 — Scope: Safe global config
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 7: Safe global config with functions ──")
"""
You need a global ETH_PRICE that functions can read,
but should only be updated through a dedicated setter.

Do the following:
  1. Define a module-level variable ETH_PRICE = 3247.85
  2. Write get_eth_price() → returns current ETH_PRICE
  3. Write set_eth_price(new_price) → updates ETH_PRICE (use global keyword)
     - Raise ValueError if new_price <= 0
  4. Write eth_value(amount_eth) → returns amount_eth * ETH_PRICE (reads global)
  5. Write usd_value(amount_usd) → returns amount_usd / ETH_PRICE (reads global)

Test:
  a. Print eth_value(2.5) using initial price
  b. Update price to 3500.00
  c. Print eth_value(2.5) using new price
  d. Try set_eth_price(-100) — should raise ValueError
  e. Print usd_value(10_000)
"""

# YOUR CODE HERE


# ─────────────────────────────────────────────────────────────
# EXERCISE 8 — Module design: blockchain_utils extension
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 8: Extend blockchain_utils ──")
"""
Write THREE new utility functions that would belong in blockchain_utils.py.

Requirements for each function:
  - Proper docstring (what it does, args, returns, example)
  - Type hints on all parameters and return value
  - At least one default argument
  - Handle edge cases (e.g. division by zero, invalid input)

Suggestions (pick any 3 or invent your own):
  a. apy_to_apr(apy, compound_periods=365) → float
     Convert APY to APR: APR = ((1 + APY/100)**(1/n) - 1) * n * 100

  b. tvl_per_user(tvl_usd, user_count) → float
     Return TVL divided by users, handle zero users

  c. trade_slippage(expected_price, actual_price) → float
     Return slippage as a percentage

  d. block_to_timestamp_estimate(block_number, known_block, known_ts, avg_block_time=12.0) → float
     Estimate Unix timestamp for any block given a reference point

  e. format_tx_hash(tx_hash, style="short") → str
     style="short" → "0xabc...xyz"
     style="full"  → full hash
     style="link"  → https://etherscan.io/tx/0xabc...

Write and test all three below.
"""

# YOUR CODE HERE


# ─────────────────────────────────────────────────────────────
# CHALLENGE — Full transaction analyser function
# ─────────────────────────────────────────────────────────────
print("\n── Challenge: Full transaction analyser ──")
"""
Write a function analyse_transactions(transactions, eth_price, min_value_eth=0.0)
that takes:
  - transactions: list of dicts (each has hash, value_eth, gas_used,
                  gas_price_gwei, status, type)
  - eth_price: current ETH price in USD
  - min_value_eth: filter out transactions below this value (default 0 — include all)

And returns a dict with:
  {
    "total_txns":      int,
    "success_count":   int,
    "failed_count":    int,
    "success_rate":    float,   # percentage
    "total_volume_eth":float,
    "total_volume_usd":float,
    "avg_tx_eth":      float,
    "largest_tx_eth":  float,
    "total_gas_usd":   float,
    "avg_gas_gwei":    float,
    "type_breakdown":  dict,    # {type: count}
    "filtered_out":    int,     # txns excluded by min_value_eth
  }

Then write a print_tx_report(analysis_result, title="Transaction Report") function
that prints the dict in a clean formatted table.

Test with the transactions list below.
"""

# YOUR CODE HERE
transactions = [
    {"hash":"0x001","value_eth":0.5,  "gas_used":21_000,  "gas_price_gwei":20,"status":"success","type":"transfer"},
    {"hash":"0x002","value_eth":12.0, "gas_used":150_000, "gas_price_gwei":25,"status":"success","type":"swap"},
    {"hash":"0x003","value_eth":0.001,"gas_used":21_000,  "gas_price_gwei":15,"status":"failed", "type":"transfer"},
    {"hash":"0x004","value_eth":75.0, "gas_used":21_000,  "gas_price_gwei":45,"status":"success","type":"transfer"},
    {"hash":"0x005","value_eth":0.05, "gas_used":160_000, "gas_price_gwei":22,"status":"success","type":"swap"},
    {"hash":"0x006","value_eth":2.1,  "gas_used":155_000, "gas_price_gwei":28,"status":"failed", "type":"swap"},
    {"hash":"0x007","value_eth":1.2,  "gas_used":250_000, "gas_price_gwei":30,"status":"success","type":"liquidity"},
    {"hash":"0x008","value_eth":0.08, "gas_used":180_000, "gas_price_gwei":19,"status":"success","type":"NFT"},
    {"hash":"0x009","value_eth":5.5,  "gas_used":148_000, "gas_price_gwei":24,"status":"success","type":"swap"},
    {"hash":"0x010","value_eth":0.0,  "gas_used":21_000,  "gas_price_gwei":12,"status":"failed", "type":"NFT"},
]

ETH_PRICE = 3247.85

# Call your function here:
# result = analyse_transactions(transactions, ETH_PRICE)
# print_tx_report(result)
# print()
# result_filtered = analyse_transactions(transactions, ETH_PRICE, min_value_eth=1.0)
# print_tx_report(result_filtered, title="Large Transactions Only (>1 ETH)")


print("\n" + "=" * 60)
print("Done! Check exercises_solutions.py to compare your answers.")
print("=" * 60)
