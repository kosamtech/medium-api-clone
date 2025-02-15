"""
WSGI config for medium project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

environment = os.environ.get("DJANGO_ENVIRONMENT", default="local")

if environment == "local":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "medium.settings.local")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "medium.settings.prod")

application = get_wsgi_application()
