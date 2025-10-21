"""
Configuración ASGI para el proyecto `tienda_proyectoweb`.

Este módulo expone la variable `application` para servidores ASGI.

Para más información sobre este archivo consulta:
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda_proyectoweb.settings')

application = get_asgi_application()
