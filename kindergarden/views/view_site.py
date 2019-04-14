from pyramid.view import view_config
from pyramid.response import Response
from ..models.bases import *


@view_config(route_name='dashboard', renderer='kindergarden:templates/site/main.jinja2')
def dashboard(request):
    return {}


@view_config(route_name='childrens', renderer='kindergarden:templates/site/childrens.jinja2')
def childrens(request):
    ch_list = session_db.query(Children).all()
    return {}


