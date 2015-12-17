<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%block name="title">Dependency ${ctx.id}</%block>

<h2>Dependency ${ctx.id}</h2>

Hello