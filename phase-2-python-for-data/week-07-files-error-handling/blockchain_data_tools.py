"""
blockchain_data_tools.py
Blockchain Data Engineering — Tools Reference & Quick-Start Guide

A comprehensive reference for every major blockchain data tool
a Blockchain Data Engineer needs to know.

Organised by category:
  1. RPC Node Providers        — direct blockchain access
  2. REST API Data Providers   — price, market, on-chain data
  3. Indexing Frameworks       — index events, build queryable APIs
  4. GraphQL Protocol Indexers — The Graph and alternatives
  5. Real-time / Streaming     — live event pipelines
  6. Multi-chain Analytics     — cross-chain data platforms
  7. Wallet & Address Intel    — labelling, clustering
  8. Python Libraries          — code-level access

All free tiers and open-source options are clearly marked.
Every tool section includes: what it does, when to use it,
free tier info, and the API pattern you'll use in Python.
"""

# ══════════════════════════════════════════════════════════════
# 1. RPC NODE PROVIDERS
# ══════════════════════════════════════════════════════════════

RPC_PROVIDERS = {

    # ── Fully free, no signup ─────────────────────────────────
    "ankr_public": {
        "name":        "Ankr Public RPC",
        "website":     "https://www.ankr.com/rpc/",
        "free_tier":   "Unlimited, no key, no signup",
        "rate_limit":  "30 requests/sec",
        "chains":      ["ethereum", "polygon", "bsc", "arbitrum", "optimism",
                        "base", "avalanche", "fantom", "celo", "gnosis"],
        "use_when":    "Development, prototyping, low-volume scripts",
        "limitation":  "No archive data, rate limited under load",
        "endpoints": {
            "ethereum":  "https://rpc.ankr.com/eth",
            "polygon":   "https://rpc.ankr.com/polygon",
            "arbitrum":  "https://rpc.ankr.com/arbitrum",
            "base":      "https://rpc.ankr.com/base",
            "optimism":  "https://rpc.ankr.com/optimism",
            "bsc":       "https://rpc.ankr.com/bsc",
            "avalanche": "https://rpc.ankr.com/avalanche",
        },
        "python_example": """
import requests

def eth_block_number(rpc_url="https://rpc.ankr.com/eth"):
    payload = {"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}
    r = requests.post(rpc_url, json=payload)
    return int(r.json()["result"], 16)

print(eth_block_number())
""",
    },

    "llamanodes": {
        "name":       "LlamaNodes",
        "website":    "https://llamanodes.com",
        "free_tier":  "Free public endpoints, no key",
        "chains":     ["ethereum", "polygon", "arbitrum", "optimism", "base"],
        "use_when":   "Backup RPC when Ankr is congested",
        "endpoints": {
            "ethereum": "https://eth.llamarpc.com",
            "polygon":  "https://polygon.llamarpc.com",
            "arbitrum": "https://arbitrum.llamarpc.com",
        },
    },

    # ── Free tier with key ────────────────────────────────────
    "infura": {
        "name":       "Infura",
        "website":    "https://infura.io",
        "free_tier":  "100,000 requests/day — free signup",
        "key_env":    "INFURA_API_KEY",
        "signup":     "https://app.infura.io/register",
        "chains":     ["ethereum", "polygon", "arbitrum", "optimism",
                       "linea", "base", "starknet", "solana"],
        "use_when":   "Reliable production-grade RPC access without hosting your own node",
        "strengths":  "Archive data, HTTPS + WSS, eth_getLogs, trace calls",
        "endpoints": {
            "ethereum_mainnet": "https://mainnet.infura.io/v3/{API_KEY}",
            "ethereum_wss":     "wss://mainnet.infura.io/ws/v3/{API_KEY}",
            "polygon":          "https://polygon-mainnet.infura.io/v3/{API_KEY}",
            "arbitrum":         "https://arbitrum-mainnet.infura.io/v3/{API_KEY}",
            "optimism":         "https://optimism-mainnet.infura.io/v3/{API_KEY}",
            "base":             "https://base-mainnet.infura.io/v3/{API_KEY}",
        },
        "python_example": """
import os, requests

INFURA_KEY = os.environ.get("INFURA_API_KEY", "demo")
BASE_URL   = f"https://mainnet.infura.io/v3/{INFURA_KEY}"

def get_balance(address):
    payload = {
        "jsonrpc": "2.0",
        "method":  "eth_getBalance",
        "params":  [address, "latest"],
        "id":      1,
    }
    r = requests.post(BASE_URL, json=payload)
    wei = int(r.json()["result"], 16)
    return wei / 1e18

print(get_balance("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"))
""",
    },

    "alchemy": {
        "name":       "Alchemy",
        "website":    "https://www.alchemy.com",
        "free_tier":  "300M compute units/month — free signup",
        "key_env":    "ALCHEMY_API_KEY",
        "signup":     "https://auth.alchemy.com/signup",
        "chains":     ["ethereum", "polygon", "arbitrum", "optimism",
                       "base", "starknet", "astar", "solana"],
        "use_when":   "Enhanced APIs (NFT, token balances), webhooks, production",
        "strengths":  "alchemy_getAssetTransfers, alchemy_getTokenBalances, Notify webhooks",
        "python_example": """
import os, requests

ALCHEMY_KEY = os.environ.get("ALCHEMY_API_KEY", "demo")
BASE_URL = f"https://eth-mainnet.g.alchemy.com/v2/{ALCHEMY_KEY}"

# Alchemy Enhanced API — get all token transfers for an address
def get_asset_transfers(address, from_block="0x0"):
    payload = {
        "id": 1, "jsonrpc": "2.0",
        "method": "alchemy_getAssetTransfers",
        "params": [{
            "fromBlock": from_block,
            "toAddress": address,
            "category": ["erc20", "erc721", "erc1155"],
            "withMetadata": True,
        }]
    }
    r = requests.post(BASE_URL, json=payload)
    return r.json()["result"]["transfers"]
""",
    },

    "quicknode": {
        "name":       "QuickNode",
        "website":    "https://www.quicknode.com",
        "free_tier":  "15M API credits/month — free signup",
        "key_env":    "QUICKNODE_ENDPOINT",
        "chains":     ["ethereum", "solana", "polygon", "bsc", "arbitrum",
                       "optimism", "base", "avalanche", "near", "aptos"],
        "use_when":   "Solana + EVM in one platform, stream subscriptions",
        "strengths":  "Solana support, Streams (real-time data), add-ons marketplace",
    },
}


