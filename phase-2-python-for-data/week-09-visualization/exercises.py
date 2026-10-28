"""
exercises.py
Python for Blockchain Analytics — Phase 2, Week 9: Data Visualization

HOW TO USE
  1. Read the docstring above each function, then write your chart code.
     Every function must RETURN the figure (don't call plt.show()).
  2. Run:  python3 exercises.py
     Each exercise prints ✅ / ❌ (with what is wrong) / ⬜ (not attempted).
  3. See your charts:  python3 exercises.py --save
     This writes PNG/HTML files into a charts/ folder. Open them and LOOK.
     The checker tests structure (titles, bars, lines, scales). Whether the
     chart is actually clear is your job as the analyst.
  4. Stuck for 20+ minutes? Re-read the lesson section first. Only then
     open exercises_solutions.py.
"""
import os
import sys

from matplotlib.ticker import FuncFormatter
import numpy as np
import matplotlib
matplotlib.use("Agg")                      # headless backend: figures are checked, not shown
import matplotlib.pyplot as plt            # noqa: E402, F401
import seaborn as sns                      # noqa: E402, F401
import plotly.express as px                # noqa: E402, F401
import plotly.graph_objects as go          # noqa: E402, F401

sys.path.insert(0, "../../phase-1-python-fundamentals/week-05-functions-modules")
from blockchain_utils import shorten_address                       # noqa: E402, F401
from viz_data import (make_eth_ohlc, make_allocation, make_dex_trades,   # noqa: E402
                      make_gas_prices, make_tvl)

ETH_PRICE = 3_250.0


# ── Exercise 1: Line chart ─────────────────────────────────────────────────────
def ex01_price_line(ohlc):
    """
    Line chart of ETH daily close price vs date.
    Needs: title, x-label, y-label. Return the Figure.
    Dune parallel: a 'Line chart' visualization on a (date, close) query result.
    Hint: fig, ax = plt.subplots(figsize=(10, 4)); ax.plot(x, y); ax.set_title(...)
    """
    # YOUR CODE HERE
    fig, ax =plt.subplots(figsize=(14,5))
    ax.plot(ohlc['date'], ohlc['close'], color='red', linewidth=1.2)
    ax.set_title("$ETH daily price")
    ax.set_ylabel("Price(USD)")
    ax.set_xlabel("Date")
    ax.yaxis.set_major_formatter(lambda v, _: f"${v:,.0f}")
    ax.xaxis.set_major_formatter("%b %Y")
    return fig

# ── Exercise 2: Overlay moving averages ────────────────────────────────────────
def ex02_moving_averages(ohlc):
    """
    Same chart plus a 7-day and a 30-day moving average of close
    (three lines total, each with a label, and a legend).
    SQL parallel: AVG(close) OVER (ORDER BY date ROWS n-1 PRECEDING)
    Hint: Series.rolling(n).mean(); pass label= to ax.plot; then ax.legend()
    """
    # YOUR CODE HERE
    fig, ax =plt.subplots(figsize=(14,5))
    ax.plot(ohlc['date'], ohlc['close'], color='red', linewidth=1.2, label="Close", alpha=0.5)
    ax.plot(ohlc["date"], ohlc["close"].rolling(7).mean(), color='blue', label="7d MA")
    ax.plot(ohlc["date"], ohlc["close"].rolling(30).mean(), label="30d MA", color='yellow')
    ax.set_title("$ETH daily price with Moving average", fontweight='bold', loc="center")
    ax.set_ylabel("Price(USD)", loc="center")
    ax.set_xlabel("Date")
    ax.yaxis.set_major_formatter(lambda v, _: f"${v:,.0f}")
    ax.xaxis.set_major_formatter("%b %Y")
    ax.legend()
    return fig


