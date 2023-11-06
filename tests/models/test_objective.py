"""This file defines the tests for the objective Enum object.

It primarily handles checking that all the required types are included.
"""

from core.models.question import Objective


def test_obejctive_values():
    """Test that the objective Enum object has the correct values."""

    assert Objective.FACTUAL.value == "factual understanding"
    assert Objective.CLARITY.value == "clarity of writing"
    assert Objective.CREATIVITY.value == "creativity"
    assert Objective.ANALYSIS.value == "analytical skills"
    assert Objective.APPLICATION.value == "application of knowledge"
    assert Objective.EVIDENCE.value == "use of evidence"
    assert Objective.REFLECTION.value == "self reflection"