# ══════════════════════════════════════════════════════════════
# 2. REST API DATA PROVIDERS
# ══════════════════════════════════════════════════════════════

REST_PROVIDERS = {

    "defillama": {
        "name":       "DefiLlama",
        "website":    "https://defillama.com",
        "free_tier":  "Completely free, no key, no signup",
        "rate_limit": "Very generous",
        "what_it_has": [
            "TVL for 3000+ protocols across 100+ chains",
            "Historical TVL time series",
            "Yield/APY data for DeFi pools",
            "Stablecoin supply and peg data",
            "DEX volume data",
            "Protocol revenue and fees",
            "Chain-level TVL breakdown",
            "Bridges volume data",
        ],
        "base_url":   "https://api.llama.fi",
        "key_endpoints": {
            "all_protocols":     "GET /protocols",
            "protocol_detail":   "GET /protocol/{slug}",
            "protocol_tvl":      "GET /tvl/{slug}",
            "all_chains":        "GET /v2/chains",
            "yield_pools":       "GET https://yields.llama.fi/pools",
            "stablecoins":       "GET https://stablecoins.llama.fi/stablecoins",
            "dex_volume":        "GET https://api.llama.fi/overview/dexs",
            "fees_revenue":      "GET https://api.llama.fi/overview/fees",
        },
        "python_example": """
import requests

def get_top_protocols_by_tvl(n=10):
    r = requests.get("https://api.llama.fi/protocols")
    protocols = r.json()
    sorted_p = sorted(protocols, key=lambda p: p.get("tvl", 0), reverse=True)
    return sorted_p[:n]

for p in get_top_protocols_by_tvl():
    print(f"{p['name']:20} ${p['tvl']/1e9:.2f}B")
""",
    },

    "coingecko": {
        "name":       "CoinGecko",
        "website":    "https://www.coingecko.com/api/documentation",
        "free_tier":  "No key needed for basic endpoints, 30 calls/min",
        "key_env":    "COINGECKO_API_KEY",
        "what_it_has": [
            "Token prices in 100+ currencies",
            "Historical OHLCV data",
            "Market cap and volume",
            "Token metadata (description, links, socials)",
            "Exchange data",
            "NFT floor prices",
            "On-chain DEX data (GeckoTerminal)",
        ],
        "base_url":   "https://api.coingecko.com/api/v3",
        "key_endpoints": {
            "markets":      "GET /coins/markets?vs_currency=usd",
            "price":        "GET /simple/price?ids={id}&vs_currencies=usd",
            "history":      "GET /coins/{id}/market_chart?vs_currency=usd&days={days}",
            "token_info":   "GET /coins/{id}",
            "ohlcv":        "GET /coins/{id}/ohlc?vs_currency=usd&days={days}",
        },
        "python_example": """
import requests

BASE = "https://api.coingecko.com/api/v3"

def get_prices(coin_ids: list) -> dict:
    ids = ",".join(coin_ids)
    r = requests.get(f"{BASE}/simple/price?ids={ids}&vs_currencies=usd")
    return {k: v["usd"] for k, v in r.json().items()}

prices = get_prices(["ethereum", "bitcoin", "uniswap", "aave"])
for token, price in prices.items():
    print(f"  {token:12} ${price:>12,.2f}")
""",
    },

    "etherscan": {
        "name":       "Etherscan",
        "website":    "https://etherscan.io/apis",
        "free_tier":  "5 calls/sec, free API key (30 second signup)",
        "key_env":    "ETHERSCAN_API_KEY",
        "signup":     "https://etherscan.io/register",
        "variants": {
            "ethereum":  "https://api.etherscan.io/api",
            "polygon":   "https://api.polygonscan.com/api",
            "arbitrum":  "https://api.arbiscan.io/api",
            "optimism":  "https://api-optimistic.etherscan.io/api",
            "base":      "https://api.basescan.org/api",
            "bsc":       "https://api.bscscan.com/api",
        },
        "what_it_has": [
            "Transaction history for any address",
            "ERC-20/721/1155 token transfers",
            "ETH/token balances",
            "Contract ABI and source code",
            "Internal transactions",
            "Block and uncle data",
            "Gas oracle (fee estimates)",
            "Event logs",
        ],
        "python_example": """
import os, requests

def get_wallet_txns(address, api_key=None, chain="ethereum"):
    key = api_key or os.environ.get("ETHERSCAN_API_KEY", "demo")
    base = "https://api.etherscan.io/api"
    params = {
        "module": "account", "action": "txlist",
        "address": address,  "startblock": 0,
        "endblock": 99999999,"sort": "desc",
        "apikey": key,
    }
    r = requests.get(base, params=params)
    data = r.json()
    if data["status"] != "1":
        raise Exception(f"Etherscan error: {data['message']}")
    return data["result"]

txns = get_wallet_txns("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045")
print(f"Found {len(txns)} transactions")
""",
    },
}


