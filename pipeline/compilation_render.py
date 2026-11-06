#!/usr/bin/env python3
"""
Build a long-form 16:9 compilation from several tracks' 30-second previews.

Why this exists: full-length audio cannot be got at. The masters are too large
to send and YouTube refuses every download from this host - it answers "sign in
to confirm you're not a bot" even for PK's own public videos. The official
30-second iTunes previews are the only audio actually reachable, so long-form
has to be built out of many tracks rather than one.

That is not purely a consolation. A 251-single catalogue is unbrowsable; "eight
songs on death and time" is something a person can actually choose. And it is a
real YouTube format that builds watch time, which Shorts do not.

Each segment is that track's own cover art under a slow camera move, its title
card, and its lyrics. Cover art is used rather than generated stills because it
is free, authentic, already varied per track, and reads like a record sleeve.

Square art in a 16:9 frame is handled the way music videos do it: the art sits
centred and sharp over a blown-up, blurred copy of itself, so the frame is full
without cropping the artwork or pillarboxing it black.

Usage: compilation_render.py <set.json> <out.mp4>
  set.json: {"title": "...", "tracks": [{"slug": "...", "title": "..."}, ...]}
"""
import json, os, subprocess, sys, tempfile, shutil

from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1920, 1080, 30
TEAL = (200, 224, 216)
DIM = (150, 170, 165)
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
LINK = "https://hyperfollow.com/PhilosophicalKing"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "music-assets")
PREVIEW_DIRS = ["/tmp", os.path.join("/tmp/claude-0/-home-user-jordan-projects/"
                                     "768ae2b7-9878-5207-b3e8-50f2736cf423/scratchpad/music")]
TITLE_CARD = 4.0        # seconds the track title holds at the top of each segment
DISSOLVE = 1.0
ENDCARD = 6.0


def font(sz):
    return ImageFont.truetype(SERIF, sz)


def ease(t):
    return t * t * (3 - 2 * t)


def find_preview(slug):
    for d in PREVIEW_DIRS:
        for name in (f"{slug}.wav", f"{slug}-preview.wav"):
            p = os.path.join(d, name)
            if os.path.exists(p):
                return p
    return None


