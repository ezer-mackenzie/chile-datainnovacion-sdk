import httpx
import pytest

import chile_datainnovacion_sdk as sdk
from chile_datainnovacion_sdk import (
    ChileDataInnovacionClient,
    ChileDataInnovacionError,
    ClientConfig,
    __version__,
)
from chile_datainnovacion_sdk.errors import (
    DataInnovacionConnectionError,
    DataInnovacionHTTPError,
    DataInnovacionProtocolError,
    DataInnovacionTimeoutError,
)
from chile_datainnovacion_sdk.models import (
    API_TO_ENGLISH,
    DataInnovacionProjectDTO,
    Project,
)
from chile_datainnovacion_sdk.services import ProjectsService


def test_list_projects_builds_filters_and_parses_response() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["accept"] == "application/json"
        assert request.headers["authorization"]
        assert request.url.params["filter[codigo]"] == "09AAP-6740"
        assert request.url.params["filter[tipo_intervencion]"] == "Subsidio"
        assert request.url.params["limit"] == "2"
        return httpx.Response(
            200,
            json={
                "value": [
                    {
                        "codigo": "09AAP-6740",
                        "titulo_del_proyecto": "Proyecto de prueba",
                        "año_adjudicacion": 2009,
                        "campo_nuevo": "conservado",
                    }
                ],
                "Count": 1,
            },
        )

    transport = httpx.MockTransport(handler)
    with ChileDataInnovacionClient(transport=transport) as client:
        projects = client.projects.list(
            code="09AAP-6740",
            intervention_type="Subsidio",
            limit=2,
        )

    assert len(projects) == 1
    assert projects[0].code == "09AAP-6740"
    assert projects[0].project_title == "Proyecto de prueba"
    assert projects[0].award_year == 2009
    assert projects[0].campo_nuevo == "conservado"


def test_version_and_error_hierarchy() -> None:
    assert __version__ == "1.0.0"
    assert issubclass(DataInnovacionHTTPError, ChileDataInnovacionError)


def test_stable_public_api_exports_only_canonical_clients() -> None:
    assert sdk.ProjectsService is ProjectsService
    assert "ChileDataInnovacionClient" in sdk.__all__
    assert "DataInnovacionClient" not in sdk.__all__
    assert "DataInnovacionSDKClient" not in sdk.__all__
    assert all(hasattr(sdk, name) for name in sdk.__all__)


def test_get_project_returns_none_when_not_found() -> None:
    transport = httpx.MockTransport(
        lambda request: httpx.Response(200, json={"value": [], "Count": 0})
    )
    with ChileDataInnovacionClient(transport=transport) as client:
        assert client.get_project("NO-EXISTE") is None


def test_protocol_error_for_invalid_envelope() -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json={"unexpected": []}))
    with ChileDataInnovacionClient(transport=transport) as client:
        try:
            client.projects.list()
        except DataInnovacionProtocolError:
            pass
        else:
            raise AssertionError("Expected DataInnovacionProtocolError")


def test_api_payload_is_mapped_to_english_project_model() -> None:
    project = Project.from_api(
        {
            "codigo": "19CV-12345",
            "titulo_del_proyecto": "Example project",
            "año_adjudicacion": 2019,
            "rut_beneficiario": "12345678K",
            "campo_nuevo": "preserved",
        }
    )

    assert project.code == "19CV-12345"
    assert project.project_title == "Example project"
    assert project.award_year == 2019
    assert project.beneficiary_rut == "12345678K"
    assert project.campo_nuevo == "preserved"


def test_wire_dto_keeps_spanish_api_names() -> None:
    dto = DataInnovacionProjectDTO.model_validate(
        {"codigo": "19CV-12345", "titulo_del_proyecto": "Proyecto"}
    )

    assert dto.codigo == "19CV-12345"
    assert dto.titulo_del_proyecto == "Proyecto"


def test_wire_fields_and_english_model_fields_are_fully_mapped() -> None:
    wire_fields = {
        field.alias or name for name, field in DataInnovacionProjectDTO.model_fields.items()
    }

    assert wire_fields.issubset(API_TO_ENGLISH)
    assert set(API_TO_ENGLISH.values()) == set(Project.model_fields)


@pytest.mark.parametrize("bad_limit", [0, -1, True, 1.5])
def test_invalid_limit_fails_before_network_request(bad_limit: int) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError("Invalid limits must not make an HTTP request")

    with ChileDataInnovacionClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(ValueError, match="positive integer"):
            client.projects.list(limit=bad_limit)


def test_additional_filter_accepts_english_and_wire_names() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["filter[año_adjudicacion]"] == "2010,2012"
        assert request.url.params["filter[sector_economico]"] == "Forestal"
        return httpx.Response(200, json={"value": []})

    with ChileDataInnovacionClient(transport=httpx.MockTransport(handler)) as client:
        client.projects.list(award_year="2010,2012", sector_economico="Forestal")


