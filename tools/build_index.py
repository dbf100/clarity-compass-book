#!/usr/bin/env python3
"""
Build a local search index over the book.

Two tiers, both optional to install:
- Keyword search (SQLite FTS5) always works, zero extra dependencies.
- Semantic search (find by meaning) turns on IF `model2vec` and `sqlite-vec` are
  installed (setup.sh tries to install them). model2vec is a small, fast, local
  embedding model with no heavy deps. If it isn't available, this script still
  builds the keyword index and just skips the vector part.

Usage:
    python3 build_index.py
    python3 build_index.py --book ../book --db clarity.db
"""
import argparse, re, sqlite3, struct, sys
from pathlib import Path

def chunk_markdown(text, source):
    """Split a chapter into chunks at headings, so each chunk is one idea."""
    chunks, cur_head, buf = [], source, []
    for line in text.splitlines():
        if re.match(r"^#{1,4}\s+", line):
            if buf and any(b.strip() for b in buf):
                chunks.append((cur_head, "\n".join(buf).strip()))
            cur_head = re.sub(r"^#+\s+", "", line).strip()
            buf = []
        else:
            buf.append(line)
    if buf and any(b.strip() for b in buf):
        chunks.append((cur_head, "\n".join(buf).strip()))
    return [(h, c) for h, c in chunks if len(c) > 40]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default=str(Path(__file__).parent.parent / "book"))
    ap.add_argument("--db", default=str(Path(__file__).parent / "clarity.db"))
    args = ap.parse_args()

    files = sorted(Path(args.book).glob("*.md"))
    if not files:
        sys.exit(f"No markdown chapters found in {args.book}")

    rows = []
    for f in files:
        for head, body in chunk_markdown(f.read_text(encoding="utf-8"), f.stem):
            rows.append((f.name, head, body))
    print(f"{len(files)} chapters -> {len(rows)} searchable sections")

    db = sqlite3.connect(args.db)
    db.execute("DROP TABLE IF EXISTS chunks")
    db.execute("CREATE TABLE chunks(id INTEGER PRIMARY KEY, source TEXT, heading TEXT, body TEXT)")
    db.execute("DROP TABLE IF EXISTS chunks_fts")
    db.execute("CREATE VIRTUAL TABLE chunks_fts USING fts5(heading, body, content='chunks', content_rowid='id')")
    for src, head, body in rows:
        cur = db.execute("INSERT INTO chunks(source, heading, body) VALUES (?,?,?)", (src, head, body))
        db.execute("INSERT INTO chunks_fts(rowid, heading, body) VALUES (?,?,?)", (cur.lastrowid, head, body))
    db.commit()
    print("Keyword search ready.")

    # Optional semantic layer
    try:
        import sqlite_vec
        from model2vec import StaticModel
    except ImportError:
        print("Meaning-based search not installed (that's fine). Keyword + graph search work.")
        db.close()
        return

    print("Building meaning-based search (first run downloads a small model)...")
    model = StaticModel.from_pretrained("minishlab/potion-base-8M")
    ids = [r[0] for r in db.execute("SELECT id FROM chunks ORDER BY id").fetchall()]
    bodies = [r[0] for r in db.execute("SELECT body FROM chunks ORDER BY id").fetchall()]
    embs = model.encode(bodies)
    dim = len(embs[0])
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.execute("DROP TABLE IF EXISTS vec_chunks")
    db.execute(f"CREATE VIRTUAL TABLE vec_chunks USING vec0(id INTEGER PRIMARY KEY, embedding FLOAT[{dim}])")
    for cid, emb in zip(ids, embs):
        db.execute("INSERT INTO vec_chunks(id, embedding) VALUES (?, ?)",
                   (cid, struct.pack(f"{dim}f", *[float(x) for x in emb])))
    db.commit()
    db.close()
    print("Meaning-based search ready.")

if __name__ == "__main__":
    main()
