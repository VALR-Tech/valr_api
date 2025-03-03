"""
VALR Account API endpoints
"""

from typing import Any, Dict, List, Optional, cast


class AccountAPI:
    """
    VALR Account API endpoints
    """

    def __init__(self, client):
        self.client = client

    def get_balances(self, subaccount_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get the account balances

        Args:
            subaccount_id: Optional subaccount ID

        Returns:
            List of account balances

        Example:
            [
                {
                    "currency": "BTC",
                    "available": "0.1",
                    "reserved": "0.0",
                    "total": "0.1"
                },
                ...
            ]
        """
        endpoint = "/v1/account/balances"
        return cast(
            List[Dict[str, Any]],
            self.client._get(
                endpoint=endpoint,
                auth_type=self.client.SIGNED_AUTH,
                subaccount_id=subaccount_id,
            ),
        )

    def get_transaction_history(
        self,
        skip: int = 0,
        limit: int = 10,
        transaction_types: Optional[List[str]] = None,
        currency: Optional[str] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        subaccount_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get transaction history.

        Args:
            skip (int, optional): Number of transactions to skip. Defaults to 0.
            limit (int, optional): Number of transactions to return. Defaults to 10.
            transaction_types (List[str], optional): Types of transactions to return
                Defaults to None.
            currency (str, optional): Currency to filter by. Defaults to None.
            start_time (int, optional): Start time in milliseconds. Defaults to None.
            end_time (int, optional): End time in milliseconds. Defaults to None.
            subaccount_id (str, optional): Subaccount ID. Defaults to None.

        Returns:
            list: List of transactions.
        """
        endpoint = "/v1/account/transactionhistory"
        params: Dict[str, Any] = {
            "skip": skip,
            "limit": limit,
        }

        if transaction_types:
            params["transactionTypes"] = ",".join(transaction_types)

        if currency:
            params["currency"] = currency

        if start_time:
            params["startTime"] = start_time

        if end_time:
            params["endTime"] = end_time

        return cast(
            List[Dict[str, Any]],
            self.client._get(
                endpoint=endpoint,
                params=params,
                auth_type=self.client.SIGNED_AUTH,
                subaccount_id=subaccount_id,
            ),
        )

    def get_trade_history(
        self,
        pair: str,
        skip: int = 0,
        limit: int = 100,
        subaccount_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get trade history for a specific currency pair

        Args:
            pair: Currency pair (e.g., BTCZAR)
            skip: Number of trades to skip (for pagination)
            limit: Maximum number of trades to return (default is 100, max is 100)
            subaccount_id: Optional subaccount ID

        Returns:
            Dictionary containing trade history and pagination info

        Example:
            {
                "trades": [
                    {
                        "price": "9999.0",
                        "quantity": "0.001",
                        "currencyPair": "BTCZAR",
                        "tradedAt": "2019-06-28T10:01:09.465Z",
                        "side": "buy",
                        "orderId": "123456",
                        ...
                    },
                    ...
                ],
                "isLastPage": true
            }
        """
        endpoint = f"/v1/account/{pair}/tradehistory"
        params = {
            "skip": skip,
            "limit": limit,
        }

        return cast(
            Dict[str, Any],
            self.client._get(
                endpoint=endpoint,
                params=params,
                auth_type=self.client.SIGNED_AUTH,
                subaccount_id=subaccount_id,
            ),
        )

    def get_subaccounts(self) -> List[Dict[str, Any]]:
        """
        Get all subaccounts

        Returns:
            List of subaccounts

        Example:
            [
                {
                    "id": "123456",
                    "label": "Trading Account",
                    "isDefault": true,
                    ...
                },
                ...
            ]
        """
        return cast(
            List[Dict[str, Any]],
            self.client._get("/v1/account/subaccounts", auth_type=self.client.SIGNED_AUTH),
        )

    def get_trade_history_by_currency_pair(
        self, currency_pair: str, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get trade history by currency pair.

        Args:
            currency_pair (str): Currency pair to get trade history for.
            limit (int, optional): Number of trades to return. Defaults to 10.

        Returns:
            list: List of trades.
        """
        endpoint = f"/v1/account/{currency_pair}/tradehistory"
        params = {"limit": limit}
        return cast(
            List[Dict[str, Any]],
            self.client._get(endpoint=endpoint, params=params, auth_type=self.client.SIGNED_AUTH),
        )
