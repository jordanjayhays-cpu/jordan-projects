#!/usr/bin/env python3
"""
Philosophical King daily video pipeline.

Each run: pick the next track from pipeline/queue.json, fetch its official
30s iTunes preview + cover art, transcribe lyrics (dual-language, no VAD),
render the locked 1080x1920 lyric-teaser template, upload to Postiz, and
schedule a post on EVERY connected Postiz channel for the day after the
last scheduled post. State is committed back to this branch.

Env:  POSTIZ_KEY (required)
Deps: ffmpeg, pip install faster-whisper  (installed automatically if missing)
"""
import json, os, re, ssl, subprocess, sys, itertools, urllib.request
from datetime import date, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIPE = os.path.join(ROOT, "pipeline")
ASSETS = os.path.join(ROOT, "music-assets")
KEY = os.environ.get("POSTIZ_KEY") or sys.exit("POSTIZ_KEY not set")
CA = "/root/.ccr/ca-bundle.crt"
CTX = ssl.create_default_context(cafile=CA) if os.path.exists(CA) else ssl.create_default_context()
POST_HOUR = "08:00:00"  # UTC

def sh(*cmd, **kw):
    return subprocess.check_output(cmd, **kw)

def ensure_deps():
    if subprocess.call(["which", "ffmpeg"], stdout=subprocess.DEVNULL) != 0:
        subprocess.call(["sudo", "apt-get", "update", "-qq"])
        subprocess.check_call(["sudo", "apt-get", "install", "-y", "-qq", "ffmpeg"])
    if subprocess.call(["which", "ffmpeg"], stdout=subprocess.DEVNULL) != 0:
        raise RuntimeError("ffmpeg unavailable after install attempt")
    try:
        import faster_whisper  # noqa
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "faster-whisper"])
    try:
        import PIL  # noqa
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "pillow"])
    if not os.path.exists("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"):
        subprocess.call(["sudo", "apt-get", "install", "-y", "-qq", "fonts-noto-color-emoji"])

def http_json(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), context=CTX, timeout=30) as r:
        return json.load(r)

def fetch(url, out):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), context=CTX, timeout=60) as r, open(out, "wb") as f:
        f.write(r.read())

def mcp(name, args):
    payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                          "params": {"name": name, "arguments": args}})
    out = sh("curl", "-sS", "--cacert", CA, "-X", "POST", "https://mcp.postiz.com/mcp",
             "-H", f"Authorization: Bearer {KEY}", "-H", "Content-Type: application/json",
             "-H", "Accept: application/json, text/event-stream", "-d", payload)
    d = json.loads(out)
    body = d["result"]["content"][0]["text"]
    if d["result"].get("isError"):
        raise RuntimeError(body[:500])
    return json.loads(body)

# HARD RULE (Jordan, Aug 2026): one link, everywhere, every track. The per-track
# DistroKid URLs this used to build (distrokid.com/hyperfollow/philosophicalking/<slug>)
# do not resolve, and song.link is not to be used either. This is replaced only when
# PK has its own website.
TRACK_LINK = "https://hyperfollow.com/PhilosophicalKing"

# The catalogue, for the series line. queue.json + state["posted"] should sum to this.
CATALOGUE = 251

def pick_hook(lines, title):
    """
    The caption's first line — the only thing most people read.

    The old rule (first 3-8 word segment, truncated to 7 words) produced
    fragments, because Whisper segments on breath, not on clauses: "decide or
    does", "and strife. Purpose is carved". Score for completeness instead and
    never truncate — a short whole line beats a long broken one.
    """
    texts = [l["text"].strip() for l in lines[:26] if l["text"].strip()]
    best, best_score = None, -99
    # Whisper segments on breath, so a whole clause usually spans two or three of
    # them ("Each step was a death," + "each truth was reborn"). Score joined
    # windows, not single segments, or every candidate is half a sentence.
    for i in range(len(texts)):
        for span in (1, 2, 3):
            if i + span > len(texts):
                break
            t = " ".join(texts[i:i + span]).strip()
            w = t.lower().split()
            n = len(w)
            if not (4 <= n <= 12):
                continue
            score = 0
            if t[0].isupper():        score += 3   # not picked up mid-clause
            if t[-1] in ".!?":        score += 4   # a finished thought
            if t.endswith(","):       score -= 5   # runs into the next line
            if w[0] in OPENERS_BAD:   score -= 4   # a continuation, not an opening
            # The real fragment tell. These transcripts are mostly unpunctuated, so
            # "ends with a full stop" rarely fires; "ends on a word that cannot end
            # a sentence" catches what it misses -- "From earth's first spark to".
            if w[-1].strip(".,!?") in DANGLING:
                score -= 6
            nxt = texts[i + span] if i + span < len(texts) else ""
            if nxt[:1].isupper():     score += 2   # next line starts fresh, so this one closed
            if not nxt:               score += 1
            if 6 <= n <= 10:          score += 1   # reads in one glance
            if score > best_score:
                best, best_score = t, score
    if best is None:
        best = texts[0] if texts else title
    return best.strip(" ,")


