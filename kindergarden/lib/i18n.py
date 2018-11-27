from pyramid.i18n import TranslationStringFactory
from pyramid.threadlocal import get_current_request

tsf = TranslationStringFactory('kindergarden')

def ugettext(string, request=None):
    if not request:
        request = get_current_request()
    return request.localizer.translate(tsf(string))


class ugettext_lazy(object):
    def __init__(self, msg, request=None):
        self.msg = msg
        self.request = request

    def __str__(self):
        return ugettext(self.msg, self.request)
