# Repository guidance

- Keep the public model and documented SDK API in English; Spanish keys belong
  only in the API wire DTO and API query parameters.
- Keep runtime dependencies limited to `httpx` and `pydantic`.
- Test API behavior with deterministic `httpx.MockTransport` responses.
- Keep live API checks opt-in and read-only.
- Run pytest, Ruff, BasedPyright, mypy, and codespell before a release.
- Keep `pyproject.toml` and `src/chile_datainnovacion_sdk/constants.py` version
  values synchronized; release tags use the `vMAJOR.MINOR.PATCH` form.