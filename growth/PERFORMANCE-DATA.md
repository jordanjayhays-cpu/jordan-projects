# What performance data actually exists, and what does not

Written 2026-09-13 after twice repeating stale claims about reach as if they
were current. The rule this file exists to enforce: **if a number is not in
here with a date on it, I do not know it.**

## What I can see

| Source | Gives | Notes |
|---|---|---|
| Postiz API | whether a post PUBLISHED, ERRORED or is QUEUED | no views, no likes, nothing about reach |
| `pipeline/health.py` | channel coverage, queue depth | delivery only |

That is the whole list. Delivery is not performance. A post can publish
perfectly every day to nobody, and every check in this repo would stay green.

## What I cannot see, and why

Tested 2026-09-13, all four failed or returned partial data:

- **youtube.com watch page** — HTTP 429 from this IP after a couple of requests.
- **Piped (pipedapi.kavin.rocks)** — HTTP 403.
- **Invidious (inv.nadeko.net)** — HTTP 403.
- **returnyoutubedislikeapi.com** — only knows videos one of its users has
  opened. For everything else it creates a record on first query with
  `viewCount: 0`, so a zero from this source usually means "no data". Reading
  those zeros as real views is exactly the error this file exists to stop.

Also unavailable: YouTube Studio retention (login only), TikTok (JS-gated),
Instagram and Facebook (login-walled). n8n holds no YouTube or TikTok
credentials, checked 2026-09-13.

## Real numbers so far

Sparse, because only the dislike API's pre-existing records are trustworthy.
Each is a snapshot from its index date, not a current figure.

| Video date | Track | Views | Likes | As of |
|---|---|---|---|---|
| 2026-09-02 | The Cave | 2 | 0 | 2026-09-03 |
| 2026-09-06 | The Cost of Playing | 60 | 0 | 2026-09-06 |
| 2026-09-10 | Natsukashii | 220 | 2 | 2026-09-10 |

220 views on a single video is not nothing, and it refutes the "TikTok and
YouTube are getting no views" line I had been repeating from a note written
weeks earlier. Jordan corrected it; the data agrees with him.

## The fix

A **YouTube Data API v3 key** solves this permanently. It is free, takes about
five minutes in Google Cloud Console, and `videos?part=statistics&id=<ids>`
returns views, likes and comments for up to 50 videos in one call. With it,
this table fills itself daily instead of depending on what anyone remembers.

It does NOT give retention (average percentage viewed). That stays Studio-only,
and it is still the number that decides the 15-second question.
