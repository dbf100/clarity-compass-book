#!/usr/bin/env python3
"""build_book.py — assemble book/ and the FULL-BOOK file from Merrill's sends.

Provenance model: the newest complete manuscript is the base, and any chapter
Merrill has revised SINCE that complete send overrides it. Every output file
records which source file and send date it came from, so a later revision can
be dropped in without guessing what is current.

Usage: python3 tools/build_book.py
"""
import os
import re
import sys
import shutil
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import pdf2md
import docx2md

SRC = os.path.join(ROOT, "source-material")
BASE_PDF = os.path.join(SRC, "2026-08-31-complete",
                        "The_Clarity_Compass_COMPLETE_UPDATED_Aug31_2026.pdf")
BASE_DATE = "2026-08-31"
REV_DIR = os.path.join(SRC, "2026-09-chapter-revisions")

WORDS = ["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE",
         "TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN",
         "SIXTEEN", "SEVENTEEN"]
NUM = {w: i + 1 for i, w in enumerate(WORDS)}

# Chapter revisions Merrill sent after the base complete manuscript.
OVERRIDES = {
    1:  ("Clarity_Compass_Chapter_One_Revised_Draft_Sept_1_2026.docx", "2026-09-01"),
    2:  ("Clarity_Compass_Chapter_Two_Revised_Draft_Sept_1_2026.docx", "2026-09-01"),
    3:  ("Clarity_Compass_Chapter_Three_Revised_Draft_Sept_1_2026.docx", "2026-09-01"),
    6:  ("Clarity_Compass_Chapter_Six_Revised_Draft_Sept_1_2026.docx", "2026-09-01"),
    15: ("Clarity_Compass_Chapter_Fifteen_Revised_Draft_Sept_2_2026.docx", "2026-09-02"),
}


def slug(title):
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return re.sub(r"-+", "-", s)


def split_base():
    """Return ordered [(kind, num, title, body)] from the complete manuscript."""
    md = pdf2md.convert(BASE_PDF)
    parts = re.split(r"^# (.+)$", md, flags=re.M)[1:]
    sections, pending_divider = [], None
    for head, body in zip(parts[0::2], parts[1::2]):
        body = body.strip()
        if head == "YOUR COMPASS":
            if sections:                       # end-of-part exercise
                sections[-1][3] += "\n\n## Your Compass\n\n" + body
            continue
        if head in pdf2md.PARTS:               # part-divider page
            sub = [l.strip() for l in body.split("\n") if l.strip() and l.strip() != "---"]
            pending_divider = (head, sub[0] if sub else "", "\n\n".join(sub[1:]))
            continue
        m = re.match(r"CHAPTER (\w+)$", head)
        if m:
            n = NUM[m.group(1)]
            tm = re.match(r"## (.+?)\n", body + "\n")
            title = tm.group(1).strip() if tm else f"Chapter {n}"
            body = body[tm.end():].strip() if tm else body
            sections.append(["chapter", n, title, body, pending_divider])
            pending_divider = None
        else:
            title = head.title() if head.isupper() else head
            sections.append(["front" if not sections else "back", None, title, body, None])
    return sections


def load_override(path):
    """Chapter docx -> (title, body). Word spells the header C H A P T E R  O N E."""
    md = docx2md.convert(path)
    lines = [l for l in md.split("\n")]
    out, title = [], None
    for line in lines:
        s = line.strip()
        if not s:
            if title is not None:
                out.append("")
            continue
        if re.fullmatch(r"(?:C\s*H\s*A\s*P\s*T\s*E\s*R)\s+[A-Z\s]+", s):
            continue
        if title is None:
            title = s.lstrip("# ").strip()
            continue
        out.append(line)
    body = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()
    body = re.sub(r"^\*\s+\*\s+\*$", "---", body, flags=re.M)
    return title, body


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

    sections = split_base()
    files, idx = [], 0
    for kind, n, title, body, divider in sections:
        source, sdate = os.path.basename(BASE_PDF), BASE_DATE
        if kind == "chapter" and n in OVERRIDES:
            fname, sdate = OVERRIDES[n]
            title, body = load_override(os.path.join(REV_DIR, fname))
            source = fname
        name = f"{idx:02d}-{slug(title)}.md"
        heading = f"Chapter {n}. {title}" if kind == "chapter" else title
        fm = ["---",
              f"title: {title}",
              f"chapter: {n if n else 'null'}",
              f"source_file: {source}",
              f"source_date: {sdate}",
              "---", ""]
        if divider:
            pname, sub, intro = divider
            fm.append(f"> **Part: {pname.title()}** — {sub}\n" if sub
                      else f"> **Part: {pname.title()}**\n")
            if intro:
                fm.append("> " + intro.replace("\n\n", "\n>\n> ") + "\n")
        front = "\n".join(fm).rstrip() + "\n\n"
        open(os.path.join(book, name), "w").write(front + f"# {heading}\n\n{body}\n")
        files.append((name, heading, body))
        idx += 1

    full = ["# The Clarity Compass",
            "",
            "Merrill Fausett and Brody Fausett",
            "",
            f"Assembled from Merrill's sends. Base manuscript {BASE_DATE}; "
            f"chapters {', '.join(str(k) for k in sorted(OVERRIDES))} replaced by his "
            "later per-chapter revisions.",
            "", "---", ""]
    for name, heading, body in files:
        full.append(f"# {heading}\n\n{body}\n\n---\n")
    open(os.path.join(ROOT, "clarity-compass-FULL-BOOK.md"), "w").write("\n".join(full))

    total = sum(len(b.split()) for _, _, b in files)
    print(f"{len(files)} files, {total:,} words")
    for name, heading, body in files:
        print(f"  {name:52s} {len(body.split()):6,} words")


if __name__ == "__main__":
    main()