def stage(art_path):
    """
    Square cover art -> a full 16:9 plate.

    Blurred, over-scaled copy behind; the real artwork sharp and centred on top.
    Cropping a square cover to 16:9 would cut the art in half, and pillarboxing
    it against black wastes two thirds of the frame.
    """
    im = Image.open(art_path).convert("RGB")
    bg = im.resize((int(W * 1.6), int(W * 1.6)), Image.LANCZOS)
    bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2,
                  (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
    bg = bg.filter(ImageFilter.GaussianBlur(48))
    bg = Image.blend(bg, Image.new("RGB", (W, H), (0, 0, 0)), 0.45)
    side = int(H * 0.86)
    fg = im.resize((side, side), Image.LANCZOS)
    bg.paste(fg, ((W - side) // 2, (H - side) // 2))
    return bg


def wrap(d, text, f, maxw):
    if d.textlength(text, font=f) <= maxw:
        return [text]
    rows, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw or not cur:
            cur = t
        else:
            rows.append(cur); cur = w
    if cur:
        rows.append(cur)
    return rows


def text_rows(img, rows, y, f, alpha, spacing, colour=TEAL):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for row in rows:
        d.text((W / 2, y + 3), row, font=f, fill=(0, 0, 0, alpha), anchor="mm")
        d.text((W / 2, y), row, font=f, fill=colour + (alpha,), anchor="mm")
        y += spacing
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")


def main():
    set_path, out = sys.argv[1:3]
    spec = json.load(open(set_path, encoding="utf-8"))
    tracks = spec["tracks"]

    segs = []
    for t in tracks:
        wav = find_preview(t["slug"])
        art = os.path.join(ASSETS, f"{t['slug']}-art.jpg")
        lyr = os.path.join(ASSETS, f"{t['slug']}-lyrics.json")
        if not wav or not os.path.exists(art):
            print(f"SKIP {t['slug']}: missing {'audio' if not wav else 'art'}")
            continue
        dur = float(subprocess.check_output(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
             "-of", "csv=p=0", wav]).strip())
        segs.append({"slug": t["slug"], "title": t["title"], "wav": wav, "art": art,
                     "dur": dur,
                     "lyrics": json.load(open(lyr)) if os.path.exists(lyr) else []})
    if not segs:
        sys.exit("no usable tracks")

    tmp = tempfile.mkdtemp()
    # One concatenated audio bed. Simpler and more reliable than muxing per
    # segment and stitching, and it guarantees picture and sound stay locked.
    lst = os.path.join(tmp, "a.txt")
    with open(lst, "w") as f:
        for s in segs:
            f.write(f"file '{s['wav']}'\n")
    audio = os.path.join(tmp, "bed.wav")
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                           "-i", lst, "-c", "copy", audio])

    starts, acc = [], 0.0
    for s in segs:
        starts.append(acc); acc += s["dur"]
    total_dur = acc
    plates = [stage(s["art"]) for s in segs]
    print(f"{len(segs)} tracks, {total_dur:.0f}s total", flush=True)

    # chapter list for the YouTube description - the reason a compilation is
    # navigable at all
    chapters = "\n".join(f"{int(st // 60)}:{int(st % 60):02d} {s['title']}"
                         for st, s in zip(starts, segs))
    open(os.path.splitext(out)[0] + "-chapters.txt", "w").write(
        chapters + f"\n\nEvery track: {LINK}\n")

    black = Image.new("RGB", (W, H), (0, 0, 0))
    total = int(total_dur * FPS)
    for i in range(total):
        t = i / FPS
        idx = max(0, next((k for k, st in enumerate(starts) if st > t), len(segs)) - 1)
        s, st = segs[idx], starts[idx]
        local = t - st

        # slow alternating push/pull so consecutive tracks do not move alike
        p = local / s["dur"]
        z = (1.00 + 0.07 * ease(p)) if idx % 2 == 0 else (1.07 - 0.07 * ease(p))
        cw, ch = W / z, H / z
        img = plates[idx].crop((int((W - cw) / 2), int((H - ch) / 2),
                                int((W - cw) / 2 + cw), int((H - ch) / 2 + ch)))
        img = img.resize((W, H), Image.LANCZOS)

        if idx > 0 and local < DISSOLVE:
            prev = plates[idx - 1].resize((W, H), Image.LANCZOS)
            img = Image.blend(prev, img, ease(local / DISSOLVE))
        if t > total_dur - 1.2:
            img = Image.blend(black, img, ease(max(0.0, (total_dur - t) / 1.2)))

        d = ImageDraw.Draw(img)
        for off, col in ((2, (0, 0, 0)), (0, DIM)):
            d.text((56, H - 46 + off), "PHILOSOPHICAL KING", font=font(26),
                   fill=col, anchor="lm")

        # title card: names the track at the top of its segment, so a listener
        # always knows what they are hearing
        if local < TITLE_CARD:
            a = min(1.0, local / 0.5, (TITLE_CARD - local) / 0.8)
            if a > 0:
                img = text_rows(img, [s["title"]], 130, font(58), int(255 * a), 0)

        cur = next((l for l in s["lyrics"] if l["s"] <= local <= l["e"]), None)
        if cur and cur.get("text") and t < total_dur - ENDCARD:
            fade = max(0.0, min(1.0, (local - cur["s"]) / 0.3, (cur["e"] - local) / 0.3 + 0.4))
            if fade > 0:
                dd = ImageDraw.Draw(img)
                rows = wrap(dd, cur["text"], font(50), 1240)
                img = text_rows(img, rows, 950 - (len(rows) - 1) * 32, font(50),
                                int(255 * fade), 64)

        left = total_dur - t
        if left < ENDCARD:
            a = min(1.0, (ENDCARD - left) / 1.0, left / 1.0 + 0.25)
            if a > 0:
                img = Image.alpha_composite(
                    img.convert("RGBA"),
                    Image.new("RGBA", (W, H), (0, 0, 0, int(165 * a)))).convert("RGB")
                img = text_rows(img, [spec["title"]], 470, font(64), int(255 * a), 0)
                img = text_rows(img, [LINK], 570, font(38), int(220 * a), 0)

        img.save(f"{tmp}/{i:05d}.jpg", quality=92)
        if i % (FPS * 30) == 0:
            print(f"  {t:6.1f}s / {total_dur:.0f}s", flush=True)

    subprocess.check_call([
        "ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", f"{tmp}/%05d.jpg",
        "-i", audio, "-vf", "noise=alls=3:allf=t+u,eq=contrast=1.04:saturation=1.03",
        "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k", "-shortest", "-t", f"{total_dur:.2f}", out])
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"\ndone: {out} ({total_dur:.0f}s, {len(segs)} tracks, {W}x{H})")
    print("chapters written alongside\n")
    print(chapters)
    return 0


if __name__ == "__main__":
    sys.exit(main())
