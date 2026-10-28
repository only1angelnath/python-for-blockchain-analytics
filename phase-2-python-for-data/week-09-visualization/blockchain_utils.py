"""
blockchain_utils.py
Python for Blockchain Analytics — Phase 1, Week 5

Your personal blockchain analytics toolkit.
Import in any notebook or script with:
    from blockchain_utils import *
    # or
    import blockchain_utils as bc

Add your own utilities at the bottom — this file grows with you.
"""

# ── Constants ──────────────────────────────────────────────────────────────────
ETH_DECIMALS   = 18
GWEI_TO_WEI    = 10**9
WEI_PER_ETH    = 10**18

CHAIN_NAMES = {
    1:      "Ethereum",
    137:    "Polygon",
    42161:  "Arbitrum One",
    8453:   "Base",
    10:     "Optimism",
    56:     "BNB Chain",
    43114:  "Avalanche C-Chain",
    250:    "Fantom",
    100:    "Gnosis",
    1101:   "Polygon zkEVM",
    324:    "zkSync Era",
    59144:  "Linea",
}

BLOCK_EXPLORER = {
    1:      "https://etherscan.io",
    137:    "https://polygonscan.com",
    42161:  "https://arbiscan.io",
    8453:   "https://basescan.org",
    10:     "https://optimistic.etherscan.io",
    56:     "https://bscscan.com",
}

STABLECOINS  = {"USDC", "USDT", "DAI", "FRAX", "LUSD", "BUSD", "TUSD", "USDP", "USDE", "PYUSD"}
MAJOR_TOKENS = {"ETH", "WETH", "BTC", "WBTC", "BNB", "SOL", "AVAX", "MATIC", "POL"}

AVG_BLOCK_TIME_ETH = 12.0   # seconds


# ── Address utilities ──────────────────────────────────────────────────────────
def shorten_address(address: str, prefix: int = 6, suffix: int = 4) -> str:
    """
    Shorten a 0x wallet address for display.

    Args:
        address: Full Ethereum address string
        prefix:  Characters to keep from the start (default: 6, includes '0x')
        suffix:  Characters to keep from the end (default: 4)

    Returns:
        str: Shortened address e.g. "0xd8dA...6045"

    Example:
        >>> shorten_address("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045")
        '0xd8dA...6045'
    """
    if len(address) <= prefix + suffix:
        return address
    return f"{address[:prefix]}...{address[-suffix:]}"


def is_valid_eth_address(address: str) -> bool:
    """
    Check if a string is a valid Ethereum address.

    A valid address starts with '0x' and is followed by exactly 40 hex characters.

    Args:
        address: String to validate

    Returns:
        bool: True if valid, False otherwise
    """
    hex_chars = set("0123456789abcdefABCDEF")
    return (
        isinstance(address, str)
        and address.startswith("0x")
        and len(address) == 42
        and all(c in hex_chars for c in address[2:])
    )


def normalize_address(address: str) -> str:
    """
    Normalize an address to lowercase for consistent comparison.

    Args:
        address: Ethereum address (any case)

    Returns:
        str: Lowercase address
    """
    return address.lower()


# ── Unit conversions ───────────────────────────────────────────────────────────
def wei_to_eth(wei: int) -> float:
    """Convert Wei (int) to ETH (float)."""
    return wei / WEI_PER_ETH


def eth_to_wei(eth: float) -> int:
    """Convert ETH (float) to Wei (int)."""
    return int(eth * WEI_PER_ETH)


def gwei_to_eth(gwei: float) -> float:
    """Convert Gwei to ETH."""
    return gwei / 1_000_000_000


def gwei_to_wei(gwei: float) -> int:
    """Convert Gwei to Wei."""
    return int(gwei * GWEI_TO_WEI)


