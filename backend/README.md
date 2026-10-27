# PPE Guard — Backend inference

Real YOLO checkpoint loaded **on first prediction** from `../models/ppe_guard_best.pt`. `GET /health` works before loading weights. Model contract is checked against the actual 12 class labels on load. The test suite mocks model computation to verify API behavior; a separate real-checkpoint smoke test is provided.

## Windows PowerShell quick start

```powershell
cd "D:\porto\100 day\day 21\PPE-Guard\backend"
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Python 3.11 or 3.12 recommended if available; modern dependency versions may also work on other Python versions. For CUDA inferencing, install a compatible PyTorch build as documented for your GPU and driver. The default project installs basic packages but does not force an incompatible CUDA wheel.

Swagger: <http://127.0.0.1:8000/docs>
Health: <http://127.0.0.1:8000/api/v1/health>
Models: <http://127.0.0.1:8000/api/v1/models>

Predict with image upload:

```powershell
curl.exe -X POST "http://127.0.0.1:8000/api/v1/predict/image?confidence=0.25&include_annotated=true" -F "file=@D:\Pictures\ppe_test.jpg"
```

A successful response contains `detections[]` with raw pixels `bbox`, `class_id`, `class_name`, `confidence`, `inference_ms`, plus `safety_observations`. When requested, `annotated_image_base64` contains Base64 JPEG without a data URL prefix. Your React app can prepend `data:image/jpeg;base64,` to display it. `safety_observations.compliance_status` always remains `not_assessed` because bounding-box detection alone cannot associate all PPE with a particular person.

**Safety / privacy:** uploaded images are processed in memory and not saved by this API; restrict access to trusted users before deployment. Only load trusted .pt checkpoint; PyTorch model deserialization can execute code. Reject nonimages, large payloads and oversized images. Real deployment should add authentication, request rate limiting, malware scanning and monitoring.

## Model contract

`helmet`, `no_helmet`, `vest`, `boots`, `gloves`, `goggles`, `head`, `no_boots`, `no_gloves`, `no_goggle`, `none`, `person`. `head` is not `no_helmet`. `none` is a dataset label, not a compliance outcome. No person-PPE ownership is asserted.

## Tests and known limits

Tests: validation, metadata mapping, safe interpretation and mocked upload inference. Real model smoke: `python ../scripts/smoke_model.py`. Model load and ONNX equivalence were **not** tested in this delivered environment because the user's checkpoint is on their own laptop. Precision, recall and mAP remain research reports; API inference does not itself establish production compliance accuracy.
