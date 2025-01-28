import os

from celery import Celery
from django.conf import settings

environment = os.environ.get("DJANGO_ENVIRONMENT", default="local")

# set the default Django settings module for the 'celery' program.
if environment == "local":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medium.settings.local')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medium.settings.prod')

app = Celery("medium")

# Using a string here means the worker doesn't 
# have to serialize the configuration object to 
# child processes. - namespace='CELERY' means all 
# celery-related configuration keys should 
# have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)