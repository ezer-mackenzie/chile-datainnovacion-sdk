# Development

## Setup

Python 3.11 or newer is required for the SDK and normal test suite.

```console
uv sync --group dev
```

## Checks

```console
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run basedpyright
uv run mypy src
uv run codespell README.md docs src tests examples
```

The tests use `httpx.MockTransport` and Hypothesis; they do not depend on the
live service. Live smoke tests should be run manually, since the public service
can change or be temporarily unavailable.

## Benchmarks

Benchmarks are optional and excluded from ordinary test discovery:

```console
uv run --group dev --group benchmark pytest benchmarks --no-cov --benchmark-only
```

BenchCore measurements require Python 3.12 or newer (the SDK still supports
Python 3.11):

```console
uv run --python 3.12 --group dev --group benchcore pytest benchmarks/benchcore_cases.py --no-cov --benchcore-save=.benchcore
```

The BenchCore measurements require Python 3.12 or newer (the SDK still supports
Python 3.11):

```console
uv run --python 3.12 --group benchcore pytest benchmarks/benchcore_cases.py --no-cov --benchcore-save=.benchcore
```

Benchmarks are local observations, not CI performance gates. Do not compare
results across different Python versions or dissimilar machines.
