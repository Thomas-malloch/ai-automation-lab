.PHONY: setup test dev migrate revision

PYTHON := .venv/bin/python
ALEMBIC := .venv/bin/alembic

setup:
	$(PYTHON) -m pip install -e ".[dev]"

test:
	$(PYTHON) -m pytest

dev:
	$(PYTHON) -m uvicorn app.main:app --reload --port 8001

migrate:
	$(ALEMBIC) upgrade head

revision:
	$(ALEMBIC) revision --autogenerate -m "$(message)"
