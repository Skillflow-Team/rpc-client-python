"""
The `core.models.question` module defines the Question class and associated
functionality.

This module is responsible for representing the question entity in a structured
form, which can be used throughout the RPC client library. It includes methods
for initializing a new Question object, setting its attributes, and preparing it
for serialization to be sent to the RPC server.

Classes:
    Question: Represents a question with methods to prepare it for an RPC call.

Example:
    >>> from core.models.question import Question
    >>> question = Question("What is the capital of France?")
    >>> print(question.text)
    What is the capital of France?
"""
from enum import Enum
from typing import Dict, Optional, Union

from pydantic import BaseModel, field_validator
from pydantic_core import ValidationError as PydanticValidationError

from core.errors import ValidationError


class Objective(Enum):
    """The objective component.

    This component defines the different objectives that can be used to grade a question. They
    the different objective grading criteria that can be used to evaluate a response.
    """

    # How well does the student provide correct information
    FACTUAL = "factual understanding"

    # Clarity of the student's writing
    CLARITY = "clarity of writing"

    # Creativity in the student's response
    CREATIVITY = "creativity"

    # Student's ability to dissect or interpret the information
    ANALYSIS = "analytical skills"

    # Student's ability to apply learned concepts to new scenarios
    APPLICATION = "application of knowledge"

    # Backing up the answer with relevant data or examples
    EVIDENCE = "use of evidence"

    # Showcasing self-awareness or connections to personal experiences
    REFLECTION = "self reflection"


class GradingCriteria(BaseModel):
    objective: Objective
    weight: float

    def __init__(self, objective: Objective = None, weight: float = None):
        try:
            super().__init__(objective=objective, weight=weight)
        except PydanticValidationError as exp:
            raise ValidationError.from_pydantic(exp) from exp

    @field_validator("weight")
    def validate_weight(cls, value: float):  # pylint: disable=no-self-argument
        """Validates the weight of the criteria."""
        if value <= 0:
            raise ValueError("Weight must be greater than 0.")
        if (value * 2) % 1 != 0:
            raise ValueError("Weight must be a multiple of 0.5")
        return value


class RubricType(Enum):
    """The type of rubric."""

    FACTUAL_RUBRIC = "Factual Rubric"
    ANALYTICAL_RUBRIC = "Analytical Rubric"
    CREATIVE_RUBRIC = "Creative Rubric"
    APPLICATION_RUBRIC = "Application Rubric"
    COMPREHENSIVE_RUBRIC = "Comprehensive Rubric"
    COMMUNICATION_RUBRIC = "Communication Rubric"
    CUSTOM_RUBRIC = "Custom Rubric"

    def get_default_criteria(self):
        """Provides the default criteria associated with each rubric type."""
        return DEFAULT_RUBRIC_CRITERIA[self]


DEFAULT_RUBRIC_CRITERIA = {
    RubricType.FACTUAL_RUBRIC: [
        # Emphasizes accuracy and supporting evidence
        (Objective.FACTUAL, 1.0),
        (Objective.EVIDENCE, 1.0),
        (Objective.CLARITY, 1.0),
    ],
    RubricType.ANALYTICAL_RUBRIC: [
        # Focuses on analysis and supporting arguments with evidence
        (Objective.ANALYSIS, 1.0),
        (Objective.EVIDENCE, 1.0),
        (Objective.REFLECTION, 1.0),
    ],
    RubricType.CREATIVE_RUBRIC: [
        # Encourages creativity and clear personal expression
        (Objective.CREATIVITY, 1.0),
        (Objective.CLARITY, 1.0),
        (Objective.REFLECTION, 1.0),
    ],
    RubricType.APPLICATION_RUBRIC: [
        # Tests application of knowledge and analytical skills
        (Objective.APPLICATION, 1.0),
        (Objective.ANALYSIS, 1.0),
        (Objective.FACTUAL, 1.0),
    ],
    RubricType.COMPREHENSIVE_RUBRIC: [
        # A balanced mix of factual, analytical, application, and creative skills
        (Objective.FACTUAL, 1.0),
        (Objective.ANALYSIS, 1.0),
        (Objective.APPLICATION, 1.0),
        (Objective.CREATIVITY, 1.0),
    ],
    RubricType.COMMUNICATION_RUBRIC: [
        # Prioritizes clear communication, reflection, and creativity
        (Objective.CLARITY, 1.0),
        (Objective.REFLECTION, 1.0),
        (Objective.CREATIVITY, 1.0),
    ],
    RubricType.CUSTOM_RUBRIC: [],
}


