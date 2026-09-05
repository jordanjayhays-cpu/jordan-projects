# The 15-second retention test

## What was tested

Average view duration sat at **0:15 regardless of video length**, across nine
30-second videos and 560 views, at ~53% average-percentage-viewed. If people
stop at fifteen seconds anyway, a fifteen-second video should finish at close to
100% rather than half.

Five 30s teasers were trimmed to 15.0s with a clean fade-out, no fade-in, and
scheduled against the 30s baseline. They live in `music-assets/short15/`.

**Trade-off accepted:** the 27–30s end card is cut, so the link exists only in
the caption for those days.

## The dates — read this before reading the numbers

| Days | What went out |
|---|---|
| **Aug 24, 25, 26, 27** | **15-second cuts — the test** |
| ~~Aug 28~~ | **was a test day, is now a control.** See below. |
| Aug 29 – Sep 7 | 30-second controls |

**Aug 28 (Soul Ride) must NOT be counted as a test day.** It was scheduled as
the fifth 15-second cut. On Aug 28 the song-title backfill re-rendered every
queued day from Aug 28 to Sep 10 and replaced those posts — which silently
swapped Soul Ride's 15-second cut for a fresh 30-second version. Four test days
survive instead of five.

That was avoidable: two tests were live and only one was checked against the
change. Before any bulk re-render, check what experiments are running over the
dates being touched.

## Reading it

From **Aug 31** — YouTube Studio → Analytics → Content → average percentage
viewed, per video. Compare the four 15s videos against the ~53% baseline.

- **Near 80%** — length is the constraint. Render proper 15s versions with the
  end card moved to ~13s, so the link survives.
- **Near 55%** — length is not the constraint; people are leaving for a reason
  the runtime does not fix. That points at the hook, which is the first thing on
  screen and the thing `pick_hook()` gets right about seven times in ten.

Four days is a smaller sample than planned. Treat a small gap as noise; only a
clear separation means anything.

## Note

These numbers can only be read from YouTube Studio. YouTube returns
LOGIN_REQUIRED to this server on every endpoint that carries view data, across
all client types, so Jordan has to read them.
