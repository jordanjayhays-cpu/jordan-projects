#!/usr/bin/env python3
"""
Auto-retry watchdog: any of today's YouTube/Instagram/TikTok posts in ERROR state
gets re-scheduled once with identical content and fresh media, and the errored
entry is deleted. Runs shortly after the morning posting window. Env: POSTIZ_KEY.
"""
import json, os, ssl, subprocess, sys, time, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mcp_parse
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIPE = os.path.join(ROOT, "pipeline")
KEY = os.environ.get("POSTIZ_KEY") or sys.exit("POSTIZ_KEY not set")
CA = "/root/.ccr/ca-bundle.crt"
# Facebook joined on 2026-10-09: it had published 11 days straight and then
# errored once, and nothing retried it because it was not in this set.
# Reddit stays out: reddit_daily.py owns that channel and has its own retry.
RETRY_PLATFORMS = {"youtube", "instagram-standalone", "tiktok", "facebook"}
RAW = "https://raw.githubusercontent.com/jordanjayhays-cpu/jordan-projects/claude/philosophical-king-poster-raq2ke/music-assets"

def mcp(name, args):
    """One Postiz MCP tool call. Retries and error text live in mcp_parse."""
    return mcp_parse.call(name, args, KEY, CA)

def main():
    """Retry channels that errored. Takes an optional lookback in days.

    It used to look at today alone, so a failure noticed later was never
    retried: TikTok dropped 2026-10-20 and the watchdog, run on the 23rd,
    reported all clean. Default is still today, so the daily run is
    unchanged; pass a number to sweep back over a window.
    """
    back = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    state = json.load(open(os.path.join(PIPE, "state.json")))
    schedule = state.get("schedule", {})
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")
    start = (now - timedelta(days=back)).strftime("%Y-%m-%d")
    posts = mcp("postsListTool", {"startDate": f"{start}T00:00:00", "endDate": f"{today}T23:59:00"})["output"]["posts"]
    errored = [p for p in posts if p.get("state") == "ERROR" and p.get("platform") in RETRY_PLATFORMS]
    if not errored:
        span = "today" if not back else f"the last {back + 1} days"
        print(f"no errored posts in {span} — all clean"); return
    when = (datetime.now(timezone.utc) + timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:00")
    for p in errored:
        # The slug has to come from the post's OWN day, not from today, or a
        # swept-up older failure is retried carrying the wrong video.
        day = (p.get("publishDate") or "")[:10]
        slug = schedule.get(day)
        if not slug:
            print(f"no schedule entry for {day or 'unknown date'}; "
                  f"cannot derive media — skipping {p['platform']}"); continue
        up = mcp("uploadFromUrlTool", {"url": f"{RAW}/{slug}-teaser.mp4"})
        s = p.get("settings") or {}
        settings = [{"key": k, "value": v} for k, v in s.items() if k != "__type" and v not in (None, "", [])]
        if p["platform"] in ("instagram-standalone", "facebook") and not any(x["key"] == "post_type" for x in settings):
            settings.append({"key": "post_type", "value": "post"})
        mcp("integrationSchedulePostTool", {"socialPost": [{
            "integrationId": p["integrationId"], "isPremium": False, "date": when,
            "shortLink": False, "type": "schedule",
            "postsAndComments": [{"content": p["content"], "attachments": [up["path"]]}],
            "settings": settings}]})
        subprocess.check_output(["curl", "-sS", "--cacert", CA, "-X", "DELETE",
            f"https://api.postiz.com/public/v1/posts/group/{p['group']}", "-H", f"Authorization: {KEY}"])
        print(f"RETRIED {p['platform']} for {when} UTC; errored copy removed")
        time.sleep(0.5)

if __name__ == "__main__":
    main()
