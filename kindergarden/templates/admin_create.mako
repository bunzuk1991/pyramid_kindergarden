<%inherit file="layout.mako"/>

<div class="content">
    <div class="title">${_('Список елекментів')}</div>
    ${h.form(request.route_url(my_model + '_create'), method='post')}
        % if form.errors:
            ${form.errors}
        % endif

        % for field_obj in form:
            <p>
                % if not form.is_hidden(field_obj):
                    ${field_obj.label.text}
                    ${field_obj}
                %endif
            </p>
        % endfor
##
##         % for field in form:
##                 <p>
##     ##                 % if not field.type == 'HiddenField':
##     ##                     <span>${ field.label.text }</span>
##     ##                 % endif
##                     <span>${ field }</span>
##                 </p>
##         % endfor

        <button name="action" value="create" type="submit">
            <span class="button-content">${_('Сторити')}</span>
        </button>
    ${h.end_form()}
</div>