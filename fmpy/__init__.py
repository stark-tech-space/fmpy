"""
FMPY: Python SDK for Financial Modeling Prep API
================================================

A Python wrapper for the Financial Modeling Prep API that provides
easy access to financial data, stock quotes, and company information.

Example:
    >>> import fmpy
    >>> client = fmpy.Client(api_key="your_api_key")
    >>> apple_profile = client.company.profile("AAPL")
    >>> apple_quote = client.quote.real_time("AAPL")
"""

__version__ = "0.1.0"

from .client import FMPClient
from .exceptions import FMPError, FMPRequestError, FMPAPIError, FMPValidationError
from .utils import (
    validate_date,
    format_date,
    validate_symbols,
    response_to_df,
    clean_params,
)

# Create a more user-friendly alias
Client = FMPClient

__all__ = [
    "Client",
    "FMPClient",
    "FMPError",
    "FMPRequestError",
    "FMPAPIError",
    "FMPValidationError",
    "validate_date",
    "format_date",
    "validate_symbols",
    "response_to_df",
    "clean_params",
]
