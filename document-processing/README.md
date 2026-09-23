# Document Processing

Autonomous invoice-processing API for the AI Automation Systems Lab.

The project accepts a text-based invoice PDF, extracts text, sends that text to a separate AI service for structured invoice extraction, validates the result, persists workflow state in Postgres, and exposes retrieval endpoints.

## Architecture

```text
curl / API client
  -> backend FastAPI service
      -> PDF text extraction with pypdf
      -> ai-service /extract-invoice
          -> OpenAI structured extraction, or mock extraction locally
          -> validation rules
      -> Postgres persistence
  -> JSON response
```

## Structure

```text
document-processing/
├── backend/        # FastAPI orchestration API, persistence, migrations
├── ai-service/     # FastAPI AI extraction and validation service
├── samples/        # Committed text fixtures; generated PDFs are ignored
├── docker-compose.yml
└── Makefile
```

## Current API

```text
POST /documents
GET  /documents
GET  /documents/{document_id}
```

`POST /documents` processes and persists a new PDF. `GET /documents` lists persisted workflow summaries. `GET /documents/{document_id}` returns the saved document, processing status, validation issues, and extracted invoice data.

## Local Setup

Create virtual environments and install dependencies in both services:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
make setup

cd ../ai-service
python3 -m venv .venv
source .venv/bin/activate
make setup
```

Copy environment examples if you need local overrides:

```bash
cp backend/.env.example backend/.env
cp ai-service/.env.example ai-service/.env
```

Start Postgres and apply migrations:

```bash
make postgres-up
make migrate
```

Run the AI service in one terminal:

```bash
make run-ai
```

Run the backend in another terminal:

```bash
make run-backend
```

## Demo

From `document-processing/`, upload the sample PDF:

```bash
make upload-sample
```

List processed documents:

```bash
make list-documents
```

Fetch one document by UUID:

```bash
curl http://127.0.0.1:8001/documents/<document-uuid>
```

Filter by status:

```bash
curl "http://127.0.0.1:8001/documents?status=AUTO_APPROVED"
```

## Tests

```bash
make test-backend
make test-ai
```

## Notes

- The backend stores document metadata, invoice fields, line items, and validation issues in Postgres.
- The backend does not call OpenAI directly. It calls `ai-service`.
- `ai-service` calls OpenAI only when `USE_MOCK_EXTRACTOR=false`; otherwise it returns deterministic mock invoice data for local development.
- Current PDF extraction supports text-based PDFs. Scanned/image-only PDFs require OCR and are not supported yet.