def token_amount(raw: int, decimals: int = 18) -> float:
    """
    Convert a raw token integer to a human-readable float.

    Args:
        raw:      Raw token amount (integer, as stored on-chain)
        decimals: Token decimals (default: 18)

    Returns:
        float: Human-readable amount

    Example:
        >>> token_amount(1_000_000, decimals=6)   # USDC
        1.0
    """
    return raw / 10**decimals


def format_token(raw: int, symbol: str, decimals: int = 18, precision: int = 6) -> str:
    """
    Format a raw token amount with symbol.

    Args:
        raw:       Raw on-chain amount
        symbol:    Token symbol (e.g. "ETH", "USDC")
        decimals:  Token decimals (default: 18)
        precision: Decimal places in output (default: 6)

    Returns:
        str: e.g. "1.500000 ETH"
    """
    return f"{token_amount(raw, decimals):,.{precision}f} {symbol}"


# ── Gas utilities ──────────────────────────────────────────────────────────────
def gas_cost_eth(gas_used: int, gas_price_gwei: float) -> float:
    """
    Calculate gas cost in ETH.

    Args:
        gas_used:       Units of gas consumed
        gas_price_gwei: Gas price in Gwei

    Returns:
        float: Gas cost in ETH
    """
    return gas_used * gas_price_gwei * GWEI_TO_WEI / WEI_PER_ETH


def gas_cost_usd(gas_used: int, gas_price_gwei: float, eth_price_usd: float) -> float:
    """
    Calculate gas cost in USD.

    Args:
        gas_used:       Units of gas consumed
        gas_price_gwei: Gas price in Gwei
        eth_price_usd:  Current ETH price in USD

    Returns:
        float: Gas cost in USD
    """
    return gas_cost_eth(gas_used, gas_price_gwei) * eth_price_usd


def gas_tier(gwei: float) -> str:
    """
    Return a human-readable gas price tier label.

    Args:
        gwei: Gas price in Gwei

    Returns:
        str: Tier label with emoji
    """
    if gwei < 10:    return "🟢 Low"
    elif gwei < 30:  return "🟡 Normal"
    elif gwei < 50:  return "🟠 High"
    elif gwei < 100: return "🔴 Very High"
    else:            return "🚨 Extreme"


# ── Price & P&L utilities ──────────────────────────────────────────────────────
def eth_to_usd(eth: float, eth_price_usd: float) -> float:
    """Convert ETH amount to USD."""
    return eth * eth_price_usd


def usd_to_eth(usd: float, eth_price_usd: float) -> float:
    """Convert USD amount to ETH."""
    if eth_price_usd <= 0:
        raise ValueError("ETH price must be positive")
    return usd / eth_price_usd


def pnl(cost_basis_usd: float, current_value_usd: float) -> tuple:
    """
    Calculate profit and loss for a position.

    Args:
        cost_basis_usd:    Original purchase cost in USD
        current_value_usd: Current market value in USD

    Returns:
        tuple: (pnl_usd: float, pnl_pct: float)
    """
    pnl_usd = current_value_usd - cost_basis_usd
    pnl_pct = (pnl_usd / cost_basis_usd * 100) if cost_basis_usd else 0.0
    return round(pnl_usd, 2), round(pnl_pct, 4)


def price_impact(amount_usd: float, liquidity_usd: float) -> float:
    """
    Estimate trade price impact as a percentage.

    Args:
        amount_usd:    Trade size in USD
        liquidity_usd: Pool liquidity in USD

    Returns:
        float: Estimated price impact percentage
    """
    if liquidity_usd <= 0:
        raise ValueError("Liquidity must be positive")
    return round((amount_usd / liquidity_usd) * 100, 4)


def trade_slippage(expected_price: float, actual_price: float) -> float:
    """
    Calculate trade slippage as a percentage.

    Positive = paid more than expected (bad for buyer).
    Negative = paid less than expected (good for buyer).

    Args:
        expected_price: Price at time of quote
        actual_price:   Price at execution

    Returns:
        float: Slippage percentage
    """
    if expected_price <= 0:
        raise ValueError("Expected price must be positive")
    return round((actual_price - expected_price) / expected_price * 100, 4)


