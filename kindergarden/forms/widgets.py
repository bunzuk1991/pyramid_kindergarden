from wtforms.widgets.core import Select, HTMLString, html_params
from wtforms.fields.core import DateField
from wtforms.validators import StopValidation
from datetime import date

MONTH_CHOICES = [
    (1, u'Січень'),
    (2, u'Лютий'),
    (3, u'Березень'),
    (4, u'Квітень'),
    (5, u'Травень'),
    (6, u'Червень'),
    (7, u'Липень'),
    (8, u'Серпень'),
    (9, u'Вересень'),
    (10, u'Жовтень'),
    (11, u'Листопад'),
    (12, u'Грудень'),
]


class SelectDateWidget(object):
    FORMAT_CHOICES = {
        '%d': [(x, str(x)) for x in range(1, 32)],
        '%m': MONTH_CHOICES,
    }

    FORMAT_CLASSES = {
        '%d': 'select_date_day',
        '%m': 'select_date_month',
        '%Y': 'select_date_year'
    }

    def __init__(self, year_in=2000, year_out=0):
        if year_in and year_out:
            years = [(x, str(x)) for x in range(year_in, year_out+1)]
        else:
            years = [(x, str(x)) for x in range(year_in, date.today().year + 1)]

        super(SelectDateWidget, self).__init__()
        self.FORMAT_CHOICES['%Y'] = years

    def __call__(self, field, **kwargs):
        field_id = kwargs.pop('id', field.id)
        html = []
        allowed_format = ['%d', '%m', '%Y']
        split_symbol = field.format[2] if field.format[2] else ' '

        for field_format in field.format.split(split_symbol):
            if field_format in allowed_format:
                choices = self.FORMAT_CHOICES[field_format]
                id_suffix = field_format.replace('%', '-')
                id_current = field_id + id_suffix

                kwargs['class'] = self.FORMAT_CLASSES[field_format]
                try:
                    del kwargs['placeholder']
                except:
                    pass

                html.append('<select %s>' % html_params(name=field.name, id=id_current, **kwargs))

                if field.data:
                    current_value = int(field.data.strftime(field_format))
                else:
                    current_value = None

                for value, label in choices:
                    selected = (value == current_value)
                    html.append(Select.render_option(value, label, selected))
                html.append('</select>')
            else:
                html.append(field_format)
                html.append('<input type="hidden" value="' + field_format + '" %s></input>' % html_params(name=field.name,
                                                                                                    id=id_current,
                                                                                                    **kwargs))

            html.append(' ')

        return HTMLString(''.join(html))


class SelectFieldDate(DateField):
    widget = SelectDateWidget()

    def __init__(self, label=None, validators=None, format='%Y-%m-%d', **kwargs):
        super(SelectFieldDate, self).__init__(label, validators, format, **kwargs)

    def pre_validate(self, form):
        format_string = self.format
        field_data = form[self.id].data

        if field_data:
            self.data = field_data
        else:
            raise StopValidation(message=u'invalid date')



