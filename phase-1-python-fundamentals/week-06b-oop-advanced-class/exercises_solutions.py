"""
Week 6 SOLUTIONS — Object-Oriented Programming
Python for Blockchain Analytics | Phase 1

Only open this after attempting exercises.py yourself.
"""

import hashlib
import time as time_module
from datetime import datetime

print("=" * 60)
print("WEEK 6 SOLUTIONS — Object-Oriented Programming")
print("=" * 60)


# ── SOLUTION 1 — Block ────────────────────────────────────────
print("\n── Solution 1: The Block class ──")

class Block:
    """Represents a single Ethereum block."""

    def __init__(self, block_number, timestamp, miner,
                 tx_hashes, gas_used, base_fee_gwei, gas_limit=30_000_000):
        self.block_number  = block_number
        self.timestamp     = timestamp
        self.miner         = miner
        self.tx_hashes     = list(tx_hashes)
        self.gas_used      = gas_used
        self.gas_limit     = gas_limit
        self.base_fee_gwei = base_fee_gwei

    def tx_count(self):
        return len(self.tx_hashes)

    def gas_utilisation(self):
        return self.gas_used / self.gas_limit * 100

    def is_full(self):
        return self.gas_utilisation() > 95

    def add_transaction(self, tx_hash):
        self.tx_hashes.append(tx_hash)

    def __repr__(self):
        return (f"Block(number={self.block_number}, "
                f"txns={self.tx_count()}, gas={self.gas_utilisation():.1f}%)")

    def __str__(self):
        return (f"Block {self.block_number:,} | {self.tx_count()} txns | "
                f"{self.gas_utilisation():.1f}% gas | {self.base_fee_gwei} Gwei")

    def __len__(self):
        return self.tx_count()


block = Block(19_847_293, 1_714_000_000,
              "0xeBec795c9c8bBD61FFc14A6662944748F299cAec",
              ["0xaaa", "0xbbb", "0xccc"], 26_174_000, 18.5)
block.add_transaction("0xddd")

print(f"  repr:            {repr(block)}")
print(f"  str:             {block}")
print(f"  tx_count:        {block.tx_count()}")
print(f"  gas_utilisation: {block.gas_utilisation():.2f}%")
print(f"  is_full:         {block.is_full()}")
print(f"  len:             {len(block)}")


# ── SOLUTION 2 — TokenRegistry ────────────────────────────────
print("\n── Solution 2: TokenRegistry class ──")

class TokenRegistry:
    """Shared registry — all instances share the same token database."""

    _registry = {}
    _count    = 0

    def __init__(self, name):
        self.name       = name
        self.created_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    def register(self, symbol, price, decimals=18):
        if symbol in TokenRegistry._registry:
            raise ValueError(f"Token '{symbol}' is already registered")
        TokenRegistry._registry[symbol] = {"price": price, "decimals": decimals}
        TokenRegistry._count += 1

    def get(self, symbol):
        if symbol not in TokenRegistry._registry:
            available = ", ".join(sorted(TokenRegistry._registry.keys()))
            raise KeyError(f"Token '{symbol}' not found. Available: {available}")
        return TokenRegistry._registry[symbol]

    def remove(self, symbol):
        if symbol not in TokenRegistry._registry:
            raise KeyError(f"Token '{symbol}' not found")
        del TokenRegistry._registry[symbol]

    def all_symbols(self):
        return sorted(TokenRegistry._registry.keys())

    @classmethod
    def count(cls):
        return cls._count

    def summary(self):
        print(f"\n  Registry: {self.name}")
        print(f"  {'Symbol':<8} {'Price':>10}  {'Decimals':>10}")
        print("  " + "-" * 32)
        for sym in self.all_symbols():
            d = TokenRegistry._registry[sym]
            print(f"  {sym:<8} ${d['price']:>9,.2f}  {d['decimals']:>10}")


TokenRegistry._registry = {}
TokenRegistry._count    = 0

