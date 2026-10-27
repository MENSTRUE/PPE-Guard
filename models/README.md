# Models — trusted Day 21 PPE detector artifacts

## Files and status

| File | Purpose | Current serving status |
|---|---|---|
| `ppe_guard_best.pt` | PyTorch/Ultralytics YOLOv8s-derived trained checkpoint | **Used by FastAPI** |
| `ppe_guard_best.onnx` | ONNX export for potential portable inference | **Not used by current API; parity unverified** |

The file exists in GitHub, but existence does not prove provenance, byte-level consistency with the original Kaggle run, safety to deserialize, third-party redistribution rights, or ONNX numerical equivalence. Before releases, record cryptographic SHA-256, file size, creation/export commands, training run ID, exact Ultralytics/PyTorch/ONNX versions, opset, input/output tensor signature, and hardware benchmark conditions.

## Before → Now → Next

**Before:** YOLOv8s-trained experiment saved a selected `.pt` and export `.onnx`. **Now:** FastAPI lazy-loads `../models/ppe_guard_best.pt`, verifies the 12-class mapping and runs image inference. **Next:** reproducible checkpoint/manifest signing, clean PT/ONNX parity tests, approved redistribution route and optimized device benchmarking.

## Frozen 12-class contract

```text
0 helmet       1 no_helmet     2 vest        3 boots
4 gloves       5 goggles       6 head        7 no_boots
8 no_gloves    9 no_goggle    10 none       11 person
```

Runtime contract lives in `../backend/app/inference/contract.py`; on model load the actual `model.names` and `model.task=detect` are asserted. **Do not reorder IDs** without retraining/re-exporting and versioning the serving API. `none`/`head` are not evidence of confirmed missing PPE.

## Local verification

```powershell
cd "D:\porto\100 day\day 21\PPE-Guard\backend"
.\.venv\Scripts\python.exe ..\scripts\smoke_model.py
```

Or use:

```powershell
.\.venv\Scripts\python.exe -c "from ultralytics import YOLO; m=YOLO('../models/ppe_guard_best.pt'); print(m.task, m.names)"
```

Only run checkpoints from trusted sources; PyTorch deserialization can execute malicious code. A successful smoke load checks identity and labels, **not** test accuracy.

## Research quality

Recorded held-out 847-image test: precision **63.06%**, recall **53.93%**, mAP50 **55.49%**, mAP50:95 **29.19%**. Numbers originate from `../reports/heldout_metrics.json`; not comparative ONNX scores and not production compliance accuracy. Data imbalances and label ontology mismatch are major caveats.

## Model distribution and license

Root MIT `LICENSE` covers repository-owned software to the extent rights are held. It does **not** prove license clearance for training datasets, pretrained model implementation or weights. The YOLO/Ultralytics dependency has its own terms; verify the exact installed version and applicable license, and each dataset's upstream terms before model redistribution or commercial use. Publicly checked-in weights are not a substitute for the provenance/license check. Consider Git LFS or release artifacts for future binaries without retroactively rewriting history without coordination.

## Troubleshooting / FAQ

**Missing model?** Confirm checkpoint filename/path; override `PPE_MODEL_PATH` relative to `backend/` or use absolute path.

**Different class names?** Stop inference. Do not silently map mismatched classes; find correct checkpoint or version the new model.

**Can ONNX replace `.pt` directly?** Not automatically: validate output shape, normalized boxes, NMS, class ordering and score tolerance on a fixed evaluation set before changing loader.

**Are weights safe?** Only if trusted provenance and integrity are established. Do not load strangers' `.pt` uploads.
