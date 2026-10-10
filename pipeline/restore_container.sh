#!/usr/bin/env bash
# Put a rebuilt container back to work.
#
# The container is wiped periodically. Each time, the same three things go:
# Pillow, the CJK fonts, and /tmp/.pz. The scripts then fail in three
# different ways, none of which say "the container rebuilt". This says it.
#
# POSTIZ_KEY is deliberately NOT in here: this repo is public. The key lives
# in the two paused fresh-session Routine prompts; paste it as the argument.
#
#   bash pipeline/restore_container.sh <POSTIZ_KEY>
set -u

key="${1:-}"
if [ -n "$key" ]; then
  umask 077
  printf '%s' "$key" > /tmp/.pz
  echo "wrote /tmp/.pz"
else
  [ -s /tmp/.pz ] && echo "/tmp/.pz already present" \
                  || echo "WARNING: /tmp/.pz missing and no key given; every Postiz script will fail"
fi

# pip and python3 can resolve to different versions after a rebuild, which is
# why this goes through python3 -m pip rather than plain pip.
python3 -c 'import PIL' 2>/dev/null \
  && echo "pillow present" \
  || { echo "installing pillow..."; python3 -m pip install --quiet pillow && echo "pillow installed"; }

CJK=/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc
[ -f "$CJK" ] \
  && echo "CJK fonts present" \
  || { echo "installing CJK fonts..."; apt-get update -qq >/dev/null 2>&1
       apt-get install -y -qq fonts-noto-cjk >/dev/null 2>&1 && echo "CJK fonts installed"; }

command -v ffmpeg >/dev/null && echo "ffmpeg present" || echo "WARNING: ffmpeg missing, nothing will render"

echo
echo "checks:"
python3 -c "import PIL; print('  pillow', PIL.__version__)" 2>/dev/null || echo "  pillow STILL MISSING"
[ -f "$CJK" ] && echo "  CJK font ok" || echo "  CJK font STILL MISSING"
if [ -s /tmp/.pz ]; then
  code=$(curl -sS -o /dev/null -w '%{http_code}' -H "Authorization: $(cat /tmp/.pz)" \
    -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36' \
    https://api.postiz.com/public/v1/integrations)
  [ "$code" = "200" ] && echo "  postiz key ok" || echo "  postiz key REJECTED (HTTP $code)"
fi
