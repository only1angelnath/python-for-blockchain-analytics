"""
exercises.py
Python for Blockchain Analytics — Phase 2, Week 8: Pandas & NumPy

HOW TO USE
  1. Read the docstring above each function. Every one has a SQL equivalent.
  2. Replace `# YOUR CODE HERE` / `return None` with your solution.
  3. Run:  python3 exercises.py
     Each exercise prints ✅ (correct), ❌ (wrong, shows what you returned)
     or ⬜ (not attempted yet).
  4. Stuck for 20+ minutes? Re-read the matching lesson section first.
     Only then open exercises_solutions.py.

Data is deterministic (fixed seed), so everyone gets identical numbers.
"""
import sys
sys.path.insert(0, "../../phase-1-python-fundamentals/week-05-functions-modules")

import numpy as np
import pandas as pd
from blockchain_utils import * # noqa: F401  (used in Exercise 15)
from sample_data import (make_dex_trades, make_gas_prices, make_tvl,
                         make_pair_info, make_wallet_labels)

ETH_PRICE = 3_250.0


# ── Exercise 1: Inspect ────────────────────────────────────────────────────────
def ex01_inspect(trades):
    """
    Return a tuple: (number_of_rows, number_of_missing_gas_price_values).
    SQL: SELECT COUNT(*), COUNT(*) - COUNT(gas_price_gwei) FROM trades
    Hint: len(), .isna(), .sum()
    """
    # YOUR CODE HERE
    num_rows = len(trades)
    num_missing_gas_price = trades['gas_price_gwei'].isna().sum()
    return (num_rows, num_missing_gas_price)


# ── Exercise 2: Filter with AND ────────────────────────────────────────────────
def ex02_filter_and(trades):
    """
    Count Uniswap BUY trades larger than $5,000.
    SQL: WHERE protocol = 'Uniswap' AND side = 'buy' AND amount_usd > 5000
    Hint: build a boolean mask with & and parentheses around each condition.
    """
    # YOUR CODE HERE
    mask = (trades['protocol'] == 'Uniswap') & (trades['side'] == 'buy') & (trades['amount_usd'] > 5000)
    return trades.loc[mask].shape[0]


# ── Exercise 3: IN and LIKE ────────────────────────────────────────────────────
def ex03_filter_isin_like(trades):
    """
    Count trades where the protocol is Curve or Balancer AND the pair
    starts with "WETH".
    SQL: WHERE protocol IN ('Curve','Balancer') AND pair LIKE 'WETH%'
    Hint: .isin() and .str.startswith()
    """
    # YOUR CODE HERE
    mask = trades['protocol'].isin(['Curve', 'Balancer']) & trades['pair'].str.startswith('WETH')
    return trades.loc[mask].shape[0]
    return None


# ── Exercise 4: Computed column with NULLs ─────────────────────────────────────
def ex04_gas_spend(trades):
    """
    Compute total gas spent in USD across all trades with a known gas price
    (ETH = $3,250, use the ETH_PRICE constant). Round to 2 decimals.
    gas_cost_eth = gas_used * gas_price_gwei / 1e9
    SQL: SUM(gas_used * gas_price_gwei / 1e9 * 3250)   -- SUM ignores NULLs
    Hint: vectorise, no loops. Does .sum() skip NaN by default?
    """
    # YOUR CODE HERE
    trades_with_gas_price = trades.dropna(subset=['gas_price_gwei'])
    trades_with_gas_price['gas_cost_usd'] = trades_with_gas_price['gas_used'] * trades_with_gas_price['gas_price_gwei'] / 1e9
    total_gas_spent_usd = trades_with_gas_price['gas_cost_usd'].sum() * ETH_PRICE
    return round(total_gas_spent_usd, 2)
    return None


# ── Exercise 5: CASE WHEN ──────────────────────────────────────────────────────
def ex05_case_when(trades):
    """
    Bucket trades by amount_usd: >= 50,000 'whale'; >= 5,000 'large';
    >= 500 'medium'; otherwise 'retail'. Return a dict {bucket: count}.
    SQL: CASE WHEN ... END, then GROUP BY bucket
    Hint: np.select(conditions, choices, default=...) then .value_counts()
    """
    # YOUR CODE HERE
    conditions = [
        trades['amount_usd'] >= 50_000,
        trades['amount_usd'] >= 5_000,
        trades['amount_usd'] >= 500
    ]
    choices = ['whale', 'large', 'medium']
    trades['bucket'] = np.select(conditions, choices, default='retail')
    return trades['bucket'].value_counts().to_dict()