# ══════════════════════════════════════════════════════════════
# 3. BLOCKCHAIN INDEXING FRAMEWORKS
# ══════════════════════════════════════════════════════════════

INDEXING_FRAMEWORKS = {

    "envio": {
        "name":        "Envio",
        "website":     "https://envio.dev",
        "github":      "https://github.com/enviodev/hyperindex",
        "free_tier":   "Open source + generous hosted free tier",
        "what_it_does": """
Envio is a modern blockchain indexing framework built for speed.
It lets you define event handlers in JavaScript/TypeScript or ReScript,
and automatically indexes smart contract events into a PostgreSQL database
exposed via GraphQL.

Key advantages over The Graph:
  - Much faster sync times (10-100x on some chains)
  - Local development with instant feedback
  - Multi-chain in a single indexer
  - No need to understand WASM or AssemblyScript
  - HyperSync for ultra-fast historical data retrieval
""",
        "chains":      ["ethereum", "polygon", "arbitrum", "optimism", "base",
                        "bsc", "avalanche", "gnosis", "celo", "linea", "zksync",
                        "scroll", "blast", "mode", "zora", "mantle"],
        "use_when":    "Building custom DeFi analytics, protocol dashboards, faster than The Graph",
        "key_concepts": {
            "HyperIndex": "The indexer engine — processes events and writes to Postgres",
            "HyperSync":  "Ultra-fast data retrieval layer (replaces standard RPC for historical data)",
            "config.yaml":"Defines which contracts and events to index",
            "EventHandlers":"JavaScript/TypeScript functions called for each event",
        },
        "install":     "npx create-envio-app@latest",
        "python_access": "Query the generated GraphQL API from Python using requests or gql",
        "python_example": """
import requests

# After deploying your Envio indexer, query its GraphQL API from Python
ENVIO_GRAPHQL = "https://your-indexer.hyperindex.xyz/v1/graphql"

def query_swaps(limit=10):
    query = \"\"\"
    query GetSwaps($limit: Int!) {
        Swap(limit: $limit, order_by: {block_number: desc}) {
            id
            token0_symbol
            token1_symbol
            amount0
            amount1
            block_number
            timestamp
        }
    }
    \"\"\"
    r = requests.post(ENVIO_GRAPHQL,
                      json={"query": query, "variables": {"limit": limit}})
    return r.json()["data"]["Swap"]
""",
        "config_example": """
# config.yaml — index Uniswap V3 Swap events
name: uniswap-v3-indexer
description: Index Uniswap V3 swaps across chains

networks:
  - id: 1
    start_block: 12369621
    contracts:
      - name: UniswapV3Pool
        abi_file_path: abis/UniswapV3Pool.json
        address:
          - 0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640
        handler: src/EventHandlers.js
        events:
          - event: Swap(address,address,int256,int256,uint160,uint128,int24)
""",
    },

    "subgraph_the_graph": {
        "name":        "The Graph — Subgraphs",
        "website":     "https://thegraph.com",
        "github":      "https://github.com/graphprotocol/graph-node",
        "free_tier":   "Hosted service free tier + decentralised network",
        "what_it_does": """
The Graph is the industry standard for indexing blockchain data.
You define a 'subgraph' — a YAML manifest + AssemblyScript handlers —
and it automatically indexes events from smart contracts into a
queryable GraphQL API.

Thousands of subgraphs exist for major protocols (Uniswap, Aave, Compound,
Curve, etc.) — you can query them immediately without building your own.

Two ways to use it:
  1. Query EXISTING subgraphs (no code needed — just GraphQL)
  2. Build your OWN subgraph for custom protocols
""",
        "chains":      ["ethereum", "polygon", "arbitrum", "optimism", "celo",
                        "bsc", "gnosis", "avalanche", "base", "fantom",
                        "moonbeam", "near", "arweave", "cosmos"],
        "use_when":    "Querying existing protocol data (Uniswap, Aave), building protocol indexers",
        "existing_subgraphs": {
            "uniswap_v3":  "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3",
            "uniswap_v2":  "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2",
            "aave_v3":     "https://api.thegraph.com/subgraphs/name/aave/protocol-v3",
            "compound_v3": "https://api.thegraph.com/subgraphs/name/graphprotocol/compound-v3",
            "curve":       "https://api.thegraph.com/subgraphs/name/convex-community/volume-ethereum",
            "balancer_v2": "https://api.thegraph.com/subgraphs/name/balancer-labs/balancer-v2",
            "lido":        "https://api.thegraph.com/subgraphs/name/lidofinance/lido",
        },
        "python_example": """
import requests

def query_subgraph(endpoint: str, query: str, variables: dict = None) -> dict:
    \"\"\"Execute a GraphQL query against any subgraph.\"\"\"
    r = requests.post(endpoint,
                      json={"query": query, "variables": variables or {}},
                      headers={"Content-Type": "application/json"})
    r.raise_for_status()
    result = r.json()
    if "errors" in result:
        raise Exception(f"GraphQL errors: {result['errors']}")
    return result["data"]

# Query Uniswap V3 — no API key needed
UNISWAP_V3 = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"

top_pools_query = \"\"\"
{
    pools(first: 5, orderBy: totalValueLockedUSD, orderDirection: desc) {
        id
        token0 { symbol }
        token1 { symbol }
        feeTier
        totalValueLockedUSD
        volumeUSD
    }
}
\"\"\"

data = query_subgraph(UNISWAP_V3, top_pools_query)
for pool in data["pools"]:
    pair = f"{pool['token0']['symbol']}/{pool['token1']['symbol']}"
    tvl  = float(pool["totalValueLockedUSD"])
    print(f"  {pair:12} TVL: ${tvl/1e6:.1f}M | Fee: {pool['feeTier']}bp")
""",
        "build_your_own": """
# To build your own subgraph:
# 1. Install Graph CLI:    npm install -g @graphprotocol/graph-cli
# 2. Initialise:          graph init --product hosted-service your-subgraph
# 3. Define schema.graphql (your data types)
# 4. Define subgraph.yaml (which contracts + events to index)
# 5. Write src/mappings.ts (AssemblyScript event handlers)
# 6. Deploy:              graph deploy --product hosted-service your-subgraph
""",
    },

    "ponder": {
        "name":        "Ponder",
        "website":     "https://ponder.sh",
        "github":      "https://github.com/ponder-sh/ponder",
        "free_tier":   "Fully open source, self-hosted",
        "what_it_does": """
Ponder is an open-source framework for building blockchain indexer APIs
using TypeScript. Unlike The Graph (WASM/AssemblyScript), Ponder lets you
write familiar TypeScript and runs locally with hot reloading.

It syncs contract events to a local database and serves them via
a REST or GraphQL API you define.
""",
        "chains":      ["any EVM chain with an RPC endpoint"],
        "use_when":    "TypeScript-first teams, local development, custom REST APIs",
        "install":     "npm create ponder@latest",
        "python_access": "Query the generated REST/GraphQL API from Python",
    },

    "hyperindex": {
        "name":        "HyperIndex (Envio)",
        "website":     "https://docs.envio.dev/docs/HyperIndex/overview",
        "what_it_does": """
HyperIndex is Envio's core indexing engine — the runtime that powers
the Envio framework (see 'envio' above). It's worth knowing as a separate
concept because you'll see it referenced in the Envio documentation.

HyperIndex uses HyperSync under the hood for extremely fast historical
data retrieval, making it orders of magnitude faster than indexers
that rely purely on JSON-RPC calls.

For practical purposes: when you use Envio, you're using HyperIndex.
""",
        "python_access": "Through Envio's GraphQL output layer",
    },

    "subsquid": {
        "name":        "Subsquid (SQD)",
        "website":     "https://subsquid.io",
        "github":      "https://github.com/subsquid/squid-sdk",
        "free_tier":   "Open source + free hosted tiers",
        "what_it_does": """
Subsquid is a decentralised data lake and indexing framework.
It stores raw blockchain data in a decentralised network of nodes
and lets you build 'squids' (indexers) that query this data lake
and serve it via GraphQL or REST.

Significantly faster than building on raw RPC because the data lake
pre-processes raw chain data.
""",
        "chains":      ["ethereum", "polygon", "bsc", "arbitrum", "optimism",
                        "avalanche", "moonbeam", "acala", "substrate chains"],
        "use_when":    "Building fast EVM + Substrate/Polkadot indexers",
        "install":     "npm install -g @subsquid/cli",
    },

    "goldsky": {
        "name":        "Goldsky",
        "website":     "https://goldsky.com",
        "free_tier":   "Free tier available",
        "what_it_does": """
Goldsky is a managed indexing platform that handles subgraph deployment
and real-time streaming. Two main products:
  - Subgraphs: hosted Graph-compatible subgraphs with better performance
  - Mirror: stream indexed data directly to your own database (Postgres, Redis, Kafka)

Mirror is especially powerful for data engineers — it streams indexed
blockchain events directly into your existing data warehouse.
""",
        "use_when":    "Production subgraphs with SLAs, streaming into your own database",
    },
}