# ── Exercise 3: Bar chart ──────────────────────────────────────────────────────
def ex03_volume_bar(trades):
    """
    Vertical bar chart of total amount_usd per protocol, tallest bar first.
    Needs: title and y-label.
    Dune parallel: 'Bar chart' on SELECT protocol, SUM(amount_usd) ... ORDER BY 2 DESC
    """
    # YOUR CODE HERE
    vol=trades.groupby("protocol")["amount_usd"].sum().sort_values(ascending=False)

    fig, ax=plt.subplots(figsize=(10,5))
    ax.bar(vol.index, vol.values)
    ax.set_title("Protocol Volume (USD)")
    ax.set_ylabel("Volume(USD)")
    return fig


# ── Exercise 4: Horizontal bars with readable labels ───────────────────────────
def ex04_wallet_barh(trades):
    """
    Horizontal bar chart of the TOP 5 wallets by total amount_usd.
    Y tick labels must be shortened addresses (shorten_address), the biggest
    wallet at the TOP of the chart. Needs a title.
    Hint: ax.barh draws the first item at the BOTTOM. Sort accordingly.
    """
    # YOUR CODE HERE
    big=trades.groupby("wallet")["amount_usd"].sum().nlargest(5).sort_values()

    fig, ax=plt.subplots(figsize=(10,5))
    ax.barh([shorten_address(w) for w in big.index], big.values)
    ax.set_title("Top 5 wallets by Volume(USD)")
    ax.set_ylabel("Volume(USD)")
    return fig


# ── Exercise 5: Grouped bars ───────────────────────────────────────────────────
def ex05_grouped_bar(trades):
    """
    Grouped bar chart: for each protocol, one bar for BUY volume and one for
    SELL volume side by side. Needs a legend and a title.
    Hint: pivot_table(index='protocol', columns='side', values='amount_usd', aggfunc='sum')
          then df.plot(kind='bar', ax=ax)
    """
    # YOUR CODE HERE
    pv=trades.pivot_table(index="protocol", columns="side", values="amount_usd", aggfunc="sum")

    fig, ax=plt.subplots(figsize=(12,5))
    pv.plot(kind="bar", ax=ax)
    ax.set_title("Protocol Buy vs Sell Volume (USD) ")
    ax.set_ylabel("Volume(USD) by Side")
    return fig


# ── Exercise 6: Scatter on log-log axes ────────────────────────────────────────
def ex06_scatter_loglog(trades):
    """
    Scatter: x = amount_usd, y = gas cost in USD (gas_used * gas_price_gwei / 1e9
    * ETH_PRICE). Drop rows with missing gas price first. BOTH axes log scale.
    Needs a title and axis labels.
    Hint: ax.scatter(..., s=10, alpha=0.4); ax.set_xscale("log")
    """
    # YOUR CODE HERE
    d = trades.dropna(subset=["gas_price_gwei"]).copy()
    d["gas_cost_usd"] = d["gas_used"] * d["gas_price_gwei"] / 1e9 * ETH_PRICE

    fig, ax=plt.subplots(figsize=(12,4.5))
    ax.scatter(d["amount_usd"], d["gas_cost_usd"], s=8, alpha=0.3)
    ax.set_title("SCatter plot of Volume(USD) vs gas cost(USD)")
    ax.set_xscale('log')
    ax.set_yscale("log")
    ax.set_xlabel("Volume")
    ax.set_ylabel("GAs cost")
    return fig


# ── Exercise 7: Stacked area ───────────────────────────────────────────────────
def ex07_stacked_area(tvl):
    """
    Stacked area chart of TVL over time, one layer per protocol (4 layers),
    with a legend and a title.
    Hint: pivot long -> wide, then ax.stackplot(x, [series...], labels=[...])
    """
    # YOUR CODE HERE
    wide=tvl.pivot_table(index="date", columns="protocol", values="tvl_usd")

    fig, ax=plt.subplots(figsize=(10,4.5))
    ax.stackplot(wide.index, wide.T.values, labels=wide.columns)
    ax.set_title("Stacked Total Value Locked per protocol")
    ax.legend(loc="upper left")
    ax.set_ylabel("TVL(USD)")
    return fig


