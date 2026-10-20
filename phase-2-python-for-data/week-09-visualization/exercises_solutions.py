"""
exercises_solutions.py
Python for Blockchain Analytics — Phase 2, Week 9: Data Visualization

⚠️  WARNING: Only open this file AFTER you have attempted exercises.py.

Run:  python3 exercises_solutions.py          (prints a structural summary)
      python3 exercises_solutions.py --save   (also writes PNG/HTML to charts/)
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")                      # headless: no windows, safe in scripts/CI
import matplotlib.pyplot as plt            # noqa: E402
import matplotlib.dates as mdates          # noqa: E402
from matplotlib.ticker import FuncFormatter   # noqa: E402
import seaborn as sns                      # noqa: E402
import plotly.express as px                # noqa: E402
import plotly.graph_objects as go          # noqa: E402

sys.path.insert(0, "../../phase-1-python-fundamentals/week-05-functions-modules")
from blockchain_utils import shorten_address                       # noqa: E402
from viz_data import (make_eth_ohlc, make_allocation, make_dex_trades,   # noqa: E402
                      make_gas_prices, make_tvl)

ETH_PRICE = 3_250.0


# ── Exercise 1 ─────────────────────────────────────────────────────────────────
def ex01_price_line(ohlc):
    """
    Line chart of ETH daily close price vs date.
    Needs: title, x-label, y-label. Return the Figure.
    Dune parallel: a 'Line chart' visualization on a (date, close) query result.
    """
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(ohlc["date"], ohlc["close"])
    ax.set_title("ETH daily close")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    return fig


# ── Exercise 2 ─────────────────────────────────────────────────────────────────
def ex02_moving_averages(ohlc):
    """
    Same chart plus a 7-day and a 30-day moving average of close
    (three lines total, each with a label, and a legend).
    SQL parallel: AVG(close) OVER (ORDER BY date ROWS n-1 PRECEDING)
    """
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(ohlc["date"], ohlc["close"], label="Close", alpha=0.5)
    ax.plot(ohlc["date"], ohlc["close"].rolling(7).mean(), label="7d MA")
    ax.plot(ohlc["date"], ohlc["close"].rolling(30).mean(), label="30d MA")
    ax.set_title("ETH close with moving averages")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.legend()
    return fig


# ── Exercise 3 ─────────────────────────────────────────────────────────────────
def ex03_volume_bar(trades):
    """
    Vertical bar chart of total amount_usd per protocol, tallest bar first.
    Needs: title and y-label.
    """
    vol = trades.groupby("protocol")["amount_usd"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(vol.index, vol.values)
    ax.set_title("DEX volume by protocol")
    ax.set_ylabel("Volume (USD)")
    return fig


# ── Exercise 4 ─────────────────────────────────────────────────────────────────
def ex04_wallet_barh(trades):
    """
    Horizontal bar chart of the TOP 5 wallets by total amount_usd.
    Y tick labels must be shortened addresses (shorten_address), the biggest
    wallet at the TOP of the chart. Needs a title.
    """
    top = trades.groupby("wallet")["amount_usd"].sum().nlargest(5).sort_values()   # ascending: barh draws bottom-up
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh([shorten_address(w) for w in top.index], top.values)
    ax.set_title("Top 5 wallets by volume")
    ax.set_xlabel("Volume (USD)")
    return fig


# ── Exercise 5 ─────────────────────────────────────────────────────────────────
def ex05_grouped_bar(trades):
    """
    Grouped bar chart: for each protocol, one bar for BUY volume and one for
    SELL volume side by side. Needs a legend and a title.
    Hint: pivot_table(index='protocol', columns='side', values='amount_usd', aggfunc='sum')
          then df.plot(kind='bar', ax=ax)
    """
    pv = trades.pivot_table(index="protocol", columns="side", values="amount_usd", aggfunc="sum")
    fig, ax = plt.subplots(figsize=(8, 4))
    pv.plot(kind="bar", ax=ax)
    ax.set_title("Buy vs sell volume by protocol")
    ax.set_ylabel("Volume (USD)")
    ax.legend(title="Side")
    return fig


# ── Exercise 6 ─────────────────────────────────────────────────────────────────
def ex06_scatter_loglog(trades):
    """
    Scatter: x = amount_usd, y = gas cost in USD (gas_used * gas_price_gwei / 1e9
    * ETH_PRICE). Drop rows with missing gas price first. BOTH axes log scale.
    Needs a title and axis labels.
    """
    d = trades.dropna(subset=["gas_price_gwei"]).copy()
    d["gas_cost_usd"] = d["gas_used"] * d["gas_price_gwei"] / 1e9 * ETH_PRICE
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.scatter(d["amount_usd"], d["gas_cost_usd"], s=10, alpha=0.4)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title("Trade size vs gas cost")
    ax.set_xlabel("Trade size (USD)")
    ax.set_ylabel("Gas cost (USD)")
    return fig


# ── Exercise 7 ─────────────────────────────────────────────────────────────────
def ex07_stacked_area(tvl):
    """
    Stacked area chart of TVL over time, one layer per protocol (4 layers),
    with a legend and a title.
    Hint: pivot long -> wide, then ax.stackplot(x, *columns, labels=...)
    """
    wide = tvl.pivot(index="date", columns="protocol", values="tvl_usd")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.stackplot(wide.index, [wide[c] for c in wide.columns], labels=wide.columns)
    ax.set_title("TVL by protocol")
    ax.set_ylabel("TVL (USD)")
    ax.legend(loc="upper left")
    return fig


# ── Exercise 8 ─────────────────────────────────────────────────────────────────
def ex08_price_and_volume(ohlc):
    """
    Two stacked panels sharing the x-axis: top = close price line,
    bottom = daily volume_usd as bars. Titles on the top panel.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 6),
                                   gridspec_kw={"height_ratios": [3, 1]})
    ax1.plot(ohlc["date"], ohlc["close"])
    ax1.set_title("ETH price and volume")
    ax1.set_ylabel("Price (USD)")
    ax2.bar(ohlc["date"], ohlc["volume_usd"])
    ax2.set_ylabel("Volume (USD)")
    return fig


