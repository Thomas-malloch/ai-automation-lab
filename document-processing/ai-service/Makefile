.PHONY: setup test dev

PYTHON := .venv/bin/python

setup:
	$(PYTHON) -m pip install -e ".[dev]"

test:
	$(PYTHON) -m pytest

dev:
	$(PYTHON) -m uvicorn app.main:app --reload --reload-dir app --port 8000
