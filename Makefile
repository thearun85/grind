.PHONY: install fmt lint typecheck test check clean init log

install:
	poetry install --no-root
	poetry run pre-commit install

init:
	python -m src.init_db

log:
	python -m src.leetlog

test:
	poetry run pytest -v -s

fmt:
	poetry run ruff format src tests
	poetry run ruff check --fix src tests

lint:
	poetry run ruff check src tests

typecheck:
	poetry run mypy src tests

check: fmt lint typecheck test

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
