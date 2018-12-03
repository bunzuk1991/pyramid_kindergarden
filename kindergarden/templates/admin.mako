<%inherit file="layout.mako"/>

<div class="content">
    <div name="title">${_('Адміністрування')}</div>

    <div class="title">${_('Панель адміністратора')}</div>

##     <a href="${request.route_url('organisation_list')}">${_('Організації')}</a><br/>
##     <a href="${request.route_url('group_list')}">${_('Групи')}</a><br/>
##     <a href="${request.route_url('gardengroup_list')}">${_('Групи по роках')}</a><br/>


    % for site in sites:
        <p>
           <a href="${request.route_url(site)}">${_(site)}</a><br/>
        </p>
    % endfor

</div>
