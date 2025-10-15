"""Settings used during automated tests."""
from .base import *  # noqa

DJANGO_ENV = "test"
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
DATABASES["default"] = {  # type: ignore # noqa: F405
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": ":memory:",
}
REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = [  # type: ignore # noqa: F405
    "rest_framework.authentication.SessionAuthentication",
]
