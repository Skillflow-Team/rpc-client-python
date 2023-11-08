"""
The Rubric object ties the question object to the lower level grading components. It is responsible 
for defining the grading criteria that the LLM will use to grade the question. It also provides
methods for creating new rubrics from a dictionary or a RubricType.

Therefore, understanding the RubricType enumeration class is a key part of the Rubric concept. We
can use RubricTypes to quickly generate Rubric objects using a factory style pattern. This allows
for quick and easy creation of Rubrics with predefined grading criteria.

It is important to note that the RubricType class is not a traditional enum class. Each value is a
tuple, therefore meaning that we cannot instantiate the class with an intializer method.
"""
from enum import Enum
from typing import Dict, Optional

from core.errors import ValidationError

from .grading_criteria import GradingCriteria
from .objective import Objective


class RubricType(Enum):
    """
    RubricType is an enumeration class that defines different types of rubrics.

    Attributes
    ----------
    FACTUAL_RUBRIC
        A rubric type that emphasizes accuracy and supporting evidence.
    ANALYTICAL_RUBRIC
        A rubric type that focuses on analysis and supporting arguments with evidence.
    CREATIVE_RUBRIC
        A rubric type that encourages creativity and clear personal expression.
    APPLICATION_RUBRIC
        A rubric type that tests application of knowledge and analytical skills.
    COMPREHENSIVE_RUBRIC
        A rubric type that is a balanced mix of factual, analytical, application, and creative skills.
    COMMUNICATION_RUBRIC
        A rubric type that emphasizes communication skills.

    Example
    -------
    As with any enum class, we can create a RubricType object by referencing the enum value::

        from core.models.rubric import RubricType

        # Create a new RubricType
        factual_rubric = RubricType.FACTUAL_RUBRIC

        print(factual_rubric.label)
        # 'Factual Rubric'

        print(factual_rubric.criteria)
        # [(Objective.FACTUAL, 1.0), (Objective.EVIDENCE, 1.0), (Objective.CLARITY, 1.0)]

    This interface provides an easy way to create Rubric objects with predefined grading criteria.
    """

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
    def label(self) -> str:
        """Provides the label associated with each rubric type."""
        return self._label

    @property
    def criteria(self) -> Dict[Objective, GradingCriteria]:
        """Provides the default criteria associated with each rubric type."""
        criteria = [
            GradingCriteria(objective, weight)
            for objective, weight in self._default_criteria
        ]
        return criteria


