"""
Django settings for facemask_shop project.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from oscar.defaults import *

ROOT_DIR = environ.Path(__file__) - 3  # (facemask_shop/config/settings/base.py - 3 = facemask_shop/)
APPS_DIR = ROOT_DIR.path('facemask_shop')

# Load operating system environment variables and then prepare to use them
env = environ.Env()

# .env file, should load only in development environment
READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)

if READ_DOT_ENV_FILE:
    # Operating System Environment variables have precedence over variables defined in the .env file,
    # that is to say variables from the .env files will only be used if not defined
    # as environment variables.
    env_file = str(ROOT_DIR.path('.env'))
    env.read_env(env_file)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xqx+sj@9n-807fe*=1nb90q=ntetvqg20pa4nqj&=tpla^ri1@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []
SITE_ID = 1

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages'
]
OSCAR_CORE_APPS = [
    'oscar',
    'oscar.apps.analytics',
    # 'oscar.apps.checkout',
    'oscar.apps.address',
    # 'oscar.apps.shipping',
    # 'oscar.apps.catalogue',
    'oscar.apps.catalogue.reviews',
    # 'oscar.apps.partner',
    # 'oscar.apps.basket',
    'oscar.apps.payment',
    'oscar.apps.offer',
    # 'oscar.apps.order',
    'oscar.apps.customer',
    'oscar.apps.search',
    'oscar.apps.voucher',
    'oscar.apps.wishlists',
    # 'oscar.apps.dashboard',
    'oscar.apps.dashboard.reports',
    'oscar.apps.dashboard.users',
    # 'oscar.apps.dashboard.orders',
    'oscar.apps.dashboard.catalogue',
    'oscar.apps.dashboard.offers',
    'oscar.apps.dashboard.partners',
    'oscar.apps.dashboard.pages',
    'oscar.apps.dashboard.ranges',
    'oscar.apps.dashboard.reviews',
    'oscar.apps.dashboard.vouchers',
    'oscar.apps.dashboard.communications',
    'oscar.apps.dashboard.shipping',
]
OSCAR_EXTRA_APPS = [
    'mollie_oscar',
]
OSCAR_THIRD_PARTY_APPS = [
    'widget_tweaks',
    'haystack',
    'treebeard',
    'sorl.thumbnail',
    'django_tables2',
]
THIRD_PARTY_APPS = []
OSCAR_LOCAL_APPS = [
    'facemask_shop.basket.apps.BasketConfig',
    'facemask_shop.catalogue.apps.CatalogueConfig',
    'facemask_shop.checkout.apps.CheckoutConfig',
    'facemask_shop.order.apps.OrderConfig',
    'facemask_shop.partner.apps.PartnerConfig',
    'facemask_shop.shipping.apps.ShippingConfig',
    'facemask_shop.dashboard.apps.DashboardConfig',
    'facemask_shop.dashboard.orders.apps.OrdersDashboardConfig',
]
LOCAL_APPS = [
    'facemask_shop.shop.apps.ShopConfig',
    'facemask_shop.editor.apps.EditorConfig',
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + OSCAR_LOCAL_APPS + OSCAR_CORE_APPS + OSCAR_EXTRA_APPS + OSCAR_THIRD_PARTY_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'oscar.apps.basket.middleware.BasketMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(ROOT_DIR.path('templates')),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'oscar.apps.search.context_processors.search_form',
                'oscar.apps.checkout.context_processors.checkout',
                'oscar.apps.customer.notifications.context_processors.notifications',
                'oscar.core.context_processors.metadata',
                'facemask_shop.context_processors.sentry',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': env.db('DATABASE_URL', default='sqlite:///{}'.format(ROOT_DIR.path('db.sqlite3'))),
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    'oscar.apps.customer.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Email
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL',
                         default='Mondmasker.app <info@mondmasker.app>')
SERVER_EMAIL = env('DJANGO_SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)
USER_EMAIL_SUBJECT_PREFIX = env('DJANGO_USER_EMAIL_SUBJECT_PREFIX', default='')
EMAIL_SUBJECT_PREFIX = env('DJANGO_EMAIL_SUBJECT_PREFIX', default='[Mondmasker.app]%s ' % USER_EMAIL_SUBJECT_PREFIX)

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'nl'
LANGUAGES = [
    ('nl', 'Nederlands'),
    ('fr', 'Francais'),
    # ('de', 'Deutsch'),
]

TIME_ZONE = 'Europe/Brussels'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    str(ROOT_DIR.path('static')),
]

# Media configuration
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR('media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# Sentry error logging
sentry_sdk.init(
    integrations=[DjangoIntegration()]
)
SENTRY_FRONTEND_DSN = env('SENTRY_FRONTEND_DSN', default=None)
SENTRY_FRONTEND_RELEASE = env('SENTRY_FRONTEND_RELEASE', default=env('SENTRY_RELEASE', default=None))
SENTRY_FRONTEND_ENVIRONMENT = env('SENTRY_FRONTEND_ENVIRONMENT', default=env('SENTRY_ENVIRONMENT', default=None))

# Oscar settings
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

OSCAR_SHOP_NAME = env('DJANGO_OSCAR_SHOP_NAME', default='Facemasksare.cool')
OSCAR_FROM_EMAIL = DEFAULT_FROM_EMAIL
OSCAR_ALLOW_ANON_CHECKOUT = True
OSCAR_DEFAULT_CURRENCY = 'EUR'
OSCAR_HIDDEN_FEATURES = ('reviews', 'wishlists')
OSCAR_GOOGLE_ANALYTICS_ID = env('DJANGO_OSCAR_GOOGLE_ANALYTICS_ID', default=None)

# Status pipeline
class OSCAR_STATUSES:
    PENDING = 'Pending payment'
    PAID = 'Being processed'
    CANCELLED = 'Cancelled'


OSCAR_INITIAL_ORDER_STATUS = OSCAR_INITIAL_LINE_STATUS = OSCAR_STATUSES.PENDING
OSCAR_ORDER_STATUS_PIPELINE = {
    OSCAR_STATUSES.PENDING: (OSCAR_STATUSES.PAID, OSCAR_STATUSES.CANCELLED,),
    OSCAR_STATUSES.PAID: (OSCAR_STATUSES.PAID, OSCAR_STATUSES.CANCELLED,),
    OSCAR_STATUSES.CANCELLED: (),
}
OSCAR_MOLLIE_CONFIRMED_STATUSES = [OSCAR_STATUSES.PAID]
OSCAR_MOLLIE_HTTPS = env.bool('DJANGO_OSCAR_MOLLIE_HTTPS', True)

# Mollie settings
MOLLIE_API_KEY = env('DJANGO_MOLLIE_API_KEY', default='dummy-mollie-key')
MOLLIE_STATUS_MAPPING = {
    'Paid': OSCAR_STATUSES.PAID,
    'Pending': OSCAR_STATUSES.PENDING,
    'Open': OSCAR_STATUSES.PENDING,
    'Cancelled': OSCAR_STATUSES.CANCELLED,
}


FACEMASKME_PRODUCT_IDS = env.dict('DJANGO_FACEMASKME_PRODUCT_IDS', default={
    'own_design': '1',
    'selfie': '3',
})
