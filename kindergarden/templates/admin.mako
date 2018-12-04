<%inherit file="layout.mako"/>

<div class="content">
    <div class="title">
        <h3>${_('Панель адміністратора')}</h3>
    </div>

##     <a href="${request.route_url('organisation_list')}">${_('Організації')}</a><br/>
##     <a href="${request.route_url('group_list')}">${_('Групи')}</a><br/>
##     <a href="${request.route_url('gardengroup_list')}">${_('Групи по роках')}</a><br/>

    <div class="urls">
        % for site in sites:
            <div class="div-url">
               <a href="${request.route_url(site)}">${_(site)}</a><br/>
            </div>
        % endfor
    </div>


</div>
