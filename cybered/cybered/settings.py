"""
Django settings for cybered project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import pathlib

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHARED_DIR = "shared"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "5h^tgrioq&37a#hvh_s4_j7bnx-@ses463sn@kj%c_mn7z$41r"

# When not in debug mode, attempt to get the secret key
# from file
RELEASE_KEY_FILE = "/etc/django/secret.txt"
ALLOWED_HOSTS = []

if not DEBUG:
    from .src.release_settings import *

    ALLOWED_HOSTS = get_allowed_hosts()

    try:
        SECRET_KEY = read_key_file(RELEASE_KEY_FILE)
    except OSError as e:
        print("WARNING: Unable to open key file - ", e)

# Application definition

INSTALLED_APPS = [
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # The site index, a landing page from which everything else is discoverable.
    "landingpage.apps.LandingpageConfig",
    # Modules
    "hashing.apps.HashingConfig",
    "steganography.apps.SteganographyConfig",
    "passwords.apps.PasswordsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
# Make the session cookie last at most three days
SESSION_COOKIE_AGE = 60 * 60 * 24 * 3
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

ROOT_URLCONF = "cybered.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, SHARED_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "libraries": {"common_filters_tags": "shared.templatetags.common_extras"},
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "cybered.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = []


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, SHARED_DIR, "static")]
STATIC_ROOT = str(pathlib.Path("../staticroot/").resolve())
