# AI Service

FastAPI service for PDF text extraction, OpenAI structured invoice extraction, confidence handling, and invoice validation helpers.

## Local Development

Install dependencies:

```bash
python3 -m pip install -e ".[dev]"
```

Run the API:

```bash
python3 -m uvicorn app.main:app --reload
```

Run tests:

```bash
python3 -m pytest
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
