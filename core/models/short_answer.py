"""
The `core.models.question` module defines the Question class and associated
functionality.

This module is responsible for representing the question entity in a structured
form, which can be used throughout the RPC client library. It includes methods
for initializing a new Question object, setting its attributes, and preparing it
for serialization to be sent to the RPC server.

Classes:
    ShortAnswerQuestion: Represents a question with methods to prepare it for an RPC call.

Example:
    >>> from core.models.question import Question
    >>> question = Question("What is the capital of France?")
    >>> print(question.text)
    What is the capital of France?
"""
from typing import Dict, Union

from core.client import RPCClient
from core.errors import ValidationError

from .objective import Objective
from .rubric import Rubric, RubricType


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
            "question": self.body,
            "example_answer": self.example_answer,
            "rubric": self.rubric.serialize(),
        }

    def grade(self, answer: str):
        """Grade the answer to the question."""
        client = RPCClient()
        feedback, score = client.short_answer(self._serialize(), answer)
        return feedback, score

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

    @classmethod
    def from_dict(cls, payload: Dict[str, Union[str, Dict[str, float]]]):
        """Creates a new short answer question from a dictionary."""
        return cls(
            body=payload["body"],
            example_answer=payload["example_answer"],
            rubric=Rubric.from_dict(payload["rubric"]),
        )
