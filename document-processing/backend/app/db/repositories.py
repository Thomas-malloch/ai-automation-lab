import uuid
from datetime import date
from decimal import Decimal
from typing import Any

from sqlalchemy import select

from app.db.models import Document, Invoice, InvoiceLineItem, ValidationIssue
from app.db.session import SessionLocal


def create_document(
    *,
    filename: str,
    content_type: str,
    document_type: str,
    status: str,
    text_length: int,
    text_preview: str,
) -> Document:
    with SessionLocal() as session:
        document = Document(
            filename=filename,
            content_type=content_type,
            document_type=document_type,
            status=status,
            text_length=text_length,
            text_preview=text_preview,
        )
        session.add(document)
        session.commit()
        session.refresh(document)
        return document


def create_invoice_extraction(
    *,
    document_id: uuid.UUID,
    invoice_data: dict[str, Any],
    validation_errors: list[dict[str, Any]],
) -> Invoice:
    with SessionLocal() as session:
        invoice = Invoice(
            document_id=document_id,
            supplier_name=invoice_data["supplier_name"],
            invoice_number=invoice_data["invoice_number"],
            invoice_date=_parse_date(invoice_data.get("invoice_date")),
            due_date=_parse_date(invoice_data.get("due_date")),
            currency=invoice_data["currency"],
            subtotal=_parse_decimal(invoice_data.get("subtotal")),
            tax=_parse_decimal(invoice_data.get("tax")),
            total=_parse_decimal(invoice_data.get("total")),
            confidence=float(invoice_data["confidence"]),
        )
        session.add(invoice)
        session.flush()

        for item in invoice_data.get("line_items", []):
            session.add(
                InvoiceLineItem(
                    invoice_id=invoice.id,
                    description=item["description"],
                    quantity=_required_decimal(item["quantity"]),
                    unit_price=_required_decimal(item["unit_price"]),
                    total=_required_decimal(item["total"]),
                )
            )

        for issue in validation_errors:
            session.add(
                ValidationIssue(
                    document_id=document_id,
                    field=issue["field"],
                    message=issue["message"],
                    severity=issue.get("severity", "ERROR"),
                )
            )

        session.commit()
        session.refresh(invoice)
        return invoice


def get_document_result(document_id: uuid.UUID) -> dict[str, Any] | None:
    with SessionLocal() as session:
        document = session.get(Document, document_id)
        if document is None:
            return None

        invoice = session.scalar(
            select(Invoice).where(Invoice.document_id == document_id)
        )
        line_items: list[InvoiceLineItem] = []
        if invoice is not None:
            line_items = list(
                session.scalars(
                    select(InvoiceLineItem).where(InvoiceLineItem.invoice_id == invoice.id)
                )
            )
        validation_issues = list(
            session.scalars(
                select(ValidationIssue).where(ValidationIssue.document_id == document_id)
            )
        )

        return {
            "document": {
                "id": document.id,
                "filename": document.filename,
                "contentType": document.content_type,
                "documentType": document.document_type,
                "textLength": document.text_length,
                "textPreview": document.text_preview,
            },
            "processing": {
                "status": document.status,
                "validationErrors": [
                    {
                        "field": issue.field,
                        "message": issue.message,
                        "severity": issue.severity,
                    }
                    for issue in validation_issues
                ],
            },
            "extraction": {
                "type": document.document_type,
                "data": _invoice_to_dict(invoice, line_items) if invoice else {},
            },
        }


def list_documents(status: str | None = None) -> list[Document]:
    with SessionLocal() as session:
        statement = select(Document).order_by(Document.created_at.desc())
        if status is not None:
            statement = statement.where(Document.status == status)

        return list(session.scalars(statement))


def _parse_date(value: str | None) -> date | None:
    if value is None:
        return None
    return date.fromisoformat(value)


def _parse_decimal(value: Any) -> Decimal | None:
    if value is None:
        return None
    return Decimal(str(value))


def _required_decimal(value: Any) -> Decimal:
    return Decimal(str(value))


def _invoice_to_dict(
    invoice: Invoice,
    line_items: list[InvoiceLineItem],
) -> dict[str, Any]:
    return {
        "supplier_name": invoice.supplier_name,
        "invoice_number": invoice.invoice_number,
        "invoice_date": invoice.invoice_date.isoformat()
        if invoice.invoice_date is not None
        else None,
        "due_date": invoice.due_date.isoformat() if invoice.due_date is not None else None,
        "currency": invoice.currency,
        "subtotal": _decimal_to_string(invoice.subtotal),
        "tax": _decimal_to_string(invoice.tax),
        "total": _decimal_to_string(invoice.total),
        "confidence": invoice.confidence,
        "line_items": [
            {
                "description": item.description,
                "quantity": _decimal_to_string(item.quantity),
                "unit_price": _decimal_to_string(item.unit_price),
                "total": _decimal_to_string(item.total),
            }
            for item in line_items
        ],
    }


def _decimal_to_string(value: Decimal | None) -> str | None:
    if value is None:
        return None
    return str(value)
