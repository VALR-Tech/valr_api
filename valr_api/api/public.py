"""
VALR Public API endpoints
"""

from typing import Any, Dict, List, Optional


class PublicAPI:
    """
    VALR Public API endpoints
    """

    def __init__(self, client):
        self.client = client

    def get_currencies(self) -> List[Dict[str, Any]]:
        """
        Get all supported currencies

        Returns:
            List of currency objects

        Example:
            [
                {
                    "symbol": "BTC",
                    "isActive": true,
                    "shortName": "Bitcoin",
                    "longName": "Bitcoin"
                },
                ...
            ]
        """
        return self.client.get("/v1/public/currencies")

    def get_currency_pairs(self) -> List[Dict[str, Any]]:
        """
        Get all supported currency pairs

        Returns:
            List of currency pair objects

        Example:
            [
                {
                    "symbol": "BTCZAR",
                    "baseCurrency": "BTC",
                    "quoteCurrency": "ZAR",
                    "shortName": "BTC/ZAR",
                    "active": true,
                    "minBaseAmount": "0.0001",
                    "maxBaseAmount": "100.0"
                },
                ...
            ]
        """
        return self.client.get("/v1/public/pairs")

    def get_order_types(self, pair: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get supported order types

        Args:
            pair: Currency pair (optional)

        Returns:
            List of order types

        Example:
            [
                {
                    "orderType": "LIMIT",
                    "supportedCurrencyPairs": [
                        "BTCZAR", "ETHZAR", ...
                    ]
                },
                ...
            ]
        """
        if pair:
            return self.client.get(f"/v1/public/{pair}/orderTypes")
        return self.client.get("/v1/public/orderTypes")

    def get_status(self) -> Dict[str, Any]:
        """
        Get VALR API server status

        Returns:
            API status information
        """
        return self.client.get("/v1/public/status")
