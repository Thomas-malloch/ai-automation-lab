from uuid import uuid4

from fastapi import APIRouter, HTTPException, UploadFile, File

from app.schemas import DocumentUploadResponse
from app.services.ai_client import AiServiceError, extract_invoice_from_text
from app.services.pdf import PdfExtractionError, extract_text_from_pdf


router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)) -> DocumentUploadResponse:
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF uploads are supported.")

    file_bytes = await file.read()

    try:
        document_text = extract_text_from_pdf(file_bytes)
    except PdfExtractionError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    try:
        extraction = await extract_invoice_from_text(document_text)
    except AiServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    invoice = extraction["invoice"]

    return DocumentUploadResponse(
        document={
            "id": uuid4(),
            "filename": file.filename or "uploaded.pdf",
            "contentType": file.content_type,
            "documentType": "INVOICE",
            "textLength": len(document_text),
            "textPreview": document_text[:500],
        },
        processing={
            "status": extraction["status"],
            "validationErrors": extraction.get("validationErrors", []),
        },
        extraction={
            "type": "INVOICE",
            "data": invoice,
        },
    )
