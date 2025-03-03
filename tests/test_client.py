"""
Unit tests for VALR API client
"""

import json
import unittest
from unittest.mock import MagicMock, patch

from valr_api.client import ValrClient
from valr_api.exceptions import (
    ValrAuthenticationError,
    ValrRateLimitError,
    ValrRequestError,
    ValrServerError,
)


class TestValrClient(unittest.TestCase):
    """Test VALR API client"""

    def setUp(self):
        """Set up test fixtures"""
        self.api_key = "test_api_key"
        self.api_secret = "test_api_secret"
        self.client = ValrClient(
            api_key=self.api_key,
            api_secret=self.api_secret,
            base_url="https://api.valr.com",
        )

    @patch("valr_api.client.requests.Session.request")
    def test_get_request(self, mock_request):
        """Test GET request"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = json.dumps({"data": "test_data"})
        mock_response.json.return_value = {"data": "test_data"}
        mock_request.return_value = mock_response

        # Make request
        response = self.client.get("/v1/public/currencies")

        # Check response
        self.assertEqual(response, {"data": "test_data"})

        # Check request was made correctly
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(kwargs["method"], "GET")
        self.assertEqual(kwargs["url"], "https://api.valr.com/v1/public/currencies")
        self.assertEqual(kwargs["params"], None)
        self.assertEqual(kwargs["data"], None)

    @patch("valr_api.client.requests.Session.request")
    def test_authenticated_request(self, mock_request):
        """Test authenticated request"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = json.dumps({"data": "test_data"})
        mock_response.json.return_value = {"data": "test_data"}
        mock_request.return_value = mock_response

        # Make request
        response = self.client.get("/v1/account/balances", auth_required=True)

        # Check response
        self.assertEqual(response, {"data": "test_data"})

        # Check request was made correctly
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(kwargs["method"], "GET")
        self.assertEqual(kwargs["url"], "https://api.valr.com/v1/account/balances")
        self.assertEqual(kwargs["params"], None)
        self.assertEqual(kwargs["data"], None)

        # Check auth headers were included
        headers = kwargs["headers"]
        self.assertEqual(headers["X-VALR-API-KEY"], self.api_key)
        self.assertIn("X-VALR-SIGNATURE", headers)
        self.assertIn("X-VALR-TIMESTAMP", headers)

    @patch("valr_api.client.requests.Session.request")
    def test_authentication_error(self, mock_request):
        """Test authentication error"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 401
        mock_response.text = "Authentication failed"
        mock_request.return_value = mock_response

        # Make request and check exception
        with self.assertRaises(ValrAuthenticationError):
            self.client.get("/v1/account/balances", auth_required=True)

    @patch("valr_api.client.requests.Session.request")
    def test_rate_limit_error(self, mock_request):
        """Test rate limit error"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 429
        mock_response.text = "Rate limit exceeded"
        mock_request.return_value = mock_response

        # Make request and check exception
        with self.assertRaises(ValrRateLimitError):
            self.client.get("/v1/public/currencies")

    @patch("valr_api.client.requests.Session.request")
    def test_server_error(self, mock_request):
        """Test server error"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 500
        mock_response.text = "Server error"
        mock_request.return_value = mock_response

        # Make request and check exception
        with self.assertRaises(ValrServerError):
            self.client.get("/v1/public/currencies")

    @patch("valr_api.client.requests.Session.request")
    def test_request_error(self, mock_request):
        """Test request error"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 400
        mock_response.text = "Bad request"
        mock_request.return_value = mock_response

        # Make request and check exception
        with self.assertRaises(ValrRequestError):
            self.client.get("/v1/public/currencies")


if __name__ == "__main__":
    unittest.main()
