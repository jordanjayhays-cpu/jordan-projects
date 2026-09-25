# Dealbook — Jordan's LinkedIn Network CRM

A personal CRM built from Jordan's LinkedIn connections export (999 connections, Oct 2013 → Aug 2026).

## What's here

| File | What it is |
|---|---|
| `data/connections_part*.tsv` | Source of truth — raw connection data (name, headline, connected date, flags) |
| `build.py` | Parses the TSVs, auto-tags each contact, and generates the outputs below |
| `template.html` | UI source for the CRM app |

Running `python3 build.py` generates (not committed — rebuild anytime):

| Output | What it is |
|---|---|
| `connections.csv` | Flat export — open in Excel / Google Sheets, or import into HubSpot/Notion |
| `connections.json` | Structured records with tags, for scripts and future apps |
| `crm.db` | SQLite database (`connections` table) with stage/priority/notes columns |
| `crm.html` | **The CRM app** — a single self-contained page, no server needed |

## Using the CRM (`crm.html`)

Open it in any browser. You can:

- **Search** across name, headline and company
- **Filter** by auto-tag (IE / MBA network, Founder / CEO, Sales / BD, Recruiting, Research / Insights, …), year connected, or "open to work" / "hiring" flags
- **Track deals**: set a pipeline stage per contact (To reach out → Contacted → In conversation → Deal → Parked), star priority contacts, and keep notes — all saved in the browser (localStorage)
- **Export CSV** including your stages/notes, and **Backup / Restore** your pipeline data as JSON to move between devices
- **Find on LinkedIn** — each contact links to a LinkedIn people search for their name (the connections export has no profile URLs)

## Updating the data

1. Add new connections as lines in `data/connections_part1.tsv` (tab-separated: `name`, `headline`, `Month D, YYYY`, optional `open_to_work`/`hiring`), or drop in a new `connections_partN.tsv`.
2. Run `python3 build.py` — it regenerates the CSV, JSON, SQLite DB and `crm.html`.

Auto-tag rules live in `TAG_RULES` in `build.py` — edit the regexes to change how contacts get categorized.

## Keeping it fresh

- The app has an **Insights** view (network eras, warm company paths, curated signals) computed live from the data — it updates automatically whenever the data is rebuilt.
- A weekly Routine ("Weekly LinkedIn CRM refresh", Mondays 09:30 Madrid) opens a session that asks Jordan to paste connections newer than the latest date in the data, merges them, and republishes the artifact at the same URL. The artifact itself embeds the full dataset (`const DATA = [...]`), so any session can recover the data from it even without this repo.
- Curated pattern cards live in the `SIGNALS` array in `template.html` — revise them as the network changes.

## Known limits

- The LinkedIn connections page doesn't expose emails, companies (only what's in the headline) or profile URLs. LinkedIn's full data export (Settings → Data privacy → Get a copy of your data) includes emails and URLs — feeding that file into `build.py` is the natural next upgrade.
- Pipeline data lives in the browser you use it in; use Backup/Restore to move it.
