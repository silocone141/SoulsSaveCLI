commands:
    pytest -vv tests/test_commands.py

init:
    python -m venv .venv
    .venv/bin/pip install --editable ".[dev]"
