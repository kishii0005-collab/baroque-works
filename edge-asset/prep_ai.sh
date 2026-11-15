#!/usr/bin/env bash
# Normalize generated photos in img/ai/: any png/webp/jpeg becomes <name>.jpg, long side 2400px, quality 82, metadata stripped.
set -euo pipefail
cd "$(dirname "$0")/img/ai"
for f in *.png *.webp *.jpeg *.PNG *.JPG; do [ -e "$f" ] || continue; convert "$f" "${f%.*}.jpg" && rm -f "$f"; done
for f in *.jpg; do [ -e "$f" ] || continue; mogrify -resize "2400x2400>" -quality 82 -strip "$f"; done
ls -la
