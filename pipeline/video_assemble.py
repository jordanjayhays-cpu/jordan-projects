#!/usr/bin/env python3
"""
Assemble generated video clips into a full-length 16:9 PK music video.

The stills renderer (movie_render_wide.py) moves a camera over static images.
This takes real motion clips - Veo 3 output, 8 seconds each at 1280x720 - and
cuts them into a finished film: upscaled, cross-dissolved, carrying the PK
lyric treatment, watermark and end card, over the real song.

Veo clips arrive with their own generated audio. It is always discarded; the
track is the audio.

Two passes, on purpose:
  1. ffmpeg builds the base cut (scale, xfade). Fast, and ffmpeg is far better
     at this than compositing frames in Python.
  2. frames stream through PIL for the text, piped both ways. Nothing is
     written to disk as an image sequence - a four-minute 1080p sequence is
     ~700MB of PNGs and this container has a fixed, small disk allowance.

Usage:
  video_assemble.py <clips_dir> <audio> <lyrics.json> <out.mp4>
  video_assemble.py --plan <seconds>     how many clips a song of that length needs

clips_dir must contain clip01.mp4, clip02.mp4, ... in order.
"""
import json, math, os, subprocess, sys

from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1920, 1080, 30
TEAL = (200, 224, 216)
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
XFADE = 0.8             # dissolve between clips
LINK = "https://hyperfollow.com/PhilosophicalKing"
ENDCARD = 7.0
CLIP_LEN = 8.0          # what Veo 3 returns


def font(sz):
    return ImageFont.truetype(SERIF, sz)


def probe(path, stream="v"):
    out = subprocess.check_output(
        ["ffprobe", "-v", "quiet", "-select_streams", stream,
         "-show_entries", "format=duration", "-of", "csv=p=0", path]).strip()
    return float(out)


def clips_needed(seconds, clip_len=CLIP_LEN, xfade=XFADE):
    """
    Each dissolve eats `xfade` seconds of total runtime, so n clips yield
    n*clip_len - (n-1)*xfade. Solve for n and round up.
    """
    return math.ceil((seconds - xfade) / (clip_len - xfade))


def build_base(clips, out):
    """Scale every clip to 1080p, drop its audio, and xfade the chain together."""
    args, filt = [], []
    for c in clips:
        args += ["-i", c]
    for i, c in enumerate(clips):
        # Veo returns 720p; pad rather than crop so nothing is lost if a clip
        # comes back at an unexpected aspect.
        filt.append(f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=decrease,"
                    f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,fps={FPS},setsar=1[v{i}]")
    if len(clips) == 1:
        filt.append("[v0]copy[outv]")
    else:
        durs = [probe(c) for c in clips]
        prev, offset = "v0", durs[0] - XFADE
        for i in range(1, len(clips)):
            label = "outv" if i == len(clips) - 1 else f"x{i}"
            filt.append(f"[{prev}][v{i}]xfade=transition=fade:duration={XFADE}:"
                        f"offset={offset:.3f}[{label}]")
            prev = label
            offset += durs[i] - XFADE
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", *args,
                           "-filter_complex", ";".join(filt), "-map", "[outv]",
                           "-an", "-c:v", "libx264", "-preset", "veryfast",
                           "-crf", "16", "-pix_fmt", "yuv420p", out])


def wrap(text, size, maxw):
    d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    if d.textlength(text, font=font(size)) <= maxw:
        return [text]
    rows, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font(size)) <= maxw or not cur:
            cur = t
        else:
            rows.append(cur); cur = w
    if cur:
        rows.append(cur)
    return rows


def scrim():
    m = Image.new("L", (1, H), 0)
    px = m.load()
    top, a, b, bot = 660, 780, 980, 1080
    for y in range(H):
        if y <= top:
            v = 0.0
        elif y < a:
            v = (y - top) / (a - top)
        elif y <= b:
            v = 1.0
        else:
            v = max(0.0, (bot - y) / (bot - b))
        px[0, y] = int(200 * v * v * (3 - 2 * v))
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    band.putalpha(m.resize((W, H)))
    return band


def draw_rows(img, rows, y, size, alpha, spacing):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for row in rows:
        d.text((W / 2, y + 3), row, font=font(size), fill=(0, 0, 0, alpha), anchor="mm")
        d.text((W / 2, y), row, font=font(size), fill=TEAL + (alpha,), anchor="mm")
        y += spacing
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")


