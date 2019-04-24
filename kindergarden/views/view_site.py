from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from ..models.bases import *
from ..forms.child_create import ChildCreateForm, ParentForm
from ..services.utils import upload_file


@view_config(route_name='dashboard', renderer='kindergarden:templates/site/main.jinja2')
def dashboard(request):
    return {}


@view_config(route_name='childrens', renderer='kindergarden:templates/site/childrens.jinja2')
def childrens(request):
    ch_list = session_db.query(Children).all()
    return {'children_with_parents': ch_list}


@view_config(route_name='children_action', match_param='action=create',
             renderer='kindergarden:templates/site/child_detail.jinja2')
@view_config(route_name='children_action', match_param='action=edit',
             renderer='kindergarden:templates/site/child_detail.jinja2')
@view_config(route_name='children_action', match_param='action=save',
             renderer='kindergarden:templates/site/child_detail.jinja2')
def child_detail(request):
    matchdict = request.matchdict
    child_slug = request.params.get('slug', None)
    group_choices = [(g.id, g.name) for g in request.dbsession.query(Group).order_by('name')]

    if child_slug:
        child = request.dbsession.query(Children).filter_by(slug=child_slug).first()
        form = ChildCreateForm(request.POST, child)
        form.group_id.choices = group_choices

        if request.method == 'POST' and form.validate():
            image_name = upload_file(form.image)

            if image_name:
                child.image = image_name

            form.populate_obj(child)
            return HTTPFound(
                location=request.route_url('childrens'))

        return {'form': form, 'action': request.matchdict.get('action'), 'slug': child_slug, 'image': child.image}


    else:
        # створення нового елемента таблиці CHILD
        pass

