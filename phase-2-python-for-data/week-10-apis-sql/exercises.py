"""
exercises.py
Python for Blockchain Analytics — Phase 2, Week 10: APIs & SQL from Python

HOW TO USE
  1. Read the docstring above each function; replace `raise NotImplementedError`
     with your solution. Every exercise has a SQL or Dune parallel noted.
  2. Run:  python3 exercises.py
     ✅ correct   ❌ wrong (with a hint about what)   ⬜ not attempted yet
  3. Everything runs OFFLINE against fixtures.py: no internet, no API keys.
     Your code is written against the same shapes as the real APIs.
  4. Stuck for 20+ minutes? Re-read the matching lesson section, THEN open
     exercises_solutions.py.

Parts:  A (Ex 1-9) HTTP & APIs      B (Ex 10-16) SQLite & SQL      Challenge
"""
import datetime as dt          # noqa: F401  (you will likely need it)
import os
import sys

import pandas as pd            # noqa: F401
import requests                # noqa: F401

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "week-08-pandas-numpy"))  # append: local modules win
from sample_data import make_dex_trades                              # noqa: E402
from api_clients import ApiError, request_json                      # noqa: E402, F401
from db_tools import connect, init_db                               # noqa: E402
from fixtures import TX_ADDRESS, FixtureSession, etherscan_txs      # noqa: E402, F401
from pipeline import run_pipeline                                   # noqa: E402

CG = "https://api.coingecko.com/api/v3"


# ══════════════════════════ PART A: HTTP & APIs ═══════════════════════════════
def ex01_build_url():
    """
    Build (do NOT send) the URL for CoinGecko's /coins/markets with these params,
    in this order: vs_currency=usd, order=market_cap_desc, per_page=5, page=2.
    Return the full URL string.
    Hint: requests.Request("GET", url, params=...).prepare().url
    """
    raise NotImplementedError


def ex02_simple_price(session):
    """
    Use request_json (imported above) to call CoinGecko /simple/price for ethereum
    and bitcoin in USD. Return a plain dict {'ethereum': <usd>, 'bitcoin': <usd>}.
    Hint: params ids="ethereum,bitcoin", vs_currencies="usd". The raw reply is nested.
    """
    raise NotImplementedError


def ex03_to_date(ts):
    """
    Convert a unix timestamp to a 'YYYY-MM-DD' UTC string. The timestamp may be in
    SECONDS (DefiLlama, Etherscan) or MILLISECONDS (CoinGecko). Detect which:
    anything above 1e11 is milliseconds. (Mixing these up is a classic 1000x bug.)
    """
    raise NotImplementedError


def ex04_top_protocols(session):
    """
    From DefiLlama GET https://api.llama.fi/protocols return the 5 protocols with the
    highest TVL as a list of (name, tvl_in_billions_rounded_to_1_decimal), biggest first.
    SQL parallel: SELECT name, tvl FROM protocols ORDER BY tvl DESC LIMIT 5
    """
    raise NotImplementedError


def ex05_total_eth(tx_rows):
    """
    tx_rows is a list of Etherscan transactions: every field is a STRING and 'value' is
    in wei (often above 2**63). Return the total ETH moved as a float rounded to 6 decimals.
    Keep the arithmetic in Python ints until the very last step.
    """
    raise NotImplementedError


def ex06_body_error(session):
    """
    Call the Etherscan V2 balance endpoint with NO api key (apikey=''), using
    request_json directly (not EtherscanClient). HTTP says 200 but the call failed.
    Return the failure reason text found in the JSON body's 'result' field.
    Params: chainid=1, module=account, action=balance, address=TX_ADDRESS, tag=latest, apikey=''
    URL: https://api.etherscan.io/v2/api
    """
    raise NotImplementedError


def fetch_with_retry(session, url, sleep, retries=4):
    """
    GET url (session.get(url)) and return (json, attempts_used). Rules:
      * HTTP 429 or >= 500: wait, then retry (up to `retries` retries; after the last one,
        raise ApiError("gave up", status, url, True))
          wait = float(Retry-After header) if present, else 1 * 2**retry_number
          (retry_number counts from 0: waits would be 1s, 2s, 4s, 8s...)
      * any other status >= 400: raise ApiError immediately, no retry
      * wait by calling sleep(seconds): it is injected so tests don't really wait
    """
    raise NotImplementedError


