"""Explicit BenchCore performance checks; excluded from normal test discovery."""

import pytest
from benchcore.core.models import BenchmarkConfig
from benchcore.integrations.pytest import BenchCoreFixture

from chile_datainnovacion_sdk.models import Project


@pytest.mark.benchcore(
    name="map-project-api-record",
    config=BenchmarkConfig(rounds=20, warmup_rounds=2, iterations=10),
)
def test_map_project_api_record(benchcore: BenchCoreFixture) -> None:
    payload = {
        "codigo": "19CV-12345",
        "titulo_del_proyecto": "A sample innovation project",
        "año_adjudicacion": 2019,
        "rut_beneficiario": "12345678K",
    }

    result = benchcore(Project.from_api, payload)

    assert result.value.code == "19CV-12345"
    assert result.value.award_year == 2019
