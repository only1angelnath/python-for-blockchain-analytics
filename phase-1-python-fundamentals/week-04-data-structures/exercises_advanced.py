"""
Week 4 Advanced Exercises — Data Structures Deep Dive
Python for Blockchain Analytics | Phase 1

These exercises are harder than the intro set.
Each one combines multiple structures and mirrors a real analytics task.

Run with: python3 exercises_advanced.py
"""

from collections import defaultdict, Counter
import copy

print("=" * 65)
print("WEEK 4 ADVANCED EXERCISES — Data Structures Deep Dive")
print("=" * 65)


# ─────────────────────────────────────────────────────────────
# EXERCISE 1 — Lists: Sliding window price analysis
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 1: Sliding window — moving average ──")
"""
A moving average smooths out price noise.
7-day MA = average of the last 7 days at each point.

Given 30 days of ETH prices, compute:
  1. The 7-day moving average for each day (where enough data exists)
  2. Days where price crossed ABOVE the MA (signal: bullish)
  3. Days where price crossed BELOW the MA (signal: bearish)
  4. Print a mini chart:
     day | price    | 7d MA    | signal
      8  | $3,247   | $3,180   | 📈 Cross up

Note: the MA is only available from day 7 onwards (need 7 days of data).

SQL parallel:
  AVG(price) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
  This is a window function — the sliding window.
"""

# YOUR CODE HERE
eth_prices_30d = [
    3050, 3120, 3080, 3200, 3150, 3180, 3247,  # days 1-7
    3310, 3290, 3350, 3400, 3375, 3420, 3380,  # days 8-14
    3450, 3480, 3510, 3490, 3550, 3520, 3480,  # days 15-21
    3420, 3380, 3350, 3400, 3430, 3460, 3490,  # days 22-28
    3520, 3550,                                 # days 29-30
]

WINDOW = 7
results = []

for i in range(len(eth_prices_30d)):
    price = eth_prices_30d[i]
    if i >= WINDOW - 1:
        window_prices = eth_prices_30d[i - WINDOW + 1: i + 1]
        ma = sum(window_prices) / WINDOW
    else:
        ma = None
    results.append({"day": i + 1, "price": price, "ma": ma})

# Find crossovers
print(f"\n  {'Day':>4}  {'Price':>8}  {'7d MA':>8}  Signal")
print("  " + "-" * 38)
for i, r in enumerate(results):
    ma_str = f"${r['ma']:>7,.0f}" if r["ma"] else "       —"
    signal = ""
    if i >= WINDOW and results[i - 1]["ma"] is not None:
        prev_above = results[i - 1]["price"] > results[i - 1]["ma"]
        curr_above = r["price"] > r["ma"]
        if not prev_above and curr_above:
            signal = "📈 Cross UP — bullish"
        elif prev_above and not curr_above:
            signal = "📉 Cross DOWN — bearish"
    print(f"  {r['day']:>4}  ${r['price']:>7,}  {ma_str}  {signal}")

# Solution: see above — uses a sliding slice [i-WINDOW+1 : i+1]


# ─────────────────────────────────────────────────────────────
# EXERCISE 2 — Tuples + namedtuple: OHLCV candle builder
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 2: OHLCV candle builder ──")
"""
OHLCV = Open, High, Low, Close, Volume
Candlestick data is the backbone of price charts.

Given tick-level trade data (timestamp, price, volume),
build 1-hour OHLCV candles.

Rules:
  - Group ticks into 1-hour buckets (hour = timestamp // 3600)
  - Open  = first price in the hour
  - High  = highest price
  - Low   = lowest price
  - Close = last price
  - Volume = sum of all volumes

Use a namedtuple for the candle structure.
Print each candle cleanly.

SQL parallel:
  SELECT
    DATE_TRUNC('hour', ts)   AS hour,
    FIRST_VALUE(price) OVER w AS open,
    MAX(price)               AS high,
    MIN(price)               AS low,
    LAST_VALUE(price) OVER w AS close,
    SUM(volume)              AS volume
  FROM ticks
  GROUP BY 1
"""

# YOUR CODE HERE
from collections import namedtuple

Candle = namedtuple("Candle", ["hour", "open", "high", "low", "close", "volume"])

