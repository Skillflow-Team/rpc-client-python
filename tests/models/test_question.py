"""This file defines the unit tests for the Question model.

We want to check that:
    - The initializer is configured correctly
    - The from_rubric_type classmethod is configured correctly
    - The add_criteria method is configured correctly
    - The set_rubric method is configured correctly
    - The _is_valid method is configured correctly
    - The _serialize method is configured correctly
"""
from unittest.mock import patch

import pytest

from core.models.question import ShortAnswerQuestion, Rubric, RubricType, Objective
from core.errors import ValidationError


def test_short_answer_question_init_no_rubric():
    """Test that the initializer is configured correctly wihtout a Rubric."""

    # Create a new question
    question = ShortAnswerQuestion(
        body="What is the capital of Australia?",
        example_answer="Canberra",
    )

    # Check that the question has the correct attributes
    assert question.body == "What is the capital of Australia?"
    assert question.example_answer == "Canberra"
    assert question.rubric.size == 0
    assert question.rubric.rubric_type == RubricType.CUSTOM_RUBRIC


def test_short_answer_question_init_with_rubric():
    """Test that the initializer is configured correctly with a Rubric."""

    # Create a new question
    question = ShortAnswerQuestion(
        body="What is the capital of Australia?",
        example_answer="Canberra",
        rubric=Rubric.from_rubric_type(RubricType.FACTUAL_RUBRIC),
    )

    # Check that the question has the correct attributes
    assert question.body == "What is the capital of Australia?"
    assert question.example_answer == "Canberra"
    assert question.rubric.size == 3
    assert question.rubric.rubric_type == RubricType.FACTUAL_RUBRIC


def test_from_rubric_type_classmethod():
    """Test that the from_rubric_type classmethod is configured correctly."""

    # Create a new question
    question = ShortAnswerQuestion.from_rubric_type(
        body="What is the capital of Australia?",
        example_answer="Canberra",
        rubric_type=RubricType.FACTUAL_RUBRIC,
    )

    # Check that the question has the correct attributes
    assert question.body == "What is the capital of Australia?"
    assert question.example_answer == "Canberra"
    assert question.rubric.size == 3
    assert question.rubric.rubric_type == RubricType.FACTUAL_RUBRIC


def test_add_criteria():
    """Test that the criteria is added via the rubrics `add_criteria` method."""
    question = ShortAnswerQuestion(
        body="What is the capital of Australia?",
        example_answer="Canberra",
    )

    with patch.object(question.rubric, "add_criteria") as mock_add_criteria:
        question.add_criteria(Objective.FACTUAL, 1.0)
        mock_add_criteria.assert_called_once_with(Objective.FACTUAL, 1.0)


def test_set_rubric():
    """Test that the rubric is set via the rubrics `set_rubric` method."""
    question = ShortAnswerQuestion(
        body="What is the capital of Australia?",
        example_answer="Canberra",
    )
    rubric = Rubric.from_rubric_type(RubricType.FACTUAL_RUBRIC)

    question.set_rubric(rubric)
    assert question.rubric == rubric

    # Ensure that the rubric type checking is working
    with pytest.raises(ValidationError):
        question.set_rubric({"rubric": "rubric value"})


@pytest.mark.parametrize(
    "question,valid",
    [
        (
            ShortAnswerQuestion(
                "What is the capital of Australia?",
                "Canberra",
                rubric=Rubric.from_rubric_type(RubricType.FACTUAL_RUBRIC),
            ),
            True,
        ),
        (
            ShortAnswerQuestion(
                "What is the capital of Australia?",
                "Canberra",
                rubric=Rubric.empty(),
            ),
            False,
        ),
        (
            ShortAnswerQuestion(
                "What is the capital of Australia?",
                "",
                rubric=Rubric.from_rubric_type(RubricType.FACTUAL_RUBRIC),
            ),
            False,
        ),
        (
            ShortAnswerQuestion(
                "",
                "Canberra",
                rubric=Rubric.from_rubric_type(RubricType.FACTUAL_RUBRIC),
            ),
            False,
        ),
    ],
)
def test__is_valid_method(question, valid):
    """Test that the _is_valid method is configured correctly."""
    if valid:
        assert question._is_valid() is None  # pylint: disable=protected-access
    else:
        with pytest.raises(ValidationError):
            question._is_valid()  # pylint: disable=protected-access


def test__serialize_method():
    """Test that the _serialize method is configured correctly."""
    question = ShortAnswerQuestion(
        "What is the capital of Australia?",
        "Canberra",
        rubric=Rubric.from_rubric_type(RubricType.FACTUAL_RUBRIC),
    )
    assert question._serialize() == {  # pylint: disable=protected-access
        "body": "What is the capital of Australia?",
        "example_answer": "Canberra",
        "rubric": {
            "factual understanding": 1.0,
            "clarity of writing": 1.0,
            "use of evidence": 1.0,
        },
    }


def test_grade_method():
    """Test the grade method."""
    with pytest.raises(NotImplementedError):
        ShortAnswerQuestion("body", "answer").grade("answer")
