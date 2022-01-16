"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from config.settings_manager import get_settings_file

# place static (recommended for production mode) -> 'config.settings.production' for faster execution
os.environ.setdefault('DJANGO_SETTINGS_MODULE', get_settings_file())

application = get_wsgi_application()
