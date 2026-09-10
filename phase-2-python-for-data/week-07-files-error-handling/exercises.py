"""
Week 7 Exercises — File Handling & Error Handling
Python for Blockchain Analytics | Phase 2

Instructions:
- Attempt every exercise before opening exercises_solutions.py
- Run with: python3 exercises.py
- Some exercises create files on disk — this is intentional

Free data sources used in this course (no paid key needed):
  DefiLlama  → https://api.llama.fi/protocols  (no key)
  CoinGecko  → https://api.coingecko.com/api/v3 (no key for basic endpoints)
  Etherscan  → https://api.etherscan.io/api     (free key at etherscan.io/apis)
  The Graph  → https://api.thegraph.com         (no key)
  Ankr RPC   → https://rpc.ankr.com/eth         (no key)

Solutions are in: exercises_solutions.py
"""

import csv, json, os, logging, time

print("=" * 60)
print("WEEK 7 EXERCISES — File Handling & Error Handling")
print("=" * 60)


# ─────────────────────────────────────────────────────────────
# EXERCISE 1 — Write and read a CSV
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 1: Write and read a DEX trade CSV ──")
"""
You've been given a list of DEX trades as Python dicts.

Part A — Write to CSV:
  Write them to "dex_trades.csv" with these columns:
  tx_hash, protocol, token_in, amount_in, token_out, amount_out, gas_gwei, block

Part B — Read back and analyse:
  Read the CSV back and compute:
  1. Total number of trades
  2. Trades per protocol (count)
  3. Average gas price across all trades
  4. The trade with the largest amount_out (in ETH/token terms — cast to float)

Print a summary of each finding.

Remember: everything from CSV comes back as a string — cast before arithmetic!
"""

trades = [
    {"tx_hash":"0xaaa","protocol":"Uniswap V3","token_in":"USDC","amount_in":1000.0,"token_out":"ETH","amount_out":0.3082,"gas_gwei":20,"block":19_847_293},
    {"tx_hash":"0xbbb","protocol":"Curve",     "token_in":"DAI", "amount_in":5000.0,"token_out":"USDC","amount_out":4997.5,"gas_gwei":22,"block":19_847_294},
    {"tx_hash":"0xccc","protocol":"Uniswap V3","token_in":"ETH", "amount_in":2.5,  "token_out":"USDC","amount_out":8119.0,"gas_gwei":19,"block":19_847_295},
    {"tx_hash":"0xddd","protocol":"Balancer",  "token_in":"USDC","amount_in":2000.0,"token_out":"UNI", "amount_out":155.76,"gas_gwei":25,"block":19_847_296},
    {"tx_hash":"0xeee","protocol":"Curve",     "token_in":"USDC","amount_in":10000.0,"token_out":"USDT","amount_out":9998.0,"gas_gwei":18,"block":19_847_297},
    {"tx_hash":"0xfff","protocol":"Uniswap V3","token_in":"UNI", "amount_in":100,  "token_out":"ETH", "amount_out":0.3952,"gas_gwei":21,"block":19_847_298},
]

# YOUR CODE HERE


# ─────────────────────────────────────────────────────────────
# EXERCISE 2 — JSON: Save and load API response cache
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 2: JSON cache for API responses ──")
"""
Write a function save_to_cache(data, filepath) that:
  - Adds a "cached_at" timestamp (int, unix timestamp) to the data
  - Writes the data to filepath as pretty-printed JSON (indent=2)
  - Returns the filepath

Write a function load_from_cache(filepath, max_age_minutes=60) that:
  - Returns (data, is_fresh) tuple
  - data = the loaded JSON (without the cached_at key)
  - is_fresh = True if cache is younger than max_age_minutes
  - If file doesn't exist, returns ({}, False)
  - If JSON is malformed, returns ({}, False) and prints a warning

Test:
  1. Save this protocol_data dict to "protocol_cache.json"
  2. Load it back immediately — should be fresh
  3. Print whether the cache is fresh and the TVL from the loaded data

protocol_data = {
    "name": "Aave V3",
    "chain": "ethereum",
    "tvl_usd": 12_800_000_000,
    "borrowed_usd": 8_200_000_000,
    "users_24h": 8_200,
}
"""

protocol_data = {
    "name": "Aave V3",
    "chain": "ethereum",
    "tvl_usd": 12_800_000_000,
    "borrowed_usd": 8_200_000_000,
    "users_24h": 8_200,
}

