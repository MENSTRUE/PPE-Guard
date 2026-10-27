from pydantic import BaseModel, Field

class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float

class Detection(BaseModel):
    class_id: int
    class_name: str
    confidence: float = Field(ge=0, le=1)
    bbox: BoundingBox

class SafetyObservations(BaseModel):
    ppe_detected: list[str]
    source_labeled_absences: list[str]
    compliance_status: str
    requires_human_review: bool
    note: str

class ImageInfo(BaseModel):
    width: int
    height: int
    filename: str

class PredictionResponse(BaseModel):
    model: str
    task: str
    image: ImageInfo
    detections: list[Detection]
    detection_count: int
    inference_ms: float
    safety_observations: SafetyObservations
    annotated_image_base64: str | None = None
