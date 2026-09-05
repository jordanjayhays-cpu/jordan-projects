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
    start = end - timedelta(days=3)
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
    # every un-posted track from the window, oldest first (self-healing catch-up)
    pending = []
    for y in sorted(yts, key=lambda x: x.get("publishDate", "")):
        raw = json.loads(y["settings"]).get("title", "") if isinstance(y.get("settings"), str) else ""
        t = raw.split(" — Philosophical King")[0].strip() or "Philosophical King"
        sl = re.sub(r"\s+", "-", re.sub(r"[^\w\s-]", "", t.lower()).strip())
        if sl not in state.get("reddit_posted", []):
            pending.append((y, t, sl))
    if not pending:
        print("all recent tracks already on Reddit — done"); return
    print(f"{len(pending)} track(s) pending for Reddit")
    p, title, slug = pending[0]

    integs = mcp("integrationList", {})["output"]
    reddit = next((i for i in integs if i["platform"] == "reddit"), None)
    if not reddit:
        print("no reddit channel connected"); return

    desc = descs.get(slug, f"One idea, one song: {title}.")
    when = (datetime.now(timezone.utc) + timedelta(minutes=15)).strftime("%Y-%m-%dT%H:%M:00")
    # Link the FULL song, not the 30-second teaser Short. Reddit is a place people
    # sit and listen; a teaser that cuts off mid-verse reads as an advert. Falls
    # back to the Short if a track is not on the Topic channel.
    sys.path.insert(0, PIPE)
    from yt_catalogue import full_song
    link = full_song(slug=slug, title=title) or p["releaseURL"]
    print(f"reddit link: {link}" + ("" if link != p["releaseURL"] else " (teaser fallback)"))
    value = {"subreddit": cfg["subreddit"], "title": title[:290], "type": "link",
             "url": link, "is_flair_required": bool(cfg.get("flair"))}
    if cfg.get("flair"):
        value["flair"] = cfg["flair"]
    res = mcp("integrationSchedulePostTool", {"socialPost": [{
        "integrationId": reddit["id"], "isPremium": False, "date": when,
        "shortLink": False, "type": "schedule",
        "postsAndComments": [{"content": f"<p>{desc}</p>", "attachments": []}],
        "settings": [{"key": "subreddit", "value": [{"value": value}]}]}]})
    # Verify the post actually exists before recording it as done.
    #
    # This is the bug that lost five days. The old code appended the slug to
    # state.reddit_posted unconditionally, so a run that scheduled nothing still
    # marked the track posted and every later run skipped it as already done.
    # The re-pin branch below made it worse: it DELETED the post first and never
    # checked that the replacement was created, so a failure there left the day
    # with no post and the state saying otherwise. Nothing ever raised, so the
    # routine reported success each morning while Reddit sat empty.
    import time as _t

    def fetch(pid):
        _t.sleep(3)
        r = urllib.request.Request(
            f"https://api.postiz.com/public/v1/posts?startDate={start.strftime('%Y-%m-%dT%H:%M:%SZ')}"
            f"&endDate={(end + timedelta(days=2)).strftime('%Y-%m-%dT%H:%M:%SZ')}",
            headers={"Authorization": KEY})
        with urllib.request.urlopen(r, context=CTX, timeout=30) as resp:
            dd = json.load(resp)
        return next((x for x in (dd["posts"] if isinstance(dd, dict) else dd)
                     if x["id"] == pid), None)

    pid = res["output"][0]["postId"]
    mine = fetch(pid)
    if mine and mine.get("publishDate", "")[:16] != when[:16]:
        print(f"WARN: stored {mine.get('publishDate')} != requested {when}; re-pinning")
        subprocess.check_output(["curl", "-sS", "--cacert", CA, "-X", "DELETE",
            f"https://api.postiz.com/public/v1/posts/group/{mine['group']}", "-H", f"Authorization: {KEY}"])
        res = mcp("integrationSchedulePostTool", {"socialPost": [{
            "integrationId": reddit["id"], "isPremium": False, "date": when,
            "shortLink": False, "type": "schedule",
            "postsAndComments": [{"content": f"<p>{desc}</p>", "attachments": []}],
            "settings": [{"key": "subreddit", "value": [{"value": value}]}]}]})
        pid = (res.get("output") or [{}])[0].get("postId")
        mine = fetch(pid) if pid else None

    if not mine:
        sys.exit(f"FAILED: scheduled {slug} but no post came back from Postiz. "
                 f"state NOT updated, so tomorrow's run retries it. Raise an alert.")

    state.setdefault("reddit_posted", []).append(slug)
    json.dump(state, open(os.path.join(PIPE, "state.json"), "w"), indent=1)
    subprocess.check_call(["git", "-C", ROOT, "add", "pipeline/state.json"])
    subprocess.call(["git", "-C", ROOT, "-c", "user.name=Claude",
                     "-c", "user.email=noreply@anthropic.com",
                     "commit", "-q", "-m", f"reddit: posted {slug}"])
    subprocess.check_call(["git", "-C", ROOT, "push", "origin", "claude/philosophical-king-poster-raq2ke"])
    print(f"scheduled Reddit link post for {title} at {when} UTC -> {link}")

if __name__ == "__main__":
    main()
