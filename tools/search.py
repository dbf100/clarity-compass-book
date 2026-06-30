#!/usr/bin/env python3
"""
Search the book index built by build_index.py.

Usage:
    python3 search.py "where do I talk about identity"   # semantic if available, else keyword
    python3 search.py --keyword "Shackleton"             # force keyword
    python3 search.py "imposter syndrome" --top 8
"""
import argparse, sqlite3, struct, sys
from pathlib import Path

def keyword_search(db, query, top):
    try:
        return db.execute(
            "SELECT c.source, c.heading, snippet(chunks_fts, 1, '[', ']', ' ... ', 14) "
            "FROM chunks_fts JOIN chunks c ON c.id = chunks_fts.rowid "
            "WHERE chunks_fts MATCH ? ORDER BY rank LIMIT ?", (query, top)).fetchall()
    except sqlite3.OperationalError:
        return db.execute(
            "SELECT c.source, c.heading, substr(c.body,1,200) FROM chunks_fts "
            "JOIN chunks c ON c.id = chunks_fts.rowid WHERE chunks_fts MATCH ? LIMIT ?",
            ('"' + query + '"', top)).fetchall()

def semantic_search(db, query, top):
    import sqlite_vec
    from model2vec import StaticModel
    model = StaticModel.from_pretrained("minishlab/potion-base-8M")
    q = model.encode([query])[0]
    blob = struct.pack(f"{len(q)}f", *[float(x) for x in q])
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    return db.execute(
        "SELECT c.source, c.heading, substr(c.body,1,260), v.distance "
        "FROM vec_chunks v JOIN chunks c ON c.id = v.id "
        "WHERE v.embedding MATCH ? AND k = ? ORDER BY v.distance", (blob, top)).fetchall()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--db", default=str(Path(__file__).parent / "clarity.db"))
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--keyword", action="store_true", help="force keyword search")
    args = ap.parse_args()

    if not Path(args.db).exists():
        sys.exit("No search index yet. Run setup first (in Claude Code: /setup).")
    db = sqlite3.connect(args.db)

    has_vec = db.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='vec_chunks'").fetchone()
    if not args.keyword and has_vec:
        try:
            print(f"\nMeaning-based results for: {args.query}\n")
            for src, head, body, dist in semantic_search(db, args.query, args.top):
                print(f"  [{src} > {head}]  (match {1-dist:.2f})\n    {body.strip()}\n")
            return
        except Exception:
            pass  # fall through to keyword
    print(f"\nKeyword results for: {args.query}\n")
    res = keyword_search(db, args.query, args.top)
    if not res:
        print("  (no exact matches. Try /graph for concept search, or just ask Claude.)\n")
    for src, head, snip in res:
        print(f"  [{src} > {head}]\n    {snip.strip()}\n")

if __name__ == "__main__":
    main()
