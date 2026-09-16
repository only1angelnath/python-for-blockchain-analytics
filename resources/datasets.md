# Blockchain Datasets & Data Sources

Free and accessible on-chain data sources used throughout this course.
No paid subscriptions required. All sources listed here have free tiers or are
completely free with no API key needed.

---

## Free APIs — no key required

| Source | What it provides | Used in |
|--------|-----------------|---------|
| [DefiLlama](https://defillama.com/docs/api) | Protocol TVL, yields, stablecoin supply, DEX volumes, fees | Phase 2, 3, 5, 7 |
| [CoinGecko](https://www.coingecko.com/api/documentation) | Token prices, OHLCV history, market cap, exchange data | Phase 2, 7 |
| [Ankr Public RPC](https://www.ankr.com/rpc/) | Direct node access for ETH, Polygon, Arbitrum, Base, and more | Phase 3, 4 |
| [LlamaNodes](https://llamanodes.com) | Free multi-chain RPC endpoints | Phase 3 |
| [The Graph](https://thegraph.com/) | Subgraph queries for Uniswap, Aave, Curve, Balancer, Lido | Phase 3, 5 |
| [Mempool.space](https://mempool.space/api) | Bitcoin mempool, fee estimates, block data | Phase 3 |

---

## Free APIs — free key (quick signup)

| Source | What it provides | Signup | Used in |
|--------|-----------------|--------|---------|
| [Etherscan](https://etherscan.io/apis) | Txns, token transfers, contract ABI, balances, event logs | [etherscan.io/register](https://etherscan.io/register) | Phase 2, 3 |
| [Infura](https://infura.io) | RPC for ETH, Polygon, Arbitrum, Base — 100k req/day | [app.infura.io/register](https://app.infura.io/register) | Phase 3, 4 |
| [Alchemy](https://www.alchemy.com/) | Enhanced APIs, NFT data, 300M CU/month | [auth.alchemy.com/signup](https://auth.alchemy.com/signup) | Phase 3, 4 |
| [Helius](https://helius.dev) | Solana RPC + enhanced APIs, 100k credits/day | [helius.dev](https://helius.dev) | Phase 3 |

---

## Indexing platforms — free tiers

| Source | What it provides | Used in |
|--------|-----------------|---------|
| [Envio / HyperIndex](https://envio.dev) | Custom fast EVM indexer, open source + free hosted | Phase 5 |
| [Flipside Crypto](https://flipsidecrypto.xyz) | SQL analytics API for blockchain data (Dune alternative) | Phase 5 |
| [Subsquid](https://subsquid.io) | Decentralised data lake + indexing framework | Phase 5 |

---

## Static datasets (CSV / Parquet)

| Dataset | Source | How to get it |
|---------|--------|---------------|
| Ethereum daily gas prices | Etherscan export | Export from etherscan.io/chart/gasprice |
| DeFi protocol TVL history | DefiLlama | `GET https://api.llama.fi/protocol/{slug}` |
| Uniswap V3 pool data | The Graph | Query `uniswap/uniswap-v3` subgraph |
| Token price history | CoinGecko | `GET /coins/{id}/market_chart?days=365` |
| NFT sales | OpenSea API | Free tier available |

---

## Setting up your API keys

Create a `.env` file in your repo root (**already in `.gitignore` — never commit this**):

```bash
# .env
ETHERSCAN_API_KEY=your_key_here
INFURA_API_KEY=your_key_here
ALCHEMY_API_KEY=your_key_here
HELIUS_API_KEY=your_key_here
```

Load in Python:
```python
from dotenv import load_dotenv  # pip install python-dotenv
import os

load_dotenv()
etherscan_key = os.environ.get("ETHERSCAN_API_KEY")
```

---

## Sample data

Each lesson folder that needs data includes a `sample_*.csv` with a small excerpt
so you can run exercises without hitting API rate limits during development.
