from fastapi import APIRouter
from app.core.config import get_settings
from app.inference.contract import CLASS_NAMES

router=APIRouter(tags=["models"])

@router.get("/models")
def models():
    settings=get_settings()
    return {"model":"ppe_guard_best.pt", "task":"detect", "classes":dict(enumerate(CLASS_NAMES)),
            "class_count":len(CLASS_NAMES), "checkpoint_available":settings.resolved_model_path.is_file(),
            "verified_contract":"Day 21 checkpoint class mapping; validated again on model load",
            "notes":["head is NOT no_helmet", "none is NOT a compliance result", "No per-person PPE association"]}
