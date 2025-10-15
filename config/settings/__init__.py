"""Django settings module that selects environment-specific defaults."""
from .base import *  # noqa
from .base import env  # type: ignore  # noqa

ENVIRONMENT = env.str("DJANGO_ENV", default="local")

if ENVIRONMENT == "local":
    from .local import *  # noqa
elif ENVIRONMENT == "test":
    from .test import *  # noqa
elif ENVIRONMENT == "production":
    from .production import *  # noqa
