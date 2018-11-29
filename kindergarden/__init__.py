from pyramid.config import Configurator
from sqlalchemy import event, engine_from_config
from kindergarden.models.bases import DBSession, Base
from pyramid.session import SignedCookieSessionFactory


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    my_session_factory = SignedCookieSessionFactory('bunzuk1991')
    # engine = engine_from_config(settings, 'sqlalchemy.')
    # DBSession.configure(bind=engine)
    # Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.set_session_factory(my_session_factory)
    config.include('pyramid_jinja2')
    config.include('kindergarden.models')
    config.include('kindergarden.routes')
    config.scan()
    return config.make_wsgi_app()
