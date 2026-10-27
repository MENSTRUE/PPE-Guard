# Day 21 — Phase 3 Frontend delivery

Extract the **contents** of this delivery into the root of `PPE-Guard`. The package contains only `frontend/` and this README; it does **not** change your model, backend, or reports.

See `frontend/README.md` for Windows PowerShell commands.

## Safety limitations

- `no_helmet`, `no_gloves`, `no_boots`, `no_goggle` are **source labels**, not confirmed violations.
- `head`, `person`, and `none` are not compliance outcomes.
- Confidence threshold affects how many bounding boxes are returned.
- No person-to-PPE association is implemented.
- Backend must be running for analysis; blank state is not made-up predictions.