mainnet = TokenRegistry("Mainnet")
mainnet.register("ETH",  3247.85, 18)
mainnet.register("BTC",  67412.0, 8)
mainnet.register("USDC", 1.00,    6)
mainnet.register("UNI",  12.84,   18)

try:
    mainnet.register("ETH", 3310.0)
except ValueError as e:
    print(f"  ValueError: {e}")

print(f"  Total tokens: {TokenRegistry.count()}")
mainnet.summary()

testnet = TokenRegistry("Testnet")
testnet.register("WETH", 3247.85, 18)
print(f"\n  After testnet, total count: {TokenRegistry.count()}")


# ── SOLUTION 3 — LiquidityPool ────────────────────────────────
print("\n── Solution 3: LiquidityPool with dunders ──")

class LiquidityPool:
    """Uniswap-style constant-product liquidity pool."""

    def __init__(self, token0, token1, reserve0, reserve1, fee_tier):
        self.token0   = token0
        self.token1   = token1
        self.reserve0 = reserve0
        self.reserve1 = reserve1
        self.fee_tier = fee_tier

    @property
    def price(self):
        return self.reserve1 / self.reserve0

    @property
    def pair_name(self):
        return f"{self.token0}/{self.token1}"

    @property
    def fee_pct(self):
        return self.fee_tier / 10_000

    def calculate_tvl(self, price0_usd, price1_usd):
        return self.reserve0 * price0_usd + self.reserve1 * price1_usd

    def _canonical_pair(self):
        return frozenset({self.token0, self.token1})

    def __repr__(self):
        return (f"LiquidityPool({self.pair_name!r}, "
                f"fee={self.fee_pct:.2%}, price={self.price:,.2f})")

    def __str__(self):
        return f"{self.pair_name} | Price: {self.price:,.2f} | Fee: {self.fee_pct:.2%}"

    def __eq__(self, other):
        if not isinstance(other, LiquidityPool): return NotImplemented
        return self._canonical_pair() == other._canonical_pair()

    def __gt__(self, other):
        if not isinstance(other, LiquidityPool): return NotImplemented
        return self.reserve0 > other.reserve0

    def __lt__(self, other):
        if not isinstance(other, LiquidityPool): return NotImplemented
        return self.reserve0 < other.reserve0


pool1 = LiquidityPool("USDC", "ETH",  1_000_000, 308.0, 500)
pool2 = LiquidityPool("USDC", "ETH",    500_000, 154.0, 3000)
pool3 = LiquidityPool("ETH",  "USDC",      308.0, 1_000_000, 500)

print(f"  {pool1}")
print(f"  price:        {pool1.price:,.4f}")
print(f"  pair_name:    {pool1.pair_name}")
print(f"  TVL:          ${pool1.calculate_tvl(1.0, 3247.85):,.2f}")
print(f"  pool1==pool3: {pool1 == pool3}")
print(f"  pool1>pool2:  {pool1 > pool2}")
sorted_pools = sorted([pool2, pool1])
print(f"  sorted:       {[p.pair_name for p in sorted_pools]}")


# ── SOLUTION 4 — Protocol hierarchy ──────────────────────────
print("\n── Solution 4: Protocol inheritance hierarchy ──")

class Protocol:
    def __init__(self, name, chain, tvl_usd):
        self.name    = name
        self.chain   = chain
        self.tvl_usd = tvl_usd

    def tvl_formatted(self):
        if self.tvl_usd >= 1e9: return f"${self.tvl_usd/1e9:.2f}B"
        if self.tvl_usd >= 1e6: return f"${self.tvl_usd/1e6:.2f}M"
        return f"${self.tvl_usd/1e3:.2f}K"

    def info(self):
        return f"{self.name} ({self.chain}) | TVL: {self.tvl_formatted()}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r}, tvl={self.tvl_formatted()})"


