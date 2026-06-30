# tools/: Optional Local Search

**Dad: you can skip this entire folder.** It is only useful if you want to search the book from a
computer terminal instead of just asking Claude. For normal writing and editing, the Claude
Project (see `../how-to-use-with-claude.md`) is all you need.

## What it does

Builds a small local search index over the book so you can run keyword and semantic searches
without uploading anything anywhere. The whole book also fits in Claude's context, so this is
mostly for scripted / offline use and for when the manuscript grows large.

## Two tiers

- **Keyword search** works out of the box. No installs. Uses Python's built-in SQLite (FTS5).
- **Semantic search** (find by meaning, not exact words) turns on if you install the optional
  dependencies in `requirements.txt`. It uses a small local embedding model (`all-MiniLM-L6-v2`)
  and the `sqlite-vec` extension. Local, free, private.

## Use

```bash
# from inside tools/
python3 build_index.py                       # builds clarity.db from ../book/*.md

python3 search.py "Shackleton" --keyword     # keyword search
python3 search.py "where do I talk about identity collapsing into the company"   # semantic (if installed)
```

To enable semantic search:

```bash
pip install -r requirements.txt
python3 build_index.py        # rerun to add the vector index
```

The index (`clarity.db`) is gitignored and rebuildable any time from the chapters.
