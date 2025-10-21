"""
Configuración WSGI para el proyecto `tienda_proyectoweb`.

Este módulo expone la variable `application` para servidores WSGI.

Para más información sobre este archivo consulta:
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda_proyectoweb.settings')

application = get_wsgi_application()
