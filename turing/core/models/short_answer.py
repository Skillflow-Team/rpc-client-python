"""
The question object is responsible for representing the question entity in a structured form,
which can be used throughout the RPC client library. It includes methods for initializing a new
Question object, setting its attributes, and preparing it for serialization to be sent to the
server.

Every operation that happens in the models model is in one way or another working to help the
question object do its job. For more information and more detailed exmaples on utilizing the 
ShortAnswerQuestion class, please look at the [notebook](https://github.com/Skillflow-Team/rpc-client-python/blob/main/examples/02_questions.ipynb)
on questions. 

There are a couple main questions that must be answered everywhere a question object is utilized:
1. How do we define the rubric?
2. How do we call the grade function?

The answer to the first question will depend on the use case. As defined in the notebooks, there
are many ways to setup question objects with different rubrics.
"""  # pylint: disable=line-too-long
from typing import Dict, Union


from .objective import Objective
from .rubric import Rubric, RubricType
from ..client import RPCClient
from ..errors import ValidationError


class ShortAnswerQuestion:
    """
    The ShortAnswerQuestion class represents a short answer question entity.

    Attributes
    ----------
    body : str
        The body of the question.
    example_answer : str
        An example answer for the question.
    rubric : Rubric
        The rubric used to grade the question.
    """

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
        """Adds a new criteria to the rubric.

        Args
        ----
        objective : Objective
            The objective to add to the rubric.
        weight : float
            The weight of the objective.

        Raises
        ------
        ValidationError
            If the validation checks for objective or weight fail.


        This method defines a wrapper for the :py:meth:`.Rubric.add_criteria`.
        It is used to build custom rubrics using the question model as a proxy for interacting
        with the underlying :py:class:`.Rubric` class. This interface can be used for simplifying
        the rubric defintion process.

        Example
        -------
        With this method, we can see how we can remove the need for the caller to interact with
        the rubric object at all::

            from turing import ShortAnswerQuestion, Objective

            # Define a new question with an empty rubric
            question = ShortAnswerQuestion(
                body="What is the meaning of life?",
                example_answer="42",
            )

            question.add_criteria(Objective.FACTUAL, 1.0)
            question.add_criteria(Objective.CLARITY, 0.5)
            question.add_criteria(Objective.CREATIVITY, 0.5)

        Now, instead of needing to add criteria to the rubric and then set the rubric on the
        question, we can simply add the criteria directly to the question object.
        """
        self.rubric.add_criteria(objective, weight)

    def set_rubric(self, rubric: Rubric) -> None:
        """Sets the rubric for the question.

        Args
        ----
        rubric : Rubric
            The rubric to set.

        Raises
        ------
        ValidationError
            If the rubric is not an instance of the :py:class:`.Rubric` class.

        This method allows us to define rubrics seperate from questions, then add the rubric to the
        question as an attribute.

        Example
        -------
        Note that using this method is not required, as the same affect can be achieved by setting
        the rubric at instantiation. This method is purely for convenience::

            from turing import ShortAnswerQuestion, Rubric, Objective

            # Define a new rubric
            rubric = Rubric.empty()

            # Add criteria to the rubric
            rubric.add_criteria(Objective.FACTUAL, 1.0)
            rubric.add_criteria(Objective.CLARITY, 0.5)
            rubric.add_criteria(Objective.CREATIVITY, 0.5)

            # Define a new question with an empty rubric
            question = ShortAnswerQuestion(
                body="What is the meaning of life?",
                example_answer="42",
            )

            question.set_rubric(rubric)

            # NOTE: This is the same as doing:
            question = ShortAnswerQuestion(
                body="What is the meaning of life?",
                example_answer="42",
                rubric=rubric,
            )

        From this example, we can see how we can define rubrics seperate from questions, then add
        the rubric to the question as an attribute, or simply set the rubric at instantiation.
        """
        if not isinstance(rubric, Rubric):
            raise ValidationError("Rubric must be an instance of the Rubric class.")
        self.rubric = rubric

    # Internal validation methods
    def _is_valid(self) -> None:
        """Whether the question is valid.

        Raises
        ------
        ValidationError
            If the rubric is empty or if the body or example_answer attributes are empty.

        This method is called internally by the grade method to check that the question is valid
        for an LLM request.
        """
        if not self.rubric.size:
            raise ValidationError("Rubric must have at least one criteria.")
        if not bool(self.body and self.example_answer):
            raise ValidationError("Question body and example answer cannot be empty.")

    def _serialize(self) -> Dict[str, Union[str, Dict[str, float]]]:
        """Serialize the question to a dictionary.

        Returns
        -------
        Dict[str, Union[str, Dict[str, float]]]
            The serialized question.
            ::

                {
                    "question": "What is the meaning of life?",
                    "example_answer": "42",
                    "rubric": {
                        "factual understanding": 1.0,
                        "clarity of writing": 0.5,
                        "creativity": 0.5,
                    }
                }

        This method is called internally by the grade method to serialize the question to a
        dictionary that can be sent to the LLM.
        """
        # Return the serialized question
        return {
            "question": self.body,
            "example_answer": self.example_answer,
            "rubric": self.rubric.serialize(),
        }

    def grade(self, answer: str):
        """Grade the answer to the question.

        Args
        ----
        answer : str
            The answer to the question.

        Returns
        -------
        Tuple[str, float]
            A tuple containing the feedback and the score.

        Raises
        ------
            ValidationError
                If the question is not valid.
            NetworkError
                If the RPC request fails due to a network error
            RPCMethodError
                If the RPC request fails due to an error in the RPC method


        We can grade requests by calling the grade method on the question object. This method
        will first run an internal validation check to ensure that the question is valid, then
        it will call the LLM to grade the question.

        Example
        -------
        ::

            from turing import ShortAnswerQuestion, RubricType

            question = "What is the capital of France?"
            example_answer = "Paris"
            student_answer = "London...I think?"

            # Create a new question object
            question = ShortAnswerQuestion(
                body=question,
                example_answer=example_answer,
            )

            # Define the grading criteria
            question.add_criteria(Objective.FACTUAL, 1.0)

            # Grade the question
            feedback, score = question.grade(student_answer)
            print(feedback)     # 'Nice try, but Paris is the capital of France, not London.'
            print(score)        # 0.0

        As you can see from this wholistic example, grading short answer questions with turing can
        be achieved in just a few short lines of code.
        """
        # Ensure that the question is valid
        self._is_valid()

        # Create a new RPC client and send the request
        client = RPCClient()
        feedback, score = client.short_answer(self._serialize(), answer)

        # Return a tuple with the desired outputs to the caller
        return feedback, score

    @classmethod
    def from_rubric_type(
        cls, body: str, example_answer: str, rubric_type: RubricType
    ) -> "ShortAnswerQuestion":
        """Creates a new short answer question from a rubric type.

        Args
        ----
        body : str
            The body of the question.
        example_answer : str
            An example answer for the question.
        rubric_type : RubricType
            The rubric type to use for the question.

        Returns
        -------
        ShortAnswerQuestion
            The new short answer question.


        This method provides a simple wrapper for the :py:meth:`.Rubric.from_rubric_type` method.
        We can use this method to instantiate a new question with a predefined rubric type, without
        ever needing to interact with the Rubric class.

        Example
        -------
        ::

                from turing import ShortAnswerQuestion, RubricType

                question = "What is the capital of France?"
                example_answer = "Paris"

                # Create a new question object
                question = ShortAnswerQuestion.from_rubric_type(
                    body=question,
                    example_answer=example_answer,
                    rubric_type=RubricType.FACTUAL,
                )

        With this example, we can see how the convenience of this method can be used to quickly
        create a new question with a predefined rubric type. This can help simplify your
        implementation of the SDK, if you never plan to use custom rubrics.
        """
        # Create a new rubric from the rubric type
        rubric = Rubric.from_rubric_type(rubric_type)
        return cls(
            body=body,
            example_answer=example_answer,
            rubric=rubric,
        )

    @classmethod
    def from_dict(cls, payload: Dict[str, Union[str, Dict[str, float]]]):
        """Creates a new short answer question from a dictionary.

        Args
        ----
        payload : Dict[str, Union[str, Dict[str, float]]]
            The payload to create the question from.

        Returns
        -------
        ShortAnswerQuestion
            The new short answer question.

        Raises
        ------
        ValidationError
            If the payload is missing any keys.


        This method allows us to define another factory for creating questions. This factory
        allows us to create questions from a dictionary, which can be useful for loading questions
        from a database or other storage medium.

        Example
        -------
        In this example, we can see how we can use this method to create a new question from a
        dictionary::

            from turing import ShortAnswerQuestion, RubricType

            question = "What is the capital of France?"
            example_answer = "Paris"
            rubric = {
                "factual understanding": 1.0,
                "clarity of writing": 0.5,
                "creativity": 0.5,
            }

            serialized_question = {
                "body": question,
                "example_answer": example_answer,
                "rubric": rubric,
            }

            # Create a new question object from the dictionary
            question = ShortAnswerQuestion.from_dict(serialized_question)

        Note, that this method calls the :py:meth:`.Rubric.from_dict` method internally. In
        practice, this means that we can override this method to allow for custom question
        creation regardless of the format of the rubric field of the payload.clear


        Example
        -------
        You can clearly then see a use case for wanting to override this method, if you may
        be receiving question payloads that aren't formatted for the Turing SDK::

            from turing import ShortAnswerQuestion, RubricType

            payload = {
                'body': "What is the capital of France?",
                'answer': "Paris",
                'tags': ["geography", "capitals"],
            }

            class CustomQuestion(ShortAnswerQuestion):

                @classmethod
                def from_dict(cls, payload: Dict[str, Union[str, Dict[str, float]]]):
                    tags = payload.pop('tags', [])
                    if 'geography' in tags:
                        return cls.from_rubric_type(
                            body = payload['body'],
                            example_answer = payload['answer'],
                            rubric_type = RubricType.FACTUAL,
                        )
                    else:
                        return cls.from_rubric_type(
                            body = payload['body'],
                            example_answer = payload['answer'],
                            rubric_type = RubricType.CREATIVITY,
                        )

            question = CustomQuestion.from_dict(payload)
            print(question.rubric.rubric_type) # RubricType.FACTUAL

        Hopefully this example helps to illustrate the flexibility that the SDK provides for
        customizing the question creation process. This flexibility can be leveraged by overriding
        the `from_dict` method to allow for custom question creation, for whatever rubric format
        suits your needs.
        """

        try:
            # Attempt to create the question from the payload
            return cls(
                body=payload["body"],
                example_answer=payload["example_answer"],
                rubric=Rubric.from_dict(  # This call will handle the validation of the rubric
                    payload["rubric"]
                ),
            )
        # If the payload is missing any keys, we will raise a validation error
        except KeyError as exp:
            raise ValidationError("Missing key in payload") from exp
