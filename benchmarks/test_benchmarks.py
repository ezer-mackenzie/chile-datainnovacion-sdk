import pytest

from chile_datainnovacion_sdk.models import Project


@pytest.mark.benchmark
def test_map_project_response(benchmark: pytest.BenchmarkFixture) -> None:
    payload = {
        "codigo": "19CV-12345",
        "titulo_del_proyecto": "A sample innovation project",
        "año_adjudicacion": 2019,
        "rut_beneficiario": "12345678K",
    }

    result = benchmark(Project.from_api, payload)

    assert result.code == "19CV-12345"
