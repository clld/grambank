<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributors" %>
<%block name="title">${_('Contributor')} ${ctx.name}</%block>

<h2>${_('Contributor')} ${ctx.name}</h2>

<p>coded ${'{0:,}'.format(sum(l[1] for l in languages))} datapoints for ${len(languages)} languages</p>

<div style="float: left">
    <%util:table items="${languages}" args="item" class_="table-nonfluid" options="${dict(searching=False)}">
        <%def name="head()">
            <th>Language</th>
            <th>Glottocode</th>
            <th>Family</th>
            <th>Macroarea</th>
            <th>Datapoints</th>
        </%def>
        <td>${h.link(request, item[0])}</td>
        <td>${u.glottolog.link(req, item[0].id, label=item[0].id)}</td>
        <td>${h.link(request, item[0].family)}</td>
        <td>${item[0].macroarea}</td>
        <td class="right">${'{0:,}'.format(item[1])}</td>
    </%util:table>
</div>