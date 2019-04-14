from kindergarden.models.bases import *
from kindergarden.lib.generic import GenericView, GenericForm
from pyramid.view import view_config


def get_tables_names():
    info = []
    for base in Base._decl_class_registry.values():
        if hasattr(base, '__table__'):
            info_detail = {"name": base.__table__.fullname, "class": base}
            info.append(info_detail)
    return info


def return_values(name):
    tables = get_tables_names()
    for a in tables:
        if name == a['name']:
            return a

    return None


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


class Group(GenericView):
    request = None

    def __init__(self, request):
        super().__init__(request)

    model = Group
    form = GenericForm
    verbose_name = 'group'
    verbose_name_plural = 'groups'
    verbose_name_i18n = 'група'
    verbose_name_plural_i18n = 'групи'


class GardenGroup(GenericView):
    request = None

    def __init__(self, request):
        super().__init__(request)

    model = GardenGroup
    form = GenericForm
    verbose_name = 'gardengroup'
    verbose_name_plural = 'gardengroups'
    verbose_name_i18n = 'група (статичні)'
    verbose_name_plural_i18n = '(статичні)'

class Children(GenericView):
    request = None

    def __init__(self, request):
        super().__init__(request)

    model = Children
    form = GenericForm
    verbose_name = 'children'
    verbose_name_plural = 'childrens'
    verbose_name_i18n = 'діти (перелік)'
    verbose_name_plural_i18n = 'дітей (перелік)'



class AdminView(GenericView):
    request = None

    def __init__(self, request):
        super().__init__(request)

    model = None
    form = None
    verbose_name = ''
    verbose_name_plural = ''
    verbose_name_i18n = verbose_name
    verbose_name_plural_i18n = verbose_name_plural


class AdminList(object):
    views = []
    list = []
    rout_names = []

    @classmethod
    def register_site(cls, name):
        if name and not name in cls.views:
            cls.views.append(name)

    @classmethod
    def get_views(cls):
        cls.list = []
        for elem in cls.views:
            ret_value = return_values(elem)
            if ret_value is not None:
                new_class = type('%s%s' % (ret_value["name"].capitalize(), 'View'), (GenericView,), {
                    'model': ret_value["class"],
                    'form': GenericForm,
                    'verbose_name': ret_value["name"],
                    'verbose_name_plural': ret_value["name"],
                    'verbose_name_i18n': ret_value["name"],
                    'verbose_name_plural_i18n': ret_value["name"]
                })
                cls.list.append({"route_name": ret_value["name"], "view_class": new_class})
                cls.rout_names.append('%s_%s' % (ret_value["name"], 'list'))
        return cls.list


@view_config(route_name='admin', renderer='kindergarden:templates/admin.mako')
def admin(request):
    return {'sites': AdminList.rout_names}
