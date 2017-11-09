# -*- coding: utf-8 -*-

"""
Django settings for bdpy3_web_project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import json, logging, os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['BIBOURLWEB__SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = json.loads( os.environ['BIBOURLWEB__DEBUG_JSON'] )  # will be True or False

ADMINS = json.loads( os.environ['BIBOURLWEB__ADMINS_JSON'] )

ALLOWED_HOSTS = json.loads( os.environ['BIBOURLWEB__ALLOWED_HOSTS'] )  # list


# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    # 'django.contrib.sessions',
    'django.contrib.messages',
    # 'django.contrib.staticfiles',
    'bib_ourl_api_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# template_dirs = json.loads( os.environ['BIBOURLWEB__TEMPLATES_JSON'] )
# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': template_dirs,
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

WSGI_APPLICATION = 'config.passenger_wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# DATABASES = json.loads( os.environ['BIBOURLWEB__DATABASES_JSON'] )


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'  # original setting is 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

# STATIC_URL = os.environ['BIBOURLWEB__STATIC_URL']
# STATIC_ROOT = os.environ['BIBOURLWEB__STATIC_ROOT']  # needed for collectstatic command


# Email
EMAIL_HOST = os.environ['BIBOURLWEB__EMAIL_HOST']
EMAIL_PORT = int( os.environ['BIBOURLWEB__EMAIL_PORT'] )


# sessions

# <https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-SESSION_SAVE_EVERY_REQUEST>
# Thinking: not that many concurrent users, and no pages where session info isn't required, so overhead is reasonable.
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


# logging

## disable module loggers
# existing_logger_names = logging.getLogger().manager.loggerDict.keys()
# print '- EXISTING_LOGGER_NAMES, `%s`' % existing_logger_names
logging.getLogger('requests').setLevel( logging.WARNING )

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'logfile': {
            'level':'DEBUG',
            'class':'logging.FileHandler',  # note: configure server to use system's log-rotate to avoid permissions issues
            'filename': os.environ.get(u'BIBOURLWEB__LOG_PATH'),
            'formatter': 'standard',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'bib_ourl_api_app': {
            'handlers': ['logfile', 'console'],
            'level': os.environ.get(u'BIBOURLWEB__LOG_LEVEL'),
            'propagate': True
        },
    }
}

CSRF_TRUSTED_ORIGINS = json.loads( os.environ['BIBOURLWEB__CSRF_TRUSTED_ORIGINS_JSON'] )
