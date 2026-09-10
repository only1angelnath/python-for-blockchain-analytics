"""
Week 6 Exercises — Object-Oriented Programming
Python for Blockchain Analytics | Phase 1

Instructions:
- Attempt every exercise before opening exercises_solutions.py
- Each exercise builds on the last — complete them in order
- Run with: python3 exercises.py

Solutions are in: exercises_solutions.py
"""

print("=" * 60)
print("WEEK 6 EXERCISES — Object-Oriented Programming")
print("=" * 60)


# ─────────────────────────────────────────────────────────────
# EXERCISE 1 — Your first class: Block
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 1: The Block class ──")
"""
A blockchain is made of blocks. Each block has:
  - block_number  (int)
  - timestamp     (int)   — Unix timestamp
  - miner         (str)   — address that mined/validated the block
  - tx_hashes     (list)  — list of transaction hashes in this block
  - gas_used      (int)
  - gas_limit     (int)   — default: 30_000_000
  - base_fee_gwei (float)

Write a Block class with:
  1. __init__ accepting all fields (gas_limit defaults to 30_000_000)
  2. tx_count()         → number of transactions
  3. gas_utilisation()  → gas_used / gas_limit as a percentage (float)
  4. is_full()          → True if gas utilisation > 95%
  5. add_transaction(tx_hash) → appends to tx_hashes
  6. __repr__  → Block(number=19847293, txns=142, gas=87.3%)
  7. __str__   → "Block 19,847,293 | 142 txns | 87.3% gas | 18.5 Gwei"
  8. __len__   → number of transactions


Test with:
  block = Block(
      block_number  = 19_847_293,
      timestamp     = 1_714_000_000,
      miner         = "0xeBec795c9c8bBD61FFc14A6662944748F299cAec",
      tx_hashes     = ["0xaaa", "0xbbb", "0xccc"],
      gas_used      = 26_174_000,
      base_fee_gwei = 18.5,
  )
  block.add_transaction("0xddd")

Print: repr, str, tx_count(), gas_utilisation(), is_full(), len(block)
"""

# YOUR CODE HERE
class Block:
    """
A blockchain is made of blocks. Each block has:
    block_number:  (int)
    timestamp:     (int)   — Unix timestamp
    miner:         (str)   — address that mined/validated the block
    tx_hashes:     (list)  — list of transaction hashes in this block
    gas_used:      (int)
    gas_limit:     (int)   — default: 30_000_000
    base_fee_gwei: (float)
  """
    def __init__(self, block_number: int, timestamp: int, miner: str, tx_hashes: list, gas_used: int, base_fee_gwei: float, gas_limit: int = 30_000_000):
        self.block_number = block_number
        self.timestamp = timestamp
        self.miner = miner
        self.tx_hashes = tx_hashes
        self.gas_used = gas_used
        self.gas_limit = gas_limit
        self.base_fee_gwei = base_fee_gwei

    def tx_count(self):
        return len(self.tx_hashes)

    def gas_utilisation(self):
        return (self.gas_used / self.gas_limit) * 100

    def is_full(self):
        return self.gas_utilisation() > 95

    def add_transaction(self, tx_hash):
        self.tx_hashes.append(tx_hash)

    def __repr__(self):
        return f"Block(number={self.block_number}, txns={self.tx_count()}, gas={self.gas_utilisation():.1f}%)"

    def __str__(self):
        return f"Block {self.block_number:,} | {self.tx_count()} txns | {self.gas_utilisation():.1f}% gas | {self.base_fee_gwei} Gwei"

    def __len__(self):
        return self.tx_count()

block = Block(
      block_number  = 19_847_293,
      timestamp     = 1_714_000_000,
      miner         = "0xeBec795c9c8bBD61FFc14A6662944748F299cAec",
      tx_hashes     = ["0xaaa", "0xbbb", "0xccc"],
      gas_used      = 26_174_000,
      base_fee_gwei = 18.5,
  )

block.add_transaction("0xddd")

print(f"  repr:            {repr(block)}")
print(f"  str:             {block}")
print(f"  tx_count:        {block.tx_count()}")
print(f"  gas_utilisation: {block.gas_utilisation():.2f}%")
print(f"  is_full:         {block.is_full()}")
print(f"  len:             {len(block)}")


