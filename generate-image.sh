#!/usr/bin/env bash
# Renders a 1080x1080 quote card with ImageMagick.
# Usage: generate-image.sh "<quote>" "<author>" <output.jpg>
set -euo pipefail

QUOTE="${1:?usage: generate-image.sh <quote> <author> <output.jpg>}"
AUTHOR="${2:?missing author}"
OUT="${3:?missing output path}"

# GitHub runners ship ImageMagick 6 (convert); IM7 uses magick.
if command -v magick >/dev/null 2>&1; then
  IM=magick
else
  IM=convert
fi

BG="#0e0f13"
GOLD="#e9c46a"
IVORY="#f2ede3"
GREY="#7a7e87"
FONT="DejaVu-Serif"

mkdir -p "$(dirname "$OUT")"

# caption: auto-sizes the text to fit the box, so long and short quotes both work.
"$IM" -size 1080x1080 "xc:${BG}" \
  \( -size 880x560 -background none -fill "$GOLD" -font "$FONT" \
     -gravity center "caption:“${QUOTE}”" \) \
  -gravity north -geometry +0+180 -composite \
  -fill "$GOLD" -draw "rectangle 465,806 615,808" \
  \( -size 880x60 -background none -fill "$IVORY" -font "$FONT" \
     -gravity center "caption:— ${AUTHOR}" \) \
  -gravity north -geometry +0+846 -composite \
  \( -size 700x36 -background none -fill "$GREY" -font "$FONT" \
     -gravity center "caption:P H I L O S O P H I C A L   K I N G" \) \
  -gravity south -geometry +0+56 -composite \
  -quality 92 "JPEG:${OUT}"

echo "Rendered ${OUT}"
