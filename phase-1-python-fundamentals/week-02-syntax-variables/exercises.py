"""
Week 2 Exercises — Syntax, Variables & Data Types
Python for Blockchain Analytics | Phase 1

Instructions:
- Work through each exercise in order
- Write your solution below the # YOUR CODE HERE comment
- Check your answer against the # Solution: section below each exercise
- Run this file with: python3 exercises.py

Don't peek at the solution before trying! Struggling is how you learn.
"""

print("=" * 60)
print("WEEK 2 EXERCISES — Syntax, Variables & Data Types")
print("=" * 60)

# ─────────────────────────────────────────────────────────────
# EXERCISE 1 — Variable assignment
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 1: Variable assignment ──")
"""
Create four variables to describe a token:
  - token_name: "Uniswap"
  - token_symbol: "UNI"
  - total_supply: 1_000_000_000   (1 billion, as an integer)
  - circulating_supply_pct: 75.4  (percentage as a float)

Then print them all in one line using an f-string:
  "UNI | Uniswap | Supply: 1,000,000,000 | Circulating: 75.4%"
"""

# YOUR CODE HERE
token_name = "Uniswap"
token_symbol = "UNI"
total_supply = 1_000_000_000
circulating_supply_pct = 75.4

print(f"{token_symbol} | {token_name} | Supply: {total_supply:,} | Circulating: {circulating_supply_pct}%")

# Solution:
# token_name = "Uniswap"
# token_symbol = "UNI"
# total_supply = 1_000_000_000
# circulating_supply_pct = 75.4
# print(f"{token_symbol} | {token_name} | Supply: {total_supply:,} | Circulating: {circulating_supply_pct}%")


# ─────────────────────────────────────────────────────────────
# EXERCISE 2 — Data types
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 2: Identify and use data types ──")
"""
Given these five values, print the type of each using type():
  19_847_293
  "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
  3247.85
  True
  "USDC"

Expected output (one line per value):
  <class 'int'>
  <class 'str'>
  <class 'float'>
  <class 'bool'>
  <class 'str'>
"""

# YOUR CODE HERE
print(type(19_847_293))
print(type("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"))
print(type(3247.85))
print(type(True))
print(type("USDC"))

# Solution:
# print(type(19_847_293))
# print(type("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"))
# print(type(3247.85))
# print(type(True))
# print(type("USDC"))


# ─────────────────────────────────────────────────────────────
# EXERCISE 3 — Wei to ETH conversion
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 3: Wei to ETH conversion ──")
"""
A Uniswap swap event recorded these values (all in Wei, as integers):
  amount_in_wei  = 2_847_000_000_000_000_000
  amount_out_wei = 9_241_500_000_000_000_000_000  <- this is a token with 18 decimals

Convert both to their human-readable values (divide by 10**18).
Then print:
  "Swapped: 2.847000 ETH → 9241.500000 TOKEN"

Tip: use :.6f in your f-string for 6 decimal places.
"""

# YOUR CODE HERE
amount_in_wei  = 2_847_000_000_000_000_000
amount_out_wei = 9_241_500_000_000_000_000_000

amount_in  = amount_in_wei / 10**18
amount_out = amount_out_wei / 10**18

print(f"Swapped: {amount_in:.6f} ETH → {amount_out:.6f} TOKEN")

# Solution:
# amount_in  = amount_in_wei / 10**18
# amount_out = amount_out_wei / 10**18
# print(f"Swapped: {amount_in:.6f} ETH → {amount_out:.6f} TOKEN")


# ─────────────────────────────────────────────────────────────
# EXERCISE 4 — String operations
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 4: String operations ──")
"""
Given this wallet address:
  address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"

Do all of the following:
  1. Print the length of the address
  2. Print whether it starts with "0x"
  3. Print a shortened version: first 6 chars + "..." + last 4 chars
     Expected: "0xd8dA...6045"
  4. Print the address in all lowercase
  5. Print whether the address equals itself in lowercase (hint: use .lower())
"""

# YOUR CODE HERE
address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"

print(len(address))
print(address.startswith("0x"))
print(f"{address[:6]}...{address[-4:]}")
print(address.lower())
print(address.lower() == address.lower())

# Solution:
# print(len(address))                            # 42
# print(address.startswith("0x"))                # True
# print(f"{address[:6]}...{address[-4:]}")       # 0xd8dA...6045
# print(address.lower())
# print(address.lower() == address.lower())      # True


# ─────────────────────────────────────────────────────────────
# EXERCISE 5 — Type casting from API response
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 5: Type casting from API response ──")
"""
This is a real-world scenario. Etherscan returns all values as strings.
Cast each field to the correct type and compute the gas cost in ETH.

raw = {
    "blockNumber": "19847293",
    "gasUsed": "84_523",          <- note: no underscores in real API
    "gasPrice": "15000000000",    <- in Wei
    "isError": "0"                <- "0" = no error, "1" = error
}

After casting:
  - block_number should be int
  - gas_used should be int
  - gas_price should be int
  - had_error should be bool (True if isError == "1", else False)
  - gas_cost_eth should be float: (gas_used * gas_price) / 10**18

Print:
  "Block 19,847,293 | Gas: 84,523 units @ 15 Gwei | Cost: 0.00126785 ETH | Error: False"
"""

