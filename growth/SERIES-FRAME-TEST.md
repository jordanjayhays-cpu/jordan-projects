# Series frame test — Aug 29 to Sep 7 2026

## What changed

Every caption from Aug 29 onward carries two changes:

**1. A complete hook line.** The old captions opened on a seven-word slice of a
Whisper segment. Whisper segments on breath, not on clauses, so most landed
mid-sentence:

| Date | Old first line | New first line |
|---|---|---|
| Aug 29 | `Never mind design, 👑` | `Imagination replaced with society's face. 👑` |
| Aug 30 | `And by loss, yet free 👑` | `The answers lie in who we are. 👑` |
| Aug 31 | `Greatness convenes zoom in 👑` | `Zoom in, zoom out — see the picture complete. 👑` |
| Sep 1 | `Policy shift, but the core 👑` | `The rules are illusion — we grind anyway. 👑` |
| Sep 2 | `Each step was a death, 👑` | `Each step was a death, each truth was reborn. 👑` |
| Sep 3 | `and strife. Purpose is carved 👑` | `Purpose is carved from the stone of life. 👑` |
| Sep 4 | `Ask and it moves, 👑` | `Ask and it moves, ask and it breathes. 👑` |
| Sep 5 | `The ego strives, true happiness 👑` | `We carry our prisons within our minds. 👑` |
| Sep 6 | `What have we lost? 👑` | `We trade moments for money, hearts for a name. 👑` |
| Sep 7 | `decide or does 👑` | `One moment, one choice, infinite streams. 👑` |

Every new hook is a real line from that track's own lyric JSON. Punctuation was
normalised; no words were changed.

**2. The series line**, as the second paragraph:

> Track {n} of 251 — turning every idea in philosophy into a song.

Numbers are the track's position in the posting run (`state.json` → `posted`),
out of the 251-track catalogue. Aug 29 is #15.

Full caption shape, identical on all four channels:

```
<hook> 👑
Track 15 of 251 — turning every idea in philosophy into a song.
Full track everywhere: https://hyperfollow.com/PhilosophicalKing
#Philosophy #PhilosophicalKing
```

## What was deliberately left alone

**Aug 26–28 keep the old captions.** Those three days carry the 15-second cuts
for the retention test (`music-assets/short15/`). Rebuilding a post means
re-uploading its video, and re-uploading the 30-second teaser over them would
have silently destroyed that test. They stay as they are until it reads out.

**The videos did not change.** Aug 29 – Sep 7 are the same 30-second teasers
that were already queued, re-uploaded byte-identical. Only text moved.

**YouTube titles did not change.** The title is arguably the better place for a
series number on Shorts, but changing caption *and* title at once would make the
result unreadable. If the caption version shows anything, try titles next.

## How to read it

This is **not a clean A/B**. Two variables moved together, and at roughly 40
views per video no split test could reach significance anyway. Pretending
otherwise would be false precision.

Read it directionally, on the metric the change actually targets:

| Metric | Where | Baseline (Aug 15–28) | Read on |
|---|---|---|---|
| **Profile visits per video** | IG + TikTok insights | record before Aug 29 | ~Sep 8 |
| Follows per video | IG + TikTok insights | ~0 | ~Sep 8 |
| Saves and shares | IG insights | record before Aug 29 | ~Sep 8 |

**Profile visits is the one that matters.** The series frame is a claim about
whether someone who just watched wants to know what else there is. That shows up
as a profile visit long before it shows up as a follower.

Average percentage viewed is *not* the metric here — a caption cannot change
watch-through much. That belongs to the 15-second test.

## Honest expectations

At this volume, "it worked" looks like profile visits going from near-zero to a
handful per video. It will not look like a follower spike. If nothing moves at
all by Sep 8, the problem is upstream of the caption — most likely the first
second of video — and lever 5 in the playbook is the next thing to try.
