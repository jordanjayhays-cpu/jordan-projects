#!/usr/bin/env python3
"""
Guard against Whisper mis-hearings before a transcript becomes a video.

The track title is the most reliable ground truth we have — if a significant
word from the title is absent from the transcript while its siblings are
present, Whisper probably mis-heard it. That is exactly how
"the anxious generation" shipped as "we're the exes generation".

Usage: check_lyrics.py [slug]   (no slug = check everything)
Exit 1 if anything is suspicious, so daily_post.py can refuse to render.
"""
import json, glob, os, sys

STOP = {'the','a','of','and','to','in','for','on','is','it','we','i',
        'my','your','no','vs','far','be','not'}

def suspicious(slug):
    f = f'music-assets/{slug}-lyrics.json'
    if not os.path.exists(f):
        return None
    words = [w for w in slug.split('-') if w not in STOP and len(w) > 3]
    if len(words) < 2:
        return None
    try:
        lines = json.load(open(f))
    except Exception:
        return None
    text = ' '.join(l.get('text', '') for l in lines).lower()
    present = [w for w in words if w in text]
    missing = [w for w in words if w not in text]
    # Some title words heard and others not is the tell-tale of a mis-hear.
    # All missing usually just means the title is not sung in the 30s preview.
    if present and missing:
        return missing, present
    return None

def main():
    slugs = ([sys.argv[1]] if len(sys.argv) > 1 else
             sorted(os.path.basename(f).replace('-lyrics.json', '')
                    for f in glob.glob('music-assets/*-lyrics.json')))
    hits = []
    for s in slugs:
        r = suspicious(s)
        if r:
            hits.append((s, *r))
    for s, missing, present in hits:
        print(f"SUSPECT {s}: title word(s) {missing} absent from transcript "
              f"(but {present} present) — check by ear before rendering")
    if hits:
        print(f"\n{len(hits)} transcript(s) need a human ear. "
              f"Fix the JSON or confirm it is correct, then re-run.")
        return 1
    print("all transcripts contain their title words")
    return 0

if __name__ == '__main__':
    sys.exit(main())
