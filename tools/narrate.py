#!/usr/bin/env python3
"""narrate.py — render a chapter of the book to an audiobook track with Kokoro.

Kokoro is local, offline, and free, so a full read costs nothing but CPU time.
Output is forced to 44.1kHz because 24kHz audio (Kokoro's native rate) does not
arrive as a playable voice message in iMessage.

Usage: narrate.py book/01-abandon-ship.md [out.m4a] [--voice am_michael]
"""
import os
import re
import subprocess
import sys

HQ = os.path.expanduser("~/HQ")
KOKORO_DIR = os.path.join(HQ, "code", "kokoro-tts")
sys.path.insert(0, KOKORO_DIR)
MODEL = os.path.join(KOKORO_DIR, "models", "kokoro-v1.0.onnx")
VOICES = os.path.join(KOKORO_DIR, "models", "voices-v1.0.bin")

MAX_CHARS = 700          # Kokoro degrades on very long single calls
PARA_PAUSE = 0.35        # seconds of silence between paragraphs
SECTION_PAUSE = 1.0      # after a heading or a scene break


def clean(md):
    """Markdown -> speakable prose. Returns [(text, pause_after)]."""
    md = re.sub(r"^---\n.*?\n---\n", "", md, flags=re.S)      # frontmatter
    blocks = []
    for raw in md.split("\n\n"):
        p = raw.strip()
        if not p:
            continue
        if re.fullmatch(r"[-*_—\s]{3,}", p):             # scene break
            blocks.append((None, SECTION_PAUSE))
            continue
        pause = PARA_PAUSE
        if p.startswith("#"):
            p = p.lstrip("#").strip()
            pause = SECTION_PAUSE
        if p.startswith(">"):
            p = re.sub(r"^>\s?", "", p, flags=re.M)
        p = re.sub(r"\*\*(.+?)\*\*", r"\1", p)
        p = re.sub(r"\*(.+?)\*", r"\1", p)
        p = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", p)
        p = p.replace("—", ", ").replace("–", ", ")  # dashes -> a beat
        p = re.sub(r"\s+", " ", p).strip()
        if p:
            blocks.append((p, pause))
    return blocks


def chunks(text):
    """Split a paragraph into sentence groups under MAX_CHARS."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    out, cur = [], ""
    for s in sentences:
        if len(cur) + len(s) + 1 > MAX_CHARS and cur:
            out.append(cur.strip())
            cur = s
        else:
            cur = (cur + " " + s).strip()
    if cur:
        out.append(cur)
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    voice = "am_michael"
    for a in sys.argv[1:]:
        if a.startswith("--voice"):
            voice = a.split("=", 1)[1] if "=" in a else "am_michael"
    src = args[0]
    out = args[1] if len(args) > 1 else os.path.splitext(src)[0] + ".m4a"

    from kokoro_onnx import Kokoro
    import numpy as np
    import soundfile as sf

    kokoro = Kokoro(MODEL, VOICES)
    blocks = clean(open(src).read())
    pieces, sr, done = [], None, 0
    total = sum(1 for t, _ in blocks if t)
    for text, pause in blocks:
        if text is None:
            if sr:
                pieces.append(np.zeros(int(sr * pause), dtype=np.float32))
            continue
        for c in chunks(text):
            samples, sr = kokoro.create(c, voice=voice, speed=1.0, lang="en-us")
            pieces.append(samples.astype(np.float32))
        done += 1
        pieces.append(np.zeros(int(sr * pause), dtype=np.float32))
        print(f"  {done}/{total} paragraphs", file=sys.stderr, flush=True)

    audio = np.concatenate(pieces)
    wav = out + ".tmp.wav"
    sf.write(wav, audio, sr)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav,
                    "-ar", "44100", "-ac", "1", "-b:a", "128k", out], check=True)
    os.remove(wav)
    print(f"{out}  {len(audio)/sr/60:.1f} min  voice={voice}")


if __name__ == "__main__":
    main()
