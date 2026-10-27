# Backend AGENTS — inference and API rules

Read `../AGENTS.md` and `README.md` first. This file applies to `backend/` and supplements global constraints.

1. **Never replace real inference** with generated detections. Mock `predict_image` only in tests explicitly labeled mock.
2. Preserve routes `/api/v1/health`, `/api/v1/models`, `/api/v1/predict/image`, and schema in `app/schemas/detection.py` unless a documented API version change is planned.
3. Preserve exact `contract.CLASS_NAMES` order (12 labels) and checkpoint validation; a model change requires versioned research evidence and explicit migration.
4. `head` and `none` are not unsafe/negative PPE classifications. Never infer compliant/noncompliant worker state from box presence/absence. Keep `compliance_status=not_assessed` unless independent methodology and tests are approved.
5. Validate both declared MIME and decoded format; bound bytes and pixels; normalize EXIF. Return 4xx for input errors, safe 503 for backend inference failures; log server details without user image bytes.
6. Model load is lazy and synchronized; inference is serialized. Do not loosen locking without concurrency stress tests and a thread-safety plan.
7. Keep `.pt` load restricted to trusted checkpoint paths. Avoid deserializing user-supplied model files. Do not commit API keys or identifiable sample uploads.
8. Dependencies should be pinned/locked for releases and hardware reproducibility; do not casually change torchvision/torch/CUDA builds.
9. Test with `python -m pytest -q`, real checkpoint `python ../scripts/smoke_model.py`, and a manually reviewed image request. Report tests actually run; `pytest` mocks do not demonstrate real accuracy.
10. A backend change must update backend README, root README if user-visible, interface types in `frontend/src/lib/types.ts`, and relevant integration tests. Report **Before → Now → Next** and unresolved limitations.