# ══════════════════════════════════════════════════════════════
# 4. PYTHON BLOCKCHAIN LIBRARIES
# ══════════════════════════════════════════════════════════════

PYTHON_LIBRARIES = {

    "web3py": {
        "name":        "web3.py",
        "install":     "pip install web3",
        "docs":        "https://web3py.readthedocs.io",
        "github":      "https://github.com/ethereum/web3.py",
        "what_it_does": """
web3.py is THE Python library for interacting with Ethereum-compatible blockchains.
It's the Python equivalent of ethers.js.

Use it to:
  - Read blockchain state (balances, contract storage)
  - Decode event logs using ABIs
  - Call read-only contract functions
  - Send transactions (requires private key)
  - Subscribe to events via WebSocket
  - Interact with ENS (Ethereum Name Service)

In this course we use it heavily in Phase 3 (Blockchain Analytics).
""",
        "key_objects": {
            "w3.eth.get_block(n)":           "Fetch a block with all transactions",
            "w3.eth.get_transaction(hash)":  "Fetch a single transaction",
            "w3.eth.get_balance(addr)":      "Get ETH balance in Wei",
            "w3.eth.get_logs(filter)":       "Fetch event logs",
            "contract.functions.X().call()": "Call a contract view function",
            "contract.events.X.process_log()":"Decode a raw log into event args",
        },
        "python_example": """
from web3 import Web3

# Connect to a free RPC
w3 = Web3(Web3.HTTPProvider("https://rpc.ankr.com/eth"))
print(f"Connected: {w3.is_connected()}")
print(f"Latest block: {w3.eth.block_number:,}")

# Read ETH balance
addr    = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
balance = w3.eth.get_balance(addr)
print(f"Balance: {w3.from_wei(balance, 'ether'):.4f} ETH")

# Read a contract (ERC-20 balanceOf)
ERC20_ABI = [{"inputs":[{"name":"account","type":"address"}],
              "name":"balanceOf","outputs":[{"name":"","type":"uint256"}],
              "type":"function","stateMutability":"view"}]

USDC_ADDRESS = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
usdc = w3.eth.contract(address=USDC_ADDRESS, abi=ERC20_ABI)
usdc_balance = usdc.functions.balanceOf(addr).call()
print(f"USDC balance: {usdc_balance / 1e6:.2f} USDC")
""",
    },

    "eth_abi": {
        "name":    "eth-abi",
        "install": "pip install eth-abi",
        "docs":    "https://eth-abi.readthedocs.io",
        "what_it_does": """
Low-level ABI encoding and decoding.
Use this when you have raw calldata or log data that you need to decode
without a full contract ABI. Useful for MEV research and raw log parsing.
""",
        "python_example": """
from eth_abi import decode

# Decode a Transfer(address,address,uint256) event log's data field
# (the 'data' field of the log — topics are decoded separately)
raw_data = bytes.fromhex("000000000000000000000000000000000000000000000000016345785d8a0000")
(amount,) = decode(["uint256"], raw_data)
print(f"Transfer amount: {amount / 1e18:.4f} ETH")
""",
    },

    "gql": {
        "name":    "gql (GraphQL client)",
        "install": "pip install gql[requests]",
        "docs":    "https://gql.readthedocs.io",
        "what_it_does": """
A typed GraphQL client for Python. Cleaner than using raw requests.post()
for GraphQL queries. Useful when querying The Graph subgraphs or Envio APIs.
""",
        "python_example": """
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

transport = RequestsHTTPTransport(
    url="https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"
)
client = Client(transport=transport, fetch_schema_from_transport=True)

query = gql(\"\"\"
    query GetTopPools {
        pools(first: 5, orderBy: totalValueLockedUSD, orderDirection: desc) {
            token0 { symbol }
            token1 { symbol }
            totalValueLockedUSD
        }
    }
\"\"\")

result = client.execute(query)
for pool in result["pools"]:
    print(f"{pool['token0']['symbol']}/{pool['token1']['symbol']}: "
          f"${float(pool['totalValueLockedUSD'])/1e6:.1f}M")
""",
    },

    "multicall": {
        "name":    "multicall.py",
        "install": "pip install multicall",
        "docs":    "https://github.com/banteg/multicall.py",
        "what_it_does": """
Batch multiple contract calls into a single RPC request using the
Multicall3 contract. Dramatically reduces API calls when reading data
for many addresses or tokens at once.

Instead of 100 individual eth_call requests, make 1.
Critical for analytics work where you're reading data for many wallets.
""",
        "python_example": """
from multicall import Call, Multicall
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://rpc.ankr.com/eth"))

USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
wallets = ["0xAlice...", "0xBob...", "0xCarol..."]

# One RPC call for all balances
calls = [
    Call(USDC, ["balanceOf(address)(uint256)", wallet],
         [[f"balance_{wallet[:6]}", lambda x: x / 1e6]])
    for wallet in wallets
]
result = Multicall(calls, _w3=w3)()
print(result)  # {balance_0xAlic: 1000.0, balance_0xBob1: 250.5, ...}
""",
    },
}


