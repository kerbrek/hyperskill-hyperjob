import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .settings import *  # pylint: disable=wildcard-import, unused-wildcard-import


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get('DEBUG', default=0))

# Configure the domain name using the environment variable
# that Azure automatically creates for us.
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']]

# Configure custom domain names if available
if 'CUSTOM_DOMAINS' in os.environ:
    domains = os.environ['CUSTOM_DOMAINS'].split(',')
    ALLOWED_HOSTS = [*ALLOWED_HOSTS, *domains]


# WhiteNoise configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Add whitenoise middleware after the security middleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Configure Postgres database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DBNAME'],
        'HOST': os.environ['DBHOST'],
        'USER': os.environ['DBUSER'],
        'PASSWORD': os.environ['DBPASS'],
        'OPTIONS': {'sslmode': 'require'}
    }
}


# Sentry configuration
if 'SENTRY_DSN' in os.environ:
    sentry_sdk.init(
        dsn=os.environ['SENTRY_DSN'],
        integrations=[DjangoIntegration()],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=float(os.environ.get(
            'SENTRY_TRACES_SAMPLE_RATE', default=1.0)),

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=int(os.environ.get(
            'SENTRY_SEND_DEFAULT_PII', default=1))
    )


# Security settings
CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True

SECURE_BROWSER_XSS_FILTER = True

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = 'DENY'
