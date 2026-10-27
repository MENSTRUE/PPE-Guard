# PPE-Guard Backend — FastAPI + trusted YOLOv8s inference

**Service contract:** read an uploaded image, validate it, run the original Day 21 `.pt` checkpoint, return class-labeled boxes, optional annotated JPEG Base64 and **conservative** PPE-related observations. It does not provide per-person compliance judgements.

## Before → Now → Next

- **Before:** research export `models/ppe_guard_best.pt`, contract of 12 exact classes and held-out report.
- **Now:** `GET /api/v1/health`, `GET /api/v1/models`, `POST /api/v1/predict/image`, FastAPI OpenAPI docs, in-memory validation, lazy checkpoint load, class assertion, serialized inference, tests.
- **Next:** real-model E2E regression fixtures, richer audit-ready errors, authentication, rate limiting, ONNX runtime comparison, profiled concurrency, observability, production hardening.

## Directory ownership

```text
backend/
├── app/main.py                  # FastAPI, CORS, router inclusion
├── app/api/routes/health.py     # API + model file existence
├── app/api/routes/models.py     # Class metadata / checkpoint presence
├── app/api/routes/predict.py    # Multipart prediction endpoint
├── app/core/config.py          # PPE_* runtime settings
├── app/inference/contract.py    # Strict 12-class ontology validator
├── app/inference/loader.py      # Lazy global model instance, lock
├── app/inference/detector.py    # Ultralytics prediction and annotation
├── app/inference/safety_rules.py # No compliance inference
├── app/schemas/detection.py    # Typed responses
├── app/services/image_service.py # MIME, format, dimension checks
├── tests/                      # Pytest + FastAPI TestClient
├── requirements.txt
└── requirements-dev.txt
```

## Installation and execution (PowerShell)

