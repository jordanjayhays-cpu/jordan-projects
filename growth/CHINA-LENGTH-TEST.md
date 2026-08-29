# Length test, Chinese market only

Does a longer video hold a Chinese audience better than a short one? Douyin and
Xiaohongshu reward completion, so length is not a neutral choice.

**This test does not touch the English channels.** They are running their own
15-second test and a series-frame test, and a third variable across the same
posts would make all three unreadable.

## Two arms, not three

Jordan asked for 60s against 30s and 15s. Three arms need roughly half again as
many posts to separate, and every post here is a *different song*, so track
quality is already fighting the signal. Two arms give a readable answer sooner.

| Arm | Length | Why |
|---|---|---|
| **A** | **15s** | The floor. Renders properly, end card at 10.8s, already built. |
| **B** | **60s** | The real question. Needs full audio, see the blocker. |

30s is dropped because it is the current default and the English data already
says average view duration sits at 0:15 regardless of runtime. If 60s wins,
30s was never the interesting comparison; if 15s wins, likewise.

**Alternate daily rather than running one arm then the other.** A good week or a
bad week would otherwise land entirely on one side.

## BLOCKER: 60s needs full audio from Jordan

The pipeline only ever holds the **30-second iTunes preview**. There is no way
to build a 60-second video from it.

Full songs exist on the YouTube Topic channel but cannot be retrieved from this
server: `yt-dlp` returns "This video is not available", the same block that
stops view counts and the player endpoint. Verified 2026-08-29.

**What is needed:** full audio for six tracks, mp3 or wav, from DistroKid or
wherever the masters live. Once those exist the renderer needs no changes at
all — it sizes the end card off the audio length, so a 60-second file produces a
proper 60-second video by itself.

## BLOCKER: nothing has been posted in China yet

Five tracks are prepared and sitting on the Notion page. As of 2026-08-29 none
of them have been posted to Douyin, Xiaohongshu or WeChat Channels.

A/B testing a channel that is not running yet measures nothing. **Get one post
up first.** If the first few land at all, the test is worth running; if the
account gets no distribution at all, length is not the problem to solve.

## Measurement

**Jordan's friend has to report the numbers.** Douyin and Xiaohongshu analytics
are inside those apps behind a login, and nothing here can reach them.

Per post, three numbers:

1. **Views**
2. **Completion rate**, or average watch time if completion is not shown
3. **Likes plus saves**

Completion is the one that matters. Views are decided by the algorithm before
anyone sees the video; completion is decided by the video.

## Reading it

Six posts, three per arm. Compare **completion rate**, not views.

- **60s clearly ahead** — longer holds them, and it is worth asking for full
  audio as standard so every Chinese post is 60s.
- **15s clearly ahead** — the same finding as the English channels, and the
  Chinese posts should default to 15s.
- **Within a few points** — length is not the lever. Stop testing it and look at
  the first two seconds instead, which is what actually decides a scroll.

Three posts an arm is a small sample and every post is a different song. Treat a
small gap as noise. Only a clear separation means anything.

## Ready now

`music-assets/zh/the-filter-zh-15s.mp4`, a true 15-second cut, 15.0s exactly,
end card at 10.8s. Not a trimmed 30-second file.
