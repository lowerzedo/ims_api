# ADR-000: Initial Stack and Project Conventions

## Status
Accepted — 2024-05-05

## Context

The IMS backend must support a complex insurance workflow with rich domain modelling, API-first delivery, and operational readiness for Render deployment. We need to choose the foundational stack, dependency management, and project conventions before implementing domain features.

## Decision

- **Framework**: Django 5 with Django REST Framework for rapid CRUD scaffolding, admin interface, and robust ORM support for Postgres.
- **Authentication**: JSON Web Tokens via `djangorestframework-simplejwt`; Django admin retained for back-office workflows.
- **Database**: Postgres (via `psycopg` v3 driver) with UUID primary keys, soft deletion, and timestamp tracking provided through shared abstract models.
- **Configuration**: Environment-driven settings split into `base`, `local`, `test`, and `production` modules, orchestrated through `django-environ`.
- **Tooling**: uv for dependency management; formatting and linting with Black, Ruff, isort; typing with mypy and django-stubs; pytest + pytest-django for tests.
- **Containerisation**: Python 3.11 slim image with Gunicorn for production, orchestrated locally with Docker Compose (web, Postgres, Redis).
- **Project Layout**: `apps/` package grouping domain apps (`common`, `accounts`, ...), `config/` package for project settings, plus documentation and infrastructure assets.

## Consequences

- Developers install dependencies via uv (`uv sync --group dev`) and run quality gates through pre-commit hooks using the provided configuration.
- Environment overrides and secrets are centralised in `.env`, easing Render deployment and Docker usage.
- Future domain apps will extend the shared `BaseModel` to guarantee UUID keys and audit-friendly fields.
- CI/CD pipelines should invoke `uv sync --group dev` (or `uv sync --frozen` in CI), linting (`uv run --group dev ruff`, `black`, `mypy`), and tests (`uv run --group dev pytest`).
- Additional ADRs should capture future architectural choices (e.g., task queue adoption, reporting implementations, external integrations).

## Alternatives Considered

- `pip-tools` for dependency management — adopted plan prefers uv for lockfile generation and optional dev dependencies.
- Monolithic settings file — rejected in favour of split settings to simplify environment parity and deployments.
- Delaying containerisation — rejected to ensure early deployment readiness and local parity.