class Throttle:
    """
    Allow at most `calls_per_second` calls. wait() is called before each API call:
      * the first call never waits
      * later calls sleep just long enough that consecutive calls are at least
        1/calls_per_second seconds apart
    clock() returns the current time in seconds; sleep(s) waits s seconds.
    """

    def __init__(self, calls_per_second, clock, sleep):
        raise NotImplementedError

    def wait(self):
        raise NotImplementedError


def iter_coin_ids(session, per_page):
    """
    GENERATOR yielding every coin id from CoinGecko /coins/markets (params: vs_currency=usd,
    order=market_cap_desc, per_page, page). Start at page 1 and continue until a page returns
    FEWER than per_page rows. Do not make an extra call after the last page.
    SQL parallel: LIMIT/OFFSET paging.
    """
    raise NotImplementedError
    yield  # makes this a generator function; leave this line in place until you write yours


# ══════════════════════════ PART B: SQLite & SQL ══════════════════════════════
def ex10_create_swaps(conn):
    """
    Create table swaps: tx_hash TEXT primary key; protocol TEXT not null;
    amount_usd REAL with a CHECK that it is > 0; ts INTEGER not null.
    """
    raise NotImplementedError


def ex11_wallet_volume(conn, wallet):
    """
    Table trades(wallet TEXT, amount_usd REAL, ...) exists. Return the SUM of amount_usd for
    `wallet`, rounded to 2 decimals (0.0 if none). Use a ? placeholder, never an f-string:
    the checker passes a malicious wallet value.
    """
    raise NotImplementedError


def ex12_sql_volume_by_protocol():
    """
    Return a SQL string for table trades(protocol, amount_usd, ...) giving two columns:
    protocol, volume (SUM of amount_usd rounded to 2 decimals), largest volume first.
    """
    raise NotImplementedError


def ex13_sql_daily_return():
    """
    Return a SQL string over prices_daily(coin_id, date, price_usd, ...) for coin_id =
    'ethereum' with two columns: date, pct_change = (price / previous day's price - 1) * 100,
    ordered by date. The first row's pct_change is NULL.
    Hint: LAG(price_usd) OVER (ORDER BY date)   (Week 8: shift(1) / pct_change())
    """
    raise NotImplementedError


def ex14_upsert_holdings(conn, rows):
    """
    Table holdings(wallet TEXT, token TEXT, amount REAL, PRIMARY KEY (wallet, token)) exists.
    rows is a list of (wallet, token, amount) tuples. Insert them; if (wallet, token) already
    exists, UPDATE its amount. Running the function twice must not duplicate rows.
    Use one transaction. Hint: INSERT ... ON CONFLICT(...) DO UPDATE SET amount = excluded.amount
    """
    raise NotImplementedError


def ex15_exact_wei(conn):
    """
    transactions.value_wei is TEXT (values can exceed int64). Return the EXACT total over all
    rows as a Python int, in wei. SQL's SUM would overflow (integer overflow error) or, via
    REAL, silently lose the low digits. Sum Python ints instead.
    """
    raise NotImplementedError


def ex16_daily_tx_counts(conn):
    """
    Return a DataFrame with columns date ('YYYY-MM-DD'), tx_count: transactions per UTC day,
    oldest first, using pandas.read_sql_query. ts is unix seconds.
    Hint: date(ts, 'unixepoch')  (DuneSQL: date_trunc('day', block_time))
    """
    raise NotImplementedError


def challenge_priciest_txs(conn):
    """
    CHALLENGE. JOIN transactions to prices_daily (coin_id='ethereum') on the transaction's UTC
    date. usd_value = value_wei / 1e18 * price_usd. Return the 3 most valuable SUCCESSFUL
    (is_error = 0) transactions as a list of (first 10 chars of hash, usd_value rounded to 2),
    biggest first. This is "enrich on-chain data with off-chain prices", the core of analytics.
    """
    raise NotImplementedError


# ══════════════════════════════════════════════════════════════════════════════
# CHECKER: you do not need to edit anything below this line
# ══════════════════════════════════════════════════════════════════════════════
def build_world():
    conn = init_db(connect())
    run_pipeline(conn, FixtureSession(), as_of="2026-10-01")
    make_dex_trades().to_sql("trades", conn, index=False)
    conn.execute("CREATE TABLE holdings (wallet TEXT, token TEXT, amount REAL, PRIMARY KEY (wallet, token))")
    return conn


