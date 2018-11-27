import logging
import traceback

from datetime import date, datetime

from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.renderers import render, render_to_response

strip_filter = lambda x: x.strip() if x else None

from kindergarden.lib import helpers as h
from kindergarden.lib.i18n import ugettext as _
from kindergarden.models.bases import session
from kindergarden.models.meta import Base
from wtforms import validators
from wtforms import widgets
from wtforms import Form as WTF_form
from wtforms import (
    StringField,
    BooleanField,
    DateField,
    DateTimeField,
    RadioField,
    PasswordField,
    FileField,
    TextAreaField,
    IntegerField,
    DecimalField,
    HiddenField,
    SelectFieldBase
)


DBSession = session
APP_NAME = 'kindergarden'

log = logging.getLogger(__name__)


def xhr_form_errors(errors, request=None):
    return render_to_response('json', {'form': {'errors': errors}}, request=request)


def xhr_flash_errors(errors, request=None):
    return render_to_response('json', {'errors': errors}, request=request)


def xhr_flash_messages(messages, request=None):
    return render_to_response('json', {'messages': messages}, request=request)


def xhr_template(name, context, options=None, request=None):
    template = {
        'body': render(name, context, request=request)
    }

    if options:
        template.update(options)

    return render_to_response('json', {'template': template}, request=request, response=request.response)


