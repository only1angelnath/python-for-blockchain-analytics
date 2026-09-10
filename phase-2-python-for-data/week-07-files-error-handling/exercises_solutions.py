"""
Week 7 SOLUTIONS — File Handling & Error Handling
Python for Blockchain Analytics | Phase 2

Only open this after attempting exercises.py yourself.
"""

import csv, json, os, logging, time
from collections import defaultdict

print("=" * 60)
print("WEEK 7 SOLUTIONS — File Handling & Error Handling")
print("=" * 60)


# ── SOLUTION 1 — Write and read a DEX trade CSV ───────────────
print("\n── Solution 1: DEX trade CSV ──")

trades = [
    {"tx_hash":"0xaaa","protocol":"Uniswap V3","token_in":"USDC","amount_in":1000.0,"token_out":"ETH","amount_out":0.3082,"gas_gwei":20,"block":19_847_293},
    {"tx_hash":"0xbbb","protocol":"Curve",     "token_in":"DAI", "amount_in":5000.0,"token_out":"USDC","amount_out":4997.5,"gas_gwei":22,"block":19_847_294},
    {"tx_hash":"0xccc","protocol":"Uniswap V3","token_in":"ETH", "amount_in":2.5,  "token_out":"USDC","amount_out":8119.0,"gas_gwei":19,"block":19_847_295},
    {"tx_hash":"0xddd","protocol":"Balancer",  "token_in":"USDC","amount_in":2000.0,"token_out":"UNI", "amount_out":155.76,"gas_gwei":25,"block":19_847_296},
    {"tx_hash":"0xeee","protocol":"Curve",     "token_in":"USDC","amount_in":10000.0,"token_out":"USDT","amount_out":9998.0,"gas_gwei":18,"block":19_847_297},
    {"tx_hash":"0xfff","protocol":"Uniswap V3","token_in":"UNI", "amount_in":100,  "token_out":"ETH", "amount_out":0.3952,"gas_gwei":21,"block":19_847_298},
]

