# Insurance Management System API

Backend service for the Insurance Management System (IMS) built with Django, Django REST Framework, and Postgres. The service is structured into modular domain apps and instrumented for high-quality delivery.

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (dependency management)
- Docker & Docker Compose (optional for local parity)

## Quickstart

1. **Install uv (once)**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
   Ensure `~/.local/bin` is on your `PATH` (or follow the installer output).

2. **Environment variables**
   ```bash
   cp .env.example .env
   ```
   Adjust values (secret key, database URL, admin path, etc.).

3. **Install dependencies**
   ```bash
   uv sync --group dev
   ```

4. **Run database migrations**
   ```bash
   uv run --group dev python manage.py migrate
   ```

5. **Start the development server**
   ```bash
   uv run --group dev python manage.py runserver 0.0.0.0:8000
   ```

6. **(Optional) Docker stack**
   ```bash
   docker-compose up --build
   ```
   The Compose service will run `uv sync --group dev` automatically before launching the server.

## Tooling

- **Dependency management**: uv (`uv sync`, `uv run`)
- **Formatting / Linting**: Black, Ruff, isort
- **Typing**: mypy with django-stubs
- **Testing**: pytest + pytest-django (see `Makefile` targets)
- **Docs**: OpenAPI schema (`/api/schema/`) with Swagger & ReDoc UIs
- **Health check**: `/api/health/`

## Project Layout

```
apps/            # Domain Django apps (accounts, common, ...)
config/          # Django project configuration & settings split by env
manage.py        # Django management utility
Dockerfile       # Container image definition (Python 3.11 + uv + Gunicorn)
docker-compose.yml
README.md
```

## Next Steps

- Flesh out domain models following `../db.md`
- Implement authentication endpoints (JWT) and role-based permissions matrix
- Build core API flows: client onboarding, policy lifecycle, endorsements, COIs
- Add CI pipeline that enforces lint, type-check, tests before deployment (`uv run --group dev ...`)
- Integrate document storage, background processing, and reporting modules

## References

- [`Requirements V4.pdf`](../Requirements%20V4.pdf) — product requirements
- [`Requirements V4.txt`](../Requirements%20V4.txt) — searchable requirements
- [`db.md`](../db.md) — canonical ERD / schema blueprint
- [`backend_development_plan.md`](../backend_development_plan.md) — milestone roadmap
- [`docs/api_endpoints.md`](docs/api_endpoints.md) — endpoint reference for frontend integration
