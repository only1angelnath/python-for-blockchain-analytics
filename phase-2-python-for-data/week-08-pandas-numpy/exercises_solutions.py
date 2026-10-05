"""
exercises_solutions.py
Python for Blockchain Analytics — Phase 2, Week 8: Pandas & NumPy

⚠️  WARNING: Only open this file AFTER you have attempted exercises.py.
    Struggling with a problem for 20 minutes teaches more than reading
    the answer in 20 seconds.

Run:  python3 exercises_solutions.py
Each solution is checked against the same expected values as exercises.py.
"""
import sys
sys.path.insert(0, "../../phase-1-python-fundamentals/week-05-functions-modules")

import numpy as np
import pandas as pd
from blockchain_utils import wei_to_eth
from sample_data import (make_dex_trades, make_gas_prices, make_tvl,
                         make_pair_info, make_wallet_labels)

ETH_PRICE = 3_250.0


# ── Exercise 1 ─────────────────────────────────────────────────────────────────
def ex01_inspect(trades):
    """
    Return a tuple: (number_of_rows, number_of_missing_gas_price_values).
    SQL: SELECT COUNT(*), COUNT(*) - COUNT(gas_price_gwei) FROM trades
    """
    return (len(trades), int(trades["gas_price_gwei"].isna().sum()))


# ── Exercise 2 ─────────────────────────────────────────────────────────────────
def ex02_filter_and(trades):
    """
    Count Uniswap BUY trades larger than $5,000.
    SQL: WHERE protocol = 'Uniswap' AND side = 'buy' AND amount_usd > 5000
    """
    mask = (trades["protocol"] == "Uniswap") & (trades["side"] == "buy") & (trades["amount_usd"] > 5000)
    return int(mask.sum())


# ── Exercise 3 ─────────────────────────────────────────────────────────────────
def ex03_filter_isin_like(trades):
    """
    Count trades where the protocol is Curve or Balancer AND the pair
    starts with "WETH".
    SQL: WHERE protocol IN ('Curve','Balancer') AND pair LIKE 'WETH%'
    """
    mask = trades["protocol"].isin(["Curve", "Balancer"]) & trades["pair"].str.startswith("WETH")
    return int(mask.sum())


# ── Exercise 4 ─────────────────────────────────────────────────────────────────
def ex04_gas_spend(trades):
    """
    Compute total gas spent in USD across all trades with a known gas price
    (ETH = $3,250). Round to 2 decimals.
    gas_cost_eth = gas_used * gas_price_gwei / 1e9
    SQL: SUM(gas_used * gas_price_gwei / 1e9 * 3250) -- SUM ignores NULLs
    """
    cost = trades["gas_used"] * trades["gas_price_gwei"] / 1e9 * ETH_PRICE
    return round(float(cost.sum()), 2)          # Series.sum() skips NaN


# ── Exercise 5 ─────────────────────────────────────────────────────────────────
def ex05_case_when(trades):
    """
    Bucket trades by amount_usd: >= 50,000 'whale'; >= 5,000 'large';
    >= 500 'medium'; otherwise 'retail'. Return a dict {bucket: count}.
    SQL: CASE WHEN ... END, then GROUP BY bucket
    """
    bucket = np.select(
        [trades["amount_usd"] >= 50_000, trades["amount_usd"] >= 5_000, trades["amount_usd"] >= 500],
        ["whale", "large", "medium"],
        default="retail",
    )
    return pd.Series(bucket).value_counts().to_dict()


# ── Exercise 6 ─────────────────────────────────────────────────────────────────
def ex06_volume_by_protocol(trades):
    """
    Return a Series of total amount_usd per protocol, sorted largest first.
    SQL: SELECT protocol, SUM(amount_usd) FROM trades GROUP BY 1 ORDER BY 2 DESC
    """
    return trades.groupby("protocol")["amount_usd"].sum().sort_values(ascending=False)


