from fastapi import APIRouter

from app.core.responses import api_success

router = APIRouter()


@router.get("/health")
def health():
    return api_success({"status": "ok"})
