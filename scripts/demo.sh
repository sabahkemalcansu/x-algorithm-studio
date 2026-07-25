#!/usr/bin/env bash
# Smart one-click: Docker if healthy, else native, else fixture fallback message.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
  if [[ -f "$ROOT/docker/compose.yml" ]]; then
    echo "→ Using Docker path (make demo → compose)"
    # Full model image may still need build; for now compose runs fixture-capable entry
    docker compose -f "$ROOT/docker/compose.yml" run --rm demo
    exit $?
  fi
fi

echo "→ Docker not ready — trying native path"
if bash "$ROOT/scripts/run_demo.sh"; then
  exit 0
fi

echo ""
echo "Native full demo unavailable (artifacts/JAX)."
echo "You can still explore the product offline:"
echo "  make demo-fixture && make open"
exit 1
