# AI Service

FastAPI service for PDF text extraction, OpenAI structured invoice extraction, confidence handling, and invoice validation helpers.

## Local Development

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
make setup
```

Run the API:

```bash
make dev
```

Run tests:

```bash
make test
```

The equivalent direct commands are:

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m uvicorn app.main:app --reload --reload-dir app
```

## Endpoints

- `GET /health`
- `POST /extract-invoice`

Example request:

```json
{
  "documentText": "raw invoice text"
}
```
