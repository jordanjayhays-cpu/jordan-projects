#!/usr/bin/env python3
"""
PK mini-movie renderer: turns a shot list of stills into a cinematic vertical film.

Per shot: slow camera move (push/pan) across an over-scanned still, cross-dissolved
into the next shot. Lyrics ride in the PK safe zone, watermark on top, film grain and
vignette unify the frames. Audio is the track itself.

Usage: movie_render.py <shots_dir> <audio.wav> <lyrics.json> <out.mp4> [seconds]
  shots_dir must contain shot1.png, shot2.png, ... in order.
"""
import json, math, os, subprocess, sys, tempfile, shutil, random

from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
TEAL = (200, 224, 216)
GREY = (122, 126, 135)
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
DISSOLVE = 0.45         # seconds of cross-fade between shots (short, so 3s shots hold)
OVERSCAN = 1.32         # how much bigger than frame the still is, to allow movement

def font(sz):
    return ImageFont.truetype(SERIF, sz)

def ease(t):
    return t * t * (3 - 2 * t)

def prep(path):
    """Upscale a still to an over-scanned canvas that fills the frame with room to move."""
    im = Image.open(path).convert("RGB")
    target_h = int(H * OVERSCAN)
    target_w = int(W * OVERSCAN)
    scale = max(target_w / im.width, target_h / im.height)
    im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    return im

# camera moves, one per shot index (cycles): (zoom_start, zoom_end, x_dir, y_dir)
# Sequenced so no two neighbouring shots share a gesture — at 3s a repeat reads as a stutter.
MOVES = [
    (1.00, 1.12,  0.00,  0.00),   # 1  drawn in
    (1.02, 1.14,  0.00, -0.20),   # 2  push toward the light
    (1.12, 1.00,  0.00,  0.00),   # 3  pull back, open up
    (1.10, 1.00,  0.15,  0.00),   # 4  pull back to reveal the wall
    (1.00, 1.11, -0.20,  0.22),   # 5  push in, settle down
    (1.06, 1.06, -0.45,  0.00),   # 6  lateral drift left
    (1.00, 1.09,  0.00,  0.12),   # 7  push, held wide enough to read
    (1.10, 1.00,  0.00, -0.35),   # 8  pull back, rise
    (1.02, 1.08,  0.10, -0.05),   # 9  slow creep, keeps the figure framed
    (1.14, 1.00,  0.00,  0.00),   # 10 pull back, settle
]

def frame_from(im, p, move):
    """Crop a moving 1080x1920 window out of the over-scanned still. p in 0..1."""
    z0, z1, dx, dy = move
    z = z0 + (z1 - z0) * ease(p)
    cw, ch = W / z, H / z
    max_x = im.width - cw
    max_y = im.height - ch
    cx = max_x / 2 + dx * (max_x / 2) * (ease(p) - 0.5) * 2
    cy = max_y / 2 + dy * (max_y / 2) * (ease(p) - 0.5) * 2
    cx = max(0, min(max_x, cx)); cy = max(0, min(max_y, cy))
    crop = im.crop((int(cx), int(cy), int(cx + cw), int(cy + ch)))
    return crop.resize((W, H), Image.LANCZOS)

def scrim(top, peak_a, peak_b, bottom, alpha):
    """A soft dark band that fades in/out vertically — keeps text legible over bright shots."""
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
    m = m.resize((W, H))
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    band.putalpha(m)
    return band

def vignette_mask():
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    d.ellipse((-W * 0.35, -H * 0.18, W * 1.35, H * 1.18), fill=255)
    return m.filter(ImageFilter.GaussianBlur(180))

