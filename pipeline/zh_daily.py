#!/usr/bin/env python3
"""Render and publish the Chinese cut of a scheduled track.

    python3 pipeline/zh_daily.py 2026-08-29 "标题" "钩子那一行"
    python3 pipeline/zh_daily.py --slug the-filter "标题" "钩子那一行"

Everything mechanical lives here. The one thing it cannot do is translate, so
it refuses to run until the bilingual lyric file exists at
music-assets/zh/<slug>-lyrics-zh.json, written by the model that day. That file
is a list of {"text": 中文, "en": English, "s": start, "e": end} with the SAME
timings as the English lyric file — copy them, do not re-transcribe.

On success it prints the caption and the raw video URL, ready to paste into the
Notion page (Notion is an MCP call, so it is not scriptable from here).
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIPE = os.path.join(ROOT, "pipeline")
ASSETS = os.path.join(ROOT, "music-assets")
ZH = os.path.join(ASSETS, "zh")
BRANCH = "claude/philosophical-king-poster-raq2ke"
RAW = (f"https://raw.githubusercontent.com/jordanjayhays-cpu/jordan-projects/"
       f"{BRANCH}/music-assets/zh/")
# Chinese posts point at QQ Music, not hyperfollow: hyperfollow routes to
# Spotify, which is not licensed in mainland China.
QQ = "https://y.qq.com/n/ryqq/singer/0013KuFu4EV5q8"


def sh(*cmd):
    subprocess.check_call(cmd)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--slug" in sys.argv:
        slug = args[0]
        rest = args[1:]
    else:
        day = args[0]
        schedule = json.load(open(os.path.join(PIPE, "state.json"))).get("schedule", {})
        slug = schedule.get(day)
        if not slug:
            sys.exit(f"state.json has no track against {day}")
        rest = args[1:]
    if len(rest) < 2:
        sys.exit(__doc__)
    title_zh, hook_zh = rest[0], rest[1]

    lyr = os.path.join(ZH, f"{slug}-lyrics-zh.json")
    if not os.path.exists(lyr):
        sys.exit(f"missing {lyr} — write the bilingual translation first")

    src = None
    for name in (f"{slug}-teaser-v2.mp4", f"{slug}-teaser.mp4"):
        if os.path.exists(os.path.join(ASSETS, name)):
            src = os.path.join(ASSETS, name)
            break
    art = os.path.join(ASSETS, f"{slug}-art.jpg")
    if not src or not os.path.exists(art):
        sys.exit(f"missing teaser or art for {slug}")

    # Sanity-check the translation before spending five minutes rendering.
    zh_lines = json.load(open(lyr))
    en_lines = json.load(open(os.path.join(ASSETS, f"{slug}-lyrics.json")))
    if len(zh_lines) != len(en_lines):
        sys.exit(f"{len(zh_lines)} translated lines vs {len(en_lines)} segments — "
                 f"timings must match one to one")
    blank = sum(1 for l in zh_lines if not l.get("text", "").strip())
    if blank > len(zh_lines) / 3:
        sys.exit(f"{blank} of {len(zh_lines)} translated lines are empty — "
                 f"looks unfinished")

    wav = f"/tmp/{slug}-zh.wav"
    sh("ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vn", "-ac", "1",
       "-ar", "44100", wav)
    out = os.path.join(ZH, f"{slug}-zh.mp4")
    os.makedirs(ZH, exist_ok=True)
    sh(sys.executable, os.path.join(PIPE, "kinetic_render.py"), slug, title_zh,
       hook_zh, "QQ音乐搜索「Philosophical King」", art, wav, lyr, out)
    os.remove(wav)

    sh("git", "-C", ROOT, "add", f"music-assets/zh/{slug}-zh.mp4", f"music-assets/zh/{slug}-lyrics-zh.json")
    subprocess.call(["git", "-C", ROOT, "-c", "user.name=Claude",
                     "-c", "user.email=noreply@anthropic.com", "commit", "-q",
                     "-m", f"zh: Chinese cut of {slug} ({title_zh})"])
    sh("git", "-C", ROOT, "push", "-q", "origin", BRANCH)

    caption = (f"{title_zh}：{hook_zh} 👑\n\n"
               f"251 首中的一首。把哲学里的每一个念头，写成一首歌。\n\n"
               f"QQ音乐搜索「Philosophical King」：{QQ}\n\n"
               f"#哲学 #说唱 #独立音乐")
    print("\n=== PASTE INTO NOTION ===")
    print(f"slug     : {slug}")
    print(f"video    : {RAW}{slug}-zh.mp4")
    print(f"size     : {os.path.getsize(out) / 1048576:.1f} MB")
    print("caption  :")
    print(caption)


if __name__ == "__main__":
    main()
