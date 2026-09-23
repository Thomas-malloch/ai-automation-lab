from fastapi import FastAPI
from app.routes.documents import router as documents_router

app = FastAPI(title="Document Processing Backend")

app.include_router(documents_router)


@app.get("/health")
def health():
    return {"status": "ok"}

