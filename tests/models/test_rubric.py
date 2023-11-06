"""This test defines the unit tests for the Rubric model.

We want to check that:
    - The RubricType enum is configured with correct values
    - The DEFAULT_RUBRIC_CRITERIA dictionary is configured correctly
    - The get_default_criteria method is configured correctly
    - The `empty` classmethod returns an empty rubric
    - The `from_rubric_type` classmethod creates a rubric with the correct
        criteria
"""

import pytest

from core.models.objective import Objective
from core.models.rubric import (
    Rubric,
    RubricType,
)
from core.errors import ValidationError


def test_rubric_type_values():
    """Test the the RubricType class has all the correct values."""
    assert RubricType.FACTUAL_RUBRIC.label == "Factual Rubric"
    assert RubricType.ANALYTICAL_RUBRIC.label == "Analytical Rubric"
    assert RubricType.CREATIVE_RUBRIC.label == "Creative Rubric"
    assert RubricType.APPLICATION_RUBRIC.label == "Application Rubric"
    assert RubricType.COMPREHENSIVE_RUBRIC.label == "Comprehensive Rubric"
    assert RubricType.COMMUNICATION_RUBRIC.label == "Communication Rubric"


@pytest.mark.parametrize(
    "rubric_type",
    [
        RubricType.FACTUAL_RUBRIC,
        RubricType.ANALYTICAL_RUBRIC,
        RubricType.CREATIVE_RUBRIC,
        RubricType.APPLICATION_RUBRIC,
        RubricType.COMPREHENSIVE_RUBRIC,
        RubricType.COMMUNICATION_RUBRIC,
    ],
)
def test_get_default_criteria(rubric_type):
    """Test that the get_default_criteria method is configured correctly."""
    criteria = rubric_type.criteria
    raw_criteria = rubric_type._default_criteria  # pylint: disable=protected-access
    for crit in criteria:
        assert (crit.objective, crit.weight) in raw_criteria


def test_empty_rubric():
    """Test that the empty classmethod returns an empty rubric."""
    rubric = Rubric.empty()
    assert rubric.criteria == dict()
    assert rubric.rubric_type == RubricType.CUSTOM_RUBRIC


@pytest.mark.parametrize(
    "rubric_type",
    [
        RubricType.FACTUAL_RUBRIC,
        RubricType.ANALYTICAL_RUBRIC,
        RubricType.CREATIVE_RUBRIC,
        RubricType.APPLICATION_RUBRIC,
        RubricType.COMPREHENSIVE_RUBRIC,
        RubricType.COMMUNICATION_RUBRIC,
    ],
)
def test_from_rubric_type(rubric_type):
    """Test that the from_rubric_type class method correctly configures a rubric
    with the correct criteria."""
    rubric = Rubric.from_rubric_type(rubric_type)
    assert rubric.rubric_type == rubric_type
    assert len(rubric.criteria) == len(rubric_type.criteria)
    for objective in rubric.criteria:
        assert rubric.criteria[objective] in rubric_type.criteria


def test_add_criteria():
    """Test that the add_criteria method correctly adds a criteria to the rubric."""
    rubric = Rubric.empty()
    rubric.add_criteria(Objective.FACTUAL, 1.0)

    assert rubric.criteria[Objective.FACTUAL].objective == Objective.FACTUAL
    assert rubric.criteria[Objective.FACTUAL].weight == 1.0
    assert rubric.size == 1

    original = rubric.criteria[Objective.FACTUAL]

    # Adding the same criteria should not change the size of the rubric
    # It should however create a new Criteria object
    rubric.add_criteria(Objective.FACTUAL, 0.5)
    assert rubric.criteria[Objective.FACTUAL].objective == Objective.FACTUAL
    assert rubric.criteria[Objective.FACTUAL].weight == 0.5
    assert rubric.size == 1
    assert rubric.criteria[Objective.FACTUAL] != original


def test_add_criteria_type_checking():
    """Test that the add_criteria method correctly type checks the objective."""
    rubric = Rubric.empty()
    with pytest.raises(ValidationError):
        rubric.add_criteria("not an objective", 1.0)


def test_serialize():
    """Test the serialization method of the rubric."""
    rubric = Rubric.from_rubric_type(RubricType.FACTUAL_RUBRIC)
    data = rubric.serialize()

    criteria = RubricType.FACTUAL_RUBRIC.criteria
    criteria_serialized_tuples = [
        (crit.objective.value, crit.weight) for crit in criteria
    ]
    for k, v in data.items():
        assert (k, v) in criteria_serialized_tuples
