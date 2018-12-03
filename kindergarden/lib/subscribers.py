from pyramid.httpexceptions import HTTPForbidden
from pyramid.threadlocal import get_current_request

from kindergarden.lib import helpers
from kindergarden.lib.i18n import ugettext as _
# from kindergarden.models import SYSTEM_SCHEMA, PUBLIC_SCHEMA, DBSession


def add_renderer_globals(event, request=None):
    if request is None:
        request = event.get('request', get_current_request())

    event['_'] = request.translate
    event['h'] = helpers


def add_localizer(event, request=None):
    if request is None:
        request = getattr(event, 'request', get_current_request())

    request.translate = lambda string: _(string, request=request)


def add_csrf_validation(event, request=None):
    request = getattr(event, 'request', request)

    if request.method == 'POST':
        token = request.POST.get('_csrf')
        if token is None or token != request.session.get_csrf_token():
            raise HTTPForbidden('CSRF token is missing or invalid')


# def pg_set_search_path(event, request=None):
#     DBSession.execute('SET search_path TO %s,%s' % (SYSTEM_SCHEMA, PUBLIC_SCHEMA))
