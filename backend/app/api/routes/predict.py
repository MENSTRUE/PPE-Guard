import logging
from pathlib import Path
from fastapi import APIRouter, File, UploadFile, Query, HTTPException
from app.core.config import get_settings
from app.services.image_service import read_verified_image
from app.inference.detector import predict_image
from app.schemas.detection import PredictionResponse

log=logging.getLogger(__name__)
router=APIRouter(tags=["prediction"])

@router.post("/predict/image", response_model=PredictionResponse)
async def predict_image_endpoint(
    file: UploadFile = File(...),
    confidence: float | None = Query(default=None,ge=0.01,le=1),
    include_annotated: bool = Query(default=False),
):
    settings=get_settings()
    image=await read_verified_image(file)
    try:
        prediction=predict_image(image,conf=confidence if confidence is not None else settings.confidence,
                                 iou=settings.iou,imgsz=settings.image_size,include_annotated=include_annotated)
    except Exception as exc:
        log.exception("Inference failed")
        raise HTTPException(status_code=503,detail="Inference unavailable; check server logs and model checkpoint") from exc
    # only a filename, never accept uploaded client paths
    filename=Path((file.filename or "upload.jpg").replace(chr(92), "/")).name[:140]
    prediction["image"]={"width":image.width,"height":image.height,"filename":filename}
    return prediction
