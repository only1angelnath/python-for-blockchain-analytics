"""
exercises_solutions.py
Python for Blockchain Analytics — Phase 2, Week 10: APIs & SQL from Python

⚠️  WARNING: Only open this file AFTER you have attempted exercises.py.

Run:  python3 exercises_solutions.py
"""
import datetime as dt

import pandas as pd
import requests

import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "week-08-pandas-numpy"))  # append: local modules win
from sample_data import make_dex_trades                              # noqa: E402
from api_clients import ApiError, request_json                      # noqa: E402
from db_tools import connect, init_db                               # noqa: E402
from fixtures import TX_ADDRESS, FixtureSession, etherscan_txs      # noqa: E402
from pipeline import run_pipeline                                   # noqa: E402

CG = "https://api.coingecko.com/api/v3"


# ── Exercise 1: query parameters ───────────────────────────────────────────────
def ex01_build_url():
    """
    Build (do NOT send) the URL for CoinGecko's /coins/markets with these params,
    in this order: vs_currency=usd, order=market_cap_desc, per_page=5, page=2.
    Return the full URL string. Hint: requests.Request("GET", url, params=...).prepare().url
    """
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 5, "page": 2}
    return requests.Request("GET", f"{CG}/coins/markets", params=params).prepare().url


# ── Exercise 2: first real call ────────────────────────────────────────────────
def ex02_simple_price(session):
    """
    Use request_json to call CoinGecko /simple/price for ethereum and bitcoin in USD.
    Return a plain dict {'ethereum': <usd>, 'bitcoin': <usd>}.
    """
    raw = request_json(session, f"{CG}/simple/price",
                       params={"ids": "ethereum,bitcoin", "vs_currencies": "usd"})
    return {coin: v["usd"] for coin, v in raw.items()}


# ── Exercise 3: epoch seconds vs milliseconds ──────────────────────────────────
def ex03_to_date(ts):
    """
    Convert a unix timestamp to a 'YYYY-MM-DD' UTC string. The timestamp may be in
    SECONDS (DefiLlama, Etherscan) or MILLISECONDS (CoinGecko). Detect which:
    anything above 1e11 is milliseconds.
    """
    seconds = ts / 1000 if ts > 1e11 else ts
    return dt.datetime.fromtimestamp(seconds, tz=dt.timezone.utc).strftime("%Y-%m-%d")


# ── Exercise 4: JSON -> DataFrame ──────────────────────────────────────────────
def ex04_top_protocols(session):
    """
    From DefiLlama GET https://api.llama.fi/protocols return the 5 protocols with the
    highest TVL as a list of (name, tvl_in_billions_rounded_to_1_decimal), biggest first.
    """
    df = pd.DataFrame(request_json(session, "https://api.llama.fi/protocols"))
    top = df.nlargest(5, "tvl")
    return [(n, round(t / 1e9, 1)) for n, t in zip(top["name"], top["tvl"])]


# ── Exercise 5: strings that are really big integers ───────────────────────────
def ex05_total_eth(tx_rows):
    """
    tx_rows is a list of Etherscan transactions: every field is a STRING and 'value' is
    in wei (often above 2**63). Return the total ETH moved as a float rounded to 6 decimals.
    Keep the arithmetic in Python ints until the very last step.
    """
    total_wei = sum(int(r["value"]) for r in tx_rows)
    return round(total_wei / 10**18, 6)


# ── Exercise 6: errors hidden inside HTTP 200 ──────────────────────────────────
def ex06_body_error(session):
    """
    Call the Etherscan V2 balance endpoint with NO api key (apikey=''), using
    request_json directly (not EtherscanClient). The HTTP status is 200 but the call
    failed. Return the failure reason text found in the JSON body ('result' field).
    Params: chainid=1, module=account, action=balance, address=<TX_ADDRESS>, tag=latest, apikey=''
    """
    body = request_json(session, "https://api.etherscan.io/v2/api",
                        params={"chainid": 1, "module": "account", "action": "balance",
                                "address": TX_ADDRESS, "tag": "latest", "apikey": ""})
    return body["result"] if str(body["status"]) == "0" else None


# ── Exercise 7: retries with backoff ───────────────────────────────────────────
def fetch_with_retry(session, url, sleep, retries=4):
    """
    GET url and return (json, attempts_used). Rules:
      * HTTP 429 or >= 500: wait, then retry (up to `retries` retries)
          wait = float(Retry-After header) if present, else 1 * 2**retry_number
          (retry_number counts from 0: first wait is 1s, then 2s, 4s...)
      * any other status >= 400: raise ApiError immediately, no retry
      * call sleep(seconds) to wait (it is injected so tests don't really wait)
    """
    for attempt in range(retries + 1):
        resp = session.get(url)
        if resp.status_code == 429 or resp.status_code >= 500:
            if attempt == retries:
                raise ApiError("gave up", resp.status_code, url, True)
            header = resp.headers.get("Retry-After")
            sleep(float(header) if header is not None else 1.0 * 2 ** attempt)
            continue
        if resp.status_code >= 400:
            raise ApiError(f"client error {resp.status_code}", resp.status_code, url)
        return resp.json(), attempt + 1