def _eq(got, want, label):
    return [] if got == want else [f"{label}: got {got!r}"]


def c01(w):
    return _eq(ex01_build_url(), "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=5&page=2", "URL")


def c02(w):
    return _eq(ex02_simple_price(FixtureSession()), {"ethereum": 3250.0, "bitcoin": 98000.0}, "prices")


def c03(w):
    return _eq((ex03_to_date(1790812800), ex03_to_date(1790812800000)), ("2026-10-01", "2026-10-01"),
               "seconds and milliseconds should give the same date")


def c04(w):
    return _eq(ex04_top_protocols(FixtureSession()),
               [("Lido", 28.0), ("Aave V3", 14.5), ("EigenLayer", 12.0), ("MakerDAO", 7.8), ("Uniswap V3", 5.6)], "top 5")


def c05(w):
    return _eq(ex05_total_eth(etherscan_txs(TX_ADDRESS)), 1125.254691, "total ETH")


def c06(w):
    return _eq(ex06_body_error(FixtureSession()), "Missing/Invalid API Key", "reason")


def c07(w):
    waits = []
    flaky = FixtureSession(flaky=[(429, {"Retry-After": "3"}), (503, {})])
    data, attempts = fetch_with_retry(flaky, "https://api.llama.fi/protocols", waits.append)
    p = _eq((attempts, waits), (3, [3.0, 2.0]), "attempts and waits (Retry-After first, then 1*2**1)")
    s404 = FixtureSession()
    try:
        fetch_with_retry(s404, "https://api.llama.fi/protocol/does-not-exist", waits.append)
        p.append("a 400/404 must raise ApiError")
    except ApiError:
        if len(s404.calls) != 1:
            p.append("do not retry client errors")
    dead = FixtureSession(flaky=[(503, {})] * 10)
    try:
        fetch_with_retry(dead, "https://api.llama.fi/protocols", lambda s: None)
        p.append("must raise ApiError after the last retry")
    except ApiError:
        if len(dead.calls) != 5:
            p.append(f"expected 1 try + 4 retries = 5 calls, saw {len(dead.calls)}")
    return p


def c08(w):
    t, sleeps = [0.0], []

    def sleep(x):
        sleeps.append(x)
        t[0] += x
    th = Throttle(2, lambda: t[0], sleep)
    for _ in range(4):
        th.wait()
    p = _eq([round(s, 6) for s in sleeps], [0.5, 0.5, 0.5], "sleeps for 4 back-to-back calls at 2/s")
    t2, s2 = [0.0], []
    th2 = Throttle(2, lambda: t2[0], s2.append)
    th2.wait()
    t2[0] += 0.8                      # caller was slow: no waiting needed
    th2.wait()
    return p + ([] if s2 == [] else ["no sleep needed when the gap is already longer than 1/rate"])


def c09(w):
    s = FixtureSession()
    ids = list(iter_coin_ids(s, 5))
    p = _eq(len(ids), 12, "number of coins")
    return p + ([] if len(s.calls) == 3 else [f"expected exactly 3 API calls (5+5+2 rows), saw {len(s.calls)}"])


def c10(w):
    c = connect()
    ex10_create_swaps(c)
    info = {r["name"]: (r["type"].upper(), r["notnull"], r["pk"]) for r in c.execute("PRAGMA table_info(swaps)")}
    p = []
    if info.get("tx_hash", (None, 0, 0))[2] != 1:
        p.append("tx_hash must be the PRIMARY KEY")
    if info.get("protocol", (None, 0, 0))[1] != 1 or info.get("ts", (None, 0, 0))[1] != 1:
        p.append("protocol and ts must be NOT NULL")
    if info.get("amount_usd", ("",))[0] != "REAL" or info.get("ts", ("",))[0] != "INTEGER":
        p.append("types: amount_usd REAL, ts INTEGER")
    try:
        c.execute("INSERT INTO swaps VALUES ('0x1', 'Uniswap', -5, 1)")
        p.append("CHECK (amount_usd > 0) is missing: a negative amount was accepted")
    except Exception:  # noqa: BLE001
        pass
    return p


