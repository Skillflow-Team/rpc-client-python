"""
The GradingCriteria class is used to manage the grading criteria for a Rubric. Primarily
we find that clients will not have to interact with the GradingCriteria class for most use cases.
We wanted to include it in the documentation however, because it plays a key role in validation
during rubric creation and when adding and updating criteria on a rubric.

The primary takeaway for this class is to understand that it is tasked with validation of the 
individual components of the Rubric class. It provides the rubric with an easy way to validate
and store grading criteria along with their respective weights.
"""

from pydantic import BaseModel, field_validator
from pydantic_core import ValidationError as PydanticValidationError


from .objective import Objective
from ..errors import ValidationError


class GradingCriteria(BaseModel):
    """The GradingCriteria class is used to manage the grading criteria for a Rubric.

    Attributes
    ----------
    objective : Objective
        The objective that the criteria is associated with.
    weight : float
        The weight of the criteria. This is used to tell the LLM how much to weigh the
        objective when grading the question.


    Most use cases won't require much interaction with the GradingCriteria class. It primarily
    serves as a validation and storage layer for the Rubric class. However, if you need to
    override the GradingCriteria to create your own implementation, perhaps for defining
    custom Objectvie values, you can do so by extending the GradingCriteria class.

    It should be noted that the GradingCriteria class inherits from pydantic's BaseModel class,
    which can sometimes cause issues with inheritance. Please see the pydantic documentation at
    https://pydantic-docs.helpmanual.io/usage/models/#model-inheritance for more information.

    Creating GradingObjectives
    --------------------------
    For some helpful context, we can use the GradingCriteria class like any other pydantic model::

        from turing.models.grading_criteria import GradingCriteria
        from turing.models.objective import Objective

        # Define a new GradingCriteria
        criteria = GradingCriteria(
            objective=Objective.FACTUAL,
            weight=1.0,
        )

    Pydantic Validation
    -------------------
    As with any pydantic model, providing invalid types will cause validation errors to be raised::

        from turing.models.grading_criteria import GradingCriteria
        from turing.models.objective import Objective

        # raises ValidationError, since "grammatical accuracy" is
        # not a valid Objective
        criteria = GradingCriteria(
            objective="grammatical accuracy",
            weight=1.0
        )

        # raises ValidationError, since 1.25 is not a valid weight
        # for a GradingCriteria
        criteria = GradingCriteria(
            objective=Objective.FACTUAL,
            weight=1.25
        )
    """

    objective: Objective
    """The objective that the criteria is associated with."""

    weight: float
    """The weight of the criteria. This is used to tell the LLM how much to weigh the
    objective when grading the question."""

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
