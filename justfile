test-all:
    pytest -vv tests/*

init:
    python -m venv .venv
    .venv/bin/pip install --editable ".[dev]"

fmt:
    ruff format
    ruff check --fix

lint:
    ruff format --check
    ruff check
