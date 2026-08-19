"""
Week 5 SOLUTIONS — Functions & Modules
Python for Blockchain Analytics | Phase 1

⚠️  Only open this after attempting exercises.py yourself.
Peeking early robs you of the learning.
"""

print("=" * 60)
print("WEEK 5 SOLUTIONS — Functions & Modules")
print("=" * 60)


# ─────────────────────────────────────────────────────────────
# SOLUTION 1 — Gas fee calculator
# ─────────────────────────────────────────────────────────────
print("\n── Solution 1: Gas fee calculator ──")

def gas_fee_usd(gas_used: int, gas_price_gwei: float, eth_price_usd: float) -> float:
    """
    Calculate transaction gas fee in USD.

    Args:
        gas_used:       Units of gas consumed
        gas_price_gwei: Gas price in Gwei
        eth_price_usd:  Current ETH price in USD

    Returns:
        float: Gas fee in USD
    """
    gas_fee_eth = gas_used * gas_price_gwei * 1e9 / 1e18
    return gas_fee_eth * eth_price_usd

ETH_PRICE = 3247.85

scenarios = [
    ("Transfer",    21_000,  20, ETH_PRICE),
    ("Uniswap swap",150_000, 25, ETH_PRICE),
    ("Deployment",  800_000, 18, ETH_PRICE),
]

for label, gas_used, gwei, price in scenarios:
    fee = gas_fee_usd(gas_used, gwei, price)
    print(f"  {label:<16} ${fee:.4f}")


# ─────────────────────────────────────────────────────────────
# SOLUTION 2 — Default arguments: Token formatter
# ─────────────────────────────────────────────────────────────
print("\n── Solution 2: Token amount formatter ──")

def format_amount(raw_amount: int, symbol: str, decimals: int = 18, precision: int = 4) -> str:
    """
    Convert a raw token integer to a human-readable string.

    Args:
        raw_amount: Raw integer amount (e.g. Wei for ETH)
        symbol:     Token symbol (e.g. "ETH", "USDC")
        decimals:   Token decimals (default: 18)
        precision:  Decimal places to display (default: 4)

    Returns:
        str: Formatted token amount string e.g. "1.5000 ETH"

    Example:
        >>> format_amount(1_500_000_000_000_000_000, "ETH")
        '1.5000 ETH'
    """
    human = raw_amount / 10**decimals
    return f"{human:,.{precision}f} {symbol}"

print(format_amount(1_500_000_000_000_000_000, "ETH"))
print(format_amount(1_500_000, "USDC", decimals=6))
print(format_amount(1_500_000, "USDC", decimals=6, precision=2))
print(format_amount(1_284_000_000_000_000_000, "UNI", precision=2))


# ─────────────────────────────────────────────────────────────
# SOLUTION 3 — Return multiple values: Position health checker
# ─────────────────────────────────────────────────────────────
print("\n── Solution 3: Position health checker ──")

def check_position(
    collateral_eth: float,
    debt_usd: float,
    eth_price: float,
    threshold: float = 0.825
) -> tuple:
    """
    Check the health of a collateralised DeFi position.

    Args:
        collateral_eth: ETH deposited as collateral
        debt_usd:       Outstanding debt in USD
        eth_price:      Current ETH price in USD
        threshold:      Liquidation threshold (default: 82.5%)

    Returns:
        tuple: (collateral_value_usd, health_factor, liquidation_price, status)
    """
    collateral_value_usd = collateral_eth * eth_price
    health_factor        = (collateral_value_usd * threshold) / debt_usd
    liquidation_price    = debt_usd / (collateral_eth * threshold)

    if health_factor >= 1.5:
        status = "✅ Safe"
    elif health_factor >= 1.0:
        status = "⚠️  Warning"
    else:
        status = "🚨 At Risk"

    return (
        round(collateral_value_usd, 2),
        round(health_factor, 4),
        round(liquidation_price, 2),
        status
    )

positions = [
    (10.0, 20_000, 3247.85),
    (5.0,  12_000, 3247.85),
    (3.0,  10_500, 3247.85),
]

for collateral, debt, price in positions:
    col_val, hf, liq, status = check_position(collateral, debt, price)
    print(f"  Collateral: ${col_val:>10,.2f} | HF: {hf:.4f} | Liq: ${liq:>8,.2f} | {status}")


# ─────────────────────────────────────────────────────────────
# SOLUTION 4 — *args: Multi-wallet volume aggregator
# ─────────────────────────────────────────────────────────────
print("\n── Solution 4: Multi-wallet volume aggregator ──")

