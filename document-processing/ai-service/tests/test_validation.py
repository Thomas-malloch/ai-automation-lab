from datetime import date
from decimal import Decimal

from app.schemas import ExtractedInvoice, WorkflowStatus
from app.validation import validate_invoice


def valid_invoice() -> ExtractedInvoice:
    return ExtractedInvoice(
        supplier_name="Example Ltd",
        invoice_number="INV-1004",
        invoice_date=date(2026, 9, 1),
        currency="NZD",
        subtotal=Decimal("372.61"),
        tax=Decimal("55.89"),
        total=Decimal("428.50"),
        confidence=0.91,
    )


def test_valid_invoice_is_auto_approved() -> None:
    status, issues = validate_invoice(valid_invoice())

    assert status == WorkflowStatus.AUTO_APPROVED
    assert issues == []


def test_missing_invoice_number_requires_review() -> None:
    invoice = valid_invoice()
    invoice.invoice_number = ""

    status, issues = validate_invoice(invoice)

    assert status == WorkflowStatus.REVIEW_REQUIRED
    assert [issue.field for issue in issues] == ["invoice_number"]


def test_invalid_total_requires_review() -> None:
    invoice = valid_invoice()
    invoice.total = Decimal("400.00")

    status, issues = validate_invoice(invoice)

    assert status == WorkflowStatus.REVIEW_REQUIRED
    assert [issue.field for issue in issues] == ["total"]


def test_low_confidence_requires_review_without_validation_errors() -> None:
    invoice = valid_invoice()
    invoice.confidence = 0.70

    status, issues = validate_invoice(invoice)

    assert status == WorkflowStatus.REVIEW_REQUIRED
    assert issues == []


def test_unrecognised_currency_requires_review() -> None:
    invoice = valid_invoice()
    invoice.currency = "BTC"

    status, issues = validate_invoice(invoice)

    assert status == WorkflowStatus.REVIEW_REQUIRED
    assert [issue.field for issue in issues] == ["currency"]

