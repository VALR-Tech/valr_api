"""
Custom exceptions for VALR API client
"""


class ValrApiError(Exception):
    """Base exception for VALR API errors"""

    def __init__(self, message=None, status_code=None, response=None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class ValrAuthenticationError(ValrApiError):
    """Exception raised for authentication errors"""

    pass


class ValrRateLimitError(ValrApiError):
    """Exception raised when API rate limit is exceeded"""

    pass


class ValrServerError(ValrApiError):
    """Exception raised for VALR server errors (5xx status codes)"""

    pass


class ValrRequestError(ValrApiError):
    """Exception raised for client request errors (4xx status codes)"""

    pass
