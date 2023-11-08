"""
The models module is the central component of the Turing SDK, providing the 
functionality to define and grade questions. It contains the `ShortAnswerQuestion` 
class, which is the cornerstone of the SDK, and the `Rubric` class, which is used 
to define how a question should be graded.

The module is split into two main layers:

1. Core Components
2. Helper Components

The core components are responsible for managing the data and logic of the SDK, while the 
helper components are used for validation and consistency. The helper components are needed
to provide a clean, flexible, and easy to use SDK, while the core components are needed to
provide the functionality that the SDK is designed to provide.

Core Components
---------------
The Turing SDK has two main components. The `ShortAnswerQuestion` class and the `Rubric` class.
The rubric is responsible for defining the grading criteria (i.e. the "instructions" for the LLM),
while the question object is responsible for storing the question data and executing the request 
to the LLM to actually grade the question. 

Short Answer Question
^^^^^^^^^^^^^^^^^^^^^
The `ShortAnswerQuestion` class is tasked with handling the question defintion and the
grading logic. Everything that happens in the SDK runs through this class. We will dig
deeper into the implementation of the class shortly, but for now it is important to
the centraility that this class holds in relation to the rest of the library.

Rubric
^^^^^^
The `Rubric` class is used internally by Turing to configure the LLM requests, 
ensuring the most accurate and relevant grading and feedback generations. This class
could be viewed as the "instructions" for the LLM. It's sole purpose is to define 
how the LLM will approach grading the question.

The `Rubric` class provides a flexible API for creating rubrics, including methods 
for creating rubrics from predefined `RubricType` instances, from `Objective` 
objects with assigned weights, and from data payloads.

Helper Components
-----------------
In addition to the core components, there are a couple of helper classes that are
used under the hood to facilate the flexibility that the SDK provides as well as the
consistency needed by the LLM to produce accurate results.

Objective
^^^^^^^^^
The easiest way to view the helper components is through the `Objective` class. This class is
the lowest level object in the module. It defines grading 'objectives' that are used by the LLM
to grade questions. It is implemeneted as an enum, with each enum value representing a different
objective.

Grading Criteria
^^^^^^^^^^^^^^^^
The enum values are then used to create `GradingCriteria` objects, which are used to define a
paring of an objective and a weight. This allows us to relate each `Objective` that we want to 
use for grading a question, to a corresponding weight value, which tells the LLM how much to 
weigh that objective when grading the question.

Rubric Type
^^^^^^^^^^^
This gives us an incredibly granular system for defining exactly how we want the LLM to grade a
question. However, some use cases may need a simpler implementation model. For this reason, the
`RubricType` class was created. This class provides a number of predefined rubric types that can
be used to quickly create a rubric. The `RubricType` is an enum class with tuples as values. The
first element of the tuple is the name, or 'label' of the rubric type and the second element is a
of `GradingCriteria` that are used in rubrics with that `RubricType`.

This gives us an easy way to join the lower level grading components with the higher level question
and rubric components. We will dig more into exactly how these components relate in the docs of
this module.
"""

from .short_answer import ShortAnswerQuestion
from .rubric import Rubric, RubricType
from .objective import Objective
from .grading_criteria import GradingCriteria
