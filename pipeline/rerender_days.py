#!/usr/bin/env python3
"""Re-render already-scheduled teasers and swap them into the queue.

    POSTIZ_KEY=... python3 pipeline/rerender_days.py 2026-09-05 2026-09-10
    POSTIZ_KEY=... python3 pipeline/rerender_days.py 2026-09-05 2026-09-10 --dry-run

Written for the lyric-correction pass: pipeline/lyric-fixes.json changed what
the transcript says, but the videos in the queue were rendered before that and
still show the old words. The captions are already right, so this changes the
VIDEO only and rebuilds the posts around it unchanged.

The three things this is careful about are the same three that have bitten
before, and none of them are optional:

- raw.githubusercontent is CDN-cached, so a re-render must go to a NEW
  filename. Re-pushing the same path can serve Postiz the stale file and the
  whole run silently does nothing. Each day gets the next free -vN.
- Replacements are scheduled BEFORE the originals are deleted, and nothing is
  deleted unless every channel rebuilt. Deleting first once left a day empty.
- The integration inside /posts calls the field `providerIdentifier`;
  /integrations calls the same thing `identifier`. Reading the wrong one
  matches nothing at all, silently.

Title and hook are carried over from the live posts rather than regenerated.
The store titles are Jordan's, typos included ("Infinite Possbilities"), and
the hooks on these days were fixed by hand already. Reddit is skipped: it
carries its own wording and a full-song link.
"""
import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import date, timedelta

PIPE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(PIPE)
ASSETS = os.path.join(ROOT, "music-assets")
KEY = os.environ["POSTIZ_KEY"]
API = "https://api.postiz.com/public/v1/"
BRANCH = "claude/philosophical-king-poster-raq2ke"
RAW = (f"https://raw.githubusercontent.com/jordanjayhays-cpu/jordan-projects/"
       f"{BRANCH}/music-assets/")
STAGGER = {"youtube": "08:00:00", "facebook": "08:03:00",
           "instagram-standalone": "08:07:00", "instagram": "08:07:00",
           "tiktok": "08:14:00"}

sys.path.insert(0, PIPE)
from daily_post import mcp, platform_settings, TRACK_LINK  # noqa: E402


def api(path, method="GET"):
    req = urllib.request.Request(
        API + path, method=method,
        headers={"Authorization": KEY, "Content-Type": "application/json"})
    raw = urllib.request.urlopen(req, timeout=120).read()
    return json.loads(raw) if raw else {}


def posts_on(day):
    d = api(f"posts?startDate={day}T00:00:00.000Z&endDate={day}T23:59:59.000Z"
            f"&customer=&display=day&day=0&week=0&month=0&year={day[:4]}")
    return d.get("posts", d if isinstance(d, list) else [])


def plat(post):
    return (post.get("integration") or {}).get("providerIdentifier")


def title_from(posts):
    for p in posts:
        s = p.get("settings")
        if isinstance(s, str):
            try:
                s = json.loads(s)
            except ValueError:
                continue
        t = ((s or {}).get("title") or "").split(" | Philosophical King")[0].strip()
        if t:
            return t
    return None


def next_version(slug):
    """The next unused -vN filename. Never overwrite: the CDN caches by path."""
    n = 2
    while os.path.exists(os.path.join(ASSETS, f"{slug}-teaser-v{n}.mp4")):
        n += 1
    return f"{slug}-teaser-v{n}.mp4"


def render(slug, title, hook):
    src = next(os.path.join(ASSETS, f)
               for f in (f"{slug}-teaser.mp4", f"{slug}-teaser-v2.mp4")
               if os.path.exists(os.path.join(ASSETS, f)))
    art = os.path.join(ASSETS, f"{slug}-art.jpg")
    lyr = os.path.join(ASSETS, f"{slug}-lyrics.json")
    for path in (art, lyr):
        if not os.path.exists(path):
            raise FileNotFoundError(path)

    wav = f"/tmp/{slug}-rerender.wav"
    subprocess.check_call(["ffmpeg", "-nostdin", "-y", "-loglevel", "error",
                           "-i", src, "-vn", "-ac", "1", "-ar", "44100", wav])
    name = next_version(slug)
    subprocess.check_call([sys.executable, os.path.join(PIPE, "kinetic_render.py"),
                           slug, title, hook, "hyperfollow.com/PhilosophicalKing",
                           art, wav, lyr, os.path.join(ASSETS, name)])
    os.remove(wav)
    return name


def do_day(day, slug, dry):
    existing = posts_on(day)
    social = [p for p in existing if plat(p) != "reddit"]
    if not social:
        return f"{day} {slug}: nothing but reddit — skipped"
    if any(p.get("state") == "PUBLISHED" for p in social):
        return f"{day} {slug}: already published — skipped"

    title = title_from(social)
    content = social[0].get("content") or ""
    m = re.match(r"\s*<p>(.*?)</p>", content, re.S)
    first = re.sub(r"<[^>]+>", "", m.group(1)).strip().replace("👑", "").strip() if m else ""
    hook = first.split(": ", 1)[1].strip() if ": " in first else first
    if not (title and hook):
        return f"{day} {slug}: could not recover title/hook — skipped"

    channels = [plat(p) for p in social]
    if dry:
        return f"{day} {slug}: WOULD re-render {title!r} / {hook!r} for {channels}"

    video = render(slug, title, hook)
    subprocess.check_call(["git", "-C", ROOT, "add", f"music-assets/{video}"])
    subprocess.call(["git", "-C", ROOT, "-c", "user.name=Claude",
                     "-c", "user.email=noreply@anthropic.com", "commit", "-q",
                     "-m", f"pipeline: re-rendered {slug} with the corrected lyrics"])
    subprocess.check_call(["git", "-C", ROOT, "push", "-q", "origin", BRANCH])

    up = mcp("uploadFromUrlTool", {"url": RAW + video})

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
        return (f"{day} {slug}: would rebuild {len(rebuilt)} of {len(social)} — "
                f"REFUSED, nothing deleted")

    made = (mcp("integrationSchedulePostTool", {"socialPost": rebuilt})
            .get("output") or [])
    if len(made) != len(rebuilt):
        return (f"{day} {slug}: scheduled {len(made)} of {len(rebuilt)} — originals "
                f"LEFT IN PLACE, remove the duplicates by hand")

    for p in social:
        api(f"posts/{p['id']}", method="DELETE")
    return f"{day} {slug}: rebuilt {len(made)} posts on {video}"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    if len(args) < 2:
        sys.exit(__doc__)
    start, end = date.fromisoformat(args[0]), date.fromisoformat(args[1])
    schedule = json.load(open(os.path.join(PIPE, "state.json"))).get("schedule", {})

    day = start
    while day <= end:
        key = day.isoformat()
        slug = schedule.get(key)
        if not slug:
            print(f"{key}: nothing in state.schedule — skipped", flush=True)
        else:
            try:
                print(do_day(key, slug, dry), flush=True)
            except Exception as exc:      # one bad day must not stop the rest
                print(f"{key} {slug}: FAILED — {type(exc).__name__}: {exc}", flush=True)
        day += timedelta(days=1)


if __name__ == "__main__":
    main()
