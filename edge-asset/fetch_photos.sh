#!/usr/bin/env bash
# Download the site photos into edge-asset/img/ so the page serves them itself.
# Needs network access to unsplash.com and images.unsplash.com.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p img
ids=(Q6sCJFHCubc -MVSfkR4xz4 TJ4CndIc9z8 pcYN7Pi8_BQ 4UVtFIfK1eo q1tyQip5AQQ rD28m9BmXVs 4mEyvORkbN0)
for id in "${ids[@]}"; do
  out="img/${id}.jpg"
  [ -s "$out" ] && { echo "skip $id"; continue; }
  curl -fsSL --retry 3 -o "$out" "https://unsplash.com/photos/${id}/download?force=true&w=1800" \
    && echo "ok   $id" || { echo "fail $id"; rm -f "$out"; }
done
python3 build.py index.html
