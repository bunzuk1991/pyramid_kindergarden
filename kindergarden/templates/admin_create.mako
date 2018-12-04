<%inherit file="layout.mako"/>

<div class="content">
    <div class="title">
        <h3>Створення елемента ${my_model}</h3>
    </div>

    <div class="form-wrapper">
        ${h.form(request.route_url(my_model + '_create'), method='post')}
            % if form.errors:
                ${form.errors}
            % endif

            % for field_obj in form:
                <div class="input-wrapper">
                    % if not form.is_hidden(field_obj):
                            %if field_obj.type == 'DateField':
                                <span>${field_obj.label.text}</span>
                                ${field_obj(class_="datepicker-date")}
                            %elif field_obj.type == 'DateTimeField':
                                <span>${field_obj.label.text}</span>
                                ${field_obj(class_="datepicker-datetime")}
                            %elif field_obj.type == 'BooleanField':
                                <div class="check-in-out">
                                   <span>${field_obj.label.text}</span>
                                   ${field_obj(class_="check-box-in-out")}
                                   <label class="switch" for="${field_obj.label.field_id}"></label>
                                </div>
                            %else:
                                <span>${field_obj.label.text}</span>
                                ${field_obj}
                            %endif
##
##                          <div class="check-in-out">
##                                         <input class="check-box-in-out" id="label1" type="checkbox">
##                                         <label class="switch" for="label1"></label>
##                                      </div>
                    %endif
                </div>
            % endfor

            <button name="action" value="create" type="submit">
                <span class="button-content">${_('Сторити')}</span>
            </button>
        ${h.end_form()}
    </div>
</div>