# words a sentence cannot end on
DANGLING = set("""a an the and but or nor yet so of to in on at for with from by as
is are was were be been being am do does did has have had will would can could
shall should may might must that this these those which who whom whose what when
where while if than then like into onto over under through up down out about not
no my your his her its their our it he she they we you i""".split())

OPENERS_BAD = set("""and but or the a an of to it that which yet is was as""".split())


def latest_published_youtube():
    """(title, url, slug) of the most recent published YouTube post, or None."""
    from datetime import datetime, timedelta, timezone
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=4)
    req = urllib.request.Request(
        f"https://api.postiz.com/public/v1/posts?startDate={start.strftime('%Y-%m-%dT%H:%M:%SZ')}"
        f"&endDate={end.strftime('%Y-%m-%dT%H:%M:%SZ')}",
        headers={"Authorization": KEY})
    with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
        data = json.load(r)
    posts = data["posts"] if isinstance(data, dict) else data
    yts = [p for p in posts
           if p.get("integration", {}).get("providerIdentifier") == "youtube"
           and p.get("state") == "PUBLISHED" and p.get("releaseURL")]
    if not yts:
        return None
    p = max(yts, key=lambda x: x.get("publishDate", ""))
    raw_title = (json.loads(p["settings"]).get("title", "") if isinstance(p.get("settings"), str)
                 else (p.get("settings") or {}).get("title", ""))
    t = raw_title.split(" — Philosophical King")[0].strip() or "Philosophical King"
    s = re.sub(r"\s+", "-", re.sub(r"[^\w\s-]", "", t.lower()).strip())
    return t, p["releaseURL"], s


def transcribe(wav):
    from faster_whisper import WhisperModel
    model = WhisperModel("small", device="cpu", compute_type="int8")
    def run(lang):
        segments, _ = model.transcribe(wav, word_timestamps=True, vad_filter=False, language=lang)
        segs = []
        for seg in segments:
            ws = [{"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)} for w in (seg.words or [])]
            if ws: segs.append(ws)
        return segs
    en = run("en")
    tl = run("tl")
    # Pick by Tagalog DENSITY, not by word count.
    #
    # The old rule required the tl pass to find 1.2x more words than the en pass.
    # That fails on exactly the songs it exists for: when a chorus is genuinely
    # SUNG in Tagalog, the English model does not produce fewer words, it produces
    # fluent English of similar length - it translates. On Bayanihan (91% Filipino
    # audience, PK's single biggest earner) that put "Together, in every corner of
    # our land" on screen where the track sings "Sama-sama sa bawat hakbang".
    # Confirmed by locating the iTunes preview at 45.0s in the full song: the same
    # seconds of audio, two different answers.
    #
    # Density is the honest test. A song actually sung in English, transcribed
    # under language="tl", does not come back peppered with Tagalog function words.
    words = [w["w"].lower().strip(".,!?") for s in tl for w in s]
    markers = {"ng", "mga", "ang", "sa", "ay", "na", "kung", "pag", "walang",
               "bawat", "ating", "kayo", "tayo", "namin", "natin", "iwanan"}
    hits = sum(1 for w in words if w in markers)
    density = hits / max(1, len(words))
    # Threshold measured, not guessed. Across real previews the separation is
    # total: English-only tracks score EXACTLY 0.000 (The Cave, Burnout Society,
    # Memento Mori) because the tl pass simply returns English; Filipino tracks
    # score 0.036 (Kapwa) to 0.246 (Bayanihan). 0.02 sits in the empty middle.
    # An earlier 0.04 was too tight and would have anglicised Kapwa, which the
    # old rule happened to get right - a fix that regresses a working case.
    return tl if density >= 0.02 else en

def split_seg(ws, maxw=5):
    if len(ws) <= maxw: return [ws]
    n = (len(ws) + maxw - 1) // maxw
    best = None
    for combo in itertools.combinations(range(1, len(ws)), n - 1):
        prev, pieces, ok = 0, [], True
        for c in combo:
            if c - prev > maxw: ok = False; break
            pieces.append((prev, c)); prev = c
        if not ok or len(ws) - prev > maxw: continue
        pieces.append((prev, len(ws)))
        score = sum(ws[c]["s"] - ws[c - 1]["e"] for c in combo)
        if best is None or score > best[0]: best = (score, pieces)
    return [ws[a:b] for a, b in best[1]]

def render(fn, wav, art, lines):
    dur = float(sh("ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", wav).strip())
    txtdir = f"/tmp/{fn}-txt"
    os.makedirs(txtdir, exist_ok=True)
    f = [f"color=c=black:s=1080x1920:d={dur:.2f}[bg]",
         "[1:v]scale=1000:1000:force_original_aspect_ratio=decrease,"
         "pad=1080:1080:(ow-iw)/2:(oh-ih)/2:color=black@0,"
         f"zoompan=z=1.0:x='40*sin(2*PI*on/1500)':y='40*cos(2*PI*on/1900)':d={int(dur*30)}:s=1080x1080:fps=30[art]",
         "[bg][art]overlay=0:250[base]",
         "[0:a]showwaves=s=900x120:mode=cline:colors=0xb09a4a[wave]",
         "[base][wave]overlay=90:1380[wv]",
         "[wv]drawtext=text='PHILOSOPHICAL KING':font=serif:fontsize=42:fontcolor=0xc8e0d8"
         ":x=(w-text_w)/2:y=110:shadowcolor=black:shadowx=2:shadowy=2[wm]"]
    chain = "[wm]"
    for i, ln in enumerate(lines):
        tf = f"{txtdir}/{i}.txt"
        open(tf, "w").write(ln["text"])
        o = f"[l{i}]" if i < len(lines) - 1 else "[out]"
        f.append(f"{chain}drawtext=textfile={tf}:font=serif:fontsize=52:fontcolor=0xc8e0d8"
                 f":x=(w-text_w)/2:y=1560:shadowcolor=black:shadowx=3:shadowy=3"
                 f":enable='between(t,{ln['s']},{ln['e']})'{o}")
        chain = o
    out = os.path.join(ASSETS, f"{fn}-teaser.mp4")
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", wav, "-loop", "1", "-i", art,
                           "-filter_complex", ";".join(f), "-map", "[out]", "-map", "0:a",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "192k", "-shortest", "-t", f"{dur:.2f}", out])
    return out

