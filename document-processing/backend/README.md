# Document Processing Backend

FastAPI backend for PDF ingestion, workflow orchestration, persistence, and retrieval.

## Responsibilities

- Accept invoice PDF uploads.
- Extract text from text-based PDFs.
- Send extracted text to the AI service.
- Persist document metadata, extracted invoices, line items, and validation issues.
- Expose processed document results by ID and list documents by status.

## Local Setup

From this directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
make setup
```

Optional local config:

```bash
cp .env.example .env
```

Start Postgres from the parent `document-processing` directory and apply migrations:

```bash
cd ..
make postgres-up
make migrate
```

Start the backend API:

```bash
cd backend
source .venv/bin/activate
make dev
```

The AI service must also be running on port `8000`, or set `AI_SERVICE_URL`.

## API Smoke Test

From the repository root:

```bash
curl -X POST http://127.0.0.1:8001/documents \
  -F "file=@document-processing/samples/invoice_basic.pdf"
```

List processed documents:

```bash
curl http://127.0.0.1:8001/documents
curl "http://127.0.0.1:8001/documents?status=AUTO_APPROVED"
```

Fetch one document:

```bash
curl http://127.0.0.1:8001/documents/<document-uuid>
```

## Tests

```bash
make test
```
