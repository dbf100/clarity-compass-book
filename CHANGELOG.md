# Changelog

## 2026-06-30: Initial workspace
- Promoted the Clarity Compass material out of the HQ inbox into a real project workspace.
- Converted all 9 chapters from the original `.docx` files into clean, heading-and-table-aware
  markdown (`book/`). Tables preserved (the Three Lenses content lives in tables).
- Built `clarity-compass-FULL-BOOK.md`: the whole manuscript (~43k words) in one file for
  single-upload into a Claude Project.
- Wrote the **editorial board**: five ready-to-use expert editor prompts (developmental,
  structural, narrative, line, reader-advocate) plus a `run-the-board` one-shot.
- Wrote `how-to-use-with-claude.md` (non-technical setup walkthrough) and
  `claude-project-instructions.md` (Project custom instructions).
- Copied the graphify knowledge-graph artifacts (interactive HTML + plain-language report) into
  `knowledge-graph/`.
- Added an optional local search tool (`tools/`, SQLite FTS5 + sqlite-vec). Not required for normal use.
- Source chapters as of: East / EntrepreneurGuide / ThreeLenses (Jun 24) + North (updated Jun 25),
  South, West, MagneticNorth, Application, Appendix (Jun 24).

## 2026-06-30: Claude Code edition (search + sync)
- Made the workspace dual-mode: still works as a simple Claude Project, now also a turnkey
  Claude Code workspace.
- Added `CLAUDE.md` (auto-loaded project brain), `setup.sh` (one-command turnkey setup), and
  `.claude/commands/` slash commands: `/setup`, `/find`, `/graph`, `/board`, `/editor`, `/update`.
- Wired in three working search modes: keyword (SQLite FTS5, zero-dep), meaning-based (model2vec +
  sqlite-vec, local, no torch), and knowledge-graph query (graphify on the shipped graph.json).
- Consolidated graph artifacts into `graphify-out/` (graph.json now ships so `/graph` works locally).
- Wrote `how-to-use-with-claude-code.md` (non-technical setup via the Claude Code app + GitHub
  Desktop for one-click sync). README now presents both paths side by side.
- Verified end to end: setup builds the index, and all three search modes return chapter-cited results.
