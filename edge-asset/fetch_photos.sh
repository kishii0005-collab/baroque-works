#!/usr/bin/env bash
# Download the site photos into edge-asset/img/ so the page serves them itself.
# Needs network access to unsplash.com and images.unsplash.com (the GitHub workflow edge-asset-photos.yml runs it).
# The plain download link answers 401 to automated requests, so each photo tries, in order:
#   1. the image URL named in the photo page's og:image
#   2. the wsrv.nl image cache in front of the download link
#   3. the download link itself with a browser user-agent
set -uo pipefail
cd "$(dirname "$0")"
mkdir -p img
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
ids=(-MVSfkR4xz4 4UVtFIfK1eo 4mEyvORkbN0 GpJ9p1QH7O4 Q6sCJFHCubc TJ4CndIc9z8 a8A-z_ZPEC0 pcYN7Pi8_BQ q1tyQip5AQQ rD28m9BmXVs)
is_jpeg() { [ -s "$1" ] && head -c 3 "$1" | od -An -tx1 | grep -q "ff d8 ff"; }
get() { curl -fsSL --retry 2 -A "$UA" -o "$2" "$1" && is_jpeg "$2"; }
for id in "${ids[@]}"; do
  out="img/${id}.jpg"
  is_jpeg "$out" && { echo "skip $id"; continue; }
  og=$(curl -fsSL -A "$UA" "https://unsplash.com/photos/${id}" | grep -o 'https://images\.unsplash\.com/photo-[^"?&]*' | head -1)
  if [ -n "$og" ] && get "${og}?w=2000&q=80&fm=jpg&fit=max" "$out"; then echo "ok   $id (og:image)"; continue; fi
  if get "https://wsrv.nl/?url=unsplash.com/photos/${id}/download%3Fforce%3Dtrue%26w%3D2000&w=2000&q=80&output=jpg" "$out"; then echo "ok   $id (wsrv)"; continue; fi
  if get "https://unsplash.com/photos/${id}/download?force=true&w=2000" "$out"; then echo "ok   $id (download)"; continue; fi
  echo "fail $id"; rm -f "$out"
done
# keep the repo light: cap width at 2000px and recompress
if command -v mogrify >/dev/null && ls img/*.jpg >/dev/null 2>&1; then mogrify -resize "2000x>" -quality 80 -strip img/*.jpg; fi
ls -la img
python3 build.py index.html
