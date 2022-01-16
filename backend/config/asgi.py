"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from config.settings_manager import get_settings_file

# place static (recommended for production mode) -> 'config.settings.production' for faster execution
os.environ.setdefault('DJANGO_SETTINGS_MODULE', get_settings_file())

application = get_asgi_application()
