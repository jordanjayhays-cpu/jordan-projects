# The follow ask — test starting 2026-09-11

## Why

Spotify's **Release Radar reaches 3 listeners**. That is the whole argument.

Release Radar goes automatically to an artist's followers. PK has **28 followers**
against a total audience of 1,130. So every new release lands, by default, in
front of three people — no matter how good it is, no matter how much work went
into it.

Followers are the only number here that compounds. Playlist placement comes and
goes at the algorithm's discretion; a follower stays, and increases the automatic
reach of every release made after it. It is also the one channel PK controls
outright.

And nothing has ever asked for one. Across 26 posts, every caption ended with the
hyperfollow link and stopped. The ask was simply missing.

## What changed

One line added to the daily caption, between the series frame and the link:

> Follow Philosophical King on Spotify so the new ones find you.

Full caption from Sep 11:

> \<hook\> 👑
> Track N of 251 — turning every idea in philosophy into a song.
> Follow Philosophical King on Spotify so the new ones find you.
> Full track everywhere: https://hyperfollow.com/PhilosophicalKing
> #Philosophy #PhilosophicalKing

**Still one link, still hyperfollow.** The follow ask is words, not a second URL —
the standing rule is untouched.

## Why Spotify and not Apple Music

Jordan has stats for both and reports Spotify running "a bit better this week".

The rule was set before looking at the numbers: name whichever platform has more
listeners, unless the gap is under ~25%, in which case Spotify wins the tiebreak
because Release Radar's automatic push to followers is confirmed and Apple's
equivalent is not. "A bit better" is inside that band, so: Spotify.

Note the reason for naming **one** platform at all. It is not that Spotify is the
better service — it is that a call to action offering two choices makes the reader
decide before acting, and most people resolve that by doing nothing. One
unambiguous instruction converts better than a menu. The hyperfollow link still
routes Apple listeners to Apple; only the sentence is single-platform.

## Timing — why Sep 11 and not now

The series-frame test runs **Aug 29 – Sep 7** and is read on **Sep 8**. Adding the
follow ask during that window would move two variables at once and make neither
result readable.

The gate in `daily_post.py` is `FOLLOW_ASK_FROM = "2026-09-08"`, but posts are
scheduled 14 days ahead and the queue already reaches Sep 10, so **the first post
carrying the line is Sep 11**. The gate is a safety net, not the start date.

## What to read, and when

**Read on Sep 25** — two weeks of posts carrying the line.

The metric is **Spotify follower count**, from Spotify for Artists. Baseline is
**28 on 2026-08-27**.

| Followers on Sep 25 | Read |
|---|---|
| 28–32 | No effect. The ask isn't the constraint; reach is. Revert it. |
| 33–45 | Working. Keep it, and consider the same ask on Substack and Reddit. |
| 45+ | Strong. Worth testing a harder version, and worth revisiting whether the daily rotation should concentrate on the tracks the algorithm already favours. |

Do **not** read followers before Sep 25 and do not read any other metric off this
change. Views, retention and profile visits are not what this line is for.

## The caveat

The numbers underneath this are small — 28 followers, 117 monthly listeners, 3
Release Radar listeners. A move from 28 to 40 is twelve people, and twelve people
is well within the noise of a normal fortnight. Treat a positive result as
"worth keeping", not as proof the line works.

The honest reason to run it anyway: it costs one sentence, it cannot make things
worse, and the thing it targets — automatic distribution on every future release
— compounds in a way nothing else in this project does.
