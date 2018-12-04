from pyramid.config import Configurator
from sqlalchemy import event, engine_from_config
from pyramid.session import SignedCookieSessionFactory
from kindergarden.lib.subscribers import add_renderer_globals, add_localizer
from pyramid.events import NewRequest, BeforeRender


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    my_session_factory = SignedCookieSessionFactory('bunzuk1991')
    # engine = engine_from_config(settings, 'sqlalchemy.')
    # DBSession.configure(bind=engine)
    # Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.add_subscriber(add_renderer_globals, BeforeRender)
    config.add_subscriber(add_localizer, NewRequest)
    config.set_session_factory(my_session_factory)
    config.include('pyramid_mako')
    config.include('kindergarden.models')
    config.include('kindergarden.routes')
    # config.add_static_view(name='static', path='kindergarden:static')
    # config.add_static_view(name='static_admin', path='kindergarden:static/admin')
    config.scan()
    return config.make_wsgi_app()
