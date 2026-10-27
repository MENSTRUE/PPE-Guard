# AGENTS.md — PPE-Guard Engineering and Research Contract

This file is binding guidance for code-writing assistants and human contributors operating in the repository. Scope: entire repository. More-specific `backend/AGENTS.md` and `frontend/AGENTS.md` supplement it; they cannot weaken its scientific/safety boundaries.

## 1. Mission and refusal-to-invent policy

Build a traceable research prototype for visual PPE object detection and **human review**, not an autonomous occupational safety judge. Never fabricate benchmark metrics, datasets, test success, deployment URLs, runtime performance, image screenshots, camera feeds, or tool execution logs. Label evidence as **recorded, observed, tested, inferred, planned, or unknown**. A successful API request is proof of execution, not proof of classification correctness.

## 2. Source-of-truth precedence

1. Actual currently checked-out source code and tests for behavior.
2. Actual checkpoint `model.names`, task, format and checksum for model identity; `backend/app/inference/contract.py` enforces exact mapping.
3. Immutable evaluation/audit JSON and CSV under `reports/` for historical experiment results.
4. Original training notebook/run/environment/source dataset licensing for research reproduction, if available and verified.
5. The README as a navigational summary; it must not override (1–4).

Do not silently harmonize contradictory reports: investigate and document why `annotation_inventory.json` reports 10 orphan labels while `selection_audit.json` lists 8,451 eligible/selected images.

## 3. Locked detection ontology

```
0 helmet        1 no_helmet      2 vest        3 boots
4 gloves        5 goggles        6 head        7 no_boots
8 no_gloves     9 no_goggle     10 none       11 person
```

No renaming `no_goggle` to `no_goggles` at model interface; no treating `head` as `no_helmet`; no treating `none` as confirmed equipment absence; no treating absent predictions as physical absence. Any ontology change requires separately versioned checkpoint, code, evaluation, docs and migration handling.

## 4. Claim boundaries — never cross

- `compliance_status` must stay `not_assessed` unless a separately validated and reviewed per-person policy assessment capability is added with explicit contract and evaluation.
- A `no_*` detection may be described only as **source-labeled visual indication requiring human review**, not verified misconduct.
- Person detection does not establish identity, employer, employment status, conduct or responsibility.
- A missing `helmet` prediction does not mean missing helmet; an unrelated nearby helmet does not establish worker compliance.
- No claims of production accuracy, legal compliance, safety certification, real-time FPS, zero false negatives or external-site generalization without applicable evaluation.
- Treat score as detector confidence, **not** probability of safety-rule breach.

## 5. Verified research evidence

Dataset: two source annotation schemas; 8,451 selected images, split 6,048/1,556/847; 12 output classes. Held-out JSON: precision 0.6306006972406554, recall 0.5392812479049882, mAP50 0.554925510207925, mAP50:95 0.29186887190219996 on 847 images. Potential near duplicates remain unquantified. The model is YOLOv8s-derived per `final_summary.json`. Do not improve or interpolate metrics without a new experiment and report.

## 6. Engineering rules

- Preserve existing API response keys and types; communicate breaking changes and add contract tests.
- Keep input validation for MIME, decoded format, byte size, pixel count and EXIF orientation.
- Load **trusted** `.pt` only. Do not download or deserialize untrusted model files.
- Maintain guarded model load and inference concurrency semantics unless you implement and test an alternative.
- Do not replace inference with hard-coded detections, screenshots or fake results. Mock only in clearly named unit tests.
- Avoid persisting user imagery or sensitive metadata by default. Never log Base64 images or private filenames without need.
- Validate all externally supplied parameters, paths and filenames. Don't commit credentials, `.env`, `.venv`, `node_modules`, generated `dist`.
- Test exact model class mapping on a real local checkpoint in addition to mocked unit tests before claiming E2E.
- Any frontend use of an annotated Base64 JPEG must preserve correct pixel-to-screen scaling; the server-rendered image is reference when overlay transforms are uncertain.
- Honor user-upload/copyright/privacy policies for example media.

## 7. Working process: Before → Now → Next

**Before:** read the relevant README, code and report data; record what is already verified. **Now:** implement the smallest coherent feature and add tests, docs, failure messages and visible behavior. **Next:** report exact passed and untested checks, commit instructions, known risk, follow-up research needed. Never call a TODO implemented or a mocked test a model quality test.

## 8. Validation checklist

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe ..\scripts\smoke_model.py
cd ..\frontend
npm ci
npm run build
```

For changes to model, preprocessing or boxes: run a real-image end-to-end test and manually inspect annotated output; for research claims: new held-out/source-wise evaluation, leakage audit and manifests. If any check cannot run, say exactly which check and why.

## 9. Ownership and licensing

Repository code is under `LICENSE` (MIT). Do not infer third-party dataset, image, pretrained component or checkpoint redistribution rights from that file. Verify individual licenses before adding media, weights or sharing derived artifacts. Do not claim the deployed or experimental model is certified to any workplace regulation.

## 10. Documentation and PR expectations

Update relevant README(s), API examples, AGENTS constraints, test expectations, and changelog/PR notes when implementation changes. PR description: goal, code paths, source of evidence, tests run with actual outputs, limitations, rollback, licensing effects and Before/Now/Next. Do not overwrite historical `reports/*.json` for cosmetic consistency. New experiments should be versioned rather than replacing prior metrics.
