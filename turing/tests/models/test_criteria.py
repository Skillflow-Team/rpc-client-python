"""This file defines the tests for the criteria object.

It primarily handles checking that:
    - The pydantic model validation is configured correctly
    - The custom error handling of initializer is configured correctly
    - The custom `weight` validation is configured correctly
"""
import pytest
from pydantic_core import ValidationError as PydanticValidationError

from turing.errors import ValidationError
from turing.models.grading_criteria import GradingCriteria
from turing.models.objective import Objective


@pytest.mark.parametrize(
    "obj,weight,raises,expected",
    [
        (Objective.FACTUAL, 1, False, 1.0),
        (Objective.FACTUAL, 1.0, False, 1.0),
        (Objective.FACTUAL, "0.5", False, 0.5),
        ("invalid objective", 1.0, True, None),
        (Objective.FACTUAL, "weight", True, None),
    ],
)
def test_pydantic_model_validation(obj, weight, raises, expected):
    """Test that the pydantic model validation is configured correctly."""
    if raises:
        with pytest.raises(Exception) as exp:
            GradingCriteria(objective=obj, weight=weight)
        assert isinstance(exp.value.__cause__, PydanticValidationError)

    else:
        criteria = GradingCriteria(objective=obj, weight=weight)
        assert criteria.weight == expected


def test_custom_init_error_handling():
    """Test that the custom error handling is configured correctly."""

    # First we want to ensure that pydantic validation errors are handled correctly
    with pytest.raises(ValidationError) as exp:
        # Pass an invalid objective to invoke a pydantic validation error
        GradingCriteria(objective="not an objective", weight=1.0)
    assert isinstance(exp.value.__cause__, PydanticValidationError)

    with pytest.raises(ValidationError):
        # Pass an invalid weight to invoke a value error
        GradingCriteria(objective=Objective.FACTUAL, weight=0.25)


@pytest.mark.parametrize(
    "weight,raises,expected",
    [
        (0.5, False, 0.5),
        (1, False, 1.0),
        (1.5, False, 1.5),
        (0, True, None),
        (-1.0, True, None),
        (0.25, True, None),
    ],
)
def test_custom_weight_validation(weight, raises, expected):
    """Test that the custom weight validation is configured correctly."""

    if raises:
        with pytest.raises(ValidationError) as exp:
            GradingCriteria(objective=Objective.FACTUAL, weight=weight)
        assert isinstance(exp.value.__cause__, PydanticValidationError)
    else:
        criteria = GradingCriteria(objective=Objective.FACTUAL, weight=weight)
        assert criteria.weight == expected