class DEX(Protocol):
    def __init__(self, name, chain, tvl_usd, volume_24h, fee_tier):
        super().__init__(name, chain, tvl_usd)
        self.volume_24h = volume_24h
        self.fee_tier   = fee_tier

    @property
    def fees_24h(self):
        return self.volume_24h * self.fee_tier

    @property
    def apr_estimate(self):
        return (self.fees_24h * 365 / self.tvl_usd) * 100

    def is_high_yield(self, threshold=20.0):
        return self.apr_estimate > threshold

    def info(self):
        return (f"{super().info()} | "
                f"Vol: ${self.volume_24h/1e6:.0f}M/d | "
                f"APR: {self.apr_estimate:.1f}%")


class LendingProtocol(Protocol):
    def __init__(self, name, chain, tvl_usd, total_borrowed):
        super().__init__(name, chain, tvl_usd)
        self.total_borrowed = total_borrowed

    @property
    def utilisation(self):
        return self.total_borrowed / self.tvl_usd * 100

    def borrow_apr(self, base_rate=2.0):
        return base_rate * (1 + self.utilisation / 100)

    def info(self):
        return (f"{super().info()} | "
                f"Borrowed: ${self.total_borrowed/1e9:.2f}B | "
                f"Utilisation: {self.utilisation:.1f}%")


uniswap = DEX("Uniswap V3", "ethereum", 5_200_000_000, 1_800_000_000, 0.003)
gmx     = DEX("GMX",        "arbitrum",   680_000_000,   310_000_000, 0.001)
aave    = LendingProtocol("Aave V3", "ethereum", 12_800_000_000, 8_200_000_000)

for p in [uniswap, gmx, aave]:
    print(f"  {p.info()}")

print(f"\n  uniswap isinstance DEX:             {isinstance(uniswap, DEX)}")
print(f"  aave    isinstance LendingProtocol: {isinstance(aave, LendingProtocol)}")
print(f"  aave    isinstance DEX:             {isinstance(aave, DEX)}")
print(f"  Uniswap high yield: {uniswap.is_high_yield()}")
print(f"  Aave borrow APR:    {aave.borrow_apr():.2f}%")
sorted_p = sorted([uniswap, gmx, aave], key=lambda p: p.tvl_usd, reverse=True)
print(f"  Sorted by TVL:      {[p.name for p in sorted_p]}")


# ── SOLUTION 5 — PriceOracle ──────────────────────────────────
print("\n── Solution 5: PriceOracle with @property ──")

class PriceOracle:
    """Tracks a token price and computes derived metrics via properties."""

    def __init__(self, symbol, initial_price, decimals=18):
        self.symbol         = symbol
        self.decimals       = decimals
        self._price         = initial_price
        self._price_history = []

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        if new_price <= 0:
            raise ValueError(f"Price must be positive, got {new_price}")
        self._price_history.append(self._price)
        self._price = new_price

    @property
    def change_24h(self):
        if not self._price_history:
            return 0.0
        return (self._price - self._price_history[0]) / self._price_history[0] * 100

    @property
    def high(self):
        return max(self.all_prices)

    @property
    def low(self):
        return min(self.all_prices)

    @property
    def all_prices(self):
        return self._price_history + [self._price]

    def __repr__(self):
        return (f"PriceOracle({self.symbol!r}, price={self._price}, "
                f"history={len(self._price_history)})")

    def __str__(self):
        sign = "+" if self.change_24h >= 0 else ""
        return (f"{self.symbol}: ${self._price:,.2f} | "
                f"24h: {sign}{self.change_24h:.2f}% | "
                f"High: ${self.high:,.2f} | Low: ${self.low:,.2f}")


oracle = PriceOracle("ETH", 3050.0)
for p in [3120.0, 3247.85, 3310.0, 3290.0, 3350.0, 3247.85]:
    oracle.price = p

print(f"  {oracle}")
print(f"  High: ${oracle.high:,.2f}")
print(f"  Low:  ${oracle.low:,.2f}")
print(f"  All prices: {oracle.all_prices}")

try:
    oracle.price = -100
except ValueError as e:
    print(f"  Error: {e}")


