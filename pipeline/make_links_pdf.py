#!/usr/bin/env python3
"""One-page Philosophical King link sheet, for sharing.

Everything on it was checked by loading the page on 2026-08-27, not by trusting
a status code — Instagram answered 429 (throttling this server, not a broken
link) and the handle comes from the connected account itself.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

OUT = "/home/user/jordan-projects/music-assets/brand/philosophical-king-links.pdf"
W, H = A4

INK = (0.08, 0.08, 0.10)
MUTED = (0.42, 0.42, 0.46)
GOLD = (0.62, 0.48, 0.16)
RULE = (0.84, 0.84, 0.86)

# DejaVu ships with most Linux images and has the glyph coverage the built-in
# Type 1 fonts lack.
FONTS = {
    "reg": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "bold": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "sansb": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
}
NAMES = {}
for k, path in FONTS.items():
    if os.path.exists(path):
        pdfmetrics.registerFont(TTFont(f"PK-{k}", path))
        NAMES[k] = f"PK-{k}"
NAMES.setdefault("reg", "Times-Roman")
NAMES.setdefault("bold", "Times-Bold")
NAMES.setdefault("sans", "Helvetica")
NAMES.setdefault("sansb", "Helvetica-Bold")

SECTIONS = [
    ("Start here", [
        ("All the music, every platform", "https://hyperfollow.com/PhilosophicalKing",
         "One link — Spotify, Apple Music, Amazon, everywhere else."),
    ]),
    ("Listen", [
        ("Apple Music", "https://music.apple.com/us/artist/philosophical-king/1791470584",
         "The full artist page."),
        ("YouTube — full songs", "https://www.youtube.com/channel/UCST1Tzuraa0CSR4o3RkVIMw",
         "All 257 tracks. This channel is hidden from YouTube search, so the link is the only way in."),
        ("YouTube — videos", "https://www.youtube.com/@philosophicalkingmusic",
         "Lyric videos and the daily posts."),
    ]),
    ("Follow", [
        ("Instagram", "https://www.instagram.com/philosophicalkingmusicofficial/", ""),
        ("TikTok", "https://www.tiktok.com/@philosophicalkingmusic", ""),
        ("Reddit", "https://www.reddit.com/user/PhilosophicalKingM", ""),
    ]),
    ("Read", [
        ("Substack", "https://philosophicalkingmusic.substack.com",
         "Writing on the ideas behind the songs."),
    ]),
]


def main():
    c = canvas.Canvas(OUT, pagesize=A4)
    c.setTitle("Philosophical King — links")
    c.setAuthor("Philosophical King")
    c.setSubject("Where to find the music")

    L = 24 * mm
    R = W - 24 * mm
    y = H - 32 * mm

    c.setFillColorRGB(*INK)
    c.setFont(NAMES["bold"], 27)
    c.drawString(L, y, "Philosophical King")
    y -= 9 * mm

    c.setFillColorRGB(*GOLD)
    c.setFont(NAMES["sans"], 10.5)
    c.drawString(L, y, "Philosophy and hip hop  ·  251 tracks")
    y -= 6 * mm

    c.setStrokeColorRGB(*RULE)
    c.setLineWidth(0.8)
    c.line(L, y, R, y)
    y -= 12 * mm

    for heading, rows in SECTIONS:
        c.setFillColorRGB(*MUTED)
        c.setFont(NAMES["sansb"], 8.5)
        c.drawString(L, y, heading.upper())
        y -= 7.5 * mm

        for label, url, note in rows:
            c.setFillColorRGB(*INK)
            c.setFont(NAMES["bold"], 12)
            c.drawString(L, y, label)
            y -= 5.4 * mm

            c.setFillColorRGB(0.13, 0.31, 0.62)
            c.setFont(NAMES["sans"], 9.5)
            c.drawString(L, y, url)
            tw = c.stringWidth(url, NAMES["sans"], 9.5)
            # Clickable, and underlined so it reads as a link on paper too.
            c.setStrokeColorRGB(0.13, 0.31, 0.62)
            c.setLineWidth(0.4)
            c.line(L, y - 1.1 * mm, L + tw, y - 1.1 * mm)
            c.linkURL(url, (L, y - 2 * mm, L + tw, y + 3.4 * mm), relative=0)
            y -= 5.2 * mm

            if note:
                c.setFillColorRGB(*MUTED)
                c.setFont(NAMES["reg"], 9)
                # Wrap by measured width rather than a character count.
                words, line = note.split(), ""
                for word in words:
                    trial = f"{line} {word}".strip()
                    if c.stringWidth(trial, NAMES["reg"], 9) > (R - L):
                        c.drawString(L, y, line)
                        y -= 4.4 * mm
                        line = word
                    else:
                        line = trial
                if line:
                    c.drawString(L, y, line)
                    y -= 4.4 * mm
            y -= 4 * mm
        y -= 3 * mm

    c.setStrokeColorRGB(*RULE)
    c.line(L, 24 * mm, R, 24 * mm)
    c.setFillColorRGB(*MUTED)
    c.setFont(NAMES["reg"], 8.5)
    c.drawString(L, 18 * mm, "Every link checked 27 August 2026.")

    c.showPage()
    c.save()
    print("wrote", OUT)


if __name__ == "__main__":
    main()
