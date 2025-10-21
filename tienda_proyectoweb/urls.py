"""
Configuración de rutas (URLs) del proyecto `tienda_proyectoweb`.

La lista `urlpatterns` mapea las URLs a vistas. Para más información:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/

Ejemplos:
- Vistas de función:
    1. Importar la vista: from my_app import views
    2. Añadir una entrada: path('', views.home, name='home')
- Vistas basadas en clases:
    1. Importar la clase: from other_app.views import Home
    2. Añadir una entrada: path('', Home.as_view(), name='home')
- Incluir otro URLconf (otra app):
    1. Importar include: from django.urls import include, path
    2. Añadir: path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from pathlib import Path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
]

if settings.DEBUG:
    # Servir archivos de media durante el desarrollo (solo en DEBUG)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # También servir la carpeta `cars/` situada en la raíz del proyecto
    # (algunas imágenes están guardadas allí fuera de MEDIA_ROOT).
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    urlpatterns += static('/cars/', document_root=str(PROJECT_ROOT / 'cars'))
