# Claude Design — Philosophical King design system prompt

Paste the block below into Claude Design ("Create here"). Everything in it is drawn from
the live PK system: `PK-claude-project.md`, `pipeline/movie_render.py`, and the shipped
assets. Nothing is invented.

---

Build a design system for **Philosophical King** — a philosophy-rap artist project. 250+
tracks turning philosophical ideas (Stoicism, memento mori, Plato, Filipino values like
Kapwa and Bayanihan, critiques of modernity) into music, promoted through daily short-form
video and a Substack.

**Audience reality:** ~90% of social plays come from the Philippines; revenue is ~50%
Apple Music (US). The work has to read as serious and universal, never as a meme account.

## Voice

Calm, aphoristic, stoic-modern. Short declarative lines. One idea carries a piece. Never
salesy, never exclamation-heavy, no hype punctuation. The tone of a line carved in stone
rather than a caption written for engagement.

## Palette

Monochrome teal-and-cyan, and nothing else. This is the single strongest identity signal —
every asset should be recognisable as PK from across a room by colour alone.

- `#0e0f13` near-black — ground for everything
- `#c8e0d8` pale teal — primary text, wordmark, lyric lines
- `#e9c46a` gold — accent ONLY: rules, the landing word of a hook, never body text
- `#b09a4a` dim gold — waveforms, secondary marks
- `#7a7e87` grey — footers, URLs, metadata
- Deep blue-black shadows, glowing turquoise mid-tones, pale aqua highlights

No other hues anywhere. If something needs emphasis, it gets gold or it gets scale — not a
new colour.

## Type

A serif throughout — the reference implementation uses DejaVu Serif. Serif is deliberate:
it reads as inscription rather than interface, which is the whole point of the project.

- Wordmark: `P H I L O S O P H I C A L   K I N G`, always spaced caps
- Mark: ♛ / 👑
- Hard drop shadows only: `0 3px 0 rgba(0,0,0,.9)`. No soft glows.
- Zero border radius anywhere. Nothing rounds.

## Layout rules (from the shipping video template)

Vertical 1080×1920 is the native canvas — everything is designed for a phone held upright.

- Watermark centred at y=200, below the platform's top UI band
- Lyric/quote line centred at y≈1380, above the platform's bottom UI band
- Anything within 1100–1760px vertical needs a soft dark scrim behind it, or teal text
  disappears against teal imagery
- Wide content never touches the frame edge; the safe zone is real and platform UI eats it

## Imagery

Stylised cinematic illustration in the vintage-35mm-film-still manner: flat graphic shapes,
minimal fine detail, heavy atmospheric haze and light bloom, soft vignette, subtle grain.
Centred, symmetrical, still.

**One recurring character across everything — the Wanderer:** a solitary figure seen
strictly from behind, face never visible, dead-centre, in a long dark ground-length hooded
robe with a deep hood pulled up, shoulders squared, rendered as a near-black silhouette with
faint teal rim-light along the hood and shoulders. He is never shown from the front. His
identity lives in shape — hood, hem, squared shoulders — so it survives even when he is a
black cut-out against blown-out light.

**Never open on black.** Measured on real data: a video that faded in from black retained
48% where the same-length alternatives retained 58–75%.

## What I need

Components and templates for: quote cards, lyric cards, Substack headers, Instagram posts
(1080×1350) and Reels covers, YouTube Shorts end cards, and a simple artist page.

Every template must carry the full URL as visible text — never "link in bio" alone. The
one link in use is `https://hyperfollow.com/PhilosophicalKing`.

## What to avoid

Gradients as decoration, rounded corners, drop shadows with blur, stock-photo warmth,
emoji beyond ♛/👑, any second accent colour, anything that reads as a startup landing page.
The reference feeling is a title card from a serious film, not a SaaS hero section.
