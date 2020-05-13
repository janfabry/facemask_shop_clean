from .base import *

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['facemask.monkeyman.be'])

STATIC_ROOT = str(ROOT_DIR.path('assets/static/'))


# STORAGES
# ------------------------------------------------------------------------------
# https://django-storages.readthedocs.io/en/latest/#installation
INSTALLED_APPS += ["storages"]  # noqa F405

# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_ACCESS_KEY_ID = env("DJANGO_AWS_ACCESS_KEY_ID")
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_SECRET_ACCESS_KEY = env("DJANGO_AWS_SECRET_ACCESS_KEY")
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_STORAGE_BUCKET_NAME = env("DJANGO_AWS_STORAGE_BUCKET_NAME")
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_QUERYSTRING_AUTH = True
# DO NOT change these unless you know what you're doing.
_AWS_EXPIRY = 60 * 60 * 24 * 7
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": f"max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate"
}
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_DEFAULT_ACL = None
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_S3_REGION_NAME = env("DJANGO_AWS_S3_REGION_NAME", default='eu-central-1')
AWS_S3_ADDRESSING_STYLE = "virtual"


# MEDIA
# ------------------------------------------------------------------------------
DEFAULT_FILE_STORAGE = "config.storages.MediaRootS3Boto3Storage"
MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/"


# EMAIL
# ------------------------------------------------------------------------------

# Anymail with Mailgun
INSTALLED_APPS += ['anymail', ]
ANYMAIL = {
    'MAILGUN_API_KEY': env('DJANGO_MAILGUN_API_KEY'),
    'MAILGUN_SENDER_DOMAIN': env('DJANGO_MAILGUN_SENDER_DOMAIN', default='mg.mondmasker.app'),
    'MAILGUN_API_URL': env('DJANGO_MAILGUN_API_URL', default='https://api.eu.mailgun.net/v3'),
}
EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'


# LOGGING CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
LOG_DIR = env('DJANGO_LOG_DIR', default=str((ROOT_DIR - 1).path('log')))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'WARNING',
        'handlers': ['file'],
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false', ],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_DIR + '/django-info.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', ],
            'level': 'INFO',
            'propagate': True
        },
    }
}

if env.bool('DJANGO_EXTENSIONS', False):
    INSTALLED_APPS += ['django_extensions']  # noqa F405
