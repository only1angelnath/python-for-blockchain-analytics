#!/usr/bin/env python3
"""
new_session.py — Run this at the start of any new Claude conversation
to generate a context summary you can paste in.

Usage: python3 new_session.py
"""

import os
import subprocess
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).parent

def count_files(folder):
    if not folder.exists():
        return 0
    return sum(1 for f in folder.rglob("*")
               if f.is_file() and f.suffix in {".py", ".ipynb", ".md"}
               and ".gitkeep" not in f.name)

def git_log(n=3):
    try:
        result = subprocess.run(
            ["git", "log", f"-{n}", "--pretty=format:%h %s", "--no-walk"],
            capture_output=True, text=True, cwd=REPO_ROOT
        )
        return result.stdout.strip().splitlines()
    except Exception:
        return []

def git_status():
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            capture_output=True, text=True, cwd=REPO_ROOT
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"

def check_phase(phase_dir):
    path = REPO_ROOT / phase_dir
    if not path.exists():
        return "⏳ Not started"
    files = count_files(path)
    if files > 5:
        return f"✅ {files} files"
    elif files > 0:
        return f"🔄 {files} files (in progress)"
    else:
        return "⏳ Empty (scaffold only)"

phases = [
    ("phase-0-setup",                  "Setup"),
    ("phase-1-python-fundamentals",    "Python Fundamentals"),
    ("phase-2-python-for-data",        "Python for Data"),
    ("phase-3-blockchain-analytics",   "Blockchain Analytics"),
    ("phase-4-advanced-python",        "Advanced Python"),
    ("phase-5-data-engineering",       "Data Engineering"),
    ("phase-6-system-design",          "System Design"),
    ("phase-7-ml-engineering",         "ML Engineering"),
    ("final-capstone-chainlens",       "ChainLens Capstone"),
]

print("=" * 65)
print("  PYTHON FOR BLOCKCHAIN ANALYTICS — SESSION CONTEXT")
print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 65)

print("\n## Current position\n")
print("Phase 2, Week 8 — Pandas & NumPy is NEXT")
print("(Phase 1 complete. Week 7 File Handling complete.)\n")

print("## Phase status\n")
for folder, name in phases:
    status = check_phase(folder)
    print(f"  {name:<30} {status}")

print("\n## Recent commits\n")
for line in git_log(5):
    print(f"  {line}")

print("\n## Uncommitted changes\n")
status = git_status()
if status:
    for line in status.splitlines():
        print(f"  {line}")
else:
    print("  Clean — nothing uncommitted")

print("""
## What to say to Claude

Paste this at the start of your new conversation in the Project:

---
Continuing the Python for Blockchain Analytics curriculum.
Current position: Phase 2, Week 8 — Pandas & NumPy.

Please read PROJECT_CONTEXT.md (uploaded to this project) for full state,
then build Week 8: lesson.ipynb + exercises.py + exercises_solutions.py.

Deliver files individually (not zipped). Verify all Python files run clean before delivering.
---
""")
print("=" * 65)

