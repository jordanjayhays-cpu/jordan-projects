#!/usr/bin/env python3
"""
PK kinetic teaser renderer — headless implementation of the kinetic template spec
(Omelette project "Music teaser animation template").

Beats:
  1. Cold open: camera pushed deep into the cover art, dark; the HOOK lands
     word by word, final word gold #e9c46a; closes on the 150x2 gold rule.
  2. One continuous pull-back settling into the locked 1080x1920 framing.
  3. Body: locked framing (art 1000x1000 @ y=250 with drift, watermark y=110,
     waveform 900x120 @ (90,1380)), lyrics one line at a time @ y=1560.
  4. End card: cover, track name, gold rule, link line, crown, wordmark.

Locked constants respected: drift x=40sin(2pi n/1500), y=40cos(2pi n/1900),
hard 0/3px black shadows, zero radius, canonical hexes, serif stack.

Usage: kinetic_render.py <slug> "<Track Title>" "<hook words>" "<link line>" \
                         <art.jpg> <preview.wav> <lyrics.json> <out.mp4>
"""
import json, math, os, shutil, subprocess, sys, tempfile

from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
FPS = 30
GOLD = (233, 196, 106)      # e9c46a
TEAL = (200, 224, 216)      # c8e0d8
IVORY = (242, 237, 227)     # f2ede3
GREY = (122, 126, 135)      # 7a7e87
BLACK = (10, 11, 14)        # 0e0f13-family
WAVE_GOLD = "0xb09a4a"

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
# DejaVu has no CJK coverage at all — Chinese, Japanese and Korean text renders
# as empty boxes. Noto Serif CJK keeps the serif look of the template rather
# than dropping to a sans fallback. The .ttc holds SC/TC/JP/HK/KR; index 2 is
# Simplified Chinese, which also covers the Han characters the others need.
CJK = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc"
CJK_INDEX = 2


def has_cjk(text):
    return any("぀" <= c <= "ヿ" or "㐀" <= c <= "鿿"
               or "가" <= c <= "힯" or "＀" <= c <= "￯"
               for c in str(text))


def font(size, text=""):
    if text and has_cjk(text) and os.path.exists(CJK):
        return ImageFont.truetype(CJK, size, index=CJK_INDEX)
    return ImageFont.truetype(SERIF, size)

def ease(t):  # smooth in-out
    return t * t * (3 - 2 * t)

def draw_text_shadow(d, xy, text, f, fill, anchor="mm"):
    x, y = xy
    d.text((x, y + 3), text, font=f, fill=(0, 0, 0), anchor=anchor)
    d.text((x, y), text, font=f, fill=fill, anchor=anchor)

def fit_art(art, size):
    a = art.copy()
    a.thumbnail((size, size), Image.LANCZOS)
    return a

def art_camera_frame(art_big, zoom, cx, cy):
    """Crop art at zoom level centered (cx,cy in 0..1), return full-canvas image."""
    aw, ah = art_big.size
    crop_w = int(aw / zoom)
    crop_h = int(crop_w * H / W)
    if crop_h > ah:
        crop_h = ah
        crop_w = int(crop_h * W / H)
    x0 = int(cx * aw - crop_w / 2); y0 = int(cy * ah - crop_h / 2)
    x0 = max(0, min(aw - crop_w, x0)); y0 = max(0, min(ah - crop_h, y0))
    return art_big.crop((x0, y0, x0 + crop_w, y0 + crop_h)).resize((W, H), Image.LANCZOS)

def locked_frame(art1000, n, dark=0, title=None):
    """The locked framing with drift; n = body frame index.

    The track title sits under the wordmark for the WHOLE body, not only on the
    end card. Most people never reach the last four seconds of a 30s teaser, so
    a title that only appears there is a title most viewers never see.
    """
    img = Image.new("RGB", (W, H), BLACK)
    dx = 40 * math.sin(2 * math.pi * n / 1500)
    dy = 40 * math.cos(2 * math.pi * n / 1900)
    img.paste(art1000, (int((W - 1000) / 2 + dx), int(270 + 40 + dy)))
    d = ImageDraw.Draw(img)
    draw_text_shadow(d, (W / 2, 186), "PHILOSOPHICAL KING", font(40), TEAL)
    if title:
        # Gold, to separate it from the teal wordmark, and shrunk to fit rather
        # than truncated — several titles run past 940px at the base size.
        ts = 36
        while ts > 22 and d.textlength(title, font=font(ts, title)) > 940:
            ts -= 2
        draw_text_shadow(d, (W / 2, 240), title, font(ts, title), GOLD)
    if dark:
        img = Image.blend(img, Image.new("RGB", (W, H), (0, 0, 0)), dark)
    return img

