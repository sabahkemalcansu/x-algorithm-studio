#!/usr/bin/env bash
# Download / extract Phoenix OSS artifacts into a shared cache.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENDOR="$ROOT/vendor/x-algorithm"
CACHE="${X_ALGORITHM_STUDIO_CACHE:-$HOME/.cache/x-algorithm-studio}"
DEST="$CACHE/oss-phoenix-artifacts"
MARKER="$DEST/.studio_ready"

mkdir -p "$CACHE"

if [[ -f "$MARKER" ]]; then
  echo "✔ artifacts already ready: $DEST"
  # Symlink into vendor for upstream scripts
  bash "$ROOT/scripts/link_artifacts.sh"
  exit 0
fi

if [[ ! -d "$VENDOR/phoenix" ]]; then
  echo "✖ vendor missing — run make vendor first"
  exit 1
fi

echo "→ Preparing Phoenix artifacts (~3GB). This can take a while on first run."
echo "  cache: $DEST"

# Strategy 1: Git LFS pull inside vendor
if command -v git-lfs >/dev/null 2>&1 || git lfs version >/dev/null 2>&1; then
  echo "→ git lfs pull (vendor)…"
  (
    cd "$VENDOR"
    git lfs install --local 2>/dev/null || true
    git lfs pull || true
  )
fi

ART_DIR="$VENDOR/phoenix/artifacts"
ZIP=""
if [[ -f "$ART_DIR/oss-phoenix-artifacts.zip" ]]; then
  # Check it is not an LFS pointer
  if head -c 50 "$ART_DIR/oss-phoenix-artifacts.zip" | grep -q "git-lfs"; then
    echo "✖ oss-phoenix-artifacts.zip is still a Git LFS pointer."
    echo "  Install git-lfs and re-run:  brew install git-lfs && make pull"
    echo "  Or manually download artifacts per upstream phoenix/README.md"
    exit 1
  fi
  ZIP="$ART_DIR/oss-phoenix-artifacts.zip"
fi

if [[ -n "$ZIP" ]]; then
  echo "→ Extracting $ZIP → $DEST"
  rm -rf "$DEST"
  mkdir -p "$DEST"
  unzip -q "$ZIP" -d "$CACHE"
  # zip may contain oss-phoenix-artifacts/ top-level
  if [[ -d "$CACHE/oss-phoenix-artifacts" && ! -f "$MARKER" ]]; then
    :
  elif [[ -d "$CACHE/artifacts/oss-phoenix-artifacts" ]]; then
    mv "$CACHE/artifacts/oss-phoenix-artifacts" "$DEST"
  fi
  # Normalize: some zips extract nested
  if [[ ! -d "$DEST" ]]; then
    found="$(find "$CACHE" -type d -name 'oss-phoenix-artifacts' 2>/dev/null | head -1 || true)"
    if [[ -n "$found" && "$found" != "$DEST" ]]; then
      rm -rf "$DEST"
      mv "$found" "$DEST"
    fi
  fi
fi

# Strategy 2: already extracted under vendor
if [[ ! -f "$MARKER" ]]; then
  if [[ -d "$ART_DIR/oss-phoenix-artifacts" ]]; then
    echo "→ Copying vendor extracted artifacts to cache…"
    rm -rf "$DEST"
    mkdir -p "$CACHE"
    cp -R "$ART_DIR/oss-phoenix-artifacts" "$DEST"
  fi
fi

# Minimal readiness: ranker or retrieval params exist
if [[ -d "$DEST/ranker" || -d "$DEST/retrieval" || -f "$DEST/sports_corpus.npz" ]]; then
  date -u +"%Y-%m-%dT%H:%M:%SZ" > "$MARKER"
  echo "✔ artifacts ready: $DEST"
  bash "$ROOT/scripts/link_artifacts.sh"
  exit 0
fi

echo "✖ Could not materialize artifacts automatically."
echo ""
echo "Manual steps (from upstream phoenix/README.md):"
echo "  1. cd vendor/x-algorithm && git lfs pull"
echo "  2. unzip phoenix/artifacts/oss-phoenix-artifacts.zip -d /tmp"
echo "  3. mv the oss-phoenix-artifacts folder to:"
echo "       $DEST"
echo "  4. re-run: make pull"
exit 1
