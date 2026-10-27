# Frontend AGENTS — truthful inspection UX

Follow `../AGENTS.md` and `README.md`.

- Read `src/lib/types.ts`, `src/lib/api.ts`, `src/App.tsx` and actual backend schema before editing UI. Do not invent endpoints or fabricate source data.
- No mocked positive prediction in shipped inspection screens. Empty detection is a valid model response; retain it honestly.
- Preserve exact 12-class names. `none` and `head` cannot become “unsafe” badges or compliance findings. A `no_*` source label prompts human review only.
- Display confidence as detector score, not certified likelihood of K3 violation. Do not call the whole scene safe just because there is no `no_*` box.
- Use backend `annotated_image_base64` as reference. If drawing interactive boxes, test letterboxing and orientation; incorrect overlay is a UI bug.
- Preserve privacy. Do not store images or Base64 in localStorage, analytics or error trackers without user authorization and data policy.
- Never expose secrets via `VITE_*` env vars. Use explicit API URLs, safe abort/cancellation and clear error states.
- Prefer accessible inputs, focus states, descriptive labels, keyboard operation, mobile responsiveness and reduced-motion compatibility.
- Test `npm ci`, `npm run build`, upload at 0.25 threshold, API disconnected state, zero detections, `no_*` class, exports and all image aspect ratios.
- Document actual test results and changed UX in frontend README; never claim a screenshot/visual test was performed without running it.