def main():
    slug, title, hook, cta, art_path, wav, lyr_path, out = sys.argv[1:9]
    lines = json.load(open(lyr_path))
    dur = float(subprocess.check_output(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", wav]).strip())

    art_src = Image.open(art_path).convert("RGB")
    if min(art_src.size) < 2000:
        art_src = art_src.resize((3000, 3000), Image.LANCZOS)
    art1000 = fit_art(art_src, 1000)

    hook_words = hook.split()
    # timeline (seconds) — proportions from the Bayanihan reference cut, scaled to preview
    t_hook_end = 1.68 + 1.52           # words land + rule beat
    t_reveal = t_hook_end + 2.0        # pull-back settles (Reveal cue)
    t_end_card = dur - 4.2             # end card length from reference
    total_frames = int(dur * FPS)

    tmp = tempfile.mkdtemp()
    body_n = 0
    for i in range(total_frames):
        t = i / FPS
        if t < t_hook_end:
            # 1. cold open — deep in the art, dark, words landing
            zoom = 2.6 - 0.15 * (t / t_hook_end)
            img = art_camera_frame(art_src, zoom, 0.5, 0.42)
            img = Image.blend(img, Image.new("RGB", (W, H), (0, 0, 0)), 0.72)
            d = ImageDraw.Draw(img)
            words_on = max(1, min(len(hook_words), 1 + int(t / (1.68 / max(1, len(hook_words))))))
            f = font(64, hook)
            # layout words centered as wrapped block
            shown = hook_words[:words_on]
            linebuf, rows = [], []
            for w_ in shown:
                trial = " ".join(linebuf + [w_])
                if d.textlength(trial, font=f) > 880 and linebuf:
                    rows.append(linebuf); linebuf = [w_]
                else:
                    linebuf.append(w_)
            rows.append(linebuf)
            y0 = H / 2 - (len(rows) - 1) * 45
            wi = 0
            for r, row in enumerate(rows):
                rowtext = " ".join(row)
                total_wd = d.textlength(rowtext, font=f)
                x = (W - total_wd) / 2
                for w_ in row:
                    wi += 1
                    color = GOLD if (wi == len(hook_words) and words_on == len(hook_words)) else IVORY
                    d.text((x, y0 + r * 90 + 3), w_, font=f, fill=(0, 0, 0), anchor="lm")
                    d.text((x, y0 + r * 90), w_, font=f, fill=color, anchor="lm")
                    x += d.textlength(w_ + " ", font=f)
            if t > 1.68:  # rule beat
                a = ease(min(1, (t - 1.68) / 0.5))
                lw = int(150 * a)
                d.rectangle([(W - lw) / 2, H / 2 + len(rows) * 60 + 40,
                             (W + lw) / 2, H / 2 + len(rows) * 60 + 42], fill=GOLD)
        elif t < t_reveal:
            # 2. continuous pull-back into locked framing
            p = ease((t - t_hook_end) / (t_reveal - t_hook_end))
            zoom = 2.45 - (2.45 - 1.0) * p
            deep = art_camera_frame(art_src, max(1.0, zoom), 0.5, 0.42)
            deep = Image.blend(deep, Image.new("RGB", (W, H), (0, 0, 0)), 0.72 * (1 - p))
            locked = locked_frame(art1000, 0, title=title)
            img = Image.blend(deep, locked, p)
        elif t < t_end_card:
            # 3. body — locked framing + one lyric line at a time, faded in/out
            img = locked_frame(art1000, body_n, title=title); body_n += 1
            cur = next((ln for ln in lines if ln["s"] <= t <= ln["e"]), None)
            if cur and cur["text"]:
                fade = min(1.0, (t - max(cur["s"], t_reveal)) / 0.25, (cur["e"] - t) / 0.25 + 0.4)
                fade = max(0.0, fade)
                if fade > 0:
                    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                    od = ImageDraw.Draw(ov)
                    a = int(255 * fade)
                    # fit: shrink to width, wrap to 2 lines if needed; sits under the art,
                    # above every platform's bottom UI band (safe zone ends ~1440)
                    LYRIC_Y, MAXW = 1350, 860

                    def wrap(text, base, floor):
                        """Largest size that fits, wrapped to at most two rows."""
                        sz = base
                        while sz > floor and od.textlength(text, font=font(sz, text)) > MAXW:
                            sz -= 2
                        if od.textlength(text, font=font(sz, text)) <= MAXW:
                            return sz, [text]
                        # CJK has no spaces to break on, so split on character count;
                        # English splits at the word boundary that balances the rows.
                        if has_cjk(text) and " " not in text.strip():
                            mid = len(text) // 2
                            return sz, [text[:mid], text[mid:]]
                        ws_ = text.split()
                        if len(ws_) < 2:
                            return sz, [text]
                        best, bestdiff = 1, 1e9
                        for cpt in range(1, len(ws_)):
                            wd = max(od.textlength(" ".join(ws_[:cpt]), font=font(sz, text)),
                                     od.textlength(" ".join(ws_[cpt:]), font=font(sz, text)))
                            if wd < bestdiff:
                                best, bestdiff = cpt, wd
                        return sz, [" ".join(ws_[:best]), " ".join(ws_[best:])]

                    def draw_rows(rows, sz, top, colour, gap):
                        y2 = top
                        for row_ in rows:
                            od.text((W / 2, y2 + 3), row_, font=font(sz, row_),
                                    fill=(0, 0, 0, a), anchor="mm")
                            od.text((W / 2, y2), row_, font=font(sz, row_),
                                    fill=colour + (a,), anchor="mm")
                            y2 += gap
                        return y2

                    # Bilingual: the primary language reads full size in teal, the
                    # secondary sits under it smaller and dimmed. A translation
                    # competing at equal weight makes both harder to read, and the
                    # pair has to clear the safe zone, so the second line is the one
                    # that gives up size.
                    size, rows_ = wrap(cur["text"], 52, 38)
                    sub = (cur.get("en") or "").strip()
                    if sub:
                        sub_size, sub_rows = wrap(sub, 34, 26)
                        block = (len(rows_) - 1) * 58 + 16 + (len(sub_rows) - 1) * 38
                        y_ = LYRIC_Y - block / 2
                        y_ = draw_rows(rows_, size, y_, TEAL, 58)
                        draw_rows(sub_rows, sub_size, y_ - 58 + 62, GREY, 38)
                    else:
                        y_ = LYRIC_Y - (len(rows_) - 1) * 30
                        draw_rows(rows_, size, y_, TEAL, 60)
                    img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
        else:
            # 4. end card
            p = ease(min(1, (t - t_end_card) / 0.6))
            img = Image.new("RGB", (W, H), BLACK)
            small = fit_art(art_src, 560)
            img.paste(small, (int((W - 560) / 2), 330))
            d = ImageDraw.Draw(img)
            tf_ = 56
            while tf_ > 40 and d.textlength(title, font=font(tf_, title)) > 940:
                tf_ -= 2
            draw_text_shadow(d, (W / 2, 1000), title, font(tf_, title), IVORY)
            d.rectangle([(W - 150) / 2, 1070, (W + 150) / 2, 1072], fill=GOLD)
            # An empty cta means no link line at all. The Chinese cuts use this:
            # nobody types a URL off a video, and the caption already carries a
            # tappable one. Note font(34, cta_disp) rather than font(34) — the
            # Latin font has no CJK glyphs, so a Chinese line here rendered as a
            # row of empty boxes until 2026-08-31.
            cta_f = font(34, cta)
            cta_disp = (cta or "").replace("https://", "").strip()
            if not cta_disp:
                pass
            elif d.textlength(cta_disp, font=cta_f) > 980 and "/" in cta_disp:
                parts = cta_disp.split("/")
                l1, l2 = parts[0], "/" + "/".join(parts[1:])
                for cut in range(1, len(parts)):
                    a = "/".join(parts[:cut]); b = "/" + "/".join(parts[cut:])
                    if d.textlength(a, font=cta_f) <= 980 and d.textlength(b, font=cta_f) <= 980:
                        l1, l2 = a, b
                draw_text_shadow(d, (W / 2, 1132), l1, cta_f, TEAL)
                draw_text_shadow(d, (W / 2, 1182), l2, cta_f, TEAL)
            else:
                draw_text_shadow(d, (W / 2, 1155), cta_disp, cta_f, TEAL)
            # PK_END_CARD=minimal drops the crown. The Chinese cuts use it: the
            # emoji reads as decoration rather than as a mark, and the wordmark
            # underneath already says who this is. Env var rather than another
            # positional arg, because backfill_titles, fix_hook and the 15s
            # cutter all call this with the existing signature.
            if os.environ.get("PK_END_CARD") != "minimal":
                try:
                    ef = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 109)
                    d.text((W / 2, 1280), "👑", font=ef, anchor="mm", embedded_color=True)
                except Exception:
                    d.rectangle([(W - 60) / 2, 1260, (W + 60) / 2, 1300], fill=GOLD)
            # Without the crown the wordmark has to move up, or the card is a
            # gold rule and then 300px of nothing.
            mark_y = 1180 if os.environ.get("PK_END_CARD") == "minimal" else 1390
            draw_text_shadow(d, (W / 2, mark_y), "P H I L O S O P H I C A L   K I N G", font(32), GREY)
            if p < 1:
                img = Image.blend(locked_frame(art1000, body_n, title=title), img, p)
        img.save(f"{tmp}/{i:05d}.jpg", quality=90)

    # assemble + waveform overlay during body + audio mux
    body_start, body_end = t_reveal, t_end_card
    subprocess.check_call([
        "ffmpeg", "-v", "error", "-y",
        "-framerate", str(FPS), "-i", f"{tmp}/%05d.jpg", "-i", wav,
        "-filter_complex",
        f"[1:a]showwaves=s=900x120:mode=cline:colors={WAVE_GOLD}[wv];"
        f"[0:v][wv]overlay=90:1380:enable='between(t,{body_start:.2f},{body_end:.2f})'[out]",
        "-map", "[out]", "-map", "1:a",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-shortest", out])
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"kinetic render complete: {out} ({dur:.1f}s)")

if __name__ == "__main__":
    main()
