from .views import view_site


def includeme(config):
    config.add_route('dashboard', '/dashboard')
    config.add_route('childrens', '/childrens')
    config.add_route('children_action', '/children/{action}')
    config.add_route('main', '/')
    # config.add_view(view_site.dashboard, route_name='dashboard', renderer='kindergarden:templates/site/main.jinja2')
    # config.add_view(view_site.childrens, route_name='childrens', renderer='kindergarden:templates/site/childrens.jinja2')