# ══════════════════════════════════════════════════════════════
# 5. SOLANA DATA TOOLS
# ══════════════════════════════════════════════════════════════

SOLANA_TOOLS = {

    "overview": """
Solana has a completely different data model from EVM chains.
Instead of accounts with bytecode, Solana uses Programs and Accounts.
The key concepts for data engineers:

  - Programs  = smart contracts (e.g. Raydium, Orca, Jupiter)
  - Accounts  = storage (like contract storage, but account-based)
  - Instructions = individual actions within a transaction
  - Logs      = program output (parse these for events)

Solana transactions contain multiple instructions, each targeting a program.
Unlike EVM, there are no "events" — you parse program logs and account state.
""",

    "solana_rpc": {
        "name":     "Solana Public RPC",
        "endpoint": "https://api.mainnet-beta.solana.com",
        "free":     True,
        "note":     "Rate limited — use Helius or QuickNode for production",
        "python_example": """
import requests

RPC = "https://api.mainnet-beta.solana.com"

def get_slot():
    r = requests.post(RPC, json={"jsonrpc":"2.0","id":1,"method":"getSlot"})
    return r.json()["result"]

def get_sol_balance(pubkey: str) -> float:
    r = requests.post(RPC, json={
        "jsonrpc": "2.0", "id": 1,
        "method": "getBalance",
        "params": [pubkey]
    })
    lamports = r.json()["result"]["value"]
    return lamports / 1e9  # 1 SOL = 1e9 lamports

print(f"Current slot: {get_slot():,}")
""",
    },

    "helius": {
        "name":       "Helius",
        "website":    "https://helius.dev",
        "free_tier":  "Free tier: 100k credits/day",
        "key_env":    "HELIUS_API_KEY",
        "what_it_does": """
Helius is the Alchemy/Infura equivalent for Solana.
It provides enhanced RPC endpoints and data APIs specifically for Solana:
  - Enhanced transactions (parsed instruction details)
  - NFT metadata APIs
  - Webhook subscriptions for account/program changes
  - DAS (Digital Asset Standard) API for NFTs and tokens
  - Historical transaction data
""",
        "python_example": """
import os, requests

HELIUS_KEY = os.environ.get("HELIUS_API_KEY", "demo")
BASE = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_KEY}"

def get_enhanced_transactions(address: str, limit: int = 10):
    \"\"\"Get parsed Solana transactions — much more readable than raw RPC.\"\"\"
    url = f"https://api.helius.xyz/v0/addresses/{address}/transactions?api-key={HELIUS_KEY}"
    r = requests.get(url, params={"limit": limit})
    return r.json()
""",
    },

    "solscan": {
        "name":       "Solscan API",
        "website":    "https://public-api.solscan.io",
        "free_tier":  "Free public API, limited rate",
        "what_it_does": "Transaction and account data for Solana — the Etherscan equivalent",
        "python_example": """
import requests

BASE = "https://public-api.solscan.io"

def get_sol_account_tokens(address: str):
    r = requests.get(f"{BASE}/account/tokens", params={"account": address})
    return r.json()
""",
    },

    "solana_py": {
        "name":    "solders + solana-py",
        "install": "pip install solders solana",
        "docs":    "https://michaelhly.com/solana-py/",
        "what_it_does": """
solders is the low-level Rust-backed Python library for Solana data types.
solana-py wraps it with a higher-level client interface.
Together they are the web3.py equivalent for Solana.
""",
        "python_example": """
from solana.rpc.api import Client
from solders.pubkey import Pubkey

client = Client("https://api.mainnet-beta.solana.com")

# Get SOL balance
pubkey  = Pubkey.from_string("Vote111111111111111111111111111111111111111p")
balance = client.get_balance(pubkey)
sol     = balance.value / 1e9
print(f"Balance: {sol:.4f} SOL")

# Get recent block
slot = client.get_slot().value
print(f"Current slot: {slot:,}")
""",
    },
}


