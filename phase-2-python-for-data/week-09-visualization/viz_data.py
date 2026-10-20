"""
viz_data.py
Python for Blockchain Analytics — Phase 2, Week 9

Deterministic offline datasets for the visualization week. It reuses the
Week 8 datasets (DEX trades, gas, TVL) and adds two new ones:

    make_eth_ohlc()      daily ETH candles + volume (like a CoinGecko OHLC export)
    make_allocation()    a small portfolio for pie / bar charts

    from viz_data import *
"""
import os
import sys

import numpy as np
import pandas as pd

# Reuse Week 8 data (works no matter which folder you run from)
_WEEK8 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "week-08-pandas-numpy")
sys.path.insert(0, _WEEK8)
from sample_data import (  # noqa: E402, F401
    make_dex_trades, make_gas_prices, make_tvl, make_pair_info, make_wallet_labels,
)

PROTOCOL_COLORS = {
    "Uniswap":   "#ff007a",
    "Sushiswap": "#f59e0b",
    "Curve":     "#3465a4",
    "Balancer":  "#6b7280",
    "Aave":      "#b6509e",
    "Lido":      "#00a3ff",
}


def make_eth_ohlc(days: int = 120, seed: int = 21) -> pd.DataFrame:
    """Daily ETH OHLC + USD volume, a random walk starting near $3,200."""
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2026-06-01", periods=days, freq="D")
    close = 3200 * np.cumprod(1 + rng.normal(0.0008, 0.025, days))
    open_ = np.concatenate([[3200.0], close[:-1]])
    high = np.maximum(open_, close) * (1 + np.abs(rng.normal(0, 0.008, days)))
    low = np.minimum(open_, close) * (1 - np.abs(rng.normal(0, 0.008, days)))
    volume = rng.lognormal(mean=22.5, sigma=0.35, size=days)
    return pd.DataFrame({
        "date": dates, "open": open_.round(2), "high": high.round(2),
        "low": low.round(2), "close": close.round(2), "volume_usd": volume.round(0),
    })


def make_allocation() -> pd.DataFrame:
    """A small wallet portfolio (for allocation charts)."""
    return pd.DataFrame({
        "asset": ["ETH", "WBTC", "USDC", "UNI", "LINK", "AAVE"],
        "value_usd": [48_000, 22_000, 15_000, 6_500, 4_200, 2_800],
    })


if __name__ == "__main__":
    for name, fn in [("eth_ohlc", make_eth_ohlc), ("allocation", make_allocation),
                     ("dex_trades", make_dex_trades), ("gas_prices", make_gas_prices),
                     ("tvl", make_tvl)]:
        print(f"{name:<12} {fn().shape}")
