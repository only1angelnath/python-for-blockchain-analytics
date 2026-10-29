"""
db_tools.py
Python for Blockchain Analytics — Phase 2, Week 10

The local analytics database ("mini data warehouse") layer:
    connect()   open SQLite safely (row access by name, foreign keys ON)
    init_db()   create the schema (safe to run repeatedly)
    upsert_*()  load data idempotently: running twice never duplicates rows

Why these choices (details in lesson_expanded.ipynb):
  * Dates are stored as 'YYYY-MM-DD' TEXT and timestamps as INTEGER unix seconds.
    SQLite has no date type, and Python 3.12 deprecated its automatic datetime adapters.
  * Wei values are stored as TEXT. SQLite INTEGER is 64-bit (max ~9.22 ETH of wei), and
    SQLite silently converts bigger numbers to lossy floats.
  * Every load is an UPSERT keyed on the natural primary key, so pipelines are re-runnable.
"""
import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS prices_daily (
    coin_id    TEXT    NOT NULL,
    date       TEXT    NOT NULL,                 -- 'YYYY-MM-DD' (UTC)
    price_usd  REAL    NOT NULL CHECK (price_usd >= 0),
    volume_usd REAL,
    mcap_usd   REAL,
    PRIMARY KEY (coin_id, date)
);

CREATE TABLE IF NOT EXISTS protocols (
    slug      TEXT PRIMARY KEY,
    name      TEXT NOT NULL,
    category  TEXT,
    chain     TEXT,
    tvl_usd   REAL
);

CREATE TABLE IF NOT EXISTS protocol_tvl (
    slug     TEXT NOT NULL REFERENCES protocols(slug),
    date     TEXT NOT NULL,
    tvl_usd  REAL NOT NULL,
    PRIMARY KEY (slug, date)
);

CREATE TABLE IF NOT EXISTS transactions (
    hash           TEXT PRIMARY KEY,
    block_number   INTEGER NOT NULL,
    ts             INTEGER NOT NULL,             -- unix seconds
    from_addr      TEXT NOT NULL,
    to_addr        TEXT,
    value_wei      TEXT NOT NULL,                -- TEXT on purpose: may exceed int64
    gas_used       INTEGER,
    gas_price_wei  TEXT,
    is_error       INTEGER NOT NULL DEFAULT 0 CHECK (is_error IN (0, 1))
);

CREATE INDEX IF NOT EXISTS idx_tx_from_ts ON transactions(from_addr, ts);

CREATE TABLE IF NOT EXISTS etl_runs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    source      TEXT NOT NULL,
    finished_at TEXT NOT NULL DEFAULT (datetime('now')),
    rows_loaded INTEGER NOT NULL
);
"""


def connect(path=":memory:"):
    """Open a connection: rows behave like dicts, and foreign keys are enforced (SQLite ships with them OFF)."""
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn):
    conn.executescript(SCHEMA)
    conn.commit()
    return conn


def _upsert(conn, sql, rows):
    """Run an executemany upsert inside ONE transaction (all rows or none). Returns rows attempted."""
    rows = list(rows)
    with conn:                                   # commits on success, rolls back on exception
        conn.executemany(sql, rows)
    return len(rows)


def upsert_prices(conn, df):
    sql = """INSERT INTO prices_daily (coin_id, date, price_usd, volume_usd, mcap_usd)
             VALUES (?, ?, ?, ?, ?)
             ON CONFLICT(coin_id, date) DO UPDATE SET
                 price_usd = excluded.price_usd, volume_usd = excluded.volume_usd,
                 mcap_usd = excluded.mcap_usd"""
    daily = df.drop_duplicates(["coin_id", "date"], keep="last")        # one row per day (last obs wins)
    rows = daily[["coin_id", "date", "price_usd", "volume_usd", "market_cap_usd"]].itertuples(index=False, name=None)
    return _upsert(conn, sql, rows)


def upsert_protocols(conn, df):
    sql = """INSERT INTO protocols (slug, name, category, chain, tvl_usd) VALUES (?, ?, ?, ?, ?)
             ON CONFLICT(slug) DO UPDATE SET name = excluded.name, category = excluded.category,
                 chain = excluded.chain, tvl_usd = excluded.tvl_usd"""
    return _upsert(conn, sql, df[["slug", "name", "category", "chain", "tvl"]].itertuples(index=False, name=None))


def upsert_protocol_tvl(conn, df):
    sql = """INSERT INTO protocol_tvl (slug, date, tvl_usd) VALUES (?, ?, ?)
             ON CONFLICT(slug, date) DO UPDATE SET tvl_usd = excluded.tvl_usd"""
    return _upsert(conn, sql, df[["slug", "date", "tvl_usd"]].itertuples(index=False, name=None))


def upsert_transactions(conn, df):
    sql = """INSERT OR IGNORE INTO transactions
             (hash, block_number, ts, from_addr, to_addr, value_wei, gas_used, gas_price_wei, is_error)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""            # transactions are immutable: ignore repeats
    cols = ["hash", "block_number", "ts", "from_addr", "to_addr", "value_wei", "gas_used", "gas_price_wei", "is_error"]
    return _upsert(conn, sql, df[cols].itertuples(index=False, name=None))


def log_run(conn, source, rows_loaded):
    with conn:
        conn.execute("INSERT INTO etl_runs (source, rows_loaded) VALUES (?, ?)", (source, rows_loaded))


def latest_date(conn, coin_id):
    """Watermark for incremental loads: the newest date already stored, or None."""
    return conn.execute("SELECT MAX(date) FROM prices_daily WHERE coin_id = ?", (coin_id,)).fetchone()[0]


def table_counts(conn):
    names = ["prices_daily", "protocols", "protocol_tvl", "transactions", "etl_runs"]
    return {n: conn.execute(f"SELECT COUNT(*) FROM {n}").fetchone()[0] for n in names}   # names are constants, not user input
