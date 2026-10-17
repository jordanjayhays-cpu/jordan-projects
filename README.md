# 👑 Philosophical King

An automatic daily posting machine. Every day at **10:00 Madrid time (08:00 UTC)** a GitHub
Action renders a 1080×1080 philosophy quote card and posts it to your **Facebook Page** and
linked **Instagram** account using the official **Meta Graph API** — no third-party services,
no servers, no cost.

## How it works

```
quotes.json ──▶ post.js generate ──▶ ImageMagick renders images/quote-YYYY-MM-DD.jpg
                                            │
                     image committed to the repo (public raw.githubusercontent.com URL)
                                            │
                     post.js publish ──▶ Facebook  /{PAGE_ID}/photos   (direct file upload)
                                    └──▶ Instagram /{IG_USER_ID}/media + /media_publish
```

| File | Purpose |
|---|---|
| `quotes.json` | 38 public-domain philosophy quotes (Marcus Aurelius, Seneca, Epictetus, Socrates, Plato, Aristotle, Nietzsche) |
| `generate-image.sh` | Renders the quote card with ImageMagick (pre-installed on GitHub runners) |
| `post.js` | Node 20+, zero npm dependencies. `generate` picks and renders the quote of the day; `publish` posts to Facebook + Instagram |
| `.github/workflows/philosophical-king.yml` | Daily schedule + manual run with optional `quote_index` |

The quote of the day is `day-of-year % number-of-quotes`, so it rotates through the whole
list and never needs state. Override it any time with the `quote_index` input on a manual run.

> **Important:** this repository must stay **public** — Instagram's API downloads the image
> from the repo's `raw.githubusercontent.com` URL, which only works for public repos.

---

## Setup guide (from zero)

### 1. Get your accounts ready

1. Your **Facebook Page** already exists ✔
2. Switch your **Instagram** account to a professional account:
   Instagram app → **Settings → Account type and tools → Switch to professional account**
   (choose *Creator* or *Business*, either works).
3. Link Instagram to the Facebook Page:
   Facebook Page → **Settings → Linked accounts → Instagram → Connect account**
   (or from Instagram: **Edit profile → Page → connect your Page**).

### 2. Create a Meta app

1. Go to [developers.facebook.com](https://developers.facebook.com) and log in with the
   Facebook account that owns the Page.
2. **My Apps → Create App** → use case **Other** → type **Business** → give it any name
   (e.g. `philosophical-king-poster`).
3. That's it — the app can stay in **Development mode**. Development-mode apps can post to
   Pages/Instagram accounts owned by the app's own admins **without App Review**, which is
   exactly our case.

### 3. Generate an access token

1. Open the [Graph API Explorer](https://developers.facebook.com/tools/explorer/).
2. Select your app in the top-right dropdown.
3. **Permissions** → add:
   - `pages_show_list`
   - `pages_manage_posts`
   - `pages_read_engagement`
   - `instagram_basic`
   - `instagram_content_publish`
4. Click **Generate Access Token** and approve the popup (select your Page and Instagram
   account when asked). Copy the token — this is your short-lived **user token**.

### 4. Exchange it for a never-expiring Page token

Run these in a terminal (fill in the CAPS placeholders):

```bash
# 4a. Short-lived user token -> long-lived user token (~60 days)
curl "https://graph.facebook.com/v21.0/oauth/access_token?grant_type=fb_exchange_token&client_id=APP_ID&client_secret=APP_SECRET&fb_exchange_token=SHORT_LIVED_TOKEN"
```

`APP_ID` and `APP_SECRET` are in your app's dashboard under **App settings → Basic**.
Copy the `access_token` from the response, then:

```bash
# 4b. Long-lived user token -> Page token + Page ID
curl "https://graph.facebook.com/v21.0/me/accounts?access_token=LONG_LIVED_USER_TOKEN"
```

The response lists your Pages. Find *Philosophical King* and copy:
- `access_token` → this is your **Page token**. A Page token obtained from a long-lived
  user token **does not expire** — this is the one we'll store.
- `id` → this is your **`FB_PAGE_ID`**.

```bash
# 4c. Get the Instagram business account ID linked to the Page
curl "https://graph.facebook.com/v21.0/PAGE_ID?fields=instagram_business_account&access_token=PAGE_TOKEN"
```

Copy `instagram_business_account.id` → this is your **`IG_USER_ID`**.
(If this field is missing, the Instagram account isn't linked to the Page yet — redo step 1.3.)

### 5. Add the GitHub Actions secrets

Repo → **Settings → Secrets and variables → Actions → New repository secret**, three times:

| Secret | Value |
|---|---|
| `META_ACCESS_TOKEN` | the Page token from step 4b |
| `FB_PAGE_ID` | the Page ID from step 4b |
| `IG_USER_ID` | the Instagram ID from step 4c (optional — omit to post to Facebook only) |

### 6. Test it

Repo → **Actions → Philosophical King — Daily Post → Run workflow**. Optionally set
`quote_index` (e.g. `0` for the first quote). Within a minute or two you should see the
post on your Facebook Page and Instagram feed.

From then on it posts automatically every day at 10:00 Madrid time. 🎉

---

## Troubleshooting

- **`(#200) permission error` / `(#10)`** — token is missing a permission from step 3, or
  you skipped selecting the Page/Instagram account in the token popup. Regenerate the token.
- **`Media ID is not available` on Instagram** — Meta was still processing the image;
  `post.js` already retries 5 times with growing delays, but if it still fails, re-run the
  workflow.
- **Instagram fails, Facebook works** — check the repo is **public** and the committed image
  opens at `https://raw.githubusercontent.com/OWNER/REPO/BRANCH/images/quote-....jpg`.
- **Nothing posts at 10:00 sharp** — GitHub schedules can start up to ~15 minutes late;
  that's normal.
- **Token stopped working** — if you change the Page's or your account's password, or remove
  the app, Meta invalidates tokens. Redo steps 3–5.

## Local testing

```bash
# render a card (needs ImageMagick + DejaVu fonts)
node post.js generate

# post it (fill in your real values)
META_ACCESS_TOKEN=... FB_PAGE_ID=... node post.js publish
```