# ── Exercise 8: rate limiter ───────────────────────────────────────────────────
class Throttle:
    """
    Allow at most `calls_per_second` calls. wait() must be called before each API call:
      * the first call never waits
      * later calls sleep just long enough that consecutive calls are at least
        1/calls_per_second seconds apart
    `clock()` returns the current time in seconds; `sleep(s)` waits s seconds.
    """

    def __init__(self, calls_per_second, clock, sleep):
        self.interval = 1.0 / calls_per_second
        self.clock, self.sleep, self.last = clock, sleep, None

    def wait(self):
        now = self.clock()
        if self.last is not None:
            remaining = self.interval - (now - self.last)
            if remaining > 0:
                self.sleep(remaining)
                now = self.clock()
        self.last = now


# ── Exercise 9: pagination with a generator ────────────────────────────────────
def iter_coin_ids(session, per_page):
    """
    Generator yielding every coin id from CoinGecko /coins/markets (params: vs_currency=usd,
    order=market_cap_desc, per_page, page). Start at page 1, keep going until a page returns
    FEWER than per_page rows. Do not make an extra call after the last page.
    """
    page = 1
    while True:
        rows = request_json(session, f"{CG}/coins/markets",
                            params={"vs_currency": "usd", "order": "market_cap_desc",
                                    "per_page": per_page, "page": page})
        for r in rows:
            yield r["id"]
        if len(rows) < per_page:
            return
        page += 1


# ── Exercise 10: schema with constraints ───────────────────────────────────────
def ex10_create_swaps(conn):
    """
    Create table swaps: tx_hash TEXT primary key; protocol TEXT not null;
    amount_usd REAL with a CHECK that it is > 0; ts INTEGER not null.
    """
    conn.execute("""CREATE TABLE swaps (
        tx_hash    TEXT PRIMARY KEY,
        protocol   TEXT NOT NULL,
        amount_usd REAL CHECK (amount_usd > 0),
        ts         INTEGER NOT NULL)""")
    conn.commit()


# ── Exercise 11: parameterized query ───────────────────────────────────────────
def ex11_wallet_volume(conn, wallet):
    """
    Table trades(wallet TEXT, amount_usd REAL, ...) exists. Return the SUM of amount_usd for
    `wallet` (0.0 if none). Use a ? placeholder. Never build SQL with an f-string:
    the checker passes a malicious wallet value.
    """
    total = conn.execute("SELECT SUM(amount_usd) FROM trades WHERE wallet = ?", (wallet,)).fetchone()[0]
    return round(total or 0.0, 2)


# ── Exercise 12: GROUP BY in SQL ───────────────────────────────────────────────
def ex12_sql_volume_by_protocol():
    """
    Return a SQL string for table trades(protocol, amount_usd, ...) giving two columns:
    protocol, volume (SUM of amount_usd rounded to 2 decimals), largest volume first.
    """
    return """SELECT protocol, ROUND(SUM(amount_usd), 2) AS volume
              FROM trades GROUP BY protocol ORDER BY volume DESC"""


# ── Exercise 13: window function ───────────────────────────────────────────────
def ex13_sql_daily_return():
    """
    Return a SQL string over prices_daily(coin_id, date, price_usd, ...) for coin_id =
    'ethereum' with columns: date, pct_change = (price / previous day's price - 1) * 100,
    ordered by date. The first row's pct_change is NULL. Use LAG() OVER (ORDER BY date).
    """
    return """SELECT date,
                     (price_usd / LAG(price_usd) OVER (ORDER BY date) - 1) * 100 AS pct_change
              FROM prices_daily WHERE coin_id = 'ethereum' ORDER BY date"""


# ── Exercise 14: idempotent upsert ─────────────────────────────────────────────
def ex14_upsert_holdings(conn, rows):
    """
    Table holdings(wallet TEXT, token TEXT, amount REAL, PRIMARY KEY (wallet, token)) exists.
    rows is a list of (wallet, token, amount) tuples. Insert them; if (wallet, token) already
    exists, UPDATE its amount. Running the function twice must not duplicate rows. Use one
    transaction.
    """
    with conn:
        conn.executemany("""INSERT INTO holdings (wallet, token, amount) VALUES (?, ?, ?)
                            ON CONFLICT(wallet, token) DO UPDATE SET amount = excluded.amount""", rows)


