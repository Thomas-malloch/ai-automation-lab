from app.db.models import Document
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