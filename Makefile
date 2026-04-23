.PHONY: help install fmt lint typecheck test check clean init log

DEFAULT_GOAL := help

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies and pre-commit hooks
	poetry install --no-root
	poetry run pre-commit install

init: ## Initialise DB
	python -m src.init_db

log: ## Process leetlog.md and insert into db
	python -m src.leetlog

test: ## Run tests
	poetry run pytest -v -s

fmt: ## Format code with ruff
	poetry run ruff format src tests
	poetry run ruff check --fix src tests

lint: ## Lint (no fixes)
	poetry run ruff check src tests

typecheck: ## Run mypy
	poetry run mypy src tests

check: fmt lint typecheck test ## Run all checks (what CI runs)

clean: ## Remove caches and build artefacts
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
