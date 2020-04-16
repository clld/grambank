<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">F-Dependency ${'&#8594;'.join(p.id for p in ctx.parameters)|n}</%block>

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
                % if iconselect:
                    <%self:iconselect id="iconselect${str(item[0])}" param="v${str(item[0])}" placement="right" tag="span">
                        <img height="20" width="20" src="${item[1].icon.url(request)}"/>
                    </%self:iconselect>
                % else:
                    <img height="20" width="20" src="${item[1].icon.url(request)}"/>
                % endif
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
