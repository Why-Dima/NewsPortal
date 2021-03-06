"""
Django settings for NewsPaper project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console_debug': {
            'format': '{asctime} - {levelname} - {message}',
            'style': '{',
        },
        'console_warning': {
            'format': '{asctime} - {levelname} - {message} - {pathname}',
            'style': '{',
        },
        'console_error': {
            'format': '{asctime} - {levelname} - {message} - {pathname} - {exc_info}',
            'style': '{',
        },
        'simple': {
            'format': '{asctime} - {levelname} - {module} - {message}',
            'style': '{',
        },

    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'console_error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'console_error',
            'filename': 'errors.log',
        },
        'console_general': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'filename': 'general.log',
        },
        'console_security': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'filename': 'security.log',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'simple',
        }
    },
    'loggers': {
        'console': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers': ['console_general'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console_error', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['console_error', 'mail_admins'],
            'propagate': True,
        },
        'django.template': {
            'handlers': ['console_error'],
            'propagate': True,
        },
        'django.db_backends': {
            'handlers': ['console_error'],
            'propagate': True,
        },
        'django.security': {
            'handlers': ['console_security'],
            'propagate': True,
        },
    }
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-i@6l!nb-hyux4n@9bntin^p8w_t&^f^9g5jo5p=0bp(2)nrot1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django_filters',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'news.apps.NewsConfig',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'accounts',
    'fpages',
    'sign',
    'django.core.mail',

    'django_apscheduler',

    'django_celery_beat',

]

DEFAULT_FROM_EMAIL = 'newspost1@yandex.ru'

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',


]

ROOT_URLCONF = 'NewsPaper.urls'

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

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

WSGI_APPLICATION = 'NewsPaper.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [BASE_DIR / 'static']

LOGIN_URL = '/accounts/login/'

LOGIN_REDIRECT_URL = '/'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_FORMS = {'signup': 'sign.models.BasicSignupForm'}


EMAIL_HOST = 'smtp.yandex.ru'  # ?????????? ?????????????? ????????????-?????????? ?????? ???????? ???????? ?? ?????? ????
EMAIL_PORT = 465  # ???????? smtp ?????????????? ???????? ????????????????????
EMAIL_HOST_USER = 'newspost1'  # ???????? ?????? ????????????????????????, ????????????????, ???????? ???????? ?????????? user@yandex.ru, ???? ???????? ???????? ???????????? user, ?????????? ??????????????, ?????? ?????? ???? ?????? ???????? ???? ????????????
EMAIL_HOST_PASSWORD = 'Znachit_A!'  # ???????????? ???? ??????????
EMAIL_USE_SSL = True  # ???????????? ???????????????????? ssl, ?????????????????? ?? ??????, ?????? ??????, ?????????????????? ?? ???????????????????????????? ????????????????????, ???? ???????????????? ?????? ?????????? ??????????????????????


APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
APSCHEDULER_RUN_NOW_TIMEOUT = 25

CELERY_BROKER_URL = 'redis://:19P5iAltZP0iIUwAYjjmnXraMQxuTX4E@redis-16719.c93.us-east-1-3.ec2.cloud.redislabs.com:16719/0'
CELERY_RESULT_BACKEND = 'redis://:19P5iAltZP0iIUwAYjjmnXraMQxuTX4E@redis-16719.c93.us-east-1-3.ec2.cloud.redislabs.com:16719/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'), # ??????????????????, ???????? ?????????? ?????????????????? ???????????????????? ??????????!
        'TIMEOUT': 60,
    }
}
