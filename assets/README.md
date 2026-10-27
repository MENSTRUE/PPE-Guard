# Assets — diagrams, demos, and auditable screenshots

`assets/` is a **presentation layer**, not a second source of truth for research metrics. Always trace generated figures to source model, image, run ID, confidence threshold and licensing.

## Inventory

```text
assets/
├── README.md
├── examples/
│   └── ppe_detection_samples.png   # Copy of a qualitative research output
├── diagrams/
│   └── .gitkeep                     # Diagram files may be added later
└── screenshots/
    └── .gitkeep                     # UI screenshots may be added later
```

`assets/examples/ppe_detection_samples.png` was copied from `reports/annotated_samples.png` during project setup. It is **qualitative evidence only**; not proof of a benchmark, model training replication or legal PPE compliance. The underlying original image licensing, identity/privacy, and redistribution rights must be checked before externally reusing it. Avoid adding random stock images without permission and provenance.

## Before → Now → Next

Before: notebook generated `reports/annotated_samples.png`. Now: example copied to `assets/examples`. Next: add manually reviewed success/error galleries, properly labeled UI screenshots, and generated architecture diagrams with provenance and reproducible scripts, once created and verified.

## Conventions

- **Examples:** show model version, checkpoint checksum, threshold, source/license and “model prediction, requires human review” caption.
- **Screenshots:** real browser captures with API state, no fabricated counters, no private identities or location details without permission.
- **Diagrams:** architecture and flows are explanatory, not guarantees of running services. Store source/editable diagram when possible.
- **Plots:** statistical graphics must be computed from persisted metrics or raw evaluation results, clearly naming dataset and split. Do not reconstruct curves from a single aggregate score.
- Use descriptive names and add alt text when embedding media in READMEs.
- If image is third-party, preserve original attribution and usage rights; the root MIT license does not auto-relicense media.

## FAQ

**Why are diagram/screenshot directories empty?** They are placeholders, not missing evaluated results.

**Is the example a measured benchmark?** No, a visual example.

**Can I upload workers' faces?** Only where permission, appropriate privacy policy and access controls are in place. Use anonymized/synthetic or rights-cleared test images when possible.
