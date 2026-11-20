from __future__ import annotations

import builtins
from collections.abc import Mapping
from types import TracebackType
from typing import Any, Self

import httpx
from pydantic import JsonValue

from chile_datainnovacion_sdk.config import ClientConfig
from chile_datainnovacion_sdk.constants import DEFAULT_BASE_URL, PUBLIC_API_TOKEN
from chile_datainnovacion_sdk.errors import (
    DataInnovacionConnectionError,
    DataInnovacionHTTPError,
    DataInnovacionProtocolError,
    DataInnovacionTimeoutError,
)
from chile_datainnovacion_sdk.models import Project
from chile_datainnovacion_sdk.typed import (
    InterventionType,
    ProjectStatus,
    Sustainability,
)

API_FILTER_NAMES = {
    "code": "codigo",
    "beneficiary_rut": "rut_beneficiario",
    "intervention_type": "tipo_intervencion",
    "data_status": "estado_data",
    "sustainable": "sostenible",
    "award_year": "año_adjudicacion",
}


class ProjectsService:
    def __init__(self, http: httpx.Client, projects_url: str) -> None:
        self._http = http
        self._projects_url = projects_url

    def list(
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
    ) -> builtins.list[Project]:
        params: dict[str, str | int] = {}
        known_filters = {
            "codigo": code,
            "rut_beneficiario": beneficiary_rut,
            "tipo_intervencion": intervention_type,
            "estado_data": data_status,
            "sostenible": sustainable,
            "año_adjudicacion": award_year,
        }
        for name, value in known_filters.items():
            if value is not None:
                params[f"filter[{name}]"] = str(value)
        for name, value in filters.items():
            if name.startswith("filter[") and name.endswith("]"):
                api_name = name
            else:
                api_name = f"filter[{API_FILTER_NAMES.get(name, name)}]"
            params[api_name] = value
        if limit is not None:
            if type(limit) is not int or limit < 1:
                raise ValueError("limit must be a positive integer")
            params["limit"] = limit
        return self._request(params)

    def get(self, code: str) -> Project | None:
        projects = self.list(code=code)
        for project in projects:
            if project.code == code:
                return project
        return None

    def search(
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
    ) -> builtins.list[Project]:
        return self.list(
            code=code,
            beneficiary_rut=beneficiary_rut,
            intervention_type=intervention_type,
            data_status=data_status,
            sustainable=sustainable,
            award_year=award_year,
            limit=limit,
            **filters,
        )

    def _request(self, params: Mapping[str, str | int]) -> builtins.list[Project]:
        if self._http.is_closed:
            raise DataInnovacionConnectionError("Client is closed")
        try:
            response = self._http.get(self._projects_url, params=dict(params))
        except httpx.TimeoutException as exc:
            raise DataInnovacionTimeoutError("Data Innovacion request timed out") from exc
        except httpx.RequestError as exc:
            raise DataInnovacionConnectionError(
                "Data Innovacion request could not be completed"
            ) from exc
        if not response.is_success:
            raise DataInnovacionHTTPError(
                f"Data Innovacion returned HTTP {response.status_code}",
                status_code=response.status_code,
            )
        try:
            payload: JsonValue = response.json()
        except ValueError as exc:
            raise DataInnovacionProtocolError("API returned invalid JSON") from exc
        if isinstance(payload, list):
            raw_value: JsonValue = payload
        elif isinstance(payload, dict):
            raw_value = payload.get("value")
        else:
            raise DataInnovacionProtocolError("API response must be a JSON object or array")
        if not isinstance(raw_value, list):
            raise DataInnovacionProtocolError("API response has no valid 'value' list")
        value = raw_value
        projects: builtins.list[Project] = []
        for item in value:
            if not isinstance(item, dict):
                raise DataInnovacionProtocolError("A project item must be a JSON object")
            project_payload: dict[str, Any] = dict(item)
            projects.append(Project.from_api(project_payload))
        return projects


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
