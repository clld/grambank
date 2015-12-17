<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Language')} ${ctx.name}</%block>

<ul class="breadcrumb">
<li>Family: ${ctx.family} <span class="divider">/</span></li>
</ul>

<h2>${_('Language')} ${ctx.name}</h2>

${request.get_datatable('values', h.models.Value, language=ctx).render()}

<%def name="sidebar()">
    ${util.codes()}
<div style="clear: right;"> </div>
<%util:well>
${request.map.render()}
${h.format_coordinates(ctx)}
</%util:well>
    % if ctx.sources:
<%util:well title="Sources">
${util.sources_list(sorted(list(ctx.sources), key=lambda s: s.name))}
<div style="clear: both;"></div>
</%util:well>
    % endif
</%def>