"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 3.2.15.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from pickle import FALSE
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0tj8u#-81x-5^1mvjl3)xuni9xh^eomk&e@jv!ukzs!d&x0t%='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["165.227.45.234","copy-products.com","www.copy-products.com"]
APP_URL = 'https://copy-products.com'


# Application definition

INSTALLED_APPS = [
    'shopify_auth',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'auth_app',
    'importproduct',
    'rest_framework',
    'background_task',

]
AUTH_USER_MODEL = 'auth_app.AuthAppShopUser'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR /"templates",],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'shopify_auth.context_processors.shopify_auth',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}
#
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'copy_productdb',
        'USER': 'mydbshuser',
        'PASSWORD': 'Og@9s@oS_54@dY0@o58T',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

#STATICFILES_DIRS = [ os.path.join(BASE_DIR, 'static/'),]
STATICFILES_DIRS = "/home/kira/copyproducts/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static-root/')

MEDIA_URL='/media/'
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Configure Shopify Application settings
SHOPIFY_APP_NAME = 'CopYIT - Import Products'
SHOPIFY_APP_API_KEY = ""
SHOPIFY_APP_API_SECRET = ""
SHOPIFY_APP_API_SCOPE = ['read_products','write_products','read_product_listings',]
# Find API version to pin at https://help.shopify.com/en/api/versioning
SHOPIFY_APP_API_VERSION = "2022-07"
SHOPIFY_APP_IS_EMBEDDED = False
SHOPIFY_APP_DEV_MODE = False
# Use the Shopify Auth authentication backend as the sole authentication backend.
AUTHENTICATION_BACKENDS = (
    'shopify_auth.backends.ShopUserBackend',
)
# Add the Shopify Auth template context processor to the list of processors.
# Note that this assumes you've defined TEMPLATE_CONTEXT_PROCESSORS earlier in your settings.
# Set the login redirect URL to the "home" page for your app (where to go after logging on).
LOGIN_REDIRECT_URL = '/'
# Set secure proxy header to allow proper detection of secure URLs behind a proxy.
# This ensures that correct 'https' URLs are generated when our Django app is running behind a proxy like nginx, or is
# being tunneled (by ngrok, for example).
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