# ── SOLUTION 6 — Transaction ──────────────────────────────────
print("\n── Solution 6: Full Transaction class ──")

class Transaction:
    """Complete Ethereum transaction model."""

    def __init__(self, tx_hash, from_address, to_address,
                 value_wei, gas_used, gas_price_gwei,
                 block_number, status="success", tx_type="transfer"):
        self.tx_hash        = tx_hash
        self.from_address   = from_address
        self.to_address     = to_address
        self.value_wei      = value_wei
        self.gas_used       = gas_used
        self.gas_price_gwei = gas_price_gwei
        self.block_number   = block_number
        self.status         = status
        self.tx_type        = tx_type

    @property
    def value_eth(self):
        return self.value_wei / 1e18

    @property
    def gas_cost_eth(self):
        return self.gas_used * self.gas_price_gwei * 1e9 / 1e18

    @property
    def total_cost_eth(self):
        return self.value_eth + self.gas_cost_eth

    @property
    def is_success(self):
        return self.status == "success"

    def _short(self, addr):
        return f"{addr[:10]}...{addr[-6:]}"

    def receipt(self, eth_price=3247.85):
        status_label = "✅ Success" if self.is_success else "❌ Failed"
        lines = [
            "=" * 54,
            "         ETHEREUM TRANSACTION RECEIPT",
            "=" * 54,
            f"  Status    : {status_label}",
            f"  Block     : {self.block_number:,}",
            f"  Type      : {self.tx_type}",
            f"  Hash      : {self.tx_hash[:18]}...{self.tx_hash[-6:]}",
            f"  From      : {self._short(self.from_address)}",
            f"  To        : {self._short(self.to_address)}",
            "-" * 54,
            f"  Value     : {self.value_eth:.6f} ETH  (${self.value_eth*eth_price:,.2f})",
            f"  Gas Used  : {self.gas_used:,} units @ {self.gas_price_gwei} Gwei",
            f"  Gas Cost  : {self.gas_cost_eth:.8f} ETH  (${self.gas_cost_eth*eth_price:.4f})",
            "-" * 54,
            f"  TOTAL     : {self.total_cost_eth:.6f} ETH  (${self.total_cost_eth*eth_price:,.2f})",
            "=" * 54,
        ]
        return "\n".join(lines)

    def summary(self):
        return (f"{self.tx_type.upper():12} | "
                f"{self._short(self.from_address)} → {self._short(self.to_address)} | "
                f"{self.value_eth:.4f} ETH | Block {self.block_number:,}")

    def __repr__(self):
        return f"Transaction({self.tx_hash[:10]!r}..., {self.value_eth:.4f} ETH, {self.status})"

    def __str__(self):
        icon  = "✅" if self.is_success else "❌"
        short = f"{self.tx_hash[:6]}...{self.tx_hash[-4:]}"
        return f"{icon} {short} | {self.value_eth:.4f} ETH | {self.gas_used:,} gas @ {self.gas_price_gwei} Gwei"

    def __eq__(self, other):
        if not isinstance(other, Transaction): return NotImplemented
        return self.tx_hash.lower() == other.tx_hash.lower()

    def __lt__(self, other):
        if not isinstance(other, Transaction): return NotImplemented
        return self.value_eth < other.value_eth


tx1 = Transaction(
    "0x5c504ed432cb51138bcf09aa5e8a410dd4a1e204ef84bfed1be16dfba1b22060",
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
    "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
    value_wei=1_500_000_000_000_000_000,
    gas_used=21_000, gas_price_gwei=20,
    block_number=19_847_293, status="success", tx_type="transfer")

tx2 = Transaction(
    "0xabc123def456abc123def456abc123def456abc123def456abc123def456abc1",
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
    "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
    value_wei=500_000_000_000_000_000,
    gas_used=148_320, gas_price_gwei=25,
    block_number=19_847_294, status="success", tx_type="swap")

