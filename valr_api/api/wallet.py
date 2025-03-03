"""
VALR Wallet API endpoints
"""

from typing import Any, Dict, Optional


class WalletAPI:
    """
    VALR Wallet API endpoints
    """

    def __init__(self, client):
        self.client = client

    def get_deposit_address(
        self, currency: str, subaccount_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get deposit address for a currency

        Args:
            currency: Currency code (e.g., BTC)
            subaccount_id: Optional subaccount ID

        Returns:
            Deposit address information

        Example:
            {
                "currency": "BTC",
                "address": "3AfEUyVxPeVZKGBj5sMhGzxKNBKADe2aqT",
                "tag": null
            }
        """
        return self.client.get(
            f"/v1/wallet/crypto/{currency}/deposit/address",
            auth_required=True,
            subaccount_id=subaccount_id,
        )

    def get_deposit_history(
        self,
        currency: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
        subaccount_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get deposit history

        Args:
            currency: Filter by currency code (optional)
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            subaccount_id: Optional subaccount ID

        Returns:
            Dictionary containing deposit history and pagination info

        Example:
            {
                "deposits": [
                    {
                        "currency": "BTC",
                        "receiveAddress": "3AfEUyVxPeVZKGBj5sMhGzxKNBKADe2aqT",
                        "amount": "0.1",
                        "transactionHash": "...",
                        "status": "COMPLETED",
                        "createdAt": "2019-06-28T10:01:09.465Z",
                        ...
                    },
                    ...
                ],
                "isLastPage": true
            }
        """
        params = {
            "skip": skip,
            "limit": limit,
        }

        if currency:
            endpoint = f"/v1/wallet/crypto/{currency}/deposit/history"
        else:
            endpoint = "/v1/wallet/crypto/deposit/history"

        return self.client.get(
            endpoint,
            params=params,
            auth_required=True,
            subaccount_id=subaccount_id,
        )

    def withdraw(
        self,
        currency: str,
        amount: str,
        address: str,
        payment_reference: Optional[str] = None,
        tag: Optional[str] = None,
        subaccount_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Withdraw cryptocurrency

        Args:
            currency: Currency code (e.g., BTC)
            amount: Amount to withdraw
            address: Withdrawal address
            payment_reference: Optional payment reference
            tag: Optional destination tag (for currencies like XRP)
            subaccount_id: Optional subaccount ID

        Returns:
            Withdrawal information

        Example:
            {
                "id": "123456",
                "fee": "0.0001",
                "currency": "BTC",
                "amount": "0.1",
                "status": "PENDING",
                ...
            }
        """
        data = {
            "amount": amount,
            "address": address,
        }

        if payment_reference:
            data["paymentReference"] = payment_reference

        if tag:
            data["destinationTag"] = tag

        return self.client.post(
            f"/v1/wallet/crypto/{currency}/withdraw",
            data=data,
            auth_required=True,
            subaccount_id=subaccount_id,
        )

    def get_withdrawal_history(
        self,
        currency: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
        subaccount_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get withdrawal history

        Args:
            currency: Filter by currency code (optional)
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            subaccount_id: Optional subaccount ID

        Returns:
            Dictionary containing withdrawal history and pagination info

        Example:
            {
                "withdrawals": [
                    {
                        "currency": "BTC",
                        "address": "3AfEUyVxPeVZKGBj5sMhGzxKNBKADe2aqT",
                        "amount": "0.1",
                        "fee": "0.0001",
                        "transactionHash": "...",
                        "status": "COMPLETED",
                        "createdAt": "2019-06-28T10:01:09.465Z",
                        ...
                    },
                    ...
                ],
                "isLastPage": true
            }
        """
        params = {
            "skip": skip,
            "limit": limit,
        }

        if currency:
            endpoint = f"/v1/wallet/crypto/{currency}/withdraw/history"
        else:
            endpoint = "/v1/wallet/crypto/withdraw/history"

        return self.client.get(
            endpoint,
            params=params,
            auth_required=True,
            subaccount_id=subaccount_id,
        )