@pytest.mark.parametrize("status_code", [301, 400, 401, 403, 429, 500])
def test_unsuccessful_http_status_raises_typed_error(status_code: int) -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(status_code, text="API error"))
    with ChileDataInnovacionClient(transport=transport) as client:
        with pytest.raises(DataInnovacionHTTPError) as error:
            client.projects.list()
    assert error.value.status_code == status_code
    assert isinstance(error.value, ChileDataInnovacionError)


@pytest.mark.parametrize(
    "response",
    [
        httpx.Response(200, text="not JSON"),
        httpx.Response(200, json={"Count": 1}),
        httpx.Response(200, json={"value": "not a list"}),
        httpx.Response(200, json={"value": [None]}),
        httpx.Response(200, json="unexpected"),
    ],
)
def test_malformed_api_responses_raise_protocol_error(response: httpx.Response) -> None:
    with ChileDataInnovacionClient(
        transport=httpx.MockTransport(lambda request: response)
    ) as client:
        with pytest.raises(DataInnovacionProtocolError):
            client.projects.list()


@pytest.mark.parametrize(
    ("exception_type", "expected_error"),
    [
        (httpx.ReadTimeout, DataInnovacionTimeoutError),
        (httpx.ConnectError, DataInnovacionConnectionError),
    ],
)
def test_transport_errors_are_converted(
    exception_type: type[httpx.RequestError],
    expected_error: type[Exception],
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise exception_type("transport failed", request=request)

    with ChileDataInnovacionClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(expected_error):
            client.projects.list()


def test_client_config_and_token_header() -> None:
    config = ClientConfig(
        base_url="https://example.test/api/",
        api_token="custom-token",
        timeout=15,
        connect_timeout=3,
        verify=False,
    )

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url == "https://example.test/api/v1/proyectos"
        assert request.headers["authorization"] == "custom-token"
        assert request.extensions["timeout"] == {
            "connect": 3,
            "read": 15,
            "write": 15,
            "pool": 15,
        }
        return httpx.Response(200, json={"value": []})

    with ChileDataInnovacionClient(config=config, transport=httpx.MockTransport(handler)) as client:
        client.projects.list()


@pytest.mark.parametrize(
    ("timeout", "connect_timeout"),
    [
        (0, 1),
        (-1, 1),
        (1, 0),
        (1, -1),
        (float("inf"), 1),
        (1, float("nan")),
        (True, 1),
    ],
)
def test_config_rejects_non_positive_timeouts(timeout: float, connect_timeout: float) -> None:
    with pytest.raises(ValueError, match="finite values greater than zero"):
        ClientConfig(timeout=timeout, connect_timeout=connect_timeout)


def test_closed_client_cannot_be_used() -> None:
    client = ChileDataInnovacionClient(
        transport=httpx.MockTransport(lambda request: httpx.Response(200, json={"value": []}))
    )
    client.close()
    with pytest.raises(DataInnovacionConnectionError, match="closed"):
        client.projects.list()


def test_closed_client_cannot_be_entered() -> None:
    client = ChileDataInnovacionClient(
        transport=httpx.MockTransport(lambda request: httpx.Response(200, json={"value": []}))
    )
    client.close()
    with pytest.raises(DataInnovacionConnectionError, match="closed"):
        client.__enter__()


def test_constructor_rejects_config_and_individual_options_together() -> None:
    with pytest.raises(ValueError, match="Pass config or token/base_url"):
        ChileDataInnovacionClient(config=ClientConfig(), token="another-token")


def test_get_project_returns_matching_english_project() -> None:
    transport = httpx.MockTransport(
        lambda request: httpx.Response(
            200,
            json={"value": [{"codigo": "19CV-12345", "titulo_del_proyecto": "Example"}]},
        )
    )
    with ChileDataInnovacionClient(transport=transport) as client:
        project = client.get_project("19CV-12345")

    assert project is not None
    assert project.code == "19CV-12345"


def test_api_accepts_a_top_level_project_array() -> None:
    transport = httpx.MockTransport(
        lambda request: httpx.Response(200, json=[{"codigo": "19CV-12345"}])
    )
    with ChileDataInnovacionClient(transport=transport) as client:
        projects = client.projects.list()

    assert [project.code for project in projects] == ["19CV-12345"]


def test_search_and_client_list_aliases_share_filter_contract() -> None:
    seen_requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen_requests.append(request)
        return httpx.Response(200, json={"value": [{"codigo": "19CV-12345"}]})

    with ChileDataInnovacionClient(transport=httpx.MockTransport(handler)) as client:
        assert client.projects.search(code="19CV-12345")[0].code == "19CV-12345"
        assert client.list_projects(code="19CV-12345")[0].code == "19CV-12345"

    assert len(seen_requests) == 2
    assert all(request.url.params["filter[codigo]"] == "19CV-12345" for request in seen_requests)
