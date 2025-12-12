"""Development (cloud dev) Django settings.

Used for the AWS dev environment. Closer to production than `local`,
but with debug and relaxed security defaults.
"""

from .base import *  # noqa

# Debug defaults to True in development, can be overridden via DJANGO_DEBUG.
DEBUG = env.bool("DJANGO_DEBUG", default=True)  # type: ignore # noqa: F405

# Allow overriding hosts from env, otherwise permit all in dev.
ALLOWED_HOSTS = get_allowed_hosts(default=["*"])  # type: ignore # noqa: F405
CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS", default=[])  # type: ignore # noqa: F405

# Keep HTTPS optional in dev.
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=False)  # type: ignore # noqa: F405
SECURE_HSTS_SECONDS = env.int("DJANGO_SECURE_HSTS_SECONDS", default=0)  # type: ignore # noqa: F405
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# Serve static assets via WhiteNoise when `collectstatic` is run.
INSTALLED_APPS += ["whitenoise.runserver_nostatic"]  # type: ignore # noqa: F405
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")  # type: ignore # noqa: F405
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

