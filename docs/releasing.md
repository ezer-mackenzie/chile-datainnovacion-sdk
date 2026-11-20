# Releasing

The package version is declared in `pyproject.toml` and mirrored by
`constants.SDK_VERSION`, which is also used in the HTTP user-agent.
Update both values together when preparing a release, and describe user-facing
changes in the release notes or GitHub release.

Before tagging:

```console
uv sync --group dev
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run basedpyright
uv run mypy src
uv run codespell README.md docs src tests examples CONTRIBUTING.md
uv build
```

Create a version tag matching the package version, for example `v0.1.0`, after
the release commit is ready. Push the commit and tag separately when publishing
to a remote:

```console
git push origin main
git push origin v0.1.0
```

Do not tag a build that has not passed the checks above.
