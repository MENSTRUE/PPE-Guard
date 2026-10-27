# PPE-Guard Frontend — React / TypeScript inspection console

**Scope:** image-based visual inference client for existing FastAPI backend. Uses actual backend response; does not compute model predictions in the browser and does not generate mock detections as live inspection results.

## Before → Now → Next

**Before:** a manually tested Swagger endpoint returned labeled bounding boxes and optionally Base64 JPEG. **Now:** source tree provides an overview, image inspection controls, model information and export-related UI. **Next:** run local build/browser E2E tests, fix any contain/letterbox overlay discrepancies, improve accessibility and usability, add secure deployment and validated report workflows.

## Source layout

```text
frontend/
├── README.md
├── AGENTS.md
├── .env.example
├── .gitignore
├── index.html
├── package.json
├── package-lock.json
├── tsconfig.json
├── vite.config.ts
├── public/brand.svg
└── src/
    ├── main.tsx            # React bootstrap
    ├── App.tsx             # Single-file page/control implementation
    ├── lib/api.ts          # Fetch + error parsing
    ├── lib/types.ts        # DTOs mirrored from Pydantic
    ├── lib/export.ts       # Client-side export helpers
    └── styles/global.css  # Responsive styles
```

**Important:** old empty scaffolding folders may remain from initialization. Source of truth is actual `src/App.tsx` and `src/lib/`, not hypothetical `components/` folders.

## Developer setup

Requirements: Node.js/npm compatible with Vite 6; backend running on port 8000; YOLO checkpoint available to backend.

```powershell
cd "D:\porto\100 day\day 21\PPE-Guard\backend"
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

In a second terminal:

```powershell
cd "D:\porto\100 day\day 21\PPE-Guard\frontend"
npm ci
npm run build
npm run dev
```

Open **http://127.0.0.1:5173**. Vite proxies `/api` to `http://127.0.0.1:8000` as specified in `vite.config.ts`. `npm run build` invokes TypeScript build then Vite; `npm run typecheck` is also available. Do not report build passing until run on your current commit.

## Configuration and API contract

In `src/lib/api.ts`, `VITE_API_BASE_URL` defaults to `/api/v1`. The frontend issues:

- `GET ${BASE}/health` — status indicator; remember healthy HTTP is not model readiness.
- `GET ${BASE}/models` — model metadata and 12 labels.
- `POST ${BASE}/predict/image?confidence=<number>&include_annotated=true` — multipart `file` and request abort signal.

For same-origin production deployment, proxy `/api/` to the backend and keep `VITE_API_BASE_URL=/api/v1`. For different origins, configure full accessible URL and backend `PPE_CORS_ORIGINS` with strictly allowed origins. Vite `VITE_*` variables are **client-visible**, never put secrets in them. Check `.env.example` for project-specific reference.

## User workflow

1. Start backend and frontend, open Overview to verify API connectivity.
2. Navigate to AI Inspection, supply real JPEG/PNG/WebP (frontend UI limit is 10 MB), adjust confidence default 0.25.
3. Submit image; wait for real backend results. An empty response is possible and should not become a fabricated positive.
4. Inspect `detection_count`, each source class/confidence, `safety_observations` and server-annotated image.
5. Export JSON and/or annotated image where the UI offers them; verify output content against API, keep personal photos private.
6. Verify model info screen displays the 12 class names accurately and explains limitations.

## Image rendering / coordinate risk

Backend bounding boxes are pixel coordinates on normalized original RGB input. When displaying a browser image with `object-fit: contain`, the image can have letterbox margins, so mapping coordinates to CSS `clientWidth/clientHeight` without offsets can cause shifted boxes. The backend's `annotated_image_base64` is the reference result for current visual inspection. Any interactive filtered overlay must compute `scale = min(containerWidth/imageWidth, containerHeight/imageHeight)`, centered offsets, plus CSS/DPR behavior, and be visually tested for portrait, landscape and square images. Do not describe a visually displaced overlay as a model error without verifying backend JSON.

## Claim boundaries and quality

- UI must distinguish `helmet` positive class from source-defined `no_helmet` observation. Likewise `no_boots`, `no_gloves`, `no_goggle`.
- `person`, `head`, `none` are not compliance verdicts, and the model cannot attribute equipment to a particular person.
- `compliance_status` is `not_assessed`, not “safe”, “unsafe”, “compliant” or “violator”.
- Do not label aggregated boxes as “workers protected” or claim safety-law certification.
- Exported data is an unvalidated model observation: provide human-review disclaimer where results may be shared.

## UI testing checklist

| Case | Expected |
|---|---|
| FastAPI offline | Clear connection/error state; no invented detections |
| Valid upload at 0.25 | Model response and corresponding preview/labels |
| Unsupported/corrupt image | Explain rejection without crashing |
| Confidence changed | New request uses selected threshold |
| Square, wide, tall photos | Annotation/overlay aligned to rendered pixels |
| Source label `none` | Not presented as confirmed no-PPE event |
| `no_*` label | Human-review indicator, not verified infraction |
| Empty prediction | Zero detections, unknown safety status |
| JSON export | Structured fields agree with API response |
| Long Base64 / large photo | UI remains usable, no accidental logs |
| Keyboard/screen reader/mobile | Controls accessible and responsive |
| Production build | `npm ci && npm run build` completes on target machine |

Current code has no confirmed browser automation suite or screenshot visual regression in this repository; these are acceptance goals, not existing checks.

## Build and deployment

`npm run build` creates `dist/`; serve it from a static host/CDN with correct SPA fallback and API reverse proxy. Do not publish a Vite dev server as production. Enforce security headers and HTTPS in hosting layer. Build-time environment values must match the target API. No production hosting URL or deployment CI pipeline is verified.

## Troubleshooting / FAQ

**Disconnected:** check backend `http://127.0.0.1:8000/api/v1/health`, proxy `/api`, and `VITE_API_BASE_URL`.

**CORS error:** same-origin proxy is simplest in development; direct cross-origin calls require correct `PPE_CORS_ORIGINS` and permitted origin.

**No boxes:** threshold, model misses, image domain; do not assume working backend means guaranteed detection.

**Annotated image is missing:** endpoint needs `include_annotated=true`; React API wrapper currently requests it.

**Big JSON:** Base64 is embedded JPEG; avoid displaying raw Base64 in normal UI.

**Can it do live webcam/video?** Not with the documented endpoint; image upload only. Adding streaming needs new latency/privacy/validation work.

**Where is frontend license?** Root `LICENSE` for repository code; uploaded images and model weights are separately governed. See root README and `AGENTS.md`.