# ── Exercise 8: Two panels, shared x-axis ──────────────────────────────────────
def ex08_price_and_volume(ohlc):
    """
    Two stacked panels sharing the x-axis: top = close price line,
    bottom = daily volume_usd as bars. Put a title on the top panel.
    Hint: plt.subplots(2, 1, sharex=True, gridspec_kw={"height_ratios": [3, 1]})
    """
    # YOUR CODE HERE
    fig, axes=plt.subplots(2, 1, sharex=True, gridspec_kw={"height_ratios": [3, 1]}, figsize=(12,6))

    axes[0].plot(ohlc["date"], ohlc["close"])
    axes[0].set_title("ETH daily price and volume")
    axes[0].set_ylabel("Price(USD)")
    axes[0].yaxis.set_major_formatter(lambda v, _: f"${v:,.0f}")
    axes[0].set_xlabel("Date")

    axes[1].bar(ohlc["date"], ohlc["volume_usd"])
    axes[1].set_ylabel("Volume(USD)", loc="center")
    axes[1].yaxis.set_major_formatter(lambda v, _: f"${v:,.0f}")
    axes[1].set_xlabel("Date")
    return fig


# ── Exercise 9: Seaborn heatmap ────────────────────────────────────────────────
def ex09_gas_heatmap(gas):
    """
    Seaborn heatmap of MEAN base_fee_gwei: rows = day of week (0=Mon..6=Sun),
    columns = hour of day (0..23). Needs a title.
    Hint: gas['timestamp'].dt.dayofweek / .dt.hour, then pivot_table(aggfunc='mean'),
          then sns.heatmap(pivot, cmap="YlOrRd", ax=ax)
    """
    # YOUR CODE HERE
    gas["day_of_week"] = gas["timestamp"].dt.dayofweek
    gas["hour_of_day"] = gas["timestamp"].dt.hour
    pivot = gas.pivot_table(index="day_of_week", columns="hour_of_day", values="base_fee_gwei", aggfunc="mean")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(pivot, cmap="YlOrRd", ax=ax)
    ax.set_title("Mean Base Fee Gwei by Day of Week and Hour of Day")
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Day of Week (0=Mon, 6=Sun)")
    ax.legend(title="Mean Base Fee (Gwei)", loc="upper right")
    return fig


# ── Exercise 10: Histogram of a heavy-tailed variable ──────────────────────────
def ex10_trade_size_hist(trades):
    """
    Seaborn histogram of amount_usd with exactly 30 bins and a LOG x-axis
    (trade sizes are heavy-tailed). Needs title and x-label.
    Hint: sns.histplot(data, bins=..., log_scale=True, ax=ax)
    """
    # YOUR CODE HERE
    data=trades["amount_usd"].dropna()

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.histplot(data, bins=30, log_scale=True, ax=ax)
    ax.set_title("Distribution of trade sizes")
    ax.set_xlabel("Trade size (USD, log scale)")
    return fig

# ── Exercise 11: Plotly candlestick ────────────────────────────────────────────
def ex11_candlestick(ohlc):
    """
    Plotly candlestick chart from the OHLC data. Needs a title, and the
    range slider must be turned OFF. Return the plotly Figure.
    Hint: go.Figure(go.Candlestick(x=..., open=..., high=..., low=..., close=...))
          fig.update_layout(title=..., xaxis_rangeslider_visible=...)
    """
    # YOUR CODE HERE
    fig = go.Figure(go.Candlestick(
        x=ohlc['date'], open=ohlc['open'], high=ohlc['high'], low=ohlc['low'], close=ohlc['close'],
        name="ETH"
    ))
    fig.update_layout(title="ETH Candlestick Chart", xaxis_rangeslider_visible=False)
    return fig


# ── Exercise 12: Interactive multi-line ────────────────────────────────────────
def ex12_interactive_tvl(tvl):
    """
    Plotly Express line chart of TVL over time, one line per protocol (use
    the 'color' argument), with a title and a UNIFIED hover (hovermode).
    Return the plotly Figure.
    Hint: px.line(df, x=, y=, color=, title=); fig.update_layout(hovermode="x unified")
    """
    # YOUR CODE HERE
    fig = px.line(tvl, x='date', y='tvl_usd', color='protocol', title='TVL over time by protocol')
    fig.update_layout(hovermode="x unified")
    return fig


