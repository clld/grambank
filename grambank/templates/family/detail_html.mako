<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! from clld_phylogeny_plugin.tree import Tree %>
<%! from clld_phylogeny_plugin.interfaces import ITree %>
<%! active_menu_item = "languages" %>

<%block name="head">
    ${Tree.head(req)|n}
</%block>

<%block name="title">Family ${ctx.name}</%block>

<%! from sqlalchemy.orm import joinedload %>

<ul class="nav nav-pills" style="float: right">
    <li class="">
        <a href="#varieties">
            <img src="${req.static_url('grambank:static/Map_Icon.png')}"
                 width="35">
            Varieties in grambank
        </a>
    </li>
    <li class="">
        <a href="#values">
            <img src="${req.static_url('grambank:static/Table_Icon.png')}"
                 width="35">
            Feature values
        </a>
    </li>
    % if phylogeny:
        <li class="">
            <a href="#tree-container">
                <img src="${req.static_url('grambank:static/Tree_Icon.png')}"
                     width="35">
                Classification
            </a>
        </li>
    % endif
</ul>

<h2>Family ${ctx.name}</h2>

        <div id="feature-container" class="${'alert alert-info' if feature else 'well well-small'}">
            <p>
                To display the datapoints for a particular feature on the map and on the
                classification tree, select the feature then click "submit".
            </p>
            <form action="${request.route_url('combine_feature_with_family')}"
                  method="get"
                  class="form-inline">
                <input type="hidden" name="family" value="${ctx.id}" />
                <select id="ps" name="feature" class="input-xxlarge">
                    <label for="ps">Feature</label>
                    % for f in features:
                        <option value="${f.id}"${' selected="selected"' if feature and feature.id == f.id else ''}>
                            ${f.id} ${f.name}
                        </option>
                    % endfor
                </select>
                <button class="btn" type="submit">Submit</button>
            </form>
        </div>

<h3 id="varieties">
    Varieties
    % if feature:
        coded for feature ${feature.id}
    % endif
    <a href="#top" title="go to top of the page" style="vertical-align: bottom">&#x21eb;</a>
    <a class="headerlink" href="#varieties" title="Permalink to this headline">¶</a>
</h3>
% if feature:
    ${request.registry.queryUtility(h.interfaces.IMap, name='parameter')(feature, req, family=ctx).render()}
% else:
    ${request.map.render()}
% endif

<div id="values">
    <h3>
        Coded values
        <a href="#top" title="go to top of the page" style="vertical-align: bottom">&#x21eb;</a>
        <a class="headerlink" href="#values" title="Permalink to this headline">¶</a>
    </h3>
    ${request.get_datatable('values', h.models.Value, family=ctx, feature=feature).render()}
</div>

% if phylogeny:
<div id="tree-container">
    <h3>
        Family classification according to Glottolog
        <a href="#top" title="go to top of the page" style="vertical-align: bottom">&#x21eb;</a>
        <a class="headerlink" href="#values" title="Permalink to this headline">¶</a>
    </h3>
    <% tree = req.registry.queryUtility(ITree)(phylogeny, req) %>
    <% tree.pids = [feature.id] if feature else [] %>
    ${tree.render()}
</div>
% endif
