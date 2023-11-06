"""This file defines the objective object."""

from enum import Enum


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
