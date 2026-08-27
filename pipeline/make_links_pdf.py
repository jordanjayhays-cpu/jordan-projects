#!/usr/bin/env python3
"""One-page Philosophical King link sheet, for sharing.

Title, then link. Nothing else — no section headings, no explanatory notes.

Every URL is written as a real PDF link annotation, so it is tappable in any
normal PDF viewer. Inline previews in chat apps rasterise the page and flatten
annotations, which makes the links look dead; that is the viewer, not the file.
"""
import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

OUT = "/home/user/jordan-projects/music-assets/brand/philosophical-king-links.pdf"
W, H = A4

INK = (0.08, 0.08, 0.10)
MUTED = (0.42, 0.42, 0.46)
GOLD = (0.62, 0.48, 0.16)
LINK = (0.13, 0.31, 0.62)
RULE = (0.84, 0.84, 0.86)

# DejaVu ships with most Linux images and has glyph coverage the built-in Type 1
# fonts lack — the em dash in "YouTube — full songs" among them.
FONTS = {
    "reg": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "bold": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
}
NAMES = {}
for key, path in FONTS.items():
    if os.path.exists(path):
        pdfmetrics.registerFont(TTFont(f"PK-{key}", path))
        NAMES[key] = f"PK-{key}"
NAMES.setdefault("reg", "Times-Roman")
NAMES.setdefault("bold", "Times-Bold")
NAMES.setdefault("sans", "Helvetica")

ROWS = [
    ("All the music, every platform", "https://hyperfollow.com/PhilosophicalKing"),
    ("Apple Music", "https://music.apple.com/us/artist/philosophical-king/1791470584"),
    ("YouTube — full songs", "https://www.youtube.com/channel/UCST1Tzuraa0CSR4o3RkVIMw"),
    ("YouTube — videos", "https://www.youtube.com/@philosophicalkingmusic"),
    ("Instagram", "https://www.instagram.com/philosophicalkingmusicofficial/"),
    ("TikTok", "https://www.tiktok.com/@philosophicalkingmusic"),
    ("Reddit", "https://www.reddit.com/user/PhilosophicalKingM"),
    ("Substack", "https://philosophicalkingmusic.substack.com"),
]


def main():
    c = canvas.Canvas(OUT, pagesize=A4)
    c.setTitle("Philosophical King — links")
    c.setAuthor("Philosophical King")
    c.setSubject("Where to find the music")

    left = 24 * mm
    right = W - 24 * mm
    y = H - 34 * mm

    c.setFillColorRGB(*INK)
    c.setFont(NAMES["bold"], 28)
    c.drawString(left, y, "Philosophical King")
    y -= 9.5 * mm

    c.setFillColorRGB(*GOLD)
    c.setFont(NAMES["sans"], 11)
    c.drawString(left, y, "Philosophy and hip hop  ·  251 tracks")
    y -= 7 * mm

    c.setStrokeColorRGB(*RULE)
    c.setLineWidth(0.8)
    c.line(left, y, right, y)

    # Eight rows spread evenly down the remaining page, so the sheet reads as one
    # deliberate block rather than a list crowded at the top.
    y -= 15 * mm
    step = (y - 34 * mm) / (len(ROWS) - 1)

    for label, url in ROWS:
        c.setFillColorRGB(*INK)
        c.setFont(NAMES["bold"], 13)
        c.drawString(left, y, label)

        ly = y - 6.2 * mm
        c.setFillColorRGB(*LINK)
        c.setFont(NAMES["sans"], 10)
        c.drawString(left, ly, url)

        width = c.stringWidth(url, NAMES["sans"], 10)
        c.setStrokeColorRGB(*LINK)
        c.setLineWidth(0.4)
        c.line(left, ly - 1.2 * mm, left + width, ly - 1.2 * mm)
        # The clickable box, sized to the drawn text with a little slack so a
        # fingertip on a phone still lands inside it.
        c.linkURL(url, (left, ly - 2.2 * mm, left + width, ly + 3.8 * mm), relative=0)

        y -= step

    c.showPage()
    c.save()
    print("wrote", OUT)


if __name__ == "__main__":
    main()
