from wtforms import (
    Form,
    StringField,
    TextAreaField,
    SelectField,
    DateField,
    DecimalField,
    IntegerField,
    FileField,
    validators)

from wtforms import IntegerField, PasswordField, FileField
from wtforms.widgets import HiddenInput

from kindergarden.models.bases import Group, session_db


class ChildCreateForm(Form):
    group_choices = [(g.id, g.name) for g in session_db.query(Group).order_by('name').all()]
    group_id = SelectField(u'Group', [validators.InputRequired(message=u'Оберіть групу із списку')],
                           choices=group_choices)
    fullname = StringField(u'Full name', [validators.InputRequired(message=u'Введіть П.І.П дитини'),
                                          validators.Length(min=1, max=255)])
    date_of_birth = DateField(u'Date of birth', [validators.InputRequired(message=u'введіть дату народження')])
    growth = IntegerField(u'Ріст (см.)', [validators.InputRequired(message=u'введіть ріст в сантиметрах'),
                                          validators.NumberRange(min=20, max=260, message=u'Мабуть дитина зависока:)')])
    weight = DecimalField(u'Вага (кг.)', [validators.InputRequired(message=u'введіть ріст в сантиметрах'),
                                          validators.NumberRange(min=5, max=150, message=u'Мабуть дитина заважка:)')],
                          places=2)
    image = FileField(u'Фотокартка дитини')
