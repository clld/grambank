<%inherit file="app.mako"/>

<%block name="brand">
    <a href="${request.resource_url(request.dataset)}" class="brand">GramBank</a>
</%block>

${next.body()}
