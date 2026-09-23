from fastapi import APIRouter, HTTPException, UploadFile, File

from app.db.repositories import create_document
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
    document_type = "INVOICE"
    saved_document = create_document(
        filename=file.filename or "uploaded.pdf",
        content_type=file.content_type,
        document_type=document_type,
        status=extraction["status"],
        text_length=len(document_text),
        text_preview=document_text[:500],
    )

    return DocumentUploadResponse(
        document={
            "id": saved_document.id,
            "filename": saved_document.filename,
            "contentType": file.content_type,
            "documentType": saved_document.document_type,
            "textLength": saved_document.text_length,
            "textPreview": saved_document.text_preview,
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
