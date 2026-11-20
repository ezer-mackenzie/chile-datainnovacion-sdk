# Usage

## Create a client

The client owns its HTTP connection pool. Use it as a context manager or close
it explicitly:

```python
from chile_datainnovacion_sdk import ChileDataInnovacionClient, ClientConfig

with ChileDataInnovacionClient() as client:
    projects = client.projects.list(limit=20)

config = ClientConfig(
    base_url="https://datainnovacion.cl/api",
    api_token="YOUR_TOKEN",
    timeout=30,
    connect_timeout=10,
)
client = ChileDataInnovacionClient(config=config)
try:
    projects = client.list_projects(sustainable="Sí")
finally:
    client.close()
```

`ClientConfig` also supports TLS verification and a custom user-agent. TLS
verification is enabled by default.

## Find and filter projects

```python
with ChileDataInnovacionClient() as client:
    project = client.get_project("09AAP-6740")
    finished_subsidies = client.projects.list(
        intervention_type="Subsidio",
        data_status="Finalizado",
        award_year="2010,2012",
        limit=50,
    )
```

`get_project` returns `None` when the API returns no matching project. The
`projects.search(...)`, `client.list_projects(...)`, and
`client.get_projects(...)` methods accept the same filters as `projects.list`.

The SDK includes the documented API filters as typed keyword arguments. Other
API filters can be passed by their wire name, for example:

```python
with ChileDataInnovacionClient() as client:
    projects = client.projects.list(sector_economico="Forestal", limit=20)
```

## Response models

Responses are converted into the English `Project` model:

```python
project.code
project.project_title
project.award_year
project.beneficiary_rut
project.model_dump()
```

The `DataInnovacionProjectDTO` mirrors the Spanish API payload and is useful for
inspecting its raw keys. `Project.from_api(payload)` maps the DTO fields to
English names. Unrecognized API fields are retained on `Project` as extra
attributes.

## Errors

All runtime errors inherit from `ChileDataInnovacionError`.

| Error | Meaning |
|---|---|
| `DataInnovacionTimeoutError` | A request timed out |
| `DataInnovacionConnectionError` | The request could not be completed, or the client is closed |
| `DataInnovacionHTTPError` | The API returned a non-success status; inspect `status_code` |
| `DataInnovacionProtocolError` | The response was not a supported JSON response |

Invalid caller input such as a non-positive `limit` raises `ValueError` before
making a request.