# Raw tick data: (unix_timestamp, price, volume_eth)
ticks = [
    (1_714_000_100, 3247.85, 2.1),
    (1_714_000_800, 3251.20, 1.5),
    (1_714_001_500, 3245.60, 3.8),
    (1_714_002_200, 3260.00, 0.9),
    (1_714_003_100, 3255.40, 2.2),
    (1_714_003_600, 3258.75, 1.1),  # same hour as above
    (1_714_003_900, 3263.50, 4.5),  # still same hour
    (1_714_004_200, 3270.00, 2.8),
    (1_714_007_000, 3265.30, 1.4),  # new hour (ts // 3600 differs)
    (1_714_007_500, 3258.90, 3.1),
    (1_714_008_100, 3275.00, 2.6),
    (1_714_008_800, 3280.50, 1.8),
    (1_714_009_200, 3272.10, 0.7),
    (1_714_010_500, 3268.40, 2.3),
]

# Group by hour bucket
hourly_ticks = defaultdict(list)
for ts, price, vol in ticks:
    hour_bucket = ts // 3600
    hourly_ticks[hour_bucket].append((ts, price, vol))

# Build candles
candles = []
for hour_bucket in sorted(hourly_ticks.keys()):
    hour_ticks = sorted(hourly_ticks[hour_bucket])  # sort by timestamp
    prices  = [t[1] for t in hour_ticks]
    volumes = [t[2] for t in hour_ticks]
    candle  = Candle(
        hour   = hour_bucket,
        open   = prices[0],
        high   = max(prices),
        low    = min(prices),
        close  = prices[-1],
        volume = round(sum(volumes), 2),
    )
    candles.append(candle)

print(f"\n  {'Hour':>12}  {'Open':>9}  {'High':>9}  {'Low':>9}  {'Close':>9}  {'Volume':>8}")
print("  " + "-" * 65)
for c in candles:
    direction = "🟢" if c.close >= c.open else "🔴"
    print(f"  {c.hour:>12}  ${c.open:>8,.2f}  ${c.high:>8,.2f}  "
          f"${c.low:>8,.2f}  ${c.close:>8,.2f} {direction}  {c.volume:>7.2f}")

# Solution: see above — namedtuple + defaultdict(list) + sorted()


# ─────────────────────────────────────────────────────────────
# EXERCISE 3 — Dicts: Mempool fee estimator
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 3: Mempool fee estimator ──")
"""
The mempool holds pending transactions waiting to be included in a block.
Miners/validators pick the highest-fee transactions first.

Given pending transactions, build a fee estimator that tells a user
what gas price to use for different confirmation speed targets.

Approach:
  - Sort pending txns by gas_gwei descending
  - The top N% get included in the next block (assume block can fit 200 txns)
  - "Fast"   = price needed to be in top 10% (next block almost certainly)
  - "Normal" = price needed to be in top 50% (within ~3 blocks)
  - "Slow"   = price needed to be in top 90% (within ~10 blocks)
  - "Cheap"  = minimum price in mempool

Build a result dict with these four tiers, then print a recommendation.
Also find: what % of pending txns would be outpriced by each tier.
"""

# YOUR CODE HERE
import random
random.seed(7)

# Simulate 500 pending transactions
pending_txns = [
    {
        "hash":      f"0x{i:04x}abc",
        "gas_gwei":  round(random.lognormvariate(3.5, 0.5), 1),  # log-normal dist
        "value_eth": round(random.uniform(0, 10), 3),
    }
    for i in range(500)
]

# Sort by gas descending
sorted_pending = sorted(pending_txns, key=lambda t: -t["gas_gwei"])
n = len(sorted_pending)

# Percentile gas prices
def gas_at_percentile(txns, pct):
    """Return gas price at the given percentile (0-100)."""
    idx = max(0, min(int(len(txns) * pct / 100) - 1, len(txns) - 1))
    return txns[idx]["gas_gwei"]

fee_estimates = {
    "fast":   gas_at_percentile(sorted_pending, 10),   # top 10%
    "normal": gas_at_percentile(sorted_pending, 50),   # top 50%
    "slow":   gas_at_percentile(sorted_pending, 90),   # top 90%
    "cheap":  sorted_pending[-1]["gas_gwei"],           # bottom
}

print(f"\n  Mempool: {n} pending transactions\n")
print(f"  {'Speed':<10} {'Gas Price':>12}  {'Txns outpriced':>16}  ETA")
print("  " + "-" * 52)

