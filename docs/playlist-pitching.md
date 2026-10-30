# Playlist pitching for Philosophical King

## The one rule that matters

Spotify's own words: *"Spotify strictly prohibits using any third party service
that promises streams or playlist placement in exchange for money."*

The penalty does not land on the service. It lands on the artist and the
distributor: warnings, a per-track fee, account suspension, or the music being
removed. PK has 251 tracks on DistroKid under one account. A single bad promo
purchase can put all of them at risk, and the risk does not transfer to whoever
took the money.

So: **never buy placement, never buy streams, never use a service that
guarantees either.** Everything below is direct, free, and reaches curators who
have publicly asked to be pitched.

Paid things that are allowed, because they are Spotify's own products and are
advertising rather than placement: Marquee and Discovery Mode.

## The two routes

### 1. Editorial (Spotify's own playlists)

Free, and the single highest-value pitch there is. It happens inside Spotify for
Artists, not by email, and it only works on an **unreleased** track submitted at
least **7 days** before release. One pitch per release.

This is Jordan's to do, and it means the release calendar matters: anything
already out cannot be pitched this way. Worth pitching every future release.

### 2. Independent curators (everyone else)

This is what the tooling below is for. Thousands of people run genre playlists
and publish a submission email in the playlist description. Pitching them is
ordinary and welcome. Blasting them is not.

## The pipeline

    pipeline/playlist-keywords.json   the search vocabulary, editable
    pipeline/playlist_harvest.py      harvest, then qualify

**Harvest** sweeps every keyword through Spotify's search and records each
playlist's name, description, owner and follower count.

**Qualify** turns that into a ranked target list. It drops:

- Spotify's own editorial playlists (wrong route, see above)
- anything under 300 followers (not worth the ask) or over 150,000 (cold email
  is not how those get filled)
- anything whose curator publishes no way to reach them

and ranks what is left by reachability: a published email beats a handle, an
explicit "submissions open" beats silence, and size breaks ties.

Output lands in `music-assets/playlists/targets.md`.

### What the API can and cannot do now

Spotify cut the Web API hard in February 2026, live since 9 March.

Still works: searching playlists, and reading one playlist's description, owner
and follower count.

Gone: reading another user's playlist contents, listing a user's playlists, and
user profile lookups. **So we cannot ask "which playlists already play artists
like PK".** That was the best targeting signal and it no longer exists through
the API. We find playlists by what they call themselves and what the curator
writes, which is weaker, and we make up the difference in the pitch.

Search is also capped at 10 results per call and 1,000 deep, and development
mode apps share a quota that answers `429 QUOTA_EXCEEDED`. The harvester stops
cleanly on that and resumes next run, so a full sweep may take a few days.

## Finding curators without Spotify credentials

The API route above needs a Premium account and a dev app. There is a second
route that needs neither, and it was the one that actually produced the first
list.

Search engines have already crawled Spotify's public playlist pages, and the
**snippet they store is the playlist description**. So a curator who wrote
"submit your music: someone@gmail.com" into their description has had that
indexed, and it can be searched directly.

The query shape that works:

    site:open.spotify.com playlist <genre words> "gmail.com" submit your music

Two things learned the hard way:

- `inurl:` does not constrain reliably here and returns academic papers.
  `site:open.spotify.com` does work.
- Stacking `OR` operators collapses the result set to almost nothing. Broad and
  simple beats clever. One narrow query returned a single podcast; the broad one
  returned fourteen usable playlists.
- Results include `/show/` podcast pages as well as `/playlist/` ones. Discard
  the podcasts by eye.

Coverage is patchy, because it depends on what the index happens to hold. It
will not enumerate a niche the way the API can. Use it for a first list and for
niches the API sweep misses.

Output of the first pass: `music-assets/playlists/targets-round-1.md`.

## The pitch

One curator, one email, one track. Never a bcc list.

The reason this project can pitch honestly: most cold pitches have nothing to
say. PK has a daily release cadence, a specific and unusual angle, and a
back catalogue deep enough that there is a *right* track for almost any
playlist. Name their playlist, name the track, say in one line why that track
suits that playlist, give the link, stop.

    Subject: <Track> for <Playlist name>

    Hi <name>,

    <One specific, true sentence about their playlist that proves it was
    actually looked at. Not flattery, an observation.>

    I make philosophy rap as Philosophical King. <Track> is about <the idea in
    one clause>, and it sits in the same lane as <something already on the
    playlist, if visible>.

    <hyperfollow link>

    No worries either way, and thanks for running the playlist.

    Jordan

Do not attach anything. Do not follow up more than once, and not within two
weeks. If a curator asks for money for placement, that is the thing Spotify
prohibits: walk away and note it in the tracker so we never pitch them again.

## Tracking

Nothing is tracked yet. Proposed table, mirroring `pk_run_log`:

    pk_playlist_outreach
      playlist_id, playlist_name, curator, contact, followers,
      pitched_on, track_pitched, outcome, notes

so a curator is never pitched twice, and so we learn which tracks and which
angles actually land.
