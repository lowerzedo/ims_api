.PHONY: help install migrate superuser run lint format test coverage up down

UV_CMD = uv run --group dev

help:
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?##"}; {printf "%-20s %s\n", $$1, $$2}'

install: ## Install dependencies via uv (including dev extras)
	uv sync --group dev

migrate: ## Apply database migrations
	$(UV_CMD) python manage.py migrate

superuser: ## Create a Django superuser
	$(UV_CMD) python manage.py createsuperuser

run: ## Start the Django development server
	$(UV_CMD) python manage.py runserver 0.0.0.0:8000

lint: ## Run static analysis (Ruff + mypy)
	$(UV_CMD) ruff check
	$(UV_CMD) mypy

format: ## Format code with Black and isort
	$(UV_CMD) black .
	$(UV_CMD) isort .

test: ## Run pytest suite
	$(UV_CMD) pytest

coverage: ## Generate coverage report
	$(UV_CMD) pytest --cov=apps --cov=config --cov-report=xml

up: ## Start docker-compose stack
	docker-compose up --build

down: ## Stop docker-compose stack
	docker-compose down