speed_meta = {
    "fast":   ("~15 sec",  "next block"),
    "normal": ("~45 sec",  "2-3 blocks"),
    "slow":   ("~2 min",   "5-10 blocks"),
    "cheap":  (">10 min",  "when uncongested"),
}

for tier in ["fast", "normal", "slow", "cheap"]:
    gas       = fee_estimates[tier]
    outpriced = sum(1 for t in sorted_pending if t["gas_gwei"] < gas)
    pct_out   = outpriced / n * 100
    eta, desc = speed_meta[tier]
    print(f"  {tier.capitalize():<10} {gas:>10.1f}G  "
          f"{outpriced:>7,} ({pct_out:>4.0f}%)  {eta} — {desc}")

print(f"\n  Recommendation: use {fee_estimates['normal']:.1f} Gwei for normal transactions.")

# Solution: see above — lognormal mempool, percentile-based tiers


# ─────────────────────────────────────────────────────────────
# EXERCISE 4 — Sets: Airdrop eligibility engine
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 4: Airdrop eligibility engine ──")
"""
Many DeFi protocols airdrop tokens to past users.
Eligibility rules are combinations of set operations.

Given snapshot data for 4 criteria, compute:

  Tier 1 (highest allocation):
    - Used the protocol before block 18,000,000 (early user)
    - AND made at least 10 transactions
    - AND held tokens at snapshot

  Tier 2:
    - Used the protocol (any time)
    - AND (held tokens OR made 5+ transactions)
    - NOT already in Tier 1

  Tier 3:
    - Used the protocol
    - NOT in Tier 1 or Tier 2

  Ineligible:
    - Never used the protocol
    - OR on the sybil_blacklist

Print each tier's wallet count and list, plus total eligible wallets.

SQL parallel:
  This is a multi-condition segmentation query — like a CASE WHEN
  with set-based conditions, equivalent to multiple CTEs joined together.
"""

# YOUR CODE HERE
all_wallets        = {f"0xWallet{i:03d}" for i in range(1, 26)}
early_users        = {f"0xWallet{i:03d}" for i in [1, 2, 3, 5, 7, 9, 11, 14]}
high_tx_users      = {f"0xWallet{i:03d}" for i in [1, 2, 3, 4, 5, 7, 9, 12, 14, 16, 18]}
token_holders      = {f"0xWallet{i:03d}" for i in [1, 2, 3, 5, 6, 7, 10, 13, 14, 17, 20]}
protocol_users     = {f"0xWallet{i:03d}" for i in range(1, 21)}  # wallets 1-20 used the protocol
mid_tx_users       = {f"0xWallet{i:03d}" for i in [1,2,3,4,5,6,7,8,9,10,11,12,13,14]}
sybil_blacklist    = {f"0xWallet{i:03d}" for i in [8, 15, 19]}

# Compute tiers
tier1 = early_users & high_tx_users & token_holders
tier1 -= sybil_blacklist

tier2 = protocol_users & (token_holders | mid_tx_users)
tier2 -= tier1
tier2 -= sybil_blacklist

tier3 = protocol_users - tier1 - tier2 - sybil_blacklist

ineligible = (all_wallets - protocol_users) | sybil_blacklist

total_eligible = tier1 | tier2 | tier3

print(f"\n  {'Tier':<12} {'Count':>6}  Wallets")
print("  " + "-" * 55)
for label, wallets in [("Tier 1 (high)", tier1), ("Tier 2 (mid)", tier2),
                        ("Tier 3 (base)", tier3), ("Ineligible", ineligible)]:
    print(f"  {label:<14} {len(wallets):>4}   {sorted(wallets)}")

print(f"\n  Total eligible wallets: {len(total_eligible)}")
print(f"  Sybil blacklisted:      {len(sybil_blacklist)}")

# Solution: see above — cascading set operations


# ─────────────────────────────────────────────────────────────
# EXERCISE 5 — Deep nesting: GraphQL-style response parser
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 5: GraphQL response parser ──")
"""
TheGraph (a blockchain indexing protocol) returns deeply nested JSON.
Parse this response and produce a flat, clean analytics table.

Extract per-pool per-day:
  - pool address (shortened)
  - token pair (token0/token1)
  - fee tier
  - date
  - volume_usd
  - fees_usd  (volume * fee_tier / 1,000,000)
  - tvl_usd

Then:
  1. Print all rows as a flat table
  2. Find the highest-volume single day across all pools
  3. Calculate total 7-day volume per pool
  4. Find which pool had the most consistent volume
     (lowest coefficient of variation: std/mean)
"""

