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

## OpenAI Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Set your local values:

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-5-mini
USE_MOCK_EXTRACTOR=false
```

Use `USE_MOCK_EXTRACTOR=true` to run the service without calling OpenAI.

## Endpoints

- `GET /health`
- `POST /extract-invoice`

Example request:

```json
{
  "documentText": "raw invoice text"
}
```

Example request using the sample invoice text:

```bash
curl -X POST http://127.0.0.1:8000/extract-invoice \
  -H "Content-Type: application/json" \
  -d "{\"documentText\":\"$(tr '\n' ' ' < ../samples/invoice_text_basic.txt)\"}"
```
