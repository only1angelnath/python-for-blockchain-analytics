"""
fixtures.py
Python for Blockchain Analytics — Phase 2, Week 10

An OFFLINE stand-in for three real APIs, so every lesson and exercise runs
without internet, API keys, or rate limits, and gives identical numbers on
every machine.

    from fixtures import FixtureSession
    session = FixtureSession()
    session.get("https://api.llama.fi/protocols")        # looks like requests.Session.get

The payloads copy the SHAPES of the real APIs (field names, nesting, string-
typed numbers on Etherscan, errors returned inside HTTP 200 on Etherscan,
429 + Retry-After on rate limits). The NUMBERS are simulated.

Real endpoints mimicked:
    CoinGecko   https://api.coingecko.com/api/v3/{ping, simple/price,
                                                  coins/markets, coins/{id}/market_chart}
    DefiLlama   https://api.llama.fi/{protocols, protocol/{slug}, v2/chains,
                                      v2/historicalChainTvl/{chain}}
    Etherscan   https://api.etherscan.io/v2/api?chainid=1&module=...&action=...

Always confirm against the official docs before trusting a field name in
production code (see RESOURCES.md).
"""
import json
import zlib
from urllib.parse import urlparse

import numpy as np
import requests

END_TS = 1_790_812_800            # 2026-10-01 00:00:00 UTC (fixed so data never changes)
DAY = 86_400

COINS = {   # id: (symbol, name, base price USD, base mcap USD)
    "bitcoin":     ("btc",  "Bitcoin",   98_000.0, 1.9e12),
    "ethereum":    ("eth",  "Ethereum",   3_250.0, 3.9e11),
    "tether":      ("usdt", "Tether",         1.0, 1.4e11),
    "binancecoin": ("bnb",  "BNB",          620.0, 9.0e10),
    "solana":      ("sol",  "Solana",       185.0, 8.7e10),
    "usd-coin":    ("usdc", "USDC",           1.0, 4.5e10),
    "ripple":      ("xrp",  "XRP",            2.4, 1.4e11),
    "dogecoin":    ("doge", "Dogecoin",      0.31, 4.6e10),
    "cardano":     ("ada",  "Cardano",       0.82, 2.9e10),
    "chainlink":   ("link", "Chainlink",    21.5, 1.3e10),
    "uniswap":     ("uni",  "Uniswap",       9.8, 5.9e9),
    "aave":        ("aave", "Aave",        265.0, 4.0e9),
}

PROTOCOLS = [   # slug, name, category, chain, tvl (USD)
    ("lido",         "Lido",         "Liquid Staking", "Ethereum", 28.0e9),
    ("aave-v3",      "Aave V3",      "Lending",        "Ethereum", 14.5e9),
    ("eigenlayer",   "EigenLayer",   "Restaking",      "Ethereum", 12.0e9),
    ("makerdao",     "MakerDAO",     "CDP",            "Ethereum",  7.8e9),
    ("uniswap-v3",   "Uniswap V3",   "Dexs",           "Ethereum",  5.6e9),
    ("curve-dex",    "Curve DEX",    "Dexs",           "Ethereum",  2.4e9),
    ("morpho",       "Morpho",       "Lending",        "Ethereum",  4.1e9),
    ("compound-v3",  "Compound V3",  "Lending",        "Ethereum",  2.1e9),
    ("rocket-pool",  "Rocket Pool",  "Liquid Staking", "Ethereum",  1.9e9),
    ("pendle",       "Pendle",       "Yield",          "Ethereum",  3.3e9),
]

TX_ADDRESS = "0xd8da6bf26964af9d7eed9e03e53415d37aa96045"   # demo address (vitalik.eth)
N_TXS = 250


def _rng(*parts):
    return np.random.default_rng(zlib.crc32("|".join(map(str, parts)).encode()))


# ── Response object ────────────────────────────────────────────────────────────
class FixtureResponse:
    """Just enough of requests.Response for this course."""

    def __init__(self, payload, status_code=200, headers=None, url=""):
        self._payload = payload
        self.status_code = status_code
        self.headers = headers or {}
        self.url = url
        self.reason = {200: "OK", 401: "Unauthorized", 404: "Not Found",
                       429: "Too Many Requests", 503: "Service Unavailable"}.get(status_code, "")

    @property
    def ok(self):
        return self.status_code < 400

    @property
    def text(self):
        return json.dumps(self._payload)

    def json(self):
        if self._payload is None:
            raise ValueError("No JSON object could be decoded")
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} {self.reason} for url: {self.url}", response=self)


# ── Payload builders ───────────────────────────────────────────────────────────
def coingecko_market_chart(coin_id, days, interval=None):
    sym, _, base, mcap = COINS[coin_id]
    hourly = interval != "daily" and 1 < days <= 90
    step = 3600 if hourly else DAY
    n = int(days * DAY / step) + 1
    ts = END_TS - step * np.arange(n - 1, -1, -1)
    vol = 0.012 if hourly else 0.03
    if coin_id in ("tether", "usd-coin"):
        vol = 0.0004
    walk = base * np.cumprod(1 + _rng("cg", coin_id, days).normal(0, vol, n))
    walk = walk / walk[-1] * base
    volume = base * 0 + _rng("vol", coin_id).lognormal(21.5, 0.4, n)
    ms = (ts * 1000).tolist()
    return {
        "prices": [[t, round(float(p), 6)] for t, p in zip(ms, walk)],
        "market_caps": [[t, round(float(p / base * mcap), 2)] for t, p in zip(ms, walk)],
        "total_volumes": [[t, round(float(v), 2)] for t, v in zip(ms, volume)],
    }


