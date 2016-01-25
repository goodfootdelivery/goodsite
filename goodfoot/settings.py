# """
# Django settings for goodfoot project.
#
# Generated by 'django-admin startproject' using Django 1.8.7.
#
# For more information on this file, see
# https://docs.djangoproject.com/en/1.8/topics/settings/
#
# For the full list of settings and their values, see
# https://docs.djangoproject.com/en/1.8/ref/settings/
# """

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6ir@9v=_bip+2%r=4g@78d0pmg_zy_t_k99^+i70(=3ng^mh4p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrapform',
    'account',
    'leaflet',
    'rest_framework',
    'api',
    # Dev only:
    'corsheaders',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Dev only:
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'account.middleware.LocaleMiddleware',
    'account.middleware.TimezoneMiddleware',
)

ROOT_URLCONF = 'goodfoot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'goodfoot', 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',
                'account.context_processors.account',
            ],
        },
    },
]

WSGI_APPLICATION = 'goodfoot.wsgi.application'

# Session Serializer
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dev',
        'USER': 'root',
        'PASSWORK': 'koncluv102',
        'HOST': 'localhost',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Site Settings
SITE_ID = 1


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'goodfoot', 'static'),
)

# Grappelli Settings
GRAPPELLI_ADMIN_TITLE = 'GoodFoot Delivery'

# Login Settings
LOGIN_URL = '/account/login'

LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (43.66, -79.40),
    'DEFAULT_ZOOM': 11,
    'MIN_ZOOM': 5,
    'MAX_ZOOM': 18,
}

REST_FRAMEWORK = {
    'PAGE_SIZE': 10
}

# DEV ONLY, CORS HEADERS
CORS_ORIGIN_ALLOW_ALL = True
