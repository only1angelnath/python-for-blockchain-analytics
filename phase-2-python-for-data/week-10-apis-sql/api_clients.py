"""
api_clients.py
Python for Blockchain Analytics — Phase 2, Week 10

Reusable, resilient clients for the three free data sources in this course:
    CoinGecko  (prices)     DefiLlama (TVL)     Etherscan V2 (transactions)

Design rules (each one is explained in the lessons):
  1. Every client takes a `session`. Pass requests.Session() for LIVE data or
     fixtures.FixtureSession() for OFFLINE data. Same code either way.
  2. All HTTP goes through request_json(): timeouts, retries with backoff,
     Retry-After support, and clean errors.
  3. Secrets come from environment variables, never from source code.
  4. Pagination is a generator (yield), so callers never hold more than needed.

    from api_clients import CoinGeckoClient, DefiLlamaClient, EtherscanClient, make_live_session
"""
import os
import time

import pandas as pd
import requests

# ── Errors ─────────────────────────────────────────────────────────────────────


class ApiError(Exception):
    """An API call failed. `retryable` says whether trying again could help."""

    def __init__(self, message, status=None, url=None, retryable=False):
        super().__init__(message)
        self.status, self.url, self.retryable = status, url, retryable


class RateLimitError(ApiError):
    """HTTP 429 or an in-body 'rate limit' message."""

    def __init__(self, message, status=429, url=None, retry_after=None):
        super().__init__(message, status, url, retryable=True)
        self.retry_after = retry_after


# ── HTTP core ──────────────────────────────────────────────────────────────────
def make_live_session(user_agent="python-for-blockchain-analytics/week-10"):
    """A real requests.Session for LIVE calls. Reuses TCP connections (faster) and sets a User-Agent."""
    s = requests.Session()
    s.headers.update({"User-Agent": user_agent, "Accept": "application/json"})
    return s


def _retry_after_seconds(resp):
    """Parse a numeric Retry-After header. Returns None if absent or an HTTP-date (rare)."""
    raw = resp.headers.get("Retry-After") if resp.headers else None
    try:
        return float(raw) if raw is not None else None
    except ValueError:
        return None


def request_json(session, url, *, params=None, headers=None, timeout=15,
                 retries=4, backoff=1.0, sleep=time.sleep):
    """
    GET a URL and return parsed JSON, retrying transient failures.

    Retry:     timeouts, connection errors, HTTP 429, HTTP 5xx
    Fail fast: other 4xx (your request is wrong; retrying cannot fix it)
    Wait:      Retry-After header if present, else backoff * 2**attempt (1s, 2s, 4s...)

    `sleep` is injectable so tests (and exercises) don't actually wait.
    """
    last = None
    for attempt in range(retries + 1):
        try:
            resp = session.get(url, params=params, headers=headers, timeout=timeout)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            last = ApiError(f"network error: {type(e).__name__}", url=url, retryable=True)
        else:
            if resp.status_code == 429 or resp.status_code >= 500:
                wait = _retry_after_seconds(resp)
                last = (RateLimitError("rate limited (429)", url=url, retry_after=wait)
                        if resp.status_code == 429
                        else ApiError(f"server error {resp.status_code}", resp.status_code, url, True))
                if attempt < retries:
                    sleep(wait if wait is not None else backoff * 2 ** attempt)
                continue
            if resp.status_code >= 400:
                raise ApiError(f"client error {resp.status_code}", resp.status_code, url, retryable=False)
            try:
                return resp.json()
            except ValueError as e:
                raise ApiError("response was not valid JSON", resp.status_code, url) from e
        if attempt < retries:
            sleep(backoff * 2 ** attempt)
    raise last