def coingecko_markets(per_page, page):
    rows = []
    for rank, (cid, (sym, name, price, mcap)) in enumerate(
            sorted(COINS.items(), key=lambda kv: -kv[1][3]), start=1):
        rows.append({"id": cid, "symbol": sym, "name": name, "current_price": price,
                     "market_cap": mcap, "market_cap_rank": rank,
                     "total_volume": round(mcap * 0.04, 2),
                     "price_change_percentage_24h": round(float(_rng("chg", cid).normal(0, 3)), 4)})
    start = (page - 1) * per_page
    return rows[start:start + per_page]


def llama_protocols():
    out = []
    for i, (slug, name, cat, chain, tvl) in enumerate(PROTOCOLS):
        r = _rng("p", slug)
        out.append({"id": str(100 + i), "name": name, "symbol": name.split()[0][:4].upper(),
                    "category": cat, "chain": chain, "chains": [chain, "Arbitrum", "Base"][: 1 + i % 3],
                    "tvl": tvl, "change_1d": round(float(r.normal(0, 2)), 4),
                    "change_7d": round(float(r.normal(0, 6)), 4), "slug": slug})
    return out


def llama_protocol(slug, days=120):
    meta = next((p for p in PROTOCOLS if p[0] == slug), None)
    if meta is None:
        return None
    _, name, cat, chain, tvl = meta
    walk = tvl * np.cumprod(1 + _rng("tvl", slug).normal(0.0005, 0.018, days))
    walk = walk / walk[-1] * tvl
    series = [{"date": int(END_TS - DAY * (days - 1 - i)), "totalLiquidityUSD": round(float(v), 2)}
              for i, v in enumerate(walk)]
    return {"id": slug, "name": name, "category": cat, "chains": [chain],
            "currentChainTvls": {chain: tvl}, "chainTvls": {chain: {"tvl": series}}, "tvl": series}


def llama_chain_tvl(chain, days=120):
    walk = 62e9 * np.cumprod(1 + _rng("chain", chain).normal(0.0004, 0.012, days))
    return [{"date": int(END_TS - DAY * (days - 1 - i)), "tvl": round(float(v), 2)} for i, v in enumerate(walk)]


def etherscan_txs(address, n=N_TXS):
    """Deterministic fake history for one address. All values are STRINGS, as on Etherscan."""
    r = _rng("tx", address.lower())
    blocks = np.sort(20_000_000 + np.cumsum(r.integers(5, 400, n)))
    ts = (END_TS - 20 * DAY) + (blocks - 20_000_000) * 12     # ends ~12 days before END_TS
    eth_values = np.where(r.random(n) < 0.12, r.uniform(9.5, 40, n), r.uniform(0.001, 2.5, n))
    out = []
    for i in range(n):
        wei = int(round(float(eth_values[i]), 6) * 10**6) * 10**12          # exact integer wei
        gas_price = int(r.integers(8, 90)) * 10**9
        gas_used = int(r.integers(21_000, 250_000))
        out.append({
            "blockNumber": str(int(blocks[i])), "timeStamp": str(int(ts[i])),
            "hash": "0x" + "".join(r.choice(list("0123456789abcdef"), 64)),
            "from": address.lower() if i % 3 else "0x" + "".join(r.choice(list("0123456789abcdef"), 40)),
            "to": "0x" + "".join(r.choice(list("0123456789abcdef"), 40)),
            "value": str(wei), "gas": str(gas_used + 5000), "gasPrice": str(gas_price),
            "gasUsed": str(gas_used), "isError": "1" if r.random() < 0.04 else "0",
            "functionName": "" if r.random() < 0.5 else "swapExactTokensForTokens(...)",
        })
    return out


