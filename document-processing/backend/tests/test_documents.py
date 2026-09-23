from types import SimpleNamespace
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app
from app.services.ai_client import AiServiceError
from app.services.pdf import PdfExtractionError


client = TestClient(app)


def test_upload_rejects_non_pdf_content_type() -> None:
    response = client.post(
        "/documents",
        files={"file": ("invoice.txt", b"not a pdf", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Only PDF uploads are supported."


def test_upload_rejects_invalid_pdf_bytes() -> None:
    response = client.post(
        "/documents",
        files={"file": ("invoice.pdf", b"GIF89a", "application/pdf")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Uploaded file is not a valid PDF."


def test_upload_returns_422_when_pdf_has_no_text(monkeypatch) -> None:
    def fake_extract_text_from_pdf(file_bytes: bytes) -> str:
        raise PdfExtractionError("No text could be extracted from PDF.")

    monkeypatch.setattr(
        "app.routes.documents.extract_text_from_pdf",
        fake_extract_text_from_pdf,
    )

    response = client.post(
        "/documents",
        files={"file": ("invoice.pdf", b"%PDF-1.3", "application/pdf")},
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "No text could be extracted from PDF."


def test_upload_persists_successful_invoice_extraction(monkeypatch) -> None:
    document_id = uuid4()
    persisted: dict = {}

    def fake_extract_text_from_pdf(file_bytes: bytes) -> str:
        return "Example invoice text"

    async def fake_extract_invoice_from_text(document_text: str) -> dict:
        return {
            "invoice": {
                "supplier_name": "Example Ltd",
                "invoice_number": "INV-1004",
                "invoice_date": "2026-09-01",
                "due_date": "2026-09-15",
                "currency": "NZD",
                "subtotal": "372.61",
                "tax": "55.89",
                "total": "428.50",
                "confidence": 0.95,
                "line_items": [
                    {
                        "description": "Consulting services",
                        "quantity": "1",
                        "unit_price": "372.61",
                        "total": "372.61",
                    }
                ],
            },
            "status": "AUTO_APPROVED",
            "validationErrors": [],
        }

    def fake_create_processed_document(**kwargs):
        persisted.update(kwargs)
        return SimpleNamespace(
            id=document_id,
            filename=kwargs["filename"],
            document_type=kwargs["document_type"],
            text_length=kwargs["text_length"],
            text_preview=kwargs["text_preview"],
        )

    monkeypatch.setattr(
        "app.routes.documents.extract_text_from_pdf",
        fake_extract_text_from_pdf,
    )
    monkeypatch.setattr(
        "app.routes.documents.extract_invoice_from_text",
        fake_extract_invoice_from_text,
    )
    monkeypatch.setattr(
        "app.routes.documents.create_processed_document",
        fake_create_processed_document,
    )

    response = client.post(
        "/documents",
        files={"file": ("invoice.pdf", b"%PDF-1.3", "application/pdf")},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["document"]["id"] == str(document_id)
    assert body["processing"]["status"] == "AUTO_APPROVED"
    assert body["extraction"]["data"]["invoice_number"] == "INV-1004"
    assert persisted["status"] == "AUTO_APPROVED"
    assert persisted["invoice_data"]["supplier_name"] == "Example Ltd"


def test_upload_persists_failed_document_when_ai_service_fails(monkeypatch) -> None:
    persisted: dict = {}

    def fake_extract_text_from_pdf(file_bytes: bytes) -> str:
        return "Example invoice text"

    async def fake_extract_invoice_from_text(document_text: str) -> dict:
        raise AiServiceError("AI service request failed")

    def fake_create_failed_document(**kwargs):
        persisted.update(kwargs)
        return SimpleNamespace()

    monkeypatch.setattr(
        "app.routes.documents.extract_text_from_pdf",
        fake_extract_text_from_pdf,
    )
    monkeypatch.setattr(
        "app.routes.documents.extract_invoice_from_text",
        fake_extract_invoice_from_text,
    )
    monkeypatch.setattr(
        "app.routes.documents.create_failed_document",
        fake_create_failed_document,
    )

    response = client.post(
        "/documents",
        files={"file": ("invoice.pdf", b"%PDF-1.3", "application/pdf")},
    )

    assert response.status_code == 502
    assert persisted["filename"] == "invoice.pdf"
    assert persisted["error_message"] == "AI service request failed"


def test_get_document_returns_404_for_missing_id(monkeypatch) -> None:
    monkeypatch.setattr("app.routes.documents.get_document_result", lambda document_id: None)

    response = client.get(f"/documents/{uuid4()}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found."