# ══════════════════════════════════════════════════════════════
# 6. MULTI-CHAIN ANALYTICS PLATFORMS
# ══════════════════════════════════════════════════════════════

ANALYTICS_PLATFORMS = {

    "dune_alternatives": {
        "note": "Dune Analytics free API has been sunsetted. Use these instead:",
        "alternatives": {
            "DefiLlama":   "TVL, protocol, yield data — completely free API",
            "The Graph":   "Query indexed DeFi protocol data via GraphQL — free",
            "Envio":       "Build your own fast indexer — open source + free hosted tier",
            "Flipside":    "SQL-based blockchain analytics — free tier available",
            "Allium":      "SQL + Python analytics on indexed blockchain data — free tier",
        },
    },

    "flipside": {
        "name":       "Flipside Crypto",
        "website":    "https://flipsidecrypto.xyz",
        "free_tier":  "Free tier with SQL analytics API",
        "key_env":    "FLIPSIDE_API_KEY",
        "what_it_does": """
Flipside provides a SQL interface to indexed blockchain data across
Ethereum, Polygon, Avalanche, BSC, Solana, Cosmos, and more.
Similar to the old Dune Analytics model — write SQL, get results via API.
Free tier gives you access to the API.
""",
        "python_example": """
# pip install flipside
from flipside import Flipside

sdk = Flipside(api_key="YOUR_KEY")

sql = \"\"\"
SELECT
    date_trunc('day', block_timestamp) AS day,
    COUNT(*)                            AS tx_count,
    SUM(eth_value)                      AS total_volume_eth
FROM ethereum.core.fact_transactions
WHERE block_timestamp >= CURRENT_DATE - 7
GROUP BY 1
ORDER BY 1 DESC
\"\"\"

result = sdk.query(sql)
for row in result.rows[:5]:
    print(row)
""",
    },

    "allium": {
        "name":       "Allium",
        "website":    "https://www.allium.so",
        "free_tier":  "Free tier available",
        "what_it_does": """
Allium is an enterprise-grade blockchain data platform with a Python SDK.
It provides clean, decoded blockchain data via SQL or Python directly.
Good alternative to Dune for programmatic access.
""",
    },

    "transpose": {
        "name":       "Transpose",
        "website":    "https://www.transpose.io",
        "free_tier":  "Free tier: 100k API credits/month",
        "what_it_does": """
Transpose provides SQL and REST APIs for indexed blockchain data.
Good for: NFT data, wallet history, token data, DEX trades.
""",
    },

    "nansen": {
        "name":       "Nansen",
        "website":    "https://www.nansen.ai",
        "free_tier":  "No free tier — but has a public API for some endpoints",
        "what_it_does": "Wallet labelling (500k+ labelled addresses), smart money tracking",
    },
}


