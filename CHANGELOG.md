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

## 2026-09-02: Rebuilt on Merrill's Aug 28 to Sept 2 rewrite
- **The book changed shape.** The June version in here was the 9-part compass manuscript
  (North / East / South / West / Magnetic North). Between Aug 27 and Sept 2 Merrill rewrote it
  as a **17-chapter narrative** built on the Endurance story, with a new Foreword, a new
  About the Authors, "Your Compass" exercises closing each part, an Application part, and a
  new Appendix on the history of navigation. `book/` now matches that.
- **Provenance is now explicit.** Every file in `book/` carries `source_file` and `source_date`
  frontmatter. The base is `The_Clarity_Compass_COMPLETE_UPDATED_Aug31_2026.pdf`; chapters 1, 2,
  3 and 6 come from his Sept 1 per-chapter revisions and chapter 15 from his Sept 2 revision,
  because those supersede the complete send.
- Kept every file Merrill actually sent in `source-material/`, organized by date, so a future
  revision can be dropped in and rebuilt instead of re-derived.
- New tools: `tools/docx2md.py`, `tools/pdf2md.py` (rejoins the print PDF's hard-wrapped lines
  and repairs words the typesetter broke across a line), `tools/build_book.py` (assembles
  `book/` + `clarity-compass-FULL-BOOK.md` from the sources above), and `tools/narrate.py`
  (Kokoro audiobook rendering, local and free, 44.1kHz so the files play in Messages).
- Rebuilt the keyword + meaning-based search index over the new chapters.
- **The knowledge graph in `graphify-out/` is STALE** and still describes the June structure.
  Refreshing it needs an AI pass over the text (`/graphify --update`), so it is flagged rather
  than silently left looking current.

## 2026-09-03: Merrill's print-ready complete replaces everything

- He folded his loose Sept 1 and Sept 2 chapter revisions back into one
  **print-ready complete manuscript** and sent it as both .docx and .pdf.
  It is now the base, and `OVERRIDES` in `build_book.py` is empty again.
- **The book grew from ~31.8k to ~41.4k words.** New in this version: a title
  page, copyright, and full contents; a **WEST part divider** (the one part
  that was missing before); a **"Take the Reading"** exercise closing 14
  chapters (renamed from "Your Compass"); a **"Sources and Notes"** section on
  13 chapters; and bridge paragraphs that hand each chapter off to the next.
- Subtitle changed to **"Discovering You, Before Success, Failure or Someone
  Else Does."** The appendix was rewritten and retitled **"The Distance
  Between Readings"** (861 words to 2,261).
- Verified the complete really does contain his later loose revisions before
  dropping them: chapter 1 still opens "The sound came before the meaning"
  (his Sept 1 rewrite) and chapter 15 still opens on the Orion reentry (Sept 2).
- Confirmed the .docx and the .pdf carry identical text (the only differences
  are running headers and contents pagination), so the build now reads the
  .docx and `pdf2md.py` is kept only as a fallback for PDF-only sends.
- `book/` renamed its unnumbered sections to `front-matter.md`, `foreword.md`,
  `appendix.md`, `about-the-authors.md` so file number still equals chapter
  number. Search index rebuilt: 21 files, 69 searchable sections.
