# Document Processing

Autonomous invoice-processing pipeline for the AI Automation Systems Lab.

Initial MVP flow:

```text
Upload invoice
Extract text
Extract structured invoice fields
Validate result
Store workflow state
Route uncertain records to review
```

## Structure

```text
document-processing/
├── backend/        # Spring Boot API and persistence
├── ai-service/     # FastAPI service for extraction and AI calls
├── frontend/       # React dashboard and review UI
├── samples/        # Sample invoices and extracted text fixtures
└── docker-compose.yml
```

