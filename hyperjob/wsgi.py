"""
WSGI config for hyperjob project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# If DJANGO_ALLOWED_HOSTS is defined as an environment variable,
# then we should use the production settings in production.py.
settings_module = "hyperjob.production" if 'DJANGO_ALLOWED_HOSTS' in os.environ else 'hyperjob.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
