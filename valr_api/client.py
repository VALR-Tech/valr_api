"""
VALR API client
"""

import json
import logging
import time
from typing import Any, Dict, List, Optional, Union, cast

import requests

from valr_api.api.account import AccountAPI
from valr_api.api.market_data import MarketDataAPI
from valr_api.api.public import PublicAPI
from valr_api.api.wallet import WalletAPI
from valr_api.exceptions import (
    ValrApiError,
    ValrAuthenticationError,
    ValrRateLimitError,
    ValrRequestError,
    ValrServerError,
)
from valr_api.utils.auth import generate_signature, get_timestamp


class ValrClient:
    """
    VALR API client

    Args:
        api_key: VALR API key
        api_secret: VALR API secret
        base_url: VALR API base URL (defaults to https://api.valr.com)
        timeout: Request timeout in seconds
    """

    # Authentication types
    BASIC_AUTH = "BASIC"
    SIGNED_AUTH = "SIGNED"

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        base_url: str = "https://api.valr.com",
        timeout: int = 30,
    ):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)

        # Initialize API endpoints
        self.public = PublicAPI(self)
        self.market_data = MarketDataAPI(self)

        # These endpoints require authentication
        if api_key and api_secret:
            self.account = AccountAPI(self)
            self.wallet = WalletAPI(self)

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        auth_required: bool = False,
        subaccount_id: Optional[str] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Make request to VALR API

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            params: URL parameters
            data: Request body for POST/PUT requests
            auth_required: Whether authentication is required
            subaccount_id: Optional subaccount ID for requests

        Returns:
            Response from API as dictionary or list

        Raises:
            ValrAuthenticationError: If authentication fails
            ValrRequestError: If request is invalid
            ValrRateLimitError: If rate limit is exceeded
            ValrServerError: If server error occurs
            ValrApiError: For any other API error
        """
        url = f"{self.base_url}{endpoint}"

        headers = {}

        if auth_required:
            if not self.api_key or not self.api_secret:
                raise ValrAuthenticationError(
                    "API key and secret are required for authenticated endpoints"
                )

            timestamp = get_timestamp()
            signature = generate_signature(
                self.api_secret,
                timestamp,
                method,
                endpoint,
                data,
            )

            headers.update(
                {
                    "X-VALR-API-KEY": self.api_key,
                    "X-VALR-SIGNATURE": signature,
                    "X-VALR-TIMESTAMP": str(timestamp),
                }
            )

            if subaccount_id:
                headers["X-VALR-SUBACCOUNT-ID"] = subaccount_id

        if data is not None:
            headers["Content-Type"] = "application/json"
            data_str = json.dumps(data)
        else:
            data_str = None

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                data=data_str,
                timeout=self.timeout,
            )

            # Log request details in debug mode
            self.logger.debug(f"Request: {method} {url} {params} {data}")
            self.logger.debug(f"Response: {response.status_code} {response.text}")

            # Handle error responses
            if not response.ok:
                if response.status_code == 401:
                    raise ValrAuthenticationError(
                        f"Authentication failed: {response.text}",
                        status_code=response.status_code,
                        response=response.text,
                    )
                elif response.status_code == 429:
                    raise ValrRateLimitError(
                        f"Rate limit exceeded: {response.text}",
                        status_code=response.status_code,
                        response=response.text,
                    )
                elif 400 <= response.status_code < 500:
                    raise ValrRequestError(
                        f"Request error: {response.text}",
                        status_code=response.status_code,
                        response=response.text,
                    )
                elif response.status_code >= 500:
                    raise ValrServerError(
                        f"Server error: {response.text}",
                        status_code=response.status_code,
                        response=response.text,
                    )
                else:
                    raise ValrApiError(
                        f"API error: {response.text}",
                        status_code=response.status_code,
                        response=response.text,
                    )

            # Return response data
            if response.text:
                return cast(Union[Dict[str, Any], List[Dict[str, Any]]], response.json())
            return {}

        except requests.RequestException as e:
            raise ValrApiError(f"Request failed: {str(e)}")

    def get(
        self,
        endpoint: str,
        params: Optional[Dict] = None,
        auth_required: bool = False,
        subaccount_id: Optional[str] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Make GET request to VALR API
        """
        return self._request(
            "GET",
            endpoint,
            params=params,
            auth_required=auth_required,
            subaccount_id=subaccount_id,
        )

    def post(
        self,
        endpoint: str,
        data: Dict,
        params: Optional[Dict] = None,
        auth_required: bool = True,
        subaccount_id: Optional[str] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Make POST request to VALR API
        """
        return self._request(
            "POST",
            endpoint,
            params=params,
            data=data,
            auth_required=auth_required,
            subaccount_id=subaccount_id,
        )

    def put(
        self,
        endpoint: str,
        data: Dict,
        params: Optional[Dict] = None,
        auth_required: bool = True,
        subaccount_id: Optional[str] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Make PUT request to VALR API
        """
        return self._request(
            "PUT",
            endpoint,
            params=params,
            data=data,
            auth_required=auth_required,
            subaccount_id=subaccount_id,
        )

    def delete(
        self,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        auth_required: bool = True,
        subaccount_id: Optional[str] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Make DELETE request to VALR API
        """
        return self._request(
            "DELETE",
            endpoint,
            params=params,
            data=data,
            auth_required=auth_required,
            subaccount_id=subaccount_id,
        )

    def _handle_response(self, response) -> Dict[str, Any]:
        """
        Handle the response from the API.

        Args:
            response (requests.Response): Response from the API.

        Returns:
            dict: Response data.

        Raises:
            ValrRequestException: If the request fails.
        """
        if response.status_code == 200:
            return cast(Dict[str, Any], response.json())

        error_message = f"Request failed with status code {response.status_code}"

        try:
            error_data = response.json()
            if "message" in error_data:
                error_message = error_data["message"]
        except ValueError:
            pass

        if response.status_code == 401:
            raise ValrAuthenticationError(error_message)
        elif response.status_code == 429:
            raise ValrRateLimitError(error_message)
        elif 400 <= response.status_code < 500:
            raise ValrRequestError(error_message)
        else:
            raise ValrServerError(error_message)

    def _get_headers(self, auth_type: str, endpoint: str, params=None, data=None) -> Dict[str, str]:
        """
        Get the headers for the request.

        Args:
            auth_type (str): Authentication type.
            endpoint (str): API endpoint.
            params (dict, optional): Query parameters. Defaults to None.
            data (dict, optional): Request data. Defaults to None.

        Returns:
            dict: Headers for the request.
        """
        headers = {"Accept": "application/json", "Content-Type": "application/json"}

        if (
            auth_type == self.SIGNED_AUTH
            and self.api_secret is not None
            and self.api_key is not None
        ):
            timestamp = int(time.time() * 1000)
            signature = generate_signature(
                api_secret=self.api_secret,
                timestamp=timestamp,
                verb="GET",
                path=endpoint,
                body=data,
            )

            headers.update(
                {
                    "X-VALR-API-KEY": self.api_key,
                    "X-VALR-SIGNATURE": signature,
                    "X-VALR-TIMESTAMP": str(timestamp),
                }
            )

        return headers

    def _get(
        self,
        endpoint: str,
        params: Optional[Dict] = None,
        auth_type: Optional[str] = None,
        subaccount_id: Optional[str] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Make a GET request to the API.

        Args:
            endpoint (str): API endpoint.
            params (dict, optional): Query parameters. Defaults to None.
            auth_type (str, optional): Authentication type. Defaults to None.
            subaccount_id (str, optional): Subaccount ID. Defaults to None.

        Returns:
            Union[Dict, List]: Response data.
        """
        if auth_type is None:
            auth_type = self.BASIC_AUTH

        headers = self._get_headers(auth_type, endpoint, params)

        if subaccount_id:
            headers["X-VALR-SUBACCOUNT-ID"] = subaccount_id

        response = self.session.get(
            f"{self.base_url}{endpoint}",
            params=params,
            headers=headers,
            timeout=self.timeout,
        )

        return cast(Union[Dict[str, Any], List[Dict[str, Any]]], self._handle_response(response))
