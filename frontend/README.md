# PPE Guard — Phase 3 Frontend

React + TypeScript + Vite inspection console for the existing Day 21 FastAPI backend.

## Windows setup

From the repository root:

```powershell
cd "D:\porto\100 day\day 21\PPE-Guard\frontend"
npm install
npm run dev
```

Open http://127.0.0.1:5173 . FastAPI must run separately at http://127.0.0.1:8000:

```powershell
cd "D:\porto\100 day\day 21\PPE-Guard\backend"
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Vite proxies `/api/v1` to backend on port 8000. The UI uses the real YOLO checkpoint through the backend; it has no fake results, no mock API, and no cloud dependencies. The UI supports image upload (JPG/PNG/WEBP, 10 MB max), detection confidence, annotated image preview, class filtering, exports, model status, and human-review observations.

**Important:** Bounding boxes with selected-class filtering are rendered on a contain-fitted image; overlay coordinate mapping may be inaccurate for letterboxed photos. Full annotated result from backend is the canonical visualization. This app provides decision support, not workplace safety certification.

`npm run build` runs TypeScript checks and bundles production files into `dist/`.
