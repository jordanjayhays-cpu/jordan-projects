#!/usr/bin/env python3
"""Rewrite queued captions into the current format, without re-rendering.

    POSTIZ_KEY=... python3 pipeline/reformat_captions.py 2026-08-31 2026-09-11
    POSTIZ_KEY=... python3 pipeline/reformat_captions.py 2026-08-31 2026-09-11 --dry-run

The em dash reads as AI-written, so captions moved to a colon after the title
and a full stop before the series line. Days already scheduled kept the old
shape. Only the text changes here: the video is untouched, so this is fast.

Same two traps as the other Postiz tooling. The integration inside /posts calls
the field `providerIdentifier` while /integrations calls it `identifier`. And
the list endpoint hides attachments, so the teaser is re-uploaded rather than
rebuilt from what the list returns, or the post loses its video.

Replacements are scheduled before the originals are deleted, and nothing is
deleted unless every channel rebuilt.
"""
import json, os, re, subprocess, sys, urllib.request
from datetime import date, timedelta

PIPE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(PIPE)
KEY = os.environ["POSTIZ_KEY"]
API = "https://api.postiz.com/public/v1/"
RAW = ("https://raw.githubusercontent.com/jordanjayhays-cpu/jordan-projects/"
       "claude/philosophical-king-poster-raq2ke/music-assets/")
STAGGER = {"youtube": "08:00:00", "facebook": "08:03:00",
           "instagram-standalone": "08:07:00", "instagram": "08:07:00",
           "tiktok": "08:14:00"}

sys.path.insert(0, PIPE)
from daily_post import mcp, platform_settings, TRACK_LINK  # noqa: E402


def api(path, method="GET"):
    req = urllib.request.Request(API + path, method=method,
        headers={"Authorization": KEY, "Content-Type": "application/json"})
    raw = urllib.request.urlopen(req, timeout=120).read()
    return json.loads(raw) if raw else {}


def posts_on(day):
    d = api(f"posts?startDate={day}T00:00:00.000Z&endDate={day}T23:59:59.000Z"
            f"&customer=&display=day&day=0&week=0&month=0&year={day[:4]}")
    return d.get("posts", d if isinstance(d, list) else [])


def plat(p):
    return (p.get("integration") or {}).get("providerIdentifier")


def do_day(day, dry):
    existing = posts_on(day)
    social = [p for p in existing if plat(p) != "reddit"]
    if not social:
        return f"{day}: nothing to do"
    if any(p.get("state") == "PUBLISHED" for p in social):
        return f"{day}: already published, skipped"

    old = social[0].get("content") or ""
    flat = re.sub(r"<[^>]+>", "\n", old)
    first = next((l.strip() for l in flat.split("\n") if l.strip()), "")
    if "Track " not in re.sub(r"<[^>]+>", " ", old) and " — " not in first:
        return f"{day}: already in the current format, skipped"

    sep = " — " if " — " in first else ": "
    title, hook = first.split(sep, 1)
    hook = hook.replace("👑", "").strip()

    content = (f"<p>{title}: {hook} 👑</p>"
               f"<p>Turning every idea in philosophy into a song.</p>"
               f"<p>Full track everywhere: {TRACK_LINK}</p>"
               f"<p>#Philosophy #PhilosophicalKing</p>")

    if dry:
        return f"{day}: {title}: {hook}"

    slug = json.load(open(os.path.join(PIPE, "state.json"))).get("schedule", {}).get(day)
    if not slug:
        return f"{day}: no slug in state.schedule, skipped"
    video = f"{slug}-teaser-v2.mp4"
    if not os.path.exists(os.path.join(ROOT, "music-assets", video)):
        video = f"{slug}-teaser.mp4"
    up = mcp("uploadFromUrlTool", {"url": RAW + video})

    channels = [plat(p) for p in social]
    rebuilt = []
    for integ in mcp("integrationList", {})["output"]:
        p_ = integ["platform"]
        if p_ == "reddit" or p_ not in channels:
            continue
        settings = platform_settings(p_, title)
        if settings is None:
            continue
        rebuilt.append({"integrationId": integ["id"], "isPremium": False,
                        "date": f"{day}T{STAGGER.get(p_, '08:00:00')}",
                        "shortLink": False, "type": "schedule",
                        "postsAndComments": [{"content": content,
                                              "attachments": [up["path"]]}],
                        "settings": settings})
    if len(rebuilt) != len(social):
        return f"{day}: would rebuild {len(rebuilt)} of {len(social)}, REFUSED"

    made = (mcp("integrationSchedulePostTool", {"socialPost": rebuilt}).get("output") or [])
    if len(made) != len(rebuilt):
        return f"{day}: scheduled {len(made)} of {len(rebuilt)}, originals LEFT, clean up by hand"
    for p in social:
        api(f"posts/{p['id']}", method="DELETE")
    return f"{day}: rewrote {len(made)} — {title}: {hook}"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    if len(args) < 2:
        sys.exit(__doc__)
    d, end = date.fromisoformat(args[0]), date.fromisoformat(args[1])
    while d <= end:
        try:
            print(do_day(d.isoformat(), dry), flush=True)
        except Exception as e:
            print(f"{d}: FAILED {type(e).__name__}: {e}", flush=True)
        d += timedelta(days=1)


if __name__ == "__main__":
    main()