# YOUR CODE HERE
import math

graph_response = {
    "data": {
        "pools": [
            {
                "id": "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640",
                "token0": {"symbol": "USDC"},
                "token1": {"symbol": "WETH"},
                "feeTier": "500",
                "poolDayData": [
                    {"date": "2024-04-01", "volumeUSD": "420000000", "tvlUSD": "800000000"},
                    {"date": "2024-04-02", "volumeUSD": "380000000", "tvlUSD": "805000000"},
                    {"date": "2024-04-03", "volumeUSD": "510000000", "tvlUSD": "820000000"},
                    {"date": "2024-04-04", "volumeUSD": "350000000", "tvlUSD": "798000000"},
                    {"date": "2024-04-05", "volumeUSD": "290000000", "tvlUSD": "790000000"},
                    {"date": "2024-04-06", "volumeUSD": "460000000", "tvlUSD": "815000000"},
                    {"date": "2024-04-07", "volumeUSD": "390000000", "tvlUSD": "810000000"},
                ],
            },
            {
                "id": "0x6c6Bc977E13Df9b0de53b251522280BB72383700",
                "token0": {"symbol": "USDC"},
                "token1": {"symbol": "USDT"},
                "feeTier": "100",
                "poolDayData": [
                    {"date": "2024-04-01", "volumeUSD": "380000000", "tvlUSD": "210000000"},
                    {"date": "2024-04-02", "volumeUSD": "420000000", "tvlUSD": "215000000"},
                    {"date": "2024-04-03", "volumeUSD": "395000000", "tvlUSD": "208000000"},
                    {"date": "2024-04-04", "volumeUSD": "410000000", "tvlUSD": "212000000"},
                    {"date": "2024-04-05", "volumeUSD": "375000000", "tvlUSD": "209000000"},
                    {"date": "2024-04-06", "volumeUSD": "430000000", "tvlUSD": "218000000"},
                    {"date": "2024-04-07", "volumeUSD": "405000000", "tvlUSD": "214000000"},
                ],
            },
            {
                "id": "0x1d42041D6bABd76e1C70b46e7e72e1B2a8F1Da0",
                "token0": {"symbol": "UNI"},
                "token1": {"symbol": "WETH"},
                "feeTier": "3000",
                "poolDayData": [
                    {"date": "2024-04-01", "volumeUSD": "12000000",  "tvlUSD": "42000000"},
                    {"date": "2024-04-02", "volumeUSD": "8500000",   "tvlUSD": "40000000"},
                    {"date": "2024-04-03", "volumeUSD": "25000000",  "tvlUSD": "45000000"},
                    {"date": "2024-04-04", "volumeUSD": "9800000",   "tvlUSD": "41000000"},
                    {"date": "2024-04-05", "volumeUSD": "7200000",   "tvlUSD": "39000000"},
                    {"date": "2024-04-06", "volumeUSD": "15000000",  "tvlUSD": "43000000"},
                    {"date": "2024-04-07", "volumeUSD": "11000000",  "tvlUSD": "42000000"},
                ],
            },
        ]
    }
}

# Flatten
flat_rows = []
for pool in graph_response["data"]["pools"]:
    pool_id   = pool["id"]
    short_id  = f"{pool_id[:6]}...{pool_id[-4:]}"
    pair      = f"{pool['token0']['symbol']}/{pool['token1']['symbol']}"
    fee_tier  = int(pool["feeTier"])

    for day in pool["poolDayData"]:
        vol   = float(day["volumeUSD"])
        tvl   = float(day["tvlUSD"])
        fees  = vol * fee_tier / 1_000_000
        flat_rows.append({
            "pool":    short_id,
            "pair":    pair,
            "fee":     fee_tier,
            "date":    day["date"],
            "vol":     vol,
            "fees":    fees,
            "tvl":     tvl,
        })

# Print flat table
print(f"\n  {'Pool':<14} {'Pair':<12} {'Fee':>5}  {'Date':<12} {'Volume':>12}  {'Fees':>10}  {'TVL':>12}")
print("  " + "-" * 80)
for r in flat_rows:
    print(f"  {r['pool']:<14} {r['pair']:<12} {r['fee']/10000:.2f}%  {r['date']:<12} "
          f"${r['vol']/1e6:>10,.1f}M  ${r['fees']/1e3:>8,.1f}K  ${r['tvl']/1e6:>10,.1f}M")

