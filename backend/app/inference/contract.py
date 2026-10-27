"""Frozen source labels verified from Day 21 PPE Guard checkpoint.
Never silently rename, merge or invent labels.
"""
CLASS_NAMES = (
    "helmet", "no_helmet", "vest", "boots", "gloves", "goggles",
    "head", "no_boots", "no_gloves", "no_goggle", "none", "person",
)
MODEL_TASK = "detect"

def assert_model_contract(names: dict, task: str) -> None:
    normalized = {int(k): str(v) for k, v in names.items()}
    expected = dict(enumerate(CLASS_NAMES))
    if task != MODEL_TASK or normalized != expected:
        raise ValueError(
            f"Incompatible PPE checkpoint: task={task!r}; classes={normalized!r}. "
            f"Expected task={MODEL_TASK!r}; classes={expected!r}."
        )
