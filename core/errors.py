"""This file defines the custom error objects that are defined in the client library."""

from pydantic_core import ValidationError as PydanticValidationError


class CoreError(Exception):
    """A generic error that is raised when an unexpected error occurs in the client library."""

    def __init__(self, message: str):
        self.message = message


class ValidationError(CoreError):
    """An error that is raised when a validation error occurs in the client library."""

    @classmethod
    def from_pydantic(cls, exp: PydanticValidationError) -> "ValidationError":
        """Creates a ValidationError from a PydanticValidationError."""
        return cls(exp.json())


class NetworkError(CoreError):
    """An error that is raised when a network error occurs in the client library."""


class RPCMethodError(CoreError):
    """An error that is raised when there is an error during the execution of an RPC method."""

    @classmethod
    def from_response_payload(cls, response_data: dict) -> "RPCMethoError":
        """Creates an RPCMethodError from a response."""
        return cls(response_data["error"])
