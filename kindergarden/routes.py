from kindergarden.views.admin.organisation import AdminList


def add_crud_routes(config, route_name, route_prefix='/admin', attrs=None, attrs_except=None):
    routes = [
        ('new', '%s/%s/new', 'GET'),
        ('list', '%s/%s/list', 'GET'),
        ('crud', '%s/%s/crud', 'GET'),
        ('edit', '%s/%s/{id}/edit', 'GET'),
        ('delete', '%s/%s/{id}/delete', 'GET'),
        ('create', '%s/%s/create', 'POST'),
        ('update', '%s/%s/{id}/update', 'POST')
    ]

    if attrs:
        routes = [route for route in routes if route[0] in attrs]
    elif attrs_except:
        routes = [route for route in routes if route[0] not in attrs_except]

    for route in routes:
        print('%s_%s' % (route_name, route[0]), route[1] % (route_prefix, route_name))
        config.add_route('%s_%s' % (route_name, route[0]), route[1] % (route_prefix, route_name),
                         request_method=route[2])


def add_crud_views(config, view, route_name, attrs=None, attrs_except=None, permission=None):
    attrs = attrs or ('new', 'list', 'crud', 'create', 'update', 'edit', 'delete')

    if attrs_except:
        attrs = [attr for attr in attrs if attr not in attrs_except]

    for attr in attrs:
        config.add_view(view, attr=attr, route_name='%s_%s' % (route_name, attr), permission=permission)
        print("%s   (%s_%s)" % (view, route_name, attr))


def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('admin', '/admin', request_method='GET')
    config.add_view('kindergarden.views.admin.organisation.admin', route_name='admin',
                    renderer='kindergarden:templates/admin.mako')

    AdminList.register_site('organisation')
    AdminList.register_site('gardengroup')
    AdminList.register_site('group')

    my_routes = AdminList.get_views()

    for a in my_routes:
        add_crud_routes(config, a['route_name'])
        add_crud_views(config, a['view_class'], a['route_name'])
    #
    # add_crud_routes(config, 'gardengroup')
    # add_crud_views(config, 'kindergarden.views.admin.organisation.GardenGroup', 'gardengroup')
    #
    # add_crud_routes(config, 'group')
    # add_crud_views(config, 'kindergarden.views.admin.organisation.Group', 'group')

    config.include('kindergarden.models')
