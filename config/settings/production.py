from .base import *

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['facemask.monkeyman.be'])

STATIC_ROOT = str(ROOT_DIR.path('assets/static/'))

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
