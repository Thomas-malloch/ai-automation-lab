from io import BytesIO

from pypdf import PdfReader


class PdfExtractionError(Exception):
    """Raised when PDF text extraction fails"""


def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        reader = PdfReader(BytesIO(file_bytes))
    except Exception as exc:
        raise PdfExtractionError("Could not read PDF file.") from exc

    page_text: list[str] = []

    for page in reader.pages:
        text = page.extract_text() or ""
        if text.strip():
            page_text.append(text.strip())

    extracted_text = "\n\n".join(page_text).strip()

    if not extracted_text:
        raise PdfExtractionError(
            "No text could be extracted from PDF. The file may be scanned or image-only."
        )

    return extracted_text