# ── Exercise 7 ─────────────────────────────────────────────────────────────────
def ex07_avg_trade_by_pair(trades):
    """
    Return a tuple (pair_name, average_trade_size_rounded_to_2dp) for the
    pair with the HIGHEST average amount_usd.
    SQL: SELECT pair, AVG(amount_usd) ... GROUP BY 1 ORDER BY 2 DESC LIMIT 1
    """
    avg = trades.groupby("pair")["amount_usd"].mean()
    return (avg.idxmax(), round(float(avg.max()), 2))


# ── Exercise 8 ─────────────────────────────────────────────────────────────────
def ex08_top_trade_per_protocol(trades):
    """
    Return a dict {protocol: tx_hash} of the LARGEST trade in each protocol.
    SQL: ROW_NUMBER() OVER (PARTITION BY protocol ORDER BY amount_usd DESC) = 1
    Hint: rank within groups, or idxmax per group.
    """
    idx = trades.groupby("protocol")["amount_usd"].idxmax()
    return trades.loc[idx].set_index("protocol")["tx_hash"].to_dict()


# ── Exercise 9 ─────────────────────────────────────────────────────────────────
def ex09_volume_by_category(trades, pair_info):
    """
    LEFT JOIN trades to pair_info on 'pair', then return a Series of total
    amount_usd per 'category', sorted largest first.
    Use validate= so a duplicate key can never inflate volume.
    """
    merged = trades.merge(pair_info, on="pair", how="left", validate="many_to_one")
    return merged.groupby("category")["amount_usd"].sum().sort_values(ascending=False)


# ── Exercise 10 ────────────────────────────────────────────────────────────────
def ex10_unlabelled_wallets(trades, wallet_labels):
    """
    How many DISTINCT wallets in trades have NO entry in wallet_labels?
    SQL: SELECT COUNT(DISTINCT t.wallet) FROM trades t
         LEFT JOIN wallet_labels l ON t.wallet = l.wallet WHERE l.wallet IS NULL
    """
    wallets = trades[["wallet"]].drop_duplicates()
    m = wallets.merge(wallet_labels, on="wallet", how="left", indicator=True)
    return int((m["_merge"] == "left_only").sum())


# ── Exercise 11 ────────────────────────────────────────────────────────────────
def ex11_gas_percentiles(trades):
    """
    Return (p90, p99) of gas_price_gwei ignoring missing values, each
    rounded to 2 decimals. Use NumPy.
    """
    g = trades["gas_price_gwei"].dropna().to_numpy()
    return (round(float(np.percentile(g, 90)), 2), round(float(np.percentile(g, 99)), 2))


# ── Exercise 12 ────────────────────────────────────────────────────────────────
def ex12_busiest_day(trades):
    """
    Return (date_string 'YYYY-MM-DD', volume_rounded_2dp) for the day with
    the highest total amount_usd.
    SQL: date_trunc('day', block_time) ... GROUP BY 1 ORDER BY 2 DESC LIMIT 1
    """
    daily = trades.set_index("block_time")["amount_usd"].resample("D").sum()
    return (daily.idxmax().strftime("%Y-%m-%d"), round(float(daily.max()), 2))


# ── Exercise 13 ────────────────────────────────────────────────────────────────
def ex13_gas_rolling(gas):
    """
    gas has columns [timestamp, base_fee_gwei], hourly.
    Compute the 24-hour rolling mean of base_fee_gwei and return
    (timestamp_string 'YYYY-MM-DD HH:MM', value_rounded_2dp) for the hour
    where that rolling mean is highest.
    SQL: AVG(base_fee_gwei) OVER (ORDER BY timestamp ROWS 23 PRECEDING)
    """
    s = gas.set_index("timestamp")["base_fee_gwei"].rolling(24).mean()
    return (s.idxmax().strftime("%Y-%m-%d %H:%M"), round(float(s.max()), 2))


