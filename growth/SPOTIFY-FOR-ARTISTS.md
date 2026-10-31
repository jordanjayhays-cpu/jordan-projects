# Getting back into Spotify for Artists

Jordan is locked out. The profile says *"This artist profile has already been
claimed. Ask your team to invite you."* He doesn't remember which email claimed
it. This is the recovery path, in the order worth trying.

Every link here was checked by reading the page body on 2026-08-27, not by
status code — **Spotify serves its 404 page with HTTP 200**, so a link can look
alive and be dead. That is what produced the "This page is out of tune" /
"Esta página se ha ido con la música a otra parte" pages.

---

## Route 1 — DistroKid (strongest, and it skips the lockout entirely)

Spotify's own provider directory lists **DistroKid as a *preferred* provider**,
and the directory says preferred providers "offer instant access to Spotify for
Artists for all their users."

<https://artists.spotify.com/providers>

Jordan has working DistroKid access. So the fastest route is not recovering the
old Spotify login at all — it is asking DistroKid to grant access to the account
he *can* log into.

1. **In DistroKid**, open the release/artist page and look for the Spotify for
   Artists link. DistroKid exposes this because of the preferred relationship.
2. Or submit the request directly at
   <https://artists.spotify.com/c/team/access/artist> while logged into whatever
   Spotify account he wants to use.

**Uncertainty, stated plainly:** Spotify's help page also says *"You can't
request to join a claimed team — ask the team's Admin to invite you."* Whether
the preferred-provider instant-access path overrides an existing claim is not
documented either way, and I could not verify it without his login. It costs one
click to find out, which is why it's first.

---

## Route 2 — find the forgotten email by enumeration

Spotify documents this themselves on the "Can't log in" page: go to password
reset and type in candidate addresses. **If the address is registered, Spotify
says the reset email was sent. If it isn't, it doesn't.** So the reset form is a
yes/no oracle for "does this email have a Spotify account" — he doesn't need to
remember, he needs to guess and check.

<https://accounts.spotify.com/en/password-reset>

Feed it every address he's ever owned: the student address, old Gmails, work
addresses, anything from before the project started.

**Also try the no-password logins.** Spotify's page notes the account may have
been created with **phone number, Google, Facebook, or Apple** — in which case no
password exists and reset will never work no matter how many emails he tries.
The "Continue with Google / Facebook / Apple" buttons on the login page are one
tap each and are worth doing before any email guessing.

**And:** the login email can be different from the business email Spotify sends
artist updates to. If he remembers getting Spotify for Artists mail somewhere,
that address is a lead but not necessarily the login.

---

## Route 3 — the phone app shows the email

If he's still logged into Spotify on his phone, the account email is displayed
in the app: **Settings → Account**. That is the single fastest answer and needs
no guessing. Try it before Route 2.

Browser saved passwords are the same idea: `chrome://settings/passwords`, search
"spotify".

---

## Route 4 — contact Spotify

Spotify's stated fallback: *"If you were the only admin on your team, contact
us."* That is exactly Jordan's situation.

<https://support.spotify.com/artists/contact-spotify-support/>
(requires being logged into *any* Spotify account first)

Lead with proof of ownership, which is strong here:

- He is the DistroKid account holder for the entire 251-track catalogue
- DistroKid is a Spotify preferred provider
- He can supply the artist URI and the UPC of any release on demand

Manual review; Spotify says a few days.

---

## Why this matters

Spotify for Artists is the only way to pitch unreleased tracks to editorial
playlists, and it is free. Pitching is the single highest-value free lever left
for future PK releases — everything else in this repo is posting into channels
with no distribution. One editorial placement outweighs a month of daily posts
at current numbers.

Pitch window: submit **at least 7 days before release date**, ideally more.
<https://support.spotify.com/us/artists/article/pitching-music-and-videos-to-playlist-editors/>

This also means: **stop releasing on the day.** Any track worth pitching needs to
be scheduled far enough ahead that the pitch fits.

---

## Reference

- Can't log in: <https://support.spotify.com/us/artists/article/cannot-log-in-to-spotify-for-artists/>
- Getting access: <https://support.spotify.com/us/artists/article/getting-access-to-spotify-for-artists/>
- Provider directory: <https://artists.spotify.com/providers>
