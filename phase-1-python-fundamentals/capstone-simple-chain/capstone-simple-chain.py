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
import hashlib
import time as time_module
class ChainTxn:
    def __init__(self, from_addr, to_addr, amount) -> None:
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.amount = amount
        self.timestamp = int(time_module.time())

    @property
    def tx_hash(self):
        raw=f"{self.from_addr}{self.to_addr}{self.amount}{self.timestamp}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def __str__(self):
            return f"{self.from_addr} → {self.to_addr} | {self.amount} ETH"

class ChainBlock:
    def __init__(self, index, previous_hash, transactions) -> None:
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = int(time_module.time())

    @property
    def block_hash(self):
        tx_hashes = ''.join(tx.tx_hash for tx in self.transactions)
        raw=f"{self.index}{self.previous_hash}{tx_hashes}{self.timestamp}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def is_valid(self):
        return self.block_hash.startswith("00")

    def __str__(self):
        return f"Block #{self.index} | {len(self.transactions)} txns | hash: {self.block_hash[:10]}..."

class SimpleBlockchain:
    def __init__(self):
        genesis_block = ChainBlock(0, "0"*64, [])
        self.chain = [genesis_block]
        self.pending_transactions = []

    def add_transaction(self, from_addr, to_addr, amount):
        txn = ChainTxn(from_addr, to_addr, amount)
        self.pending_transactions.append(txn)

    def mine_block(self):
        index = len(self.chain)
        previous_hash = self.chain[-1].block_hash
        new_block = ChainBlock(index, previous_hash, self.pending_transactions)
        self.chain.append(new_block)
        self.pending_transactions = []

    def is_valid_chain(self):
        for i in range(1, len(self.chain)):
            if self.chain[i].previous_hash != self.chain[i-1].block_hash:
                return False
        return True

    def get_balance(self, address):
        balance = 0.0
        for block in self.chain:
            for txn in block.transactions:
                if txn.to_addr == address:
                    balance += txn.amount
                if txn.from_addr == address:
                    balance -= txn.amount
        return balance

    def __len__(self):
        return len(self.chain)

    def __str__(self):
        return f"Blockchain: {len(self.chain)} blocks | valid: {self.is_valid_chain()}"

# TESTS
bc = SimpleBlockchain()
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

print()
print(f"  {bc}")


print("\n" + "=" * 60)
print("Capstone Project Done! Check exercises_solutions.py to compare.")
print("Phase 1 complete — 6 weeks of Python foundations!")
print("=" * 60)
