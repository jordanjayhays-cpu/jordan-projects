#!/usr/bin/env python3
"""
Generate a storyboard's shots as STILL images, for the free render path.

The Veo route costs real money and is capped by Postiz credits. Image
generation is a separate, working pool, so a full-length film can be made for
nothing by generating one still per shot and letting movie_render_wide.py move
a camera over them.

Same storyboard, same character and style blocks as storyboard_generate.py.
The differences are only what a still cannot have: no camera motion, no
"single continuous shot", and the figure count stated explicitly because a
still has to show the whole crowd at once rather than accumulate one.

The generator prints a film border into the image - the same defect the video
path hit - so every still is cropped by 5.5% before use, per CHARACTER.md.

Usage: storyboard_stills.py <storyboard.json> <out_dir> [--plan] [--from N] [--to N]
"""
import argparse, json, os, subprocess, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from storyboard_generate import CHAR, STYLE, exposure

BORDER = 0.055   # the generator's printed film edge, per CHARACTER.md


def crowd(count):
    """
    Say the figure count plainly. Bayanihan's whole arc is the frame filling up,
    so a shot that quietly renders one figure where thirty belong breaks it.
    Every extra person is the SAME silhouette - a crowd of him, not extras.
    """
    if count is None or count <= 1:
        return "Exactly ONE figure in frame, alone."
    if count == 2:
        return ("Exactly TWO figures, identical to each other in every detail - same hood, "
                "same ground-length robe, same squared shoulders - both seen from behind.")
    if count <= 6:
        return (f"Exactly {count} figures, all identical to each other in every detail - same "
                "hood, same ground-length robe, same squared shoulders - all seen from behind.")
    return (f"A crowd of roughly {count} figures, every one identical to the others - same hood, "
            "same ground-length robe, same squared shoulders - all seen from behind, filling "
            "the frame.")


def build_prompt(shot, extra=None):
    # `light` is optional: it is The Cave's spine, but Bayanihan's is the figure
    # COUNT, and those shots carry no light value at all.
    bits = [CHAR, STYLE]
    if "light" in shot:
        bits.append(exposure(shot["light"]))
    if "count" in shot:
        bits.append(crowd(shot["count"]))
    bits.append(f"{shot['size']} SHOT. {shot['desc']}")
    if extra:
        bits.append(extra)
    return " ".join(bits)


def trim_border(path):
    from PIL import Image
    im = Image.open(path).convert("RGB")
    w, h = im.size
    mx, my = int(w * BORDER), int(h * BORDER)
    im.crop((mx, my, w - mx, h - my)).save(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("storyboard"); ap.add_argument("out_dir")
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--from", dest="start", type=int, default=1)
    ap.add_argument("--to", dest="end", type=int, default=999)
    a = ap.parse_args()

    sb = json.load(open(a.storyboard, encoding="utf-8"))
    shots = [s for s in sb["shots"] if a.start <= s["n"] <= a.end]
    extra = sb.get("palette_note")

    if a.plan:
        for s in shots:
            print(f"--- {s['n']:2} {s['act']:20} {s['size']:6} "
                  f"count={s.get('count','-')}{'  [trim]' if s.get('trim') else ''}")
            print(f"    {build_prompt(s, extra)[len(CHAR) + len(STYLE) + 2:]}\n")
        print(f"{len(shots)} stills")
        return 0

    os.makedirs(a.out_dir, exist_ok=True)
    sys.path.insert(0, "/tmp/claude-0/-home-user-jordan-projects/"
                       "768ae2b7-9878-5207-b3e8-50f2736cf423/scratchpad")
    import series_frame as S

    for s in shots:
        out = os.path.join(a.out_dir, f"shot{s['n']:02d}.png")
        if os.path.exists(out):
            print(f"{s['n']:2} exists, skipping"); continue
        print(f"{s['n']:2} {s['act']:20} {s['size']:6} generating...", flush=True)
        r = S.mcp("generateImageTool", {"prompt": build_prompt(s, extra)}, tries=3)
        if "path" not in r:
            print(f"\nSTOPPED at shot {s['n']}: {r.get('error', str(r)[:200])}", file=sys.stderr)
            return 1
        subprocess.check_call(["curl", "-sS", "-o", out, r["path"]])
        trim_border(out)
        print(f"   -> {out}", flush=True)
        time.sleep(2)
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
