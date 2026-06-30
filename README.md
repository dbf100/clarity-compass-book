# The Clarity Compass: Book Workspace

A complete writing, editing, and review workspace for **The Clarity Compass** by
Merrill Fausett & Brody Fausett. Everything you need to write the book with Claude as a
partner, get expert editorial feedback, search across every chapter, and see how the whole
framework connects.

## Two ways to use it (pick one)

| | **Simple** (Claude Project) | **Full power** (Claude Code) |
|---|---|---|
| Setup | Upload one file, no install | Open this folder in the Claude Code app |
| Best for | Writing and editing, fast start | Writing, editing, **search**, and auto-syncing updates |
| Search tools | Claude reads the whole book | Claude reads it **plus** keyword + knowledge-graph search |
| Staying in sync | Re-upload to get updates | One-click pull / `/update` |
| Start here | [`how-to-use-with-claude.md`](how-to-use-with-claude.md) | [`how-to-use-with-claude-code.md`](how-to-use-with-claude-code.md) |

Both run off the exact same book files, so nothing is lost by choosing one. The Claude Code version
just adds the search tools and stays in sync automatically.

---

## What's in here

```
clarity-compass-book/
├── how-to-use-with-claude.md       ← simple path: set up a Claude Project
├── how-to-use-with-claude-code.md  ← full path: open in Claude Code (search + auto-sync)
├── claude-project-instructions.md  ← paste into a Claude Project so Claude knows how to help
├── CLAUDE.md                       ← auto-loaded by Claude Code (you don't touch this)
│
├── book/                           ← the book itself, one clean file per chapter (edit these)
│   ├── 00-entrepreneur-guide.md        Teaser / front matter
│   ├── 01-three-lenses.md              How the challenges show up across three contexts
│   ├── 02-north-identity.md            NORTH: Identity
│   ├── 03-east-action.md               EAST: Action
│   ├── 04-south-values.md              SOUTH: Values
│   ├── 05-west-reflection.md           WEST: Reflection & Recalibration
│   ├── 06-magnetic-north-forces.md     MAGNETIC NORTH: the forces that pull you off course
│   ├── 07-application.md               Applying the compass
│   └── 08-appendix.md                  Appendix
│
├── clarity-compass-FULL-BOOK.md    ← all chapters in one file (upload THIS in the simple path)
│
├── editorial-board/                ← your panel of five expert book editors (ready-to-use prompts)
│   ├── developmental-editor.md         is the whole book working?
│   ├── structural-architect.md         does the compass framework hold up?
│   ├── narrative-editor.md             are the stories landing?
│   ├── line-editor.md                  sharper sentences, your voice
│   ├── reader-advocate.md              what a real entrepreneur thinks
│   └── run-the-board.md                all five at once + the consensus
│
├── graphify-out/                   ← knowledge graph: every concept and how they connect
│   ├── graph.html                      open in any web browser to click around
│   ├── graph.json                      powers /graph search in Claude Code
│   └── GRAPH_REPORT.md                 the same map in plain language
│
├── tools/                          ← local search engine (keyword + optional semantic)
├── setup.sh                        ← one-time setup the Claude Code app runs for you
└── .claude/commands/              ← the /find, /graph, /board, /editor, /update commands
```

## In Claude Code, the simple commands are

- `/setup` — one-time, installs search and builds the index (Claude runs it for you)
- `/find <words>` — fast keyword search of the book
- `/graph <question>` — search how the ideas connect, with chapter citations
- `/board` — run the full editorial board (five editors + a consensus)
- `/editor <name>` — run one editor: developmental, structural, narrative, line, or reader
- `/update` — pull the latest version of the book and refresh search

## The knowledge graph

`graphify-out/graph.html` is an interactive map of every idea in the book and how they link
together. It surfaces the load-bearing concepts, where ideas cluster, and where there may be gaps.
Open it in a browser and click around. `GRAPH_REPORT.md` says the same thing in words.

---

_Source of truth lives here. Edit the markdown, keep it in git, and the whole thing stays portable._
