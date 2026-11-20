"""Unofficial typed SDK for the Chile Data Innovacion projects API."""

from chile_datainnovacion_sdk import constants
from chile_datainnovacion_sdk.client import (
    ChileDataInnovacionClient,
    DataInnovacionClient,
    DataInnovacionSDKClient,
    ProjectsService,
)
from chile_datainnovacion_sdk.config import ClientConfig
from chile_datainnovacion_sdk.errors import (
    ChileDataInnovacionError,
    DataInnovacionConnectionError,
    DataInnovacionError,
    DataInnovacionHTTPError,
    DataInnovacionProtocolError,
    DataInnovacionTimeoutError,
)
from chile_datainnovacion_sdk.models import (
    DataInnovacionProjectDTO,
    Project,
)

__version__ = constants.SDK_VERSION

__all__ = [
    "ChileDataInnovacionClient",
    "ChileDataInnovacionError",
    "ClientConfig",
    "DataInnovacionClient",
    "DataInnovacionConnectionError",
    "DataInnovacionError",
    "DataInnovacionHTTPError",
    "DataInnovacionProjectDTO",
    "DataInnovacionProtocolError",
    "DataInnovacionSDKClient",
    "DataInnovacionTimeoutError",
    "Project",
    "ProjectsService",
    "__version__",
    "constants",
]
