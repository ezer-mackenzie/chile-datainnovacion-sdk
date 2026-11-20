"""Unofficial typed SDK for the Chile Data Innovacion projects API."""

from chile_datainnovacion_sdk import constants
from chile_datainnovacion_sdk.client import (
    ChileDataInnovacionClient,
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
from chile_datainnovacion_sdk.typed import (
    InterventionType,
    ProjectStatus,
    Sustainability,
)

__version__ = constants.SDK_VERSION

__all__ = [
    "ChileDataInnovacionClient",
    "ChileDataInnovacionError",
    "ClientConfig",
    "DataInnovacionConnectionError",
    "DataInnovacionError",
    "DataInnovacionHTTPError",
    "DataInnovacionProjectDTO",
    "DataInnovacionProtocolError",
    "DataInnovacionTimeoutError",
    "InterventionType",
    "Project",
    "ProjectStatus",
    "ProjectsService",
    "Sustainability",
    "__version__",
    "constants",
]
