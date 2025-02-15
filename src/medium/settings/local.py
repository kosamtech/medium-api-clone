from .base import *  # noqa

# # SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "DAJNGO_SECRET_KEY",
    default="django-insecure-&d58bbs!&m^d5u7wb-@q+%-l3flmy1teogvgmxsx1lmgcr#t!w",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", "http://127.0.0.0:8000"]

EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="mailhog")
EMAIL_PORT = env("EMAIL_PORT", default="1025")
DEFAULT_FROM_EMAIL = "support@kosamtech.dev"
DOMAIN = env("DOMAIN", default="localhost:8000")
SITE_NAME = "Medium Clone"
