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
from wtforms.fields.html5 import TelField

from kindergarden.models.bases import Group, session_db

RENDER_KW = {
    'all_fields': {'class': 'input-wrp'},
    'text-area-non-resize': {'class': 'input-wrp non-resize-text-area'},
    'text-area-disabled': {'class': 'input-wrp disabled-text-area'},
    'date-picker': {'class': 'input-wrp cl-date-picker'},
    'readonly': {'readonly': True},
    'text-area-no-cols': {'readonly': True, 'cols': None, 'rows': None}

}


class ParentForm(Form):
    relation_id = SelectField(u'Relation', [validators.InputRequired()], render_kw=RENDER_KW['readonly'], coerce=int)
    fullname = StringField(u'Full name', [validators.InputRequired(message=u'Введіть П.І.П'),
                                          validators.Length(min=1, max=255)], render_kw=RENDER_KW['readonly'])
    date_of_birth = DateField(u'Дата народження', [validators.InputRequired()], render_kw=RENDER_KW['readonly'])
    phone = StringField(u'Full name', [validators.InputRequired(message=u'Введіть мобільний телефон'),
                                          validators.Length(min=1, max=15), validators], render_kw=RENDER_KW['readonly'])
    address = TextAreaField(u'Адреса проживання', [validators.Length(min=1, max=255), validators.Optional()],
                            render_kw=RENDER_KW['text-area-no-cols'])
    work = TextAreaField(u'Місце проживання', [validators.InputRequired(message=u'Введіть місце роботи'),
                                                   validators.Length(min=1, max=255)],
                            render_kw=RENDER_KW['readonly'])
    workplace = TextAreaField(u'Посада', [validators.InputRequired(message=u'Введіть посаду'),
                                                validators.Length(min=1, max=255)],
                         render_kw=RENDER_KW['readonly'])


class ChildCreateForm(Form):
    group_choices = [(g.id, g.name) for g in session_db.query(Group).order_by('name').all()]

    group_id = SelectField(u'Group', [validators.InputRequired(message=u'Оберіть групу із списку')], render_kw=RENDER_KW['all_fields'], coerce=int)
    fullname = StringField(u'Full name', [validators.InputRequired(message=u'Введіть П.І.П дитини'),
                                          validators.Length(min=1, max=255)], render_kw=RENDER_KW['all_fields'])
    date_of_birth = SelectFieldDate(u'Date of birth', format='%d %m %Y')

    growth = IntegerField(u'Ріст (см.)', [validators.InputRequired(message=u'введіть ріст в сантиметрах'),
                                          validators.NumberRange(min=20, max=260, message=u'Мабуть дитина зависока:)')],
                          render_kw=RENDER_KW['all_fields'])
    weight = DecimalField(u'Вага (кг.)', [validators.InputRequired(message=u'введіть ріст в сантиметрах'),
                                          validators.NumberRange(min=5, max=150, message=u'Мабуть дитина заважка:)')],
                          places=2, render_kw=RENDER_KW['all_fields'])
    image = FileField(u'Фотокартка дитини', render_kw={'id': 'id_child-image'})
    date_start = DateField(u'Початок навчання', [validators.InputRequired()], render_kw=RENDER_KW['date-picker'])
    date_end = DateField(u'Закінчення навчання', [validators.Optional()], render_kw=RENDER_KW['date-picker'])
    address = TextAreaField(u'Адреса проживання', [validators.InputRequired(message=u'Введіть П.І.П дитини'),
                                                   validators.Length(min=1, max=255)],
                            render_kw=RENDER_KW['text-area-non-resize'])
    slug = StringField(widget=HiddenInput())

    parents = FieldList(FormField(ParentForm), min_entries=0)