# ══════════════════════════════════════════════════════════════
# 7. THE FREE DATA STACK FOR THIS COURSE
# ══════════════════════════════════════════════════════════════

FREE_STACK_FOR_COURSE = {
    "description": """
Everything you need through all 7 phases of this course.
No credit card. No paid subscription. All real production-quality tools.
""",
    "price_data":       "CoinGecko (no key) or DefiLlama",
    "protocol_tvl":     "DefiLlama (no key, most comprehensive)",
    "on_chain_txns":    "Etherscan (free key, 30 seconds to register)",
    "contract_reads":   "web3.py + Ankr/LlamaNodes RPC (no key)",
    "defi_events":      "The Graph existing subgraphs (no key)",
    "custom_indexing":  "Envio (free tier) or The Graph (hosted service free tier)",
    "solana_data":      "Helius free tier or Solscan public API",
    "multi_chain_sql":  "Flipside (free tier) as Dune alternative",
    "streaming":        "web3.py WebSocket subscription + Infura/Alchemy free tier",

    "env_vars_to_set": {
        "ETHERSCAN_API_KEY": "Free at etherscan.io/apis — takes 30 seconds",
        "INFURA_API_KEY":    "Free at app.infura.io/register — 100k req/day",
        "ALCHEMY_API_KEY":   "Free at auth.alchemy.com/signup — 300M CU/month",
        "HELIUS_API_KEY":    "Free at helius.dev — for Solana data",
    },

    "dotenv_setup": """
# .env file (add to .gitignore — NEVER commit API keys!)
ETHERSCAN_API_KEY=your_key_here
INFURA_API_KEY=your_key_here
ALCHEMY_API_KEY=your_key_here
HELIUS_API_KEY=your_key_here

# Load in Python:
# pip install python-dotenv
# from dotenv import load_dotenv; load_dotenv()
# import os; key = os.environ.get("ETHERSCAN_API_KEY")
""",
}


