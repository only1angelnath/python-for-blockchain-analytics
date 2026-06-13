# 01 — Environment Setup

Follow these steps on **Ubuntu Linux** (recommended), macOS, or Windows WSL.

---

## Step 1: Install Python 3.12+

```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3-pip -y
python3 --version   # should print Python 3.12.x
```

## Step 2: Install VS Code

Download from [code.visualstudio.com](https://code.visualstudio.com/) and install.

Then install extensions:
- **Python** (Microsoft)
- **Jupyter** (Microsoft)
- **GitLens** (optional but useful)

## Step 3: Install Jupyter Lab

```bash
pip install jupyterlab
jupyter lab   # opens in your browser
```

## Step 4: Create a virtual environment

Always work inside a virtual environment — it keeps your project dependencies isolated.

```bash
python3 -m venv .venv
source .venv/bin/activate    # on Linux/macOS
# .venv\Scripts\activate    # on Windows
pip install jupyterlab pandas numpy matplotlib requests
```

## Step 5: Verify everything works

```bash
python3 -c "import pandas; print('pandas ✓')"
python3 -c "import numpy; print('numpy ✓')"
```

✅ If both print without errors, your environment is ready.

---

## Troubleshooting

**`python3` not found** → try `python` instead, or reinstall from python.org  
**`pip` not found** → run `sudo apt install python3-pip`  
**Jupyter won't open** → try `python3 -m jupyter lab`
