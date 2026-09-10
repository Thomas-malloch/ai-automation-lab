from fastapi import FastAPI, HTTPException

from app.extraction import ExtractionError, extract_invoice
from app.schemas import ExtractInvoiceRequest, ExtractInvoiceResponse
from app.validation import validate_invoice

app = FastAPI(title="Document Processing AI Service", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/extract-invoice", response_model=ExtractInvoiceResponse)
def extract_invoice_endpoint(request: ExtractInvoiceRequest) -> ExtractInvoiceResponse:
    try:
        invoice = extract_invoice(request.document_text)
    except ExtractionError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    status, validation_errors = validate_invoice(invoice)

    return ExtractInvoiceResponse(
        invoice=invoice,
        status=status,
        validationErrors=validation_errors,
    )
