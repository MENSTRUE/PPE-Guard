# Scripts — checks, tooling and release evidence

## Current files

- `smoke_model.py` — invokes the backend lazy loader against the **actual trusted** `models/ppe_guard_best.pt`, prints model class/type/task and class map, and asserts checkpoint contract via `get_model()`.

This directory **does not** presently contain a training pipeline, benchmark harness, dataset re-split tool or export validation script. Do not list those as implemented.

## Before → Now → Next

Before: direct Ultralytics checkpoint inspection established `detect` task and 12 classes. Now: repeatable model-load smoke script accompanies mocked API tests. Next: add automated evaluated image fixtures, SHA-256 checkpoint manifest, ONNX/PT parity checks, split duplicate audit and explicit reproducibility environment exporter.

## Usage (PowerShell)

```powershell
cd "D:\porto\100 day\day 21\PPE-Guard\backend"
.\.venv\Scripts\python.exe ..\scripts\smoke_model.py
```

**Important:** check that the opening module docstring uses balanced triple quotes (`"""`) if running a stale copy. The latest repository script closes it properly. Run with backend virtual environment to ensure dependencies are available.

Expected conceptual evidence: model type YOLO, task `detect`, names dictionary with 12 exact classes, and `CHECKPOINT CONTRACT: PASS`. No benchmark performance is computed by this script, and passing does not prove uploaded images are classified correctly.

## Add-on script standards

- Deterministic inputs or recorded random seeds; source paths through repo-relative config; no hardcoded private directories.
- Read-only inspection by default; require explicit flag for destructive writes.
- Machine-readable JSON/CSV plus concise human report, versioned with timestamp/run and dependency versions.
- Do not overwrite `reports/heldout_metrics.json` or other historical audit output.
- Check image rights before exporting demos; avoid logging secrets or identifiable photos.
- Test failures with nonzero exit status; document supported Python/env and purpose in this README.

## Troubleshooting and licensing

If `ModuleNotFoundError`, install `backend/requirements-dev.txt` in `.venv`. If checkpoint missing, verify `models/ppe_guard_best.pt`. If class mismatch, do not suppress assertion; check weights or create a separately versioned model. Scripts are MIT-covered repository software subject to root `LICENSE`; third-party model/data rights remain separate.
