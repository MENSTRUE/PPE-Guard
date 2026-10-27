from app.inference.contract import assert_model_contract,CLASS_NAMES
from app.inference.safety_rules import summarize_observations
import pytest

def test_verified_mapping():
    assert_model_contract(dict(enumerate(CLASS_NAMES)),"detect")
    with pytest.raises(ValueError):
        assert_model_contract({0:"head"},"detect")

def test_no_implied_missing_ppe():
    obs=summarize_observations([{"class_name":"head"},{"class_name":"person"},{"class_name":"none"}])
    assert not obs["source_labeled_absences"]
    assert obs["compliance_status"] == "not_assessed"

def test_negative_source_label_requires_review():
    obs=summarize_observations([{"class_name":"no_helmet"}])
    assert obs["requires_human_review"]
    assert obs["compliance_status"] == "not_assessed"
