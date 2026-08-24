#!/usr/bin/env python3
"""
Create a Substack DRAFT from a markdown essay.

Deliberately stops at the draft. `publish_draft` and `schedule_draft` exist in
the library and are one line away, but the essay is the piece readers would pay
for and the only channel where automation would be visible to them. Jordan reads
it and presses publish. That costs him thirty seconds and removes the whole class
of "the AI published something wrong under my name".

Auth: SUBSTACK_COOKIE — the `substack.sid` value from a logged-in browser
(DevTools -> Application -> Cookies). Never a password, never in the repo.
Cookies rotate, so expect to refresh this occasionally.

This talks to Substack's PRIVATE API. It is not sanctioned and can break without
warning when they change something. Fine for drafts on your own publication;
know that going in.

Usage:
  substack_draft.py essay.md --title "..." [--subtitle "..."] [--youtube URL] [--dry-run]

Front matter is optional; --title wins over a leading "# Heading".
"""
import argparse, os, re, sys

PUBLICATION = "https://philosophicalkingmusic.substack.com"


def split_title(md, title_arg):
    """Take the title from --title, else lift a leading '# Heading' out of the body."""
    lines = md.strip().split("\n")
    title = title_arg
    if not title and lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()
        lines = lines[1:]
    body = "\n".join(lines).strip()
    return title, body


def build(md, title, subtitle, user_id, youtube_url=None):
    from substack.post import Post
    post = Post(title=title, subtitle=subtitle or "", user_id=user_id)
    post.from_markdown(md)
    if youtube_url:
        # The video goes last, after the essay — it is the payoff, not the intro.
        post.paragraph()
        post.youtube(youtube_url)
    return post


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("markdown", help="path to the essay in markdown")
    ap.add_argument("--title")
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--youtube", help="YouTube URL to embed at the end")
    ap.add_argument("--dry-run", action="store_true",
                    help="build and print the draft structure without touching Substack")
    a = ap.parse_args()

    md = open(a.markdown, encoding="utf-8").read()
    title, body = split_title(md, a.title)
    if not title:
        sys.exit("no title: pass --title or start the file with '# Title'")

    if a.dry_run:
        from substack.post import Post
        post = build(body, title, a.subtitle, user_id=0, youtube_url=a.youtube)
        draft = post.get_draft()
        blocks = draft.get("draft_body", {})
        import json
        content = json.loads(blocks)["content"] if isinstance(blocks, str) else blocks.get("content", [])
        print(f"title:    {title}")
        print(f"subtitle: {a.subtitle or '(none)'}")
        print(f"blocks:   {len(content)}")
        kinds = {}
        for c in content:
            kinds[c.get("type", "?")] = kinds.get(c.get("type", "?"), 0) + 1
        for k, v in sorted(kinds.items()):
            print(f"  {k:16} x{v}")
        if a.youtube:
            print(f"youtube:  {a.youtube}")
        print("\ndry run — nothing sent to Substack")
        return 0

    from substack import Api
    cookie = os.environ.get("SUBSTACK_COOKIE")
    email = os.environ.get("SUBSTACK_EMAIL")
    password = os.environ.get("SUBSTACK_PASSWORD")

    if cookie:
        api = Api(cookies_string=f"substack.sid={cookie}", publication_url=PUBLICATION)
    elif email and password:
        # Simpler to set up than the cookie, and it does not expire. Substack
        # defaults to magic-link sign-in, so a password may need setting first
        # under Settings -> Account.
        api = Api(email=email, password=password, publication_url=PUBLICATION)
    else:
        sys.exit("set SUBSTACK_EMAIL + SUBSTACK_PASSWORD (simplest), or "
                 "SUBSTACK_COOKIE with the substack.sid value from a logged-in browser")
    user_id = api.get_user_id()
    post = build(body, title, a.subtitle, user_id=user_id, youtube_url=a.youtube)
    draft = api.post_draft(post.get_draft())
    print(f"draft created: {PUBLICATION}/publish/post/{draft.get('id')}")
    print("review it and press publish yourself — this script never publishes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
