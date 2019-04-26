from wtforms import (
    Form,
    StringField,
    TextAreaField,
    SelectField,
    DecimalField,
    IntegerField,
    FileField,
    DateField,
    FormField,
    FieldList,
    validators)

# from wtforms.fields.html5 import DateField

from wtforms import PasswordField, FileField
from wtforms.widgets import HiddenInput, Select, TextInput
from .widgets import SelectFieldDate
from kindergarden.services.utils import upload_file

from kindergarden.models.bases import Group, Relation, session_db

RENDER_KW = {
    'all_fields': {'class': 'input-wrp'},
    'text-area-non-resize': {'class': 'input-wrp non-resize-text-area'},
    'text-area-disabled': {'class': 'input-wrp disabled-text-area'},
    'date-picker': {'class': 'input-wrp cl-date-picker'},
    'readonly': {'readonly': True},
    'text-area-no-cols': {'readonly': True, 'cols': None, 'rows': None}

}


class FieldListMixin(FieldList):
    def populate_obj(self, obj, name):
        # while len(getattr(obj, name)) < len(self.entries):
        #     newModel = self.model()
        #     session_db.add(newModel)
        #     getattr(obj, name).append(newModel)
        entries_list = {x.data['id']: x for x in self.entries}

        for parent in getattr(obj, name):
            if parent.id not in entries_list:
                getattr(obj, name).remove(parent)
        super(FieldListMixin, self).populate_obj(obj, name)

        #
        #
        # while getattr(obj, name).count() > len(self.entries):
        #     session_db.delete(getattr(obj, name).remove())
        # super(FieldListMixin, self).populate_obj(obj, name)


class ParentForm(Form):
    relation_choices = [(g.id, g.name) for g in session_db.query(Relation).order_by('name')]

    id = IntegerField(u'id', [validators.InputRequired()], render_kw=RENDER_KW['readonly'], widget=HiddenInput())
    child_id = IntegerField(u'child_id', [validators.InputRequired()], render_kw=RENDER_KW['readonly'],
                            widget=HiddenInput())
    relation_id = SelectField(u'Relation', [validators.InputRequired()], render_kw=RENDER_KW['readonly'],
                              choices=relation_choices, coerce=int)
    fullname = StringField(u'Full name', [validators.InputRequired(message=u'Введіть П.І.П'),
                                          validators.Length(min=1, max=255)], render_kw=RENDER_KW['readonly'])
    date_of_birth = DateField(u'Дата народження', [validators.InputRequired()], render_kw=RENDER_KW['readonly'])
    phone = StringField(u'Full name', [validators.InputRequired(message=u'Введіть мобільний телефон'),
                                       validators.Length(min=1, max=15)], render_kw=RENDER_KW['readonly'])
    address = TextAreaField(u'Адреса проживання', [validators.Length(min=1, max=255), validators.Optional()],
                            render_kw=RENDER_KW['text-area-no-cols'])
    work = TextAreaField(u'Місце проживання', [validators.Optional(),
                                               validators.Length(min=1, max=255)],
                         render_kw=RENDER_KW['readonly'])
    workplace = StringField(u'Посада', [validators.Optional(),
                                        validators.Length(min=1, max=255)],
                            render_kw=RENDER_KW['readonly'])

    def validate(self):
        return True


class ChildCreateForm(Form):
    __do_not_populate__ = ['image']

    group_choices = [(g.id, g.name) for g in session_db.query(Group).order_by('name').all()]

    group_id = SelectField(u'Group', [validators.InputRequired(message=u'Оберіть групу із списку')],
                           render_kw=RENDER_KW['all_fields'], coerce=int)
    fullname = StringField(u'Full name', [validators.InputRequired(message=u'Введіть П.І.П дитини'),
                                          validators.Length(min=1, max=255)], render_kw=RENDER_KW['all_fields'])
    date_of_birth = SelectFieldDate(u'Date of birth', format='%d %m %Y')

    growth = IntegerField(u'Ріст (см.)', [validators.InputRequired(message=u'введіть ріст в сантиметрах'),
                                          validators.NumberRange(min=20, max=260, message=u'Мабуть дитина зависока:)')],
                          render_kw=RENDER_KW['all_fields'])
    weight = DecimalField(u'Вага (кг.)', [validators.InputRequired(message=u'введіть ріст в сантиметрах'),
                                          validators.NumberRange(min=5, max=150, message=u'Мабуть дитина заважка:)')],
                          places=2, render_kw=RENDER_KW['all_fields'])
    image = FileField(u'Фотокартка дитини', [validators.Optional()], render_kw={'id': 'id_child-image'})
    date_start = DateField(u'Початок навчання', [validators.InputRequired()], render_kw=RENDER_KW['date-picker'])
    date_end = DateField(u'Закінчення навчання', [validators.Optional()], render_kw=RENDER_KW['date-picker'])
    address = TextAreaField(u'Адреса проживання', [validators.InputRequired(message=u'Введіть П.І.П дитини'),
                                                   validators.Length(min=1, max=255)],
                            render_kw=RENDER_KW['text-area-non-resize'])
    slug = StringField(widget=HiddenInput())

    parents = FieldListMixin(FormField(ParentForm), min_entries=0)

    def populate_obj(self, obj):
        for name, field in self._fields.items():
            if name not in self.__do_not_populate__:
                field.populate_obj(obj, name)
