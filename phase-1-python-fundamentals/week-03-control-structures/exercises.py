"""
Week 3 Exercises — Control Structures: Loops & Conditionals
Python for Blockchain Analytics | Phase 1

Instructions:
- Try each exercise before looking at the solution
- Run with: python3 exercises.py
- SQL parallels are noted where relevant — lean on what you know

SQL analyst reminder:
  if/elif/else  ≈  CASE WHEN ... THEN ... ELSE ... END
  for loop      ≈  processing each row from a SELECT result
  continue      ≈  WHERE clause filtering
  accumulating  ≈  SUM(), COUNT(), AVG()
"""

print("=" * 60)
print("WEEK 3 EXERCISES — Control Structures")
print("=" * 60)


# ─────────────────────────────────────────────────────────────
# EXERCISE 1 — if/elif/else: Gas price tier labeler
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 1: Gas price tier labeler ──")
"""
Write a function gas_tier(gwei) that returns a label based on gas price:
  < 10 gwei   → "🟢 Low — great time to transact"
  10–29 gwei  → "🟡 Normal — reasonable"
  30–49 gwei  → "🟠 High — consider waiting"
  50–99 gwei  → "🔴 Very High — network congested"
  >= 100 gwei → "🚨 Extreme — only transact if urgent"

Test with these values: 7, 25, 38, 72, 150
Expected output:
  7 gwei   → 🟢 Low — great time to transact
  25 gwei  → 🟡 Normal — reasonable
  38 gwei  → 🟠 High — consider waiting
  72 gwei  → 🔴 Very High — network congested
  150 gwei → 🚨 Extreme — only transact if urgent


"""

# YOUR CODE HERE
def gas_tier(gwei):
    if gwei < 10:
        return "🟢 Low — great time to transact"
    elif gwei < 30:
        return "🟡 Normal — reasonable"
    elif gwei < 50:
        return "🟠 High — consider waiting"
    elif gwei < 100:
        return "🔴 Very High — network congested"
    else:
        return "🚨 Extreme — only transact if urgent"

for gwei in [7, 25, 38, 72, 150]:
    print(f"  {gwei:>3} gwei → {gas_tier(gwei)}")

# Solution:
# def gas_tier(gwei):
#     if gwei < 10:   return "🟢 Low — great time to transact"
#     elif gwei < 30: return "🟡 Normal — reasonable"
#     elif gwei < 50: return "🟠 High — consider waiting"
#     elif gwei < 100:return "🔴 Very High — network congested"
#     else:           return "🚨 Extreme — only transact if urgent"


# ─────────────────────────────────────────────────────────────
# EXERCISE 2 — Logical operators: Token safety checker
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 2: Token safety checker ──")
"""
SQL parallel: WHERE is_verified = TRUE AND NOT is_flagged AND liquidity_usd > 500000

Write a function is_safe_token(token) that returns True only if ALL of:
  - is_verified is True
  - is_flagged is False
  - liquidity_usd >= 500_000
  - age_days >= 30

Then check each token in the list and print:
  "TOKEN_SYMBOL → Safe: True/False"

tokens = [
    {"symbol": "UNI",   "is_verified": True,  "is_flagged": False, "liquidity_usd": 5_000_000, "age_days": 1200},
    {"symbol": "SCAM1", "is_verified": False, "is_flagged": True,  "liquidity_usd": 50_000,    "age_days": 3},
    {"symbol": "NEW1",  "is_verified": True,  "is_flagged": False, "liquidity_usd": 800_000,   "age_days": 15},
    {"symbol": "RUGP",  "is_verified": True,  "is_flagged": True,  "liquidity_usd": 2_000_000, "age_days": 60},
    {"symbol": "AAVE",  "is_verified": True,  "is_flagged": False, "liquidity_usd": 80_000_000,"age_days": 1400},
]
"""

# YOUR CODE HERE
def is_safe_token(token):
    return (
        token["is_verified"]
        and not token["is_flagged"]
        and token["liquidity_usd"] >= 500_000
        and token["age_days"] >= 30
    )

