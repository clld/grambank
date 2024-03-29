<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<% from grambank import models %>

<%! active_menu_item = "parameters" %>
<%block name="title">Feature ${ctx.id}: ${ctx.name}</%block>

<%! import sqlalchemy %>

<%block name="head">
    <link href="${request.static_url('clld:web/static/css/select2.css')}" rel="stylesheet">
    <script src="${request.static_url('clld:web/static/js/select2.js')}"></script>
    ${util.head_coloris()|n}
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
    <div class="span1">
        ${h.alt_representations(req, ctx, doc_position='right', exclude=['snippet.html'])|n}
    </div>
    <div class="span9">
        <strong>Patrons:</strong>
        % for i, patron in enumerate(ctx.patrons):
            % if i:
                 and
            % endif
            ${h.link(req, patron)}
        % endfor
    </div>
</div>

<h3 id="info-container">
    Description
    <a href="#top" title="go to top of the page" style="vertical-align: bottom">&#x21eb;</a>
</h3>
${u.process_markdown(ctx.description, req)|n}

<br style="clear: right"/>

<div class="well well-small">
    <p>
        To display the datapoints for a particular language family on the map
        and on the classification tree, select the family then click "submit".
    </p>
    <form action="${request.route_url('combine_feature_with_family')}"
          method="get"
          class="form-inline">
        <input type="hidden" name="feature" value="${ctx.id}" />
        <select id="fs" name="family">
            <label for="fs">Family</label>
            ## XXX: This can probably be expressed in SQLAlchemy dot-notation.
            <%! query = sqlalchemy.text('''
                SELECT DISTINCT family.id, family.name
                FROM value
                JOIN valueset ON valueset.pk = value.valueset_pk
                JOIN grambanklanguage ON grambanklanguage.pk = valueset.language_pk
                JOIN family ON family.pk = grambanklanguage.family_pk
                WHERE valueset.parameter_pk = :param_pk
                ORDER BY family.name;''')
            %>
            % for family_id, family_name in request.db.execute(query, {'param_pk': ctx.pk}):
              <option value="${family_id}">${family_name}</option>
            % endfor
        </select>
        <button class="btn" type="submit">Submit</button>
    </form>
</div>

<div class="well well-small">
    <p>
        You may combine this variable with a different variable by selecting on in the list below
        and clicking "Submit".
    </p>
    <form action="${request.route_url('select_combination')}"
          method="get"
          class="form-inline">
        <input type="hidden" name="parameters" value="${ctx.id}"/>
        <select id="pa" name="parameters">
            <label for="pa">Variable</label>
            % for param in request.db.query(models.Parameter).filter(models.Parameter.pk != ctx.pk):
                <option value="${param.id}">${param.id} ${param.name}</option>
            % endfor
        </select>
        <button class="btn" type="submit">Submit</button>
    </form>
</div>


<div class="alert alert-info" style="float: right">
    <button type="button" class="close" data-dismiss="alert">&times;</button>
    Customize map markers:
    <table class="table table-condensed">
        <tbody>
        % for de in ctx.domain:
        <tr>
            <td>${util.coloris_icon_picker(u.icon_from_req(de, req))|n}</td>
            <td>${de.name}</td>
            <td>${de.description}</td>
            <td class="right">${len(de.values)}</td>
        </tr>
        % endfor
        </tbody>
    </table>
    ${util.parameter_map_reloader([u.icon_from_req(de, req) for de in ctx.domain])}
</div>

<h3 id="map-container">
    Map
    <a href="#top" title="go to top of the page" style="vertical-align: bottom">&#x21eb;</a>
</h3>

<br style="clear: both">

${request.map.render()}

<h3 id="table-container">
    Values
    <a href="#top" title="go to top of the page" style="vertical-align: bottom">&#x21eb;</a>
</h3>
${request.get_datatable('values', h.models.Value, parameter=ctx).render()}