# ══════════════════════════════════════════════════════════════
# SELF-TEST / REFERENCE PRINT
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 65)
    print("  BLOCKCHAIN DATA TOOLS REFERENCE")
    print("=" * 65)

    print("\n  ── RPC Providers ──")
    for key, tool in RPC_PROVIDERS.items():
        tier = tool.get("free_tier", "N/A")
        print(f"  {tool['name']:<20} {tier}")

    print("\n  ── REST API Providers ──")
    for key, tool in REST_PROVIDERS.items():
        tier = tool.get("free_tier", "N/A")
        print(f"  {tool['name']:<20} {tier}")

    print("\n  ── Indexing Frameworks ──")
    for key, tool in INDEXING_FRAMEWORKS.items():
        tier = tool.get("free_tier", "N/A")
        print(f"  {tool['name']:<30} {tier}")

    print("\n  ── Python Libraries ──")
    for key, tool in PYTHON_LIBRARIES.items():
        print(f"  {tool['name']:<20} {tool['install']}")

    print("\n  ── Solana Tools ──")
    for key, tool in SOLANA_TOOLS.items():
        if isinstance(tool, dict) and "name" in tool:
            tier = tool.get("free_tier", "varies")
            print(f"  {tool['name']:<25} {tier}")

    print("\n  ── Free Stack for This Course ──")
    stack = FREE_STACK_FOR_COURSE
    for use_case, tool in stack.items():
        if use_case not in ("description", "env_vars_to_set", "dotenv_setup"):
            print(f"  {use_case:<20} → {tool}")

    print("\n  ── Environment Variables to Set ──")
    for var, note in FREE_STACK_FOR_COURSE["env_vars_to_set"].items():
        print(f"  {var:<25} {note}")

    print(f"\n  Full reference: see the dicts in this file for")
    print(f"  Python examples, endpoints, and install commands.")
    print("=" * 65)