# ── DeFi metrics ───────────────────────────────────────────────────────────────
def calculate_liquidation_price(
    collateral_eth: float,
    debt_usd: float,
    liquidation_threshold: float = 0.825,
) -> float:
    """
    Calculate the ETH price at which a collateralised position gets liquidated.

    Args:
        collateral_eth:         ETH deposited as collateral
        debt_usd:               Outstanding debt in USD
        liquidation_threshold:  Protocol threshold (default: 82.5%)

    Returns:
        float: ETH price (USD) at liquidation point
    """
    if collateral_eth <= 0 or liquidation_threshold <= 0:
        raise ValueError("Collateral and threshold must be positive")
    return round(debt_usd / (collateral_eth * liquidation_threshold), 2)


def health_factor(
    collateral_eth: float,
    debt_usd: float,
    eth_price_usd: float,
    liquidation_threshold: float = 0.825,
) -> float:
    """
    Calculate position health factor (> 1 = safe, < 1 = liquidatable).

    Args:
        collateral_eth:         Collateral in ETH
        debt_usd:               Debt in USD
        eth_price_usd:          Current ETH price
        liquidation_threshold:  Protocol threshold (default: 82.5%)

    Returns:
        float: Health factor
    """
    collateral_usd = collateral_eth * eth_price_usd
    return round((collateral_usd * liquidation_threshold) / debt_usd, 4)


def apy_to_apr(apy: float, compound_periods: int = 365) -> float:
    """
    Convert APY to APR.

    Args:
        apy:               APY as percentage (e.g. 12.5 for 12.5%)
        compound_periods:  Compounding periods per year (default: 365)

    Returns:
        float: APR as percentage
    """
    if apy < 0:
        raise ValueError("APY cannot be negative")
    apr = ((1 + apy / 100) ** (1 / compound_periods) - 1) * compound_periods * 100
    return round(apr, 4)


# ── Token classification ───────────────────────────────────────────────────────
def token_category(symbol: str) -> str:
    """Classify a token symbol: 'stablecoin', 'major', or 'altcoin'."""
    if symbol in STABLECOINS:   return "stablecoin"
    if symbol in MAJOR_TOKENS:  return "major"
    return "altcoin"


def is_stablecoin(symbol: str) -> bool:
    """Return True if the symbol is a known stablecoin."""
    return symbol in STABLECOINS


# ── Wallet classification ──────────────────────────────────────────────────────
def classify_wallet(
    tx_count: int,
    balance_eth: float,
    has_contract_interactions: bool = False,
) -> str:
    """
    Classify a wallet based on activity metrics.

    Args:
        tx_count:                    Total transaction count
        balance_eth:                 Current ETH balance
        has_contract_interactions:   Whether wallet interacts with contracts

    Returns:
        str: Wallet label with emoji
    """
    if tx_count > 10_000:                     return "🤖 Bot / High-frequency"
    if balance_eth > 1_000:                   return "🐋 Whale"
    if balance_eth > 10 and tx_count > 100:   return "🐬 Dolphin"
    if has_contract_interactions:             return "⚡ DeFi User"
    if tx_count > 50:                         return "👤 Active Retail"
    return "🐣 New / Inactive"


# ── Chain & explorer utilities ─────────────────────────────────────────────────
def chain_name(chain_id: int) -> str:
    """Return human-readable chain name for a chain ID."""
    return CHAIN_NAMES.get(chain_id, f"Unknown Chain ({chain_id})")


def get_explorer_url(chain_id: int, tx_hash: str = "", address: str = "") -> str:
    """
    Build a block explorer URL for a transaction or address.

    Args:
        chain_id: EVM chain ID
        tx_hash:  Transaction hash (optional)
        address:  Wallet/contract address (optional)

    Returns:
        str: Full explorer URL
    """
    base = BLOCK_EXPLORER.get(chain_id, "https://etherscan.io")
    if tx_hash:
        return f"{base}/tx/{tx_hash}"
    if address:
        return f"{base}/address/{address}"
    return base


