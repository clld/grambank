<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "phylogenys" %>
<%block name="title">Phylogeny ${ctx.name}</%block>
<%! from clld_phylogeny_plugin.tree import Tree %>
<%! from clld_phylogeny_plugin.interfaces import ITree %>
<% tree = req.registry.queryUtility(ITree)(ctx, req) %>

<%block name="head">
    ${Tree.head(req)|n}
    <link href="${request.static_url('clld:web/static/css/select2.css')}"
          rel="stylesheet">
    <script src="${request.static_url('clld:web/static/js/select2.js')}"></script>
</%block>

<div class="row-fluid">
    <div class="span8">
        <h2>${title()}</h2>

        % if ctx.description:
            <div class="alert alert-info">${ctx.description}</div>
        % endif
        % if tree.parameters:
            <div class="alert alert-success">
                The tree has been pruned to only contain leaf nodes with values for
                the selected variables. For the full tree click
                <a href="${req.resource_url(ctx)}">here</a>.
            </div>
        % endif
        <div>
            <form action="${req.resource_url(ctx)}">
                <fieldset>
                    <p>
                        You may combine these ${_('Parameters').lower()} with another
                        one.
                        Start typing the ${_('Parameter').lower()} name or number in
                        the field below.
                    </p>
                    ${ms(request, combination=tree).render()|n}
                    <button class="btn" type="submit">Submit</button>
                </fieldset>
            </form>
        </div>
        ${tree.render()}
    </div>

    <div class="span4">
        <% ca = h.get_adapter(h.interfaces.IRepresentation, ctx, req, ext='description.html') %>
        % if ca:
            <div class="well well-small">
                ${ca.render(ctx, req)|n}
            </div>
        % endif
        % if tree.parameters:
            <div class="accordion" id="values-acc" data-spy="affix" data-offset-top="0"
                 style="margin-right: 10px;">
                % for parameter in tree.parameters:
                    <div class="accordion-group">
                        <div class="accordion-heading">
                            <a class="accordion-toggle" data-toggle="collapse"
                               data-parent="#values-acc" href="#acc-${parameter.id}">
                                ${parameter.name}
                            </a>
                        </div>
                        <div id="acc-${parameter.id}"
                             class="accordion-body collapse${' in' if loop.first else ''}">
                            <div class="accordion-inner">
                                ${h.get_adapter(h.interfaces.IRepresentation, parameter, req, ext='valuetable.html').render(parameter, req)|n}
                            </div>
                        </div>
                    </div>
                % endfor
            </div>
        % endif
    </div>
</div>
