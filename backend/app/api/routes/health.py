from fastapi import APIRouter
from app.core.config import get_settings

router=APIRouter(tags=["health"])

@router.get("/health")
def health():
    settings=get_settings()
    return {"status":"ok", "service":"PPE Guard API", "model_file_present": settings.resolved_model_path.is_file()}
