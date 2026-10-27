"""Conservative observations only; no person-to-PPE association.

Bounding boxes may overlap different people. A no_* detection is a source-label
observation, NOT independently verified policy violation.
"""

NEGATIVE_LABELS = {"no_helmet", "no_boots", "no_gloves", "no_goggle"}
POSITIVE_LABELS = {"helmet", "vest", "boots", "gloves", "goggles"}

def summarize_observations(detections: list[dict]) -> dict:
    positive = sorted({d["class_name"] for d in detections if d["class_name"] in POSITIVE_LABELS})
    negative = sorted({d["class_name"] for d in detections if d["class_name"] in NEGATIVE_LABELS})
    return {
        "ppe_detected": positive,
        "source_labeled_absences": negative,
        "compliance_status": "not_assessed",
        "requires_human_review": bool(negative),
        "note": "Source labels are object detections, not worker-level compliance. 'head', 'person', and 'none' do not prove missing PPE. Absence of a detected item is not evidence of a violation.",
    }