# ── Challenge: 2x2 dashboard ───────────────────────────────────────────────────
def challenge_dashboard(ohlc, trades, allocation):
    """
    One Figure, 2x2 grid, a suptitle, and a title on every panel:
      [0,0] ETH close line            [0,1] volume by protocol (4 bars)
      [1,0] allocation pie (6 slices) [1,1] histogram of gas_price_gwei (>= 10 bins)
    Use plt.subplots(2, 2) and fig.tight_layout(). Return the Figure.
    Bonus (not checked): format the dates and the $ axis so nothing overlaps
    and no '1e6' appears. Look at charts/challenge.png.
    """
    # YOUR CODE HERE
    """
        One Figure, 2x2 grid, suptitle set, every panel has a title:
        [0,0] ETH close line            [0,1] volume by protocol (4 bars)
        [1,0] allocation pie (6 slices) [1,1] histogram of gas_price_gwei (>= 10 bins)
        Use plt.subplots(2, 2) and tight_layout. Return the Figure.
        Bonus (not checked): format the dates and the $ axis so nothing overlaps
    """
    vol = trades.groupby("protocol")["amount_usd"].sum().sort_values(ascending=False)
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes[0, 0].plot(ohlc["date"], ohlc["close"])
    axes[0, 0].set_title("ETH close")
    #axes[0, 0].xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))        # readable dates
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


# ══════════════════════════════════════════════════════════════════════════════
# CHECKER: you do not need to edit anything below this line
# ══════════════════════════════════════════════════════════════════════════════
def _is_plotly(f):
    return hasattr(f, "to_html")


def _txt(s):
    return bool(s and str(s).strip())


def _problems_ex01(f, ohlc):
    ax, p = f.axes[0], []
    if len(ax.lines) != 1:
        return [f"expected 1 line, found {len(ax.lines)}"]
    if len(ax.lines[0].get_ydata()) != len(ohlc):
        p.append("line should have one point per day")
    elif abs(float(ax.lines[0].get_ydata()[-1]) - float(ohlc["close"].iloc[-1])) > 0.01:
        p.append("y data is not the close price")
    if not (_txt(ax.get_title()) and _txt(ax.get_xlabel()) and _txt(ax.get_ylabel())):
        p.append("needs a title, x-label and y-label")
    return p


def _problems_ex02(f, ohlc):
    ax, p = f.axes[0], []
    if len(ax.lines) != 3:
        return [f"expected 3 lines, found {len(ax.lines)}"]
    nans = sorted(int(np.isnan(ln.get_ydata().astype(float)).sum()) for ln in ax.lines)
    if nans != [0, 6, 29]:
        p.append("expected one raw line, a 7-day MA and a 30-day MA (rolling windows)")
    if ax.get_legend() is None:
        p.append("needs a legend")
    return p


def _problems_ex03(f, _):
    ax = f.axes[0]
    h = [round(b.get_height()) for b in ax.patches]
    p = []
    if h != [1561473, 563483, 535068, 320959]:
        p.append(f"bar heights {h} are not volume per protocol, tallest first")
    if not (_txt(ax.get_title()) and _txt(ax.get_ylabel())):
        p.append("needs a title and y-label")
    return p


def _problems_ex04(f, _):
    ax = f.axes[0]
    w = [round(b.get_width()) for b in ax.patches]
    labels = [t.get_text() for t in ax.get_yticklabels()]
    p = []
    if len(w) != 5:
        return [f"expected 5 bars, found {len(w)}"]
    if sorted(w) != [125590, 127629, 132903, 133083, 158959]:
        p.append("bar lengths are not the top 5 wallets by volume")
    elif w != sorted(w):
        p.append("biggest wallet must be at the TOP (barh draws the first bar at the bottom)")
    if not all("..." in lab for lab in labels):
        p.append("y labels must be shortened addresses")
    if not _txt(ax.get_title()):
        p.append("needs a title")
    return p


