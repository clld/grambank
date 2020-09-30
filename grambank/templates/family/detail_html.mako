<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">Family ${ctx.name}</%block>

<%! from sqlalchemy.orm import joinedload %>

<ul class="nav nav-pills pull-right">
    <li><a href="#varieties">Varieties in grambank</a></li>
    <li><a href="#values">Feature values</a></li>
</ul>

<h2>Family ${ctx.name}</h2>

<h3 id="varieties">
    ${len(ctx.languages)} varieties
    <a href="#top" title="go to top of the page" style="vertical-align: bottom">&#x21eb;</a>
    <a class="headerlink" href="#varieties" title="Permalink to this headline">¶</a>
</h3>
${request.map.render()}

<div id="values">
    <h3>
        Coded values
        <a href="#top" title="go to top of the page" style="vertical-align: bottom">&#x21eb;</a>
        <a class="headerlink" href="#values" title="Permalink to this headline">¶</a>
    </h3>
    ${request.get_datatable('values', h.models.Value, family=ctx).render()}
</div>
