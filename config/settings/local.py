"""Settings overrides for local development."""
from .base import *  # noqa

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "0.0.0.0"]
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:8000", "http://localhost:8000", "http://0.0.0.0:8000", "http://ims-api-k3j2.onrender.com"]
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS += ["django_extensions"]  # type: ignore # noqa: F405

REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = [  # type: ignore # noqa: F405
    "rest_framework.permissions.IsAuthenticatedOrReadOnly",
]
