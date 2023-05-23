<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<% from clld.web.icon import Icon %>

<%block name="title">F-Dependency ${'&#8594;'.join(p.id for p in ctx.parameters)|n}</%block>
<%block name="head">
    ${util.head_coloris()|n}
</%block>

<h3>${_('F-Dependency')} ${' &#8594; '.join(h.link(request, p) for p in ctx.parameters)|n}</h3>



% if request.map:
    ${request.map.render()}
% endif

<%def name="combination_valuetable(ctx, iconselect=False)">
    <%util:table items="${enumerate(ctx.domain)}" args="item" eid="refs" class_="table-condensed table-striped table-nonfluid" options="${dict(aaSorting=[[2, 'asc']], bFilter=False)}">
        <%def name="head()">
            <th></th>
            <th></th>
            <th>${' / '.join(h.link(request, p) for p in ctx.parameters)|n}</th>
            <th>Number of languages</th>
        </%def>
        <td>
            % if item[1].languages:
                <button title="click to toggle display of languages for value ${item[1].name}"
                        type="button" class="btn btn-mini expand-collapse"
                        data-toggle="collapse" data-target="#de-${item[0]}">
                    <i class="icon icon-plus"> </i>
                </button>
            % endif
        </td>
        <td>
            % if item[1].languages:
            ${util.coloris_icon_picker(Icon.from_req(item[1], req))|n}
            ${util.parameter_map_reloader([Icon.from_req(de, req) for de in ctx.domain])|n}
            % endif
        </td>
        <td>
            ${item[1].name}
            <div id="de-${item[0]}" class="collapse">
                <table class="table table-condensed table-nonfluid">
                    <tbody>
                        % for language in item[1].languages:
                            <tr>
                                <td>${h.link_to_map(language)}</td>
                                <td>${h.link(request, language)}</td>
                            </tr>
                        % endfor
                    </tbody>
                </table>
            </div>
        </td>
        <td style="text-align: right;">${str(len(item[1].languages))}</td>
    </%util:table>
    % if iconselect:
        <script>
            $(document).ready(function () {
                $('.expand-collapse').click(function () {
                    $(this).children('i').toggleClass('icon-minus icon-plus');
                });
            });
        </script>
    % endif
</%def>


% if ctx.domain:
    <div id="list-container">
        ${combination_valuetable(ctx, iconselect=iconselect or False)}
    </div>
% endif
