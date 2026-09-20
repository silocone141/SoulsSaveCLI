test-all:
    pytest -vv tests/*

init:
    python -m venv .venv
    .venv/bin/pip install --editable ".[dev]"