# ── The fake session ───────────────────────────────────────────────────────────
class FixtureSession:
    """
    Drop-in replacement for requests.Session in this course.

    FixtureSession(flaky=[(429, {"Retry-After": "3"}), (503, {})])
        -> the first two calls fail with those statuses, then it behaves normally.
    .calls  -> list of (url, params) so you can assert on what your code sent.
    """

    def __init__(self, flaky=None):
        self.flaky = list(flaky or [])
        self.calls = []
        self.headers = {}

    def get(self, url, params=None, headers=None, timeout=None, **_):
        params = dict(params or {})
        self.calls.append((url, params))
        if self.flaky:
            status, hdrs = self.flaky.pop(0)
            return FixtureResponse({"error": "temporary"}, status, hdrs, url)
        return self._route(url, params, {**self.headers, **(headers or {})})

    def _route(self, url, params, headers):
        u = urlparse(url)
        host, path = u.netloc, u.path.rstrip("/")
        if host == "api.coingecko.com":
            return self._coingecko(url, path, params, headers)
        if host == "api.llama.fi":
            return self._llama(url, path)
        if host == "api.etherscan.io":
            return self._etherscan(url, path, params)
        return FixtureResponse({"error": "unknown host (offline fixtures)"}, 404, {}, url)

    def _coingecko(self, url, path, p, headers):
        if headers.get("x-cg-demo-api-key") == "bad":
            return FixtureResponse({"status": {"error_code": 10002, "error_message": "API Key Missing"}}, 401, {}, url)
        path = path.replace("/api/v3", "")
        if path == "/ping":
            return FixtureResponse({"gecko_says": "(V3) To the Moon!"}, 200, {}, url)
        if path == "/simple/price":
            out = {}
            for cid in str(p.get("ids", "")).split(","):
                if cid in COINS:
                    out[cid] = {"usd": COINS[cid][2]}
                    if p.get("include_24hr_change") in (True, "true"):
                        out[cid]["usd_24h_change"] = round(float(_rng("chg", cid).normal(0, 3)), 4)
            return FixtureResponse(out, 200, {}, url)
        if path == "/coins/markets":
            return FixtureResponse(coingecko_markets(int(p.get("per_page", 100)), int(p.get("page", 1))), 200, {}, url)
        if path.startswith("/coins/") and path.endswith("/market_chart"):
            cid = path.split("/")[2]
            if cid not in COINS:
                return FixtureResponse({"error": "coin not found"}, 404, {}, url)
            return FixtureResponse(coingecko_market_chart(cid, float(p.get("days", 1)), p.get("interval")), 200, {}, url)
        return FixtureResponse({"error": "not found"}, 404, {}, url)

    def _llama(self, url, path):
        if path == "/protocols":
            return FixtureResponse(llama_protocols(), 200, {}, url)
        if path.startswith("/protocol/"):
            data = llama_protocol(path.split("/")[2])
            return FixtureResponse(data, 200, {}, url) if data else FixtureResponse(None, 400, {}, url)
        if path == "/v2/chains":
            return FixtureResponse([{"name": "Ethereum", "tvl": 62e9, "chainId": 1, "tokenSymbol": "ETH"},
                                    {"name": "Arbitrum", "tvl": 3.1e9, "chainId": 42161, "tokenSymbol": "ARB"},
                                    {"name": "Base", "tvl": 4.4e9, "chainId": 8453, "tokenSymbol": None}], 200, {}, url)
        if path.startswith("/v2/historicalChainTvl/"):
            return FixtureResponse(llama_chain_tvl(path.split("/")[3]), 200, {}, url)
        return FixtureResponse({"error": "not found"}, 404, {}, url)

    def _etherscan(self, url, path, p):
        # NOTE: Etherscan reports most errors with HTTP 200 and status "0" in the BODY.
        def body(status, message, result):
            return FixtureResponse({"status": status, "message": message, "result": result}, 200, {}, url)

        if path != "/v2/api":
            return FixtureResponse({"error": "V1 endpoint removed. Use /v2/api"}, 404, {}, url)
        if not p.get("apikey") or p.get("apikey") == "bad":
            return body("0", "NOTOK", "Missing/Invalid API Key")
        if not p.get("chainid"):
            return body("0", "NOTOK", "Missing chainid parameter")
        module, action = p.get("module"), p.get("action")
        if module == "account" and action == "balance":
            return body("1", "OK", str(1234_500_000_000_000_000_000))
        if module == "gastracker" and action == "gasoracle":
            return body("1", "OK", {"LastBlock": "20123456", "SafeGasPrice": "12", "ProposeGasPrice": "13",
                                    "FastGasPrice": "15", "suggestBaseFee": "11.4", "gasUsedRatio": "0.52,0.48,0.61"})
        if module == "account" and action == "txlist":
            page, offset = int(p.get("page", 1)), int(p.get("offset", 10000))
            if page * offset > 10_000:
                return body("0", "Result window is too large, PageNo x Offset size must be less than or equal to 10000", None)
            txs = etherscan_txs(str(p.get("address", "")))
            lo, hi = int(p.get("startblock", 0)), int(p.get("endblock", 99_999_999))
            txs = [t for t in txs if lo <= int(t["blockNumber"]) <= hi]
            if p.get("sort", "asc") == "desc":
                txs = txs[::-1]
            rows = txs[(page - 1) * offset: page * offset]
            return body("1", "OK", rows) if rows else body("0", "No transactions found", [])
        return body("0", "NOTOK", "Error! Missing or invalid Action name")


if __name__ == "__main__":
    s = FixtureSession()
    print("coingecko ping :", s.get("https://api.coingecko.com/api/v3/ping").json())
    print("llama protocols:", len(s.get("https://api.llama.fi/protocols").json()))
    r = s.get("https://api.etherscan.io/v2/api", params={"chainid": 1, "module": "account", "action": "txlist",
                                                           "address": TX_ADDRESS, "apikey": "k", "offset": 5})
    print("etherscan      :", r.status_code, r.json()["message"], len(r.json()["result"]), "txs")