# ─────────────────────────────────────────────────────────────
# EXERCISE 2 — Instance vs class attributes: TokenRegistry
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 2: TokenRegistry class ──")
"""
Build a TokenRegistry that tracks all registered tokens.

Class attributes (shared across ALL registry instances):
  - _registry: dict  — {symbol: {price, decimals}}
  - _count: int      — total tokens ever registered

Instance attributes (per registry object):
  - name: str        — name of this registry (e.g. "Mainnet")
  - created_at: str  — timestamp string when this registry was created

Methods:
  - register(symbol, price, decimals=18)
      Raises ValueError if symbol already exists. Increments _count.
  - get(symbol)
      Returns token dict or raises KeyError with a helpful message.
  - remove(symbol)
      Removes a token. Raises KeyError if not found.
  - all_symbols()
      Returns sorted list of all registered symbols.
  - count() — @classmethod returning _count
  - summary() — prints a formatted table of all tokens

Test:
  1. mainnet = TokenRegistry("Mainnet")
  2. Register ETH, BTC, USDC, UNI
  3. Try registering ETH again — catch ValueError
  4. Print mainnet.count() and mainnet.summary()
  5. testnet = TokenRegistry("Testnet"), register WETH
  6. Show _count includes both registries' tokens
"""

# YOUR CODE HERE
import datetime
class TokenRegistry:
  """
  A TokenRegistry that tracks all registered tokens.

  Class attributes (shared across ALL registry instances):
    - _registry: dict  — {symbol: {price, decimals}}
    - _count: int      — total tokens ever registered
  """
  _registry = {}
  _count = 0

  def __init__(self, name: str, created_at: str):
    self.name = name
    self.created_at = created_at

  def register(self, symbol: str, price: float, decimals: int = 18):
    if symbol in TokenRegistry._registry:
      raise ValueError(f"Token {symbol} is already registered.")
    TokenRegistry._registry[symbol] = {"price": price, "decimals": decimals}
    TokenRegistry._count += 1

  def get(self, symbol: str):
    if symbol not in TokenRegistry._registry:
      raise KeyError(f"Token {symbol} not found in registry.")
    return TokenRegistry._registry[symbol]

  def remove(self, symbol: str):
    if symbol not in TokenRegistry._registry:
      raise KeyError(f"Token {symbol} not found in registry.")
    del TokenRegistry._registry[symbol]
    TokenRegistry._count -= 1

  def all_symbols(self):
    return sorted(TokenRegistry._registry.keys())

  @classmethod
  def count(cls):
    return cls._count

  def summary(self):
    print(f"Token Registry: {self.name} (created at {self.created_at})")
    print("Symbol | Price | Decimals")
    print("-" * 30)
    for symbol, info in sorted(TokenRegistry._registry.items()):
      print(f"{symbol} | {info['price']} | {info['decimals']}")

TokenRegistry._registry = {}
TokenRegistry._count    = 0

mainnet = TokenRegistry("Mainnet", "2026-08-19 05:22")
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

testnet = TokenRegistry("Testnet", "2026-08-19 05:30")
testnet.register("WETH", 3247.85, 18)
print(f"\n  After testnet, total count: {TokenRegistry.count()}")


# ─────────────────────────────────────────────────────────────
# EXERCISE 3 — Dunder methods: LiquidityPool
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 3: LiquidityPool with dunders ──")
"""
Write a LiquidityPool class:

  Attributes:
    - token0 (str)     — first token symbol
    - token1 (str)     — second token symbol
    - reserve0 (float) — amount of token0 in pool
    - reserve1 (float) — amount of token1 in pool
    - fee_tier (int)   — in basis points (500 = 0.05%)

  Properties (@property):
    - price      → reserve1 / reserve0
    - pair_name  → "token0/token1"
    - fee_pct    → fee_tier / 10_000  (as a decimal, e.g. 0.0005)

  Regular method:
    - calculate_tvl(price0_usd, price1_usd)
        → reserve0 * price0_usd + reserve1 * price1_usd

  Dunder methods:
    - __repr__ → LiquidityPool('USDC/ETH', fee=0.05%, price=3247.85)
    - __str__  → "USDC/ETH | Price: 3,247.85 | Fee: 0.05%"
    - __eq__   → equal if same pair regardless of order (USDC/ETH == ETH/USDC)
    - __gt__   → pool A > pool B if pool A has higher reserve0
    - __lt__   → pool A < pool B if pool A has lower reserve0

Test:
  pool1 = LiquidityPool("USDC", "ETH",  1_000_000, 308.0, fee_tier=500)
  pool2 = LiquidityPool("USDC", "ETH",  500_000,   154.0, fee_tier=3000)
  pool3 = LiquidityPool("ETH",  "USDC", 308.0,     1_000_000, fee_tier=500)

  Print pool1.price, pool1.pair_name, pool1.calculate_tvl(1.0, 3247.85)
  Test: pool1 == pool3, pool1 > pool2, sorted([pool2, pool1])
"""

