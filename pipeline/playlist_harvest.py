#!/usr/bin/env python3
"""Find Spotify playlists worth pitching Philosophical King to, and the curators behind them.

    python3 pipeline/playlist_harvest.py auth-url
    python3 pipeline/playlist_harvest.py exchange "<the whole redirect URL>"
    python3 pipeline/playlist_harvest.py harvest [--max-per-query 200]
    python3 pipeline/playlist_harvest.py qualify

Credentials come from the environment and are never written to this repo, which
is public:
    SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REFRESH_TOKEN

WHY A USER TOKEN. Spotify's February 2026 changes moved metadata endpoints off
the client credentials flow, so this authorises once as Jordan and then refreshes
forever. `auth-url` prints the consent link; he opens it, approves, and pastes
the URL he lands on into `exchange`, which prints a refresh token to store.

WHAT SURVIVED THE CUT. As of the Feb/Mar 2026 changes, GET /search still returns
playlists, and GET /playlists/{id} still returns description, owner and follower
count. What is gone: reading another user's playlist contents, listing a user's
playlists, and user profile lookups. So this cannot ask "who already plays
artists like PK" through the API; it finds playlists by name and description and
qualifies them on what the curator publishes.

Search is capped at limit=10 and offset<=1000 now, so a sweep is many small
calls. Development mode apps also share a quota bucket and answer 429 with
reason QUOTA_EXCEEDED when it runs out; this stops cleanly and keeps what it has.
"""
import json, os, re, sys, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIPE = os.path.join(ROOT, "pipeline")
OUT = os.path.join(ROOT, "music-assets", "playlists")
REDIRECT = "http://127.0.0.1:8080/callback"
API = "https://api.spotify.com/v1"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125.0 Safari/537.36")


def env(name):
    v = os.environ.get(name)
    if not v:
        sys.exit(f"{name} not set. See the docstring; credentials never live in this repo.")
    return v.strip()