# ── Exercise 15: exact big-number math from TEXT ───────────────────────────────
def ex15_exact_wei(conn):
    """
    transactions.value_wei is TEXT (values can exceed int64). Return the EXACT total over all
    rows as a Python int, in wei. SQL's SUM would overflow (integer overflow error) or, via
    REAL, silently lose the low digits. Sum Python ints instead.
    """
    return sum(int(r[0]) for r in conn.execute("SELECT value_wei FROM transactions"))


# ── Exercise 16: SQL date functions + pandas ───────────────────────────────────
def ex16_daily_tx_counts(conn):
    """
    Return a DataFrame with columns date ('YYYY-MM-DD'), tx_count: transactions per UTC day,
    oldest first, via pandas.read_sql_query. ts is unix seconds. Hint: date(ts, 'unixepoch').
    """
    return pd.read_sql_query("""SELECT date(ts, 'unixepoch') AS date, COUNT(*) AS tx_count
                                FROM transactions GROUP BY 1 ORDER BY 1""", conn)


# ── Challenge: price every transaction in USD ──────────────────────────────────
def challenge_priciest_txs(conn):
    """
    JOIN transactions to prices_daily (coin_id='ethereum') on the transaction's UTC date.
    usd_value = value_wei / 1e18 * price_usd. Return the 3 most valuable successful
    (is_error = 0) transactions as a list of (first 10 chars of hash, usd_value rounded to 2).
    """
    rows = conn.execute("""
        SELECT substr(t.hash, 1, 10), ROUND(CAST(t.value_wei AS REAL) / 1e18 * p.price_usd, 2) AS usd
        FROM transactions t
        JOIN prices_daily p ON p.coin_id = 'ethereum' AND p.date = date(t.ts, 'unixepoch')
        WHERE t.is_error = 0 ORDER BY usd DESC LIMIT 3""").fetchall()
    return [(r[0], r[1]) for r in rows]


# ── Runner ─────────────────────────────────────────────────────────────────────
def build_world():
    """An in-memory DB with everything the exercises need (same one exercises.py uses)."""
    conn = init_db(connect())
    run_pipeline(conn, FixtureSession(), as_of="2026-10-01")
    make_dex_trades().to_sql("trades", conn, index=False)
    conn.execute("CREATE TABLE holdings (wallet TEXT, token TEXT, amount REAL, PRIMARY KEY (wallet, token))")
    return conn


if __name__ == "__main__":
    conn = build_world()
    s = FixtureSession()
    sleeps = []
    flaky = FixtureSession(flaky=[(429, {"Retry-After": "3"}), (503, {})])
    fake_t = [0.0]
    th = Throttle(2, lambda: fake_t[0], lambda x: (sleeps.append(x), fake_t.__setitem__(0, fake_t[0] + x)))
    for _ in range(4):
        th.wait()
    wallet = pd.read_sql_query("SELECT wallet FROM trades GROUP BY wallet ORDER BY SUM(amount_usd) DESC LIMIT 1", conn)["wallet"][0]
    waits = []
    ps = FixtureSession()
    ex14_upsert_holdings(conn, [("w1", "ETH", 1.0), ("w2", "ETH", 2.0)])
    ex14_upsert_holdings(conn, [("w1", "ETH", 5.0), ("w3", "UNI", 7.0)])
    res = {
        "ex01": ex01_build_url(), "ex02": ex02_simple_price(s), "ex03": (ex03_to_date(1790812800), ex03_to_date(1790812800000)),
        "ex04": ex04_top_protocols(s), "ex05": ex05_total_eth(etherscan_txs(TX_ADDRESS)),
        "ex06": ex06_body_error(s), "ex07": (fetch_with_retry(flaky, "https://api.llama.fi/protocols", waits.append)[1], waits),
        "ex08": sleeps, "ex09": (len(list(iter_coin_ids(ps, 5))), len(ps.calls)),
        "ex11": (wallet, ex11_wallet_volume(conn, wallet), ex11_wallet_volume(conn, "x' OR '1'='1")),
        "ex12": conn.execute(ex12_sql_volume_by_protocol()).fetchall(),
        "ex13": [tuple(r) for r in conn.execute(ex13_sql_daily_return()).fetchall()][-1],
        "ex14": [tuple(r) for r in conn.execute("SELECT * FROM holdings ORDER BY wallet, token")],
        "ex15": ex15_exact_wei(conn), "ex16": ex16_daily_tx_counts(conn).head(3).values.tolist(),
        "challenge": challenge_priciest_txs(conn),
    }
    c2 = connect()
    ex10_create_swaps(c2)
    res["ex10"] = [tuple(r)[1:3] + (tuple(r)[5],) for r in c2.execute("PRAGMA table_info(swaps)")]
    for k, v in res.items():
        print(f"{k:<10} {v}")
    print("\nAll solutions ran ✓")
    print("Commit: git add . && git commit -m 'phase-2/week-10: solutions' && git push")
