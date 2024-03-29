"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from core import variables
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = variables.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = variables.DEBUG

ALLOWED_HOSTS = variables.ALLOWED_HOSTS

# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # packages
    'django_celery_beat',
    # apps
    'apps.pricing'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': variables.DATABASE
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'zh-hant'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# django-redis
CACHES = {
    "default": variables.CACHE
}

# logging
import logging  # noqa

LOGS_FOLDER = os.path.join(BASE_DIR, 'logs')
if not os.path.isdir(LOGS_FOLDER):
    logging.info("CREATE LOGS Folder.")
    os.makedirs(LOGS_FOLDER)
else:
    logging.info("LOGS Folder is exists.")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 設定已存在的logger不失效
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s - %(filename)s -> %(funcName)s - %(lineno)d : %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, "logs", 'backend.log'),
            'when': 'midnight',
            'formatter': 'standard',
        },
        'celery': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, "logs", 'celery.log'),
            'when': 'midnight',
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            'level': 'INFO',
            'handlers': ['console', 'default']
        },
        'django.celery': {
            'level': 'INFO',
            'handlers': ['console', 'celery']
        },
        'gunicorn': {
            'level': 'INFO',
            'handlers': ['console', 'default']
        }
    },
}

# CELERY STUFF
CELERY_BROKER_URL = f"{variables.CACHE['LOCATION']}/1"
CELERY_RESULT_BACKEND = f"{variables.CACHE['LOCATION']}/0"
CELERY_TIMEZONE = "UTC"
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_IMPORTS = ["core.tasks"]
CELERY_BEAT_SCHEDULE = {
    "system-get-pricing": {
        "task": "system-get-pricing",
        "schedule": 10.0
    }
}

ASGI_APPLICATION = "core.asgi.application"
