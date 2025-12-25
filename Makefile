.PHONY: install
install: ## Install the UV environment and install the pre-commit hooks
	@echo "🚀 Creating virtual environment using UV"
	@uv sync --all-extras
	@uv run pre-commit install
	@echo "✓ Virtual environment ready at .venv/"

.PHONY: check
check: ## Run code quality tools.
	@echo "🚀 Checking UV lock file consistency with 'pyproject.toml': Running uv lock --check"
	@uv lock --check
	@echo "🚀 Linting code: Running pre-commit"
	@uv run pre-commit run -a
	@echo "🚀 Static type checking: Running mypy"
	@uv run mypy

.PHONY: test
test: ## Test the code with pytest
	@echo "🚀 Testing code: Running pytest"
	@$(eval args := )
	@uv run pytest -vv --cov --cov-config=pyproject.toml --cov-report=xml ${args}

.PHONY: build
build: clean-build ## Build wheel file using UV
	@echo "🚀 Creating wheel file"
	@uv build

.PHONY: clean-build
clean-build: ## clean build artifacts
	@rm -rf dist

.PHONY: clean
clean: ## Clean all generated files and caches
	@echo "🧹 Cleaning up..."
	@rm -rf dist/
	@rm -rf build/
	@rm -rf *.egg-info
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf .ruff_cache
	@rm -rf htmlcov/
	@rm -rf .coverage
	@rm -rf coverage.xml
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type f -name "*.backup" -delete
	@find . -type f -name "*~" -delete
	@echo "✓ Cleanup complete"

.PHONY: publish
publish: clean build ## Clean, build and publish a release to PyPI
	@echo "🚀 Publishing to PyPI..."
	@uv publish
	@echo "✓ Published successfully"

.PHONY: test-integration
test-integration: ## Run integration tests on example project
	@echo "🚀 Running scanner integration tests on blueking-paas"
	@mkdir -p example/scan-results
	@echo "📊 Generating YAML and Markdown reports..."
	@for scanner in \
		"blocking-operations:" \
		"complexity-patterns:--threshold 10" \
		"concurrency-patterns:" \
		"django-models:" \
		"django-settings:" \
		"django-urls:" \
		"env-vars:" \
		"exception-handlers:" \
		"http-requests:" \
		"metrics:" \
		"signals:" \
		"unit-tests:" \
		"redis-usage:" \
		"module-symbols:" \
		"logging:"; do \
		name=$${scanner%%:*}; \
		args=$${scanner#*:}; \
		echo "  ⚡ Running scan-$$name..."; \
		uv run upcast scan-$$name example/blueking-paas \
			-o example/scan-results/$$name.yaml \
			$$args || true; \
		uv run upcast scan-$$name example/blueking-paas \
			--format markdown \
			--markdown-language zh \
			--markdown-title "$$name 扫描报告" \
			-o example/markdown-reports/$$name.md \
			$$args || true; \
	done
	@echo "✓ Integration tests complete. Results in example/scan-results/"
	@echo "  📄 YAML reports: example/scan-results/*.yaml"
	@echo "  📝 Markdown reports: example/scan-results/*.md"

.PHONY: clean-scan-results
clean-scan-results: ## Clean integration test results
	@echo "🧹 Cleaning scan results"
	@rm -rf example/scan-results/*
	@echo "✓ Scan results cleaned"

.PHONY: test-integration-update
test-integration-update: test-integration ## Run integration tests and update baseline

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