# YOUR CODE HERE
class LiquidityPool:
    """
    A LiquidityPool class representing a pair of tokens in a pool.

    Attributes:
        - token0 (str)     — first token symbol
        - token1 (str)     — second token symbol
        - reserve0 (float) — amount of token0 in pool
        - reserve1 (float) — amount of token1 in pool
        - fee_tier (int)   — in basis points (500 = 0.05%)
    """
    def __init__(self, token0: str, token1: str, reserve0: float, reserve1: float, fee_tier: int):
        self.token0 = token0
        self.token1 = token1
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

    def calculate_tvl(self, price0_usd: float, price1_usd: float):
        return self.reserve0 * price0_usd + self.reserve1 * price1_usd

    def __repr__(self):
        return f"LiquidityPool('{self.pair_name}', fee={self.fee_pct*100:.2f}%, price={self.price:.2f})"

    def __str__(self):
        return f"{self.pair_name} | Price: {self.price:.2f} | Fee: {self.fee_pct*100:.2f}%"

    def __eq__(self, other):
        return {self.token0, self.token1} == {other.token0, other.token1}

    def __gt__(self, other):
        return self.reserve0 > other.reserve0

    def __lt__(self, other):
        return self.reserve0 < other.reserve0

pool1 = LiquidityPool("USDC", "ETH",  1_000_000, 308.0, fee_tier=500)
pool2 = LiquidityPool("USDC", "ETH",  500_000,   154.0, fee_tier=3000)
pool3 = LiquidityPool("ETH",  "USDC", 308.0,     1_000_000, fee_tier=500)

print(f"  {pool1}")
print(f"  {pool2}")
print(f"  {pool3}")
print(f"  price:        {pool1.price:,.4f}")
print(f"  pair_name:    {pool1.pair_name}")
print(f"  TVL:          ${pool1.calculate_tvl(1.0, 3247.85):,.2f}")
print(f"  pool1==pool3: {pool1 == pool3}")
print(f"  pool1>pool2:  {pool1 > pool2}")
sorted_pools = sorted([pool2, pool1])
print(f"  sorted:       {[p.pair_name for p in sorted_pools]}") 


# ─────────────────────────────────────────────────────────────
# EXERCISE 4 — Inheritance: DeFi Protocol hierarchy
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 4: Protocol inheritance hierarchy ──")

class Protocol:
    """
    Base class for DeFi protocols.

    Attributes:
        - name (str)
        - chain (str)
        - tvl_usd (float)
    """
    def __init__(self, name: str, chain: str, tvl_usd: float):
        self.name = name
        self.chain = chain
        self.tvl_usd = tvl_usd

    def tvl_formatted(self):
        if self.tvl_usd >= 1_000_000_000:
            return f"${self.tvl_usd / 1_000_000_000:.2f}B"
        elif self.tvl_usd >= 1_000_000:
            return f"${self.tvl_usd / 1_000_000:.2f}M"
        elif self.tvl_usd >= 1_000:
            return f"${self.tvl_usd / 1_000:.2f}K"
        else:
            return f"${self.tvl_usd:.2f}"

    def info(self):
        return f"{self.name} on {self.chain} | with TVL: {self.tvl_formatted()}"

class DEX(Protocol):
    """
    Class representing a decentralized exchange (DEX).

    Attributes:
        - name (str)
        - chain (str)
        - tvl_usd (float)
        - volume_24h (float)
        - fee_tier (float)
    """
    def __init__(self, name: str, chain: str, tvl_usd: float, volume_24h: float, fee_tier: float):
        super().__init__(name, chain, tvl_usd)
        self.volume_24h = volume_24h
        self.fee_tier = fee_tier

    @property
    def fees_24h(self):
        return self.volume_24h * self.fee_tier

    @property
    def apr_estimate(self):
        return self.fees_24h * 365 / self.tvl_usd * 100

    def info(self):
        return f"{super().info()} | 24H Volume: ${self.volume_24h:.2f} | APR: {self.apr_estimate:.2f}%"

    def is_high_yield(self, threshold=20.0):
        return self.apr_estimate > threshold