def total_volume(*wallet_volumes: float) -> dict:
    """
    Aggregate volume statistics across multiple wallets.

    Args:
        *wallet_volumes: Any number of float volume values (ETH)

    Returns:
        dict: count, total, average, max, min
    """
    if not wallet_volumes:
        return {"count": 0, "total": 0, "average": 0, "max": 0, "min": 0}

    return {
        "count":   len(wallet_volumes),
        "total":   round(sum(wallet_volumes), 4),
        "average": round(sum(wallet_volumes) / len(wallet_volumes), 4),
        "max":     max(wallet_volumes),
        "min":     min(wallet_volumes),
    }

for label, vols in [
    ("3 wallets", (5.2, 18.7, 0.3)),
    ("5 wallets", (250.0, 12.5, 0.8, 45.3, 3.1)),
    ("1 wallet",  (100.0,)),
]:
    stats = total_volume(*vols)
    print(f"  {label}: total={stats['total']:.4f} ETH | avg={stats['average']:.4f} | "
          f"max={stats['max']} | min={stats['min']}")


# ─────────────────────────────────────────────────────────────
# SOLUTION 5 — **kwargs: API request builder
# ─────────────────────────────────────────────────────────────
print("\n── Solution 5: Etherscan API request builder ──")

def build_etherscan_url(action: str, api_key: str = "demo", **params) -> str:
    """
    Build a full Etherscan API URL with query parameters.

    Args:
        action:  API action (e.g. "txlist", "tokentx", "balance")
        api_key: Etherscan API key (default: "demo")
        **params: Additional query parameters

    Returns:
        str: Full API URL with query string
    """
    base = "https://api.etherscan.io/api"
    query_parts = [
        "module=account",
        f"action={action}",
        f"apikey={api_key}",
    ]
    for key, val in params.items():
        query_parts.append(f"{key}={val}")

    return f"{base}?{'&'.join(query_parts)}"

print(build_etherscan_url("txlist",
      address="0xd8dA...6045", startblock=0, endblock=99999999))

print(build_etherscan_url("tokentx",
      address="0xd8dA...6045", contractaddress="0xA0b8...eB48"))

print(build_etherscan_url("balance", api_key="MYKEY123",
      address="0xd8dA...6045", tag="latest"))


# ─────────────────────────────────────────────────────────────
# SOLUTION 6 — Lambda: Token list sorter
# ─────────────────────────────────────────────────────────────
print("\n── Solution 6: Token list sorter ──")

tokens = [
    {"symbol":"ETH",  "name":"Ethereum",   "price":3247.85, "market_cap":390e9, "volume_24h":15.8e9, "change_24h":2.4},
    {"symbol":"BTC",  "name":"Bitcoin",    "price":67412.0, "market_cap":1320e9,"volume_24h":32.0e9, "change_24h":-0.8},
    {"symbol":"UNI",  "name":"Uniswap",    "price":12.84,   "market_cap":9.7e9, "volume_24h":180e6,  "change_24h":-1.2},
    {"symbol":"AAVE", "name":"Aave",       "price":98.50,   "market_cap":1.47e9,"volume_24h":95e6,   "change_24h":3.1},
    {"symbol":"ARB",  "name":"Arbitrum",   "price":1.24,    "market_cap":1.57e9,"volume_24h":420e6,  "change_24h":-0.5},
    {"symbol":"CRV",  "name":"Curve DAO",  "price":0.48,    "market_cap":630e6, "volume_24h":130e6,  "change_24h":1.8},
]

sorts = [
    ("By price asc",          sorted(tokens, key=lambda t: t["price"]),                         lambda t: f"${t['price']:>10,.2f}"),
    ("By market_cap desc",    sorted(tokens, key=lambda t: -t["market_cap"]),                   lambda t: f"${t['market_cap']/1e9:>7.1f}B"),
    ("By 24h change desc",    sorted(tokens, key=lambda t: -t["change_24h"]),                   lambda t: f"{t['change_24h']:>+6.1f}%"),
    ("By name alpha",         sorted(tokens, key=lambda t: t["name"]),                          lambda t: t["name"]),
    ("By vol/mcap desc",      sorted(tokens, key=lambda t: -(t["volume_24h"]/t["market_cap"])), lambda t: f"{t['volume_24h']/t['market_cap']:.4f}x"),
]

for title, ranked, val_fn in sorts:
    print(f"\n  {title}:")
    for i, t in enumerate(ranked, 1):
        print(f"    {i}. {t['symbol']:5} (${t['price']:>10,.2f}) — {val_fn(t)}")


