"""Rubric model."""
from enum import Enum
from typing import Dict, Optional

from core.errors import ValidationError

from .grading_criteria import GradingCriteria
from .objective import Objective


class RubricType(Enum):
    """The type of rubric."""

    FACTUAL_RUBRIC = (
        "Factual Rubric",
        [
            # Emphasizes accuracy and supporting evidence
            (Objective.FACTUAL, 1.0),
            (Objective.EVIDENCE, 1.0),
            (Objective.CLARITY, 1.0),
        ],
    )
    ANALYTICAL_RUBRIC = (
        "Analytical Rubric",
        [
            # Focuses on analysis and supporting arguments with evidence
            (Objective.ANALYSIS, 1.0),
            (Objective.EVIDENCE, 1.0),
            (Objective.REFLECTION, 1.0),
        ],
    )
    CREATIVE_RUBRIC = (
        "Creative Rubric",
        [
            # Encourages creativity and clear personal expression
            (Objective.CREATIVITY, 1.0),
            (Objective.CLARITY, 1.0),
            (Objective.REFLECTION, 1.0),
        ],
    )
    APPLICATION_RUBRIC = (
        "Application Rubric",
        [
            # Tests application of knowledge and analytical skills
            (Objective.APPLICATION, 1.0),
            (Objective.ANALYSIS, 1.0),
            (Objective.FACTUAL, 1.0),
        ],
    )
    COMPREHENSIVE_RUBRIC = (
        "Comprehensive Rubric",
        [
            # A balanced mix of factual, analytical, application, and creative skills
            (Objective.FACTUAL, 1.0),
            (Objective.ANALYSIS, 1.0),
            (Objective.APPLICATION, 1.0),
            (Objective.CREATIVITY, 1.0),
        ],
    )
    COMMUNICATION_RUBRIC = (
        "Communication Rubric",
        [
            # Prioritizes clear communication, reflection, and creativity
            (Objective.CLARITY, 1.0),
            (Objective.REFLECTION, 1.0),
            (Objective.CREATIVITY, 1.0),
        ],
    )
    CUSTOM_RUBRIC = ("Custom Rubric", [])

    def __init__(self, label, default_criteria):
        self._label = label
        self._default_criteria = default_criteria

    @property
    def label(self):
        return self._label

    @property
    def criteria(self):
        """Provides the default criteria associated with each rubric type."""
        criteria = [
            GradingCriteria(objective, weight)
            for objective, weight in self._default_criteria
        ]
        return criteria


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
        criteria = {criteria.objective: criteria for criteria in rubric_type.criteria}
        return cls(criteria=criteria, _type=rubric_type)

    @classmethod
    def from_dict(cls, payload: Dict[str, float]) -> "Rubric":
        """Creates a new rubric from a dictionary."""
        try:
            criteria = {
                Objective(objective): GradingCriteria(
                    objective=Objective(objective), weight=weight
                )
                for objective, weight in payload.items()
            }
            # Create a new rubric with the provided criteria and a RubricType of CUSTOM_RUBRIC
            return cls(criteria=criteria)
        except ValueError as exp:
            raise ValidationError("Invalid payload.") from exp
        except AttributeError as exp:
            raise ValidationError(
                "Invalid payload provided. Must be a dictionary."
            ) from exp
