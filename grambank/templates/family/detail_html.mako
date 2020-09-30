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

        <div id="feature-container" class="${'alert alert-info' if feature else 'well well-small'}">
            <p>
                To display the datapoints for a particular feature on the map and on the
                classification tree, select the feauture then click "submit".
            </p>
            <form action="${request.route_url('family', id=ctx.id)}"
                  method="get"
                  class="form-inline">
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
