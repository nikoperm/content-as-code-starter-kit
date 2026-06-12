VENV := .venv/bin
PYTHON := $(VENV)/python

.PHONY: help setup build build-html validate validate-deep validate-design status activity changelog catalog clean

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

setup: ## Install Python dependencies in .venv
	@test -d .venv || python3 -m venv .venv
	$(VENV)/pip install -q -r requirements.txt
	@echo "Setup complete. Open this folder in Claude Code, Antigravity, or Cursor to get started."

build: build-html ## Build all outputs (HTML)
	@echo "Build complete."

build-html: ## Build HTML overview documents
	@mkdir -p build
	$(PYTHON) scripts/build_presentation.py --all 2>/dev/null || echo "(presentation build skipped — check scripts/build_presentation.py)"

validate: ## Run workspace health check
	$(PYTHON) scripts/validate_workspace.py

validate-deep: ## Run extended validation (incl. cross-references)
	$(PYTHON) scripts/validate_workspace.py --deep

validate-design: ## Check Telegrafen design compliance
	$(PYTHON) scripts/validate_design.py

status: ## Show workspace status (git + content health)
	@echo "=== Git Status ==="
	@git status --short 2>/dev/null || echo "(not a git repository)"
	@echo ""
	@echo "=== Content Health ==="
	@$(PYTHON) scripts/validate_workspace.py --summary 2>/dev/null || echo "(run 'make setup' first)"

activity: ## Show recent activity
	@echo "=== Recent Activity (git log) ==="
	@git log --format="  %C(cyan)%ad%C(reset) | %C(yellow)%an%C(reset) | %s" --date=short -20 2>/dev/null || echo "(no commits yet)"
	@echo ""
	@if [ -f logs/activity.log ]; then echo "=== Agent Activity (last 20 entries) ===" && tail -20 logs/activity.log; else echo "(no agent activity log yet)"; fi

changelog: ## Show changelog (last 7 days)
	@$(PYTHON) scripts/generate_changelog.py

catalog: ## Regenerate CATALOG.md from front-matter
	$(PYTHON) scripts/generate_catalog.py --save

clean: ## Delete build outputs
	rm -rf build/*
	@echo "Build outputs cleaned."