def post_form(url, data, headers=None):
    body = urllib.parse.urlencode(data).encode()
    h = {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": UA}
    h.update(headers or {})
    req = urllib.request.Request(url, data=body, headers=h, method="POST")
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.load(r)


def basic_auth():
    import base64
    raw = f"{env('SPOTIFY_CLIENT_ID')}:{env('SPOTIFY_CLIENT_SECRET')}".encode()
    return {"Authorization": "Basic " + base64.b64encode(raw).decode()}


def cmd_auth_url():
    """Print the one-time consent URL."""
    q = urllib.parse.urlencode({
        "client_id": env("SPOTIFY_CLIENT_ID"), "response_type": "code",
        "redirect_uri": REDIRECT, "scope": "", "show_dialog": "true"})
    print("1. Put this EXACT redirect URI in the app settings at "
          "developer.spotify.com/dashboard:\n")
    print("   " + REDIRECT + "\n")
    print("2. Open this, approve, and copy the whole URL of the page you land on\n"
          "   (it will fail to load, that is fine, the code is in the address bar):\n")
    print("   https://accounts.spotify.com/authorize?" + q)


def cmd_exchange(redirect_url):
    """Swap the one-time code for a refresh token."""
    qs = urllib.parse.parse_qs(urllib.parse.urlparse(redirect_url).query)
    if "error" in qs:
        sys.exit(f"Spotify refused: {qs['error'][0]}")
    code = (qs.get("code") or [None])[0]
    if not code:
        sys.exit("No ?code= in that URL. Paste the whole address bar, including the query.")
    tok = post_form("https://accounts.spotify.com/api/token",
                    {"grant_type": "authorization_code", "code": code,
                     "redirect_uri": REDIRECT}, basic_auth())
    print("\nSPOTIFY_REFRESH_TOKEN=" + tok["refresh_token"])
    print("\nStore that in Supabase app_secrets next to NOTION_TOKEN. "
          "Do not put it in the repo.")


def access_token():
    tok = post_form("https://accounts.spotify.com/api/token",
                    {"grant_type": "refresh_token",
                     "refresh_token": env("SPOTIFY_REFRESH_TOKEN")}, basic_auth())
    return tok["access_token"]


class Quota(Exception):
    """Development-mode quota is spent; stop and keep what we have."""


def get(path, token, params=None, tries=3):
    url = f"{API}{path}" + ("?" + urllib.parse.urlencode(params) if params else "")
    for attempt in range(tries):
        req = urllib.request.Request(
            url, headers={"Authorization": f"Bearer {token}", "User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            if e.code == 429:
                if "QUOTA_EXCEEDED" in body:
                    raise Quota(body[:200])
                time.sleep(int(e.headers.get("Retry-After", "5")) + 1)
                continue
            if e.code in (500, 502, 503) and attempt < tries - 1:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"{e.code} on {path}: {body[:300]}")
    raise RuntimeError(f"gave up on {path}")


def keywords():
    d = json.load(open(os.path.join(PIPE, "playlist-keywords.json")))
    return [q for k, v in d.items() if not k.startswith("_") for q in v]


def cmd_harvest(max_per_query=200):
    """Sweep every keyword and collect playlist metadata. Resumable."""
    os.makedirs(OUT, exist_ok=True)
    raw_path = os.path.join(OUT, "raw.json")
    found = json.load(open(raw_path)) if os.path.exists(raw_path) else {}
    print(f"starting from {len(found)} playlist(s) already harvested")
    token, calls = access_token(), 0
    try:
        for q in keywords():
            before = len(found)
            for offset in range(0, min(max_per_query, 1000), 10):
                page = get("/search", token,
                           {"q": q, "type": "playlist", "limit": 10, "offset": offset})
                calls += 1
                if calls % 50 == 0:            # refresh well before the hour
                    token = access_token()
                items = [p for p in (page.get("playlists") or {}).get("items") or [] if p]
                if not items:
                    break
                for p in items:
                    found.setdefault(p["id"], {
                        "id": p["id"], "name": p.get("name") or "",
                        "description": p.get("description") or "",
                        "owner_id": (p.get("owner") or {}).get("id") or "",
                        "owner_name": (p.get("owner") or {}).get("display_name") or "",
                        "followers": (p.get("followers") or {}).get("total"),
                        "url": (p.get("external_urls") or {}).get("spotify") or "",
                        "found_via": q,
                    })
                time.sleep(0.12)
            print(f"  {q!r}: +{len(found) - before} (total {len(found)})")
    except Quota as e:
        print(f"\nQUOTA SPENT after {calls} calls — stopping and keeping what we have.\n"
              f"Rerun tomorrow; it resumes from raw.json. ({e})")
    except KeyboardInterrupt:
        print("\ninterrupted, saving what we have")
    json.dump(found, open(raw_path, "w"), ensure_ascii=False, indent=1)
    print(f"\nwrote {len(found)} playlist(s) to {raw_path} in {calls} call(s)")


EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
HANDLE = re.compile(r"(?<![\w@])@([A-Za-z0-9._]{3,30})\b")
LINK = re.compile(r"https?://[^\s\"'<>]+")
ASKS = re.compile(r"submit|submission|send (?:me|us)|dm (?:me|us)|accepting|"
                  r"for consideration|pitch", re.I)


def unescape(s):
    import html
    return html.unescape(s or "")


def cmd_qualify():
    """Turn the raw harvest into a ranked, contactable target list."""
    raw_path = os.path.join(OUT, "raw.json")
    if not os.path.exists(raw_path):
        sys.exit("No raw.json yet. Run `harvest` first.")
    rows = list(json.load(open(raw_path)).values())
    out = []
    for p in rows:
        desc = unescape(p["description"])
        # Spotify's own editorial playlists take pitches through Spotify for
        # Artists, not email. They are not targets for this list.
        if p["owner_id"].lower() in ("spotify", "spotifycharts", "spotifymaps"):
            continue
        f = p.get("followers")
        if f is None:
            continue
        # Under a few hundred followers a placement is not worth the ask; far
        # above six figures and a cold email is not how it gets filled.
        if f < 300 or f > 150_000:
            continue
        emails = sorted(set(EMAIL.findall(desc)))
        links = sorted(set(LINK.findall(desc)))
        handles = sorted(set(HANDLE.findall(desc)))
        asks = bool(ASKS.search(desc))
        if not (emails or links or handles):
            continue                    # no published way to reach the curator
        score = (300 if emails else 0) + (120 if asks else 0) + \
                (60 if handles else 0) + (40 if links else 0) + min(f // 500, 200)
        out.append({**p, "description": desc, "emails": emails, "links": links,
                    "handles": handles, "invites_submissions": asks, "score": score})
    out.sort(key=lambda r: -r["score"])
    json.dump(out, open(os.path.join(OUT, "targets.json"), "w"),
              ensure_ascii=False, indent=1)

    md = ["# Playlist targets", "",
          f"{len(out)} contactable playlists out of {len(rows)} harvested. "
          "Ranked by how reachable the curator is, then by size.", ""]
    for r in out[:120]:
        who = r["emails"][0] if r["emails"] else (
            "@" + r["handles"][0] if r["handles"] else r["links"][0])
        md.append(f"## [{r['name']}]({r['url']})")
        md.append(f"{r['followers']:,} followers · {r['owner_name']} · **{who}**"
                  + ("  · asks for submissions" if r["invites_submissions"] else ""))
        md.append("")
        md.append("> " + (r["description"][:300] or "(no description)"))
        md.append("")
    path = os.path.join(OUT, "targets.md")
    open(path, "w").write("\n".join(md))
    print(f"{len(out)} contactable of {len(rows)} harvested -> {path}")
    with_email = sum(1 for r in out if r["emails"])
    print(f"  {with_email} publish an email address")
    print(f"  {sum(1 for r in out if r['invites_submissions'])} explicitly ask for submissions")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "auth-url":
        cmd_auth_url()
    elif cmd == "exchange":
        cmd_exchange(sys.argv[2])
    elif cmd == "harvest":
        n = 200
        if "--max-per-query" in sys.argv:
            n = int(sys.argv[sys.argv.index("--max-per-query") + 1])
        cmd_harvest(n)
    elif cmd == "qualify":
        cmd_qualify()
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