# Highest single day volume
best_day = max(flat_rows, key=lambda r: r["vol"])
print(f"\n  Peak day: {best_day['pool']} on {best_day['date']} — ${best_day['vol']/1e6:,.1f}M")

# 7-day total per pool
pool_7d = defaultdict(float)
for r in flat_rows:
    pool_7d[r["pool"]] += r["vol"]
print("\n  7-day volume by pool:")
for pool, vol in sorted(pool_7d.items(), key=lambda x: -x[1]):
    print(f"    {pool}: ${vol/1e9:.2f}B")

# Coefficient of variation (consistency)
pool_vols = defaultdict(list)
for r in flat_rows:
    pool_vols[r["pool"]].append(r["vol"])

print("\n  Volume consistency (lower CV = more stable):")
for pool, vols in pool_vols.items():
    avg = sum(vols) / len(vols)
    std = math.sqrt(sum((v - avg)**2 for v in vols) / len(vols))
    cv  = std / avg * 100
    bar = "█" * int((100 - cv) / 10)
    print(f"    {pool}: CV={cv:.1f}%  {bar}")

# Solution: see above — flatten → aggregate → sort


# ─────────────────────────────────────────────────────────────
# EXERCISE 6 — Copy pitfalls: Snapshot divergence detector
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 6: Snapshot copy safety ──")
"""
You're building a system that takes a portfolio snapshot every hour.
A bug caused shallow copies to be used instead of deep copies —
causing historical snapshots to be silently mutated.

Part A: Demonstrate the bug
  - Create an initial portfolio (list of dicts)
  - Take a "snapshot" using .copy() (shallow)
  - Update prices in the original
  - Show that the snapshot was also mutated

Part B: Fix the bug
  - Use copy.deepcopy() instead
  - Show that the snapshot is now preserved

Part C: Detect which snapshots are corrupted
  - Given a list of snapshots that may have been taken with shallow copy,
    find any two consecutive snapshots with identical wallet balances
    (a sign they share the same underlying dict objects)
"""

# YOUR CODE HERE

# Part A — demonstrate the bug
print("\n  Part A — The shallow copy bug:")
portfolio = [
    {"wallet": "0xAlice", "eth_balance": 5.0,  "usd_value": 16_239.25},
    {"wallet": "0xBob",   "eth_balance": 2.3,  "usd_value":  7_470.06},
]

snapshot_buggy = portfolio.copy()           # shallow copy — BUG!

# "Update" prices after snapshot
portfolio[0]["eth_balance"] = 10.0          # Alice bought more ETH
portfolio[0]["usd_value"]   = 32_478.50

print(f"  Original Alice balance: {portfolio[0]['eth_balance']} ETH")
print(f"  Snapshot Alice balance: {snapshot_buggy[0]['eth_balance']} ETH  ← should be 5.0 but got mutated!")

# Part B — fixed with deepcopy
print("\n  Part B — The fix with deepcopy:")
portfolio = [
    {"wallet": "0xAlice", "eth_balance": 5.0,  "usd_value": 16_239.25},
    {"wallet": "0xBob",   "eth_balance": 2.3,  "usd_value":  7_470.06},
]

snapshot_safe = copy.deepcopy(portfolio)    # deep copy — SAFE ✓

portfolio[0]["eth_balance"] = 10.0
portfolio[0]["usd_value"]   = 32_478.50

print(f"  Original Alice balance: {portfolio[0]['eth_balance']} ETH")
print(f"  Snapshot Alice balance: {snapshot_safe[0]['eth_balance']} ETH  ← preserved correctly ✓")

# Part C — detect corrupted snapshots
print("\n  Part C — Detecting corrupted snapshots:")

base = [{"wallet": "0xAlice", "balance": 5.0}, {"wallet": "0xBob", "balance": 2.3}]

# Simulate 5 snapshots — some shallow (buggy), some deep (correct)
snapshots = []
for hour in range(5):
    if hour in [0, 2, 4]:   # these were deep-copied correctly
        snapshots.append(copy.deepcopy(base))
    else:                    # these were shallow-copied (buggy)
        snapshots.append(base.copy())
    base[0]["balance"] += 0.5   # price update after snapshot

