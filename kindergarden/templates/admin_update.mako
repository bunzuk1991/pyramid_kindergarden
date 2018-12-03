<%inherit file="layout.mako"/>

<div class="content">
    <div class="title">${_('Список елекментів')}</div>
    ${h.form(request.route_url(my_model + '_update', id=id), method='post')}
        % if form.errors:
            ${form.errors}
        % endif

        % for field_obj in form:
            <p>
                % if not form.is_hidden(field_obj):
                    ${field_obj.label.text}
                    ${field_obj}
                % else:
                    ${field_obj}
                %endif
            </p>
        % endfor

        <button name="action" value="update" type="submit">
            <span class="button-content">${_('Записати')}</span>
        </button>
    ${h.end_form()}
</div>