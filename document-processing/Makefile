.PHONY: setup setup-backend setup-ai postgres-up postgres-down migrate test-backend test-ai run-backend run-ai upload-sample list-documents

setup: setup-backend setup-ai

setup-backend:
	cd backend && python3 -m venv .venv && .venv/bin/python -m pip install -e ".[dev]"

setup-ai:
	cd ai-service && python3 -m venv .venv && .venv/bin/python -m pip install -e ".[dev]"

postgres-up:
	docker compose up -d postgres

postgres-down:
	docker compose down

migrate:
	cd backend && .venv/bin/alembic upgrade head

test-backend:
	cd backend && .venv/bin/python -m pytest

test-ai:
	cd ai-service && .venv/bin/python -m pytest

run-backend:
	cd backend && .venv/bin/python -m uvicorn app.main:app --reload --port 8001

run-ai:
	cd ai-service && .venv/bin/python -m uvicorn app.main:app --reload --reload-dir app --port 8000

upload-sample:
	curl -X POST http://127.0.0.1:8001/documents \
		-F "file=@samples/invoice_basic.pdf"

list-documents:
	curl http://127.0.0.1:8001/documents