def _problems_ex05(f, _):
    ax = f.axes[0]
    got = [[round(b.get_height()) for b in c] for c in ax.containers]
    p = []
    if got != [[186079, 360375, 358669, 785734], [134880, 203108, 176399, 775739]]:
        p.append("expected two bar groups (buy, sell) with volume per protocol")
    if ax.get_legend() is None or not _txt(ax.get_title()):
        p.append("needs a legend and a title")
    return p


def _problems_ex06(f, _):
    ax, p = f.axes[0], []
    n = sum(len(c.get_offsets()) for c in ax.collections)
    if n != 985:
        p.append(f"expected 985 points (rows with a gas price), found {n}")
    if ax.get_xscale() != "log" or ax.get_yscale() != "log":
        p.append("both axes must be log scale")
    if not (_txt(ax.get_title()) and _txt(ax.get_xlabel()) and _txt(ax.get_ylabel())):
        p.append("needs a title and both axis labels")
    return p


def _problems_ex07(f, _):
    ax, p = f.axes[0], []
    if len(ax.collections) != 4:
        p.append(f"expected 4 stacked layers, found {len(ax.collections)}")
    if ax.get_legend() is None or not _txt(ax.get_title()):
        p.append("needs a legend and a title")
    return p


def _problems_ex08(f, _):
    p = []
    if len(f.axes) != 2:
        return [f"expected 2 panels, found {len(f.axes)}"]
    a1, a2 = f.axes
    if not a1.get_shared_x_axes().joined(a1, a2):
        p.append("panels must share the x-axis (sharex=True)")
    if len(a1.lines) != 1:
        p.append("top panel should have the price line")
    if len(a2.patches) != 120:
        p.append("bottom panel should have 120 volume bars")
    if not _txt(a1.get_title()):
        p.append("top panel needs a title")
    return p


def _problems_ex09(f, _):
    p = []
    if not f.axes or not f.axes[0].collections:
        return ["no heatmap found"]
    if f.axes[0].collections[0].get_array().size != 168:
        p.append("heatmap should have 7 weekdays x 24 hours = 168 cells")
    if not _txt(f.axes[0].get_title()):
        p.append("needs a title")
    return p


def _problems_ex10(f, _):
    ax, p = f.axes[0], []
    if len(ax.patches) != 30:
        p.append(f"expected 30 bins, found {len(ax.patches)}")
    if ax.get_xscale() != "log":
        p.append("x-axis must be log scale")
    if not (_txt(ax.get_title()) and _txt(ax.get_xlabel())):
        p.append("needs a title and x-label")
    return p


def _problems_ex11(f, _):
    p = []
    if not _is_plotly(f) or not f.data or f.data[0].type != "candlestick":
        return ["expected a plotly figure with a Candlestick trace"]
    if len(f.data[0].x) != 120:
        p.append("expected 120 candles")
    if f.layout.xaxis.rangeslider.visible is not False:
        p.append("range slider must be turned off")
    if not _txt(f.layout.title.text):
        p.append("needs a title")
    return p


def _problems_ex12(f, _):
    p = []
    if not _is_plotly(f):
        return ["expected a plotly figure"]
    if len(f.data) != 4:
        p.append(f"expected 4 lines (one per protocol), found {len(f.data)}")
    if f.layout.hovermode != "x unified":
        p.append('hovermode must be "x unified"')
    if not _txt(f.layout.title.text):
        p.append("needs a title")
    return p