def block_to_timestamp_estimate(
    target_block: int,
    known_block: int,
    known_timestamp: int,
    avg_block_time: float = AVG_BLOCK_TIME_ETH,
) -> int:
    """
    Estimate Unix timestamp for any block number given a reference point.

    Args:
        target_block:    Block to estimate
        known_block:     Reference block with known timestamp
        known_timestamp: Unix timestamp of the reference block
        avg_block_time:  Seconds per block (default: 12.0 for Ethereum)

    Returns:
        int: Estimated Unix timestamp
    """
    block_diff = target_block - known_block
    return known_timestamp + int(block_diff * avg_block_time)


# ── Formatting helpers ─────────────────────────────────────────────────────────
def fmt_usd(value: float, decimals: int = 2) -> str:
    """Format a USD value: '$1,234.56'"""
    return f"${value:,.{decimals}f}"


def fmt_eth(value: float, decimals: int = 4) -> str:
    """Format an ETH value: '1.2500 ETH'"""
    return f"{value:,.{decimals}f} ETH"


def fmt_pct(value: float, decimals: int = 2, sign: bool = True) -> str:
    """Format a percentage: '+12.50%'"""
    return f"{value:+.{decimals}f}%" if sign else f"{value:.{decimals}f}%"


def fmt_large(value: float) -> str:
    """Format large numbers as '$1.23B', '$456.78M', '$12.34K'."""
    if abs(value) >= 1e9:   return f"${value/1e9:.2f}B"
    if abs(value) >= 1e6:   return f"${value/1e6:.2f}M"
    if abs(value) >= 1e3:   return f"${value/1e3:.2f}K"
    return f"${value:.2f}"


def fmt_hash(tx_hash: str, style: str = "short") -> str:
    """
    Format a transaction hash.

    Args:
        tx_hash: Full transaction hash
        style:   'short' (default) → '0xabc...xyz'
                 'full'            → full hash
                 'link'            → etherscan URL

    Returns:
        str: Formatted hash
    """
    if style == "full":
        return tx_hash
    if style == "link":
        return f"https://etherscan.io/tx/{tx_hash}"
    return shorten_address(tx_hash, prefix=10, suffix=8)


# ── Self-test ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("blockchain_utils.py — self test")
    print("-" * 45)

    addr = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    tx   = "0x5c504ed432cb51138bcf09aa5e8a410dd4a1e204ef84bfed1be16dfba1b22060"

    tests = [
        ("shorten_address",    shorten_address(addr)),
        ("is_valid_address",   is_valid_eth_address(addr)),
        ("wei_to_eth",         f"{wei_to_eth(1_500_000_000_000_000_000):.4f} ETH"),
        ("eth_to_wei",         f"{eth_to_wei(1.5):,} Wei"),
        ("gas_cost_usd",       fmt_usd(gas_cost_usd(21_000, 20, 3247.85))),
        ("gas_tier(35)",       gas_tier(35)),
        ("token_category",     f"USDC={token_category('USDC')}, UNI={token_category('UNI')}"),
        ("classify_wallet",    classify_wallet(250, 15.0, True)),
        ("chain_name(42161)",  chain_name(42161)),
        ("explorer_url",       get_explorer_url(1, tx_hash=tx[:20] + "...")),
        ("pnl",                str(pnl(10_000, 12_500))),
        ("apy_to_apr",         f"{apy_to_apr(12.68):.2f}% APR"),
        ("fmt_large",          fmt_large(5_800_000_000)),
        ("fmt_hash short",     fmt_hash(tx, "short")),
    ]

    for label, result in tests:
        print(f"  {label:<25} → {result}")

    print("-" * 45)
    print("All checks passed ✓")