# Detect corruption: if snapshot i and i+1 have same object ids for inner dicts
print(f"  {'Hour':>5}  {'Alice bal':>12}  Status")
print("  " + "-" * 35)
for i, snap in enumerate(snapshots):
    alice_bal = snap[0]["balance"]
    # A simple corruption signal: balance shouldn't match the "current" base if properly snapshotted
    # More rigorously: check if inner dict is the same object
    is_shared = any(snap[j] is base[j] for j in range(len(snap)))
    status = "⚠️  CORRUPTED (shared reference)" if is_shared else "✅ Safe (deep copy)"
    print(f"  {i:>5}  {alice_bal:>11.1f}E  {status}")

# Solution: see above — demonstrates shallow vs deep copy consequences


# ─────────────────────────────────────────────────────────────
# EXERCISE 7 — Counter + defaultdict: MEV activity analyser
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 7: MEV activity analyser ──")
"""
MEV (Maximal Extractable Value) bots perform sandwich attacks, arbitrage,
and liquidations. Identify them from transaction patterns.

Given a list of transactions from one block:
  1. Use Counter to count txns per sender
  2. Use defaultdict to group txns by sender
  3. For each sender with > 2 txns in the block:
     a. Calculate their total gas spent (gas_used * gas_price)
     b. Calculate net ETH flow (value_out - value_in)
     c. Detect sandwich pattern: same token in consecutive txns
        with a victim txn between them (type: "victim")
     d. Label: "🥪 Sandwich Bot", "⚡ Arbitrage Bot", "💰 Liquidator", or "👤 Normal"

Print a ranked MEV report sorted by total gas spent.
"""

# YOUR CODE HERE
block_txns = [
    {"sender": "0xBot1",    "type": "swap",       "token": "ETH",   "value_eth": 5.0,  "gas_used": 180_000, "gas_gwei": 200, "position": 1},
    {"sender": "0xUser1",   "type": "victim",     "token": "ETH",   "value_eth": 1.0,  "gas_used": 150_000, "gas_gwei": 50,  "position": 2},
    {"sender": "0xBot1",    "type": "swap",       "token": "ETH",   "value_eth": 5.1,  "gas_used": 180_000, "gas_gwei": 200, "position": 3},
    {"sender": "0xArb1",    "type": "swap",       "token": "USDC",  "value_eth": 10.0, "gas_used": 220_000, "gas_gwei": 150, "position": 4},
    {"sender": "0xArb1",    "type": "swap",       "token": "UNI",   "value_eth": 10.3, "gas_used": 220_000, "gas_gwei": 150, "position": 5},
    {"sender": "0xLiq1",    "type": "liquidation","token": "ETH",   "value_eth": 50.0, "gas_used": 350_000, "gas_gwei": 180, "position": 6},
    {"sender": "0xUser2",   "type": "transfer",   "token": "ETH",   "value_eth": 0.5,  "gas_used": 21_000,  "gas_gwei": 30,  "position": 7},
    {"sender": "0xBot1",    "type": "swap",       "token": "USDC",  "value_eth": 2.0,  "gas_used": 180_000, "gas_gwei": 200, "position": 8},
    {"sender": "0xArb1",    "type": "swap",       "token": "USDC",  "value_eth": 10.3, "gas_used": 220_000, "gas_gwei": 150, "position": 9},
    {"sender": "0xUser3",   "type": "swap",       "token": "UNI",   "value_eth": 0.8,  "gas_used": 160_000, "gas_gwei": 25,  "position": 10},
]

# Group by sender
sender_txns = defaultdict(list)
for tx in block_txns:
    sender_txns[tx["sender"]].append(tx)

tx_counter = Counter(tx["sender"] for tx in block_txns)

# Analyse active senders
print(f"\n  {'Sender':<12} {'Txns':>5}  {'Gas Spent':>12}  {'Net Flow':>10}  Label")
print("  " + "-" * 60)

