


<div class="title">${_('Список елекментів')}</div>
${h.form(request.route_url('${o.id}' + '_crud'), method='get')}
    % if objects:
        % for obj in objects:
                <p>
                    ${h.radio('id', obj.id)}
                    % for field in fields:
                        ${obj[field]}
                    % endfor
                </p>
        % endfor
    % else:
        ${_('Не знайдено жодного елемента.')}
    % endif
    <button name="action" value="new" type="submit">
        <span class="button-content">${_('Сторити')}</span>
    </button>
    <button name="action" value="edit" type="submit">
        <span class="button-content">${_('Оновити')}</span>
    </button>
    <button name="action" value="delete" type="submit">
        <span class="button-content">${_('Видалити')}</span>
    </button>
${h.end_form()}
