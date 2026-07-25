# Code map

## This studio

| Path | Responsibility |
|------|----------------|
| `scripts/doctor.sh` | Environment checks |
| `scripts/ensure_vendor.sh` | Fetch `xai-org/x-algorithm` |
| `scripts/pull-artifacts.sh` | ~3GB Phoenix artifacts cache |
| `scripts/run_demo.sh` | Native full demo orchestration |
| `scripts/run_and_report.py` | Normalize → `results.json` |
| `scripts/render_aha_report.py` | Aha HTML (product face) |
| `fixtures/sample_results.json` | Offline teaching run |
| `extensions/` | **Your** code |
| `agent/` | Drop-in learning loop |
| `AGENTS.md` | Agent entrypoint |

## Upstream (after `make vendor`)

| Path | Responsibility |
|------|----------------|
| `vendor/x-algorithm/phoenix/` | JAX retrieval + ranking demo |
| `vendor/x-algorithm/phoenix/run_pipeline.py` | E2E retrieval→rank entry |
| `vendor/x-algorithm/home-mixer/` | Orchestration (Rust) |
| `vendor/x-algorithm/thunder/` | In-network store |
| `vendor/x-algorithm/candidate-pipeline/` | Pipeline traits |
| `vendor/x-algorithm/grox/` | Content understanding |

Pin the submodule/clone; prefer reading over forking upstream files.
