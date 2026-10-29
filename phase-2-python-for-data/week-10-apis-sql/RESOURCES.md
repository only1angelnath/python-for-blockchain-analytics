# Week 10 Resources — APIs & SQL from Python

How to use this page: **docs first, video second, book for depth.** Official docs are the source of truth
when an API changes (and APIs change); videos and books explain *why*.

Every link is marked with how much I could verify when this week was built (October 2026):

- ✅ **Verified** — the page came up in my research and its content matched what I describe
- ☑️ **Standard** — a well-known official page I'm confident exists, but did not re-open; open it and confirm
- 🔎 **Search it** — I could not confirm a direct link, so I give the exact title to search for. I won't invent a URL

---

## 1. Official API docs (read these before trusting any course)

| Source | Link | Status | What to read |
|---|---|---|---|
| CoinGecko — authentication (Demo plan) | https://docs.coingecko.com/demo/reference/authentication | ✅ | How the `x-cg-demo-api-key` header works |
| CoinGecko — sign up for a Demo key | https://support.coingecko.com/hc/en-us/articles/21880397454233-User-Guide-How-to-sign-up-for-CoinGecko-Demo-API-and-generate-an-API-key | ✅ | Get your free key; check your **plan's actual limits** here |
| Etherscan V2 — rate limits | https://docs.etherscan.io/etherscan-v2/rate-limits | ✅ | Free tier numbers (5 calls/sec, 100k/day at time of writing) |
| Etherscan V2 — FAQ / V1 migration | https://docs.etherscan.io/etherscan-v2/support/v2-faq | ✅ | One key across chains via `chainid`; V1 is retired |
| Etherscan V2 docs — cookbook | https://docs.etherscan.io/ | ✅ (site) | Find "Get an Address's Full Transaction History" in the sidebar: the official take on the pagination problem from `lesson.ipynb` §10.3 |
| DefiLlama API docs | https://defillama.com/docs/api | ✅ (cited as the official docs by the `defillamaAPI` PyPI page) | Endpoint list; free vs Pro sections |
| DefiLlama docs (alternate) | https://docs.llama.fi/ | ✅ (cited by Avalanche's integration docs) | Same, older entry point |

**Course correction worth knowing:** earlier project notes said CoinGecko needs no key. It now has a **free Demo plan with a key**; keyless access still exists but is heavily throttled. `api_clients.py` supports both.

## 2. Python documentation (the reference you'll keep open)

| Topic | Link | Status |
|---|---|---|
| `requests` quickstart | https://requests.readthedocs.io/en/latest/user/quickstart/ | ☑️ |
| `sqlite3` module (connections, cursors, placeholders, transactions) | https://docs.python.org/3/library/sqlite3.html | ☑️ |
| `logging` HOWTO | https://docs.python.org/3/howto/logging.html | ☑️ |
| `argparse` tutorial | https://docs.python.org/3/howto/argparse.html | ☑️ |
| Generators (the `yield` keyword) | https://docs.python.org/3/howto/functional.html#generators | ☑️ |
| `pandas.read_sql_query` | https://pandas.pydata.org/docs/reference/api/pandas.read_sql_query.html | ☑️ |
| urllib3 `Retry` (connection-level retries) | https://urllib3.readthedocs.io/en/stable/reference/urllib3.util.html | ☑️ |

## 3. SQLite itself

| Topic | Link | Status |
|---|---|---|
| SQLite documentation index | https://www.sqlite.org/docs.html | ☑️ |
| Datatypes in SQLite (affinity, why there's no date type) | https://www.sqlite.org/datatype3.html | ☑️ |
| UPSERT (`ON CONFLICT DO UPDATE`) | https://www.sqlite.org/lang_upsert.html | ☑️ |
| Window functions | https://www.sqlite.org/windowfunctions.html | ☑️ |
| Date and time functions | https://www.sqlite.org/lang_datefunc.html | ☑️ |
| Query planning / `EXPLAIN QUERY PLAN` | https://www.sqlite.org/eqp.html | ☑️ |
| DB Browser for SQLite (free GUI to look inside your `.db`) | https://sqlitebrowser.org/ | ☑️ |

## 4. Videos 📺

I could not retrieve direct YouTube links from my environment, so these are **exact titles to search**.
Check the upload date: prefer videos from the last few years that use Python 3.

| Topic | Search for | Why it helps |
|---|---|---|
| Calling APIs | **"Python Requests Tutorial: Request Web Pages, Download Images, POST Data, Read JSON, and More"** (Corey Schafer) | Best short tour of `requests`: GET/POST, params, status codes, JSON. Maps to `lesson.ipynb` §1-§5 |
| JSON handling | **"Python Tutorial: Working with JSON Data using the json Module"** (Corey Schafer) | Reinforces `lesson.ipynb` §2 (JSON ↔ dict/list) |
| SQLite from Python | search **"Python sqlite3 tutorial"** and pick a recent, well-rated one | Maps to `lesson_expanded.ipynb` §1-§2. I couldn't verify a specific video, so judge by: uses `?` placeholders (not f-strings), shows `commit()`/`with conn` |
| Window functions | search **"SQL window functions explained"** | You know the idea from Dune; this checks the syntax carries over to SQLite (§9.4) |
| REST APIs conceptually | search **"REST API concepts and examples"** | Only if the HTTP anatomy in `lesson.ipynb` §1 felt fast |

## 5. Free books and PDFs 📖

| Resource | Where | Status | Read |
|---|---|---|---|
| **Python for Everybody** (Charles Severance), free book, free PDF/EPUB downloads, CC-licensed | https://www.pythonlearn.com (also py4e.com) | ✅ | **Ch. 13 "Using Web Services"** (HTTP + JSON, pairs with `lesson.ipynb`); **Ch. 15 "Using Databases and SQL"** (SQLite from Python, pairs with `lesson_expanded.ipynb`). Slower pace than this course; good if a concept didn't land |
| Python `sqlite3` docs | see §2 | ☑️ | Reference, not a tutorial |
| SQLite docs "Datatypes" | see §3 | ☑️ | Short, and it explains the type quirks from `lesson_expanded.ipynb` §3 directly |

## 6. Tools worth installing

| Tool | Use |
|---|---|
| `curl` / `httpie` | Poke an endpoint from the terminal before writing Python |
| `jq` | Pretty-print and filter JSON in the terminal |
| DB Browser for SQLite | Look at `chainlens.db` as tables, run queries visually |
| `python-dotenv` | Load `.env` into `os.environ` (`lesson.ipynb` §6.3) |

## 7. Suggested study order (about 6-8 hours total)

1. **`lesson.ipynb`** (2 h) — skim §1-§3 if you know HTTP; slow down on §7 (errors), §8 (retries), §10 (pagination + generators)
2. 📺 Corey Schafer's requests video (30 min), only if §1-§5 felt shaky
3. **Exercises 1-9** (1.5 h) — Part A
4. **`lesson_expanded.ipynb`** (2 h) — slow down on §3 (types), §4 (injection), §7.2 (upsert)
5. **Exercises 10-16** (1 h) — Part B
6. **`lesson_advanced.ipynb`** (1.5 h), then the **challenge** exercise
7. Get free keys, run **`python3 live_smoke_test.py`**, then **`python3 pipeline.py --live`**
8. Optional depth: *Python for Everybody* ch. 13 and 15

## 8. When something breaks live

1. Run `python3 live_smoke_test.py` and read which source failed and the hint
2. Compare the response shape with the provider's current docs (§1). **The docs win over this course**
3. Fix it in the matching client method in `api_clients.py`; add a one-line note to your README. That's the job.
