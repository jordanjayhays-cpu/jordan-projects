#!/usr/bin/env python3
"""One-page Philosophical King link sheet: a title, then the bare list of URLs.

No per-link labels, no sections, no notes — Jordan asked for exactly the list as
he writes it.

Every URL is a real PDF link annotation, so it is tappable in any normal PDF
viewer. Inline previews in chat apps rasterise the page and flatten annotations,
which makes the links look dead; that is the viewer, not the file.
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
LINK = (0.13, 0.31, 0.62)

FONTS = {
    "bold": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
}
NAMES = {}
for key, path in FONTS.items():
    if os.path.exists(path):
        pdfmetrics.registerFont(TTFont(f"PK-{key}", path))
        NAMES[key] = f"PK-{key}"
NAMES.setdefault("bold", "Times-Bold")
NAMES.setdefault("sans", "Helvetica")

LINKS = [
    "https://hyperfollow.com/PhilosophicalKing",
    "https://music.apple.com/us/artist/philosophical-king/1791470584",
    "https://www.youtube.com/channel/UCST1Tzuraa0CSR4o3RkVIMw",
    "https://www.youtube.com/@philosophicalkingmusic",
    "https://www.instagram.com/philosophicalkingmusicofficial/",
    "https://www.tiktok.com/@philosophicalkingmusic",
    "https://www.reddit.com/user/PhilosophicalKingM",
    "https://philosophicalkingmusic.substack.com",
]


def main():
    c = canvas.Canvas(OUT, pagesize=A4)
    c.setTitle("Philosophical King")
    c.setAuthor("Philosophical King")

    left = 24 * mm
    y = H - 36 * mm

    c.setFillColorRGB(*INK)
    c.setFont(NAMES["bold"], 28)
    c.drawString(left, y, "Philosophical King")
    y -= 16 * mm

    size = 11.5
    for url in LINKS:
        c.setFillColorRGB(*LINK)
        c.setFont(NAMES["sans"], size)
        c.drawString(left, y, url)

        width = c.stringWidth(url, NAMES["sans"], size)
        c.setStrokeColorRGB(*LINK)
        c.setLineWidth(0.4)
        c.line(left, y - 1.3 * mm, left + width, y - 1.3 * mm)
        # Clickable box sized to the drawn text, with slack so a fingertip on a
        # phone still lands inside it.
        c.linkURL(url, (left, y - 2.4 * mm, left + width, y + 4.2 * mm), relative=0)

        y -= 9.5 * mm

    c.showPage()
    c.save()
    print("wrote", OUT)


if __name__ == "__main__":
    main()