# ── Exercise 9 ─────────────────────────────────────────────────────────────────
def ex09_gas_heatmap(gas):
    """
    Seaborn heatmap of MEAN base_fee_gwei: rows = day of week (0=Mon..6=Sun),
    columns = hour of day (0..23). Needs a title.
    Hint: gas['timestamp'].dt.dayofweek / .dt.hour, then pivot_table(aggfunc='mean')
    """
    d = gas.assign(dow=gas["timestamp"].dt.dayofweek, hour=gas["timestamp"].dt.hour)
    pv = d.pivot_table(index="dow", columns="hour", values="base_fee_gwei", aggfunc="mean")
    fig, ax = plt.subplots(figsize=(11, 4))
    sns.heatmap(pv, cmap="YlOrRd", ax=ax)
    ax.set_title("Mean base fee (gwei) by weekday and hour")
    return fig


# ── Exercise 10 ────────────────────────────────────────────────────────────────
def ex10_trade_size_hist(trades):
    """
    Seaborn histogram of amount_usd with exactly 30 bins and a LOG x-axis
    (trade sizes are heavy-tailed). Needs title and x-label.
    """
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.histplot(trades["amount_usd"], bins=30, log_scale=True, ax=ax)
    ax.set_title("Distribution of trade sizes")
    ax.set_xlabel("Trade size (USD, log scale)")
    return fig


# ── Exercise 11 ────────────────────────────────────────────────────────────────
def ex11_candlestick(ohlc):
    """
    Plotly candlestick chart from the OHLC data. Needs a title, and the
    range slider must be turned OFF.
    Return the plotly Figure.
    """
    fig = go.Figure(go.Candlestick(x=ohlc["date"], open=ohlc["open"], high=ohlc["high"],
                                   low=ohlc["low"], close=ohlc["close"], name="ETH"))
    fig.update_layout(title="ETH daily candles", xaxis_rangeslider_visible=False)
    return fig


# ── Exercise 12 ────────────────────────────────────────────────────────────────
def ex12_interactive_tvl(tvl):
    """
    Plotly Express line chart of TVL over time, one line per protocol (use
    the 'color' argument), with a title and a UNIFIED hover (hovermode).
    Return the plotly Figure.
    """
    fig = px.line(tvl, x="date", y="tvl_usd", color="protocol", title="TVL by protocol")
    fig.update_layout(hovermode="x unified")
    return fig


# ── Challenge ──────────────────────────────────────────────────────────────────
def challenge_dashboard(ohlc, trades, allocation):
    """
    One Figure, 2x2 grid, suptitle set, every panel has a title:
      [0,0] ETH close line            [0,1] volume by protocol (4 bars)
      [1,0] allocation pie (6 slices) [1,1] histogram of gas_price_gwei (>= 10 bins)
    Use plt.subplots(2, 2) and tight_layout. Return the Figure.
    """
    vol = trades.groupby("protocol")["amount_usd"].sum().sort_values(ascending=False)
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes[0, 0].plot(ohlc["date"], ohlc["close"])
    axes[0, 0].set_title("ETH close")
    axes[0, 0].xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))        # readable dates
    axes[0, 1].bar(vol.index, vol.values)
    axes[0, 1].set_title("Volume by protocol")
    axes[0, 1].yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${v/1e6:.1f}M"))   # no '1e6'
    axes[1, 0].pie(allocation["value_usd"], labels=allocation["asset"], autopct="%1.0f%%")
    axes[1, 0].set_title("Portfolio allocation")
    axes[1, 1].hist(trades["gas_price_gwei"].dropna(), bins=20)
    axes[1, 1].set_title("Gas price distribution")
    fig.suptitle("DeFi desk dashboard", fontsize=16)
    fig.tight_layout()
    return fig


# ── Runner ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    ohlc, trades, gas = make_eth_ohlc(), make_dex_trades(), make_gas_prices()
    tvl, alloc = make_tvl(), make_allocation()
    figs = {
        "ex01": ex01_price_line(ohlc), "ex02": ex02_moving_averages(ohlc),
        "ex03": ex03_volume_bar(trades), "ex04": ex04_wallet_barh(trades),
        "ex05": ex05_grouped_bar(trades), "ex06": ex06_scatter_loglog(trades),
        "ex07": ex07_stacked_area(tvl), "ex08": ex08_price_and_volume(ohlc),
        "ex09": ex09_gas_heatmap(gas), "ex10": ex10_trade_size_hist(trades),
        "ex11": ex11_candlestick(ohlc), "ex12": ex12_interactive_tvl(tvl),
        "challenge": challenge_dashboard(ohlc, trades, alloc),
    }
    for k, f in figs.items():
        kind = "plotly" if hasattr(f, "to_html") else "matplotlib"
        print(f"{k:<10} {kind} figure built")
    if "--save" in sys.argv:
        os.makedirs("charts", exist_ok=True)
        for k, f in figs.items():
            if hasattr(f, "to_html"):
                f.write_html(f"charts/{k}.html")
            else:
                f.savefig(f"charts/{k}.png", dpi=110, bbox_inches="tight")
        print("Saved to charts/")
    print("\nAll solutions ran ✓")
    print("Commit: git add . && git commit -m 'phase-2/week-09: solutions' && git push")
