"""
Django settings for energy_monitoring project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import mongoengine
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-u0m#p#mu$ua9n0f2f=j6zypav$@-%p2sqa+gr@6!!(b(^tb*^='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sensor_data',
    'rest_framework',
    'django_mongoengine',
    'rest_framework_mongoengine',

]
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'energy_monitoring.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'energy_monitoring.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
# Configuration MongoDB avec mongoengine
MONGODB_DATABASES = {
    'default': {
        'name': 'sensors_bd',
        'host': 'localhost',
        'port': 27017,
    }
}
# Connexion à MongoDB
mongoengine.connect(
    db=MONGODB_DATABASES['default']['name'],
    host=MONGODB_DATABASES['default']['host'],
    port=MONGODB_DATABASES['default']['port'],
)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Base de données SQLite pour les fonctionnalités internes
        'NAME': BASE_DIR / 'db.sqlite3',         # Fichier de base de données SQLite
    }
}
# Supprimer la configuration DATABASES car mongoengine gère cela
#DATABASES = {
 #   'default': {
 #       'ENGINE': 'django.db.backends.dummy',  # Nécessaire pour éviter les erreurs Django
  #  }
#}
# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MIGRATION_MODULES = {
    'sensor_data': None,  # Désactive les migrations pour votre app
}
# Remove Redis cache configuration
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }

# Add default cache configuration using local memory
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Configuration MQTT
MQTT_BROKER = "192.168.1.14"
MQTT_PORT = 1883
MQTT_TOPIC = "esp32/#"
MQTT_CONTROL_TOPIC = "esp32/control"
MQTT_KEEPALIVE = 60
MQTT_MAX_RETRIES = 5
# settings.py
AUTOMATION_SETTINGS = {
    'LIGHT_OPTIMAL_LUX': 500,
    'TEMP_OPTIMAL_C': 22,
    'TEMP_THRESHOLD': 1.0,
    'POWER_THRESHOLD_W': 1000,
    'VOLTAGE_THRESHOLD_V': 200,
    'MOTION_TIMEOUT_MIN': 15,
}