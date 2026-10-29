"""
pipeline.py
Python for Blockchain Analytics — Phase 2, Week 10

A small, re-runnable ETL pipeline: APIs -> clean DataFrames -> SQLite.

    python3 pipeline.py                  # OFFLINE: uses fixtures (default, always works)
    python3 pipeline.py --live           # LIVE: real APIs (needs ETHERSCAN_API_KEY; COINGECKO_DEMO_API_KEY recommended)
    python3 pipeline.py --db chainlens.db --days 90

Properties that make it production-shaped:
    idempotent    run it twice, get the same database
    incremental   only fetches days newer than what is already stored
    observable    logs what it did; records each load in etl_runs
    checkable     quality_checks() reports problems instead of hiding them
"""
import argparse
import datetime as dt
import logging
import sys

from api_clients import (CoinGeckoClient, DefiLlamaClient, EtherscanClient, RateLimiter,
                         make_live_session, tx_dataframe)
from db_tools import (connect, init_db, latest_date, log_run, table_counts, upsert_prices,
                      upsert_protocol_tvl, upsert_protocols, upsert_transactions)
from fixtures import TX_ADDRESS, FixtureSession

log = logging.getLogger("pipeline")

DEFAULT_COINS = ["ethereum", "bitcoin"]
DEFAULT_SLUGS = ["lido", "aave-v3"]


def days_to_fetch(last_date, as_of, max_days=90):
    """
    Incremental window. No data yet -> max_days. Otherwise days since the stored
    watermark, plus a 2-day overlap to refresh the most recent (still-changing) rows.
    """
    if last_date is None:
        return max_days
    gap = (dt.date.fromisoformat(as_of) - dt.date.fromisoformat(last_date)).days
    return max(2, min(max_days, gap + 2))


def run_pipeline(conn, session, *, coins=DEFAULT_COINS, slugs=DEFAULT_SLUGS, address=TX_ADDRESS,
                 etherscan_key="demo", days=90, as_of=None, limiter_factory=lambda: RateLimiter(1000)):
    """Run all three loads. Returns {source: rows_loaded}. Failures in one source don't stop the others."""
    as_of = as_of or dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    cg = CoinGeckoClient(session, limiter=limiter_factory())
    dl = DefiLlamaClient(session, limiter=limiter_factory())
    es = EtherscanClient(session, api_key=etherscan_key, limiter=limiter_factory())
    summary = {}

    # 1) prices: incremental per coin
    n = 0
    for coin in coins:
        window = days_to_fetch(latest_date(conn, coin), as_of, max_days=days)
        try:
            n += upsert_prices(conn, cg.market_chart(coin, window))
        except Exception as e:  # noqa: BLE001  (one bad source must not kill the run)
            log.error("prices %s failed: %s", coin, e)
    summary["prices"] = n
    log_run(conn, "coingecko", n)

    # 2) protocols (dimension) then their TVL history (fact; FK requires the dimension first)
    try:
        upsert_protocols(conn, dl.protocols())
        n = sum(upsert_protocol_tvl(conn, dl.protocol_tvl(s)) for s in slugs)
    except Exception as e:  # noqa: BLE001
        log.error("defillama failed: %s", e)
        n = 0
    summary["tvl"] = n
    log_run(conn, "defillama", n)

    # 3) transactions (immutable: INSERT OR IGNORE)
    try:
        n = upsert_transactions(conn, tx_dataframe(list(es.iter_txlist_all(address))))
    except Exception as e:  # noqa: BLE001
        log.error("etherscan failed: %s", e)
        n = 0
    summary["transactions"] = n
    log_run(conn, "etherscan", n)

    log.info("pipeline done: %s | tables: %s", summary, table_counts(conn))
    return summary


def quality_checks(conn, as_of=None, max_staleness_days=2):
    """Return a list of human-readable problems. Empty list = healthy."""
    problems = []
    counts = table_counts(conn)
    for t in ("prices_daily", "protocols", "protocol_tvl", "transactions"):
        if counts[t] == 0:
            problems.append(f"{t} is empty")
    bad = conn.execute("SELECT COUNT(*) FROM prices_daily WHERE price_usd IS NULL OR price_usd <= 0").fetchone()[0]
    if bad:
        problems.append(f"{bad} price rows are null or non-positive")
    orphans = conn.execute("PRAGMA foreign_key_check").fetchall()
    if orphans:
        problems.append(f"{len(orphans)} foreign-key violations")
    if as_of:
        for r in conn.execute("SELECT coin_id, MAX(date) AS d FROM prices_daily GROUP BY coin_id"):
            age = (dt.date.fromisoformat(as_of) - dt.date.fromisoformat(r["d"])).days
            if age > max_staleness_days:
                problems.append(f"{r['coin_id']} prices are {age} days stale")
    return problems


def main(argv=None):
    ap = argparse.ArgumentParser(description="APIs -> SQLite pipeline")
    ap.add_argument("--live", action="store_true", help="use real APIs instead of offline fixtures")
    ap.add_argument("--db", default="chainlens.db")
    ap.add_argument("--days", type=int, default=90)
    ap.add_argument("--address", default=TX_ADDRESS)
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    import os
    session = make_live_session() if args.live else FixtureSession()
    key = os.environ.get("ETHERSCAN_API_KEY", "") if args.live else "demo"
    if args.live and not key:
        log.error("ETHERSCAN_API_KEY is not set; Etherscan will be skipped/fail")
    limiter = (lambda: RateLimiter(0.5)) if args.live else (lambda: RateLimiter(1000))
    as_of = None if args.live else "2026-10-01"

    conn = init_db(connect(args.db))
    summary = run_pipeline(conn, session, etherscan_key=key, days=args.days, address=args.address,
                           as_of=as_of, limiter_factory=limiter)
    issues = quality_checks(conn, as_of=as_of)
    for i in issues:
        log.warning("QUALITY: %s", i)
    print("summary:", summary)
    print("quality:", "OK" if not issues else issues)
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
