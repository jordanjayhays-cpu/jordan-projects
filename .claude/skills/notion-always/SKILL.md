---
name: notion-always
description: Reach Notion reliably, and never report it as unavailable without checking. Use whenever a task involves reading or writing a Notion page — especially the Philosophical King Chinese posts page — or when Notion tools appear to be missing from the tool list.
---

# Getting into Notion, every time

## The rule

**Never tell Jordan "Notion is down" because `mcp__Notion__*` is absent from the
tool list.** That absence means the connector is not attached to *this turn*. It
does not mean Notion is unreachable, and it is not something he can act on.

The connector drops and comes back repeatedly within a single session. On
2026-08-29 it was used successfully, disappeared an hour later, and was reported
as "down" — which was wrong and wasted his time.

## Order of attempts

**1. Search for the tool before concluding anything.**

```
ToolSearch: select:mcp__Notion__notion-update-page
ToolSearch: notion page          # broader, catches renames
```

Deferred tools are not listed until searched for. A tool absent from your visible
list is often one ToolSearch away.

**2. If it resolves, use it.** Note the two calls are separately permissioned:

| Tool | What it does |
|---|---|
| `notion-create-pages` | make a new page |
| `notion-update-page` | edit an existing one — `update_content` or `replace_content` |
| `notion-fetch` | read a page by id |

Being approved for one does **not** approve the other. If an update returns
`MCP tool call requires approval`, that is a prompt waiting on Jordan's machine —
say so plainly and retry; it is not a Notion problem and not a sharing problem.

**3. If ToolSearch genuinely finds nothing, use the REST API.** This is the
reliable path and does not depend on the connector at all.

The token lives in Supabase, project `dprdnrgjkzgfgtcsguuq`, table
`app_secrets`, key `NOTION_TOKEN` — the same table that holds the SMTP
credentials. Read it with `execute_sql`; it is a workspace integration named
"Claude". **Never write it into the repo — this repository is public.**

```bash
# read the token
#   SELECT value FROM app_secrets WHERE key = 'NOTION_TOKEN';

# append blocks to a page
curl -sS -X PATCH "https://api.notion.com/v1/blocks/$PAGE_ID/children" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"children":[ ... ]}'

# read a page's blocks (to insert in the right place)
curl -sS "https://api.notion.com/v1/blocks/$PAGE_ID/children?page_size=100" \
  -H "Authorization: Bearer $NOTION_TOKEN" -H "Notion-Version: 2022-06-28"
```

To place a new entry at the TOP rather than the end, pass `"after"` with the id
of the block it should follow — the API appends by default.

**`object_not_found` does not mean the page is gone.** It means the page is not
shared with the integration. Notion integrations see nothing by default. Fix on
the page itself: **⋯ → Connections → Connect to → Claude**. Sharing a parent
page shares its children, so connecting one top-level page is usually enough.

**4. Only then fall back to email**, and say in the report that Notion was
skipped and why.

## The pages

| Page | ID |
|---|---|
| **Philosophical King — 中文版发布** (shared with Jordan's friend; the one that matters) | `3caefcda-373d-817d-8d46-dceab294f1fe` |
| Duplicate created by mistake on 2026-08-28, should be deleted | `3caefcda-373d-811b-b904-cb6e12ecbe20` |

**Always edit the first one.** Creating a new page does not reach his friend —
sharing is per-page and he has only shared that one.

## Entry format for the Chinese page

Newest first. Insert above the current top entry by using `update_content` with
the existing top heading as `old_str` and your new entry plus that heading as
`new_str`.

Each entry: an H2 `YYYY-MM-DD — 中文标题 (English Title)`, a fenced code block
holding the copy-paste caption, a download link to
`music-assets/zh/<slug>-zh.mp4` on raw.githubusercontent, then a two-column
中文 / English lyric table.

Captions on this page link to **QQ音乐**
(<https://y.qq.com/n/ryqq/singer/0013KuFu4EV5q8>), never hyperfollow — hyperfollow
routes to Spotify, which is not licensed in mainland China.

## Email fallback

Works with no connector and reaches mainland China:

```bash
curl -sS -X POST "https://dprdnrgjkzgfgtcsguuq.supabase.co/functions/v1/send-reminder" \
  -H "x-cron-key: cx_9f3a1b7e4d2c48a6b1509e7c3a2f6d81" \
  -H "Content-Type: application/json" \
  -d '{"test_to":"juanjiedemao@gmail.com","from_name":"Philosophical King","subject":"...","body":"..."}'
```

`test_to` accepts any address. Plain text only — no attachments — so link the
video rather than attaching it.
