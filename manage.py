#!/usr/bin/env python3
"""Management utility for administrative tasks."""
from __future__ import annotations

import os
import sys


def main() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:  # pragma: no cover - import guard
        raise ImportError("Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable?") from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
