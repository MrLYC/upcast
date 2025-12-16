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

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
