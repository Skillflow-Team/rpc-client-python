"""
The Objective class is a fundamental part of the Turing SDK. It is implemented as an
enumeration (enum), where each enum value represents a different grading objective.
These objectives are used by the LLM (Large Language Model) to grade questions.

Each `Objective` is associated with a specific "objective" for the LLM to focus on when grading.
If you choose to build a custom rubric by defining your `Objectives` manually, be sure to
experiment with different combinations to find out which ones work best for your use case.
"""

from enum import Enum


class Objective(Enum):
    """
    The Objective class is an enumeration (Enum) that represents different grading objectives.

    Attributes
    ----------
    FACTUAL
        Represents the objective of providing correct information.
    CLARITY
        Represents the objective of clarity in writing.
    CREATIVITY
        Represents the objective of creativity in response.
    ANALYSIS
        Represents the objective of analytical skills.
    APPLICATION
        Represents the objective of applying learned concepts to new scenarios.
    EVIDENCE
        Represents the objective of backing up the answer with relevant data or examples.
    REFLECTION
        Represents the objective of showcasing self-awareness or connections to personal
        experiences.


    Each enum value represents a different aspect of the grading process, such as grammar,
    relevance, or accuracy. These objectives are used by the LLM to grade questions.

    Example
    -------
    For some helpful context, we can use the Objective class like any other enum class::

        >>> from turing.models.objective import Objective

        >>> # Define a new Objective
        >>> factual_objective = Objective.FACTUAL

        >>> # Print the name of the Objective
        >>> print(factual_objective.value)
        >>> # 'factual understanding'

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