class LendingProtocol(Protocol):
        
        def __init__(self, name: str, chain: str, tvl_usd: float, total_borrowed: float):
            super().__init__(name, chain, tvl_usd)
            self.total_borrowed = total_borrowed

        @property
        def utilisation(self):
            return self.total_borrowed / self.tvl_usd * 100

        def info(self):
            return f"{super().info()} | Utilisation: {self.utilisation:.2f}%"

        def borrow_apr(self, base_rate=2.0):
            return base_rate * (1 + self.utilisation/100)

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

# ─────────────────────────────────────────────────────────────

"""      
Protocol (parent)
  - name, chain, tvl_usd
  - tvl_formatted() → "$5.20B" / "$420.00M" / "$12.50K"
  - info() → basic one-line description

DEX(Protocol)
  - volume_24h, fee_tier (decimal, e.g. 0.003)
  - fees_24h (@property) → volume_24h * fee_tier
  - apr_estimate (@property) → fees_24h * 365 / tvl_usd * 100
  - Override info() to include volume and APR
  - is_high_yield(threshold=20.0) → True if apr > threshold

LendingProtocol(Protocol)
  - total_borrowed
  - utilisation (@property) → total_borrowed / tvl_usd * 100
  - Override info() to include utilisation
  - borrow_apr(base_rate=2.0) → base_rate * (1 + utilisation/100)

Test:
  uniswap = DEX("Uniswap V3", "ethereum", 5_200_000_000, 1_800_000_000, 0.003)
  gmx     = DEX("GMX", "arbitrum", 680_000_000, 310_000_000, 0.001)
  aave    = LendingProtocol("Aave V3", "ethereum", 12_800_000_000, 8_200_000_000)

  for p in [uniswap, gmx, aave]:
      print(p.info())

  isinstance checks, is_high_yield(), borrow_apr()
  sorted by tvl_usd descending
"""

# YOUR CODE HERE


# ─────────────────────────────────────────────────────────────
# EXERCISE 5 — @property: PriceOracle
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 5: PriceOracle with @property ──")
"""
Write a PriceOracle class:

  Attributes:
    - symbol (str)
    - _price (float)         — private, exposed via @property
    - _price_history (list)  — past prices, most recent last
    - decimals (int, default 18)

  Properties:
    - price (getter) → return _price
    - price (setter) → validate > 0, save old price to history, update _price
    - change_24h → (current - first_in_history) / first_in_history * 100
                   Return 0.0 if history has fewer than 1 entry
    - high  → max of all prices including current
    - low   → min of all prices including current
    - all_prices → _price_history + [_price]

  Dunder methods:
    - __repr__ → PriceOracle('ETH', price=3247.85, history=5)
    - __str__  → "ETH: $3,247.85 | 24h: +2.40% | High: $3,400.00 | Low: $3,050.00"

Test:
  oracle = PriceOracle("ETH", 3050.0)
  for price in [3120.0, 3247.85, 3310.0, 3290.0, 3350.0, 3247.85]:
      oracle.price = price

  print(oracle)
  print("High:", oracle.high)
  print("Low:", oracle.low)
  print("All prices:", oracle.all_prices)

  try:
      oracle.price = -100
  except ValueError as e:
      print("Error:", e)
"""

# YOUR CODE HERE
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

# ─────────────────────────────────────────────────────────────
# EXERCISE 6 — Full class: Transaction
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 6: Full Transaction class ──")
"""
Build a complete Transaction class:

  Attributes:
    - tx_hash, from_address, to_address
    - value_wei (int), gas_used (int), gas_price_gwei (float)
    - block_number (int)
    - status (str)   — "success" or "failed"
    - tx_type (str)  — "transfer", "swap", "contract_call", etc.

  Properties:
    - value_eth        → value_wei / 1e18
    - gas_cost_eth     → gas_used * gas_price_gwei * 1e9 / 1e18
    - total_cost_eth   → value_eth + gas_cost_eth
    - is_success       → status == "success"

  Methods:
    - receipt(eth_price=3247.85) → formatted multi-line string
    - summary() → one-line string

  Dunder methods:
    - __repr__ → Transaction('0xabc...', 1.5 ETH, success)
    - __str__  → "✅ 0xabc...xyz | 1.5000 ETH | 21,000 gas @ 20 Gwei"
    - __eq__   → same tx_hash (case-insensitive)
    - __lt__   → sort by value_eth ascending

Test:
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

  Print: repr, str, value_eth, gas_cost_eth, receipt() for tx1
  Print: summary() for both
  Test: tx1 == tx2, sorted([tx2, tx1])
"""