class RateLimiter:
    """
    Keep calls at or below `calls_per_second` by sleeping BEFORE each call.
    clock and sleep are injectable for tests.
    """

    def __init__(self, calls_per_second, clock=time.monotonic, sleep=time.sleep):
        self.min_interval = 1.0 / calls_per_second
        self.clock, self.sleep = clock, sleep
        self._last = None

    def wait(self):
        now = self.clock()
        if self._last is not None:
            gap = self.min_interval - (now - self._last)
            if gap > 0:
                self.sleep(gap)
                now = self.clock()
        self._last = now


# ── CoinGecko ──────────────────────────────────────────────────────────────────
class CoinGeckoClient:
    """
    Prices. Uses the free Demo plan when COINGECKO_DEMO_API_KEY is set
    (sent in the `x-cg-demo-api-key` header, the documented recommended method).
    Without a key it still tries the keyless public API, which is heavily throttled.
    """
    BASE = "https://api.coingecko.com/api/v3"

    def __init__(self, session, api_key=None, limiter=None, **req_kw):
        self.session = session
        self.api_key = api_key or os.environ.get("COINGECKO_DEMO_API_KEY")
        self.limiter = limiter or RateLimiter(0.5)            # conservative: 1 call / 2 s keyless
        self.req_kw = req_kw

    def _get(self, path, **params):
        self.limiter.wait()
        headers = {"x-cg-demo-api-key": self.api_key} if self.api_key else None
        return request_json(self.session, f"{self.BASE}{path}", params=params, headers=headers, **self.req_kw)

    def ping(self):
        return self._get("/ping")

    def simple_price(self, ids, vs="usd"):
        """{'ethereum': {'usd': 3250.0}} for one or many coin ids."""
        return self._get("/simple/price", ids=",".join(ids), vs_currencies=vs)

    def market_chart(self, coin_id, days=30, vs="usd", interval="daily"):
        """Price, market cap and volume history as a tidy DataFrame (one row per timestamp, UTC)."""
        raw = self._get(f"/coins/{coin_id}/market_chart", vs_currency=vs, days=days, interval=interval)
        df = pd.DataFrame(raw["prices"], columns=["ts_ms", "price_usd"])
        df["market_cap_usd"] = [x[1] for x in raw["market_caps"]]
        df["volume_usd"] = [x[1] for x in raw["total_volumes"]]
        df["ts"] = pd.to_datetime(df["ts_ms"], unit="ms", utc=True)
        df["date"] = df["ts"].dt.strftime("%Y-%m-%d")
        df.insert(0, "coin_id", coin_id)
        return df.drop(columns="ts_ms")

    def iter_markets(self, per_page=100, max_pages=50):
        """Generator over ALL coins, one page at a time (page-number pagination)."""
        for page in range(1, max_pages + 1):
            rows = self._get("/coins/markets", vs_currency="usd", order="market_cap_desc",
                             per_page=per_page, page=page)
            if not rows:
                return
            yield from rows
            if len(rows) < per_page:
                return


# ── DefiLlama ──────────────────────────────────────────────────────────────────
class DefiLlamaClient:
    """TVL. The free API needs no key."""
    BASE = "https://api.llama.fi"

    def __init__(self, session, limiter=None, **req_kw):
        self.session = session
        self.limiter = limiter or RateLimiter(2)
        self.req_kw = req_kw

    def _get(self, path):
        self.limiter.wait()
        return request_json(self.session, f"{self.BASE}{path}", **self.req_kw)

    def protocols(self):
        """One row per protocol with current TVL."""
        df = pd.DataFrame(self._get("/protocols"))
        return df[["slug", "name", "category", "chain", "tvl", "change_1d", "change_7d"]]

    def protocol_tvl(self, slug):
        """Daily TVL history for one protocol: columns slug, date, tvl_usd."""
        raw = self._get(f"/protocol/{slug}")
        df = pd.DataFrame(raw["tvl"])
        df["date"] = pd.to_datetime(df["date"], unit="s", utc=True).dt.strftime("%Y-%m-%d")
        return df.rename(columns={"totalLiquidityUSD": "tvl_usd"}).assign(slug=slug)[["slug", "date", "tvl_usd"]]

    def chains(self):
        return pd.DataFrame(self._get("/v2/chains"))

    def chain_tvl_history(self, chain="Ethereum"):
        df = pd.DataFrame(self._get(f"/v2/historicalChainTvl/{chain}"))
        df["date"] = pd.to_datetime(df["date"], unit="s", utc=True).dt.strftime("%Y-%m-%d")
        return df.rename(columns={"tvl": "tvl_usd"})


