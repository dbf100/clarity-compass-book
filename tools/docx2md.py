#!/usr/bin/env python3
"""docx2md.py — convert a .docx manuscript to clean Markdown.

Heading-aware (maps Word Heading 1/2/3 to #/##/###), keeps blockquotes for
Word "Quote"/"Intense Quote" styles, and renders tables as pipe tables.
Book text is kept FAITHFUL to the author (em-dashes and all).

Usage: docx2md.py IN.docx [OUT.md]
"""
import sys
import re
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph


def iter_blocks(doc):
    body = doc.element.body
    for child in body.iterchildren():
        tag = child.tag.split('}')[-1]
        if tag == 'p':
            yield Paragraph(child, doc)
        elif tag == 'tbl':
            yield Table(child, doc)


def para_md(p):
    text = p.text.strip()
    if not text:
        return ''
    style = (p.style.name or '').lower()
    m = re.match(r'heading (\d)', style)
    if m:
        return '#' * min(int(m.group(1)), 6) + ' ' + text
    if 'quote' in style:
        return '> ' + text
    if 'title' in style:
        return '# ' + text
    if 'subtitle' in style:
        return '## ' + text
    if 'list' in style:
        return '- ' + text
    return text


def table_md(t):
    rows = [[c.text.strip().replace('\n', ' ') for c in r.cells] for r in t.rows]
    if not rows:
        return ''
    width = max(len(r) for r in rows)
    rows = [r + [''] * (width - len(r)) for r in rows]
    out = ['| ' + ' | '.join(rows[0]) + ' |',
           '| ' + ' | '.join(['---'] * width) + ' |']
    for r in rows[1:]:
        out.append('| ' + ' | '.join(r) + ' |')
    return '\n'.join(out)


def convert(path):
    doc = Document(path)
    parts = []
    for block in iter_blocks(doc):
        md = para_md(block) if isinstance(block, Paragraph) else table_md(block)
        if md:
            parts.append(md)
    text = '\n\n'.join(parts)
    return re.sub(r'\n{3,}', '\n\n', text).strip() + '\n'


if __name__ == '__main__':
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    md = convert(src)
    if out:
        open(out, 'w').write(md)
        print(f'{out}  {len(md.split())} words')
    else:
        sys.stdout.write(md)
