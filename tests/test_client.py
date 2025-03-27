import os
import unittest
from unittest.mock import patch, MagicMock

import requests
import fmpy
from fmpy.exceptions import FMPRequestError, FMPAPIError


class TestFMPClient(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.client = fmpy.Client(api_key=self.api_key)

    def test_init_with_api_key(self):
        client = fmpy.Client(api_key="my_test_key")
        self.assertEqual(client.api_key, "my_test_key")

    @patch.dict(os.environ, {"FMP_API_KEY": "env_test_key"})
    def test_init_with_env_var(self):
        client = fmpy.Client()
        self.assertEqual(client.api_key, "env_test_key")

    def test_init_without_api_key(self):
        with patch.dict(os.environ, clear=True):
            with self.assertRaises(ValueError):
                fmpy.Client()

    def test_get_url(self):
        url = self.client._get_url("test-endpoint")
        self.assertEqual(url, "https://financialmodelingprep.com/stable/test-endpoint")

    def test_add_api_key_empty_params(self):
        params = {}
        result = self.client._add_api_key(params)
        self.assertEqual(result, {"apikey": self.api_key})

    def test_add_api_key_with_params(self):
        params = {"param1": "value1", "param2": "value2"}
        result = self.client._add_api_key(params)
        self.assertEqual(
            result, {"param1": "value1", "param2": "value2", "apikey": self.api_key}
        )

    @patch("requests.Session.request")
    def test_request_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"key": "value"}
        mock_request.return_value = mock_response

        response = self.client._request("GET", "test-endpoint")

        self.assertEqual(response, {"key": "value"})
        mock_request.assert_called_once()

    @patch("requests.Session.request")
    def test_request_http_error(self, mock_request):
        # Use a requests-specific exception
        mock_request.side_effect = requests.exceptions.RequestException(
            "Request failed"
        )

        with self.assertRaises(FMPRequestError):
            self.client._request("GET", "test-endpoint")

    @patch("requests.Session.request")
    def test_request_json_error(self, mock_request):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.text = "Not JSON"
        mock_request.return_value = mock_response

        with self.assertRaises(FMPAPIError):
            self.client._request("GET", "test-endpoint")

    def test_endpoint_properties(self):
        """Test all endpoint properties return the correct objects"""
        self.assertIsNotNone(self.client.search)
        self.assertIsNotNone(self.client.company)
        self.assertIsNotNone(self.client.quote)
        self.assertIsNotNone(self.client.chart)
        self.assertIsNotNone(self.client.statements)
        self.assertIsNotNone(self.client.analyst)
        self.assertIsNotNone(self.client.calendar)
        self.assertIsNotNone(self.client.news)
        self.assertIsNotNone(self.client.etf)
        self.assertIsNotNone(self.client.crypto)
        self.assertIsNotNone(self.client.forex)
        self.assertIsNotNone(self.client.sec)
        self.assertIsNotNone(self.client.bulk)


if __name__ == "__main__":
    unittest.main()
