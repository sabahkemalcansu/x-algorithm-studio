#!/usr/bin/env bash
# Environment diagnostics for x-algorithm-studio
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CACHE="${X_ALGORITHM_STUDIO_CACHE:-$HOME/.cache/x-algorithm-studio}"
ok=0
warn=0
fail=0

pass() { echo "✔ $*"; ok=$((ok + 1)); }
note() { echo "• $*"; warn=$((warn + 1)); }
bad()  { echo "✖ $*"; fail=$((fail + 1)); }

echo "x-algorithm-studio doctor"
echo "root: $ROOT"
echo ""

# OS
uname_s="$(uname -s 2>/dev/null || echo unknown)"
uname_m="$(uname -m 2>/dev/null || echo unknown)"
pass "OS: $uname_s $uname_m"

# Disk (need ~5GB free recommended)
if command -v df >/dev/null 2>&1; then
  avail_kb="$(df -k "$HOME" 2>/dev/null | awk 'NR==2 {print $4}')"
  if [[ -n "${avail_kb:-}" ]]; then
    avail_gb=$((avail_kb / 1024 / 1024))
    if (( avail_gb >= 5 )); then
      pass "Free disk (home): ~${avail_gb} GB"
    elif (( avail_gb >= 2 )); then
      note "Free disk (home): ~${avail_gb} GB (artifacts need ~3–4 GB; may be tight)"
    else
      bad "Free disk (home): ~${avail_gb} GB — need more space for ~3GB artifacts"
    fi
  fi
fi

# Python
if command -v python3 >/dev/null 2>&1; then
  pass "python3: $(python3 --version 2>&1)"
else
  bad "python3 not found (needed for report renderer)"
fi

# Docker (preferred one-click)
if command -v docker >/dev/null 2>&1; then
  if docker info >/dev/null 2>&1; then
    pass "Docker: available and running"
  else
    note "Docker: installed but daemon not running"
  fi
else
  note "Docker: not found (native path still possible)"
fi

# Git + LFS
if command -v git >/dev/null 2>&1; then
  pass "git: $(git --version | head -1)"
else
  bad "git not found"
fi

if command -v git-lfs >/dev/null 2>&1 || git lfs version >/dev/null 2>&1; then
  pass "git-lfs: available"
else
  note "git-lfs: not found — artifact pull from upstream LFS may fail (brew install git-lfs)"
fi

# uv (native path)
if command -v uv >/dev/null 2>&1; then
  pass "uv: $(uv --version 2>&1 | head -1)"
else
  note "uv: not found — native phoenix run prefers uv (https://docs.astral.sh/uv/)"
fi

# Vendor
if [[ -d "$ROOT/vendor/x-algorithm/phoenix" ]]; then
  pass "vendor/x-algorithm: present"
  if [[ -f "$ROOT/vendor/x-algorithm/.git" ]] || [[ -d "$ROOT/vendor/x-algorithm/.git" ]]; then
    rev="$(git -C "$ROOT/vendor/x-algorithm" rev-parse --short HEAD 2>/dev/null || echo unknown)"
    note "vendor revision: $rev"
  fi
else
  note "vendor/x-algorithm: missing — run: make vendor"
fi

# Cache / artifacts
if [[ -d "$CACHE" ]]; then
  pass "cache dir: $CACHE"
else
  note "cache dir: will create $CACHE on first pull"
fi

if [[ -f "$CACHE/oss-phoenix-artifacts/.studio_ready" ]]; then
  pass "artifacts: cached and marked ready"
elif [[ -d "$CACHE/oss-phoenix-artifacts" ]]; then
  note "artifacts: cache dir exists (verify with make pull)"
else
  note "artifacts: not cached yet (~3GB download on first full demo)"
fi

# Fixture path always works
if [[ -f "$ROOT/fixtures/sample_results.json" ]]; then
  pass "fixtures: sample_results.json ready (make demo-fixture works offline)"
else
  bad "fixtures/sample_results.json missing"
fi

echo ""
echo "summary: $ok ok · $warn notes · $fail failures"
if (( fail > 0 )); then
  echo "fix some failures before full demo."
  exit 1
fi
echo "tip: offline explore now →  make demo-fixture && make open"
echo "tip: full Phoenix demo  →  make vendor && make pull && make demo-native"
exit 0
