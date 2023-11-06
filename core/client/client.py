"""This file defines the RPC client, which connects to the RPC server."""
import os
from typing import Any, Dict, List, Union

import requests

HOSTED_ENDPOINT = "http://18.118.162.4/"


class RPCClient:
    """The RPC client is responsible for making requests to the RPC server."""

    def __init__(self, api_key: str = None):
        # Setup the endpoint value.
        if os.environ.get("OVERRIDDEN_ENDPOINT", False):
            # If the endpoint is overridden in .env, use that one
            endpoint = os.environ["OVERRIDDEN_ENDPOINT"]
        else:
            # Otherwise, use the standard hosted endpoint
            endpoint = HOSTED_ENDPOINT
        self.endpoint = endpoint

        # Setup the API Key value.
        if api_key:
            # If the api_key is passed as a kwarg, use that one
            self.api_key = api_key
        else:
            # If the api_key is not passed as a kwarg, use the one in .env
            self.api_key = os.environ.get("TURING_API_KEY", "")

    @property
    def headers(self) -> Dict[str, str]:
        """Return the headers for the request."""
        return {"Authorization": f"Bearer {self.api_key}"}

    def payload(self, method: str, params: Any) -> Dict[str, Any]:
        """Return the payload for the request."""
        return {
            "id": 1,
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
        }

    def parse_response(self, response: requests.Response) -> Dict[str, Any]:
        """Parse the response from the RPC server."""
        response_data = response.json()
        if "error" in response_data:
            raise Exception(  # pylint: disable=broad-exception-raised
                response_data["error"]
            )
        result = response_data["result"]
        return result

    def _make_request(
        self, method: str, params: Union[Dict, List] = None
    ) -> requests.Response:
        """Make a request to the RPC server."""
        payload = self.payload(method, params)
        response = requests.post(
            self.endpoint, json=payload, headers=self.headers, timeout=10
        )

        result = self.parse_response(response)
        return result

    def short_answer(self, data: Any, answer: str) -> bool:
        """Send a short answer to the server."""
        result = self._make_request("short_answer", [data, answer])
        feedback, score = result["feedback"], result["score"]
        return feedback, score
