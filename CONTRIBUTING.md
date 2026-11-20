# Contributing

## Development setup

Use Python 3.11 or newer and install the development tools with uv:

```console
uv sync --group dev
```

## Before opening a pull request

Run the offline checks:

```console
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run basedpyright
uv run mypy src
uv run codespell README.md docs src tests examples
```

Tests must use deterministic transports or local fixtures. Do not make live API
calls in the default test suite. Add an `integration`-marked test only for
read-only behavior that cannot be tested with a mock transport.

## Optional benchmarks

```console
uv run --group dev --group benchmark pytest benchmarks --no-cov --benchmark-only
uv run --python 3.12 --group dev --group benchcore pytest benchmarks/benchcore_cases.py --no-cov --benchcore-save=.benchcore
```

Benchmark results are diagnostic only and must not be used as timing gates.
BenchCore requires Python 3.12 or newer; that optional tool does not change the
SDK's minimum supported Python version.

See [the development guide](docs/development.md) for tool configuration and
[the release guide](docs/releasing.md) for version and tag requirements.