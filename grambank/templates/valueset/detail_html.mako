<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>


<h2>
    Datapoint ${h.link(request, ctx.language)}/${h.link(request, ctx.parameter)}
    ${h.contactmail(req, ctx, title="suggest changes")}
</h2>

<dl class="dl-horizontal">
    <dt>Language or dialect:</dt>
    <dd>${h.link(req, ctx.language)}</dd>
    <dt>Feature:</dt>
    <dd>${h.link(req, ctx.parameter)}</dd>
    <dt>Coding:</dt>
    <dd>
        ${ctx.values[0].domainelement.description}
        (${h.linked_references(req, ctx)})
    </dd>
    % if ctx.values[0].description:
        <dt>Comment:</dt>
        <dd>${ctx.values[0].description}</dd>
    % endif

<%def name="sidebar()">
<div class="well well-small">
<dl>
    <dt class="contribution">${_('Contribution')}:</dt>
    <dd class="contribution">
        ${h.link(request, ctx.contribution)}
        by
        ${h.linked_contributors(request, ctx.contribution)}
        ${h.button('cite', onclick=h.JSModal.show(ctx.contribution.name, request.resource_url(ctx.contribution, ext='md.html')))}
    </dd>
</dl>
</div>
</%def>
