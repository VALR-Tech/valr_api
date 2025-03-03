# Installation

## Requirements

- Python 3.8 or higher
- `requests` library

## Install from PyPI

The recommended way to install the VALR API client is via pip:

```bash
pip install valr-api
```

## Install from Source

You can also install the package directly from the source code:

```bash
git clone https://github.com/yourusername/valr-api.git
cd valr-api
pip install -e .
```

## Verify Installation

You can verify that the installation was successful by importing the package in Python:

```python
import valr_api
print(valr_api.__version__)
``` 