# ── Exercise 6: GROUP BY ───────────────────────────────────────────────────────
def ex06_volume_by_protocol(trades):
    """
    Return a Series of total amount_usd per protocol, sorted largest first.
    SQL: SELECT protocol, SUM(amount_usd) FROM trades GROUP BY 1 ORDER BY 2 DESC
    """
    # YOUR CODE HERE
    volume_by_protocol = trades.groupby('protocol')['amount_usd'].sum().sort_values(ascending=False)
    return volume_by_protocol


# ── Exercise 7: GROUP BY + pick the winner ─────────────────────────────────────
def ex07_avg_trade_by_pair(trades):
    """
    Return a tuple (pair_name, average_trade_size_rounded_to_2dp) for the
    pair with the HIGHEST average amount_usd.
    SQL: SELECT pair, AVG(amount_usd) ... GROUP BY 1 ORDER BY 2 DESC LIMIT 1
    Hint: .groupby().mean(), then .idxmax() and .max()
    """
    # YOUR CODE HERE
    avg_trade_by_pair = trades.groupby('pair')['amount_usd'].mean()
    pair_with_highest_avg = avg_trade_by_pair.idxmax()
    highest_avg_trade_size = round(avg_trade_by_pair.max(), 2)
    return (pair_with_highest_avg, highest_avg_trade_size)  
    return None


# ── Exercise 8: Window function ────────────────────────────────────────────────
def ex08_top_trade_per_protocol(trades):
    """
    Return a dict {protocol: tx_hash} of the LARGEST trade in each protocol.
    SQL: ROW_NUMBER() OVER (PARTITION BY protocol ORDER BY amount_usd DESC) = 1
    Hint: groupby(...)["amount_usd"].idxmax() gives row labels you can pass to .loc
    """
    # YOUR CODE HERE
    top_trades = trades.loc[trades.groupby('protocol')['amount_usd'].idxmax()]
    return top_trades.set_index('protocol')['tx_hash'].to_dict()
    return None


# ── Exercise 9: LEFT JOIN + GROUP BY ───────────────────────────────────────────
def ex09_volume_by_category(trades, pair_info):
    """
    LEFT JOIN trades to pair_info on 'pair', then return a Series of total
    amount_usd per 'category', sorted largest first.
    Use validate="many_to_one" so a duplicate key can never inflate volume.
    SQL: FROM trades t LEFT JOIN pair_info p ON t.pair = p.pair GROUP BY p.category
    """
    # YOUR CODE HERE
    merged_df = trades.merge(pair_info[['pair', 'category']], on='pair', how='left', validate='many_to_one')
    volume_by_category = merged_df.groupby('category')['amount_usd'].sum().sort_values(ascending=False)
    return volume_by_category
    return None


# ── Exercise 10: Anti-join ─────────────────────────────────────────────────────
def ex10_unlabelled_wallets(trades, wallet_labels):
    """
    How many DISTINCT wallets in trades have NO entry in wallet_labels?
    SQL: SELECT COUNT(DISTINCT t.wallet) FROM trades t
         LEFT JOIN wallet_labels l ON t.wallet = l.wallet WHERE l.wallet IS NULL
    Hint: merge(..., how="left", indicator=True) and look at the _merge column.
    """
    # YOUR CODE HERE
    merged_df = trades.merge(wallet_labels[['wallet']], on='wallet', how='left', indicator=True)
    unlabelled_wallets_count = merged_df[merged_df['_merge'] == 'left_only']['wallet'].nunique()
    return unlabelled_wallets_count
    return None


# ── Exercise 11: NumPy percentiles ─────────────────────────────────────────────
def ex11_gas_percentiles(trades):
    """
    Return (p90, p99) of gas_price_gwei ignoring missing values, each
    rounded to 2 decimals. Use NumPy.
    Hint: .dropna().to_numpy() then np.percentile(arr, q)
    """
    # YOUR CODE HERE
    gas_prices = trades['gas_price_gwei'].dropna().to_numpy()
    p90 = round(np.percentile(gas_prices, 90), 2)
    p99 = round(np.percentile(gas_prices, 99), 2)
    return (p90, p99)
    return None


