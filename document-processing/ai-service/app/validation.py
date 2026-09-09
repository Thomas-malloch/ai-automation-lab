from decimal import Decimal

from app.schemas import ExtractedInvoice, ValidationIssue, WorkflowStatus

AUTO_APPROVAL_CONFIDENCE_THRESHOLD = 0.85
TOTAL_TOLERANCE = Decimal("0.02")
RECOGNISED_CURRENCIES = {"NZD", "AUD", "USD", "EUR", "GBP"}


def validate_invoice(invoice: ExtractedInvoice) -> tuple[WorkflowStatus, list[ValidationIssue]]:
    issues: list[ValidationIssue] = []

    if not invoice.supplier_name.strip():
        issues.append(
            ValidationIssue(
                field="supplier_name",
                message="Supplier name is required.",
            )
        )

    if not invoice.invoice_number.strip():
        issues.append(
            ValidationIssue(
                field="invoice_number",
                message="Invoice number is required.",
            )
        )

    currency = invoice.currency.strip().upper()
    if not currency:
        issues.append(
            ValidationIssue(
                field="currency",
                message="Currency is required.",
            )
        )
    elif currency not in RECOGNISED_CURRENCIES:
        issues.append(
            ValidationIssue(
                field="currency",
                message=f"Currency '{invoice.currency}' is not recognised.",
            )
        )

    if invoice.invoice_date is None:
        issues.append(
            ValidationIssue(
                field="invoice_date",
                message="Invoice date is required.",
            )
        )

    if invoice.total is None:
        issues.append(
            ValidationIssue(
                field="total",
                message="Total is required.",
            )
        )
    elif invoice.total <= 0:
        issues.append(
            ValidationIssue(
                field="total",
                message="Total must be greater than zero.",
            )
        )

    if invoice.subtotal is not None and invoice.tax is not None and invoice.total is not None:
        calculated_total = invoice.subtotal + invoice.tax
        if abs(calculated_total - invoice.total) > TOTAL_TOLERANCE:
            issues.append(
                ValidationIssue(
                    field="total",
                    message="Subtotal plus tax does not match total.",
                )
            )

    if issues or invoice.confidence < AUTO_APPROVAL_CONFIDENCE_THRESHOLD:
        return WorkflowStatus.REVIEW_REQUIRED, issues

    return WorkflowStatus.AUTO_APPROVED, issues