tokens = [
    {"symbol": "UNI",   "is_verified": True,  "is_flagged": False, "liquidity_usd": 5_000_000,  "age_days": 1200},
    {"symbol": "SCAM1", "is_verified": False,  "is_flagged": True,  "liquidity_usd": 50_000,     "age_days": 3},
    {"symbol": "NEW1",  "is_verified": True,  "is_flagged": False, "liquidity_usd": 800_000,    "age_days": 15},
    {"symbol": "RUGP",  "is_verified": True,  "is_flagged": True,  "liquidity_usd": 2_000_000,  "age_days": 60},
    {"symbol": "AAVE",  "is_verified": True,  "is_flagged": False, "liquidity_usd": 80_000_000, "age_days": 1400},
]

for token in tokens:
    safe = is_safe_token(token)
    icon = "✅" if safe else "❌"
    print(f"  {icon} {token['symbol']:6} → Safe: {safe}")

# Solution:
# def is_safe_token(token):
#     return (
#         token["is_verified"]
#         and not token["is_flagged"]
#         and token["liquidity_usd"] >= 500_000
#         and token["age_days"] >= 30
#     )


# ─────────────────────────────────────────────────────────────
# EXERCISE 3 — for loop: DEX volume aggregator
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 3: DEX volume aggregator ──")
"""
SQL parallel:
  SELECT protocol, SUM(volume_usd) AS total_volume, COUNT(*) AS trade_count
  FROM dex_trades
  GROUP BY protocol

Given this list of trades, calculate per-protocol:
  - total volume (USD)
  - number of trades

Print a summary table sorted by total volume descending.

trades = [
    {"protocol": "Uniswap v3", "volume_usd": 125_000},
    {"protocol": "Curve",      "volume_usd": 340_000},
    {"protocol": "Uniswap v3", "volume_usd": 87_500},
    {"protocol": "Balancer",   "volume_usd": 52_000},
    {"protocol": "Curve",      "volume_usd": 210_000},
    {"protocol": "Uniswap v3", "volume_usd": 430_000},
    {"protocol": "Balancer",   "volume_usd": 18_000},
    {"protocol": "Curve",      "volume_usd": 95_000},
]

Expected output format:
  Protocol       Trades    Volume (USD)
  Uniswap v3        3      $642,500.00
  Curve             3      $645,000.00
  Balancer          2       $70,000.00
(sorted by volume desc)
"""

# YOUR CODE HERE
trades = [
    {"protocol": "Uniswap v3", "volume_usd": 125_000},
    {"protocol": "Curve",      "volume_usd": 340_000},
    {"protocol": "Uniswap v3", "volume_usd": 87_500},
    {"protocol": "Balancer",   "volume_usd": 52_000},
    {"protocol": "Curve",      "volume_usd": 210_000},
    {"protocol": "Uniswap v3", "volume_usd": 430_000},
    {"protocol": "Balancer",   "volume_usd": 18_000},
    {"protocol": "Curve",      "volume_usd": 95_000},
]

# Aggregate
protocol_stats = {}
for trade in trades:
    p = trade["protocol"]
    if p not in protocol_stats:
        protocol_stats[p] = {"trades": 0, "volume_usd": 0}
    protocol_stats[p]["trades"]     += 1
    protocol_stats[p]["volume_usd"] += trade["volume_usd"]

# Sort by volume descending
sorted_protocols = sorted(protocol_stats.items(), key=lambda x: x[1]["volume_usd"], reverse=True)

# Print table
print(f"\n  {'Protocol':<15} {'Trades':>6}   {'Volume (USD)':>14}")
print("  " + "-" * 40)
for protocol, stats in sorted_protocols:
    print(f"  {protocol:<15} {stats['trades']:>6}   ${stats['volume_usd']:>13,.2f}")

# Solution: see above — uses a dict to accumulate, then sorts with sorted()


# ─────────────────────────────────────────────────────────────
# EXERCISE 4 — break and continue: Transaction scanner
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 4: Transaction scanner ──")
"""
Given the list of transactions below:

1. Use `continue` to skip any transaction where status is "failed"
2. Use `break` to stop scanning once you find a transaction
   with value_eth >= 100 (a whale tx)
3. Print each processed transaction as:
   "✅ 0xabc... | 2.500 ETH"
4. After the loop, print how many were processed before stopping

transactions = [
    {"hash": "0xaaa111", "value_eth": 1.5,   "status": "success"},
    {"hash": "0xbbb222", "value_eth": 0.3,   "status": "failed"},
    {"hash": "0xccc333", "value_eth": 4.2,   "status": "success"},
    {"hash": "0xddd444", "value_eth": 0.1,   "status": "failed"},
    {"hash": "0xeee555", "value_eth": 150.0,  "status": "success"},  # whale — stop here
    {"hash": "0xfff666", "value_eth": 2.1,   "status": "success"},   # should NOT be reached
]
"""

