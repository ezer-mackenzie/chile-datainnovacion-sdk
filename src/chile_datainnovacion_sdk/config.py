from dataclasses import dataclass
from math import isfinite

from chile_datainnovacion_sdk.constants import DEFAULT_BASE_URL, SDK_VERSION


@dataclass(frozen=True, slots=True)
class ClientConfig:
    base_url: str = DEFAULT_BASE_URL
    api_token: str | None = None
    timeout: float = 30.0
    connect_timeout: float = 10.0
    verify: bool = True
    user_agent: str = f"chile-datainnovacion-sdk/{SDK_VERSION}"

    def __post_init__(self) -> None:
        if not self.base_url or not self.base_url.strip():
            raise ValueError("base_url must not be empty")
        if (
            isinstance(self.timeout, bool)
            or isinstance(self.connect_timeout, bool)
            or not isfinite(self.timeout)
            or not isfinite(self.connect_timeout)
            or self.timeout <= 0
            or self.connect_timeout <= 0
        ):
            raise ValueError("timeouts must be finite values greater than zero")