def platform_settings(platform, title, media_url=None):
    t = f"{title} — Philosophical King (Official Lyric Teaser)"
    if platform == "youtube":
        return [{"key": "title", "value": t[:100]}, {"key": "type", "value": "public"},
                {"key": "selfDeclaredMadeForKids", "value": "no"},
                {"key": "tags", "value": [{"value": x, "label": x} for x in
                                          [title.lower(), "philosophy", "philosophical king"]]}]
    if platform == "tiktok":
        return [{"key": "title", "value": f"{title} — Philosophical King"[:90]},
                {"key": "content_posting_method", "value": "DIRECT_POST"},
                {"key": "privacy_level", "value": "PUBLIC_TO_EVERYONE"},
                {"key": "comment", "value": True}, {"key": "duet", "value": True},
                {"key": "stitch", "value": True}, {"key": "video_made_with_ai", "value": True},
                {"key": "autoAddMusic", "value": "no"},
                {"key": "brand_content_toggle", "value": False},
                {"key": "brand_organic_toggle", "value": False}]
    if platform in ("instagram", "instagram-standalone"):
        return [{"key": "post_type", "value": "post"}]
    if platform == "facebook":
        return [{"key": "post_type", "value": "post"}]
    if platform == "reddit":
        # requires pipeline/reddit.json: {"subreddit": "/r/...", "flair": {"id":..., "name":...}?}
        cfg_path = os.path.join(PIPE, "reddit.json")
        if not os.path.exists(cfg_path):
            return None  # skip reddit until configured
        cfg = json.load(open(cfg_path))
        # HARD RULE: every Reddit post is a link post to a LIVE YouTube video
        # (renders as playable video on Reddit). No link -> no Reddit post.
        if not media_url:
            return None
        value = {"subreddit": cfg["subreddit"], "title": title[:290], "type": "link",
                 "url": media_url, "is_flair_required": bool(cfg.get("flair"))}
        if cfg.get("flair"):
            value["flair"] = cfg["flair"]
        return [{"key": "subreddit", "value": [{"value": value}]}]
    return []  # others: defaults

