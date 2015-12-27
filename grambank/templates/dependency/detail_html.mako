<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "dependencys" %>
<%block name="title">Dependency ${ctx.id}</%block>

<h2>Dependency ${ctx.id}: ${ctx.strength}</h2>

<div id="list-container">

    <%util:table items="" args="item" eid="refs" class_="table-condensed table-striped table-nonfluid" options="${dict(aaSorting=[[2, 'desc']])}">\
        <%def name="head()">
            <th>${h.link(request, ctx.feature1)}</th>
	    <th>${h.link(request, ctx.feature2)}</th>
            <th>Number of languages</th>
        </%def>
        <td style="text-align: right;">12</td>
	<td style="text-align: right;">13</td>
	<td style="text-align: right;">14</td>
    </%util:table>

</div>

<%def name="sidebar()">
    HELLO
<div style="clear: right;"> </div>
</%def>