# Part A — Write
fieldnames = ["tx_hash","protocol","token_in","amount_in","token_out","amount_out","gas_gwei","block"]
with open("dex_trades.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(trades)
print(f"  Written {len(trades)} trades to dex_trades.csv")

# Part B — Read and analyse
with open("dex_trades.csv", newline="") as f:
    rows = list(csv.DictReader(f))

total_trades = len(rows)

protocol_counts = defaultdict(int)
gas_prices      = []
largest_out     = None

for row in rows:
    protocol_counts[row["protocol"]] += 1
    gas_prices.append(int(row["gas_gwei"]))
    amount_out = float(row["amount_out"])
    if largest_out is None or amount_out > float(largest_out["amount_out"]):
        largest_out = row

avg_gas = sum(gas_prices) / len(gas_prices)

print(f"  Total trades:   {total_trades}")
print(f"  By protocol:    {dict(protocol_counts)}")
print(f"  Avg gas price:  {avg_gas:.1f} Gwei")
print(f"  Largest output: {largest_out['amount_out']} {largest_out['token_out']} "
      f"(tx: {largest_out['tx_hash']})")


# ── SOLUTION 2 — JSON cache ───────────────────────────────────
print("\n── Solution 2: JSON cache ──")

def save_to_cache(data: dict, filepath: str) -> str:
    """Add timestamp and write data to a JSON cache file."""
    to_save = {**data, "cached_at": int(time.time())}
    with open(filepath, "w") as f:
        json.dump(to_save, f, indent=2)
    return filepath

def load_from_cache(filepath: str, max_age_minutes: int = 60):
    """
    Load a JSON cache file.
    Returns (data, is_fresh) where is_fresh is True if cache is young enough.
    """
    if not os.path.exists(filepath):
        return {}, False
    try:
        with open(filepath) as f:
            raw = json.load(f)
    except json.JSONDecodeError as e:
        print(f"  ⚠️  Malformed cache file {filepath}: {e}")
        return {}, False

    cached_at = raw.pop("cached_at", 0)
    age_seconds = time.time() - cached_at
    is_fresh = age_seconds < (max_age_minutes * 60)
    return raw, is_fresh

protocol_data = {
    "name": "Aave V3",
    "chain": "ethereum",
    "tvl_usd": 12_800_000_000,
    "borrowed_usd": 8_200_000_000,
    "users_24h": 8_200,
}

path = save_to_cache(protocol_data, "protocol_cache.json")
print(f"  Saved to {path}")

data, fresh = load_from_cache("protocol_cache.json", max_age_minutes=60)
print(f"  Cache fresh: {fresh}")
print(f"  TVL loaded:  ${data.get('tvl_usd', 0)/1e9:.2f}B")


# ── SOLUTION 3 — Robust transaction parser ────────────────────
print("\n── Solution 3: Robust transaction parser ──")

def parse_transaction(raw: dict, row_num: int = 0):
    """
    Parse a raw Etherscan transaction dict into clean Python types.
    Returns a clean dict or None on any error.
    """
    try:
        return {
            "hash":           raw["hash"],
            "from_addr":      raw["from"],
            "to_addr":        raw["to"],
            "value_eth":      int(raw["value"]) / 1e18,
            "gas_used":       int(raw["gasUsed"]),
            "gas_price_gwei": int(raw["gasPrice"]) / 1e9,
            "block":          int(raw["blockNumber"]),
            "success":        raw["isError"] == "0",
        }
    except KeyError as e:
        print(f"  ⚠️  Row {row_num}: missing field {e}")
        return None
    except ValueError as e:
        print(f"  ⚠️  Row {row_num}: bad value — {e}")
        return None

raw_transactions = [
    {"hash":"0xaaa","from":"0xAlice","to":"0xBob",  "value":"1500000000000000000","gasUsed":"21000","gasPrice":"20000000000","blockNumber":"19847293","isError":"0"},
    {"hash":"0xbbb","from":"0xBob",  "to":"0xCarol","value":"not_a_number",        "gasUsed":"21000","gasPrice":"18000000000","blockNumber":"19847294","isError":"0"},
    {"hash":"0xccc","from":"0xCarol","to":"0xDave",  "value":"500000000000000000", "gasUsed":"21000","gasPrice":"22000000000","blockNumber":"19847295","isError":"1"},
    {"hash":"0xddd","to":"0xEve",                    "value":"250000000000000000", "gasUsed":"21000","gasPrice":"25000000000","blockNumber":"19847296","isError":"0"},
    {"hash":"0xeee","from":"0xDave", "to":"0xAlice", "value":"2000000000000000000","gasUsed":"21000","gasPrice":"19000000000","blockNumber":"19847297","isError":"0"},
]

parsed = [parse_transaction(r, i+1) for i, r in enumerate(raw_transactions)]
successful = [p for p in parsed if p is not None]
total_volume = sum(p["value_eth"] for p in successful)

print(f"  Parsed OK:    {len(successful)} / {len(raw_transactions)}")
print(f"  Total volume: {total_volume:.4f} ETH")


# ── SOLUTION 4 — Custom exceptions ───────────────────────────
print("\n── Solution 4: Custom exceptions ──")

class BlockchainDataError(Exception):
    """Base exception for blockchain data pipeline errors."""
    pass

class InvalidAddressError(BlockchainDataError):
    def __init__(self, address: str, reason: str = ""):
        self.address = address
        msg = f"Invalid address {address!r}"
        if reason: msg += f": {reason}"
        super().__init__(msg)

class StaleDataError(BlockchainDataError):
    def __init__(self, source: str, age_seconds: int, max_age_seconds: int):
        self.source          = source
        self.age_seconds     = age_seconds
        self.max_age_seconds = max_age_seconds
        super().__init__(
            f"Stale data from {source}: {age_seconds}s old "
            f"(max allowed: {max_age_seconds}s)"
        )

class ProtocolNotFoundError(BlockchainDataError):
    def __init__(self, protocol_name: str, available: list):
        self.protocol_name = protocol_name
        self.available     = available
        super().__init__(
            f"Protocol {protocol_name!r} not found. "
            f"Available: {', '.join(available)}"
        )

SUPPORTED_PROTOCOLS = ["uniswap-v3", "aave-v3", "curve", "balancer", "gmx"]

def validate_pipeline_input(address: str, data_age_seconds: int, protocol: str):
    """Validate all pipeline inputs, raising specific errors for each failure."""
    if not address.startswith("0x") or len(address) != 42:
        raise InvalidAddressError(address,
              f"must start with 0x and be 42 chars, got {len(address)}")
    if data_age_seconds > 3600:
        raise StaleDataError("cache", data_age_seconds, 3600)
    if protocol not in SUPPORTED_PROTOCOLS:
        raise ProtocolNotFoundError(protocol, SUPPORTED_PROTOCOLS)
    return True

test_cases = [
    ("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", 300,  "uniswap-v3"),
    ("0xshort",                                     300,  "uniswap-v3"),
    ("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", 7200, "aave-v3"),
    ("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", 300,  "dydx"),
]

for addr, age, proto in test_cases:
    try:
        validate_pipeline_input(addr, age, proto)
        print(f"  ✅ Valid: addr={addr[:10]}... age={age}s proto={proto}")
    except BlockchainDataError as e:
        print(f"  ❌ {type(e).__name__}: {e}")


# ── SOLUTION 5 — Logging pipeline ────────────────────────────
print("\n── Solution 5: Logging pipeline ──")

handler_c = logging.StreamHandler()
handler_c.setFormatter(logging.Formatter("%(levelname)-8s | %(message)s"))
handler_f = logging.FileHandler("pipeline.log")
handler_f.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s"))

log = logging.getLogger("week7.pipeline")
log.setLevel(logging.DEBUG)
log.addHandler(handler_c)
log.addHandler(handler_f)
log.propagate = False

sample_blocks = [
    {"number": 19_847_000, "transactions": [
        {"hash": "0xaaa", "value": 1.5},
        {"hash": "0xbbb", "value": 0.3},
    ]},
    {"number": 19_847_001, "transactions": []},
    {"number": 19_847_002, "transactions": [
        {"hash": "0xccc", "value": None},
        {"hash": "0xddd", "value": 5.0},
    ]},
    {"number": 19_847_003, "transactions": [
        {"hash": "0xeee", "value": 12.0},
    ]},
]

log.info(f"Starting pipeline — {len(sample_blocks)} blocks to process")
total_value = 0.0
total_txns  = 0
skipped     = 0

for block in sample_blocks:
    if not block["transactions"]:
        log.debug(f"Block {block['number']:,} is empty — skipping")
        continue

    log.debug(f"Processing block {block['number']:,} with {len(block['transactions'])} txns")

    for tx in block["transactions"]:
        if tx["value"] is None:
            log.warning(f"Block {block['number']:,} | tx {tx['hash']} has no value — skipping")
            skipped += 1
            continue
        total_value += tx["value"]
        total_txns  += 1
        log.debug(f"  {tx['hash']}: {tx['value']} ETH")

log.info(f"Pipeline complete — {total_txns} txns processed, {skipped} skipped, {total_value:.2f} ETH total")


# ── SOLUTION 6 — API config file builder ─────────────────────
print("\n── Solution 6: API config ──")

DEFAULT_CONFIG = {
    "version": "1.0",
    "apis": {
        "defillama":  {"requires_key": False, "base_url": "https://api.llama.fi"},
        "coingecko":  {"requires_key": False, "base_url": "https://api.coingecko.com/api/v3"},
        "etherscan":  {"requires_key": True,  "key_env_var": "ETHERSCAN_API_KEY",
                       "base_url": "https://api.etherscan.io/api"},
        "thegraph":   {"requires_key": False, "base_url": "https://api.thegraph.com"},
    },
    "rpc_endpoints": {
        "ethereum": ["https://rpc.ankr.com/eth", "https://eth.llamarpc.com",
                     "https://ethereum.publicnode.com"],
        "polygon":  ["https://rpc.ankr.com/polygon", "https://polygon.llamarpc.com"],
        "arbitrum": ["https://rpc.ankr.com/arbitrum", "https://arbitrum.llamarpc.com"],
    }
}

class APIConfig:
    """Manages API configuration stored in a JSON file."""

    def __init__(self, config_path: str = "api_config.json"):
        self.config_path = config_path
        if os.path.exists(config_path):
            with open(config_path) as f:
                self.config = json.load(f)
        else:
            self.config = DEFAULT_CONFIG.copy()
            self.save()

    def get_rpc(self, chain: str = "ethereum") -> str:
        endpoints = self.config["rpc_endpoints"].get(chain, [])
        if not endpoints:
            raise KeyError(f"No RPC endpoints configured for chain: {chain}")
        return endpoints[0]

    def get_api_key(self, api_name: str) -> str:
        api = self.config["apis"].get(api_name, {})
        if not api.get("requires_key", False):
            return ""
        env_var = api.get("key_env_var", "")
        key     = os.environ.get(env_var, "demo")
        if key == "demo":
            print(f"  ⚠️  {api_name}: using 'demo' key — set ${env_var} for full access")
        return key

    def add_rpc(self, chain: str, url: str) -> None:
        self.config["rpc_endpoints"].setdefault(chain, [])
        if url not in self.config["rpc_endpoints"][chain]:
            self.config["rpc_endpoints"][chain].append(url)

    def save(self) -> None:
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=2)

    def summary(self) -> None:
        print(f"\n  API Config v{self.config.get('version', '?')}:")
        print(f"  {'API':<12} {'Key Required':>14}  {'Base URL'}")
        print("  " + "-" * 58)
        for name, info in self.config["apis"].items():
            key_note = "Yes" if info.get("requires_key") else "No"
            url      = info.get("base_url", "")[:40]
            print(f"  {name:<12} {key_note:>14}  {url}")
        print(f"\n  RPC chains: {', '.join(self.config['rpc_endpoints'].keys())}")

