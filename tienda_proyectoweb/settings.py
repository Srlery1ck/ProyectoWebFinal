"""
Configuración (settings) de Django para el proyecto `tienda_proyectoweb`.

Este archivo fue generado por `django-admin startproject` (Django 5.2.7)
y contiene las principales opciones de configuración que el proyecto
usa en tiempo de ejecución.

Puntos importantes (resumen):
- `BASE_DIR`: directorio raíz del proyecto.
- `SECRET_KEY`: clave secreta usada para firmar cookies y otros valores.
- `DEBUG`: modo de desarrollo; NO dejar True en producción.
- `INSTALLED_APPS`: las aplicaciones activas (aquí está `shop`).
- `MEDIA_URL` / `MEDIA_ROOT`: dónde se sirven y almacenan los archivos subidos (imagenes).

Consulta la documentación oficial de Django para más detalles:
https://docs.djangoproject.com/en/5.2/topics/settings/
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Ajustes rápidos para desarrollo - no aptos para producción.
# Revisa la guía de despliegue de Django antes de publicar en un servidor.
# https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# ADVERTENCIA DE SEGURIDAD: mantén la clave secreta fuera de repositorios públicos
# y usa variables de entorno en producción.
SECRET_KEY = 'django-insecure--+9b%6ynkxx@3^xyz0p6_+5%7s@3j06i-ieoh$3*mp!6a+uc5m'

# ADVERTENCIA: DEBUG = True habilita información detallada de errores y
# servido de ficheros estáticos/medios en desarrollo. Deshabilitar en producción.
DEBUG = True

ALLOWED_HOSTS = []

LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
LOGIN_URL = "login"




# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop.apps.ShopConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tienda_proyectoweb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tienda_proyectoweb.wsgi.application'
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
