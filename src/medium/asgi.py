"""
ASGI config for medium project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

environment = os.environ.get("DJANGO_ENVIRONMENT", default="local")

if environment == "local":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medium.settings.local')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medium.settings.prod')

application = get_asgi_application()