# YOUR CODE HERE
raw = {
    "blockNumber": "19847293",
    "gasUsed": "84523",
    "gasPrice": "15000000000",
    "isError": "0"
}

block_number  = int(raw["blockNumber"])
gas_used      = int(raw["gasUsed"])
gas_price     = int(raw["gasPrice"])
had_error     = raw["isError"] == "1"
gas_cost_eth  = (gas_used * gas_price) / 10**18
gas_price_gwei = gas_price // 10**9

print(f"Block {block_number:,} | Gas: {gas_used:,} units @ {gas_price_gwei} Gwei | Cost: {gas_cost_eth:.8f} ETH | Error: {had_error}")

# Solution:
# block_number   = int(raw["blockNumber"])
# gas_used       = int(raw["gasUsed"])
# gas_price      = int(raw["gasPrice"])
# had_error      = raw["isError"] == "1"
# gas_cost_eth   = (gas_used * gas_price) / 10**18
# gas_price_gwei = gas_price // 10**9
# print(f"Block {block_number:,} | Gas: {gas_used:,} units @ {gas_price_gwei} Gwei | Cost: {gas_cost_eth:.8f} ETH | Error: {had_error}")


# ─────────────────────────────────────────────────────────────
# EXERCISE 6 — Portfolio value calculator
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 6: Portfolio calculator ──")
"""
Calculate the total USD value of this DeFi portfolio:

  eth_amount  = 3.75         (ETH)
  btc_amount  = 0.12         (BTC)
  usdc_amount = 4_250.00     (USDC — already in USD)
  uni_amount  = 850          (UNI tokens)

Current prices:
  eth_price_usd  = 3247.85
  btc_price_usd  = 67_412.00
  uni_price_usd  = 12.84

Print a portfolio summary like this:
  ┌─────────────────────────────────┐
  │        PORTFOLIO SUMMARY        │
  ├─────────────────────────────────┤
  │  ETH   3.7500  →  $12,179.44   │
  │  BTC   0.1200  →   $8,089.44   │
  │  USDC  4250.00 →   $4,250.00   │
  │  UNI   850     →  $10,914.00   │
  ├─────────────────────────────────┤
  │  TOTAL          →  $35,432.88  │
  └─────────────────────────────────┘

Note: the exact spacing doesn't need to match — focus on the values being correct.
"""

# YOUR CODE HERE
eth_amount   = 3.75
btc_amount   = 0.12
usdc_amount  = 4_250.00
uni_amount   = 850

eth_price_usd  = 3247.85
btc_price_usd  = 67_412.00
uni_price_usd  = 12.84

eth_value  = eth_amount  * eth_price_usd
btc_value  = btc_amount  * btc_price_usd
usdc_value = usdc_amount
uni_value  = uni_amount  * uni_price_usd
total      = eth_value + btc_value + usdc_value + uni_value

print("┌─────────────────────────────────┐")
print("│        PORTFOLIO SUMMARY        │")
print("├─────────────────────────────────┤")
print(f"│  ETH   {eth_amount:.4f}  →  ${eth_value:>10,.2f}   │")
print(f"│  BTC   {btc_amount:.4f}  →   ${btc_value:>9,.2f}   │")
print(f"│  USDC  {usdc_amount:.2f} →   ${usdc_value:>9,.2f}   │")
print(f"│  UNI   {uni_amount:<7}  →  ${uni_value:>10,.2f}   │")
print("├─────────────────────────────────┤")
print(f"│  TOTAL           →  ${total:>10,.2f}  │")
print("└─────────────────────────────────┘")

# Solution: see above — multiple valid approaches


# ─────────────────────────────────────────────────────────────
# EXERCISE 7 — Address validator
# ─────────────────────────────────────────────────────────────
print("\n── Exercise 7: Wallet address validator ──")
"""
Write validation logic for these four addresses.
For each one, check:
  1. Does it start with "0x"?
  2. Is it exactly 42 characters long?
  3. Are all characters after "0x" valid hex? (0-9 and a-f/A-F only)

An address is valid if ALL THREE checks pass.

Hint for check 3: after slicing off "0x", try:
  all(c in "0123456789abcdefABCDEF" for c in hex_part)
  (We'll cover loops properly in Week 3 — for now, just use this pattern as-is)

Addresses to check:
  a = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"   <- valid
  b = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA9604"    <- too short (41 chars)
  c = "d8dA6BF26964aF9D7eEd9e03E53415D37aA96045xx"   <- no 0x prefix
  d = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA9604Z"   <- invalid character Z

Print: "0xd8dA...6045 → Valid: True"  (shortened address + result)
"""

