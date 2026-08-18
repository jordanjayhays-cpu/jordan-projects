#!/usr/bin/env python3
"""
Same-day Reddit poster: after the morning YouTube Short publishes (08:00 UTC),
link-post it to Reddit. Dedupes via state.reddit_posted. Env: POSTIZ_KEY.
"""
import json, os, re, ssl, subprocess, sys, urllib.request
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIPE = os.path.join(ROOT, "pipeline")
KEY = os.environ.get("POSTIZ_KEY") or sys.exit("POSTIZ_KEY not set")
CA = "/root/.ccr/ca-bundle.crt"
CTX = ssl.create_default_context(cafile=CA) if os.path.exists(CA) else ssl.create_default_context()

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
    cfg_path = os.path.join(PIPE, "reddit.json")
    if not os.path.exists(cfg_path):
        print("no reddit.json — nothing to do"); return
    cfg = json.load(open(cfg_path))
    state = json.load(open(os.path.join(PIPE, "state.json")))
    descs = json.load(open(os.path.join(PIPE, "descriptions.json")))

    end = datetime.now(timezone.utc)
    start = end - timedelta(days=2)
    req = urllib.request.Request(
        f"https://api.postiz.com/public/v1/posts?startDate={start.strftime('%Y-%m-%dT%H:%M:%SZ')}"
        f"&endDate={end.strftime('%Y-%m-%dT%H:%M:%SZ')}", headers={"Authorization": KEY})
    with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
        data = json.load(r)
    posts = data["posts"] if isinstance(data, dict) else data
    yts = [p for p in posts if p.get("integration", {}).get("providerIdentifier") == "youtube"
           and p.get("state") == "PUBLISHED" and p.get("releaseURL")]
    if not yts:
        print("no published YouTube video found"); return
    p = max(yts, key=lambda x: x.get("publishDate", ""))
    raw = json.loads(p["settings"]).get("title", "") if isinstance(p.get("settings"), str) else ""
    title = raw.split(" — Philosophical King")[0].strip() or "Philosophical King"
    slug = re.sub(r"\s+", "-", re.sub(r"[^\w\s-]", "", title.lower()).strip())
    if slug in state.get("reddit_posted", []):
        print(f"{slug} already on Reddit — done"); return

    integs = mcp("integrationList", {})["output"]
    reddit = next((i for i in integs if i["platform"] == "reddit"), None)
    if not reddit:
        print("no reddit channel connected"); return

    desc = descs.get(slug, f"One idea, one song: {title}.")
    when = (datetime.now(timezone.utc) + timedelta(minutes=15)).strftime("%Y-%m-%dT%H:%M:00")
    value = {"subreddit": cfg["subreddit"], "title": title[:290], "type": "link",
             "url": p["releaseURL"], "is_flair_required": bool(cfg.get("flair"))}
    if cfg.get("flair"):
        value["flair"] = cfg["flair"]
    mcp("integrationSchedulePostTool", {"socialPost": [{
        "integrationId": reddit["id"], "isPremium": False, "date": when,
        "shortLink": False, "type": "schedule",
        "postsAndComments": [{"content": f"<p>{desc}</p>", "attachments": []}],
        "settings": [{"key": "subreddit", "value": [{"value": value}]}]}]})
    state.setdefault("reddit_posted", []).append(slug)
    json.dump(state, open(os.path.join(PIPE, "state.json"), "w"), indent=1)
    subprocess.check_call(["git", "-C", ROOT, "add", "pipeline/state.json"])
    subprocess.call(["git", "-C", ROOT, "-c", "user.name=pk-pipeline",
                     "-c", "user.email=pipeline@philosophical-king.local",
                     "commit", "-q", "-m", f"reddit: posted {slug}"])
    subprocess.check_call(["git", "-C", ROOT, "push", "origin", "claude/philosophical-king-poster-raq2ke"])
    print(f"scheduled Reddit link post for {title} at {when} UTC -> {p['releaseURL']}")

if __name__ == "__main__":
    main()