```powershell
cd "D:\porto\100 day\day 21\PPE-Guard\backend"
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe ..\scripts\smoke_model.py
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Run from `backend/`: relative model path `../models/ppe_guard_best.pt` is resolved from the backend root by `config.py`, not your terminal's current directory. `py -3.11` assumes installed Python 3.11. Test via http://127.0.0.1:8000/docs.

### Runtime settings

All values can be overridden by environment variables prefixed `PPE_`, or `backend/.env` (do **not** commit secrets). Defaults currently in `app/core/config.py`:

| Environment key | Default | Meaning |
|---|---|---|
| `PPE_MODEL_PATH` | `../models/ppe_guard_best.pt` | Trusted checkpoint path |
| `PPE_MAX_UPLOAD_MB` | `10` | Input file byte limit, bounded 1–50 MB |
| `PPE_MAX_IMAGE_PIXELS` | `16000000` | Maximum decoded image pixels |
| `PPE_CONFIDENCE` | `0.25` | Detector threshold if query absent |
| `PPE_IOU` | `0.45` | Prediction NMS IoU setting |
| `PPE_IMAGE_SIZE` | `640` | Inference image size |
| `PPE_CORS_ORIGINS` | localhost/127.0.0.1:5173 | CSV list of allowed CORS origins |

`backend/.env` uses `PPE_` keys. Changing confidence is **post-training filtering**, not model recalibration.

## Endpoint contracts

### `GET /api/v1/health`

Returns `status`, `service`, `model_file_present`. Note: `status=ok` confirms the web process responds; it does **not** load weights or guarantee the GPU/model is healthy. Use smoke test/prediction for model readiness.

### `GET /api/v1/models`

Returns `model`, `task`, `classes` (JSON object with string keys `"0"`…`"11"`), `class_count=12`, `checkpoint_available`, `verified_contract`, and `notes`. Real checkpoint mapping is **asserted again on load**.

### `POST /api/v1/predict/image`

**Multipart:** required part `file`. Optional query: `confidence` in [0.01, 1] or absent to use config; `include_annotated` boolean, default false. Image MIME must be `image/jpeg`, `image/png`, or `image/webp` **and** decoder must confirm format. EXIF orientation normalized. A valid 1280×1280 input may be resized for model inference to configured `imgsz=640`; final boxes are mapped to original oriented image pixel coordinates by Ultralytics.

```powershell
curl.exe -X POST "http://127.0.0.1:8000/api/v1/predict/image?confidence=0.25&include_annotated=true" -F "file=@D:\Pictures\ppe.jpg"
```

**Response keys:**

```json
{
  "model": "ppe_guard_best.pt",
  "task": "detect",
  "image": {"width": 1280, "height": 1280, "filename": "ppe.jpg"},
  "detections": [{
    "class_id": 0,
    "class_name": "helmet",
    "confidence": 0.9,
    "bbox": {"x1": 10, "y1": 20, "x2": 200, "y2": 160}
  }],
  "detection_count": 1,
  "inference_ms": 123.4,
  "safety_observations": {
    "ppe_detected": ["helmet"],
    "source_labeled_absences": [],
    "compliance_status": "not_assessed",
    "requires_human_review": false,
    "note": "Source labels are object detections; not worker-level compliance."
  },
  "annotated_image_base64": null
}
```

**Example is schematic, not a measured prediction.** Confidence 1.0 can suppress nearly all boxes. Empty `detections` means no output passed the selected filter on this image; do not interpret as evidence of no PPE.

### Errors

| HTTP | Trigger | Expected action |
|---:|---|---|
| 400 | Empty payload | Upload image bytes |
| 413 | File too large or decoded pixel budget exceeded | Reduce file size / dimensions |
| 415 | Disallowed MIME or decoded format | Use genuine JPEG, PNG or WebP |
| 422 | Unreadable/invalid image; also FastAPI input validation | Verify bytes and query fields |
| 503 | Inference exception caught by endpoint | Inspect server logs and run smoke test |

## Model loading and performance

The model is loaded *lazily*: health endpoint should work without loading it; first prediction loads the trusted PyTorch checkpoint under a lock. The detector serializes calls with a prediction lock because shared Ultralytics instances are not assumed thread-safe. Device selection follows `torch.cuda.is_available()`; without CUDA it explicitly uses CPU. CUDA availability alone is not a speed guarantee. `inference_ms` measures a model prediction call, excluding multipart transfer and Base64 encoding. For realistic production latency, benchmark concurrent end-to-end requests, model cold start, decoded image size and GPU memory pressure. `.onnx` exists but is **not** used by this server.

## Tests and evidence boundary

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe ..\scripts\smoke_model.py
```

The unit tests mock expensive inference where appropriate. A previous dev terminal recorded `9 passed, 1 warning`; future commits must rerun them. Smoke script loads the **real** checkpoint and asserts names/task. Manual Swagger inference previously returned boxes at threshold 0.25. None of this establishes external-site precision or certified PPE compliance.

## Security, privacy and deployment

- Current image validation restricts MIME, format, bytes and pixel count, and processes image in memory. No durable photo archive is implemented.
- PyTorch `.pt` files are executable deserialization surfaces: **load trusted weights only**.
- Auth, rate limiting, TLS, malware scanning, observability, request retention, abuse controls and managed multi-worker model lifecycle are **not implemented**.
- Do not use `--reload` beyond development. Production requires a trusted reverse proxy, TLS, authentication, resource limits and a clear photo-deletion/privacy policy.
- Beware of multiple workers loading separate model copies, memory exhaustion and concurrency assumptions.

## Troubleshooting / FAQ

**The Swagger endpoint returns 200 but no detections.** Check confidence (`1` is nearly impossible), use 0.25 and an in-domain image. The model may miss true objects.

**503 and missing model?** Check `models/ppe_guard_best.pt`; run the smoke test to separate load failures from API problems.

**Why `compliance_status=not_assessed`?** Per-person equipment and worksite policy cannot be inferred from a set of object boxes.

**Why does annotated Base64 look huge?** It contains entire compressed JPEG bytes encoded as JSON string; leave `include_annotated=false` when not needed.

**Why are `head`/`none` not warnings?** These are original dataset class names with no validated compliance semantics.

**What is licensed?** Repository source under root `LICENSE`; dataset, image and checkpoint rights require separate review. See `../models/README.md`, `../reports/README.md`, and `AGENTS.md`.
