# Blockchain Datasets

Free and accessible on-chain datasets used throughout this course.

## APIs (free tier available)

| Source | What it provides | Used in |
|---|---|---|
| [Etherscan](https://etherscan.io/apis) | Transactions, token transfers, contract ABIs | Phase 2, 3 |
| [CoinGecko](https://www.coingecko.com/api/documentation) | Token prices, market data, historical OHLCV | Phase 2, 7 |
| [Dune SIM API](https://sim.dune.com) | Real-time on-chain data via API | Phase 2, 3 |
| [Alchemy](https://www.alchemy.com/) | RPC node access, enhanced APIs | Phase 3, 4 |
| [Infura](https://infura.io/) | Ethereum + multi-chain RPC | Phase 3 |
| [DefiLlama](https://defillama.com/docs/api) | Protocol TVL, yields, stablecoin data | Phase 5, 7 |
| [The Graph](https://thegraph.com/) | Subgraph queries for DEX/DeFi protocols | Phase 5 |

## Static datasets (CSV / Parquet)

| Dataset | Source | Size |
|---|---|---|
| Uniswap v3 swaps | Dune Analytics export | varies |
| Ethereum daily gas prices | Etherscan export | ~3MB |
| NFT sales history | OpenSea public data | varies |
| DeFi protocol TVL history | DefiLlama export | ~10MB |

## Sample data

Each lesson folder includes a `sample_*.csv` with a small excerpt so you can run exercises without hitting API rate limits.