class Rubric:
    criteria: Dict[Objective, GradingCriteria]
    _type: RubricType

    def __init__(
        self,
        criteria: Dict[Objective, GradingCriteria],
        _type: Optional[RubricType] = RubricType.CUSTOM_RUBRIC,
    ) -> None:
        self.criteria = criteria
        self._type = _type

    @property
    def size(self) -> int:
        """The number of criteria in the rubric."""
        return len(self.criteria)

    @property
    def rubric_type(self) -> str:
        """The type of rubric."""
        return self._type

    def add_criteria(self, objective: Objective, weight: float) -> None:
        """Adds a new criteria to the rubric."""
        if not isinstance(objective, Objective):
            raise ValidationError(
                "Objective must be an instance of the Objective class."
            )
        self.criteria[objective] = GradingCriteria(objective=objective, weight=weight)

    def serialize(self) -> Dict[str, float]:
        """Serialize the rubric to a dictionary."""
        return {
            objective.value: float(criteria.weight)
            for objective, criteria in self.criteria.items()
        }

    @classmethod
    def empty(cls) -> "Rubric":
        """Creates a new empty rubric."""
        return cls(criteria={})

    @classmethod
    def from_rubric_type(cls, rubric_type: RubricType) -> "Rubric":
        """Creates a new rubric from a rubric type."""
        criteria = {
            objective: GradingCriteria(objective=objective, weight=weight)
            for objective, weight in rubric_type.get_default_criteria()
        }
        return cls(criteria=criteria, _type=rubric_type)


class ShortAnswerQuestion:
    body: str
    example_answer: str
    rubric: Rubric

    def __init__(
        self, body: str, example_answer: str, rubric: Rubric = Rubric.empty()
    ) -> None:
        self.body = body
        self.example_answer = example_answer
        self.rubric = rubric

    # Adding Criteria methods
    def add_criteria(self, objective: Objective, weight: float) -> None:
        """Adds a new criteria to the rubric."""
        self.rubric.add_criteria(objective, weight)

    def set_rubric(self, rubric: Rubric) -> None:
        """Sets the rubric for the question."""
        if not isinstance(rubric, Rubric):
            raise ValidationError("Rubric must be an instance of the Rubric class.")
        self.rubric = rubric

    # Internal validation methods
    def _is_valid(self) -> None:
        """Whether the question is valid."""
        if not self.rubric.size:
            raise ValidationError("Rubric must have at least one criteria.")
        if not bool(self.body and self.example_answer):
            raise ValidationError("Question body and example answer cannot be empty.")

    def _serialize(self) -> Dict[str, Union[str, Dict[str, float]]]:
        """Serialize the question to a dictionary."""
        # Return the serialized question
        return {
            "body": self.body,
            "example_answer": self.example_answer,
            "rubric": self.rubric.serialize(),
        }

    def grade(self, answer: str):
        """Grade the answer to the question."""
        raise NotImplementedError()

    @classmethod
    def from_rubric_type(
        cls, body: str, example_answer: str, rubric_type: RubricType
    ) -> "ShortAnswerQuestion":
        """Creates a new short answer question from a rubric type."""
        rubric = Rubric.from_rubric_type(rubric_type)
        return cls(
            body=body,
            example_answer=example_answer,
            rubric=rubric,
        )
