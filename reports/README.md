# Reports — provenance, dataset audit, and held-out model metrics

> **Historical research records.** Do not alter original report values to improve a README, “clean” inconvenient findings, or imply retesting. Any new experiment should write a versioned report with method, date, seed and source revision.

## Report index

| Artifact | Content | Caveat |
|---|---|---|
| `final_summary.json` | Project, Kaggle path, 12 classes, 8,451 images, model type and caveats | Training details incomplete |
| `heldout_metrics.json` | Precision, recall, mAP and 847-image test size | Aggregate only; no per-class AP |
| `source_inventory.json` | Files/extensions and two YAML paths | Inventory is not a data license audit |
| `annotation_inventory.json` | Source ontology, orphan labels and target box distribution | **10 orphan labels** reported |
| `selection_audit.json` | Selected image counts, split and box counts | No complete near-duplicate audit |
| `staged_manifest.csv` | Staged sample-level manifest | Check privacy, source paths and split integrity before reuse |
| `annotated_samples.png` | Visual example from research output | Qualitative only, not a measured metric |

## Before → Now → Next

Before: source inventory and annotation staging, model held-out evaluation. Now: JSON/CSV provide read-only experiment evidence linked from product documentation. Next: dataset hash audit, source-wise metrics, per-class metrics, calibration, versioned validation images and failures, independent worksite test, detailed training environment manifest.

## Dataset audit (recorded)

- Kaggle input root: `/kaggle/input/datasets/loliwibu/ppe-guard-datset`.
- Two source manifests: `Hard Hat Workers.v14-raw_headclassonly.yolov8/data.yaml` (`head` only) and `construction-ppe/data.yaml` (11 source classes, including capitalized `Person`).
- `source_inventory.json`: total files 16,917: `.txt` 8,463; `.yaml` 2; `.jpg` 8,298; `.jpeg` 153; no extension 1.
- `annotation_inventory.json`: images **8,451** and **10 orphan labels**.
- `selection_audit.json`: all/eligible/selected **8,451**; excluded categories `{}`; train **6,048**, validation **1,556**, test **847**. These sum to 8,451.

There is no documented result proving that the 10 orphan labels affected, or did not affect, particular selected samples. Do not claim all label files perfectly paired. Nor does `excluded={}` imply absence of corrupt imagery or source leakage across original files.

### Box distribution

| Class | Count | Class | Count |
|---|---:|---|---:|
| head | 26,424 | helmet | 1,734 |
| person | 2,245 | vest | 1,618 |
| boots | 1,597 | gloves | 1,445 |
| none | 797 | no_gloves | 556 |
| goggles | 518 | no_helmet | 485 |
| no_goggle | 411 | no_boots | 115 |

Counts represent annotated boxes, **not people, images or verified infractions**. The source schemas differ: one dataset labels heads only and another has a richer PPE scheme. This is a mixed/partial annotation problem; conventional aggregate mAP under mixed labels may not faithfully measure workplace safety performance.

## Held-out metrics (recorded file)

```json
{
  "eval_split": "test",
  "images": 847,
  "precision": 0.6306006972406554,
  "recall": 0.5392812479049882,
  "map50": 0.554925510207925,
  "map50_95": 0.29186887190219996
}
```

**Interpret carefully.** Precision/recall in this file are detector evaluation aggregate metrics; mAP50/95 evaluates localization/classification over IoU thresholds. The file does not establish per-person compliance F1, false-alarm costs, sensitivity to PPE absence, per-class performance, confidence calibration or validation on an independent site. The model was selected during training/validation according to project experiment; do not treat this held-out evaluation as a production certificate.

## Limitations and integrity gates

1. **Unresolved orphan labels**: inventory count 10; investigate filenames and handling in the original notebook.
2. **Potential near-duplicate leakage**: no complete perceptual-hash check documented; identical-looking frames can artificially inflate evaluation.
3. **Ontology mismatch**: not all sources annotate every target class consistently.
4. **Imbalanced classes**: `head` dominates; `no_boots` has only 115 boxes.
5. **Cross-domain generalization**: not assessed; test on new worksites and camera perspectives.
6. **Missing metadata**: this directory alone does not certify exact epochs, seed, scheduler, preprocessing augmentations or environment lock.
7. **Image sample bias**: one collage does not establish error rates or correct output across varied lighting and people.
8. **Legal/license provenance**: dataset manifests and sample images need separate upstream legal review before reuse/distribution.

## Reproducing / extending the experiment

Recover original Kaggle notebook and pinned dataset revision. Verify image/label pairing and source identities. Run exact hashes + perceptual duplicate detection **across split boundaries**, grouping related frames/source sequences. Record train/val/test manifests with immutable SHA-256. Train with logged model seed, model settings, library versions and machine. Select only on validation, evaluate once on an isolated test (then perform further pre-registered independent test). Save confusion matrix, per-class AP and P/R, failure gallery and external-site error analysis. Keep the historical report unchanged, produce a new folder or run identifier.

## Troubleshooting / FAQ

**Why 8,451 images but 8,463 `.txt`?** Inventory includes label-like text files and 10 reported orphan labels; file counts differ from paired-image counts. Inspect manifests before attributing all discrepancies.

**Why 847 test images?** That is the staged held-out split recorded in two audit JSONs; not necessarily a fully independent domain holdout.

**Can we say 55.49% accuracy?** No. The actual metric is **mAP@50**, not accuracy or PPE-compliance success rate.

**Are sample images licensed by MIT?** No: the repository's code license does not override third-party image/dataset terms.

**What about `head` and `none`?** Their raw dataset semantics must not be mapped to confirmed no-PPE findings. See root README and AGENTS.