for sender, count in tx_counter.most_common():
    txns = sender_txns[sender]
    gas_spent_eth = sum(t["gas_used"] * t["gas_gwei"] for t in txns) / 1e9
    value_out = sum(t["value_eth"] for t in txns if t["type"] in ["swap","liquidation"])
    net_flow  = value_out  # simplified

    # Detect patterns
    types    = [t["type"] for t in sorted(txns, key=lambda x: x["position"])]
    tokens   = [t["token"] for t in sorted(txns, key=lambda x: x["position"])]
    avg_gas  = sum(t["gas_gwei"] for t in txns) / len(txns)

    has_sandwich   = "victim" in types or (len(set(tokens)) < len(tokens) and avg_gas > 100)
    has_liquidation= "liquidation" in types
    is_arb         = len(txns) >= 2 and len(set(tokens)) > 1 and avg_gas > 100

    if has_sandwich:
        label = "🥪 Sandwich Bot"
    elif has_liquidation:
        label = "💰 Liquidator"
    elif is_arb:
        label = "⚡ Arbitrage Bot"
    else:
        label = "👤 Normal User"

    print(f"  {sender:<12} {count:>5}  {gas_spent_eth:>11.4f}E  {net_flow:>9.2f}E  {label}")

# Solution: see above — Counter + defaultdict + pattern detection


# ─────────────────────────────────────────────────────────────
# EXERCISE 8 — All structures: Full on-chain analytics report
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 8 (Challenge): Full protocol analytics report ──")
"""
This is the hardest exercise. You're building a complete analytics
report for a DeFi protocol from raw event data.

Given raw_events (mixed event types), produce:

  1. EVENT SUMMARY
     - Count of each event type (Counter)
     - Unique wallets involved (set)
     - Total value locked change (sum of deposits - withdrawals)

  2. TOP WALLETS
     - For each wallet: total deposited, total withdrawn, net position, event count
     - Sorted by net position descending
     - Label: "🐋 Whale" (>100 ETH net), "💧 LP" (deposits+withdrawals > 20),
              "⚡ Active" (>3 events), "👤 User"

  3. HOURLY ACTIVITY
     - Group events by hour (timestamp // 3600)
     - Count events and volume per hour
     - Find peak hour

  4. TOKEN BREAKDOWN
     - Volume by token (sum value_eth per token)
     - Unique depositors per token (set per token)

Build this using: defaultdict, Counter, set, list of dicts, sorted()
"""

# YOUR CODE HERE
raw_events = [
    {"ts": 1_714_000_100, "type": "deposit",    "wallet": "0xWhale1", "token": "ETH",  "value_eth": 150.0},
    {"ts": 1_714_000_500, "type": "swap",        "wallet": "0xTrader1","token": "USDC", "value_eth": 5.0},
    {"ts": 1_714_001_200, "type": "deposit",    "wallet": "0xLP1",    "token": "USDC", "value_eth": 25.0},
    {"ts": 1_714_001_800, "type": "withdraw",   "wallet": "0xWhale1", "token": "ETH",  "value_eth": 30.0},
    {"ts": 1_714_002_100, "type": "deposit",    "wallet": "0xLP1",    "token": "ETH",  "value_eth": 15.0},
    {"ts": 1_714_002_900, "type": "swap",        "wallet": "0xTrader1","token": "ETH",  "value_eth": 3.0},
    {"ts": 1_714_003_400, "type": "deposit",    "wallet": "0xRetail1","token": "USDC", "value_eth": 2.0},
    {"ts": 1_714_003_900, "type": "liquidation","wallet": "0xLiq1",   "token": "ETH",  "value_eth": 45.0},
    {"ts": 1_714_004_200, "type": "deposit",    "wallet": "0xWhale2", "token": "ETH",  "value_eth": 200.0},
    {"ts": 1_714_004_800, "type": "withdraw",   "wallet": "0xLP1",    "token": "USDC", "value_eth": 10.0},
    {"ts": 1_714_007_100, "type": "deposit",    "wallet": "0xRetail2","token": "ETH",  "value_eth": 0.5},
    {"ts": 1_714_007_500, "type": "swap",        "wallet": "0xTrader1","token": "USDC", "value_eth": 8.0},
    {"ts": 1_714_008_000, "type": "withdraw",   "wallet": "0xWhale2", "token": "ETH",  "value_eth": 50.0},
    {"ts": 1_714_008_600, "type": "deposit",    "wallet": "0xLP1",    "token": "ETH",  "value_eth": 20.0},
    {"ts": 1_714_009_000, "type": "liquidation","wallet": "0xLiq1",   "token": "USDC", "value_eth": 12.0},
    {"ts": 1_714_009_500, "type": "swap",        "wallet": "0xBot1",   "token": "ETH",  "value_eth": 1.0},
    {"ts": 1_714_010_000, "type": "swap",        "wallet": "0xBot1",   "token": "ETH",  "value_eth": 1.0},
    {"ts": 1_714_010_200, "type": "deposit",    "wallet": "0xRetail3","token": "USDC", "value_eth": 1.5},
]

