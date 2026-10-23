#!/usr/bin/env bash
# Download the site photos into edge-asset/img/ so the page serves them itself.
# Needs network access to unsplash.com and images.unsplash.com (the GitHub workflow edge-asset-photos.yml runs it).
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p img
ids=(-MVSfkR4xz4 4UVtFIfK1eo 4mEyvORkbN0 GpJ9p1QH7O4 Q6sCJFHCubc TJ4CndIc9z8 a8A-z_ZPEC0 pcYN7Pi8_BQ q1tyQip5AQQ rD28m9BmXVs)
for id in "${ids[@]}"; do
  out="img/${id}.jpg"
  [ -s "$out" ] && { echo "skip $id"; continue; }
  curl -fsSL --retry 3 -o "$out" "https://unsplash.com/photos/${id}/download?force=true&w=1800" \
    && head -c 3 "$out" | od -An -tx1 | grep -q "ff d8 ff" && echo "ok   $id" || { echo "fail $id"; rm -f "$out"; }
done
# keep the repo light: cap width at 2000px and recompress
if command -v mogrify >/dev/null; then mogrify -resize "2000x>" -quality 80 -strip img/*.jpg; fi
ls -la img
python3 build.py index.html
