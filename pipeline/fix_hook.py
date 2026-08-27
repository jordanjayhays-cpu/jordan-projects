#!/usr/bin/env python3
"""Replace the hook line on an already-scheduled day, across every social channel.

pick_hook() gets roughly seven in ten right. The other three are mush, because
Whisper breaks on breath rather than on clauses and a bad transcript compounds
that. Fixing it by hand in the Postiz UI means four edits and a re-upload each
time, so this does it in one call.

    POSTIZ_KEY=... python3 pipeline/fix_hook.py 2026-09-10 "Laughing so hard that the summer almost broke"

TWO TRAPS, both of which have already cost a day's posts:

1. The two endpoints disagree on field names. /integrations calls it
   `identifier`; the integration nested inside /posts calls it
   `providerIdentifier`. Reading the wrong one returns None for every channel,
   which silently matches nothing.

2. The list endpoint does not return attachments, so a post rebuilt from what
   the list gives you loses its video. We re-upload the teaser from
   raw.githubusercontent the same way daily_post.py does.

Order matters: schedule the replacements FIRST, and only delete the originals
once they exist. Deleting first leaves the day empty if anything downstream
fails.

Reddit is left alone on purpose: it carries its own community wording and a full
song link, not the hook.
"""
import json
import os
import re
import subprocess
import sys
import urllib.request

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


def api(path, method="GET", body=None):
    req = urllib.request.Request(
        API + path, method=method,
        headers={"Authorization": KEY, "Content-Type": "application/json"},
        data=json.dumps(body).encode() if body else None)
    raw = urllib.request.urlopen(req, timeout=120).read()
    return json.loads(raw) if raw else {}


def posts_on(day):
    d = api(f"posts?startDate={day}T00:00:00.000Z&endDate={day}T23:59:59.000Z"
            f"&customer=&display=day&day=0&week=0&month=0&year={day[:4]}")
    return d.get("posts", d if isinstance(d, list) else [])


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    day, hook = sys.argv[1], sys.argv[2].strip()

    existing = posts_on(day)
    if not existing:
        sys.exit(f"no posts scheduled on {day}")

    # providerIdentifier, NOT identifier — see the docstring.
    social = [p for p in existing
              if (p.get("integration") or {}).get("providerIdentifier") != "reddit"]
    if not social:
        sys.exit(f"nothing but reddit on {day} — nothing to fix")
    if any(p.get("state") == "PUBLISHED" for p in social):
        sys.exit(f"{day} is already published — too late to change the hook")

    old = social[0].get("content") or ""
    m = re.search(r"Track (\d+) of (\d+)", old)
    if not m:
        sys.exit(f"could not find the series line in the existing caption:\n{old}")
    series_no, catalogue = m.group(1), m.group(2)

    state = json.load(open(os.path.join(PIPE, "state.json")))
    slug = state.get("schedule", {}).get(day)
    if slug is None:
        sys.exit(f"state.json has no track recorded against {day}")
    title = slug.replace("-", " ").title()

    # Keep the title line the live caption already carries rather than
    # regenerating it from the slug — "Dolce Far Niente" is not what
    # "dolce-far-niente".title() produces for every track.
    live_title = None
    tm = re.search(r"</p>\s*<p>(.*?)</p>\s*<p>Track \d+ of", old, re.S)
    if tm and tm.group(1).strip():
        live_title = tm.group(1).strip()

    content = (f"<p>{hook} 👑</p>"
               + (f"<p>{live_title}</p>" if live_title else f"<p>{title}</p>")
               + f"<p>Track {series_no} of {catalogue} — turning every idea in "
                 f"philosophy into a song.</p>"
                 f"<p>Full track everywhere: {TRACK_LINK}</p>"
                 f"<p>#Philosophy #PhilosophicalKing</p>")

    channels = [(p.get("integration") or {}).get("providerIdentifier") for p in social]
    print(f"track:    {slug}")
    print(f"was:      {re.sub(r'<[^>]+>', ' ', old).strip()[:80]}")
    print(f"now:      {hook}")
    print(f"channels: {channels}")

    up = mcp("uploadFromUrlTool", {"url": f"{RAW}{slug}-teaser.mp4"})

    rebuilt = []
    for integ in mcp("integrationList", {})["output"]:
        plat = integ["platform"]
        if plat == "reddit" or plat not in channels:
            continue
        settings = platform_settings(plat, title)
        if settings is None:
            print(f"skipping {plat}: not configured")
            continue
        rebuilt.append({"integrationId": integ["id"], "isPremium": False,
                        "date": f"{day}T{STAGGER.get(plat, '08:00:00')}",
                        "shortLink": False, "type": "schedule",
                        "postsAndComments": [{"content": content,
                                              "attachments": [up["path"]]}],
                        "settings": settings})
    if len(rebuilt) != len(social):
        sys.exit(f"would rebuild {len(rebuilt)} of {len(social)} posts — refusing "
                 f"to delete anything. Channels found: {channels}")

    res = mcp("integrationSchedulePostTool", {"socialPost": rebuilt})
    made = res.get("output") or []
    if len(made) != len(rebuilt):
        sys.exit(f"scheduled only {len(made)} of {len(rebuilt)} — originals left "
                 f"in place, remove the duplicates by hand")

    # Only now that the replacements exist is it safe to drop the originals.
    for p in social:
        api(f"posts/{p['id']}", method="DELETE")
    print(f"rewrote {len(made)} post(s) on {day}")

    subprocess.call(["git", "-C", ROOT, "-c", "user.name=Claude",
                     "-c", "user.email=noreply@anthropic.com",
                     "commit", "-q", "--allow-empty",
                     "-m", f"pipeline: corrected the hook on {day} ({slug})"])


if __name__ == "__main__":
    main()
