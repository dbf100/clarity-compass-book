# The Clarity Compass: Book Workspace

A complete writing, editing, and review workspace for **The Clarity Compass** by
Merrill Fausett & Brody Fausett. Everything you need to write the book with Claude as a
partner, get expert editorial feedback, and see how the whole framework connects.

**New here? Read [`how-to-use-with-claude.md`](how-to-use-with-claude.md) first.** It walks you
through setup step by step, no tech skills required.

---

## What's in here

```
clarity-compass-book/
├── how-to-use-with-claude.md      ← START HERE. Step-by-step setup for Claude.
├── claude-project-instructions.md ← paste into your Claude Project so Claude knows how to help
│
├── book/                          ← the book itself, one clean file per chapter (edit these)
│   ├── 00-entrepreneur-guide.md       Teaser / front matter
│   ├── 01-three-lenses.md             How the challenges show up across three contexts
│   ├── 02-north-identity.md           NORTH: Identity
│   ├── 03-east-action.md              EAST: Action
│   ├── 04-south-values.md             SOUTH: Values
│   ├── 05-west-reflection.md          WEST: Reflection & Recalibration
│   ├── 06-magnetic-north-forces.md    MAGNETIC NORTH: the forces that pull you off course
│   ├── 07-application.md              Applying the compass
│   └── 08-appendix.md                 Appendix
│
├── clarity-compass-FULL-BOOK.md   ← all chapters combined into one file (upload THIS to Claude)
│
├── editorial-board/               ← your panel of five expert book editors (ready-to-use prompts)
│   ├── README.md
│   ├── developmental-editor.md
│   ├── structural-architect.md
│   ├── narrative-editor.md
│   ├── line-editor.md
│   ├── reader-advocate.md
│   └── run-the-board.md               run all five at once + get the consensus
│
├── knowledge-graph/               ← a visual map of every concept in the book and how they connect
│   ├── clarity-compass-graph.html     open in any web browser
│   └── GRAPH_REPORT.md                the same map in plain language
│
└── tools/                         ← OPTIONAL, technical. Local search over the book. Skippable.
```

## The simple version (for writing and editing)

1. Set up a Claude Project once (see `how-to-use-with-claude.md`).
2. Upload **`clarity-compass-FULL-BOOK.md`** so Claude has the whole book.
3. Write, edit, and ask questions in plain English.
4. When you want a hard review, summon an editor from `editorial-board/`.

That's the whole system. The book is plain text files, so you can edit them anywhere, and Claude
can read all of them at once because the whole book fits comfortably in its memory.

## The knowledge graph (a bonus view)

`knowledge-graph/clarity-compass-graph.html` is an interactive map of every idea in the book and
how they link together. It surfaces the "load-bearing" concepts, where ideas cluster, and where
there might be gaps. Open it in a browser and click around. `GRAPH_REPORT.md` says the same thing
in words.

## tools/ (optional, technical)

If you (Brody) want keyword + semantic search over the book locally without uploading anything,
`tools/` has a small SQLite indexer. Dad never needs this. See `tools/README.md`.

---

_Source of truth lives here. Edit the markdown, keep it in git, and the whole thing stays portable._