# YOUR CODE HERE
transactions = [
    {"hash": "0xaaa111", "value_eth": 1.5,   "status": "success"},
    {"hash": "0xbbb222", "value_eth": 0.3,   "status": "failed"},
    {"hash": "0xccc333", "value_eth": 4.2,   "status": "success"},
    {"hash": "0xddd444", "value_eth": 0.1,   "status": "failed"},
    {"hash": "0xeee555", "value_eth": 150.0, "status": "success"},
    {"hash": "0xfff666", "value_eth": 2.1,   "status": "success"},
]

processed = 0

for tx in transactions:
    if tx["status"] == "failed":
        print(f"  ⏭️  {tx['hash']} | skipped (failed)")
        continue

    if tx["value_eth"] >= 100:
        print(f"  🐋 {tx['hash']} | {tx['value_eth']:.3f} ETH — WHALE! Stopping scan.")
        processed += 1
        break

    print(f"  ✅ {tx['hash']} | {tx['value_eth']:.3f} ETH")
    processed += 1

print(f"\n  Processed {processed} transactions before stopping.")

# Solution: see above


# ─────────────────────────────────────────────────────────────
# EXERCISE 5 — while loop: Block confirmation poller
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 5: Block confirmation poller ──")
"""
Simulate waiting for a transaction to reach 12 confirmations.

A "confirmation" = each new block mined after the block containing the tx.
  tx_block        = 19_847_293
  current_block   = 19_847_293  (starts at same block as tx)
  target_confirms = 12

Use a while loop that:
  - Increments current_block by 1 each iteration (simulating a new block)
  - Calculates confirmations = current_block - tx_block
  - Prints: "  Block 19,847,294 | Confirmations: 1/12"
  - Stops when confirmations >= 12
  - Prints "✅ Transaction confirmed!" at the end

Hint: you'll also need a safety cap — add:
  if current_block > tx_block + 50:
      print("⚠️  Timeout — something is wrong")
      break
"""

# YOUR CODE HERE
tx_block        = 19_847_293
current_block   = 19_847_293
target_confirms = 12

print(f"\n  Waiting for {target_confirms} confirmations on tx in block {tx_block:,}...\n")

while True:
    current_block += 1
    confirmations  = current_block - tx_block

    print(f"  Block {current_block:,} | Confirmations: {confirmations}/{target_confirms}")

    if confirmations >= target_confirms:
        print(f"\n  ✅ Transaction confirmed after {confirmations} blocks!")
        break

    if current_block > tx_block + 50:
        print("  ⚠️  Timeout — something is wrong")
        break

# Solution: see above


# ─────────────────────────────────────────────────────────────
# EXERCISE 6 — Nested loops: Multi-wallet, multi-token screener
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 6: Multi-wallet token screener ──")
"""
SQL parallel:
  SELECT w.address, t.symbol, t.balance_usd
  FROM wallets w JOIN holdings h ON w.id = h.wallet_id JOIN tokens t ON h.token_id = t.id
  WHERE t.is_flagged = TRUE

For each wallet, loop through their holdings.
If any holding is a flagged token, print a warning for that wallet.
Count how many wallets hold at least one flagged token.

FLAGGED_TOKENS = ["SQUID", "LUNA", "FTT", "TITAN"]

wallets = [
    {"address": "0xWallet1", "holdings": ["ETH", "USDC", "UNI"]},
    {"address": "0xWallet2", "holdings": ["ETH", "SQUID", "BTC"]},
    {"address": "0xWallet3", "holdings": ["DAI", "AAVE", "LUNA"]},
    {"address": "0xWallet4", "holdings": ["ETH", "BTC", "SOL"]},
    {"address": "0xWallet5", "holdings": ["FTT", "SRM", "MAPS"]},
]

Expected output:
  ✅ 0xWallet1 — clean
  ⚠️  0xWallet2 — holds flagged token: SQUID
  ⚠️  0xWallet3 — holds flagged token: LUNA
  ✅ 0xWallet4 — clean
  ⚠️  0xWallet5 — holds flagged token: FTT

  2 of 5 wallets hold clean portfolios.
  3 wallets flagged for review.
"""