# ─────────────────────────────────────────────────────────────
# SOLUTION 7 — Scope: Safe global config
# ─────────────────────────────────────────────────────────────
print("\n── Solution 7: Safe global config ──")

ETH_PRICE = 3247.85

def get_eth_price() -> float:
    """Return the current global ETH price."""
    return ETH_PRICE

def set_eth_price(new_price: float) -> None:
    """
    Update the global ETH price.

    Args:
        new_price: New ETH price in USD

    Raises:
        ValueError: If new_price is zero or negative
    """
    global ETH_PRICE
    if new_price <= 0:
        raise ValueError(f"ETH price must be positive, got {new_price}")
    ETH_PRICE = new_price

def eth_value(amount_eth: float) -> float:
    """Return USD value of an ETH amount at current price."""
    return amount_eth * ETH_PRICE

def usd_value(amount_usd: float) -> float:
    """Return ETH equivalent of a USD amount at current price."""
    return amount_usd / ETH_PRICE

# a. Initial price
print(f"  eth_value(2.5) at ${get_eth_price():,.2f}: ${eth_value(2.5):,.2f}")

# b. Update price
set_eth_price(3500.00)
print(f"  eth_value(2.5) at ${get_eth_price():,.2f}: ${eth_value(2.5):,.2f}")

# c. ValueError test
try:
    set_eth_price(-100)
except ValueError as e:
    print(f"  ValueError caught: {e}")

# d. USD to ETH
print(f"  usd_value($10,000) = {usd_value(10_000):.4f} ETH")

# Reset for other exercises
set_eth_price(3247.85)


# ─────────────────────────────────────────────────────────────
# SOLUTION 8 — Module design: blockchain_utils extension
# ─────────────────────────────────────────────────────────────
print("\n── Solution 8: blockchain_utils extensions ──")

import math

def apy_to_apr(apy: float, compound_periods: int = 365) -> float:
    """
    Convert APY (Annual Percentage Yield) to APR (Annual Percentage Rate).

    APR = ((1 + APY/100)^(1/n) - 1) * n * 100
    where n = number of compounding periods per year

    Args:
        apy:               APY as a percentage (e.g. 12.5 for 12.5%)
        compound_periods:  Number of compounding periods per year (default: 365 daily)

    Returns:
        float: APR as a percentage

    Example:
        >>> apy_to_apr(12.68, 365)
        12.0
    """
    if apy < 0:
        raise ValueError("APY cannot be negative")
    n   = compound_periods
    apr = ((1 + apy / 100) ** (1 / n) - 1) * n * 100
    return round(apr, 4)

def trade_slippage(expected_price: float, actual_price: float) -> float:
    """
    Calculate the price slippage of a trade as a percentage.

    Positive slippage = worse price than expected (paid more / received less).
    Negative slippage = better price than expected.

    Args:
        expected_price: Price quoted before the trade
        actual_price:   Price actually executed

    Returns:
        float: Slippage percentage (positive = bad for trader)

    Example:
        >>> trade_slippage(3247.85, 3280.00)
        0.99  (paid ~1% more than expected)
    """
    if expected_price <= 0:
        raise ValueError("Expected price must be positive")
    return round((actual_price - expected_price) / expected_price * 100, 4)

def block_to_timestamp_estimate(
    target_block: int,
    known_block: int,
    known_timestamp: int,
    avg_block_time: float = 12.0
) -> int:
    """
    Estimate the Unix timestamp for any block number.

    Args:
        target_block:    Block number to estimate timestamp for
        known_block:     A block number with a known timestamp
        known_timestamp: Unix timestamp of the known block
        avg_block_time:  Average seconds per block (default: 12.0 for Ethereum)

    Returns:
        int: Estimated Unix timestamp for target block

    Example:
        >>> block_to_timestamp_estimate(19_847_300, 19_847_293, 1_714_000_000)
        1714000084
    """
    block_diff   = target_block - known_block
    time_diff    = int(block_diff * avg_block_time)
    return known_timestamp + time_diff

# Test all three
print(f"  APY→APR: 12.68% APY = {apy_to_apr(12.68):.2f}% APR (daily compounding)")
print(f"  APY→APR: 5.0%   APY = {apy_to_apr(5.0, 12):.2f}% APR (monthly compounding)")

print(f"  Slippage (3247.85→3280.00): {trade_slippage(3247.85, 3280.00):+.2f}%")
print(f"  Slippage (3247.85→3230.00): {trade_slippage(3247.85, 3230.00):+.2f}%")

