#!/usr/bin/env python3
"""
Build a local search index over the book.

Optional. Dad never needs this. It gives you (Brody) fast keyword AND semantic
search over the manuscript locally, without uploading anything.

- Keyword search (SQLite FTS5) always works, zero extra dependencies.
- Semantic search additionally turns on IF `sentence-transformers` and
  `sqlite-vec` are installed (see requirements.txt). If they're not, the script
  still builds the keyword index and just skips the vector part.

Usage:
    python3 build_index.py              # indexes ../book/*.md into clarity.db
    python3 build_index.py --book ../book --db clarity.db
"""
import argparse, re, sqlite3, sys
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
    print(f"{len(files)} chapters -> {len(rows)} chunks")

    db = sqlite3.connect(args.db)
    db.execute("DROP TABLE IF EXISTS chunks")
    db.execute("CREATE TABLE chunks(id INTEGER PRIMARY KEY, source TEXT, heading TEXT, body TEXT)")
    db.execute("DROP TABLE IF EXISTS chunks_fts")
    db.execute("CREATE VIRTUAL TABLE chunks_fts USING fts5(heading, body, content='chunks', content_rowid='id')")
    for src, head, body in rows:
        cur = db.execute("INSERT INTO chunks(source, heading, body) VALUES (?,?,?)", (src, head, body))
        db.execute("INSERT INTO chunks_fts(rowid, heading, body) VALUES (?,?,?)", (cur.lastrowid, head, body))
    db.commit()
    print("Keyword index (FTS5) built.")

    # Optional semantic layer
    try:
        import sqlite_vec
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("Semantic search skipped (install sentence-transformers + sqlite-vec to enable). "
              "Keyword search is ready.")
        db.close()
        return

    print("Building semantic (vector) index. First run downloads a small model.")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.execute("DROP TABLE IF EXISTS vec_chunks")
    db.execute("CREATE VIRTUAL TABLE vec_chunks USING vec0(id INTEGER PRIMARY KEY, embedding FLOAT[384])")
    ids = [r[0] for r in db.execute("SELECT id FROM chunks").fetchall()]
    bodies = [r[0] for r in db.execute("SELECT body FROM chunks ORDER BY id").fetchall()]
    embs = model.encode(bodies, normalize_embeddings=True, show_progress_bar=True)
    import struct
    for cid, emb in zip(ids, embs):
        db.execute("INSERT INTO vec_chunks(id, embedding) VALUES (?, ?)",
                   (cid, struct.pack(f"{len(emb)}f", *emb)))
    db.commit()
    db.close()
    print("Semantic index built. Run: python3 search.py \"your question\"")

if __name__ == "__main__":
    main()
