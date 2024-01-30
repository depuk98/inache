"""
WSGI config for InacheBackend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from InacheBackend import settings
settings_file = os.environ.get('SETTINGS_FILE')
print(settings_file,"wsgi configuration")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_file)
application = get_wsgi_application()
