# Chile Data Innovacion SDK

An unofficial, typed Python client for the public Data Innovación projects API.
It provides a synchronous HTTP client, English project models, and explicit
errors for network, HTTP, and response-format failures.

## Quick example

```python
from chile_datainnovacion_sdk import ChileDataInnovacionClient

with ChileDataInnovacionClient() as client:
    for project in client.projects.list(limit=10):
        print(project.code, project.project_title)
```

The SDK uses Data Innovación's documented public token by default. Pass your own
token with `ChileDataInnovacionClient(token="...")` when required.

## Project links

- [Usage and configuration](usage.md)
- [API field mappings](api-fields.md)
- [Development and tests](development.md)
- [Release process](releasing.md)
