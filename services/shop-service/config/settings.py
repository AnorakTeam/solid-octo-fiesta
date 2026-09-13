import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'shop-service-secret-key-change-in-production')
JWT_SIGNING_KEY = os.getenv('JWT_SIGNING_KEY', SECRET_KEY)
INTERNAL_API_SECRET = os.getenv('INTERNAL_API_SECRET', 'internal-shared-secret-key-123')
GAME_SERVICE_URL = os.getenv('GAME_SERVICE_URL', 'http://game-service:8002')
DEBUG = os.getenv('DJANGO_DEBUG', '1') == '1'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'apps.shop',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.request',
        ]
    }
}]

WSGI_APPLICATION = 'config.wsgi.application'


DB_ENGINE = os.getenv('DB_ENGINE', 'postgres').lower()
DATABASE_URL = os.getenv('DATABASE_URL') or os.getenv('SHOP_DATABASE_URL')
DB_SSL_REQUIRE = os.getenv('DB_SSL_REQUIRE', '0') == '1'

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=DB_SSL_REQUIRE
        )
    }
elif DB_ENGINE == 'postgres':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB', 'shop_db'),
            'USER': os.getenv('POSTGRES_USER', 'clicker'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'clicker'),
            'HOST': os.getenv('POSTGRES_HOST', 'db'),
            'PORT': os.getenv('POSTGRES_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

REST_FRAMEWORK = {
    'UNAUTHENTICATED_USER': None,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'apps.shop.auth.StatelessJWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = False

LANGUAGE_CODE = 'es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
