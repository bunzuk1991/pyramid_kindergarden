from kindergarden.models.bases import *
from kindergarden.lib.generic import GenericView, GenericForm
from pyramid.view import view_config





class Organisation(GenericView):
    request = None

    def __init__(self, request):
        super().__init__(request)

    model = Organisation
    form = GenericForm
    verbose_name = 'organisation'
    verbose_name_plural = 'organisations'
    verbose_name_i18n = 'організація'
    verbose_name_plural_i18n = 'організації'


