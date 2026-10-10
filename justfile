# List recipes
default:
    @just --list

# Run all pytests and lint
test:
    pytest -vv tests/*
    @just lint

# Install dev dependencies in setup file
init:
    python -m venv .venv
    .venv/bin/pip install --editable ".[dev]"

# Format
fmt:
    ruff format
    ruff check --fix

# Lint
lint:
    ruff format --check
    ruff check
