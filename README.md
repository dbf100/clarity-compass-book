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
│   ├── 00-foreword.md                  Foreword
│   ├── 01-abandon-ship.md              1. Abandon Ship
│   ├── 02-the-wrong-north.md           2. The Wrong North
│   ├── 03-the-battle-for-identity.md   3. The Battle for Identity
│   ├── 04-becoming.md                  4. Becoming
│   ├── 05-right-action.md              5. Right Action
│   ├── 06-the-capacity-dividend.md     6. The Capacity Dividend
│   ├── 07-seeing-further.md            7. Seeing Further
│   ├── 08-...values-and-preferences.md 8. The Difference Between Values and Preferences
│   ├── 09-values-as-architecture.md    9. Values as Architecture
│   ├── 10-when-values-are-tested.md    10. When Values Are Tested
│   ├── 11-look-and-live.md             11. Look and Live
│   ├── 12-the-recalibration.md         12. The Recalibration
│   ├── 13-the-invisible-pull.md        13. The Invisible Pull
│   ├── 14-knowing-your-...ability.md   14. Knowing Your Specific Vulnerability
│   ├── 15-speed-drift-...compass.md    15. Speed, Drift, and the Modern Compass
│   ├── 16-the-gap-the-gulf-...gain.md  16. The Gap, the Gulf, and the Gain
│   ├── 17-the-lighthouse.md            17. The Lighthouse
│   ├── 18-appendix.md                  Appendix: How Humans Learned to Find Their Way
│   └── 19-about-the-authors.md         About the Authors
│
├── audio/                          ← Kokoro narration of the chapters (local, free to make)
├── source-material/                ← the exact .docx / .pdf files Merrill sent, by date
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
├── tools/                          ← local search, docx/pdf converters, book builder, narrator
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