class GenericView(object):
    model = None
    form = None
    query = None
    ordering = None
    paginate = None
    verbose_name = None
    verbose_name_plural = None
    verbose_name_i18n = verbose_name
    verbose_name_plural_i18n = verbose_name_plural

    def __init__(self, request):
        self.request = request
        self.db = DBSession
        self.context = {}
        self.settings = self.request.registry.settings

    def list(self):
        if not self.query:
            q = self.db.query(self.model)
            if self.ordering:
                q = q.order_by(*self.ordering)
        else:
            q = self.query

        try:
            if self.paginate:
                objects = h.page(q, self.request, items_per_page=self.paginate)
            else:
                objects = q
        except:
            self.request.session.flash(_('Помилка. Неможливо відобразити список.'))
            return HTTPFound(location=self.request.route_url('%s_list' % self.verbose_name))

        self.context.update({'objects': objects})
        return render_to_response('%s:templates/model/%s/list.mako' % (APP_NAME, self.verbose_name), self.context,
                                  request=self.request)

    def crud(self):
        try:
            return getattr(self, self.request.params.get('action'))()
        except AttributeError:
            return HTTPNotFound()

    def new(self):
        form = self.form()
        self.context.update({'form': form})
        return render_to_response('%s:templates/model/%s/create.mako' % (APP_NAME, self.verbose_name), self.context,
                                  request=self.request)

    def create(self):
        form = self.form(self.request.POST)

        try:
            if form.validate():
                obj = self.model()
                if hasattr(form, 'process_obj'):
                    form.process_obj(obj)
                form.populate_obj(obj)
                self.before_create(form, obj)
                self.db.add(obj)
                self.after_create(form, obj)
            else:
                if self.request.is_xhr:
                    return xhr_form_errors(form.errors, self.request)

                self.context.update({'form': form})
                return render_to_response('%s:templates/model/%s/create.mako' % (APP_NAME, self.verbose_name),
                                          self.context, request=self.request)
        except Exception as e:
            flash_msg = _('Помилка. Неможливо створити елемент.') % self.verbose_name_i18n

            if self.request.is_xhr:
                return xhr_flash_errors([flash_msg], self.request)

            self.context.update({'form': form})
            self.request.session.flash(flash_msg)
            return render_to_response('%s:templates/model/%s/create.mako' % (APP_NAME, self.verbose_name), self.context,
                                      request=self.request)

        flash_msg = _('%s успішно створено.') % self.verbose_name_i18n.capitalize()

        if self.request.is_xhr:
            return xhr_flash_messages([flash_msg], self.request)

        self.request.session.flash(flash_msg)
        return HTTPFound(location=self.get_redirect_location(obj))

    def edit(self):
        if 'id' in self.request.matchdict:
            id = self.request.matchdict['id']
        else:
            id = self.request.params.get('id')

        obj = self.db.query(self.model).filter_by(id=id).first()
        if obj:
            form = self.form(obj=obj)
        else:
            self.request.session.flash(_('Помилка. Не вибраний жоден з елементів.'))
            return HTTPFound(location=self.request.route_url('%s_list' % self.verbose_name))

        self.context.update({'form': form, 'id': id})
        return render_to_response('%s:templates/model/%s/update.mako' % (APP_NAME, self.verbose_name), self.context,
                                  request=self.request)

    def update(self):
        id = self.request.matchdict.get('id')

        form = self.form(self.request.POST)
        try:
            if form.validate():
                obj = self.db.query(self.model).filter_by(id=id).first()
                if hasattr(form, 'process_obj'):
                    form.process_obj(obj)
                form.populate_obj(obj)
                self.before_update(form, obj)
                self.db.add(obj)
                self.after_update(form, obj)
            else:
                if self.request.is_xhr:
                    return xhr_form_errors(form.errors, self.request)

                self.context.update({'form': form, 'id': id})
                return render_to_response('%s:templates/model/%s/update.mako' % (APP_NAME, self.verbose_name),
                                          self.context, request=self.request)
        except:
            flash_msg = _('Помилка. Неможливо оновити елемент.')

            if self.request.is_xhr:
                return xhr_flash_errors([flash_msg], self.request)

            self.context.update({'form': form, 'id': id})
            self.request.session.flash(flash_msg)
            return render_to_response('%s:templates/model/%s/update.mako' % (APP_NAME, self.verbose_name), self.context,
                                      request=self.request)

        flash_msg = _('Елемент успішно оновлений.')

        if self.request.is_xhr:
            return xhr_flash_messages([flash_msg], self.request)

        self.request.session.flash(flash_msg)
        return HTTPFound(location=self.get_redirect_location(obj))

    def delete(self):
        if 'id' in self.request.matchdict:
            id = self.request.matchdict['id']
        else:
            id = self.request.params.get('id')

        if not id:
            flash_msg = _('Помилка. Не вибраний жоден з елементів.')

            if self.request.is_xhr:
                return xhr_flash_errors([flash_msg], self.request)

            self.request.session.flash(flash_msg)
            return HTTPFound(location=self.request.route_url('%s_list' % self.verbose_name))

        try:
            self.before_delete()
            obj = self.db.query(self.model).filter_by(id=id).delete()
            self.after_delete()
        except:
            flash_msg = _('Неможливо видалити елемент.')

            if self.request.is_xhr:
                return xhr_flash_errors([flash_msg], self.request)

            self.request.session.flash(flash_msg)
        else:
            flash_msg = _('Елемент успішно видалений.')

            if self.request.is_xhr:
                return xhr_flash_messages([flash_msg], self.request)

            self.request.session.flash(flash_msg)

        return HTTPFound(location=self.get_redirect_location(obj))

    def view(self):
        if 'slug' in self.request.matchdict:
            slug = self.request.matchdict.get('slug')
            obj = self.db.query(self.model).filter_by(slug=slug).first()
        else:
            id = self.request.matchdict.get('id')
            obj = self.db.query(self.model).filter_by(id=id).first()

        if obj:
            self.context.update({'object': obj})
            return render_to_response('%s:templates/model/%s/view.mako' % (APP_NAME, self.verbose_name), self.context,
                                      request=self.request)
        else:
            self.request.session.flash(_('Помилка при перегляді елементу.') % self.verbose_name_i18n)
            return HTTPFound(location=self.get_redirect_location(obj))

    # TODO: maybe add separate get_redirect_location for all crud actions?
    def get_redirect_location(self, obj):
        return self.request.route_url('%s_list' % self.verbose_name)

    def before_create(self, form, obj):
        pass

    def before_update(self, form, obj):
        pass

    def before_delete(self):
        pass

    def after_create(self, form, obj):
        pass

    def after_update(self, form, obj):
        pass

    def after_delete(self):
        pass



def get_class_from_table_name(table_name):
    for base in Base._decl_class_registry.values():
        if hasattr(base, '__table__') and base.__table__.fullname == table_name:
            return base


