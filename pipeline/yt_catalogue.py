#!/usr/bin/env python3
"""
Look up the FULL-LENGTH YouTube URL for a track.

The full songs are not on @PhilosophicalKingMusic — that channel only holds our
own lyric Shorts. They are on the auto-generated `Philosophical King - Topic`
channel (UCST1Tzuraa0CSR4o3RkVIMw), where DistroKid delivers them.

That channel is search-suppressed: searching YouTube or YouTube Music for the
channel or for any track title returns nothing at all. Never conclude from a
search that a track is absent — look it up here, or by video ID.

Data: music-assets/youtube-tracks.json (257 tracks). Refresh notes and the
enumeration method are in music-assets/YOUTUBE-CATALOGUE.md.

These are streams, not files. Good for Substack embeds and Reddit link posts;
NOT an audio source for the renderer.
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOGUE = os.path.join(ROOT, "music-assets", "youtube-tracks.json")


def _key(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def _load():
    if not os.path.exists(CATALOGUE):
        return []
    return json.load(open(CATALOGUE, encoding="utf-8"))


def full_song(slug=None, title=None):
    """
    Full-length watch URL for a track, or None.

    Matches on slug first, then on title with punctuation and case stripped —
    titles drift between our queue and YouTube ("Voltaire's Vision" vs
    "Voltaire’s Vision"), so an exact compare misses.
    """
    tracks = _load()
    if slug:
        for t in tracks:
            if t.get("slug") == slug:
                return t["url"]
    for want in (slug, title):
        if not want:
            continue
        k = _key(want.replace("-", " ") if want is slug else want)
        for t in tracks:
            if _key(t.get("title")) == k or _key(t.get("slug", "").replace("-", " ")) == k:
                return t["url"]
    return None


if __name__ == "__main__":
    import sys
    for a in sys.argv[1:]:
        print(f"{a}: {full_song(slug=a, title=a) or 'NOT FOUND'}")
