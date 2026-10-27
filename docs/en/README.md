# PPE-Guard — Technical Research and Operations Guide (English)

**Day 21 · 100 Days of Projects.** PPE-Guard is an AI-assisted image object detector for personal protective equipment (PPE). Its output is **visual source-label evidence requiring human interpretation**; it is not a worker-level compliance system, safety certification, or authorization for automated enforcement.

## Before → Now → Next

**Before:** audit two heterogeneous annotation sources, train a YOLOv8s-based 12-class detector and evaluate a staged 847-image test split. **Now:** versioned JSON evidence, trusted `.pt` and exported `.onnx`, FastAPI inference service, React/Vite UI and a real checkpoint smoke script. **Next:** source-aware evaluation and leakage review, E2E test fixtures, ONNX parity, stronger visual alignment, security/identity controls and deployable release process.

## Source of truth

`reports/final_summary.json` and `selection_audit.json` are authoritative for staged counts; `annotation_inventory.json` for label provenance; `heldout_metrics.json` for historical test scores; `backend/app/inference/contract.py` plus actual checkpoint for strict class mapping; backend/frontend source code for app behavior. Unknown metadata are **not** inferred. Source report identifies 10 orphan labels and incomplete duplicate/domain evaluation; keep those caveats.

## Datasets and methods

Input root in original Kaggle run: `/kaggle/input/datasets/loliwibu/ppe-guard-datset`. Sources: `Hard Hat Workers.v14-raw_headclassonly.yolov8` (original `head` class) and `construction-ppe` (11 source classes). Staged image counts: **8,451**, split **train 6,048 / val 1,556 / test 847**. Mixed annotation policy raises partial-label issues. The audit lists **10 orphan labels**, severe box imbalance, and an unverified risk of near-duplicate leakage. A source-independent dataset license and split-provenance check remain required.

Box counts: `head` 26,424, `person` 2,245, `helmet` 1,734, `vest` 1,618, `boots` 1,597, `gloves` 1,445, `none` 797, `no_gloves` 556, `goggles` 518, `no_helmet` 485, `no_goggle` 411, `no_boots` 115. These are annotation boxes, not images, employees or violations.

## Evaluation and scientific limits

From the recorded held-out report (847 images): **precision 0.6306006972; recall 0.5392812479; mAP@50 0.5549255102; mAP@50:95 0.2918688719**. These are detector metrics, not occupational-safety compliance accuracy. Per-class AP, external-site generalization, worker association, calibration and cross-split perceptual duplicate audit are not established.

## Frozen class IDs and claim boundaries

`0 helmet`; `1 no_helmet`; `2 vest`; `3 boots`; `4 gloves`; `5 goggles`; `6 head`; `7 no_boots`; `8 no_gloves`; `9 no_goggle`; `10 none`; `11 person`.

`head ≠ no_helmet`, `none ≠ all PPE missing`. Missing prediction is not physical absence. Positive and negative source classes can be visually wrong and cannot be assigned to a specific person without a separately validated association method. API field `compliance_status` remains `not_assessed`; `requires_human_review` is set for detected `no_*` source labels. Do not convert detector confidence into breach probability or disciplinary determination.

## Architecture and repository

Browser React/TypeScript/Vite → `/api/v1` proxy → FastAPI validation → lazy-load trusted YOLO `.pt` with exact contract check → pixel bounding boxes and inference timing → safe source-label summary → JSON plus optional Base64 JPEG. UI uses the API, not simulated model output. Files: root `README.md` and `AGENTS.md`; `backend/README.md` / `frontend/README.md`; `models/README.md`, `reports/README.md`, `assets/README.md`, `scripts/README.md`. `.onnx` is an export artifact, **not currently serving**.

## Windows reproducibility runbook

```powershell
cd "D:\porto\100 day\day 21\PPE-Guard\backend"
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe ..\scripts\smoke_model.py
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

In another terminal:

```powershell
cd "D:\porto\100 day\day 21\PPE-Guard\frontend"
npm ci
npm run build
npm run dev
```

Open `http://127.0.0.1:5173` and Swagger `http://127.0.0.1:8000/docs`. `POST /api/v1/predict/image` accepts JPEG/PNG/WebP multipart `file` and query `confidence` (0.01–1.0), `include_annotated` (Boolean); response includes `detections`, `inference_ms`, `safety_observations`, `annotated_image_base64`. Threshold 1.0 is generally too restrictive; start at 0.25. Local backend unit tests historically passed 9 cases but some use mocked inference; rerun on current version and inspect at least one real-image prediction.

## Reproducibility and security

Inference can run with repo checkpoint and compatible dependencies. **Training replication** additionally requires pinned original dataset source and exact run notebook, seed, hyperparameters, environment, train/validation checkpoint-selection logic and model hash. Do not report it as fully reproduced solely because the `.pt` runs.

Current API validates declared/decoded image formats, payload and pixel limits; processes uploads in memory. It lacks deployment-ready authorization, rate limiting, TLS termination, audit retention controls and independent cybersecurity review. A `.pt` checkpoint must be trusted due to deserialization risks; do not load arbitrary uploads. The developer UI's Vite proxy is not a production security boundary.

## Testing and deployment gates

Before release: `pytest`; smoke actual `.pt`; `npm ci` + build; manual API + UI inspection with in-domain examples and aspect ratios; corrupt/large upload rejection; empty detections; `no_*` review; image privacy review. For public deployment also add TLS, identity/access control, structured observability, retention and infrastructure sizing; validate latency at concurrent load and safe model provenance. There is no verified live hosted URL or production deployment pipeline in this repository.

## Roadmap, troubleshooting, FAQ

**P0:** E2E regression and documentation. **P1:** resolve orphan labels, audit duplicates, per-class/source-wise accuracy, ONNX comparison, overlay correctness and independent-site tests. **P2:** secured deployment, immutable model manifests, telemetry and privacy. **P3:** separately validated video/person–PPE association.

**No detections?** Confirm confidence=0.25, image domain and model quality. **HTTP 503?** Check model path/contract and server logs. **Missing module?** Use correct virtual environment. **Frontend disconnected?** Check backend port and proxy/base URL. **Shifted boxes?** Validate contain/letterbox scaling against server-annotated image. **Is `none` proof of unsafe work?** No. **Is ONNX active?** No. **Does MIT cover third-party media and weights?** Not automatically.

## License / provenance

The root repository has an MIT `LICENSE` for rights-controlled software. Third-party datasets, uploaded photos, pretrained dependencies and derived weights may have separate requirements. Audit actual upstream licenses and distribution rights before publishing or selling. Follow `../../AGENTS.md` and keep every claim tied to code or evidence.
