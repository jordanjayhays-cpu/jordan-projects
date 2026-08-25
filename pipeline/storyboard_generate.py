#!/usr/bin/env python3
"""
Generate a storyboard's shots as Veo 3 clips, in order, with visual continuity.

The point of this file is the CHAINING. Generating 34 clips from 34 independent
prompts produces 34 unrelated videos - the first test cut from a mountain range
into a cave inside a single 8-second clip. Instead each shot is generated with
the PREVIOUS clip's final frame passed back as a reference image, so the look,
palette and staging carry forward and the result reads as one film.

Three things are pinned into every prompt:
  - the locked character block (back-to-camera silhouette, never a face)
  - the locked style block (flat graphic, monochrome teal, 35mm grain)
  - "single continuous shot, no cuts" - Veo will cut scenes inside one clip if
    the prompt leaves it room

Clips are expensive. So: --plan prints what would be generated and costs nothing,
--only N generates a single shot, and --from N resumes a part-finished run
without re-paying for the shots already done.

Usage:
  storyboard_generate.py <storyboard.json> <out_dir> [--plan] [--only N] [--from N] [--to N]
"""
import argparse, json, os, subprocess, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

CHAR = ("RECURRING CHARACTER, identical in every shot: a solitary figure seen strictly from "
        "behind, face never visible, wearing a long dark hooded robe falling all the way to the "
        "ground with a deep hood pulled up, shoulders squared, arms hanging straight down at the "
        "sides, rendered as a near-black silhouette with faint teal rim-light along the hood and "
        "shoulders.")
# "vintage 35mm film still" is what the stills prompts use, and for video Veo takes
# it literally: it draws an actual filmstrip - sprocket holes, edge scratches, a
# frame inside the frame. Cropping it away costs ~20% of every shot, so it is said
# differently here and ruled out explicitly instead.
STYLE = ("Stylized cinematic illustration with the colour and grain of vintage 35mm film: flat "
         "graphic shapes, minimal fine detail, heavy atmospheric haze and light bloom, a strictly "
         "monochrome teal-and-cyan palette - deep blue-black shadows, glowing turquoise mid-tones, "
         "pale aqua highlights, no other hues - soft vignette, subtle grain. The image fills the "
         "entire frame edge to edge: no film border, no sprocket holes, no filmstrip edges, no "
         "letterboxing, no frame within the frame, no text, no watermark.")

# light 0-10 -> how the exposure should read. The ramp is the story's spine, so it
# is stated explicitly rather than left to the model to infer from the description.
def exposure(v):
    if v <= 1:  return "Almost entirely black; only the faintest teal rim-light is visible."
    if v <= 3:  return "Very dark, deep blue-black, a little teal glow."
    if v <= 5:  return "Low light, teal mid-tones emerging from shadow."
    if v <= 7:  return "Bright, strong cyan-white light source, heavy bloom and haze."
    if v <= 9:  return "Very bright, highlights blowing out toward white."
    return "Almost completely overexposed, blinding white, the figure a pure black cut-out."


def build_prompt(shot):
    bits = [CHAR, STYLE, exposure(shot["light"])]
    bits.append(f"{shot['size']} SHOT. {shot['desc']}")
    bits.append(f"Camera: {shot['camera']}.")
    bits.append("A single continuous shot, no cuts, no scene changes, no dialogue, "
                "no speech, no on-screen text.")
    return " ".join(bits)


def upload_file(path):
    """
    Push a local file to Postiz and get a public URL back.

    uploadFromUrlTool only takes URLs, so a locally-extracted frame cannot go
    through it. The REST endpoint accepts multipart, which is what makes
    frame-to-frame continuity possible at all.
    """
    key = open("/tmp/claude-0/-home-user-jordan-projects/"
               "768ae2b7-9878-5207-b3e8-50f2736cf423/scratchpad/.pk").read().strip()
    out = subprocess.check_output(
        ["curl", "-sS", "-X", "POST", "https://api.postiz.com/public/v1/upload",
         "-H", f"Authorization: {key}", "-F", f"file=@{path}"])
    return json.loads(out)


