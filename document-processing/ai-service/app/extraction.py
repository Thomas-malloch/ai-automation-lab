from datetime import date
from decimal import Decimal

from app.schemas import ExtractedInvoice, InvoiceLineItem


def extract_invoice(document_text: str) -> ExtractedInvoice:
    """Temporary extractor until the OpenAI structured output client is added."""
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

