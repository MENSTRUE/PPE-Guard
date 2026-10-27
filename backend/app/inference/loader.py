import logging
from threading import Lock
from typing import Any
from app.core.config import get_settings
from app.inference.contract import assert_model_contract

log = logging.getLogger(__name__)
_lock = Lock()
_model: Any = None

def get_model():
    global _model
    if _model is not None:
        return _model
    with _lock:
        if _model is None:
            path = get_settings().resolved_model_path
            if not path.is_file():
                raise RuntimeError(f"Checkpoint not found: {path}. Copy your trusted Day 21 best.pt into models/.")
            from ultralytics import YOLO  # defer costly import until inference
            log.info("Loading trusted PPE checkpoint: %s", path)
            candidate = YOLO(str(path))
            assert_model_contract(candidate.names, candidate.task)
            _model = candidate
    return _model
