"""
VALR Market Data API endpoints
"""

from typing import Any, Dict, List, Optional


class MarketDataAPI:
    """
    VALR Market Data API endpoints
    """

    def __init__(self, client):
        self.client = client

    def get_orderbook(self, pair: str) -> Dict[str, Any]:
        """
        Get the current orderbook for a given currency pair

        Args:
            pair: Currency pair (e.g., BTCZAR)

        Returns:
            Orderbook information

        Example:
            {
                "Asks": [
                    {"price": "10001.0", "quantity": "0.1"},
                    ...
                ],
                "Bids": [
                    {"price": "9999.0", "quantity": "0.1"},
                    ...
                ],
                "LastChange": 123456789
            }
        """
        return self.client.get(f"/v1/marketdata/{pair}/orderbook")

    def get_orderbook_summary(self, pair: str) -> List[Dict[str, Any]]:
        """
        Get a summary of the current orderbook for a given currency pair

        Args:
            pair: Currency pair (e.g., BTCZAR)

        Returns:
            Summary of orderbook
        """
        return self.client.get(f"/v1/marketdata/{pair}/orderbook/summary")

    def get_orderbook_full(self, currency_pair: str) -> Dict[str, Any]:
        """
        Get the full orderbook for a currency pair.

        Args:
            currency_pair (str): Currency pair to get orderbook for.

        Returns:
            dict: Full orderbook.
        """
        endpoint = f"/v1/marketdata/{currency_pair}/orderbook"
        return self.client._get(endpoint=endpoint, auth_type=self.client.BASIC_AUTH)

    def get_trade_history(self, currency_pair: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get trade history for a currency pair.

        Args:
            currency_pair (str): Currency pair to get trade history for.
            limit (int, optional): Number of trades to return. Defaults to 100.

        Returns:
            list: List of trades.
        """
        endpoint = f"/v1/marketdata/{currency_pair}/tradehistory"
        params = {"limit": limit}
        return self.client._get(endpoint=endpoint, params=params, auth_type=self.client.BASIC_AUTH)

    def get_market_summary(self, pair: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get market summary information

        Args:
            pair: Optional currency pair to filter results

        Returns:
            List of market summary objects

        Example:
            [
                {
                    "currencyPair": "BTCZAR",
                    "askPrice": "10000.0",
                    "bidPrice": "9999.0",
                    "lastTradedPrice": "9999.5",
                    "previousClosePrice": "10100.0",
                    "baseVolume": "10.0",
                    "quoteVolume": "100000.0",
                    "high": "10200.0",
                    "low": "9900.0",
                    "created": "2019-08-16T07:22:53.440Z",
                    "changeFromPrevious": "-0.01"
                },
                ...
            ]
        """
        if pair:
            return self.client.get(f"/v1/marketdata/{pair}/marketsummary")
        return self.client.get("/v1/marketdata/marketsummary")

    def get_server_time(self) -> Dict[str, Any]:
        """
        Get the server time.

        Returns:
            dict: Server time.
        """
        endpoint = "/v1/public/time"
        return self.client._get(endpoint=endpoint, auth_type=self.client.BASIC_AUTH)