print(f"  repr:         {repr(tx1)}")
print(f"  str:          {tx1}")
print(f"  value_eth:    {tx1.value_eth}")
print(f"  gas_cost_eth: {tx1.gas_cost_eth:.8f}")
print()
print(tx1.receipt())
print()
print(f"  tx1 summary:  {tx1.summary()}")
print(f"  tx2 summary:  {tx2.summary()}")
print(f"  tx1 == tx2:   {tx1 == tx2}")
print(f"  sorted:       {[repr(t) for t in sorted([tx2, tx1])]}")


# ── SOLUTION — Challenge: simple_chain ───────────────────────
print("\n── Solution — Challenge: simple_chain ──")

class ChainTransaction:
    def __init__(self, from_addr, to_addr, amount):
        self.from_addr = from_addr
        self.to_addr   = to_addr
        self.amount    = amount
        self.timestamp = int(time_module.time())

    @property
    def tx_hash(self):
        raw = f"{self.from_addr}{self.to_addr}{self.amount}{self.timestamp}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def __str__(self):
        return f"{self.from_addr} → {self.to_addr} | {self.amount} ETH"


class ChainBlock:
    def __init__(self, index, previous_hash, transactions, timestamp=None):
        self.index         = index
        self.previous_hash = previous_hash
        self.transactions  = transactions
        self.timestamp     = timestamp or int(time_module.time())

    @property
    def block_hash(self):
        tx_hashes = "".join(tx.tx_hash for tx in self.transactions)
        raw = f"{self.index}{self.previous_hash}{tx_hashes}{self.timestamp}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def is_valid(self):
        return self.block_hash.startswith("00")

    def __str__(self):
        return (f"Block #{self.index} | {len(self.transactions)} txns | "
                f"hash: {self.block_hash[:12]}...")


class Blockchain:
    def __init__(self):
        self.pending_transactions = []
        genesis = ChainBlock(index=0, previous_hash="0"*64,
                             transactions=[], timestamp=0)
        self.chain = [genesis]

    def add_transaction(self, from_addr, to_addr, amount):
        self.pending_transactions.append(ChainTransaction(from_addr, to_addr, amount))

    def mine_block(self):
        if not self.pending_transactions:
            raise ValueError("No pending transactions")
        new_block = ChainBlock(
            index         = len(self.chain),
            previous_hash = self.chain[-1].block_hash,
            transactions  = list(self.pending_transactions),
        )
        self.chain.append(new_block)
        self.pending_transactions = []
        return new_block

    def is_valid_chain(self):
        for i in range(1, len(self.chain)):
            if self.chain[i].previous_hash != self.chain[i-1].block_hash:
                return False
        return True

    def get_balance(self, address):
        balance = 0.0
        for block in self.chain:
            for tx in block.transactions:
                if tx.to_addr   == address: balance += tx.amount
                if tx.from_addr == address: balance -= tx.amount
        return round(balance, 8)

    def __len__(self):
        return len(self.chain)

    def __str__(self):
        return f"Blockchain: {len(self.chain)} blocks | valid: {self.is_valid_chain()}"


bc = Blockchain()
bc.add_transaction("0xAlice", "0xBob",   5.0)
bc.add_transaction("0xBob",   "0xCarol", 2.0)
bc.mine_block()

bc.add_transaction("0xCarol", "0xAlice", 1.0)
bc.add_transaction("0xAlice", "0xDave",  0.5)
bc.mine_block()

print(f"\n  {bc}")
print(f"  Chain valid: {bc.is_valid_chain()}")
for block in bc.chain:
    print(f"  {block}")
    for tx in block.transactions:
        print(f"    {tx}")

print()
for addr in ["0xAlice", "0xBob", "0xCarol", "0xDave"]:
    print(f"  Balance {addr}: {bc.get_balance(addr)} ETH")

print("\n" + "=" * 60)
print("Phase 1 complete! 6 weeks of Python foundations done.")
print("Next → Phase 2: Python for Data Analysis")
print("=" * 60)