ref_block = 19_847_293
ref_ts    = 1_714_000_000
for target in [19_847_300, 19_847_500, 19_848_000]:
    est = block_to_timestamp_estimate(target, ref_block, ref_ts)
    diff = target - ref_block
    print(f"  Block {target:,} (+{diff} blocks) → ts={est:,} (+{est-ref_ts}s)")


# ─────────────────────────────────────────────────────────────
# SOLUTION — Challenge: Full transaction analyser
# ─────────────────────────────────────────────────────────────
print("\n── Solution — Challenge: Full transaction analyser ──")

def analyse_transactions(
    transactions: list,
    eth_price: float,
    min_value_eth: float = 0.0
) -> dict:
    """
    Analyse a list of transactions and return aggregated statistics.

    Args:
        transactions:  List of transaction dicts (hash, value_eth, gas_used,
                       gas_price_gwei, status, type)
        eth_price:     Current ETH price in USD
        min_value_eth: Exclude transactions below this ETH value (default: 0)

    Returns:
        dict: Aggregated analytics results
    """
    filtered_out   = 0
    success_txns   = []
    failed_count   = 0
    total_gas_usd  = 0.0
    gas_prices     = []
    type_breakdown = {}

    for tx in transactions:
        # Apply minimum value filter
        if tx["value_eth"] < min_value_eth:
            filtered_out += 1
            continue

        # Gas cost (always count, even for failed txns)
        gas_eth = tx["gas_used"] * tx["gas_price_gwei"] * 1e9 / 1e18
        total_gas_usd += gas_eth * eth_price
        gas_prices.append(tx["gas_price_gwei"])

        if tx["status"] == "success":
            success_txns.append(tx)
            t = tx["type"]
            type_breakdown[t] = type_breakdown.get(t, 0) + 1
        else:
            failed_count += 1

    total_txns   = len(transactions) - filtered_out
    success_count= len(success_txns)
    success_rate = (success_count / total_txns * 100) if total_txns else 0

    volumes = [t["value_eth"] for t in success_txns]
    total_volume_eth = sum(volumes)

    return {
        "total_txns":       total_txns,
        "success_count":    success_count,
        "failed_count":     failed_count,
        "success_rate":     round(success_rate, 2),
        "total_volume_eth": round(total_volume_eth, 6),
        "total_volume_usd": round(total_volume_eth * eth_price, 2),
        "avg_tx_eth":       round(total_volume_eth / success_count, 6) if success_count else 0,
        "largest_tx_eth":   max(volumes) if volumes else 0,
        "total_gas_usd":    round(total_gas_usd, 4),
        "avg_gas_gwei":     round(sum(gas_prices) / len(gas_prices), 2) if gas_prices else 0,
        "type_breakdown":   type_breakdown,
        "filtered_out":     filtered_out,
    }


def print_tx_report(result: dict, title: str = "Transaction Report") -> None:
    """Print a formatted transaction analysis report."""
    print(f"\n  {'=' * 48}")
    print(f"  {title.center(48)}")
    print(f"  {'=' * 48}")
    print(f"  Total txns        : {result['total_txns']}")
    print(f"  Success / Failed  : {result['success_count']} / {result['failed_count']}")
    print(f"  Success rate      : {result['success_rate']:.1f}%")
    if result["filtered_out"]:
        print(f"  Filtered out      : {result['filtered_out']}")
    print(f"  Total volume      : {result['total_volume_eth']:.4f} ETH  (${result['total_volume_usd']:,.2f})")
    print(f"  Avg tx size       : {result['avg_tx_eth']:.4f} ETH")
    print(f"  Largest tx        : {result['largest_tx_eth']:.4f} ETH")
    print(f"  Total gas cost    : ${result['total_gas_usd']:.4f}")
    print(f"  Avg gas price     : {result['avg_gas_gwei']:.1f} Gwei")
    print(f"  Type breakdown    :")
    sorted_result = list(result["type_breakdown"].items())
    sorted_result.sort(key=lambda x: x[1], reverse=True)
    for t, count in sorted_result:
        print(f"    {t:<14} {count}")
    print(f"  {'=' * 48}")


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

result = analyse_transactions(transactions, ETH_PRICE)
print_tx_report(result)

result_filtered = analyse_transactions(transactions, ETH_PRICE, min_value_eth=1.0)
print_tx_report(result_filtered, title="Large Transactions Only (>1 ETH)")

print("\n" + "=" * 60)
print("End of solutions. How did you do?")
print("=" * 60)
