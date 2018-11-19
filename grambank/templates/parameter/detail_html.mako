<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">Feature ${ctx.id}: ${ctx.name}</%block>

<%block name="head">
    <link href="${request.static_url('clld:web/static/css/select2.css')}" rel="stylesheet">
    <script src="${request.static_url('clld:web/static/js/select2.js')}"></script>
</%block>

<div class="span4" style="float: right; margin-top: 1em;">
        <%util:well title="Values">
        <table class="table table-condensed">
            % for de in ctx.domain:
                <tr>
                    <td title="click to select a different map marker" id="iconselect${str(de.number)}"
                        data-toggle="popover" data-placement="left">
                        ${h.map_marker_img(req, de)}
                    </td>
                    <td>${de.name}</td>
                    <td>${de.description}</td>
                    <td class="right">${len(de.values)}</td>
                </tr>
            % endfor
        </table>
    </%util:well>
</div>

<h2>Feature ${ctx.id}: ${ctx.name}</h2>
<div>${h.alt_representations(req, ctx, doc_position='right', exclude=['snippet.html'])|n}</div>


<br style="clear: right"/>

% if request.map:
    ${request.map.render()}
% endif



<div class="tabbable">
    <ul class="nav nav-tabs">
        <li class="active"><a href="#values" data-toggle="tab">Values</a></li>
        <li><a href="#doc" data-toggle="tab">Description</a></li>
    </ul>
    <div class="tab-content" style="overflow: visible;">
        <div id="values" class="tab-pane active">
            ${request.get_datatable('values', h.models.Value, parameter=ctx).render()}
        </div>
        <div id="doc" class="tab-pane">
            ${u.process_markdown(ctx.description, req)|n}
        </div>
    </div>
    <script>
        $(document).ready(function () {
            if (location.hash !== '') {
                $('a[href="#' + location.hash.substr(2) + '"]').tab('show');
            }
            return $('a[data-toggle="tab"]').on('shown', function (e) {
                return location.hash = 't' + $(e.target).attr('href').substr(1);
            });
        });
    </script>
</div>
