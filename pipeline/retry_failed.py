#!/usr/bin/env python3
"""
Auto-retry watchdog: any of today's YouTube/Instagram/TikTok posts in ERROR state
gets re-scheduled once with identical content and fresh media, and the errored
entry is deleted. Runs shortly after the morning posting window. Env: POSTIZ_KEY.
"""
import json, os, ssl, subprocess, sys, time, urllib.request
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIPE = os.path.join(ROOT, "pipeline")
KEY = os.environ.get("POSTIZ_KEY") or sys.exit("POSTIZ_KEY not set")
CA = "/root/.ccr/ca-bundle.crt"
RETRY_PLATFORMS = {"youtube", "instagram-standalone", "tiktok"}
RAW = "https://raw.githubusercontent.com/jordanjayhays-cpu/jordan-projects/claude/philosophical-king-poster-raq2ke/music-assets"

def mcp(name, args):
    payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                          "params": {"name": name, "arguments": args}})
    out = subprocess.check_output(["curl", "-sS", "--cacert", CA, "-X", "POST",
        "https://mcp.postiz.com/mcp", "-H", f"Authorization: Bearer {KEY}",
        "-H", "Content-Type: application/json", "-H", "Accept: application/json, text/event-stream", "-d", payload])
    d = json.loads(out)
    body = d["result"]["content"][0]["text"]
    if d["result"].get("isError"):
        raise RuntimeError(body[:300])
    return json.loads(body)

def main():
    state = json.load(open(os.path.join(PIPE, "state.json")))
    schedule = state.get("schedule", {})
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    posts = mcp("postsListTool", {"startDate": f"{today}T00:00:00", "endDate": f"{today}T23:59:00"})["output"]["posts"]
    errored = [p for p in posts if p.get("state") == "ERROR" and p.get("platform") in RETRY_PLATFORMS]
    if not errored:
        print("no errored posts today — all clean"); return
    slug = schedule.get(today)
    when = (datetime.now(timezone.utc) + timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:00")
    for p in errored:
        if not slug:
            print(f"no schedule entry for {today}; cannot derive media — skipping {p['platform']}"); continue
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
