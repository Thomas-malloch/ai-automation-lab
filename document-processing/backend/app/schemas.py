from typing import Any
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DocumentSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: UUID
    filename: str
    content_type: str = Field(alias="contentType")
    document_type: str = Field(alias="documentType")
    text_length: int = Field(alias="textLength")
    text_preview: str = Field(alias="textPreview")


class ProcessingSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: str
    validation_errors: list[dict[str, Any]] = Field(
        default_factory=list,
        alias="validationErrors",
    )


class ExtractionResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: str
    data: dict[str, Any]


class DocumentUploadResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    document: DocumentSummary
    processing: ProcessingSummary
    extraction: ExtractionResult


class DocumentListItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: UUID
    filename: str
    document_type: str = Field(alias="documentType")
    status: str
    text_length: int = Field(alias="textLength")
    created_at: datetime = Field(alias="createdAt")


class DocumentListResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    documents: list[DocumentListItem]