# YOUR CODE HERE
FLAGGED_TOKENS = ["SQUID", "LUNA", "FTT", "TITAN"]

wallets = [
    {"address": "0xWallet1", "holdings": ["ETH", "USDC", "UNI"]},
    {"address": "0xWallet2", "holdings": ["ETH", "SQUID", "BTC"]},
    {"address": "0xWallet3", "holdings": ["DAI", "AAVE", "LUNA"]},
    {"address": "0xWallet4", "holdings": ["ETH", "BTC", "SOL"]},
    {"address": "0xWallet5", "holdings": ["FTT", "SRM", "MAPS"]},
]

flagged_wallets = 0

for wallet in wallets:
    found_flagged = None
    for token in wallet["holdings"]:
        if token in FLAGGED_TOKENS:
            found_flagged = token
            break   # one flagged token is enough to flag the wallet

    if found_flagged:
        print(f"  ⚠️  {wallet['address']} — holds flagged token: {found_flagged}")
        flagged_wallets += 1
    else:
        print(f"  ✅ {wallet['address']} — clean")

clean_wallets = len(wallets) - flagged_wallets
print(f"\n  {clean_wallets} of {len(wallets)} wallets hold clean portfolios.")
print(f"  {flagged_wallets} wallets flagged for review.")

# Solution: see above


# ─────────────────────────────────────────────────────────────
# EXERCISE 7 — range(): Block range scanner
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 7: Block range revenue calculator ──")
"""
Simulate scanning a block range to calculate protocol revenue.

For blocks 19_847_000 to 19_847_099 (100 blocks):
  - Every block generates a "fee" between 0.01 and 0.5 ETH
    Use this formula to simulate it (deterministic, no randomness):
      fee = 0.01 + (block_number % 50) * 0.01
  - Accumulate total_fees_eth
  - Count blocks where fee > 0.3 ETH (high-fee blocks)
  - Track the highest single-block fee

Print:
  "Scanned 100 blocks"
  "Total fees: X.XXXX ETH"
  "High-fee blocks (>0.3 ETH): N"
  "Peak block fee: X.XXXX ETH"
"""

# YOUR CODE HERE
START_BLOCK   = 19_847_000
END_BLOCK     = 19_847_099
total_fees    = 0
high_fee_blocks = 0
peak_fee      = 0

for block in range(START_BLOCK, END_BLOCK + 1):
    fee = 0.01 + (block % 50) * 0.01

    total_fees += fee

    if fee > 0.3:
        high_fee_blocks += 1

    if fee > peak_fee:
        peak_fee = fee

blocks_scanned = END_BLOCK - START_BLOCK + 1
print(f"\n  Scanned {blocks_scanned} blocks")
print(f"  Total fees: {total_fees:.4f} ETH")
print(f"  High-fee blocks (>0.3 ETH): {high_fee_blocks}")
print(f"  Peak block fee: {peak_fee:.4f} ETH")

# Solution: see above


# ─────────────────────────────────────────────────────────────
# CHALLENGE — Full wallet activity report
# ─────────────────────────────────────────────────────────────
print("\n── Challenge: Full Wallet Activity Report ──")
"""
Build a complete wallet analysis report from this transaction list.

Calculate:
  1. Total txns, success count, failed count, success rate
  2. Total volume (ETH) from successful txns only
  3. Average, min, max transaction value (successful only)
  4. Count by tx type (transfer, swap, liquidity, NFT)
  5. Most common tx type
  6. Flag wallet if failed_rate > 30% → "⚠️ Suspicious failure rate"
  7. Classify wallet: Whale (any tx >= 50 ETH), DeFi Trader (3+ swaps),
     LP (any liquidity tx), NFT Collector (2+ NFT txns), or Regular User

transactions = [
    {"hash":"0x001","value_eth":0.5,  "status":"success","type":"transfer"},
    {"hash":"0x002","value_eth":12.0, "status":"success","type":"swap"},
    {"hash":"0x003","value_eth":0.001,"status":"failed", "type":"transfer"},
    {"hash":"0x004","value_eth":75.0, "status":"success","type":"transfer"},
    {"hash":"0x005","value_eth":0.05, "status":"success","type":"swap"},
    {"hash":"0x006","value_eth":2.1,  "status":"failed", "type":"swap"},
    {"hash":"0x007","value_eth":1.2,  "status":"success","type":"liquidity"},
    {"hash":"0x008","value_eth":0.08, "status":"success","type":"NFT"},
    {"hash":"0x009","value_eth":5.5,  "status":"success","type":"swap"},
    {"hash":"0x010","value_eth":0.0,  "status":"failed", "type":"NFT"},
    {"hash":"0x011","value_eth":0.15, "status":"success","type":"NFT"},
    {"hash":"0x012","value_eth":3.3,  "status":"success","type":"swap"},
]
"""

