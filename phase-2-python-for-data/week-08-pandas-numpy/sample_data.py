"""
sample_data.py
Python for Blockchain Analytics — Phase 2, Week 8

Deterministic, offline sample datasets for the Pandas & NumPy week.
Same seed => same data, so your numbers match the lesson and the solutions.

    from sample_data import (make_dex_trades, make_gas_prices,
                             make_tvl, make_pair_info, make_wallet_labels)

These are SYNTHETIC but shaped like the tables you already query on Dune:
    dex.trades        -> make_dex_trades()
    gas.fees          -> make_gas_prices()
    DefiLlama /tvl    -> make_tvl()
"""
import numpy as np
import pandas as pd

PROTOCOLS = ["Uniswap", "Sushiswap", "Curve", "Balancer"]
PAIRS = ["WETH-USDC", "WETH-USDT", "WBTC-WETH", "DAI-USDC", "UNI-WETH", "LINK-WETH"]


def make_wallet_addresses(n: int = 40, seed: int = 7) -> list:
    """Generate n fake-but-valid-looking 0x addresses."""
    rng = np.random.default_rng(seed)
    return ["0x" + "".join(rng.choice(list("0123456789abcdef"), 40)) for _ in range(n)]


def make_dex_trades(n: int = 1000, seed: int = 42) -> pd.DataFrame:
    """One row per DEX trade over 14 days (like dex.trades)."""
    rng = np.random.default_rng(seed)
    wallets = make_wallet_addresses()
    start = pd.Timestamp("2026-09-01")
    seconds = rng.integers(0, 14 * 24 * 3600, n)
    df = pd.DataFrame({
        "tx_hash": ["0x" + "".join(rng.choice(list("0123456789abcdef"), 12)) for _ in range(n)],
        "block_time": start + pd.to_timedelta(np.sort(seconds), unit="s"),
        "protocol": rng.choice(PROTOCOLS, n, p=[0.55, 0.15, 0.2, 0.1]),
        "pair": rng.choice(PAIRS, n, p=[0.35, 0.2, 0.15, 0.1, 0.1, 0.1]),
        "wallet": rng.choice(wallets, n),
        "side": rng.choice(["buy", "sell"], n),
        "amount_usd": np.round(rng.lognormal(mean=7.0, sigma=1.4, size=n), 2),
        "gas_used": rng.integers(100_000, 350_000, n),
        "gas_price_gwei": np.round(rng.gamma(shape=4, scale=6, size=n), 2),
    })
    # Realistic dirt: a few missing gas prices (NULLs)
    df.loc[rng.choice(n, 15, replace=False), "gas_price_gwei"] = np.nan
    return df


def make_gas_prices(days: int = 14, seed: int = 11) -> pd.DataFrame:
    """Hourly base fee in gwei with a daily cycle (busy US/EU hours)."""
    rng = np.random.default_rng(seed)
    ts = pd.date_range("2026-09-01", periods=days * 24, freq="h")
    daily_cycle = 8 * np.sin((ts.hour - 8) / 24 * 2 * np.pi) + 18
    noise = rng.normal(0, 3, len(ts))
    spikes = (rng.random(len(ts)) < 0.02) * rng.uniform(20, 60, len(ts))
    return pd.DataFrame({"timestamp": ts,
                         "base_fee_gwei": np.round(np.clip(daily_cycle + noise + spikes, 1, None), 2)})


def make_tvl(days: int = 90, seed: int = 5) -> pd.DataFrame:
    """Daily TVL per protocol (long format, like a DefiLlama export)."""
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2026-07-01", periods=days, freq="D")
    start_tvl = {"Aave": 12e9, "Lido": 25e9, "Uniswap": 5e9, "Curve": 2e9}
    rows = []
    for name, tvl0 in start_tvl.items():
        walk = np.cumprod(1 + rng.normal(0.001, 0.02, days)) * tvl0
        rows.append(pd.DataFrame({"date": dates, "protocol": name, "tvl_usd": walk.round(0)}))
    return pd.concat(rows, ignore_index=True)


def make_pair_info() -> pd.DataFrame:
    """Dimension table: one row per pair (for JOIN practice)."""
    return pd.DataFrame({
        "pair": PAIRS + ["PEPE-WETH"],           # PEPE-WETH has no trades on purpose
        "category": ["major", "major", "major", "stable", "defi", "defi", "meme"],
        "risk_score": [1, 1, 1, 0, 3, 3, 5],
    })


def make_wallet_labels() -> pd.DataFrame:
    """Dimension table: labels for SOME wallets (so LEFT JOIN leaves NULLs)."""
    wallets = make_wallet_addresses()
    labels = ["whale", "market_maker", "retail", "bot", "fund"]
    rng = np.random.default_rng(3)
    chosen = wallets[:25]                         # only 25 of 40 are labelled
    return pd.DataFrame({"wallet": chosen, "label": rng.choice(labels, len(chosen))})


if __name__ == "__main__":
    for name, fn in [("dex_trades", make_dex_trades), ("gas_prices", make_gas_prices),
                     ("tvl", make_tvl), ("pair_info", make_pair_info),
                     ("wallet_labels", make_wallet_labels)]:
        d = fn()
        print(f"{name:<14} {d.shape}")