def main():
    ensure_deps()
    queue = json.load(open(os.path.join(PIPE, "queue.json")))
    state = json.load(open(os.path.join(PIPE, "state.json")))
    if not queue:
        print("QUEUE EMPTY — nothing to schedule"); return

    track = queue[0]
    title, slug_, upc = track["title"], track["slug"], track.get("upc")
    print(f"Next track: {title}")

    # UPC is the usual key, from the royalty CSVs. Tracks released after that
    # baseline have no UPC on file, so they carry an iTunes collectionId instead
    # — found by searching the store for an exact artist + title match. Same
    # lookup endpoint, different key.
    key = f"upc={upc}" if upc else f"id={track['collectionId']}"
    d = http_json(f"https://itunes.apple.com/lookup?{key}&entity=song")
    songs = [x for x in d.get("results", []) if x.get("kind") == "song"]
    if not songs:
        print(f"SKIP {title}: no iTunes song for {key}")
        queue.pop(0)
        state.setdefault("skipped", []).append(title)
        json.dump(queue, open(os.path.join(PIPE, "queue.json"), "w"), indent=1)
        json.dump(state, open(os.path.join(PIPE, "state.json"), "w"), indent=1)
        return main()  # try the next one
    song = songs[0]

    wav, art = f"/tmp/{slug_}.wav", f"/tmp/{slug_}-art.jpg"
    fetch(song["previewUrl"], f"/tmp/{slug_}.m4a")
    fetch(song["artworkUrl100"].replace("100x100", "3000x3000"), art)
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", f"/tmp/{slug_}.m4a", wav])
    import shutil as _sh
    _sh.copy(art, os.path.join(ASSETS, f"{slug_}-art.jpg"))  # pushed with the video; Reddit uses it

    segs = transcribe(wav)
    lines = []
    for ws in segs:
        for grp in split_seg(ws):
            lines.append({"text": " ".join(x["w"] for x in grp), "s": grp[0]["s"], "e": grp[-1]["e"]})
    if not lines:
        lines = [{"text": "", "s": 0, "e": 0.1}]
    # bridge small gaps only — during real instrumental breaks the screen goes clean
    for a, b in zip(lines, lines[1:]):
        gap = b["s"] - a["e"]
        if 0 < gap <= 1.0:
            a["e"] = b["s"]
        elif gap > 1.0:
            a["e"] += 1.0
    lines[-1]["e"] += 1.0
    json.dump(lines, open(os.path.join(ASSETS, f"{slug_}-lyrics.json"), "w"), indent=1)

    # kinetic template (current standard) — hook = first strong short line
    hook_line = pick_hook(lines, title)
    video = os.path.join(ASSETS, f"{slug_}-teaser.mp4")
    track_link = TRACK_LINK
    subprocess.check_call([sys.executable, os.path.join(PIPE, "kinetic_render.py"),
                           slug_, title, hook_line, track_link,
                           art, wav, os.path.join(ASSETS, f"{slug_}-lyrics.json"), video])
    print("rendered (kinetic)", video)

    # push video so Postiz can fetch it from the public raw URL
    subprocess.check_call(["git", "-C", ROOT, "add", "music-assets"])
    subprocess.call(["git", "-C", ROOT, "-c", "user.name=Claude",
                     "-c", "user.email=noreply@anthropic.com",
                     "commit", "-q", "-m", f"pipeline: add {title} teaser"])
    subprocess.check_call(["git", "-C", ROOT, "push", "origin",
                           "claude/philosophical-king-poster-raq2ke"])

    # next date = day after last scheduled
    nxt = (date.fromisoformat(state["last_scheduled_date"]) + timedelta(days=1)).isoformat()
    link = track_link
    hook = hook_line
    # Series frame: people follow projects, not posts. The number tells a first-time
    # viewer there are dozens behind this one and hundreds coming, which turns the
    # catalogue depth from a liability into the pitch. Written "Track N" rather than
    # "#N" on purpose — a leading "#N" renders as a hashtag on Instagram and TikTok.
    series_no = len(state["posted"]) + 1
    # Follow ask. Release Radar goes automatically to Spotify followers, and PK has
    # 28 of them — so a new release currently reaches 3 listeners by default. That
    # number is the floor under everything, and no post has ever asked for a follow.
    #
    # Spotify rather than Apple because Jordan reports the two are close, and the
    # tiebreak goes to the platform whose mechanic is confirmed: Release Radar
    # pushes to followers, Apple's equivalent is unverified.
    #
    # Date-gated to the day AFTER the series-frame test closes (Sep 7). Running both
    # at once would move two variables and neither result would be readable.
    # One link only, still hyperfollow — the follow ask is words, not a second URL.
    FOLLOW_ASK_FROM = "2026-09-08"
    follow = ("<p>Follow Philosophical King on Spotify so the new ones find you.</p>"
              if nxt >= FOLLOW_ASK_FROM else "")
    content = (f"<p>{hook} 👑</p>"
               f"<p>Track {series_no} of {CATALOGUE} — turning every idea in "
               f"philosophy into a song.</p>"
               f"{follow}"
               f"<p>Full track everywhere: {link}</p>"
               f"<p>#Philosophy #PhilosophicalKing</p>")

    integrations = mcp("integrationList", {})["output"]
    up = mcp("uploadFromUrlTool",
             {"url": f"https://raw.githubusercontent.com/jordanjayhays-cpu/jordan-projects/"
                     f"claude/philosophical-king-poster-raq2ke/music-assets/{slug_}-teaser.mp4"})
    # Reddit gets community wording: one plain sentence on what the song is, no promotion
    desc_path = os.path.join(PIPE, "descriptions.json")
    descs = json.load(open(desc_path)) if os.path.exists(desc_path) else {}
    reddit_content = f"<p>{descs.get(slug_, f'A philosophy track exploring the idea behind its title: {title}.')}</p>"

    social = []
    for integ in integrations:
        if integ["platform"] == "reddit":
            # Reddit posts SAME-DAY (not at queue end): link the newest LIVE YouTube video,
            # once per track ever (state.reddit_posted), scheduled for later this morning UTC.
            yt = latest_published_youtube()
            if yt is None:
                print("skipping reddit: no published YouTube video to link yet")
                continue
            yt_title, yt_url, yt_slug = yt
            # Prefer the FULL song over the 30-second teaser. Reddit is a place
            # people sit and listen; a teaser cutting off mid-verse reads as an ad.
            from yt_catalogue import full_song
            yt_url = full_song(slug=yt_slug, title=yt_title) or yt_url
            if yt_slug in state.get("reddit_posted", []):
                print(f"skipping reddit: {yt_slug} already posted there")
                continue
            r_desc = descs.get(yt_slug, f"One idea, one song: {yt_title}.")
            from datetime import datetime as _dt, timezone as _tz, timedelta as _td
            now = _dt.now(_tz.utc)
            r_when = max(now.replace(hour=10, minute=0, second=0), now + _td(minutes=30))
            social.append({"integrationId": integ["id"], "isPremium": False,
                           "date": r_when.strftime("%Y-%m-%dT%H:%M:00"),
                           "shortLink": False, "type": "schedule",
                           "postsAndComments": [{"content": f"<p>{r_desc}</p>", "attachments": []}],
                           "settings": platform_settings("reddit", yt_title, media_url=yt_url)})
            state.setdefault("reddit_posted", []).append(yt_slug)
            continue
        else:
            body, attach = content, [up["path"]]
            settings = platform_settings(integ["platform"], title)
        if settings is None:
            print(f"skipping {integ['platform']} ({integ['name']}): not configured")
            continue
        STAGGER = {"youtube": "08:00:00", "facebook": "08:03:00",
                   "instagram-standalone": "08:07:00", "instagram": "08:07:00", "tiktok": "08:14:00"}
        slot = STAGGER.get(integ["platform"], POST_HOUR)
        social.append({"integrationId": integ["id"], "isPremium": False, "date": f"{nxt}T{slot}",
                       "shortLink": False, "type": "schedule",
                       "postsAndComments": [{"content": body, "attachments": attach}],
                       "settings": settings})
    res = mcp("integrationSchedulePostTool", {"socialPost": social})
    print(f"scheduled {title} on {nxt} across {len(res['output'])} channel(s):",
          [i["platform"] for i in integrations])

    queue.pop(0)
    state["posted"].append(title)
    state.setdefault("schedule", {})[nxt] = slug_
    state["last_scheduled_date"] = nxt
    json.dump(queue, open(os.path.join(PIPE, "queue.json"), "w"), indent=1)
    json.dump(state, open(os.path.join(PIPE, "state.json"), "w"), indent=1)
    subprocess.check_call(["git", "-C", ROOT, "add", "pipeline"])
    subprocess.call(["git", "-C", ROOT, "-c", "user.name=Claude",
                     "-c", "user.email=noreply@anthropic.com",
                     "commit", "-q", "-m", f"pipeline: scheduled {title} for {nxt}"])
    subprocess.check_call(["git", "-C", ROOT, "push", "origin",
                           "claude/philosophical-king-poster-raq2ke"])

if __name__ == "__main__":
    main()