def construct_colum_for_column_type(type_name,
                                    column_name,
                                    required=False,
                                    column_default = None,
                                    column_min = None,
                                    column_max = None,
                                    widget = None,
                                    filter_ = None,
                                    primary = False,
                                    rel_class = None
                                    ):

    validators_ = []

    if required:
        validators_.append(validators.data_required())
    else:
        validators_.append(validators.optional())

    if not type_name == 'date' and not type_name == 'datetime':
        if column_min or column_max:
            if column_min and column_max:
                lenght_validator = validators.length(min=column_min, max=column_max)
            elif column_min and not column_max:
                lenght_validator = validators.length(min=column_min)
            else:
                lenght_validator = validators.length(max=column_max)
            validators_.append(lenght_validator)
    else:
        if column_min or column_max:
            if column_min and column_max:
                lenght_validator = validators.number_range(min=date(column_min, 1, 1), max=date(column_max, 12, 31))
            elif column_min and not column_max:
                lenght_validator = validators.number_range(min=date(column_min, 1, 1))
            else:
                lenght_validator = validators.number_range(max=date(column_max, 12, 31))

    data = {
        'integer': IntegerField(column_name),
        'unicode_text': StringField(column_name),
        'text': StringField(column_name),
        'string': StringField(column_name),
        'decimal': IntegerField(column_name),
        'boolean': BooleanField(column_name),
        'datetime': DateTimeField(column_name),
        'select': SelectFieldBase(column_name, coerce=int)
    }

    if type_name in data:
        current_column = data[type_name]
        current_column.validators = validators_
        if column_default:
            current_column.default = column_default
        if widget:
            current_column.widget = widget
        if filter_:
            current_column.filters = [filter_]
        if primary:
            current_column.widget = widgets.HiddenInput()
        if rel_class:
            current_column.choices = [(g.id, g.name) for g in rel_class.query.order_by('id')]
    else:
        current_column = None

    return current_column


# generic form
class GenericForm(WTF_form):
    model = None

    def __init__(self, model, fields_exclude = None, default_=None, min_=None, max_=None):
        if model:
            self.model = model
        if self.model:
            for column in self.model.__table__.columns:
                column_name = column.name
                column_nullable = column.nullable
                column_primary_key = column.primary_key
                column_relations = column.foreign_keys
                column_relation_class = None
                column_relation_table_name = None
                current_field_type = column.type.__visit_name__
                column_default = None
                column_min = None
                column_max = None
                column_filter = None

                if column_relations.__len__() > 0:
                    for a in column_relations:
                        col_tokens  = a._column_tokens
                        column_relation_table_name = col_tokens[1]
                        column_relation_class = get_class_from_table_name(column_relation_table_name)

                if column_relation_class:
                    current_field_type = 'select'

                if default_:
                    column_default = default_
                if min:
                    column_min = min_
                if max:
                    column_max = max_

                if current_field_type == 'integer':
                    if not column_default:
                        column_default = 0
                elif current_field_type == 'unicode_text':
                    column_filter = strip_filter
                    if not column_default:
                        column_default = ""
                elif current_field_type == 'string':
                    column_filter = strip_filter
                    if not column_default:
                        column_default = ""
                elif current_field_type == 'text':
                    column_filter = strip_filter
                    if not column_default:
                        column_default = ""
                elif current_field_type == 'boolean':
                    if not column_default:
                        column_default = False
                elif current_field_type == 'datetime':
                    if not column_min and not column_max:
                        column_min = 1900
                elif current_field_type == 'date':
                    if not column_min and not column_max:
                        column_min = 1900
                elif current_field_type == 'decimal':
                    if not column_default:
                        column_default = 0

                self.__setattr__(column_name, construct_colum_for_column_type(
                    current_field_type,
                    column_name,
                    not column_nullable,
                    column_default=column_default,
                    column_max=column_max,
                    column_min=column_min,
                    filter_=column_filter,
                    rel_class=column_relation_class,
                    primary=column_primary_key
                ))


def apply_sorting_query(query, request, config, sort_exp='sort_exp', default_exp=None):
    if not default_exp:
        default_exp = []

    criterion = [config[f]() for f in request.GET.getall(sort_exp) or default_exp if f in config]

    if not criterion:
        return query

    return query.order_by(*criterion)


def apply_filtering_query(query, request, config, filter_exp='filter_exp', filter_val='filter_val'):
    criterion = [config[f](v) for f, v in zip(request.GET.getall(filter_exp), request.GET.getall(filter_val))
                 if f in config]

    if not criterion:
        return query

    return query.filter(*criterion)


def apply_redirect_filtering(request, config, filter_exp='filter_exp', filter_val='filter_val'):
    if request.GET.get(filter_exp) in config:
        return config[request.GET.get(filter_exp)](request.GET.get(filter_val))