config = APIConfig()
config.summary()
print(f"\n  ETH RPC:       {config.get_rpc('ethereum')}")
print(f"  Etherscan key: {config.get_api_key('etherscan')}")
config.add_rpc("base", "https://rpc.ankr.com/base")
config.save()
config2 = APIConfig()
print(f"  Base RPC (reloaded): {config2.get_rpc('base')}")


# ── SOLUTION — Challenge ──────────────────────────────────────
print("\n── Solution — Challenge: Full robust pipeline ──")

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)-8s | %(message)s")
pipe_log = logging.getLogger("week7.challenge")

def process_wallet_csv(input_path: str, output_path: str, log_path: str = "challenge.log"):
    """Full pipeline: validate → parse → enrich → aggregate → export."""
    fh = logging.FileHandler(log_path)
    fh.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s"))
    pipe_log.addHandler(fh)

    pipe_log.info(f"Pipeline started: {input_path}")

    # Step 1 — Read
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    valid_rows = []
    skipped    = 0

    with open(input_path, newline="") as f:
        reader = csv.DictReader(f)
        required = {"wallet", "token", "raw_amount", "decimals", "price_usd"}

        for i, row in enumerate(reader, 2):
            missing = required - set(row.keys())
            if missing:
                pipe_log.error(f"Row {i}: missing columns {missing} — skipping")
                skipped += 1
                continue

            # Step 2 — Validate
            wallet    = row["wallet"].strip()
            token     = row["token"].strip()
            try:
                raw_amt  = int(row["raw_amount"])
                decimals = int(row["decimals"])
                price    = float(row["price_usd"])
            except ValueError as e:
                pipe_log.warning(f"Row {i} ({token}): bad numeric value — {e}")
                skipped += 1
                continue

            if not (wallet.startswith("0x") and len(wallet) == 42):
                pipe_log.warning(f"Row {i}: invalid wallet {wallet!r} — skipping")
                skipped += 1
                continue
            if raw_amt <= 0:
                pipe_log.warning(f"Row {i}: raw_amount must be positive — skipping")
                skipped += 1
                continue
            if not (0 <= decimals <= 18):
                pipe_log.warning(f"Row {i}: decimals {decimals} out of range — skipping")
                skipped += 1
                continue
            if price <= 0:
                pipe_log.warning(f"Row {i}: price_usd must be positive — skipping")
                skipped += 1
                continue

            # Step 3 — Enrich
            amount_human = raw_amt / 10**decimals
            value_usd    = amount_human * price
            valid_rows.append({
                "wallet": wallet, "token": token,
                "amount_human": round(amount_human, 6),
                "value_usd":    round(value_usd, 2),
            })

    pipe_log.info(f"Parsed {len(valid_rows)} valid rows, skipped {skipped}")

    # Step 4 — Aggregate
    wallet_totals = defaultdict(lambda: {"total_usd": 0.0, "tokens": [], "largest": None})
    for row in valid_rows:
        w = row["wallet"]
        wallet_totals[w]["total_usd"] += row["value_usd"]
        wallet_totals[w]["tokens"].append(row["token"])
        if wallet_totals[w]["largest"] is None or row["value_usd"] > wallet_totals[w]["largest"]["value_usd"]:
            wallet_totals[w]["largest"] = {"token": row["token"], "value_usd": row["value_usd"]}

    # Step 5 — Export CSV
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["wallet","token","amount_human","value_usd"])
        writer.writeheader()
        writer.writerows(valid_rows)
    pipe_log.info(f"Enriched CSV written: {output_path}")

    # Step 5b — Export JSON summary
    summary = {
        "generated_at": int(time.time()),
        "total_valid_rows": len(valid_rows),
        "total_skipped":    skipped,
        "wallets": {
            w: {
                "total_value_usd": round(s["total_usd"], 2),
                "token_count":     len(set(s["tokens"])),
                "largest_holding": s["largest"],
            }
            for w, s in sorted(wallet_totals.items(), key=lambda x: -x[1]["total_usd"])
        }
    }
    summary_path = output_path.replace(".csv", "_summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    pipe_log.info(f"JSON summary written: {summary_path}")
    pipe_log.info("Pipeline complete")

    return summary


sample_holdings = [
    "wallet,token,raw_amount,decimals,price_usd",
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045,ETH,3500000000000000000,18,3247.85",
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045,USDC,5000000000,6,1.00",
    "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984,UNI,500000000000000000000,18,12.84",
    "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984,ETH,1000000000000000000,18,3247.85",
    "0xBadAddress,ETH,1000000000000000000,18,3247.85",
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045,AAVE,not_a_number,18,98.50",
    "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D,WBTC,10000000,8,67412.0",
    "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D,ETH,500000000000000000,18,-100",
]
with open("wallet_holdings.csv", "w") as f:
    f.write("\n".join(sample_holdings))

summary = process_wallet_csv("wallet_holdings.csv", "wallet_enriched.csv")

print("\n  Wallet summary:")
for wallet, data in summary["wallets"].items():
    print(f"  {wallet[:14]}... | ${data['total_value_usd']:>12,.2f} | "
          f"{data['token_count']} tokens | "
          f"Largest: {data['largest_holding']['token']} "
          f"(${data['largest_holding']['value_usd']:,.2f})")

print("\n" + "=" * 60)
print("Solutions complete! Phase 2 Week 7 done.")
print("=" * 60)
