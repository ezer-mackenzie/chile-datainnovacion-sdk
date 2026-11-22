from __future__ import annotations

from types import TracebackType
from typing import Self

import httpx

from chile_datainnovacion_sdk.config import ClientConfig
from chile_datainnovacion_sdk.constants import DEFAULT_BASE_URL, PUBLIC_API_TOKEN
from chile_datainnovacion_sdk.errors import DataInnovacionConnectionError
from chile_datainnovacion_sdk.models import Project
from chile_datainnovacion_sdk.services import ProjectsService
from chile_datainnovacion_sdk.typed import (
    InterventionType,
    ProjectStatus,
    Sustainability,
)


class ChileDataInnovacionClient:
    """Synchronous client for the public Data Innovacion projects API."""

    def __init__(
        self,
        *,
        token: str | None = None,
        api_token: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        config: ClientConfig | None = None,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        if config is not None and (
            token is not None or api_token is not None or base_url != DEFAULT_BASE_URL
        ):
            raise ValueError("Pass config or token/base_url, not both")
        if config is None:
            config = ClientConfig(
                base_url=base_url,
                api_token=api_token if api_token is not None else token,
            )
        resolved_token = config.api_token if config.api_token is not None else PUBLIC_API_TOKEN
        projects_url = f"{config.base_url.rstrip('/')}/v1/proyectos"
        headers = {
            "Accept": "application/json",
            "Authorization": resolved_token,
            "User-Agent": config.user_agent,
        }
        self.config = config
        self._http = httpx.Client(
            headers=headers,
            timeout=httpx.Timeout(
                connect=config.connect_timeout,
                read=config.timeout,
                write=config.timeout,
                pool=config.timeout,
            ),
            verify=config.verify,
            follow_redirects=False,
            trust_env=False,
            transport=transport,
        )

        self.projects = ProjectsService(self._http, projects_url)

    @property
    def is_closed(self) -> bool:
        return self._http.is_closed

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> Self:
        if self.is_closed:
            raise DataInnovacionConnectionError("Client is closed")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def list_projects(
        self,
        *,
        code: str | None = None,
        beneficiary_rut: str | None = None,
        intervention_type: InterventionType | None = None,
        data_status: ProjectStatus | None = None,
        sustainable: Sustainability | None = None,
        award_year: int | str | None = None,
        limit: int | None = None,
        **filters: str | int,
    ) -> list[Project]:
        return self.projects.list(
            code=code,
            beneficiary_rut=beneficiary_rut,
            intervention_type=intervention_type,
            data_status=data_status,
            sustainable=sustainable,
            award_year=award_year,
            limit=limit,
            **filters,
        )

    def get_project(self, code: str) -> Project | None:
        return self.projects.get(code)
