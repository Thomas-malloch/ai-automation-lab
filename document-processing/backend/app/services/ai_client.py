from typing import Any

import httpx

from app.settings import get_settings


class AiServiceError(Exception):
    """Raised when the AI service cannot extract invoice data."""


async def extract_invoice_from_text(document_text: str) -> dict[str, Any]:
    settings = get_settings()
    endpoint = f"{settings.ai_service_url.rstrip('/')}/extract-invoice"

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                endpoint,
                json={"documentText": document_text},
            )
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise AiServiceError(
            f"AI service returned {exc.response.status_code}: {exc.response.text}"
        ) from exc
    except httpx.HTTPError as exc:
        raise AiServiceError(f"AI service request failed: {exc}") from exc

    return response.json()
