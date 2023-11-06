"""This test defines the unit tests for the Rubric model.

We want to check that:
    - The RubricType enum is configured with correct values
    - The DEFAULT_RUBRIC_CRITERIA dictionary is configured correctly
    - The get_default_criteria method is configured correctly
    - The `empty` classmethod returns an empty rubric
    - The `from_rubric_type` classmethod creates a rubric with the correct
        criteria
"""
from unittest.mock import patch, call

import pytest

from core.models.question import (
    Rubric,
    RubricType,
    DEFAULT_RUBRIC_CRITERIA,
    Objective,
)
from core.errors import ValidationError


def test_rubric_type_values():
    """Test the the RubricType class has all the correct values."""
    assert RubricType.FACTUAL_RUBRIC.value == "Factual Rubric"
    assert RubricType.ANALYTICAL_RUBRIC.value == "Analytical Rubric"
    assert RubricType.CREATIVE_RUBRIC.value == "Creative Rubric"
    assert RubricType.APPLICATION_RUBRIC.value == "Application Rubric"
    assert RubricType.COMPREHENSIVE_RUBRIC.value == "Comprehensive Rubric"
    assert RubricType.COMMUNICATION_RUBRIC.value == "Communication Rubric"


def test_default_criteria_dictonary():
    """Test that the DEFAULT_RUBRIC_CRITERIA dictionary is configured correctly with
    all the RubricType values.
    """
    assert RubricType.FACTUAL_RUBRIC in DEFAULT_RUBRIC_CRITERIA
    assert RubricType.ANALYTICAL_RUBRIC in DEFAULT_RUBRIC_CRITERIA
    assert RubricType.CREATIVE_RUBRIC in DEFAULT_RUBRIC_CRITERIA
    assert RubricType.APPLICATION_RUBRIC in DEFAULT_RUBRIC_CRITERIA
    assert RubricType.COMPREHENSIVE_RUBRIC in DEFAULT_RUBRIC_CRITERIA
    assert RubricType.COMMUNICATION_RUBRIC in DEFAULT_RUBRIC_CRITERIA


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
    assert rubric_type.get_default_criteria() == DEFAULT_RUBRIC_CRITERIA[rubric_type]


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
    with patch("core.models.question.GradingCriteria") as mock_criteria:
        rubric = Rubric.from_rubric_type(rubric_type)
        expected_calls = [
            call(objective=objective, weight=weight)
            for objective, weight in DEFAULT_RUBRIC_CRITERIA[rubric_type]
        ]
        assert mock_criteria.call_args_list == expected_calls
        assert len(rubric.criteria) == len(expected_calls)

        # Ensure all the necessary values of the rubric are present
        criteria_expected = rubric_type.get_default_criteria()
        for objective, weight in criteria_expected:
            assert objective in rubric.criteria
            assert float(rubric.criteria[objective].weight) == weight


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

    criteria = RubricType.FACTUAL_RUBRIC.get_default_criteria()
    serialized_criteria = [(k.value, v) for k, v in criteria]
    for k, v in data.items():
        assert (k, v) in serialized_criteria
