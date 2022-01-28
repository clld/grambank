<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributors" %>
<%block name="title">${_('Contributor')} ${ctx.name}</%block>

<h2>${_('Contributor')} ${ctx.name}</h2>

<p>coded ${sum([i[1] for i in languages])} datapoints for ${len(languages)} languages</p>

<div style="float: left">
    <%util:table items="${languages}" args="item" class_="table-nonfluid" options="${dict(searching=False)}">
        <%def name="head()">
            <th>Datapoints</th>
            <th>Language</th>
            <th>Glottocode</th>
            <th>Family</th>
            <th>Macroarea</th>
        </%def>
            <td class="align-right right">${item[1]}</td>
            <td>${h.link(request, item[0])}</td>
        <td>${u.glottolog.link(req, item[0].id, label=item[0].id)}</td>
        <td>
            % if item[0].family:
                ${h.link(request, item[0].family)}
            % else:
                isolate
            % endif
        </td>
        <td>${item[0].macroarea}</td>
    </%util:table>
</div>