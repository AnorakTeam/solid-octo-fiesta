import os
from pathlib import Path
from datetime import timedelta
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY',
                       'dev-only-secret-key-change-me-32-bytes')
DEBUG = os.getenv('DJANGO_DEBUG', '1') == '1'
# Vercel establece HTTP_HOST con el dominio público. No depender solamente de
# DJANGO_ALLOWED_HOSTS: una variable antigua (por ejemplo "localhost") no debe
# impedir que la función serverless atienda su propio dominio de Vercel.
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.vercel.app', '.railway.app']
ALLOWED_HOSTS += [
    host.strip()
    for host in os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')
    if host.strip()
]
if vercel_url := os.getenv('VERCEL_URL'):
    ALLOWED_HOSTS.append(vercel_url)
INSTALLED_APPS = ['django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.messages', 'django.contrib.staticfiles', 'corsheaders', 'rest_framework', 'apps.accounts', 'apps.game']
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware', 'django.middleware.security.SecurityMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware',
              'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware', 'django.contrib.messages.middleware.MessageMiddleware']
ROOT_URLCONF = 'config.urls'
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [], 'APP_DIRS': True, 'OPTIONS': {'context_processors': [
    'django.template.context_processors.request', 'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION = 'config.wsgi.application'
DB_ENGINE = os.getenv('DB_ENGINE', 'postgres').lower()
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {'default': dj_database_url.parse(
        DATABASE_URL, conn_max_age=600, ssl_require=True)}
elif DB_ENGINE == 'postgres':
    DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql', 'NAME': os.getenv('POSTGRES_DB', 'clicker'), 'USER': os.getenv(
        'POSTGRES_USER', 'clicker'), 'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'clicker'), 'HOST': os.getenv('POSTGRES_HOST', 'localhost'), 'PORT': os.getenv('POSTGRES_PORT', '5432')}}
else:
    DATABASES = {'default': {
        'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}
AUTH_USER_MODEL = 'accounts.User'
REST_FRAMEWORK = {'DEFAULT_AUTHENTICATION_CLASSES': (
    'rest_framework_simplejwt.authentication.JWTAuthentication',), 'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',)}
SIMPLE_JWT = {
    # El access token se usa para las solicitudes normales y el refresh token
    # permite obtener uno nuevo sin pedir credenciales al jugador.
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=4),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}
# El MVP usa JWT en el header Authorization, no cookies cross-site. Por ello
# puede aceptar solicitudes desde cualquier frontend sin habilitar credenciales.
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = False
LANGUAGE_CODE = 'es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
