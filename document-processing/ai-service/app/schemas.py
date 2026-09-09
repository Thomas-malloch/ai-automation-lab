from datetime import date
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class WorkflowStatus(StrEnum):
    AUTO_APPROVED = "AUTO_APPROVED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    FAILED = "FAILED"


class ValidationSeverity(StrEnum):
    ERROR = "ERROR"
    WARNING = "WARNING"


class InvoiceLineItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    description: str = Field(min_length=1)
    quantity: Decimal = Field(gt=0)
    unit_price: Decimal = Field(ge=0)
    total: Decimal = Field(ge=0)


class ExtractedInvoice(BaseModel):
    model_config = ConfigDict(extra="forbid")

    supplier_name: str = Field(default="")
    invoice_number: str = Field(default="")
    invoice_date: date | None = None
    due_date: date | None = None
    currency: str = Field(default="")
    subtotal: Decimal | None = None
    tax: Decimal | None = None
    total: Decimal | None = None
    confidence: float = Field(ge=0, le=1)
    line_items: list[InvoiceLineItem] = Field(default_factory=list)


class ValidationIssue(BaseModel):
    model_config = ConfigDict(extra="forbid")

    field: str
    message: str
    severity: ValidationSeverity = ValidationSeverity.ERROR


class ExtractInvoiceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    document_text: str = Field(min_length=1, alias="documentText")


class ExtractInvoiceResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    invoice: ExtractedInvoice
    status: WorkflowStatus
    validation_errors: list[ValidationIssue] = Field(
        default_factory=list,
        alias="validationErrors",
    )

