#!/usr/bin/env bash
# Native: run upstream phoenix pipeline when possible, then aha report.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENDOR="$ROOT/vendor/x-algorithm"
CACHE="${X_ALGORITHM_STUDIO_CACHE:-$HOME/.cache/x-algorithm-studio}"
ART="$CACHE/oss-phoenix-artifacts"
OUT="$ROOT/out/latest"
mkdir -p "$OUT"

START="$(date +%s)"

bash "$ROOT/scripts/ensure_vendor.sh"
bash "$ROOT/scripts/pull-artifacts.sh"

# Try upstream run_pipeline via uv or python
PIPELINE_JSON="$OUT/pipeline_raw.json"
RUN_OK=0

run_pipeline() {
  local py_cmd=("$@")
  (
    cd "$VENDOR/phoenix"
    "${py_cmd[@]}" run_pipeline.py \
      --artifacts_dir "$ART" \
      --top_k_retrieval "${TOP_K_RETRIEVAL:-200}" \
      --top_k_display "${TOP_K_DISPLAY:-20}" \
      2>&1 | tee "$OUT/pipeline.log"
  )
}

if command -v uv >/dev/null 2>&1 && [[ -f "$VENDOR/phoenix/pyproject.toml" ]]; then
  echo "→ uv run run_pipeline.py …"
  (
    cd "$VENDOR/phoenix"
    uv sync 2>&1 | tee "$OUT/uv_sync.log" || true
  )
  if (cd "$VENDOR/phoenix" && uv run python run_pipeline.py --artifacts_dir "$ART" --top_k_retrieval "${TOP_K_RETRIEVAL:-200}" --top_k_display "${TOP_K_DISPLAY:-20}" 2>&1 | tee "$OUT/pipeline.log"); then
    RUN_OK=1
  fi
elif command -v python3 >/dev/null 2>&1; then
  echo "→ python3 run_pipeline.py …"
  if (cd "$VENDOR/phoenix" && python3 run_pipeline.py --artifacts_dir "$ART" --top_k_retrieval "${TOP_K_RETRIEVAL:-200}" --top_k_display "${TOP_K_DISPLAY:-20}" 2>&1 | tee "$OUT/pipeline.log"); then
    RUN_OK=1
  fi
fi

END="$(date +%s)"
DURATION=$((END - START))

if [[ "$RUN_OK" -eq 1 ]]; then
  echo "→ Normalizing pipeline log → results.json"
  python3 "$ROOT/scripts/run_and_report.py" \
    --mode parse-log \
    --log "$OUT/pipeline.log" \
    --output "$OUT/results.json" \
    --duration "$DURATION" \
    --artifacts-dir "$ART" \
    --vendor "$VENDOR" \
    || python3 "$ROOT/scripts/run_and_report.py" \
         --mode fixture \
         --fixture "$ROOT/fixtures/sample_results.json" \
         --output "$OUT/results.json" \
         --duration "$DURATION" \
         --note "parse-log fallback to structure from fixture meta"
else
  echo "✖ Pipeline did not complete. See out/latest/pipeline.log if present."
  echo "  Falling back is disabled for demo-native (use make demo-fixture for offline)."
  exit 1
fi

python3 "$ROOT/scripts/render_aha_report.py" \
  --input "$OUT/results.json" \
  --output "$OUT/report.html" \
  --lang tr

echo ""
echo "✔ Demo complete in ${DURATION}s"
echo "  JSON: $OUT/results.json"
echo "  HTML: $OUT/report.html"
echo "  make open"
