import os
import sys

import environ

env = environ.Env(
    ALLOWED_HOSTS=(list, []),
    CSRF_COOKIE_SECURE=(bool, True),
    DEBUG=(bool, False),
    SECURE_SSL_REDIRECT=(bool, True),
    SESSION_COOKIE_SECURE=(bool, True)
)

environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: keep the secret key used in production secret!
# Used to encrypt/decrypt certain features in the database
FERNET_KEY = env('FERNET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env('ALLOWED_HOSTS')

# Application definition

# Django Applications
INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django_celery_results',
    'debug_toolbar',
    'rest_auth',
    'rest_framework',
    'rest_framework.authtoken',
]

# Project Applications
INSTALLED_APPS.extend([
    'account.account',
    'account.login',
    'billing.payment',
    'billing.reason',
    'company.company',
    'company.dns',
    'company.domain',
    'database',
    'hardware.client',
    'hardware.company',
    'network.pool',
    'setting.banned',
    'setting.email',
    'store.fraud',
    'store.product',
    'store.product.domain',
    'store.product.price',
    'worker.apache',
    'worker.awstats',
    'worker.bind',
    'worker.console',
    'worker.cron',
    'worker.daemon',
    'worker.dovecot',
    'worker.ejabberd',
    'worker.mail',
    'worker.mysql',
    'worker.nginx',
    'worker.php',
    'worker.postfix',
    'worker.postgresql',
    'worker.queue',
    'worker.rabbitmq',
    'worker.system',
    'worker.vsftpd',
    'worker.web'
])

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'application.urls'

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
                'django.contrib.messages.context_processors.messages'
            ]
        }
    }
]

WSGI_APPLICATION = 'application.wsgi.application'

# Database
DATABASES = {
    'default': env.db('DATABASE_DEFAULT'),
    'default_read1': env.db('DATABASE_READ1')
}

# Database Routers
DATABASE_ROUTERS = [
    'database.router.ReadWrite'
]

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 5
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    }
]

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

"""
Django Rest
"""

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication'
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}

"""
Login Settings
"""

# Login / Redirect URL's
LOGIN_URL = '/api-auth/login/'
LOGIN_REDIRECT_URL = '/'

# Logout / Redirect URL's
LOGOUT_URL = '/api-auth/logout/'
LOGOUT_REDIRECT_URL = LOGIN_URL

# Authentication Model
AUTH_USER_MODEL = 'database.Account'

"""
Email Settings
"""

# Backend
EMAIL_BACKEND = env('EMAIL_BACKEND')

# Hostname
EMAIL_HOST = env('EMAIL_HOST')

# Username
EMAIL_HOST_USER = env('EMAIL_HOST_USER')

# Password
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

# Port
EMAIL_PORT = env('EMAIL_PORT')

# TLS Support
EMAIL_USE_TLS = env('EMAIL_USE_TLS')

# From Email Address
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

#
# Set the administrator email address(es)
#
# Only used when important notications need to be sent
# Example; Queue failed to process
#
# For more than 1 admin, recommended to use a mailing list address here
ADMINS = [
    env.tuple('ADMINS')
]

#
# Set the manager email address(es)
#
# Only used when DEBUG is False
# Example; 404 Errors
#
# For more than 1 manager, recommended to use a mailing list address here
MANAGERS = [
    env.tuple('MANAGERS')
]

"""
COR Headers
"""

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_EXPOSE_HEADERS = (
    'Access-Control-Allow-Origin: *',
)

"""
Sites
"""

SITE_ID = env('SITE_ID')

"""
Debug Toolbar
"""

INTERNAL_IPS = ALLOWED_HOSTS

DEBUG_TOOLBAR_PANELS = [
    # 'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    # 'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    # 'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    # 'debug_toolbar.panels.signals.SignalsPanel',
    # 'debug_toolbar.panels.logging.LoggingPanel',
    # 'debug_toolbar.panels.redirects.RedirectsPanel',
    # 'debug_toolbar.panels.profiling.ProfilingPanel'
]

"""
Celery
"""

CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'default'

BROKER_USER = env('CELERY_BROKER_USER')
BROKER_PASSWORD = env('CELERY_BROKER_PASSWORD')
BROKER_HOST = env('CELERY_BROKER_HOST')
BROKER_PORT = env('CELERY_BROKER_PORT')
BROKER_VHOST = env('CELERY_BROKER_VHOST')

CELERY_BROKER_URL = f"amqp://{BROKER_USER}:{BROKER_PASSWORD}@{BROKER_HOST}:{BROKER_PORT}/{BROKER_VHOST}"

"""
Operating System
"""

OS_NIC = env('OS_NIC')

OS_NS_1 = env('OS_NS_1')
OS_NS_2 = env('OS_NS_2')

OS_TYPE = env('OS_TYPE')

OS_QUEUE_SLEEP_CYCLE = env('OS_QUEUE_SLEEP_CYCLE')
OS_QUEUE_SLEEP_TASKS = env('OS_QUEUE_SLEEP_TASKS')

"""
CACHE
"""

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'django_cache'
    }
}

"""
CSRF
"""

CSRF_COOKIE_SECURE = env('CSRF_COOKIE_SECURE')

"""
SSL
"""

SECURE_HSTS_SECONDS = 0
SECURE_SSL_REDIRECT = env('SECURE_SSL_REDIRECT')

"""
Session
"""

SESSION_COOKIE_SAMESITE = None
SESSION_COOKIE_SECURE = env('SESSION_COOKIE_SECURE')
