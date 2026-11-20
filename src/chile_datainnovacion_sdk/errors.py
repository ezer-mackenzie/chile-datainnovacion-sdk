class ChileDataInnovacionError(Exception):
    """Base exception for Data Innovacion SDK failures."""


class DataInnovacionError(ChileDataInnovacionError):
    """Base exception for Data Innovacion API failures."""


class DataInnovacionHTTPError(DataInnovacionError):
    """The API returned an unsuccessful HTTP response."""

    def __init__(self, message: str, *, status_code: int) -> None:
        super().__init__(message)
        self.status_code = status_code


class DataInnovacionTimeoutError(DataInnovacionError):
    """The API request timed out."""


class DataInnovacionConnectionError(DataInnovacionError):
    """The HTTP connection could not be completed."""


class DataInnovacionProtocolError(DataInnovacionError):
    """The API response did not match the expected JSON envelope."""
