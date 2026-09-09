.PHONY: setup test dev

setup:
	python -m pip install -e ".[dev]"

test:
	python -m pytest

dev:
	python -m uvicorn app.main:app --reload --reload-dir app

