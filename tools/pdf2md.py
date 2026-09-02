#!/usr/bin/env python3
"""pdf2md.py — convert the Clarity Compass print PDF back to clean Markdown.

The print PDF hard-wraps lines. PyMuPDF preserves a trailing space on every
wrapped line and drops it on the last line of a paragraph, so that is the
signal used to rejoin paragraphs. Page numbers (bare digits) are dropped.
Section headings (FOREWORD / CHAPTER X / APPENDIX / ABOUT THE AUTHORS /
YOUR COMPASS / APPLICATION) become Markdown headings.

Usage: pdf2md.py IN.pdf [OUT.md]
"""
import re
import sys
import fitz

# Part-divider pages (NORTH / EAST / SOUTH / MAGNETIC NORTH / APPLICATION) sit
# between chapters and would otherwise be swallowed into the previous chapter.
PARTS = ('NORTH', 'EAST', 'SOUTH', 'WEST', 'MAGNETIC NORTH', 'APPLICATION')
TOP = re.compile(r'^(FOREWORD|APPENDIX|ABOUT THE AUTHORS|YOUR COMPASS|'
                 r'NORTH|EAST|SOUTH|WEST|MAGNETIC NORTH|APPLICATION|'
                 r'CHAPTER (?:ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN|'
                 r'ELEVEN|TWELVE|THIRTEEN|FOURTEEN|FIFTEEN|SIXTEEN|SEVENTEEN))$')


def raw_lines(path):
    doc = fitz.open(path)
    for page in doc:
        for line in page.get_text("text").split("\n"):
            if not line.strip():
                yield ""          # blank -> hard paragraph break
                continue
            if re.fullmatch(r'\d{1,3}', line.strip()):
                continue          # page number
            yield line


def paragraphs(path):
    buf = ""
    for line in raw_lines(path):
        if line == "":
            if buf.strip():
                yield buf.strip()
            buf = ""
            continue
        stripped = line.strip()
        if TOP.match(stripped):
            if buf.strip():
                yield buf.strip()
            buf = ""
            yield ("HEADING", stripped)
            continue
        # A line ending in a hyphen is a word broken across the line; keep the
        # hyphen for now and let dehyphenate() decide using the rest of the text.
        if line.endswith(" "):
            buf += line
        elif line.rstrip().endswith("-"):
            buf += line.rstrip() + "\x00"
        else:
            buf += line.rstrip() + "\n@@BREAK@@"
        if buf.endswith("@@BREAK@@"):
            for piece in buf.split("\n@@BREAK@@"):
                if piece.strip():
                    yield piece.strip()
            buf = ""
    if buf.strip():
        yield buf.strip()


def convert(path):
    out = []
    pending_title = False
    for p in paragraphs(path):
        if isinstance(p, tuple):
            out.append("# " + p[1])
            pending_title = p[1].startswith("CHAPTER")
            continue
        if pending_title:
            out.append("## " + p)
            pending_title = False
            continue
        if re.fullmatch(r'[—\-\*\s]{3,}', p) or p == "\u2295":
            out.append("---")
            continue
        # The typeset PDF repeats a chapter subtitle on the divider page and
        # again on the chapter opener. Collapse the immediate repeat.
        if out and out[-1] == p:
            continue
        out.append(p)
    # A wrapped line that ends right before an em-dash continuation gets split
    # by the trailing-space rule. Re-join any paragraph that opens with a dash.
    merged = []
    for para in out:
        if merged and para.startswith(("\u2014", "\u2013")) and not merged[-1].startswith("#"):
            merged[-1] = merged[-1].rstrip() + para
        else:
            merged.append(para)
    return dehyphenate("\n\n".join(merged).strip() + "\n")


def dehyphenate(text):
    """Resolve words the typesetter broke across a line.

    Each break is marked with a NUL after the hyphen. "open-\x00boat" is either
    a real compound (open-boat) or a split word (extraor-dinary). Decide from
    the rest of the manuscript: if the closed-up form appears elsewhere, use it;
    otherwise keep the hyphen, which is the safer default for compounds.
    """
    corpus = set(re.findall(r"[A-Za-z]+", text.replace("\x00", "")))
    def fix(m):
        a, b = m.group(1), m.group(2)
        joined = a + b
        if joined.lower() in {w.lower() for w in corpus} and (a + "-" + b) not in text:
            return joined
        return a + "-" + b
    return re.sub(r"([A-Za-z]+)-\x00([A-Za-z]+)", fix, text)


if __name__ == "__main__":
    md = convert(sys.argv[1])
    if len(sys.argv) > 2:
        open(sys.argv[2], "w").write(md)
        print(f"{sys.argv[2]}  {len(md.split())} words")
    else:
        sys.stdout.write(md)