# ── Exercise 14 ────────────────────────────────────────────────────────────────
def ex14_worst_drawdown(tvl):
    """
    tvl is LONG format [date, protocol, tvl_usd]. Pivot it wide, then for each
    protocol compute max drawdown in % (lowest value of tvl / running max - 1).
    Return (protocol, drawdown_pct_rounded_2dp) for the WORST one.
    """
    wide = tvl.pivot(index="date", columns="protocol", values="tvl_usd")
    dd = (wide / wide.cummax() - 1) * 100
    worst = dd.min()
    return (worst.idxmin(), round(float(worst.min()), 2))


# ── Exercise 15 ────────────────────────────────────────────────────────────────
def ex15_safe_wei_total(wei_values):
    """
    wei_values is a list of Python ints (some > 9.2 ETH worth of Wei).
    Return the total in ETH as a float, WITHOUT overflowing.
    Do NOT put them in an int64 array.
    """
    total_wei = sum(wei_values)           # Python ints: arbitrary precision
    return wei_to_eth(total_wei)


# ── Challenge ──────────────────────────────────────────────────────────────────
def challenge_wallet_summary(trades, pair_info, wallet_labels, eth_price=ETH_PRICE):
    """
    Build a wallet summary DataFrame with one row per wallet and columns:
      wallet, label (fill missing with 'unknown'), trades, volume_usd,
      gas_spent_usd, avg_trade_usd, favourite_pair (the pair they trade most).
    Return the top 3 wallets by volume_usd as a DataFrame (index reset).
    """
    d = trades.copy()
    d["gas_cost_usd"] = d["gas_used"] * d["gas_price_gwei"] / 1e9 * eth_price
    g = d.groupby("wallet").agg(
        trades=("tx_hash", "count"),
        volume_usd=("amount_usd", "sum"),
        gas_spent_usd=("gas_cost_usd", "sum"),
        avg_trade_usd=("amount_usd", "mean"),
    ).reset_index()
    fav = (d.groupby("wallet")["pair"].agg(lambda s: s.value_counts().idxmax())
             .rename("favourite_pair").reset_index())
    out = (g.merge(fav, on="wallet", validate="one_to_one")
            .merge(wallet_labels, on="wallet", how="left", validate="many_to_one"))
    out["label"] = out["label"].fillna("unknown")
    return out.nlargest(3, "volume_usd").reset_index(drop=True)


# ── Runner ─────────────────────────────────────────────────────────────────────
def _norm(x):
    if isinstance(x, pd.Series):
        return [(k, round(float(v), 2)) for k, v in x.items()]
    if isinstance(x, tuple):
        return tuple(_norm(i) for i in x)
    if isinstance(x, float):
        return round(x, 6)
    return x


if __name__ == "__main__":
    trades = make_dex_trades()
    gas, tvl = make_gas_prices(), make_tvl()
    pair_info, labels = make_pair_info(), make_wallet_labels()

    results = {
        "ex01": ex01_inspect(trades),
        "ex02": ex02_filter_and(trades),
        "ex03": ex03_filter_isin_like(trades),
        "ex04": ex04_gas_spend(trades),
        "ex05": ex05_case_when(trades),
        "ex06": ex06_volume_by_protocol(trades),
        "ex07": ex07_avg_trade_by_pair(trades),
        "ex08": ex08_top_trade_per_protocol(trades),
        "ex09": ex09_volume_by_category(trades, pair_info),
        "ex10": ex10_unlabelled_wallets(trades, labels),
        "ex11": ex11_gas_percentiles(trades),
        "ex12": ex12_busiest_day(trades),
        "ex13": ex13_gas_rolling(gas),
        "ex14": ex14_worst_drawdown(tvl),
        "ex15": ex15_safe_wei_total([10 * 10**18, 250 * 10**18, 3 * 10**17, 5 * 10**18]),
        "challenge": challenge_wallet_summary(trades, pair_info, labels)["wallet"].iloc[0],
    }
    for k, v in results.items():
        print(f"{k:<10} {_norm(v)}")
    print("\nAll solutions ran ✓")
    print("Commit: git add . && git commit -m 'phase-2/week-08: solutions' && git push")