def _problems_challenge(f, _):
    p = []
    if len(f.axes) != 4:
        return [f"expected 4 panels, found {len(f.axes)}"]
    a = f.axes
    if getattr(f, "_suptitle", None) is None:
        p.append("needs a suptitle (fig.suptitle)")
    if not all(_txt(x.get_title()) for x in a):
        p.append("every panel needs a title")
    if len(a[0].lines) != 1:
        p.append("[0,0] should be a line chart")
    if len(a[1].patches) != 4:
        p.append("[0,1] should have 4 bars")
    if len(a[2].patches) != 6:
        p.append("[1,0] should be a pie with 6 slices")
    if len(a[3].patches) < 10:
        p.append("[1,1] should be a histogram with at least 10 bins")
    return p


def check(label, build, problems_fn, data, saved):
    try:
        fig = build()
    except Exception as e:  # noqa: BLE001  (a learner's code may raise anything)
        print(f"❌ {label}\n     your code raised: {type(e).__name__}: {e}")
        return False
    if fig is None:
        print(f"⬜ {label}: not attempted yet")
        return False
    if not (hasattr(fig, "axes") or _is_plotly(fig)):
        print(f"❌ {label}\n     return the figure object (fig), not None or an Axes")
        return False
    try:
        problems = problems_fn(fig, data)
    except Exception as e:  # noqa: BLE001
        problems = [f"could not inspect your figure ({type(e).__name__}); check the docstring"]
    if saved is not None:
        key = label.split()[0:2]
        name = "challenge" if label.startswith("Challenge") else f"ex{int(key[1]):02d}"
        os.makedirs("charts", exist_ok=True)
        if _is_plotly(fig):
            fig.write_html(f"charts/{name}.html")
        else:
            fig.savefig(f"charts/{name}.png", dpi=110, bbox_inches="tight")
    if problems:
        print(f"❌ {label}")
        for pr in problems:
            print(f"     - {pr}")
        return False
    print(f"✅ {label}")
    return True


if __name__ == "__main__":
    ohlc, trades, gas = make_eth_ohlc(), make_dex_trades(), make_gas_prices()
    tvl, alloc = make_tvl(), make_allocation()
    saved = True if "--save" in sys.argv else None

    print("Week 9 — Data Visualization exercises\n" + "-" * 50)
    plan = [
        ("Ex 1  price line",        lambda: ex01_price_line(ohlc),            _problems_ex01, ohlc),
        ("Ex 2  moving averages",   lambda: ex02_moving_averages(ohlc),       _problems_ex02, ohlc),
        ("Ex 3  volume bars",       lambda: ex03_volume_bar(trades),          _problems_ex03, None),
        ("Ex 4  wallet barh",       lambda: ex04_wallet_barh(trades),         _problems_ex04, None),
        ("Ex 5  grouped bars",      lambda: ex05_grouped_bar(trades),         _problems_ex05, None),
        ("Ex 6  log-log scatter",   lambda: ex06_scatter_loglog(trades),      _problems_ex06, None),
        ("Ex 7  stacked area",      lambda: ex07_stacked_area(tvl),           _problems_ex07, None),
        ("Ex 8  price + volume",    lambda: ex08_price_and_volume(ohlc),      _problems_ex08, None),
        ("Ex 9  gas heatmap",       lambda: ex09_gas_heatmap(gas),            _problems_ex09, None),
        ("Ex 10 trade size hist",   lambda: ex10_trade_size_hist(trades),     _problems_ex10, None),
        ("Ex 11 candlestick",       lambda: ex11_candlestick(ohlc),           _problems_ex11, None),
        ("Ex 12 interactive TVL",   lambda: ex12_interactive_tvl(tvl),        _problems_ex12, None),
        ("Challenge dashboard",     lambda: challenge_dashboard(ohlc, trades, alloc), _problems_challenge, None),
    ]
    results = [check(lbl, b, pf, d, saved) for lbl, b, pf, d in plan]

    print("-" * 50)
    print(f"{sum(results)}/{len(results)} correct")
    if saved:
        print("Charts written to charts/ (open them and look!)")
    print("\nNext steps:")
    print("  • python3 exercises.py --save   to see your charts")
    print("  • Compare with exercises_solutions.py ONLY after attempting everything")
    print("  • Commit: git add . && git commit -m 'phase-2/week-09: my exercise attempts' && git push")
