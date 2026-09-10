import json
from datetime import date
from decimal import Decimal

from app.schemas import ExtractedInvoice, InvoiceLineItem
from app.settings import get_settings


def extract_invoice(document_text: str) -> ExtractedInvoice:
    settings = get_settings()
    if settings.use_mock_extractor:
        return mock_extract_invoice(document_text)

    return openai_extract_invoice(document_text)


def mock_extract_invoice(document_text: str) -> ExtractedInvoice:
    return ExtractedInvoice(
        supplier_name="Example Ltd",
        invoice_number="INV-1004",
        invoice_date=date(2026, 9, 1),
        due_date=date(2026, 9, 15),
        currency="NZD",
        subtotal=Decimal("372.61"),
        tax=Decimal("55.89"),
        total=Decimal("428.50"),
        confidence=0.91,
        line_items=[
            InvoiceLineItem(
                description="Consulting services",
                quantity=Decimal("1"),
                unit_price=Decimal("372.61"),
                total=Decimal("372.61"),
            )
        ],
    )


class ExtractionError(Exception):
    """Raised when invoice extraction cannot produce a valid structured result."""


INVOICE_EXTRACTION_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "supplier_name": {"type": "string"},
        "invoice_number": {"type": "string"},
        "invoice_date": {
            "type": ["string", "null"],
            "description": "Invoice date as YYYY-MM-DD, or null if not present.",
        },
        "due_date": {
            "type": ["string", "null"],
            "description": "Due date as YYYY-MM-DD, or null if not present.",
        },
        "currency": {
            "type": "string",
            "description": "Three-letter ISO currency code such as NZD, AUD, or USD.",
        },
        "subtotal": {"type": ["number", "null"]},
        "tax": {"type": ["number", "null"]},
        "total": {"type": ["number", "null"]},
        "confidence": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
            "description": "Overall confidence in the extracted invoice fields.",
        },
        "line_items": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "description": {"type": "string"},
                    "quantity": {"type": "number"},
                    "unit_price": {"type": "number"},
                    "total": {"type": "number"},
                },
                "required": ["description", "quantity", "unit_price", "total"],
            },
        },
    },
    "required": [
        "supplier_name",
        "invoice_number",
        "invoice_date",
        "due_date",
        "currency",
        "subtotal",
        "tax",
        "total",
        "confidence",
        "line_items",
    ],
}


def openai_extract_invoice(document_text: str) -> ExtractedInvoice:
    settings = get_settings()
    if not settings.openai_api_key:
        raise ExtractionError("OPENAI_API_KEY is required when USE_MOCK_EXTRACTOR=false.")

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise ExtractionError(
            "The openai package is not installed. Run `make setup` from ai-service."
        ) from exc

    client = OpenAI(api_key=settings.openai_api_key)

    try:
        response = client.responses.create(
            model=settings.openai_model,
            input=[
                {
                    "role": "developer",
                    "content": (
                        "Extract invoice fields from raw document text. "
                        "Return only fields supported by the JSON schema. "
                        "Use null for missing dates or money values. "
                        "Use empty strings for missing text values. "
                        "Do not invent values that are not supported by the document."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Invoice document text:\n\n{document_text}",
                },
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "invoice_extraction",
                    "schema": INVOICE_EXTRACTION_SCHEMA,
                    "strict": True,
                }
            },
            store=False,
        )
    except Exception as exc:
        raise ExtractionError(f"OpenAI extraction request failed: {exc}") from exc

    try:
        payload = json.loads(response.output_text)
        return ExtractedInvoice.model_validate(payload)
    except Exception as exc:
        raise ExtractionError(f"OpenAI response did not match invoice schema: {exc}") from exc
