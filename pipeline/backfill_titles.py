#!/usr/bin/env python3
"""Re-render and re-caption already-scheduled days so they carry the song title.

The title landed in the pipeline on 2026-08-27, by which point the queue was
already fourteen days deep — Aug 28 to Sep 10 were rendered and scheduled
without it. This walks those days and rebuilds them.

    POSTIZ_KEY=... python3 pipeline/backfill_titles.py 2026-08-28 2026-09-10
    POSTIZ_KEY=... python3 pipeline/backfill_titles.py 2026-08-28 2026-09-10 --dry-run

Per day: pull the scheduled posts, recover the title from the YouTube post's
settings (the only place it is currently recorded) and the hook from the live
caption, re-render the teaser with the title on screen, push it, then replace
the four social posts.

Three things this is careful about, all learned the hard way:

- The new video is written to `<slug>-teaser-v2.mp4` rather than overwriting.
  raw.githubusercontent is CDN-cached, so re-pushing the same path can serve
  Postiz the stale file and the whole run would silently do nothing.
- Replacements are scheduled BEFORE the originals are deleted, and nothing is
  deleted unless every channel rebuilt. Deleting first once left a day empty.
- The integration object inside /posts calls the field `providerIdentifier`;
  /integrations calls the same thing `identifier`. Reading the wrong one
  matches nothing.

Reddit is skipped — it carries its own wording and a full-song link.
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
RAW = ("https://raw.githubusercontent.com/jordanjayhays-cpu/jordan-projects/"
       "claude/philosophical-king-poster-raq2ke/music-assets/")
BRANCH = "claude/philosophical-king-poster-raq2ke"
STAGGER = {"youtube": "08:00:00", "facebook": "08:03:00",
           "instagram-standalone": "08:07:00", "instagram": "08:07:00",
           "tiktok": "08:14:00"}

sys.path.insert(0, PIPE)
from daily_post import mcp, platform_settings, TRACK_LINK, CATALOGUE  # noqa: E402


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
    """The track title, recovered from a post's settings field."""
    for p in posts:
        s = p.get("settings")
        if isinstance(s, str):
            try:
                s = json.loads(s)
            except ValueError:
                continue
        t = (s or {}).get("title") or ""
        t = t.split(" | Philosophical King")[0].split(" — Philosophical King")[0].strip()
        if t:
            return t
    return None


def hook_from(caption):
    """The hook, from the live caption's first paragraph."""
    m = re.match(r"\s*<p>(.*?)</p>", caption or "", re.S)
    if not m:
        return None
    first = re.sub(r"<[^>]+>", "", m.group(1)).strip()
    # Captions written before this change read "<hook> 👑"; ones written after
    # read "<Title> — <hook> 👑". Handle both so a partial re-run is safe.
    first = first.replace("👑", "").strip()
    for sep in (": ", " — "):
        if sep in first:
            first = first.split(sep, 1)[1].strip()
            break
    return first or None


def series_from(caption):
    m = re.search(r"Track (\d+) of (\d+)", caption or "")
    return (m.group(1), m.group(2)) if m else (None, str(CATALOGUE))


def render(slug, title, hook):
    """Re-render the teaser with the title on screen. Returns the new filename."""
    src = os.path.join(ASSETS, f"{slug}-teaser.mp4")
    art = os.path.join(ASSETS, f"{slug}-art.jpg")
    lyr = os.path.join(ASSETS, f"{slug}-lyrics.json")
    for path in (src, art, lyr):
        if not os.path.exists(path):
            raise FileNotFoundError(path)

    wav = os.path.join("/tmp", f"{slug}-backfill.wav")
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", src,
                           "-vn", "-ac", "1", "-ar", "44100", wav])
    out_name = f"{slug}-teaser-v2.mp4"
    out = os.path.join(ASSETS, out_name)
    subprocess.check_call([sys.executable, os.path.join(PIPE, "kinetic_render.py"),
                           slug, title, hook, "hyperfollow.com/PhilosophicalKing",
                           art, wav, lyr, out])
    os.remove(wav)
    return out_name


def git(*args):
    subprocess.check_call(["git", "-C", ROOT, *args])


def do_day(day, slug, dry):
    existing = posts_on(day)
    if not existing:
        return f"{day} {slug}: no posts scheduled — skipped"
    social = [p for p in existing if plat(p) != "reddit"]
    if not social:
        return f"{day} {slug}: reddit only — skipped"
    if any(p.get("state") == "PUBLISHED" for p in social):
        return f"{day} {slug}: already published — skipped"

    title = title_from(social)
    caption = social[0].get("content") or ""
    hook = hook_from(caption)
    series_no, catalogue = series_from(caption)
    if not (title and hook):
        return (f"{day} {slug}: could not recover title/hook "
                f"(title={title!r} hook={hook!r}) — skipped")

    if f"{title}:" in re.sub(r"<[^>]+>", "", caption)[:120]:
        return f"{day} {slug}: already carries the title — skipped"

    # Days scheduled before the series frame existed have no "Track N of 251"
    # line. Add the title to those without inventing a series number they were
    # never posted with.
    series_line = (f"<p>Track {series_no} of {catalogue}. Turning every idea in "
                   f"philosophy into a song.</p>") if series_no else ""
    content = (f"<p>{title}: {hook} 👑</p>"
               f"{series_line}"
               f"<p>Full track everywhere: {TRACK_LINK}</p>"
               f"<p>#Philosophy #PhilosophicalKing</p>")

    channels = [plat(p) for p in social]
    if dry:
        return f"{day} {slug}: WOULD rebuild {channels} as {title!r} / {hook!r}"

    video = render(slug, title, hook)
    git("add", f"music-assets/{video}")
    subprocess.call(["git", "-C", ROOT, "-c", "user.name=Claude",
                     "-c", "user.email=noreply@anthropic.com",
                     "commit", "-q", "-m", f"pipeline: titled teaser for {slug}"])
    git("push", "origin", BRANCH)

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
        return (f"{day} {slug}: scheduled {len(made)} of {len(rebuilt)} — "
                f"originals LEFT IN PLACE, clean up duplicates by hand")

    for p in social:
        api(f"posts/{p['id']}", method="DELETE")
    return f"{day} {slug}: rebuilt {len(made)} posts — {title}"


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
            except Exception as exc:  # keep going; one bad day must not stop the rest
                print(f"{key} {slug}: FAILED — {type(exc).__name__}: {exc}", flush=True)
        day += timedelta(days=1)


if __name__ == "__main__":
    main()
