# The Wanderer — locked character & style spec

Every PK mini movie uses the **same character**, so the films read as one body of work.
Paste both blocks verbatim into every image prompt. Do not paraphrase them — the wording
is what holds the character stable across separate generations.

## Character block

> RECURRING CHARACTER, identical in every image: a solitary figure seen strictly from
> behind, face never visible, dead-centre, wearing a long dark hooded robe falling all the
> way to the ground with a deep hood pulled up, shoulders squared, arms hanging straight
> down at the sides, rendered as a near-black silhouette with faint teal rim-light along
> the hood and shoulders.

Why it holds: the figure is always **back-to-camera and silhouetted**, so there is no face
to mismatch between generations. Identity is carried by *shape* — deep hood, ground-length
hem, squared shoulders, arms straight down — which survives even when he is a black
cut-out against blown-out light.

## Style block

> Stylized cinematic illustration, vintage 35mm film still: flat graphic shapes, minimal
> fine detail, heavy atmospheric haze and light bloom, a strictly monochrome teal-and-cyan
> palette — deep blue-black shadows, glowing turquoise mid-tones, pale aqua highlights, no
> other hues — soft vignette, subtle film grain. Centered symmetrical composition.
> No text, no watermark.

Add `strong backlight glow` when the shot faces a light source. The teal palette is the
brand teal (`#c8e0d8` family), so the wordmark and lyrics sit in the same colour world.

## Post-processing (required)

The generator prints a film border into the frame. Trim it before rendering:

```python
m = int(w * 0.055)
im.crop((m, m, w - m, h - m)).save(f)
```

## Cutting to the lyrics

Shots are a fixed 3s each, so `n_shots = round(duration / 3)`. Assign each 3s window the
line that **dominates** it, not the line that starts in it, and write the shot to that
image. The Cave's sequence is the reference:

| # | Window | Line | Shot |
|---|--------|------|------|
| 1 | 0–3 | Each step was a death | dark passage, one pinprick of light |
| 2 | 3–6 | the sunlight burned | cave mouth blazing |
| 3 | 6–9 | beyond what I'd ever discerned | vast mountain world revealed |
| 4 | 9–12 | Shadows dance where the darkness thrives | his shadow thrown huge on the wall |
| 5 | 12–15 | Break the chains, step outside | manacle snapping open |
| 6 | 15–18 | The cave dissolves, truth's light collides | rock splitting, light tearing through |
| 7 | 18–21 | Outside the cave, I saw the sky | open rock beneath an immense sky |
| 8 | 21–24 | The stars, the sun, the questions why | star field, him tiny beneath it |
| 9 | 24–27 | Truth ain't easy, it's sharp, it's cold | knife-edge ridge, sleet, hard light |
| 10 | 27–30 | I went back | walking back into the black cave mouth |

Note the song is **non-linear** — it leaves the cave in verse one and flashes back to the
shadows afterwards. Follow the lyric, not the myth's chronology.