# YOUR CODE HERE
transactions = [
    {"hash":"0x001","value_eth":0.5,  "status":"success","type":"transfer"},
    {"hash":"0x002","value_eth":12.0, "status":"success","type":"swap"},
    {"hash":"0x003","value_eth":0.001,"status":"failed", "type":"transfer"},
    {"hash":"0x004","value_eth":75.0, "status":"success","type":"transfer"},
    {"hash":"0x005","value_eth":0.05, "status":"success","type":"swap"},
    {"hash":"0x006","value_eth":2.1,  "status":"failed", "type":"swap"},
    {"hash":"0x007","value_eth":1.2,  "status":"success","type":"liquidity"},
    {"hash":"0x008","value_eth":0.08, "status":"success","type":"NFT"},
    {"hash":"0x009","value_eth":5.5,  "status":"success","type":"swap"},
    {"hash":"0x010","value_eth":0.0,  "status":"failed", "type":"NFT"},
    {"hash":"0x011","value_eth":0.15, "status":"success","type":"NFT"},
    {"hash":"0x012","value_eth":3.3,  "status":"success","type":"swap"},
]

total_txns    = len(transactions)
success_count = 0
failed_count  = 0
total_volume  = 0
values        = []
type_counts   = {}
largest_tx    = 0

for tx in transactions:
    if tx["status"] == "failed":
        failed_count += 1
        continue

    success_count += 1
    total_volume  += tx["value_eth"]
    values.append(tx["value_eth"])

    if tx["value_eth"] > largest_tx:
        largest_tx = tx["value_eth"]

    t = tx["type"]
    type_counts[t] = type_counts.get(t, 0) + 1

success_rate = (success_count / total_txns) * 100
failed_rate  = (failed_count  / total_txns) * 100
avg_value    = total_volume / success_count if success_count else 0
min_value    = min(values) if values else 0
max_value    = max(values) if values else 0

# Most common type
most_common_type = max(type_counts, key=type_counts.get) if type_counts else "N/A"

# Classification
if largest_tx >= 50:
    wallet_class = "🐋 Whale"
elif type_counts.get("swap", 0) >= 3:
    wallet_class = "⚡ DeFi Trader"
elif "liquidity" in type_counts:
    wallet_class = "💧 Liquidity Provider"
elif type_counts.get("NFT", 0) >= 2:
    wallet_class = "🎨 NFT Collector"
else:
    wallet_class = "👤 Regular User"

flag = "⚠️  Suspicious failure rate!" if failed_rate > 30 else ""

print("\n  " + "=" * 48)
print("    WALLET ACTIVITY REPORT")
print("  " + "=" * 48)
print(f"  Classification : {wallet_class}")
if flag:
    print(f"  Flag           : {flag}")
print(f"  Total Txns     : {total_txns} ({success_count} success / {failed_count} failed)")
print(f"  Success Rate   : {success_rate:.1f}%")
print(f"  Total Volume   : {total_volume:.4f} ETH")
print(f"  Avg Tx Size    : {avg_value:.4f} ETH")
print(f"  Min / Max Tx   : {min_value:.4f} / {max_value:.4f} ETH")
print(f"  Top Activity   : {most_common_type} ({type_counts.get(most_common_type, 0)} txns)")
print(f"  Activity Mix   :", end="")
for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
    print(f"  {c}x {t}", end="")
print()
print("  " + "=" * 48)

print("\n" + "=" * 60)
print("All exercises complete! Commit your work:")
print("  git add phase-1-python-fundamentals/week-03-control-structures/")
print('  git commit -m "phase-1/week-03: completed control structures"')
print("  git push")
print("=" * 60)
