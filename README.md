# VALR API Python Client

A Python client library for the [VALR](https://www.valr.com) cryptocurrency exchange API.

## Installation

```bash
git clone https://github.com/VALR-Tech/valr_api.git
cd valr_api
python setup.py install
```

## Features

- Full coverage of the VALR API endpoints
- Easy-to-use client with automatic authentication
- Comprehensive error handling
- Support for subaccounts
- Fully typed with modern Python type hints

## Usage Examples

### Initialize Client

```python
from valr_api import ValrClient

# Initialize client with API key and secret
client = ValrClient(api_key="your_api_key", api_secret="your_api_secret")

# For public endpoints only (no authentication)
public_client = ValrClient()
```

### Access Public Information

```python
# Get all supported currencies
currencies = client.public.get_currencies()
print(f"Available currencies: {[c['symbol'] for c in currencies]}")

# Get all currency pairs
pairs = client.public.get_currency_pairs()
print(f"Available trading pairs: {[p['symbol'] for p in pairs]}")

# Get server time
server_time = client.market_data.get_server_time()
print(f"Server time: {server_time['epochTime']}")
```

### Access Market Data

```python
# Get market summary for all pairs
market_summary = client.market_data.get_market_summary()
for market in market_summary:
    print(f"{market['currencyPair']}: Last price {market['lastTradedPrice']}")

# Get orderbook for a specific pair
orderbook = client.market_data.get_orderbook("BTCZAR")
print(f"Top ask: {orderbook['Asks'][0]['price']}")
print(f"Top bid: {orderbook['Bids'][0]['price']}")

# Get recent trades
trades = client.market_data.get_trade_history("BTCZAR", limit=5)
for trade in trades:
    print(f"Trade at {trade['tradedAt']}: {trade['price']} ({trade['takerSide']})")
```

### Access Account Information (Authenticated)

```python
# Get account balances
balances = client.account.get_balances()
for balance in balances:
    if float(balance['total']) > 0:
        print(f"{balance['currency']}: {balance['available']} available, {balance['reserved']} reserved")

# Get transaction history
transactions = client.account.get_transaction_history(limit=10)
for tx in transactions['transactions']:
    print(f"{tx['timestamp']} - {tx['transactionType']}: {tx['amount']} {tx['currency']}")
```

### Wallet Operations (Authenticated)

```python
# Get deposit address
btc_address = client.wallet.get_deposit_address("BTC")
print(f"BTC deposit address: {btc_address['address']}")

# Get deposit history
deposits = client.wallet.get_deposit_history(currency="BTC", limit=5)
for deposit in deposits['deposits']:
    print(f"{deposit['createdAt']} - {deposit['amount']} {deposit['currency']} - {deposit['status']}")

# Request a withdrawal (requires confirmation)
withdrawal = client.wallet.withdraw(
    currency="BTC",
    amount="0.001",
    address="3AfEUyVxPeVZKGBj5sMhGzxKNBKADe2aqT",
    payment_reference="Withdrawal reference"
)
print(f"Withdrawal request created: {withdrawal['id']}")
```

## Error Handling

The client includes proper error handling for API errors:

```python
from valr_api import ValrClient
from valr_api.exceptions import ValrApiError, ValrAuthenticationError

client = ValrClient(api_key="your_api_key", api_secret="your_api_secret")

try:
    # Attempt to access an authenticated endpoint
    balances = client.account.get_balances()
except ValrAuthenticationError as e:
    print(f"Authentication error: {e}")
except ValrApiError as e:
    print(f"API error: {e}")
```

## Documentation

For more detailed documentation, refer to the [VALR API Documentation](https://docs.valr.com/).

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
