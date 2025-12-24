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

.PHONY: publish
publish: ## publish a release to pypi.
	@echo "🚀 Publishing."
	@uv publish

.PHONY: test-integration
test-integration: ## Run integration tests on example project
	@echo "🚀 Running scanner integration tests on blueking-paas"
	@mkdir -p example/scan-results
	@uv run upcast scan-blocking-operations example/blueking-paas -o example/scan-results/blocking-operations.yaml || true
	@uv run upcast scan-complexity-patterns example/blueking-paas -o example/scan-results/complexity-patterns.yaml --threshold 10 || true
	@uv run upcast scan-concurrency-patterns example/blueking-paas -o example/scan-results/concurrency-patterns.yaml || true
	@uv run upcast scan-django-models example/blueking-paas -o example/scan-results/django-models.yaml || true
	@uv run upcast scan-django-settings example/blueking-paas -o example/scan-results/django-settings.yaml || true
	@uv run upcast scan-django-urls example/blueking-paas -o example/scan-results/django-urls.yaml || true
	@uv run upcast scan-env-vars example/blueking-paas -o example/scan-results/env-vars.yaml || true
	@uv run upcast scan-exception-handlers example/blueking-paas -o example/scan-results/exception-handlers.yaml || true
	@uv run upcast scan-http-requests example/blueking-paas -o example/scan-results/http-requests.yaml || true
	@uv run upcast scan-metrics example/blueking-paas -o example/scan-results/metrics.yaml || true
	@uv run upcast scan-signals example/blueking-paas -o example/scan-results/signals.yaml || true
	@uv run upcast scan-unit-tests example/blueking-paas -o example/scan-results/unit-tests.yaml || true
	@uv run upcast scan-redis-usage example/blueking-paas -o example/scan-results/redis-usage.yaml || true
	@uv run upcast scan-module-symbols example/blueking-paas -o example/scan-results/module-symbols.yaml || true

	@echo "✓ Integration tests complete. Results in example/scan-results/"

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
