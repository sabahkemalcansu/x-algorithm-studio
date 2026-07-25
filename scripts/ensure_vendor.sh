#!/usr/bin/env bash
# Ensure vendor/x-algorithm exists (submodule or shallow clone).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENDOR="$ROOT/vendor/x-algorithm"
UPSTREAM_URL="${X_ALGORITHM_URL:-https://github.com/xai-org/x-algorithm.git}"

if [[ -d "$VENDOR/phoenix" ]]; then
  echo "✔ vendor/x-algorithm already present"
  exit 0
fi

echo "→ Fetching xai-org/x-algorithm into vendor/…"
mkdir -p "$ROOT/vendor"

# Prefer submodule if .gitmodules configured
if [[ -f "$ROOT/.gitmodules" ]] && grep -q "vendor/x-algorithm" "$ROOT/.gitmodules" 2>/dev/null; then
  git -C "$ROOT" submodule update --init --recursive vendor/x-algorithm
else
  # Shallow clone for speed; pin can be updated later
  git clone --depth 1 "$UPSTREAM_URL" "$VENDOR"
fi

if [[ ! -d "$VENDOR/phoenix" ]]; then
  echo "✖ vendor clone failed (phoenix/ missing)"
  exit 1
fi

rev="$(git -C "$VENDOR" rev-parse --short HEAD 2>/dev/null || echo unknown)"
echo "✔ vendor ready @ $rev"
echo "  path: $VENDOR"
