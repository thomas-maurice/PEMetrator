# Copyright (C) 2015 Thomas Maurice <thomas@maurice.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

from __future__ import absolute_import

import os
import djcelery
from datetime import timedelta
from .celery import app as celery_app

djcelery.setup_loader()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not os.path.exists(os.path.join(BASE_DIR, "logs")):
    os.makedirs(os.path.join(BASE_DIR, "logs"))

SECRET_KEY = 'secretlol'
DEBUG = True

ALLOWED_HOSTS = []

LOGIN_URL = "/registration/login/"
LOGIN_REDIRECT_URL = "/ssl/certificates/1"

# Application definition
INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'registration.backends.hmac',
    'djcelery',
    'djmail',
    'bootstrapform',
    'user',
    'certificates',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'webapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'webapp.wsgi.application'

# This is an example configuration obviously.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ssldb',
        'USER': 'ssldb',
        'PASSWORD': 'ssldb',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Not mandatory, you can enable this if you want
"""
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "KEY_PREFIX": "dj-cache",
        "VERSION": 1,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": 3,
            "SOCKET_TIMEOUT": 3,
            "IGNORE_EXCEPTIONS": True,
        }
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True
"""

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "common", 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Used buy Django registration
ACCOUNT_ACTIVATION_DAYS = 7

# Celery configuration
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_TASK_RESULT_EXPIRES = 3600
CELERY_TIMEZONE = 'Europe/Paris'
CELERY_TIMEZONE = 'UTC'

celery_app.conf.update(CELERYBEAT_SCHEDULE={
    'djmail-retry-send-every-120-seconds': {
        'task': 'tasks.retry_send_messages',
        'schedule': timedelta(seconds=600),
    },
    'cleanup-expired-certificates': {
        'task': 'certificates.tasks.cleanups.check_expired_certificates',
        'schedule': timedelta(seconds=60),
    },
})

# Email configuration
DJMAIL_MAX_RETRY_NUMBER = 30
EMAIL_BACKEND="djmail.backends.celery.EmailBackend"
DJMAIL_REAL_BACKEND="django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST="yourserver.tld"
EMAIL_PORT="587"
EMAIL_HOST_USER="noreply"
EMAIL_HOST_PASSWORD="password"
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL = "ssl robot <noreply@yourserver.tld>"

# Registration settings
REGISTRATION_OPEN = True

USE_TZ=True