def c11(w):
    top = "0xc334cfc4bb625d81e850982d8134bcd9e59a57bd"
    p = _eq(ex11_wallet_volume(w, top), 158958.77, "wallet volume")
    evil = ex11_wallet_volume(w, "x' OR '1'='1")
    return p + ([] if evil in (0, 0.0) else ["injection worked: use a ? placeholder"])


def c12(w):
    rows = [tuple(r) for r in w.execute(ex12_sql_volume_by_protocol())]
    return _eq(rows, [("Uniswap", 1561473.47), ("Curve", 563482.96), ("Sushiswap", 535068.05), ("Balancer", 320958.61)], "rows")


def c13(w):
    rows = [tuple(r) for r in w.execute(ex13_sql_daily_return())]
    vals = [r[1] for r in rows if r[1] is not None]
    ok = len(rows) == 91 and rows[0][1] is None and len(vals) == 90 and round(sum(vals) / len(vals), 4) == -0.2812
    return [] if ok else [f"expected 91 rows, first pct_change NULL, mean of the other 90 = -0.2812 (got {len(rows)} rows, mean {round(sum(vals)/max(len(vals),1),4)})"]


def c14(w):
    ex14_upsert_holdings(w, [("w1", "ETH", 1.0), ("w2", "ETH", 2.0)])
    ex14_upsert_holdings(w, [("w1", "ETH", 5.0), ("w3", "UNI", 7.0)])
    ex14_upsert_holdings(w, [("w1", "ETH", 5.0), ("w3", "UNI", 7.0)])      # idempotent re-run
    got = [tuple(r) for r in w.execute("SELECT wallet, token, amount FROM holdings ORDER BY wallet, token")]
    return _eq(got, [("w1", "ETH", 5.0), ("w2", "ETH", 2.0), ("w3", "UNI", 7.0)], "holdings")


def c15(w):
    got = ex15_exact_wei(w)
    p = _eq(got, 1125254691000000000000, "exact total wei")
    return p + (["must be a Python int, not a float"] if isinstance(got, float) else [])


def c16(w):
    df = ex16_daily_tx_counts(w)
    p = []
    if list(df.columns) != ["date", "tx_count"]:
        p.append(f"columns must be ['date', 'tx_count'], got {list(df.columns)}")
        return p
    return p + _eq(df.head(3).values.tolist(), [["2026-09-11", 36], ["2026-09-12", 37], ["2026-09-13", 38]], "first 3 days")


def cch(w):
    return _eq(challenge_priciest_txs(w), [("0xbc5fc4bf", 154378.46), ("0xdecdd704", 148730.6), ("0xa4b79510", 144087.83)], "top 3")


PLAN = [
    ("Ex 1  build URL", c01), ("Ex 2  simple price", c02), ("Ex 3  epoch s vs ms", c03),
    ("Ex 4  JSON -> top 5", c04), ("Ex 5  wei strings -> ETH", c05), ("Ex 6  error inside HTTP 200", c06),
    ("Ex 7  retry + backoff", c07), ("Ex 8  rate limiter", c08), ("Ex 9  pagination generator", c09),
    ("Ex 10 create table", c10), ("Ex 11 safe query", c11), ("Ex 12 GROUP BY in SQL", c12),
    ("Ex 13 LAG window", c13), ("Ex 14 upsert", c14), ("Ex 15 exact wei sum", c15),
    ("Ex 16 read_sql + dates", c16), ("Challenge: price every tx", cch),
]


def main():
    print("Week 10 — APIs & SQL exercises\n" + "-" * 52)
    ok = 0
    for label, fn in PLAN:
        try:
            problems = fn(build_world())
        except NotImplementedError:
            print(f"⬜ {label}: not attempted yet")
            continue
        except Exception as e:  # noqa: BLE001  (a learner's code may raise anything)
            print(f"❌ {label}\n     your code raised {type(e).__name__}: {e}")
            continue
        if problems:
            print(f"❌ {label}")
            for p in problems:
                print(f"     - {p}")
        else:
            print(f"✅ {label}")
            ok += 1
    print("-" * 52)
    print(f"{ok}/{len(PLAN)} correct")
    print("\nNext steps:")
    print("  • Compare with exercises_solutions.py ONLY after attempting everything")
    print("  • Commit: git add . && git commit -m 'phase-2/week-10: my exercise attempts' && git push")


if __name__ == "__main__":
    main()
