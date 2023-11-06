"""This file defines the GradingCriteria. The GradingCriteria is an ineternal Model used for managing the grading criteria for a Rubric."""

from pydantic import BaseModel, field_validator
from pydantic_core import ValidationError as PydanticValidationError

from core.errors import ValidationError

from .objective import Objective


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
