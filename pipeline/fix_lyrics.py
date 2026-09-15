#!/usr/bin/env python3
"""Apply pipeline/lyric-fixes.json to the transcripts on disk.

    python3 pipeline/fix_lyrics.py            # every slug in the fixes file
    python3 pipeline/fix_lyrics.py dk         # one slug
    python3 pipeline/fix_lyrics.py --check    # report, change nothing

Whisper gets proper nouns and homophones wrong often enough that the errors
reach the screen: "Dunning-Kruger" came through as "done in Kruger", "in flux"
as "influx", "a maze in the dark" as "amazing, the dark". The transcript is the
lyric layer of every video, so an error here is an error the audience reads.

A fix only lands if `was` matches the segment exactly. If it does not, the fix
is reported and skipped rather than forced — a segment that has changed since
the fix was written may have different timings, and dropping corrected words
onto the wrong moment is worse than the original error.

daily_post.py calls apply() for the current track before rendering, so a slug
listed here is corrected the moment it is transcribed, not afterwards.
"""
import json
import os
import sys

PIPE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(PIPE), "music-assets")
FIXES = os.path.join(PIPE, "lyric-fixes.json")


def load():
    with open(FIXES) as f:
        return {k: v for k, v in json.load(f).items() if not k.startswith("_")}


def apply(slug, lines, report=print):
    """Correct `lines` in place. Returns the number of fixes applied."""
    fixes = load().get(slug)
    if not fixes:
        return 0
    n = 0
    for fix in fixes:
        i, was, now = fix["i"], fix["was"], fix["now"]
        if i >= len(lines):
            report(f"  ! {slug}[{i}]: past the end of a {len(lines)}-segment "
                   f"transcript — skipped")
            continue
        have = lines[i]["text"]
        if have == now:
            continue                      # already corrected
        if have != was:
            report(f"  ! {slug}[{i}]: expected {was!r}, found {have!r} — skipped")
            continue
        lines[i]["text"] = now
        report(f"  · {slug}[{i}]: {was!r} -> {now!r}")
        n += 1
    return n


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    check = "--check" in sys.argv
    slugs = args or sorted(load())

    total = 0
    for slug in slugs:
        path = os.path.join(ASSETS, f"{slug}-lyrics.json")
        if not os.path.exists(path):
            print(f"{slug}: no transcript on disk — skipped")
            continue
        lines = json.load(open(path))
        n = apply(slug, lines)
        if n and not check:
            json.dump(lines, open(path, "w"), indent=1)
        print(f"{slug}: {n} fix(es){' (check only, not written)' if check and n else ''}")
        total += n
    print(f"{total} fix(es) total")


if __name__ == "__main__":
    main()
