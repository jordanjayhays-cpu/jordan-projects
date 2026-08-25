#!/usr/bin/env python3
"""
PK long-form renderer: a full-length 16:9 lyric film. NOT a Short.

YouTube classifies a video as a Short when it is vertical/square AND three
minutes or under. This breaks both conditions: 1920x1080, full song length. A
16:9 video is never a Short regardless of duration, so the aspect alone is the
guarantee and the length is belt-and-braces.

Deliberately a sibling of movie_render.py rather than a flag on it. The vertical
renderer is production, running daily; the safe zones, shot pacing, dissolve
length and end card all differ here, and threading two layouts through one file
would put the working one at risk for no gain.

Shot pacing is the real difference. The vertical standard is 2.75s per shot,
which at four minutes would need ~87 stills. Here shots hold 12-18s under a slow
camera move, so 12-20 stills carry a whole song.

Usage: movie_render_wide.py <shots_dir> <audio> <lyrics.json> <out.mp4> [seconds]
  shots_dir must contain shot1.png, shot2.png, ... in order.
"""
import json, os, subprocess, sys, tempfile, shutil

from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1920, 1080, 30
TEAL = (200, 224, 216)
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
DISSOLVE = 1.2          # long shots deserve a slow dissolve; 0.45s would snap
OVERSCAN = 1.28
LINK = "https://hyperfollow.com/PhilosophicalKing"
ENDCARD = 7.0           # seconds of end card, over the final shot


def font(sz):
    return ImageFont.truetype(SERIF, sz)


def ease(t):
    return t * t * (3 - 2 * t)


