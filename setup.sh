#!/usr/bin/env bash
# One-time setup for the Clarity Compass workspace.
# Safe to run more than once. Installs the search tools and builds the index.
set -e
cd "$(dirname "$0")"

echo ""
echo "Setting up your Clarity Compass workspace. This takes about a minute."
echo ""

# 1. Pick a Python
PY=python3
command -v "$PY" >/dev/null 2>&1 || { echo "Python 3 is needed. Install it from python.org, then run this again."; exit 1; }

# 2. Create a private virtual environment (keeps everything self-contained)
if [ ! -d .venv ]; then
  echo "  - creating workspace environment..."
  "$PY" -m venv .venv
fi
VPY=.venv/bin/python
"$VPY" -m pip install -q --upgrade pip >/dev/null 2>&1 || true

# 3. Install the knowledge-graph search engine (graphify)
echo "  - installing the knowledge-graph search (graphify)..."
"$VPY" -m pip install -q graphifyy >/dev/null 2>&1 || echo "    (graphify install hiccup. Keyword search and Claude reading still work.)"

# 4. Optional: semantic (meaning-based) passage search. Heavier, allowed to fail quietly.
echo "  - (optional) installing meaning-based search..."
"$VPY" -m pip install -q sqlite-vec model2vec >/dev/null 2>&1 || echo "    (skipped the optional semantic layer. Keyword + graph search still work great.)"

# 5. Turn on auto-refresh: rebuild the search index automatically on every save/pull
if [ -d .git ]; then
  echo "  - turning on auto-refresh of search..."
  git config core.hooksPath .githooks 2>/dev/null || true
fi

# 6. Build the keyword search index over the book (uses Python's built-in database, no extra deps)
echo "  - building the search index over your book..."
"$VPY" tools/build_index.py || echo "    (index build hiccup. You can still ask Claude to read and search the book directly.)"

echo ""
echo "All set. You can now:"
echo "    /find <words>      fast keyword search"
echo "    /graph <question>  search how the ideas connect"
echo "    /board             get the full editorial review"
echo "    or just ask Claude anything about the book in plain English."
echo ""