def overlay_pass(base, audio, lyrics, out, dur, title):
    """Stream frames through PIL, adding lyrics/watermark/end card, then mux the song."""
    lines = json.load(open(lyrics)) if os.path.exists(lyrics) else []
    band = scrim()
    black = Image.new("RGB", (W, H), (0, 0, 0))
    nbytes = W * H * 3
    total = int(dur * FPS)

    src = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", base, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        stdout=subprocess.PIPE)
    dst = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", audio,
         "-vf", "noise=alls=3:allf=t+u,eq=contrast=1.05:saturation=1.03",
         "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "256k", "-shortest", "-t", f"{dur:.2f}", out],
        stdin=subprocess.PIPE)

    for i in range(total):
        raw = src.stdout.read(nbytes)
        if len(raw) < nbytes:
            break
        t = i / FPS
        img = Image.frombytes("RGB", (W, H), raw)

        if t > dur - 1.5:
            img = Image.blend(black, img, max(0.0, (dur - t) / 1.5))

        d = ImageDraw.Draw(img)
        for off, col in ((2, (0, 0, 0)), (0, (150, 170, 165))):
            d.text((56, H - 46 + off), "PHILOSOPHICAL KING", font=font(26),
                   fill=col, anchor="lm")

        # Lyrics stop when the end card begins. Both live in the lower half, and
        # a half-faded lyric under the link reads as a mistake.
        cur = None if t > dur - ENDCARD else next(
            (l for l in lines if l["s"] <= t <= l["e"]), None)
        if cur and cur.get("text"):
            fade = max(0.0, min(1.0, (t - cur["s"]) / 0.35, (cur["e"] - t) / 0.35 + 0.4))
            if fade > 0:
                sc = band.copy()
                sc.putalpha(sc.getchannel("A").point(lambda v: int(v * fade)))
                img = Image.alpha_composite(img.convert("RGBA"), sc).convert("RGB")
                rows = wrap(cur["text"], 62, 1280)
                img = draw_rows(img, rows, 880 - (len(rows) - 1) * 38, 62,
                                int(255 * fade), 76)

        left = dur - t
        if left < ENDCARD:
            a = min(1.0, (ENDCARD - left) / 1.0, left / 1.0 + 0.25)
            if a > 0:
                img = Image.alpha_composite(
                    img.convert("RGBA"),
                    Image.new("RGBA", (W, H), (0, 0, 0, int(150 * a)))).convert("RGB")
                img = draw_rows(img, [title], 470, 76, int(255 * a), 0)
                img = draw_rows(img, [LINK], 570, 40, int(220 * a), 0)

        dst.stdin.write(img.tobytes())
        if i % (FPS * 30) == 0:
            print(f"  {t:6.1f}s / {dur:.1f}s", flush=True)

    dst.stdin.close(); dst.wait(); src.wait()


def main():
    if sys.argv[1] == "--plan":
        secs = float(sys.argv[2])
        n = clips_needed(secs)
        print(f"{secs:.0f}s song -> {n} Veo clips "
              f"({n * CLIP_LEN:.0f}s raw, {n * CLIP_LEN - (n - 1) * XFADE:.0f}s after dissolves)")
        print(f"generation time ~{n * 82 / 60:.0f} min at 82s per clip")
        return 0

    clips_dir, audio, lyrics, out = sys.argv[1:5]
    clips = sorted(os.path.join(clips_dir, f) for f in os.listdir(clips_dir)
                   if f.startswith("clip") and f.endswith(".mp4"))
    if not clips:
        sys.exit("no clip*.mp4 found")
    dur = probe(audio)
    have = sum(probe(c) for c in clips) - (len(clips) - 1) * XFADE
    print(f"{len(clips)} clips -> {have:.1f}s of footage for a {dur:.1f}s track")
    if have < dur - 0.5:
        sys.exit(f"SHORT BY {dur - have:.1f}s — need {clips_needed(dur)} clips total, "
                 f"have {len(clips)}. Generate more rather than looping: a visible "
                 f"repeat reads worse than anything else in the cut.")

    base = os.path.join(os.path.dirname(out) or ".", ".base_cut.mp4")
    print("building base cut...", flush=True)
    build_base(clips, base)
    title = os.path.basename(out).rsplit(".", 1)[0].replace("-", " ").upper()
    print("overlay pass...", flush=True)
    overlay_pass(base, audio, lyrics, out, dur, title)
    os.remove(base)
    print(f"done: {out} ({dur:.1f}s, {len(clips)} clips, {W}x{H})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
