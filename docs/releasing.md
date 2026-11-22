# Releasing

The package version is declared in `pyproject.toml` and mirrored by
`constants.SDK_VERSION`, which is also used in the HTTP user-agent.
Update both values together when preparing a release, and describe user-facing
changes in the release notes or GitHub release.

Before tagging:

```console
uv sync --locked --group dev --group docs
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run basedpyright
uv run mypy src
uv run codespell README.md docs src tests examples CONTRIBUTING.md
uv run mkdocs build --strict
uv build
```

The CI workflow runs these checks on Python 3.11, 3.12, 3.13, and 3.14. Confirm
that all matrix jobs pass before tagging. The release tag must match the package
version (for example, `v1.0.0` for version `1.0.0`).

Create the tag only after the release commit is ready. Pushing a tag does not
itself publish to PyPI; publishing requires creating a non-prerelease GitHub
Release for that tag. The publish workflow verifies the tag/version match and
uses PyPI trusted publishing. Do not dispatch a manual publish workflow.

To push a reviewed release when explicitly ready:

```console
git push origin main
git push origin v1.0.0
```

Do not tag a build that has not passed the checks above.
