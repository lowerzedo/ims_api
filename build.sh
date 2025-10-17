#!/usr/bin/env bash
set -o errexit  # Exit on error

# Install uv if not present
pip install --upgrade pip uv

# Install dependencies
uv sync --no-dev

# Run database migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