# 1. EVENT SUMMARY
event_counter  = Counter(e["type"] for e in raw_events)
unique_wallets = set(e["wallet"] for e in raw_events)
tvl_change     = sum(
    e["value_eth"] if e["type"] == "deposit" else
    -e["value_eth"] if e["type"] == "withdraw" else 0
    for e in raw_events
)

print(f"\n  ── 1. EVENT SUMMARY ──")
print(f"  Total events    : {len(raw_events)}")
print(f"  Unique wallets  : {len(unique_wallets)}")
print(f"  TVL change      : {tvl_change:+.2f} ETH")
print(f"  Event breakdown :")
for etype, count in event_counter.most_common():
    print(f"    {etype:<14} {count:>4}")

# 2. TOP WALLETS
wallet_stats = defaultdict(lambda: {"deposited": 0.0, "withdrawn": 0.0, "events": 0})
for e in raw_events:
    w = e["wallet"]
    wallet_stats[w]["events"] += 1
    if e["type"] == "deposit":
        wallet_stats[w]["deposited"]  += e["value_eth"]
    elif e["type"] == "withdraw":
        wallet_stats[w]["withdrawn"] += e["value_eth"]

wallet_rows = []
for wallet, stats in wallet_stats.items():
    net      = stats["deposited"] - stats["withdrawn"]
    activity = stats["deposited"] + stats["withdrawn"]
    if net > 100:              label = "🐋 Whale"
    elif activity > 20:        label = "💧 LP"
    elif stats["events"] > 3:  label = "⚡ Active"
    else:                      label = "👤 User"
    wallet_rows.append({"wallet": wallet, "net": net, "label": label, **stats})

print(f"\n  ── 2. TOP WALLETS (by net position) ──")
print(f"  {'Wallet':<12} {'Deposited':>10}  {'Withdrawn':>10}  {'Net':>8}  {'Evts':>5}  Label")
print("  " + "-" * 65)
for r in sorted(wallet_rows, key=lambda x: -x["net"]):
    print(f"  {r['wallet']:<12} {r['deposited']:>9.2f}E  {r['withdrawn']:>9.2f}E  "
          f"{r['net']:>+7.2f}E  {r['events']:>5}  {r['label']}")

# 3. HOURLY ACTIVITY
hourly = defaultdict(lambda: {"count": 0, "volume": 0.0})
for e in raw_events:
    h = e["ts"] // 3600
    hourly[h]["count"]  += 1
    hourly[h]["volume"] += e["value_eth"]

print(f"\n  ── 3. HOURLY ACTIVITY ──")
print(f"  {'Hour bucket':>14}  {'Events':>7}  {'Volume':>10}")
print("  " + "-" * 38)
peak_hour = max(hourly.items(), key=lambda x: x[1]["volume"])
for h in sorted(hourly.keys()):
    flag = " ← peak" if h == peak_hour[0] else ""
    print(f"  {h:>14}  {hourly[h]['count']:>7}  {hourly[h]['volume']:>9.2f}E{flag}")

# 4. TOKEN BREAKDOWN
token_vol   = defaultdict(float)
token_users = defaultdict(set)
for e in raw_events:
    token_vol[e["token"]]    += e["value_eth"]
    token_users[e["token"]].add(e["wallet"])

print(f"\n  ── 4. TOKEN BREAKDOWN ──")
print(f"  {'Token':<8}  {'Volume':>10}  {'Unique Wallets':>16}")
print("  " + "-" * 40)
for token in sorted(token_vol, key=lambda t: -token_vol[t]):
    print(f"  {token:<8}  {token_vol[token]:>9.2f}E  {len(token_users[token]):>16}")

print("\n" + "=" * 65)
print("All advanced exercises complete! Commit your work:")
print("  git add phase-1-python-fundamentals/week-04-data-structures/")
print('  git commit -m "phase-1/week-04: advanced deep-dive exercises"')
print("  git push")
print("=" * 65)