def main():
    shots_dir, audio, lyr_path, out = sys.argv[1:5]
    dur = float(sys.argv[5]) if len(sys.argv) > 5 else None
    if dur is None:
        dur = float(subprocess.check_output(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
             "-of", "csv=p=0", audio]).strip())

    shots = sorted([f for f in os.listdir(shots_dir) if f.startswith("shot") and f.endswith(".png")],
                   key=lambda s: int("".join(c for c in s if c.isdigit())))
    if not shots:
        sys.exit("no shot*.png found")
    imgs = [prep(os.path.join(shots_dir, s)) for s in shots]
    n = len(imgs)
    per = dur / n

    lines = json.load(open(lyr_path)) if os.path.exists(lyr_path) else []
    vig = vignette_mask()
    top_scrim = scrim(60, 150, 250, 400, 135)          # holds the watermark on bright shots
    lyric_scrim = scrim(1100, 1290, 1510, 1760, 205)   # holds the lyric line
    black = Image.new("RGB", (W, H), (0, 0, 0))
    total = int(dur * FPS)
    tmp = tempfile.mkdtemp()
    random.seed(7)

    for i in range(total):
        t = i / FPS
        idx = min(n - 1, int(t / per))
        p = (t - idx * per) / per
        img = frame_from(imgs[idx], p, MOVES[idx % len(MOVES)])

        # cross-dissolve into the next shot
        into_next = (idx + 1) * per - t
        if idx < n - 1 and into_next < DISSOLVE:
            a = 1 - (into_next / DISSOLVE)
            nxt = frame_from(imgs[idx + 1], (DISSOLVE - into_next) / per, MOVES[(idx + 1) % len(MOVES)])
            img = Image.blend(img, nxt, ease(a))

        # open from / close to black
        if t < 1.2:
            img = Image.blend(black, img, ease(t / 1.2))
        elif t > dur - 1.2:
            img = Image.blend(black, img, ease(max(0.0, (dur - t) / 1.2)))

        # vignette (light — the stills already carry their own falloff)
        img = Image.composite(img, Image.blend(img, black, 0.35), vig)

        img = Image.alpha_composite(img.convert("RGBA"), top_scrim).convert("RGB")

        d = ImageDraw.Draw(img)
        # watermark, below the platform's top UI band
        d.text((W / 2, 200 + 3), "PHILOSOPHICAL KING", font=font(38), fill=(0, 0, 0), anchor="mm")
        d.text((W / 2, 200), "PHILOSOPHICAL KING", font=font(38), fill=TEAL, anchor="mm")

        # lyric line, safe zone
        cur = next((l for l in lines if l["s"] <= t <= l["e"]), None)
        if cur and cur.get("text"):
            fade = max(0.0, min(1.0, (t - cur["s"]) / 0.3, (cur["e"] - t) / 0.3 + 0.4))
            if fade > 0:
                sc = lyric_scrim.copy()
                sc.putalpha(sc.getchannel("A").point(lambda v: int(v * fade)))
                img = Image.alpha_composite(img.convert("RGBA"), sc).convert("RGB")
                ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                od = ImageDraw.Draw(ov)
                a = int(255 * fade)
                size, MAXW, Y = 52, 880, 1380
                while size > 38 and od.textlength(cur["text"], font=font(size)) > MAXW:
                    size -= 2
                rows = [cur["text"]]
                if od.textlength(cur["text"], font=font(size)) > MAXW:
                    ws = cur["text"].split()
                    cut = max(1, len(ws) // 2)
                    rows = [" ".join(ws[:cut]), " ".join(ws[cut:])]
                y = Y - (len(rows) - 1) * 32
                for row in rows:
                    od.text((W / 2, y + 3), row, font=font(size), fill=(0, 0, 0, a), anchor="mm")
                    od.text((W / 2, y), row, font=font(size), fill=TEAL + (a,), anchor="mm")
                    y += 64
                img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")

        img.save(f"{tmp}/{i:05d}.jpg", quality=92)

    subprocess.check_call([
        "ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", f"{tmp}/%05d.jpg",
        "-i", audio,
        # film grain + slight contrast for cohesion across generated stills
        "-vf", "noise=alls=4:allf=t+u,eq=contrast=1.06:saturation=1.04",
        "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-shortest", "-t", f"{dur:.2f}", out])
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"mini movie rendered: {out} ({dur:.1f}s, {n} shots)")

if __name__ == "__main__":
    main()
