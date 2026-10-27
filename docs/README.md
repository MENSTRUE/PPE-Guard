# Documentation hub — PPE-Guard

This directory organizes research, product, and operational knowledge without creating imaginary implementation evidence. Root [`README.md`](../README.md) is the high-level entry point. Root [`AGENTS.md`](../AGENTS.md) is binding for contributors and coding assistants.

## Language guides

| Guide | Audience | Coverage |
|---|---|---|
| [`id/README.md`](id/README.md) | Indonesian researchers, judges, contributors | Project summary, dataset, metrics, limitations, runbook, claim boundaries |
| [`en/README.md`](en/README.md) | International reviewers/developers | Technical status, evidence, reproduction, limitations, operations |

## Core reference documents elsewhere

- [`../backend/README.md`](../backend/README.md): API schemas, PowerShell, validation, errors, tests and deployment caveats.
- [`../frontend/README.md`](../frontend/README.md): React/Vite setup, UI, proxy, exports, rendering and responsive testing.
- [`../models/README.md`](../models/README.md): trusted checkpoint, ONNX limits, classes and model license caveats.
- [`../reports/README.md`](../reports/README.md): 8,451-image audit, 847-image held-out evaluation and integrity questions.
- [`../assets/README.md`](../assets/README.md): qualitative media provenance, attribution, screenshots and plots.
- [`../scripts/README.md`](../scripts/README.md): model smoke test and future script standards.

## Before → Now → Next

**Before:** experiment produced reports, checkpoint and a sample annotation. **Now:** backend/frontend and detailed README+AGENTS source map exist. **Next:** a verified, versioned full training protocol; dataset-license inventory; external evaluation; deployment/runbook security review; an issue-linked documentation change process.

## Evidence classification

**Recorded:** values exactly present in repository JSON. **Observed:** user-run terminal/Swagger outputs from development; separate from repeatable test suite. **Implemented:** source code present, even if not browser-tested here. **Tested:** exact command and result captured. **Planned:** roadmap only. **Unknown:** source not provided or not evaluated. Every quantitative project claim should state category, date/run if available, dataset split and evidence file.

## Maintainer rule

No new metrics invented to decorate a README. No new license assumptions. No screenshots represented as actual before capture. Update all relevant English/Indonesian docs when change affects API contract or safety interpretation. Claims are intentionally limited to **object detections + human-review observations**, never individual PPE-rule compliance.
