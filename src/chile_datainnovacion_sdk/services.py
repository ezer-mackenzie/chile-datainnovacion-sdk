from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import httpx
from pydantic import JsonValue

from chile_datainnovacion_sdk.constants import API_FILTER_NAMES
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


class ProjectsService:
    def __init__(self, http: httpx.Client, projects_url: str) -> None:
        self._http = http
        self._projects_url = projects_url

    def _request(self, params: Mapping[str, str | int]) -> list[Project]:
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
        projects: list[Project] = []
        for item in value:
            if not isinstance(item, dict):
                raise DataInnovacionProtocolError("A project item must be a JSON object")
            project_payload: dict[str, Any] = dict(item)
            projects.append(Project.from_api(project_payload))
        return projects

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
    ) -> list[Project]:
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
    ) -> list[Project]:
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