def prep(path):
    """
    Build the over-scanned plate a camera move crops out of.

    A 16:9 source can simply be scaled up. A SQUARE one cannot: the generator
    returns square images, and cropping 16:9 out of an over-scanned square shows
    roughly the middle 40% at 2.7x - which threw away the house in the shot whose
    entire subject was a line of figures wading toward it.

    So square (and portrait) sources are composited instead: the full image, whole
    and sharp, over a blown-up blurred copy of itself that fills the sides. The
    composition survives intact and the frame still reads as full rather than
    pillarboxed against black.
    """
    im = Image.open(path).convert("RGB")
    if abs(im.width / im.height - W / H) < 0.12:
        scale = max(W * OVERSCAN / im.width, H * OVERSCAN / im.height)
        return im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)

    pw, ph = int(W * OVERSCAN), int(H * OVERSCAN)
    bs = max(pw / im.width, ph / im.height) * 1.5
    bg = im.resize((int(im.width * bs), int(im.height * bs)), Image.LANCZOS)
    bg = bg.crop(((bg.width - pw) // 2, (bg.height - ph) // 2,
                  (bg.width - pw) // 2 + pw, (bg.height - ph) // 2 + ph))
    bg = bg.filter(ImageFilter.GaussianBlur(52))
    bg = Image.blend(bg, Image.new("RGB", (pw, ph), (0, 0, 0)), 0.42)
    side = ph
    fg = im.resize((int(im.width * side / im.height), side), Image.LANCZOS)
    bg.paste(fg, ((pw - fg.width) // 2, 0))
    return bg


# Slower and shallower than the vertical moves: a 15s shot magnifies everything,
# and a push that reads as gentle over 2.75s becomes a lurch over 15.
MOVES = [
    (1.00, 1.06,  0.00,  0.00),
    (1.05, 1.00,  0.12,  0.00),
    (1.00, 1.05, -0.14,  0.08),
    (1.04, 1.04, -0.22,  0.00),
    (1.00, 1.07,  0.00, -0.10),
    (1.06, 1.00,  0.00,  0.12),
    (1.02, 1.06,  0.16,  0.06),
    (1.05, 1.00, -0.10, -0.08),
]


def frame_from(im, p, move):
    z0, z1, dx, dy = move
    z = z0 + (z1 - z0) * ease(p)
    cw, ch = W / z, H / z
    max_x, max_y = im.width - cw, im.height - ch
    cx = max_x / 2 + dx * (max_x / 2) * (ease(p) - 0.5) * 2
    cy = max_y / 2 + dy * (max_y / 2) * (ease(p) - 0.5) * 2
    cx = max(0, min(max_x, cx)); cy = max(0, min(max_y, cy))
    return im.crop((int(cx), int(cy), int(cx + cw), int(cy + ch))).resize((W, H), Image.LANCZOS)


def scrim(top, peak_a, peak_b, bottom, alpha):
    m = Image.new("L", (1, H), 0)
    px = m.load()
    for y in range(H):
        if y <= top or y >= bottom:
            v = 0.0
        elif y < peak_a:
            v = ease((y - top) / (peak_a - top))
        elif y <= peak_b:
            v = 1.0
        else:
            v = ease((bottom - y) / (bottom - peak_b))
        px[0, y] = int(alpha * v)
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    band.putalpha(m.resize((W, H)))
    return band


def vignette_mask():
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).ellipse((-W * 0.22, -H * 0.30, W * 1.22, H * 1.30), fill=255)
    return m.filter(ImageFilter.GaussianBlur(200))


def draw_text(img, rows, y, size, alpha, spacing):
    """Teal with a hard black drop shadow — survives any background brightness."""
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for row in rows:
        d.text((W / 2, y + 3), row, font=font(size), fill=(0, 0, 0, alpha), anchor="mm")
        d.text((W / 2, y), row, font=font(size), fill=TEAL + (alpha,), anchor="mm")
        y += spacing
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")


def wrap(text, size, maxw):
    d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    if d.textlength(text, font=font(size)) <= maxw:
        return [text]
    words, rows, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font(size)) <= maxw or not cur:
            cur = t
        else:
            rows.append(cur); cur = w
    if cur:
        rows.append(cur)
    return rows


def main():
    shots_dir, audio, lyr_path, out = sys.argv[1:5]
    dur = float(sys.argv[5]) if len(sys.argv) > 5 else float(subprocess.check_output(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", audio]).strip())

    shots = sorted([f for f in os.listdir(shots_dir) if f.startswith("shot") and f.endswith(".png")],
                   key=lambda s: int("".join(c for c in s if c.isdigit())))
    if not shots:
        sys.exit("no shot*.png found")
    title = os.path.basename(out).rsplit(".", 1)[0].replace("-wide", "").replace("-", " ").upper()

    imgs = [prep(os.path.join(shots_dir, s)) for s in shots]
    n = len(imgs)
    per = dur / n
    print(f"{n} shots over {dur:.1f}s -> {per:.1f}s per shot", flush=True)

    lines = json.load(open(lyr_path)) if os.path.exists(lyr_path) else []
    vig = vignette_mask()
    lyric_scrim = scrim(660, 780, 980, 1080, 200)
    black = Image.new("RGB", (W, H), (0, 0, 0))
    tmp = tempfile.mkdtemp()
    total = int(dur * FPS)

    for i in range(total):
        t = i / FPS
        idx = min(n - 1, int(t / per))
        p = (t - idx * per) / per
        img = frame_from(imgs[idx], p, MOVES[idx % len(MOVES)])

        into_next = (idx + 1) * per - t
        if idx < n - 1 and into_next < DISSOLVE:
            a = 1 - (into_next / DISSOLVE)
            nxt = frame_from(imgs[idx + 1], (DISSOLVE - into_next) / per, MOVES[(idx + 1) % len(MOVES)])
            img = Image.blend(img, nxt, ease(a))

        # No fade from black at the open — same retention reasoning as the Shorts.
        if t > dur - 1.5:
            img = Image.blend(black, img, ease(max(0.0, (dur - t) / 1.5)))

        img = Image.composite(img, Image.blend(img, black, 0.32), vig)

        # Watermark, bottom-left. No platform UI to dodge in 16:9, so it sits out
        # of the way rather than in the middle of frame.
        d = ImageDraw.Draw(img)
        for off, col in ((2, (0, 0, 0)), (0, (150, 170, 165))):
            d.text((56, H - 46 + off), "PHILOSOPHICAL KING", font=font(26), fill=col, anchor="lm")

        # Lyrics stop when the end card begins. Both live in the lower half, and a
        # half-faded lyric under the link reads as a mistake. (Same fix as
        # video_assemble.py - it was made there first and not ported here.)
        cur = None if t > dur - ENDCARD else next(
            (l for l in lines if l["s"] <= t <= l["e"]), None)
        if cur and cur.get("text"):
            fade = max(0.0, min(1.0, (t - cur["s"]) / 0.35, (cur["e"] - t) / 0.35 + 0.4))
            if fade > 0:
                sc = lyric_scrim.copy()
                sc.putalpha(sc.getchannel("A").point(lambda v: int(v * fade)))
                img = Image.alpha_composite(img.convert("RGBA"), sc).convert("RGB")
                rows = wrap(cur["text"], 62, 1280)
                img = draw_text(img, rows, 880 - (len(rows) - 1) * 38, 62,
                                int(255 * fade), 76)

        # End card over the final shot: the link lives here as well as the
        # description, because long-form viewers reach the end on screen.
        left = dur - t
        if left < ENDCARD:
            a = min(1.0, (ENDCARD - left) / 1.0, left / 1.0 + 0.25)
            if a > 0:
                img = Image.alpha_composite(
                    img.convert("RGBA"),
                    Image.new("RGBA", (W, H), (0, 0, 0, int(150 * a)))).convert("RGB")
                img = draw_text(img, [title], 470, 76, int(255 * a), 0)
                img = draw_text(img, [LINK], 570, 40, int(220 * a), 0)

        img.save(f"{tmp}/{i:05d}.jpg", quality=93)
        if i % (FPS * 30) == 0:
            print(f"  {t:6.1f}s / {dur:.1f}s", flush=True)

    subprocess.check_call([
        "ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", f"{tmp}/%05d.jpg",
        "-i", audio,
        "-vf", "noise=alls=3:allf=t+u,eq=contrast=1.05:saturation=1.03",
        "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k", "-shortest", "-t", f"{dur:.2f}", out])
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"long-form rendered: {out} ({dur:.1f}s, {n} shots, {W}x{H})")


if __name__ == "__main__":
    main()
