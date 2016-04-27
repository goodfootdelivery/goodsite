"""
Django settings for goodfoot project on Heroku. Fore more info, see:
https://github.com/heroku/heroku-django-template

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import socket

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Production vs. Local Settings
if socket.gethostname() == 'box3045.bluehost.com':
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": "goodfop0_gamma",
            'USER': 'goodfop0',
            'PASSWORD': 'Redmond2013!',
            'HOST': 'localhost'
        }
    }
    DEBUG = False
    STATIC_ROOT = os.path.join('/home2/goodfop0/public_html/gamma/static')

elif socket.gethostname() == 'Connors-MacBook-Pro.local':
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "dev.db",
        }
    }
    DEBUG = True
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

else:
    import dj_database_url
    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(db_from_env)
    DEBUG = True
    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "0i+s(u^($6&7@uy-vrujwo^!h16n5yk=7j4y3g0@evpvgu_2pl"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = [
    'grappelli',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    # api
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'corsheaders',
    # theme
    "bootstrapform",
    # external
    "metron",
    # project
    "goodfoot",
    'delivery',
    'invoicing',
]

MIDDLEWARE_CLASSES = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    # Cors
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'django.middleware.security.SecurityMiddleware',
]

ROOT_URLCONF = 'goodfoot.urls'

TEMPLATES = (
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
            'debug': DEBUG,
        },
    },
)

WSGI_APPLICATION = 'goodfoot.wsgi.application'


AUTH_PASSWORD_VALIDATORS = (
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
)

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'US/Eastern'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']
# Cors Settings
CORS_ORIGIN_ALLOW_ALL = True


# REST Settings


REST_FRAMEWORK = {
    'PAGE_SIZE': 20
}


# Static files (CSS, JavaScript, Images)


STATIC_URL = '/static/'
# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
]
# Simplified static file serving.
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
# https://warehouse.python.org/project/whitenoise/



# Delivery APP Settings



# Google Key
G_KEY = 'AIzaSyAF5a1ktypMvsvnMMnoaFGHkmt_9vnWfok'
# Easypost Key
EP_KEY = 'OJwynagQo2hRGHBnKbAiHg' # TEST
# Office Location
OFFICE_SHORT = '720 Bathurst St, Toronto, ON M5S 2R4, CA'
OFFICE_LONG = {
    'name' : 'GoodFoot Delivery Office',
    'phone' : '416 572 3771',
    'street1' : '720 Bathurst St',
    'street2' : '411',
    'city' : 'Toronto',
    'state' : 'ON',
    'country' : 'Canada',
    'zip' : 'M5S 2R4'
}


if __name__ == '__main__':
    print "Base Dir:"
    print BASE_DIR
    print
    print 'Project Dir'
    print PROJECT_ROOT
