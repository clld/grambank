<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">Feature ${ctx.id}: ${ctx.name}</%block>

<%block name="head">
    <link href="${request.static_url('clld:web/static/css/select2.css')}" rel="stylesheet">
    <script src="${request.static_url('clld:web/static/js/select2.js')}"></script>
</%block>

<ul class="nav nav-pills" style="float: right">
    <li class="">
        <a href="#info-container">
            <img src="${req.static_url('grambank:static/About_Icon.png')}"
                 width="35">
            Description
        </a>
    </li>
    <li class="">
        <a href="#map-container">
            <img src="${req.static_url('grambank:static/Map_Icon.png')}"
                 width="35">
            Map
        </a>
    </li>
    <li class="">
        <a href="#table-container">
            <img src="${req.static_url('grambank:static/Table_Icon.png')}"
                 width="35">
            Values
        </a>
    </li>
</ul>


<h2>Feature ${ctx.id}: ${ctx.name}</h2>
<div>
    ${h.alt_representations(req, ctx, doc_position='right', exclude=['snippet.html'])|n}
    <div class="badge">
        <strong>Patron:</strong> ${h.link(req, ctx.patron)}
    </div>
</div>

<h3 id="info-container">
    Description
    <a href="#top" title="go to top of the page" style="vertical-align: bottom">&#x21eb;</a>
</h3>
${u.process_markdown(ctx.description, req)|n}

<br style="clear: right"/>

<h3 id="map-container">
    Map
    <a href="#top" title="go to top of the page" style="vertical-align: bottom">&#x21eb;</a>
</h3>
${request.map.render()}

<h3 id="table-container">
    Values
    <a href="#top" title="go to top of the page" style="vertical-align: bottom">&#x21eb;</a>
</h3>
${request.get_datatable('values', h.models.Value, parameter=ctx).render()}
