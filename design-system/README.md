# Philosophical King — design system

**Philosophical King** is a philosophy music project: 250+ tracks turning Stoicism,
memento mori, Plato and Filipino values like Kapwa and Bayanihan into songs, promoted
through daily short-form video across YouTube, TikTok, Instagram and Facebook, plus a
Substack. The audience is roughly 90% Philippines; revenue is roughly half Apple Music
in the US. The work has to read as serious and universal — never as a meme account.

Everything in this folder is taken from the shipping system, not written for a brief.

## What's here

| File | |
|---|---|
| `tokens.css` | Colour, type, form and video safe-zone tokens as CSS custom properties |
| `components.css` | Wordmark, type scale, gold rule, cards, buttons, quote card, social post, scrim |
| `index.html` | A rendered showcase of every component — open it to see the system |
| `CHARACTER.md` | The Wanderer: the one recurring figure across all imagery |
| `assets/` | Real published output — Instagram post, video frame, six character stills |

## The rules that matter

**Monochrome teal and cyan, nothing else.** There is no second accent colour anywhere in
the brand. This is the strongest identity signal — every asset should be recognisable as
PK from across a room by colour alone. Emphasis comes from gold or from scale, never from
introducing a new hue.

| Token | Hex | Role |
|---|---|---|
| `--pk-ground` | `#0e0f13` | Near-black — the ground for everything |
| `--pk-teal` | `#c8e0d8` | Primary text, wordmark, lyric lines |
| `--pk-gold` | `#e9c46a` | **Accent only** — rules, one landing word |
| `--pk-gold-dim` | `#b09a4a` | Waveforms, secondary marks |
| `--pk-grey` | `#7a7e87` | Footers, URLs, metadata |

**Serif throughout.** It reads as inscription rather than interface, which is the whole
point of the project. Wordmark is always spaced caps: `P H I L O S O P H I C A L   K I N G`.
Mark: ♛.

**The brand font is DejaVu Serif**, and it ships in `fonts/` as woff2 with `@font-face`
already wired up in `tokens.css` — nothing to install, nothing proprietary, no network
call. It is the same face `pipeline/movie_render.py` draws every lyric line and watermark
with, so web output matches published video exactly. `DejaVu Sans` is bundled for the rare
supporting label. Licence in `fonts/LICENSE.txt` (permissive — free to embed and
redistribute).

**Nothing rounds.** `border-radius: 0` everywhere. Shadows are hard —
`0 3px 0 rgba(0,0,0,.9)` — never blurred. No gradients used as decoration.

**Gold is an accent only.** Rules, and the single landing word of a hook. Never body text,
never a whole line.

**The full URL is always visible text.** Never "link in bio" alone, on any platform,
including Instagram where it won't hyperlink. The one link in use is
`https://hyperfollow.com/PhilosophicalKing`.

**Never open on black.** Measured on real retention data: a video that faded in from black
held 48% where the same-length alternatives held 58–75%. On a short-form feed the first
second is the entire retention decision.

## Video safe zones — 1080×1920 native canvas

Short-form platform UI eats the top and bottom of the frame. These are measured positions
from the shipping renderer, not guesses.

- **y = 200** — watermark, below the top UI band
- **y ≈ 1380** — lyric or quote line, above the bottom UI band
- **1100–1760** — anything here needs a dark scrim behind it, or teal text disappears
  against teal imagery

## Imagery

Stylised cinematic illustration in the vintage-35mm-film-still manner: flat graphic
shapes, minimal fine detail, heavy atmospheric haze and light bloom, soft vignette, subtle
grain. Centred, symmetrical, still.

One recurring character across everything — **the Wanderer**. Full spec in
`CHARACTER.md`, six examples in `assets/`. He is a solitary figure seen strictly from
behind, face never visible, in a long dark ground-length hooded robe, hood up, shoulders
squared — a near-black silhouette with faint teal rim-light. He is never shown from the
front. His identity lives in shape, so it survives even as a cut-out against blown-out
light.

## Voice

Calm, aphoristic, stoic-modern. Short declarative lines. One idea carries a piece. Never
salesy, no exclamation marks, no urgency. The tone of a line cut into stone rather than
written for engagement.

## What to build

Quote cards, lyric cards, Substack headers, Instagram posts (1080×1350), Reels covers,
YouTube Shorts end cards, and a simple artist page. Every template carries the full URL as
visible text.

## What to avoid

Gradients as decoration, rounded corners, blurred shadows, stock-photo warmth, emoji
beyond ♛, any second accent colour, anything resembling a SaaS landing page. The reference
is a title card from a serious film, not a hero section.
