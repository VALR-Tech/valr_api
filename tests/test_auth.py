"""
Unit tests for VALR API auth utilities
"""

import unittest
from unittest.mock import patch

from valr_api.utils.auth import generate_signature, get_timestamp


class TestAuthUtilities(unittest.TestCase):
    """Test VALR API auth utilities"""

    def test_generate_signature(self):
        """Test generate_signature function"""
        # Test data from VALR API docs
        api_secret = "2b286ac2291bfdc9fce6b7294d0efbcc5b18925"
        timestamp = 1643102132854
        verb = "GET"
        path = "/v1/account/balances"
        body = None

        # Generate signature
        signature = generate_signature(api_secret, timestamp, verb, path, body)

        # Verify the signature format (base64 encoded)
        self.assertTrue(len(signature) > 0)

        # Test with request body
        body = {"orderId": "123456", "amount": "0.1"}
        signature_with_body = generate_signature(
            api_secret, timestamp, "POST", "/v1/orders/limit", body
        )

        # Verify the signature format
        self.assertTrue(len(signature_with_body) > 0)

        # Ensure signatures are different
        self.assertNotEqual(signature, signature_with_body)

    @patch("time.time")
    def test_get_timestamp(self, mock_time):
        """Test get_timestamp function"""
        # Mock time.time() to return a fixed value
        mock_time.return_value = 1643102132.854

        # Get timestamp
        timestamp = get_timestamp()

        # Verify timestamp is in milliseconds
        self.assertEqual(timestamp, 1643102132854)


if __name__ == "__main__":
    unittest.main()