# ── Etherscan V2 ───────────────────────────────────────────────────────────────
class EtherscanClient:
    """
    On-chain data. One free key works across chains via the `chainid` parameter
    (5 calls/second, 100k/day on the free tier per Etherscan's docs).
    Reads ETHERSCAN_API_KEY from the environment if api_key is not given.

    GOTCHA: Etherscan usually answers HTTP 200 even on failure. The truth is in
    the JSON body: {"status": "0", "message": "NOTOK", "result": "<reason>"}.
    """
    BASE = "https://api.etherscan.io/v2/api"

    def __init__(self, session, api_key=None, chain_id=1, limiter=None, **req_kw):
        self.session = session
        self.api_key = api_key if api_key is not None else os.environ.get("ETHERSCAN_API_KEY", "")
        self.chain_id = chain_id
        self.limiter = limiter or RateLimiter(3)              # stay under the 5/s free limit
        self.req_kw = req_kw

    def _call(self, module, action, **params):
        self.limiter.wait()
        query = {"chainid": self.chain_id, "module": module, "action": action,
                 "apikey": self.api_key, **params}
        body = request_json(self.session, self.BASE, params=query, **self.req_kw)
        if str(body.get("status")) == "1":
            return body["result"]
        message, result = str(body.get("message", "")), body.get("result")
        if message == "No transactions found":                # empty is not an error
            return []
        text = f"{message}: {result}"
        if "rate limit" in text.lower():
            raise RateLimitError(text, status=200, url=self.BASE)
        raise ApiError(text, status=200, url=self.BASE)

    def balance_eth(self, address):
        wei = int(self._call("account", "balance", address=address, tag="latest"))   # Python int: exact
        return wei / 10**18

    def gas_oracle(self):
        return self._call("gastracker", "gasoracle")

    def txlist(self, address, page=1, offset=100, startblock=0, endblock=99_999_999, sort="asc"):
        return self._call("account", "txlist", address=address, startblock=startblock,
                          endblock=endblock, page=page, offset=offset, sort=sort)

    def iter_txlist(self, address, page_size=100):
        """Page-number pagination: simple, but Etherscan caps page x offset at 10,000 results."""
        page = 1
        while True:
            rows = self.txlist(address, page=page, offset=page_size)
            yield from rows
            if len(rows) < page_size:
                return
            page += 1

    def iter_txlist_all(self, address, page_size=100):
        """
        Block-cursor pagination: no 10,000 cap. Fetch page 1 starting at the cursor block,
        then move the cursor to the last block seen. Transactions in the boundary block can
        repeat, so de-duplicate by hash.
        """
        cursor, seen = 0, set()
        while True:
            rows = self.txlist(address, page=1, offset=page_size, startblock=cursor)
            fresh = [r for r in rows if r["hash"] not in seen]
            for r in fresh:
                seen.add(r["hash"])
                yield r
            if len(rows) < page_size or not fresh:
                return
            cursor = int(rows[-1]["blockNumber"])


def tx_dataframe(rows):
    """Etherscan rows (all strings) -> typed DataFrame. value_wei/gas_price_wei stay TEXT: they can exceed int64."""
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    out = pd.DataFrame({
        "hash": df["hash"], "block_number": df["blockNumber"].astype("int64"),
        "ts": df["timeStamp"].astype("int64"),
        "from_addr": df["from"], "to_addr": df["to"],
        "value_wei": df["value"], "gas_used": df["gasUsed"].astype("int64"),
        "gas_price_wei": df["gasPrice"], "is_error": df["isError"].astype("int64"),
    })
    return out
