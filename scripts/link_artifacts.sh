#!/usr/bin/env bash
# Symlink cached artifacts into vendor/phoenix/artifacts for run_pipeline.py
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENDOR="$ROOT/vendor/x-algorithm"
CACHE="${X_ALGORITHM_STUDIO_CACHE:-$HOME/.cache/x-algorithm-studio}"
SRC="$CACHE/oss-phoenix-artifacts"
LINK_PARENT="$VENDOR/phoenix/artifacts"
LINK="$LINK_PARENT/oss-phoenix-artifacts"

if [[ ! -d "$SRC" ]]; then
  echo "✖ cache missing: $SRC"
  exit 1
fi

mkdir -p "$LINK_PARENT"
if [[ -L "$LINK" || -d "$LINK" || -f "$LINK" ]]; then
  rm -rf "$LINK"
fi
ln -s "$SRC" "$LINK"
echo "✔ linked $LINK → $SRC"
