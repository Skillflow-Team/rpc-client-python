"""This file is responsible for unit testing the RPCClient object.

We primarily want to test for:
    - The intializer is configured correctly to allow overrides of default vals
    - The correct headers are used
    - Payload is serialized correctly
    - Result is deserialized correctly
    - _make_request is called correctly
"""
import os
from uuid import uuid4
from unittest.mock import MagicMock, patch

import pytest

from core.client.client import RPCClient, HOSTED_ENDPOINT
from core.errors import NetworkError, RPCMethodError


def test_init_method():
    """Test that the initializer is configured correctly."""
    # Ensure the default values are functioning correctly
    client = RPCClient()
    assert client.endpoint == HOSTED_ENDPOINT
    assert client.api_key == ""

    # Ensure the endpoint and api_key can be overriden correctly
    os.environ["OVERRIDDEN_ENDPOINT"] = "http://example.com/"
    client = RPCClient(api_key="test-api-key")

    assert client.endpoint == "http://example.com/"
    assert client.api_key == "test-api-key"

    # Cleanup the env varibale used for overriding
    del os.environ["OVERRIDDEN_ENDPOINT"]


def test_headers_property():
    """Test that the headers are correctly initialized."""
    client = RPCClient(api_key="test-api-key")
    headers = client.headers
    assert "Authorization" in headers
    assert headers["Authorization"] == "Bearer test-api-key"


def test_payload_builder():
    """Ensure that the client builds payloads correctly."""
    data = {"test": "data"}
    method = "test_method"
    client = RPCClient()
    payload = client.payload(method, data)
    assert payload["jsonrpc"] == "2.0"
    assert payload["method"] == method
    assert payload["params"] == data
    assert len(payload["id"]) == 36


def test_response_parser():
    """Ensure that the response parser works correctly."""

    response = MagicMock()
    client = RPCClient()

    response_data = {"id": uuid4(), "jsonrpc": "2.0", "result": "test-result"}
    response.json.return_value = response_data
    result = client.parse_response(response)
    assert result == "test-result"

    response_data = {"id": uuid4(), "jsonrpc": "2.0", "error": "test-error"}
    response.json.return_value = response_data
    with pytest.raises(RPCMethodError) as exp:
        client.parse_response(response)
    assert exp.value.args[0] == "test-error"


@patch("requests.post")
def test__make_request(mock_post):
    """Test that the requests are correctly made by the client."""
    method = "test_method"
    params = {"test": "data"}

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": uuid4(),
        "jsonrpc": "2.0",
        "result": "test-result",
    }
    mock_post.return_value = mock_response

    result = RPCClient()._make_request(  # pylint: disable=protected-access
        method, params
    )
    assert result == "test-result"


@patch("requests.post", side_effect=Exception("test-error"))
def test__failed_request(_):
    """Test that the client handles failed requests correctly."""
    method = "test_method"
    params = {"test": "data"}

    with pytest.raises(NetworkError) as exp:
        RPCClient()._make_request(method, params)  # pylint: disable=protected-access
    assert exp.value.args[0] == "Failed to connect to the RPC server: test-error"


@patch("core.client.client.RPCClient._make_request")
def test_short_answer(mock_request):
    """Test the short answer method of the RPCClient."""
    mock_request.return_value = {"feedback": "GOOD JOB!", "score": 3.0}
    client = RPCClient()
    data = "test-data"
    answer = "test-answer"
    feedback, score = client.short_answer(data, answer)
    assert feedback == "GOOD JOB!"
    assert score == 3.0
    assert mock_request.called_once_with("short_answer", [data, answer])
