# Chile Data Innovacion SDK

Unofficial, typed Python SDK for querying the public projects API from [Data Innovación](https://datainnovacion.cl/api).

[![Python versions](https://img.shields.io/pypi/pyversions/chile-datainnovacion-sdk)](https://pypi.org/project/chile-datainnovacion-sdk/)
[![Version](https://img.shields.io/pypi/v/chile-datainnovacion-sdk)](https://pypi.org/project/chile-datainnovacion-sdk/)

## Installation

```bash
pip install chile-datainnovacion-sdk
```

## Quick Start

```python
from chile_datainnovacion_sdk import ChileDataInnovacionClient

with ChileDataInnovacionClient() as client:
    projects = client.projects.list(limit=20)

    for project in projects:
        print(project.code, project.project_title)
```

The SDK includes the public token by default, so it is not necessary to configure it for public requests.
It can also be replaced explicitly:

```python
with ChileDataInnovacionClient(token="YOUR_TOKEN") as client:
    projects = client.projects.list(
        intervention_type="Subsidio",
        data_status="Finalizado",
        award_year="2010,2012",
        limit=50,
    )
```

To find a project by code:

```python
with ChileDataInnovacionClient() as client:
    project = client.get_project("09AAP-6740")
```

## Available Filters

| Python name | API parameter | Values |
|---|---|---|
| `code` | `filter[codigo]` | Exact project code |
| `beneficiary_rut` | `filter[rut_beneficiario]` | Beneficiary RUT |
| `intervention_type` | `filter[tipo_intervencion]` | `Ley` or `Subsidio` |
| `data_status` | `filter[estado_data]` | `Vigente` or `Finalizado` |
| `sustainable` | `filter[sostenible]` | `Sí` or `No` |
| `award_year` | `filter[año_adjudicacion]` | Year or comma-separated year range |
| `limit` | `limit` | Maximum number of records |

Every documented API field is mapped to an English name on `Project`. Additional fields returned by the API are preserved through `extra="allow"`; use `DataInnovacionProjectDTO` only when you need to inspect the original Spanish wire format.

## Documentation

The [full documentation on Read the Docs](https://chile-datainnovacion-sdk.readthedocs.io/en/latest/) includes configuration, the field mapping, error handling, development, and release guides.

## Development

```console
uv sync --group dev
uv run pytest
uv run ruff check .
uv run basedpyright
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for all local checks and optional benchmarks.
Release changes are recorded in [CHANGELOG.md](CHANGELOG.md).