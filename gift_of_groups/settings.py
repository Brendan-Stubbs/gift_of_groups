"""
Django settings for gift_of_groups project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECURITY WARNING: don't run with debug turned on in production!
try:
    from gift_of_groups import local_settings
    DEBUG = local_settings.DEBUG
    ENVIRONMENT = local_settings.ENVIRONMENT
    SECRET_KEY = local_settings.SECRET_KEY
    DOMAIN_NAME = local_settings.DOMAIN_NAME
except:
    DEBUG = True
    ENVIRONMENT = "local"
    SECRET_KEY = "fe1769t_=18)kl@p-hq97&id3l&r=c1zrn8zy#7!zv-2gtks0_"
    DOMAIN_NAME = "http://127.0.0.1:8090"

ALLOWED_HOSTS = ["www.giftlygroups.com", "localhost", "127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "crispy_forms",
    "uac.apps.UacConfig",
    "gifts.apps.GiftsConfig",
    "social_django",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "social_core.backends.facebook.FacebookOAuth2",
    "social_core.backends.google.GoogleOAuth2",

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
]

ROOT_URLCONF = "gift_of_groups.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates", os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'utils.custom_context_processors.get_custom_context_processors',
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

WSGI_APPLICATION = "gift_of_groups.wsgi.application"

try:
    DATABASES = local_settings.DATABASES
except:
  DATABASES = {
      'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_DATABASE'),
        'USER': os.environ.get('MYSQL_USER'),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD'),
        'HOST': os.environ.get('MYSQL_HOST'),
        'OPTIONS': {
          'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
      },
      }
  }


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"
if ENVIRONMENT == "live":
    STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
] if ENVIRONMENT == "local" else []


CRISPY_TEMPLATE_PACK = "bootstrap4"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = "/login"

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.INFO: '',
    30: 'red-text',
    25: 'green-text'
}

try:
    ACTIVATE_EMAIL_ON_ENVIRONMENT = local_settings.ACTIVATE_EMAIL_ON_ENVIRONMENT
except:
    ACTIVATE_EMAIL_ON_ENVIRONMENT = False

try:
    EMAIL_HOST_USER = local_settings.EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD = local_settings.EMAIL_HOST_PASSWORD
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = 'Giftly Groups <giftlygroups@gmail.com>'
except:
    print("Add email settings in local_settings.py")