def last_frame(clip, out_png):
    """Grab a clip's final frame to seed the next generation."""
    dur = float(subprocess.check_output(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", clip]).strip())
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0, dur - 0.15):.2f}",
                           "-i", clip, "-frames:v", "1", out_png])
    return out_png


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("storyboard")
    ap.add_argument("out_dir")
    ap.add_argument("--plan", action="store_true", help="print prompts, generate nothing")
    ap.add_argument("--only", type=int, help="generate just this shot number")
    ap.add_argument("--from", dest="start", type=int, default=1)
    ap.add_argument("--to", dest="end", type=int, default=999)
    a = ap.parse_args()

    sb = json.load(open(a.storyboard, encoding="utf-8"))
    shots = sb["shots"]
    if a.only:
        shots = [s for s in shots if s["n"] == a.only]
    else:
        shots = [s for s in shots if a.start <= s["n"] <= a.end]

    if a.plan:
        print(f"{sb['track']} — {len(shots)} shots\n")
        for s in shots:
            print(f"--- {s['n']:2}  {s['act']:16} {s['size']:6} light={s['light']:2}"
                  f"{'  [trim]' if s.get('trim') else ''}")
            print(f"    {build_prompt(s)[len(CHAR) + len(STYLE) + 2:]}\n")
        print(f"{len(shots)} clips · ~{len(shots) * 82 / 60:.0f} min generation")
        return 0

    os.makedirs(a.out_dir, exist_ok=True)
    sys.path.insert(0, "/tmp/claude-0/-home-user-jordan-projects/"
                       "768ae2b7-9878-5207-b3e8-50f2736cf423/scratchpad")
    import series_frame as S

    # Seed continuity from the newest already-rendered clip, so --from resumes
    # looking like the run it is continuing rather than restarting the style.
    prev_png = None
    done = sorted(f for f in os.listdir(a.out_dir) if f.startswith("clip") and f.endswith(".mp4"))
    if done:
        prev_png = last_frame(os.path.join(a.out_dir, done[-1]),
                              os.path.join(a.out_dir, ".prev.png"))
        print(f"seeding continuity from {done[-1]}")

    for s in shots:
        out = os.path.join(a.out_dir, f"clip{s['n']:02d}.mp4")
        if os.path.exists(out):
            print(f"{s['n']:2} exists, skipping"); continue
        # THE CONTINUITY LINK. Push the previous clip's last frame to Postiz and
        # hand it back to Veo as a reference, so this shot starts from where the
        # last one ended instead of reinventing the world.
        #
        # But a reference frame is WRONG when the shot changes location: shot 4
        # opened by holding shot 3's chain for seconds before finding its own
        # frame, because it was told to start there. Shots that begin somewhere
        # new set "chain": false and generate clean.
        refs = []
        if prev_png and s.get("chain", True):
            u = upload_file(prev_png)
            refs = [{"id": u["id"], "path": u["path"]}]
        prompt = build_prompt(s)
        print(f"{s['n']:2} {s['act']:16} {s['size']:6} generating...", flush=True)
        t0 = time.time()
        r = S.mcp("generateVideoTool", {
            "identifier": "veo3", "output": "horizontal",
            "customParams": [{"key": "prompt", "value": prompt},
                             {"key": "images", "value": refs}]}, tries=2)
        # Running out of video credits comes back as a 200 with an `error` key
        # rather than a failure, so an unguarded r["url"] dies with a KeyError
        # that says nothing about the real cause. Stop the run and say why -
        # every later shot would fail identically.
        if "url" not in r:
            msg = r.get("error", json.dumps(r)[:200])
            print(f"\nSTOPPED at shot {s['n']}: {msg}", file=sys.stderr)
            if "credit" in msg.lower() or "subscription" in msg.lower():
                print("Postiz video credits are exhausted. Top them up, then resume "
                      f"with:\n  --from {s['n']}\nShots already downloaded are kept "
                      "and will not be regenerated.", file=sys.stderr)
            return 1
        subprocess.check_call(["curl", "-sS", "-o", out, r["url"]])
        prev_png = last_frame(out, os.path.join(a.out_dir, ".prev.png"))
        print(f"   -> {out}  ({time.time() - t0:.0f}s)", flush=True)

    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
