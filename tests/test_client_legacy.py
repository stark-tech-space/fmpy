import os
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd

from fmpy.client_legacy import FMPClientLegacy
from fmpy.exceptions import FMPRequestError


class TestFMPClientLegacy(unittest.TestCase):
    """Tests for the FMPClientLegacy class."""

    def setUp(self):
        """Set up test environment."""
        self.api_key = "test_api_key"
        self.client = FMPClientLegacy(api_key=self.api_key)

    def test_init_with_api_key(self):
        """Test initialization with API key."""
        client = FMPClientLegacy(api_key=self.api_key)
        self.assertEqual(client.api_key, self.api_key)

    @patch.dict(os.environ, {"FMP_API_KEY": "env_api_key"})
    def test_init_with_env_var(self):
        """Test initialization with environment variable."""
        client = FMPClientLegacy()
        self.assertEqual(client.api_key, "env_api_key")

    def test_init_without_api_key(self):
        """Test initialization without API key."""
        with patch.dict(os.environ, clear=True):
            with self.assertRaises(ValueError):
                FMPClientLegacy()

    @patch("requests.Session.request")
    def test_get(self, mock_request):
        """Test get method."""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"test": "data"}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Call method
        result = self.client.get("test_endpoint")

        # Check result
        self.assertEqual(result, {"test": "data"})
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(kwargs["params"], {"apikey": self.api_key})

    @patch("requests.Session.request")
    def test_get_with_params(self, mock_request):
        """Test get method with parameters."""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"test": "data"}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Call method
        result = self.client.get("test_endpoint", params={"param1": "value1"})

        # Check result
        self.assertEqual(result, {"test": "data"})
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(kwargs["params"], {"param1": "value1", "apikey": self.api_key})

    @patch("requests.Session.request")
    def test_post(self, mock_request):
        """Test post method."""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"test": "data"}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Call method
        result = self.client.post("test_endpoint", data={"data1": "value1"})

        # Check result
        self.assertEqual(result, {"test": "data"})
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(kwargs["params"], {"apikey": self.api_key})
        self.assertEqual(kwargs["json"], {"data1": "value1"})

    @patch("requests.Session.request")
    def test_request_error(self, mock_request):
        """Test request error handling."""
        # Mock response
        mock_request.side_effect = Exception("Request failed")

        # Call method
        with self.assertRaises(FMPRequestError):
            self.client.get("test_endpoint")

    @patch("requests.Session.request")
    def test_csv_response(self, mock_request):
        """Test CSV response handling."""
        # Mock response
        mock_response = MagicMock()
        mock_response.text = "column1,column2\nvalue1,value2"
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Call method
        result = self.client.get("test_endpoint", expect_csv=True)

        # Check result
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape, (1, 2))
        self.assertEqual(result.iloc[0, 0], "value1")
        self.assertEqual(result.iloc[0, 1], "value2")

    @patch("requests.Session.request")
    def test_bulk_endpoint_access(self, mock_request):
        """Test bulk endpoint access."""
        # Mock response
        mock_response = MagicMock()
        mock_response.text = "symbol,name,price\nAAPL,Apple Inc.,150.00\nMSFT,Microsoft Corporation,300.00"
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Call bulk endpoint method
        result = self.client.bulk.company_profiles(part=0)

        # Check result
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape, (2, 3))
        self.assertEqual(result.iloc[0, 0], "AAPL")
        self.assertEqual(result.iloc[1, 0], "MSFT")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(kwargs["params"], {"part": 0, "apikey": self.api_key})


if __name__ == "__main__":
    unittest.main()
