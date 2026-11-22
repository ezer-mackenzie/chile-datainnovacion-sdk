import os

import pytest

from chile_datainnovacion_sdk import ChileDataInnovacionClient

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        os.environ.get("CHILE_DATAINNOVACION_LIVE_TESTS") != "1",
        reason="Set CHILE_DATAINNOVACION_LIVE_TESTS=1 to run read-only API checks",
    ),
]


@pytest.mark.parametrize(
    ("filter_name", "filter_value", "field_name", "expected_value"),
    [
        ("code", "09AAP-6740", "code", "09AAP-6740"),
        ("beneficiary_rut", "77295440-9", "beneficiary_rut", "77295440-9"),
        ("intervention_type", "Subsidio", "intervention_type", "Subsidio"),
        ("data_status", "Finalizado", "data_status", "Finalizado"),
        ("sustainable", "Sí", "sustainable", "Sí"),
        ("award_year", 2010, "award_year", 2010),
    ],
)
def test_documented_filters_match_live_api_records(
    filter_name: str,
    filter_value: str | int,
    field_name: str,
    expected_value: str | int,
) -> None:
    with ChileDataInnovacionClient() as client:
        projects = client.projects.list(limit=1, **{filter_name: filter_value})

    assert projects
    actual_value = getattr(projects[0], field_name)
    if isinstance(expected_value, str):
        assert actual_value.casefold() == expected_value.casefold()
    else:
        assert actual_value == expected_value


def test_api_returns_a_limited_top_level_project_array() -> None:
    with ChileDataInnovacionClient() as client:
        projects = client.projects.list(limit=2)

    assert 0 < len(projects) <= 2
    assert all(project.code for project in projects)
