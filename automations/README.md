# Automations (n8n + Supabase edge functions), as of 2026-11-24

n8n instance: neuromatch.app.n8n.cloud. Board and secrets: Supabase project neurodashboards (dprdnrgjkzgfgtcsguuq).
Rule for everything here: alert, log or draft. Nothing sends to a third party without Jordan's tap.

## Live workflows

| Workflow | Fires | Does | Backed by |
| --- | --- | --- | --- |
| Daily Brief (Telegram) | 06:45 Mon-Fri Madrid | Top 5 open tasks, board count, oldest task age, reminders, Japan call reminder | board-read v2 |
| Placewell: Japan kumiai call sheet + outcome form | 06:45 Mon-Thu, plus a form | Ten kumiai due today to Telegram; form logs each call back to kumiai_targets | kumiai-sheet, table kumiai_targets |
| Instantly campaign digest (Telegram) | 09:00 daily | Sent, replies, reply rate, bounces per active campaign; flags 3+ bounces | instantly-stats (reads every app_secrets key starting "instantly") |
| Friday scorecard (Telegram) | 16:00 Friday | Sends, replies, meetings per lane; board done/created/oldest; Massage Club requests, 5-min replies, confirmations, deposits. Writes lane_metrics | scorecard-read, mc-scorecard-read (MC project) |
| Reply landed, log plus alert | Webhook | Any inbound reply stamps replied_at on the matching prospect, logs reply_events, pings Telegram | reply-log |
| Approve-then-send gate (Telegram to Gmail) | Webhook | Draft arrives on Telegram with Send / Do not send; only Send delivers, from the lane mailbox | board-read; Gmail per lane |
| Monthly AI retro reminder | First Sunday 10:00 | The three retro questions from the gen AI operating rules | board-read |
| Board: urgent task landed, email Jordan | Event | Pre-existing | |
| Amigo Sales: send as jordan@amigosales.com | Event | Pre-existing | |

## Email skeletons (unpublished until each mailbox credential is connected)

One per lane, identical shape: Gmail trigger every 5 min (unread) -> Lane Config -> Normalise -> Classify.
noise -> mark read. prospect reply (prospect_lane = true) -> reply-log + Telegram. human inquiry -> Gmail DRAFT + Telegram. other -> nothing.
Lanes: personal (credential already connected), amigo-sales, niah, placewell, vaya, kinsol, pk-music, massage-club (read-only by the routing rule).
Tune noise_regex, keep_regex and own_domains in the Lane Config node.

## Backlog sweep (run by hand)

Inbox backlog sweep (personal Gmail): reads the last 90 days of the inbox in one run, classifies every email, logs every human reply to reply-log, one Telegram summary. Duplicate it per mailbox by switching the Gmail credential and the Lane Config values. Unpublished; run from the editor with Execute workflow.

## Email skeleton IDs

personal BdtCptK359uE5BCe (credential connected) · amigo-sales vhC1laX6rBR5tgpE · niah 66pb3ErT38OEGC6u · placewell DcbkpoEySPHSdcIf · vaya yNElJEYE2px7Ihz7 · kinsol CEnpTyQR6ttuoxKM · pk-music NmAqnrjXlzoJrk1O · massage-club ykqWnMxI3tEOloKp · backlog sweep MWYpNWNCGYaljhEa.
On the seven non-personal skeletons n8n auto-attached the personal Gmail credential at creation; their New Email trigger is DISABLED until the lane credential is selected on the three Gmail nodes.

## Webhook URLs

- Replies: https://neuromatch.app.n8n.cloud/webhook/reply-landed (POST; Instantly reply_received, HeyReach campaign webhook, or any JSON with email/text)
- Approve-then-send: https://neuromatch.app.n8n.cloud/webhook/approve-send (POST {lane, to, subject, body})
- Kumiai outcome form: open the workflow, Call Outcome Form node, copy the production URL, pin it in Telegram

## Edge functions added (neurodashboards unless noted)

board-read v2 (adds chat_id, top5, oldest_open_days), scorecard-read, reply-log, kumiai-sheet, instantly-stats, mc-scorecard-read v3 (Massage Club project, test contacts excluded).
All authenticate with header x-capture-key = app_secrets.CAPTURE_KEY (mc-scorecard-read: x-scorecard-key = SCORECARD_KEY). Telegram chat id is read from app_secrets.TELEGRAM_CHAT_ID so no workflow hardcodes it.

## Tables added

pisco_prospects, niah_prospects, comare_prospects: replied_at, reply_text, meeting_at, reply_source (+ last_sent_at where missing).
reply_events: every inbound reply. kumiai_targets: the Japan call list and its log.

## Jordan's setup steps (board task "n8n: three 2-minute setup steps", extended)

1. Telegram chat id into app_secrets.TELEGRAM_CHAT_ID (message @get_id_bot).
2. SCORECARD_KEY into the Massage Club project's app_secrets (value in the n8n node header).
3. Instantly reply webhook to /webhook/reply-landed. Optional: main workspace key as app_secrets.instantly_api_key.
4. Import the 87 kumiai into kumiai_targets.
5. Connect Gmail credentials for Amigo Sales and Vaya, wire the two disabled Send nodes in the gate, publish the email skeletons you want.

## Not built on purpose

Anything that sends LinkedIn messages or cold email from n8n. Any Massage Club customer or studio message (owned by the Massage Club ops chat; three alert proposals await Jordan's yes/no on the board).
