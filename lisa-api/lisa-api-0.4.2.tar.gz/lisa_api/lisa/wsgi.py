"""
WSGI config for lisa_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lisa_api.lisa.settings")

application = get_wsgi_application()

from lisa_api.lisa.plugin_manager import PluginManager
from django.core.management import call_command

call_command("migrate")
PM = PluginManager()
PM.load_intents()
