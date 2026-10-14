#!/usr/bin/env python3
"""Append one Chinese-post entry to the top of the shared Notion page.

    NOTION_TOKEN=... python3 push_entry.py <slug> <YYYY-MM-DD> <English Title>

Reads title/hook/note from music-assets/zh/titles.json and the bilingual lyric
file, builds the blocks, and PATCHes them in after the intro divider so the new
entry lands at the top. The page-note paragraph is read from <slug>.note if it
sits next to this script, otherwise falls back to the titles.json note.
"""
import json, os, sys, urllib.request

PAGE = "3caefcda-373d-817d-8d46-dceab294f1fe"
AFTER = "a0b70f37-deae-4934-b268-8504975912b5"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANCH = "claude/philosophical-king-poster-raq2ke"
RAW = f"https://raw.githubusercontent.com/jordanjayhays-cpu/jordan-projects/{BRANCH}/music-assets/zh/"
QQ = "https://y.qq.com/n/ryqq/singer/0013KuFu4EV5q8"


def rt(text, link=None):
    o = {"type": "text", "text": {"content": text}}
    if link:
        o["text"]["link"] = {"url": link}
    return [o]


def main():
    slug, day, en_title = sys.argv[1], sys.argv[2], sys.argv[3]
    tok = os.environ["NOTION_TOKEN"]
    meta = json.load(open(f"{ROOT}/music-assets/zh/titles.json"))[slug]
    rows = json.load(open(f"{ROOT}/music-assets/zh/{slug}-lyrics-zh.json"))

    here = os.path.dirname(os.path.abspath(__file__))
    note_path = os.path.join(here, f"{slug}.note")
    page_note = open(note_path).read().strip() if os.path.exists(note_path) else meta["note"]

    caption = (f"{meta['title']}：{meta['hook']} 👑\n\n{meta['note']}\n\n"
               "把哲学里的每一个念头，写成一首歌。\n\n"
               f"QQ音乐搜索「Philosophical King」：{QQ}\n\n#哲学 #说唱 #独立音乐")

    trs = [{"object": "block", "type": "table_row",
            "table_row": {"cells": [rt("中文"), rt("English")]}}]
    for r in rows:
        trs.append({"object": "block", "type": "table_row",
                    "table_row": {"cells": [rt(r["text"]), rt(r["en"])]}})

    children = [
        {"object": "block", "type": "heading_2",
         "heading_2": {"rich_text": rt(f"{day} — {meta['title']} ({en_title})")}},
        {"object": "block", "type": "code",
         "code": {"rich_text": rt(caption), "language": "plain text"}},
        {"object": "block", "type": "paragraph",
         "paragraph": {"rich_text": rt("下载视频 / Download (MP4, 1080×1920, 30s)",
                                       f"{RAW}{slug}-zh.mp4")}},
        {"object": "block", "type": "paragraph",
         "paragraph": {"rich_text": rt(page_note)}},
        {"object": "block", "type": "table",
         "table": {"table_width": 2, "has_column_header": True,
                   "has_row_header": False, "children": trs}},
        {"object": "block", "type": "divider", "divider": {}},
    ]

    body = json.dumps({"children": children, "after": AFTER}).encode()
    req = urllib.request.Request(
        f"https://api.notion.com/v1/blocks/{PAGE}/children", data=body, method="PATCH",
        headers={"Authorization": f"Bearer {tok}", "Notion-Version": "2022-06-28",
                 "Content-Type": "application/json",
                 "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                               "(KHTML, like Gecko) Chrome/125.0 Safari/537.36"})
    try:
        out = json.load(urllib.request.urlopen(req, timeout=90))
    except urllib.error.HTTPError as e:
        sys.exit(f"Notion {e.code}: {e.read().decode()[:600]}")
    print("appended", len(out.get("results", [])), "blocks for", slug)


main()
