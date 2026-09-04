#!/usr/bin/env python3
"""build_book.py — assemble book/ and the FULL-BOOK file from Merrill's sends.

Provenance model: the newest COMPLETE manuscript is the base, and any chapter
he revised AFTER that complete send overrides it (the OVERRIDES dict). When he
folds his loose chapter revisions back into a new complete, OVERRIDES empties
out again. Every output file records the source file and send date it came
from, so nothing has to be guessed later.

Usage: python3 tools/build_book.py [--force]
"""
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import docx2md

SRC = os.path.join(ROOT, "source-material")
BASE_DOCX = os.path.join(SRC, "2026-09-03-print-ready",
                         "The_Clarity_Compass_Complete_Print_Ready_Sept_2_2026.docx")
BASE_DATE = "2026-09-03"
REV_DIR = os.path.join(SRC, "2026-09-chapter-revisions")

WORDS = ["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE",
         "TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN",
         "SIXTEEN", "SEVENTEEN"]
NUM = {w: i + 1 for i, w in enumerate(WORDS)}

PARTS = ("NORTH", "EAST", "SOUTH", "WEST", "MAGNETIC NORTH", "APPLICATION")
# Repeating in-chapter sections. They become H2 inside the chapter they close.
SUBSECTIONS = ("TAKE THE READING", "SOURCES AND NOTES")

# Chapter revisions Merrill has sent SINCE the base complete manuscript.
# Empty right now: his Sept 1 and Sept 2 loose chapters are already folded into
# the Sept 2 print-ready complete (verified against the chapter openings).
OVERRIDES = {}


def despace(s):
    """'C H A P T E R   O N E' -> 'CHAPTER ONE'. Word letterspaces its headings."""
    if re.fullmatch(r'(?:[A-Z]\s+)+[A-Z]', s):
        # Two-or-more spaces separate words; single spaces separate letters.
        return re.sub(r'\s{2,}', '\x00', s).replace(' ', '').replace('\x00', ' ')
    return s


def nice(caps):
    """'SOURCES AND NOTES' -> 'Sources and Notes' (small words stay lowercase)."""
    small = {"and", "the", "of", "a", "in", "for", "to"}
    words = caps.lower().split()
    return " ".join(w if i and w in small else w.capitalize()
                    for i, w in enumerate(words))


def slug(title):
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return re.sub(r"-+", "-", s)


def split_base():
    """Return ordered section dicts from the complete manuscript."""
    paras = [p.strip() for p in docx2md.convert(BASE_DOCX).split("\n\n") if p.strip()]
    sections, cur, pending_part = [], None, None

    def start(kind, num, title):
        nonlocal cur, pending_part
        cur = {"kind": kind, "num": num, "title": title, "body": [],
               "part": pending_part}
        pending_part = None
        sections.append(cur)

    start("front", None, "Front Matter")
    for raw in paras:
        p = despace(raw)
        m = re.fullmatch(r'CHAPTER (\w+)', p)
        if m and m.group(1) in NUM:
            start("chapter", NUM[m.group(1)], None)
            continue
        if p in PARTS:
            pending_part = [p, "", []]
            continue
        if p == "FOREWORD":
            start("front", None, "Foreword")
            continue
        if p == "APPENDIX":
            start("back", None, "Appendix")
            continue
        if p == "ABOUT THE AUTHORS":
            start("back", None, "About the Authors")
            continue
        if p in SUBSECTIONS:
            cur["body"].append("## " + nice(p))
            continue
        if pending_part is not None:          # still on the part-divider page
            if p == "⊕":
                continue
            if not pending_part[1]:
                pending_part[1] = p
            else:
                pending_part[2].append(p)
            continue
        if cur["kind"] == "chapter" and cur["title"] is None:
            cur["title"] = p                  # first line after CHAPTER N is the title
            continue
        if p == "⊕" or re.fullmatch(r'[—\-\*\s]{3,}', p):
            cur["body"].append("---")
            continue
        cur["body"].append(p)
    return sections


def load_override(path):
    """Chapter docx -> (title, body)."""
    paras = [p.strip() for p in docx2md.convert(path).split("\n\n") if p.strip()]
    title, out = None, []
    for raw in paras:
        p = despace(raw)
        if re.fullmatch(r'CHAPTER \w+', p):
            continue
        if title is None:
            title = p.lstrip("# ").strip()
            continue
        if p in SUBSECTIONS:
            out.append("## " + nice(p))
            continue
        if re.fullmatch(r'[\*—\-\s]{3,}', p):
            out.append("---")
            continue
        out.append(p)
    return title, "\n\n".join(out)


def main():
    book = os.path.join(ROOT, "book")
    # book/ is the working manuscript and the author edits it directly, so a
    # rebuild must never silently discard unsaved edits. Refuse if git sees any.
    dirty = subprocess.run(["git", "-C", ROOT, "status", "--porcelain", "book"],
                           capture_output=True, text=True).stdout.strip()
    if dirty and "--force" not in sys.argv:
        sys.exit("book/ has unsaved changes:\n" + dirty +
                 "\nCommit them first, or re-run with --force to overwrite.")
    if os.path.isdir(book):
        shutil.rmtree(book)
    os.makedirs(book)

    files = []
    for sec in split_base():
        title, n = sec["title"], sec["num"]
        body = "\n\n".join(sec["body"]).strip()
        source, sdate = os.path.basename(BASE_DOCX), BASE_DATE
        if sec["kind"] == "chapter" and n in OVERRIDES:
            fname, sdate = OVERRIDES[n]
            title, body = load_override(os.path.join(REV_DIR, fname))
            source = fname
        if sec["kind"] == "chapter":
            name, heading = f"{n:02d}-{slug(title)}.md", f"Chapter {n}. {title}"
        else:
            name, heading = f"{slug(title)}.md", title
        fm = ["---", f"title: {title}", f"chapter: {n if n else 'null'}",
              f"source_file: {source}", f"source_date: {sdate}", "---", ""]
        if sec["part"]:
            pname, sub, intro = sec["part"]
            fm.append(f"> **Part: {pname.title()}**" + (f" — {sub}" if sub else ""))
            for para in intro:
                fm.append(">\n> " + para)
            fm.append("")
        front = "\n".join(fm).rstrip() + "\n\n"
        open(os.path.join(book, name), "w").write(front + f"# {heading}\n\n{body}\n")
        files.append((name, heading, body))

    full = ["# The Clarity Compass", "", "Merrill Fausett and Brody Fausett", "",
            f"Assembled from Merrill's sends. Base manuscript {BASE_DATE}"
            + (f"; chapters {', '.join(str(k) for k in sorted(OVERRIDES))} replaced by "
               "his later per-chapter revisions." if OVERRIDES else "."),
            "", "---", ""]
    for name, heading, body in files:
        full.append(f"# {heading}\n\n{body}\n\n---\n")
    open(os.path.join(ROOT, "clarity-compass-FULL-BOOK.md"), "w").write("\n".join(full))

    total = sum(len(b.split()) for _, _, b in files)
    print(f"{len(files)} files, {total:,} words")
    for name, _, body in files:
        print(f"  {name:52s} {len(body.split()):6,} words")


if __name__ == "__main__":
    main()
