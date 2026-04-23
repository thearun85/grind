.PHONY: install fmt lint typecheck test check clean

install:
	poetry install

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