# YOUR CODE HERE


# ─────────────────────────────────────────────────────────────
# EXERCISE 3 — Error handling: Robust transaction parser
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 3: Robust transaction parser ──")
"""
Write a function parse_transaction(raw: dict, row_num: int = 0) -> dict | None
that safely parses a raw Etherscan-style transaction dict.

Expected fields in raw:
  hash, from, to, value (Wei as string), gasUsed, gasPrice, blockNumber, isError

The function should:
  - Return a clean dict with Python types on success:
    {hash, from_addr, to_addr, value_eth (float), gas_used (int),
     gas_price_gwei (float), block (int), success (bool)}
  - Return None on ANY parsing error
  - Print a descriptive warning for each failure, including which field failed

Then process this batch of raw transactions and print:
  - How many parsed successfully
  - How many failed and why (from your warning prints)
  - Total volume in ETH from successful ones
"""

raw_transactions = [
    {"hash":"0xaaa","from":"0xAlice","to":"0xBob",  "value":"1500000000000000000","gasUsed":"21000","gasPrice":"20000000000","blockNumber":"19847293","isError":"0"},
    {"hash":"0xbbb","from":"0xBob",  "to":"0xCarol","value":"not_a_number",        "gasUsed":"21000","gasPrice":"18000000000","blockNumber":"19847294","isError":"0"},
    {"hash":"0xccc","from":"0xCarol","to":"0xDave",  "value":"500000000000000000", "gasUsed":"21000","gasPrice":"22000000000","blockNumber":"19847295","isError":"1"},
    {"hash":"0xddd","to":"0xEve",                    "value":"250000000000000000", "gasUsed":"21000","gasPrice":"25000000000","blockNumber":"19847296","isError":"0"},
    {"hash":"0xeee","from":"0xDave", "to":"0xAlice", "value":"2000000000000000000","gasUsed":"21000","gasPrice":"19000000000","blockNumber":"19847297","isError":"0"},
]

# YOUR CODE HERE


# ─────────────────────────────────────────────────────────────
# EXERCISE 4 — Custom exceptions
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 4: Custom exceptions ──")
"""
Create a hierarchy of custom exceptions for a blockchain data pipeline:

  BlockchainDataError (base)
    ├── InvalidAddressError(address, reason)
    ├── StaleDataError(source, age_seconds, max_age_seconds)
    └── ProtocolNotFoundError(protocol_name, available_protocols: list)

Each exception should:
  - Store the relevant attributes (address, age_seconds, etc.)
  - Have a clear, informative __str__ message

Then write a function validate_pipeline_input(address, data_age_seconds, protocol) that:
  - Raises InvalidAddressError if address doesn't start with 0x or isn't 42 chars
  - Raises StaleDataError if data_age_seconds > 3600 (1 hour)
  - Raises ProtocolNotFoundError if protocol not in SUPPORTED_PROTOCOLS

SUPPORTED_PROTOCOLS = ["uniswap-v3", "aave-v3", "curve", "balancer", "gmx"]

Test:
  a. Valid input: ("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", 300, "uniswap-v3")
  b. Bad address: ("0xshort", 300, "uniswap-v3")
  c. Stale data:  ("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", 7200, "aave-v3")
  d. Unknown:     ("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", 300, "dydx")

For each test case, catch BlockchainDataError (the base) and print the error.
"""

SUPPORTED_PROTOCOLS = ["uniswap-v3", "aave-v3", "curve", "balancer", "gmx"]

# YOUR CODE HERE


# ─────────────────────────────────────────────────────────────
# EXERCISE 5 — Logging: Pipeline with proper logs
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 5: Logging a data pipeline ──")
"""
Rewrite the following pipeline function to use proper logging instead of print().

Rules:
  - Set up a logger named "week7.pipeline"
  - Use DEBUG for individual block/item processing details
  - Use INFO for start/end messages and summary stats
  - Use WARNING for skipped/failed items
  - Use ERROR for things that stop processing a batch (but not the whole run)
  - Format: "%(levelname)-8s | %(message)s"
  - Log to both console AND a file called "pipeline.log"

The function processes a list of blocks — each block has a list of transactions.
Some transactions have a "value" of None (simulate missing data) — log a warning and skip them.
Some blocks are "empty" (no transactions) — log at DEBUG level.

After converting, show that:
  a. Running with level=logging.INFO hides DEBUG messages
  b. Running with level=logging.DEBUG shows everything
"""

