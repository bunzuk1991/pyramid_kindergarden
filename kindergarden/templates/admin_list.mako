<%inherit file="layout.mako"/>

<div class="content">

    <div class="title">
        <h3>Список ${my_model}</h3>
    </div>

    <div class="home">
        <a href="${request.route_url('admin')}">
            Повернутися до "адміністративної панелі"
        </a>
    </div>

    <div class="table-wrapper">
        ${h.form(request.route_url(my_model + '_crud'), method='get')}
        % if objects:
            <table class="table">
                <tr>
                    <th class="table-header-column"></th>
                    % for field1 in fields:
                        %if field1 == 'id':
                            <th class="table-header-column hidden"></th>
                        % else:
                            <th class="table-header-column"> ${field1}</th>
                        %endif
        ##                 ${field1}
                    % endfor
                </tr>

                % for obj in objects:
                    <tr>
                         <td class="table-row-column">
                            ${h.radio('id', obj.id)}
                         </td>
                         % for field in fields:
                             % if field == 'id':
                                 <td class="table-row-column hidden"></td>
                             % else:
                                 <td class="table-row-column">
                                     ${obj.__getattribute__(field)}
                                 </td>
                             % endif
                         % endfor
                    </tr>
                % endfor
            </table>
        % else:
            ${'Не знайдено жодного елемента.'}
        % endif
        <div class="button-wrapper">
            <button name="action" value="new" type="submit">
                <span class="button-content">${_('Сторити')}</span>
            </button>
            <button name="action" value="edit" type="submit">
                <span class="button-content">${_('Оновити')}</span>
            </button>
            <button name="action" value="delete" type="submit">
                <span class="button-content">${_('Видалити')}</span>
            </button>
        </div>
        ${h.end_form()}
    </div>
</div>