# ── Exercise 12: Resample ──────────────────────────────────────────────────────
def ex12_busiest_day(trades):
    """
    Return (date_string 'YYYY-MM-DD', volume_rounded_2dp) for the day with
    the highest total amount_usd.
    SQL: date_trunc('day', block_time) ... GROUP BY 1 ORDER BY 2 DESC LIMIT 1
    Hint: set_index("block_time"), then ["amount_usd"].resample("D").sum()
    """
    # YOUR CODE HERE
    trades['block_time'] = pd.to_datetime(trades['block_time'])
    trades.set_index('block_time', inplace=True)
    daily_volume = trades['amount_usd'].resample('D').sum()
    busiest_day = daily_volume.idxmax().strftime('%Y-%m-%d')
    highest_volume = round(daily_volume.max(), 2)
    return (busiest_day, highest_volume)
    return None


# ── Exercise 13: Rolling window ────────────────────────────────────────────────
def ex13_gas_rolling(gas):
    """
    gas has columns [timestamp, base_fee_gwei], hourly.
    Compute the 24-hour rolling mean of base_fee_gwei and return
    (timestamp_string 'YYYY-MM-DD HH:MM', value_rounded_2dp) for the hour
    where that rolling mean is highest.
    SQL: AVG(base_fee_gwei) OVER (ORDER BY timestamp ROWS 23 PRECEDING)
    Hint: .rolling(24).mean(), then .idxmax(); strftime("%Y-%m-%d %H:%M")
    """
    # YOUR CODE HERE
    gas['timestamp'] = pd.to_datetime(gas['timestamp'])
    gas.set_index('timestamp', inplace=True)
    rolling_mean = gas['base_fee_gwei'].rolling(window=24).mean()
    max_rolling_mean_timestamp = rolling_mean.idxmax().strftime('%Y-%m-%d %H:%M')
    max_rolling_mean_value = round(rolling_mean.max(), 2)
    return (max_rolling_mean_timestamp, max_rolling_mean_value)
    return None


# ── Exercise 14: Pivot + drawdown ──────────────────────────────────────────────
def ex14_worst_drawdown(tvl):
    """
    tvl is LONG format [date, protocol, tvl_usd]. Pivot it wide, then for each
    protocol compute max drawdown in % (lowest value of tvl / running max - 1).
    Return (protocol, drawdown_pct_rounded_2dp) for the WORST one.
    Hint: .pivot(), .cummax(), then .min() per column
    """
    # YOUR CODE HERE
    tvl['date'] = pd.to_datetime(tvl['date'])
    tvl_pivot = tvl.pivot(index='date', columns='protocol', values='tvl_usd')
    drawdowns = (tvl_pivot / tvl_pivot.cummax() - 1).min()
    worst_protocol = drawdowns.idxmin()
    worst_drawdown_pct = round(drawdowns.min() * 100, 2)
    return (worst_protocol, worst_drawdown_pct)
    return None


# ── Exercise 15: The Wei trap ──────────────────────────────────────────────────
def ex15_safe_wei_total(wei_values):
    """
    wei_values is a list of Python ints (several exceed 9.2 ETH worth of Wei).
    Return the total in ETH as a float, WITHOUT overflowing.
    Do NOT put them in an int64 NumPy array.
    Hint: Python ints never overflow. You already have wei_to_eth().
    """
    # YOUR CODE HERE
    total_wei = sum(wei_values)
    total_eth = wei_to_eth(total_wei)
    return total_eth
    return None


# ── Challenge: wallet summary ──────────────────────────────────────────────────
def challenge_wallet_summary(trades, pair_info, wallet_labels, eth_price=ETH_PRICE):
    """
    Build a wallet summary DataFrame with one row per wallet and columns:
      wallet, label (fill missing with 'unknown'), trades, volume_usd,
      gas_spent_usd, avg_trade_usd, favourite_pair (the pair they trade most).
    Return the top 3 wallets by volume_usd as a DataFrame (index reset).
    The checker looks at the wallet in row 0 and that all 7 columns exist.
    Hint: .agg() for the numbers; value_counts().idxmax() inside a groupby
    for favourite_pair; merge in labels; .fillna("unknown"); .nlargest(3, ...)
    """
    # YOUR CODE HERE
    d=trades.copy()
    d['gas_spent_usd'] = d['gas_used'] * d['gas_price_gwei'] / 1e9 * eth_price
    summary = d.groupby('wallet').agg(
        trades=('tx_hash', 'count'),
        volume_usd=('amount_usd', 'sum'),
        gas_spent_usd=('gas_spent_usd', 'sum'),
        avg_trade_usd=('amount_usd', 'mean'),
        favourite_pair=('pair', lambda x: x.value_counts().idxmax())
    ).reset_index()
    summary = summary.merge(wallet_labels, on='wallet', how='left')
    summary['label'] = summary['label'].fillna('unknown')
    summary = summary[['wallet', 'label', 'trades', 'volume_usd', 'gas_spent_usd', 'avg_trade_usd', 'favourite_pair']]
    top_3_wallets = summary.nlargest(3, 'volume_usd').reset_index(drop=True)
    return top_3_wallets
    return None