class Rubric:
    """
    The Rubric class is responsible for defining the grading criteria that will be used to grade a
    question.

    Attributes
    ----------
        criteria : Dict[Objective, GradingCriteria]
            A dictionary of Objective and GradingCriteria pairs that define the grading criteria.
        rubric_type : RubricType
            The type of rubric. (RubricType.CUSTOM_RUBRIC for manually created rubrics)
        size : int
            The number of grading criteria in the rubric.


    The Rubric object let's us define how we are going to grade a question. It is responsible for
    defining the grading criteria that the LLM will use to grade the question. It's primary
    purpose is to provide a flexible API for creating rubrics.

    For more clarity on the Rubric class, please look at the [rubric notebook](https://github.com/Skillflow-Team/rpc-client-python/blob/main/examples/01_rubrics.ipynb).

    Examples
    --------
    With the factory pattern of the RubricType class, we can create fully functional rubrics
    with just one line of code::

        from turing import Rubric, RubricType

        rubric = Rubric.from_rubric_type(RubricType.FACTUAL_RUBRIC)

    Additionally, for more custom use cases, we can create a rubric manually, by adding the
    criteria as we go::

        from turing import Rubric, Objective

        rubric = Rubric.empty()

        rubric.add_criteria(Objective.FACTUAL, 1.0)
        rubric.add_criteria(Objective.EVIDENCE, 1.5)
        rubric.add_criteria(Objective.CLARITY, 0.5)

    Hopefully these examples can help paint the picture of how flexible the Rubric class is.
    """  # pylint: disable=line-too-long

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
        """Adds a new criteria to the rubric.

        Args
        ----
            objective : Objective
                The objective that the criteria is associated with.
            weight : float
                The weight of the criteria. This is used to tell the LLM how much to weigh the
                objective when grading the question.

        Raises
        ------
            ValidationError
                If the objective is not an instance of the Objective class or if
                the weight fails the validation check of the GradingCriteria class.
        """
        # Off load the validation checks to the GradingCriteria class
        self.criteria[objective] = GradingCriteria(objective=objective, weight=weight)

    def serialize(self) -> Dict[str, float]:
        """Serialize the rubric to a dictionary.

        Returns
        -------
            Dict[str, float]
                A dictionary of the rubric criteria
                ::
                    {
                        "factual understanding": 1.0,
                        "use of evidence": 1.0,
                        "clarity of writing": 1.0
                    }

        This method is used by the question model when serializing the question to a dictionary.

        NOTE: This method should NOT be overriden, as it is used internally by the SDK for
        serializing the question object for requests to Turing's LLM.
        """
        return {
            objective.value: float(criteria.weight)
            for objective, criteria in self.criteria.items()
        }

    @classmethod
    def empty(cls) -> "Rubric":
        """Creates a new empty rubric.

        Returns
        -------
            Rubric
                A new empty rubric.

        This method is used by the RubricType class to create new, empty rubrics. The rubric_type
        on a class created with this classmethod is set to RubricType.CUSTOM_RUBRIC.

        NOTE: You will not be able to grade questions with an empty rubric. You must add criteria
        manually before grading a response.
        """
        return cls(criteria={})

    @classmethod
    def from_rubric_type(cls, rubric_type: RubricType) -> "Rubric":
        """Creates a new rubric from a rubric type.

        Args
        ----
            rubric_type : RubricType
                The rubric type to create the rubric from.

        Returns
        -------
            Rubric
                A new rubric with the criteria from the provided rubric type.

        This method provides a factory for creating rubrics. By simply providing an enum value from
        the RubricType class, we can create a fully functional rubric with predefined grading
        criteria in just one line of code.

        Example
        -------
        Let's see how simple it is to use this factory pattern in practice::

            from turing import Rubric, RubricType

            rubric = Rubric.from_rubric_type(RubricType.FACTUAL_RUBRIC)

        Now this rubric can be used to create a question object. This method is also used
        internally by the ShortAnswerQuestion object's `from_rubric_type` classmethod. If
        you perfer, you can simply leverage that classmethod instead for even easier
        instantiation.
        """
        # Form the crtieria dictionary that will be used by the GradingGriteria class
        # to create the grading criteria
        criteria = {criteria.objective: criteria for criteria in rubric_type.criteria}
        return cls(criteria=criteria, _type=rubric_type)

    @classmethod
    def from_dict(cls, payload: Dict[str, float]) -> "Rubric":
        """Creates a new rubric from a dictionary.

        Args
        ----
            payload : Dict[str, float]
                A dictionary of the grading criteria. The keys should be the objective and the
                values should be the weight of the criteria.

        Returns
        -------
            Rubric
                A new rubric with the criteria from the provided dictionary.

        Raises
        ------
            ValidationError
                If the payload is not a dictionary or if the payload is not formatted correctly.

        This method provides another factory for creating rubrics. By simply providing a dictionary
        with the serialized grading criteria, we can create a fully functional rubric directly
        from a python dictionary.

        Example
        -------
        Let's look at how we can create a rubric from a dictionary::

            from turing import Rubric

            payload = {
                "factual understanding": 1.0,
                "use of evidence": 1.0,
                "clarity of writing": 1.0
            }

            rubric = Rubric.from_dict(payload)

        If it better suits your needs, this method can be overriden to define a custom Rubric
        object, with it's own custom logic for creating rubrics from a dictionary. This can allow
        you to adjust your rubric creation logic to fit your use case.
        """

        try:
            # Attempt to create a new criteria dictionary from the payload
            criteria = {
                # For each objective-weight pair, setup a new GradingCriteria object
                Objective(objective): GradingCriteria(
                    objective=Objective(objective), weight=weight
                )
                # Extract the items from the payload
                for objective, weight in payload.items()
            }
            # Create a new rubric with the provided criteria and a RubricType of CUSTOM_RUBRIC
            return cls(criteria=criteria)

        # If any of the provided objective keys are not valid Objective values, a value error will
        # be raised
        except ValueError as exp:
            raise ValidationError("Invalid payload.") from exp

        # If any of the payload is not an instance of a dictionary, the `items()` call will
        # through a AttributeError
        except AttributeError as exp:
            raise ValidationError(
                "Invalid payload provided. Must be a dictionary."
            ) from exp
