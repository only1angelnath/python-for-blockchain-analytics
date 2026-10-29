"""
live_smoke_test.py
Python for Blockchain Analytics — Phase 2, Week 10

Run this BEFORE debugging anything else when you switch to live data:

    python3 live_smoke_test.py            # real APIs (needs internet; keys from environment)
    python3 live_smoke_test.py --offline  # same checks against fixtures (proves the checker itself works)

It checks each source end to end (key present, reachable, response has the shape our
code expects) and prints PASS / FAIL / SKIP with a plain-English hint.
Exit code: 0 = no failures (SKIPs are fine), 1 = at least one FAIL.

Keys are read from the environment only and are NEVER printed:
    ETHERSCAN_API_KEY          (free: etherscan.io/apis)
    COINGECKO_DEMO_API_KEY     (free Demo plan; optional but recommended)

NOTE: written from the providers' public documentation. It could not be run against the
live APIs in the environment where this course was built, so if a check fails, compare the
reported shape with the provider's current docs (see RESOURCES.md): the docs win.
"""
import os
import sys

import requests

from api_clients import (ApiError, CoinGeckoClient, DefiLlamaClient, EtherscanClient,
                         RateLimitError, RateLimiter, make_live_session)
from fixtures import FixtureSession

VITALIK = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"


def hint_for(exc):
    if isinstance(exc, RateLimitError):
        return "rate limited: wait a minute and retry; keyless CoinGecko is heavily throttled, consider a free Demo key"
    if isinstance(exc, ApiError) and exc.status in (401, 403):
        return "key rejected: check the env var is set in THIS shell and the key is active in the provider dashboard"
    if isinstance(exc, ApiError) and exc.status == 404:
        return "endpoint not found: the provider may have changed the URL; check the official docs"
    if isinstance(exc, ApiError) and "Invalid API Key" in str(exc):
        return "Etherscan rejected the key: regenerate it at etherscan.io/apis and re-export ETHERSCAN_API_KEY"
    if isinstance(exc, (requests.exceptions.ConnectionError, requests.exceptions.Timeout)) or \
            (isinstance(exc, ApiError) and "network" in str(exc)):
        return "cannot reach the server: check your internet, VPN or proxy settings"
    return "unexpected: see the message and compare with the provider's docs"


def check(name, fn, results):
    try:
        detail = fn()
        results.append((name, "PASS", detail))
    except Exception as e:  # noqa: BLE001  (a smoke test must report, never crash)
        results.append((name, "FAIL", f"{type(e).__name__}: {e}\n         hint: {hint_for(e)}"))


def main():
    offline = "--offline" in sys.argv
    session = FixtureSession() if offline else make_live_session()
    limiter = (lambda r: RateLimiter(10_000)) if offline else (lambda r: RateLimiter(r))
    cg_key, es_key = os.environ.get("COINGECKO_DEMO_API_KEY"), os.environ.get("ETHERSCAN_API_KEY", "")
    if offline:
        es_key = es_key or "demo"
    print(f"mode: {'OFFLINE fixtures' if offline else 'LIVE'} | "
          f"CoinGecko key: {'set' if cg_key else 'not set (keyless)'} | Etherscan key: {'set' if es_key else 'NOT SET'}\n")

    results = []
    cg = CoinGeckoClient(session, limiter=limiter(0.5), retries=1)
    dl = DefiLlamaClient(session, limiter=limiter(2), retries=1)
    es = EtherscanClient(session, api_key=es_key, limiter=limiter(3), retries=1)

    def cg_price():
        p = cg.simple_price(["ethereum"])["ethereum"]["usd"]
        assert isinstance(p, (int, float)) and p > 0, f"unexpected price {p!r}"
        return f"ETH = ${p:,.2f}"

    def cg_chart():
        df = cg.market_chart("ethereum", days=7)
        assert {"date", "price_usd"} <= set(df.columns) and len(df) >= 7, f"shape {df.shape}"
        return f"{len(df)} daily rows, last date {df['date'].iloc[-1]}"

    def dl_protocols():
        df = dl.protocols()
        assert len(df) > 0 and {"slug", "tvl"} <= set(df.columns)
        top = df.nlargest(1, "tvl").iloc[0]
        return f"{len(df)} protocols; top by TVL: {top['name']} (${top['tvl']/1e9:,.1f}B)"

    def dl_history():
        df = dl.protocol_tvl("lido")
        assert len(df) > 30 and {"date", "tvl_usd"} <= set(df.columns)
        return f"lido: {len(df)} daily TVL points, last {df['date'].iloc[-1]}"

    def es_gas():
        g = es.gas_oracle()
        assert "ProposeGasPrice" in g, f"keys: {list(g)[:5]}"
        return f"propose gas = {g['ProposeGasPrice']} gwei"

    def es_balance():
        b = es.balance_eth(VITALIK)
        assert b >= 0
        return f"balance = {b:,.4f} ETH"

    check("CoinGecko  simple/price", cg_price, results)
    check("CoinGecko  market_chart", cg_chart, results)
    check("DefiLlama  /protocols", dl_protocols, results)
    check("DefiLlama  /protocol/lido", dl_history, results)
    if es_key:
        check("Etherscan  gas oracle", es_gas, results)
        check("Etherscan  balance", es_balance, results)
    else:
        results.append(("Etherscan  (all)", "SKIP", "ETHERSCAN_API_KEY not set. Get a free key at etherscan.io/apis, then: export ETHERSCAN_API_KEY=..."))

    for name, status, detail in results:
        icon = {"PASS": "✅", "FAIL": "❌", "SKIP": "⏭️ "}[status]
        print(f"{icon} {status:<4} {name:<28} {detail}")
    fails = sum(1 for _, s, _ in results if s == "FAIL")
    print(f"\n{sum(s == 'PASS' for _, s, _ in results)} passed, {fails} failed, {sum(s == 'SKIP' for _, s, _ in results)} skipped")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