# ══════════════════════════════════════════════════════════════════════════════
# CHECKER: you do not need to edit anything below this line
# ══════════════════════════════════════════════════════════════════════════════
def _norm(x):
    if isinstance(x, pd.Series):
        return [(k, round(float(v), 2)) for k, v in x.items()]
    if isinstance(x, tuple):
        return tuple(_norm(i) for i in x)
    if isinstance(x, (float, np.floating)):
        return round(float(x), 2)
    if isinstance(x, (np.integer,)):
        return int(x)
    return x


def check(label, got, expected):
    if got is None:
        print(f"⬜ {label}: not attempted yet")
        return False
    try:
        ok = _norm(got) == _norm(expected)
    except (TypeError, ValueError):
        ok = False
    if ok:
        print(f"✅ {label}")
    else:
        print(f"❌ {label}\n     you returned: {_norm(got)!r}\n     expected    : (hidden. Re-read the docstring and the lesson)")
    return ok


if __name__ == "__main__":
    trades = make_dex_trades()
    gas, tvl = make_gas_prices(), make_tvl()
    pair_info, labels = make_pair_info(), make_wallet_labels()

    print("Week 8 — Pandas & NumPy exercises\n" + "-" * 50)
    results = [
        check("Ex 1  inspect",              ex01_inspect(trades), (1000, 15)),
        check("Ex 2  filter AND",           ex02_filter_and(trades), 35),
        check("Ex 3  IN + LIKE",            ex03_filter_isin_like(trades), 152),
        check("Ex 4  gas spend",            ex04_gas_spend(trades), 17925.98),
        check("Ex 5  CASE WHEN",            ex05_case_when(trades),
              {"medium": 585, "retail": 294, "large": 116, "whale": 5}),
        check("Ex 6  volume by protocol",   ex06_volume_by_protocol(trades),
              pd.Series({"Uniswap": 1561473.47, "Curve": 563482.96,
                         "Sushiswap": 535068.05, "Balancer": 320958.61})),
        check("Ex 7  avg trade by pair",    ex07_avg_trade_by_pair(trades), ("WETH-USDT", 3617.39)),
        check("Ex 8  top trade / protocol", ex08_top_trade_per_protocol(trades),
              {"Balancer": "0x2522f17df225", "Curve": "0xcee392b6baf7",
               "Sushiswap": "0xd8b23d7873dc", "Uniswap": "0x3730dc8011b3"}),
        check("Ex 9  volume by category",   ex09_volume_by_category(trades, pair_info),
              pd.Series({"major": 2261237.39, "defi": 515727.89, "stable": 204017.81})),
        check("Ex 10 unlabelled wallets",   ex10_unlabelled_wallets(trades, labels), 15),
        check("Ex 11 gas percentiles",      ex11_gas_percentiles(trades), (41.6, 62.49)),
        check("Ex 12 busiest day",          ex12_busiest_day(trades), ("2026-09-07", 340099.63)),
        check("Ex 13 rolling gas",          ex13_gas_rolling(gas), ("2026-09-06 20:00", 23.99)),
        check("Ex 14 worst drawdown",       ex14_worst_drawdown(tvl), ("Aave", -28.42)),
        check("Ex 15 safe Wei total",
              ex15_safe_wei_total([10 * 10**18, 250 * 10**18, 3 * 10**17, 5 * 10**18]), 265.3),
    ]

    ch = challenge_wallet_summary(trades, pair_info, labels)
    need = {"wallet", "label", "trades", "volume_usd", "gas_spent_usd", "avg_trade_usd", "favourite_pair"}
    ch_ok = (ch is not None and isinstance(ch, pd.DataFrame) and len(ch) == 3
             and need.issubset(ch.columns)
             and ch["wallet"].iloc[0] == "0xc334cfc4bb625d81e850982d8134bcd9e59a57bd")
    results.append(check("Challenge wallet summary", ch if ch is None else (True if ch_ok else "wrong"), True))

    done = sum(results)
    print("-" * 50)
    print(f"{done}/{len(results)} correct")
    print("\nNext steps:")
    print("  • Compare with exercises_solutions.py ONLY after attempting everything")
    print("  • Commit: git add . && git commit -m 'phase-2/week-08: my exercise attempts' && git push")