# YOUR CODE HERE
class completeTransaction:
    """
    A complete Transaction class representing a blockchain transaction.

    Attributes:
        - tx_hash, from_address, to_address
        - value_wei (int), gas_used (int), gas_price_gwei (float)
        - block_number (int)
        - status (str)   — "success" or "failed"
        - tx_type (str)  — "transfer", "swap", "contract_call", etc.
    """
    def __init__(self, tx_hash, from_address, to_address, value_wei, gas_used, gas_price_gwei, block_number, status, tx_type):
        self.tx_hash = tx_hash
        self.from_address = from_address
        self.to_address = to_address
        self.value_wei = value_wei
        self.gas_used = gas_used
        self.gas_price_gwei = gas_price_gwei
        self.block_number = block_number
        self.status = status
        self.tx_type = tx_type

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

    def receipt(self, eth_price=3247.85):
        total_cost_usd = self.total_cost_eth * eth_price
        return (f"Transaction Receipt:\n"
                f"  Hash: {self.tx_hash}\n"
                f"  From: {self.from_address}\n"
                f"  To: {self.to_address}\n"
                f"  Value: {self.value_eth:.4f} ETH\n"
                f"  Gas Used: {self.gas_used}\n"
                f"  Gas Price: {self.gas_price_gwei} Gwei\n"
                f"  Total Cost: {self.total_cost_eth:.4f} ETH (${total_cost_usd:.2f})\n"
                f"  Block Number: {self.block_number}\n"
                f"  Status: {self.status}\n"
                f"  Type: {self.tx_type}")

    def summary(self):
        return (f"{'✅' if self.is_success else '❌'} {self.tx_hash[:10]}... | "
                f"{self.value_eth:.4f} ETH | "
                f"{self.gas_used:,} gas @ {self.gas_price_gwei} Gwei")

    def __repr__(self):
        return (f"Transaction(tx_hash='{self.tx_hash}', "
                f"from_address='{self.from_address}', "
                f"to_address='{self.to_address}', "
                f"value_wei={self.value_wei}, "
                f"gas_used={self.gas_used}, "
                f"gas_price_gwei={self.gas_price_gwei}, "
                f"block_number={self.block_number}, "
                f"status='{self.status}', "
                f"tx_type='{self.tx_type}')")

    def __str__(self):
        return self.summary()

    def __eq__(self, other):
        return self.tx_hash == other.tx_hash

    def __lt__(self, other):
# ─────────────────────────────────────────────────────────────
# CHALLENGE — Phase 1 Capstone: simple_chain.py
# ─────────────────────────────────────────────────────────────
print("\n── Challenge: simple_chain — Simulated blockchain ──")
"""
Build a minimal blockchain in pure Python using three classes.

1. Transaction
   - from_addr, to_addr, amount, timestamp
   - tx_hash property: built by hashing a string of the four fields
     Hint: import hashlib; hashlib.sha256(string.encode()).hexdigest()
   - __str__ → "0xAlice → 0xBob | 1.5 ETH"

2. Block
   - index, previous_hash, transactions (list), timestamp
   - block_hash property → sha256 of index + previous_hash + all tx hashes + timestamp
   - is_valid() → True if block_hash starts with "00" (simplified PoW)
   - __str__ → "Block #3 | 2 txns | hash: 00ab1234..."

3. Blockchain
   - chain (list of Block)
   - __init__ creates the genesis block (index=0, previous_hash="0"*64, no txns)
   - pending_transactions (list)
   - add_transaction(from_addr, to_addr, amount) → adds to pending
   - mine_block() → creates Block from pending, clears pending
   - is_valid_chain() → every block's previous_hash matches prior block's hash
   - get_balance(address) → sum of received - sum of sent across all mined txns
   - __len__ → number of blocks
   - __str__ → "Blockchain: 4 blocks | valid: True"

Demo:
  bc = Blockchain()
  bc.add_transaction("0xAlice", "0xBob",   5.0)
  bc.add_transaction("0xBob",   "0xCarol", 2.0)
  bc.mine_block()

  bc.add_transaction("0xCarol", "0xAlice", 1.0)
  bc.add_transaction("0xAlice", "0xDave",  0.5)
  bc.mine_block()

  print(bc)
  print("Chain valid:", bc.is_valid_chain())
  for block in bc.chain:
      print(block)
  print("Bob's balance:", bc.get_balance("0xBob"))
"""

# YOUR CODE HERE


print("\n" + "=" * 60)
print("Done! Check exercises_solutions.py to compare.")
print("Phase 1 complete — 6 weeks of Python foundations!")
print("=" * 60)
