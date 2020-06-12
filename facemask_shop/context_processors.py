import json

from django.conf import settings
from django.utils.safestring import mark_safe


def playcanvas_editor(request):
    return {
        'playcanvas_root': settings.STATIC_URL + 'editor/playcanvas/%s/' % settings.FACEMASK_EDITOR_VERSION
    }


def sentry(request):
    if not settings.SENTRY_FRONTEND_DSN:
        return {'sentry_config': None}
    return {
        'sentry_config': mark_safe(json.dumps({
            'dsn': settings.SENTRY_FRONTEND_DSN,
            'release': settings.SENTRY_FRONTEND_RELEASE,
            'environment': settings.SENTRY_FRONTEND_ENVIRONMENT,
        }))
    }