sample_blocks = [
    {"number": 19_847_000, "transactions": [
        {"hash": "0xaaa", "value": 1.5},
        {"hash": "0xbbb", "value": 0.3},
    ]},
    {"number": 19_847_001, "transactions": []},  # empty block
    {"number": 19_847_002, "transactions": [
        {"hash": "0xccc", "value": None},        # missing value
        {"hash": "0xddd", "value": 5.0},
    ]},
    {"number": 19_847_003, "transactions": [
        {"hash": "0xeee", "value": 12.0},
    ]},
]

# YOUR CODE HERE


# ─────────────────────────────────────────────────────────────
# EXERCISE 6 — Free APIs: Config file builder
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 6: API config file builder ──")
"""
Build a utility that manages API configuration stored in a JSON file.
This is the config system you'll use throughout the rest of the course.

Write a class APIConfig with:
  - __init__(config_path="api_config.json")
      Loads config from file if it exists, otherwise creates a default config
  - get_rpc(chain="ethereum") → returns first RPC URL for that chain
  - get_api_key(api_name) → returns key from environment variable,
      or "demo" if not set. Prints a warning if using "demo".
  - add_rpc(chain, url) → adds a new RPC URL to the list for that chain
  - save() → saves current config back to JSON file
  - summary() → prints a clean table of configured APIs and chains

Default config should include:
  - RPC endpoints for ethereum, polygon, arbitrum (use free ones from the lesson)
  - API info for defillama (no key), coingecko (no key), etherscan (key from env)

Test:
  config = APIConfig()
  config.summary()
  print(config.get_rpc("ethereum"))
  print(config.get_api_key("etherscan"))
  config.add_rpc("base", "https://rpc.ankr.com/base")
  config.save()
  print("Saved. Reload test:")
  config2 = APIConfig()
  print(config2.get_rpc("base"))
"""

# YOUR CODE HERE


# ─────────────────────────────────────────────────────────────
# CHALLENGE — Full pipeline: Validate → Parse → Analyse → Export
# ─────────────────────────────────────────────────────────────
print("\n── Challenge: Full robust data pipeline ──")
"""
Build a complete pipeline function:

  process_wallet_csv(input_path, output_path, log_path)

It should:

Step 1 — READ: Load a CSV of wallet holdings (same format as Exercise 1 but more fields)
  Expected columns: wallet, token, raw_amount, decimals, price_usd
  Handle missing files → raise a clear error
  Handle missing columns → log error for that row, skip it
  Handle bad values → log warning for that row, skip it

Step 2 — VALIDATE: For each row
  - wallet must start with 0x and be 42 chars
  - raw_amount must be a positive integer
  - decimals must be between 0 and 18
  - price_usd must be > 0
  Log invalid rows as warnings, skip them

Step 3 — ENRICH: Add computed fields
  - amount_human = raw_amount / 10**decimals
  - value_usd    = amount_human * price_usd

Step 4 — AGGREGATE: Build wallet summaries
  - total_value_usd per wallet
  - number of tokens per wallet
  - largest single holding (token + value_usd)

Step 5 — EXPORT: Write two files
  - output_path: enriched CSV with all valid rows + computed fields
  - A JSON summary of the aggregated wallet data

Step 6 — LOG everything properly using the logging module

Create a sample CSV first, then run the pipeline on it.
Print the JSON summary at the end.
"""

# Create sample input CSV
sample_holdings = [
    "wallet,token,raw_amount,decimals,price_usd",
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045,ETH,3500000000000000000,18,3247.85",
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045,USDC,5000000000,6,1.00",
    "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984,UNI,500000000000000000000,18,12.84",
    "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984,ETH,1000000000000000000,18,3247.85",
    "0xBadAddress,ETH,1000000000000000000,18,3247.85",          # bad address
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045,AAVE,not_a_number,18,98.50",  # bad amount
    "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D,WBTC,10000000,8,67412.0",
    "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D,ETH,500000000000000000,18,-100", # bad price
]

with open("wallet_holdings.csv", "w") as f:
    f.write("\n".join(sample_holdings))

# YOUR CODE HERE: implement process_wallet_csv and call it


print("\n" + "=" * 60)
print("Exercises complete! Check exercises_solutions.py to compare.")
print("=" * 60)