# YOUR CODE HERE
addresses = [
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA9604",
    "d8dA6BF26964aF9D7eEd9e03E53415D37aA96045xx",
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA9604Z",
]

hex_chars = "0123456789abcdefABCDEF"

for addr in addresses:
    has_prefix    = addr.startswith("0x")
    correct_len   = len(addr) == 42
    hex_part      = addr[2:] if has_prefix else addr
    valid_chars   = all(c in hex_chars for c in hex_part)
    is_valid      = has_prefix and correct_len and valid_chars
    short         = f"{addr[:6]}...{addr[-4:]}"
    print(f"{short} → Valid: {is_valid}")

# Solution:
# hex_chars = "0123456789abcdefABCDEF"
# for addr in addresses:
#     has_prefix  = addr.startswith("0x")
#     correct_len = len(addr) == 42
#     hex_part    = addr[2:] if has_prefix else addr
#     valid_chars = all(c in hex_chars for c in hex_part)
#     is_valid    = has_prefix and correct_len and valid_chars
#     short       = f"{addr[:6]}...{addr[-4:]}"
#     print(f"{short} → Valid: {is_valid}")


# ─────────────────────────────────────────────────────────────
# CHALLENGE EXERCISE — Full transaction receipt formatter
# ─────────────────────────────────────────────────────────────
print("\n── Challenge: Full Transaction Receipt ──")
"""
This is the mini-project from the lesson, with one addition.

Take this raw transaction, parse it, and display a formatted receipt
that also shows:
  - Total cost = value + gas cost (in ETH and USD)
  - A "savings vs peak gas" note if gas_price < 50 gwei
    (peak is assumed to be 50 gwei = 50_000_000_000 wei)

raw_tx = {
    "hash": "0x5c504ed432cb51138bcf09aa5e8a410dd4a1e204ef84bfed1be16dfba1b22060",
    "from": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
    "to": "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
    "value": "1500000000000000000",
    "gasUsed": "21000",
    "gasPrice": "20000000000",
    "blockNumber": "19847293",
    "status": "1"
}
eth_price_usd = 3247.85
"""

# YOUR CODE HERE
raw_tx = {
    "hash": "0x5c504ed432cb51138bcf09aa5e8a410dd4a1e204ef84bfed1be16dfba1b22060",
    "from": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
    "to": "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
    "value": "1500000000000000000",
    "gasUsed": "21000",
    "gasPrice": "20000000000",
    "blockNumber": "19847293",
    "status": "1"
}
eth_price_usd = 3247.85

tx_hash      = raw_tx["hash"]
sender       = raw_tx["from"]
receiver     = raw_tx["to"]
value_wei    = int(raw_tx["value"])
gas_used     = int(raw_tx["gasUsed"])
gas_price    = int(raw_tx["gasPrice"])
block_number = int(raw_tx["blockNumber"])
success      = raw_tx["status"] == "1"

value_eth    = value_wei / 10**18
gas_cost_wei = gas_used * gas_price
gas_cost_eth = gas_cost_wei / 10**18
total_eth    = value_eth + gas_cost_eth
value_usd    = value_eth * eth_price_usd
gas_usd      = gas_cost_eth * eth_price_usd
total_usd    = total_eth * eth_price_usd
gas_gwei     = gas_price // 10**9
status_label = "✅ Success" if success else "❌ Failed"

peak_gwei    = 50
savings_pct  = ((peak_gwei - gas_gwei) / peak_gwei) * 100
savings_note = f"⚡ You saved {savings_pct:.0f}% vs peak ({peak_gwei} Gwei)" if gas_gwei < peak_gwei else ""

print("=" * 57)
print("          ETHEREUM TRANSACTION RECEIPT")
print("=" * 57)
print(f"  Status      : {status_label}")
print(f"  Block       : {block_number:,}")
print(f"  Tx Hash     : {tx_hash[:10]}...{tx_hash[-8:]}")
print(f"  From        : {sender[:10]}...{sender[-6:]}")
print(f"  To          : {receiver[:10]}...{receiver[-6:]}")
print("-" * 57)
print(f"  Value       : {value_eth:.6f} ETH  (${value_usd:>10,.2f})")
print(f"  Gas Used    : {gas_used:,} units @ {gas_gwei} Gwei")
print(f"  Gas Cost    : {gas_cost_eth:.8f} ETH  (${gas_usd:>8,.4f})")
print("-" * 57)
print(f"  TOTAL COST  : {total_eth:.6f} ETH  (${total_usd:>10,.2f})")
if savings_note:
    print(f"  {savings_note}")
print("=" * 57)

print("\n" + "=" * 60)
print("All exercises complete! Commit your work:")
print("  git add phase-1-python-fundamentals/week-02-syntax-variables/")
print('  git commit -m "phase-1/week-02: completed exercises"')
print("  git push")
print("=" * 60)
