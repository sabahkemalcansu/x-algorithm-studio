# x-algorithm-studio — Run · Understand · Extend
SHELL := /bin/bash
.DEFAULT_GOAL := help

ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
export STUDIO_ROOT := $(ROOT)
export PYTHONPATH := $(ROOT)/scripts:$(PYTHONPATH)

.PHONY: help doctor pull vendor demo demo-native demo-fixture report report-fixture open clean

help: ## Show targets
	@echo "x-algorithm-studio — Run · Understand · Extend"
	@echo ""
	@echo "  make doctor         Check environment"
	@echo "  make vendor         Init/update x-algorithm submodule"
	@echo "  make pull           Download/cache Phoenix artifacts (~3GB)"
	@echo "  make demo           One-click demo (Docker if available, else native)"
	@echo "  make demo-native    Native uv/python path"
	@echo "  make demo-fixture   Offline aha report from fixtures (no model)"
	@echo "  make report         Re-render HTML from out/latest/results.json"
	@echo "  make open           Open out/latest/report.html"
	@echo "  make clean          Remove out/"
	@echo ""

doctor: ## Environment diagnostics
	@bash "$(ROOT)/scripts/doctor.sh"

vendor: ## Ensure vendor/x-algorithm is present
	@bash "$(ROOT)/scripts/ensure_vendor.sh"

pull: vendor ## Pull artifacts into cache
	@bash "$(ROOT)/scripts/pull-artifacts.sh"

demo: ## Preferred one-click path
	@bash "$(ROOT)/scripts/demo.sh"

demo-native: vendor pull ## Native pipeline + aha report
	@bash "$(ROOT)/scripts/run_demo.sh"

demo-fixture: ## No GPU/JAX — render aha report from sample JSON
	@mkdir -p "$(ROOT)/out/latest"
	@cp "$(ROOT)/fixtures/sample_results.json" "$(ROOT)/out/latest/results.json"
	@python3 "$(ROOT)/scripts/render_aha_report.py" \
		--input "$(ROOT)/out/latest/results.json" \
		--output "$(ROOT)/out/latest/report.html"
	@echo ""
	@echo "✔ Fixture demo ready → out/latest/report.html"
	@echo "  make open"

report: ## Render aha HTML from last results.json
	@test -f "$(ROOT)/out/latest/results.json" || (echo "No out/latest/results.json — run make demo or make demo-fixture"; exit 1)
	@python3 "$(ROOT)/scripts/render_aha_report.py" \
		--input "$(ROOT)/out/latest/results.json" \
		--output "$(ROOT)/out/latest/report.html"
	@echo "✔ Wrote out/latest/report.html"

report-fixture: demo-fixture

open: ## Open report in browser (macOS)
	@test -f "$(ROOT)/out/latest/report.html" || (echo "No report — run make demo-fixture"; exit 1)
	@open "$(ROOT)/out/latest/report.html" 2>/dev/null || xdg-open "$(ROOT)/out/latest/report.html" 2>/dev/null || echo "Open: $(ROOT)/out/latest/report.html"

clean: ## Clear generated outputs
	@rm -rf "$(ROOT)/out"
	@echo "✔ out/ cleaned"
