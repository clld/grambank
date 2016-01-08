<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! from grambank.models import Support %>
<%! active_menu_item = "deepfamilys" %>
<%block name="title">Deep Family Suggestion ${ctx.id}</%block>

<h3>Deep Family Suggestion ${ctx.id}</h3>


<p>
The support score for each feature is the difference between historical score (the stability the feature) and the cross-linguistic rarity of the feature value(s) in question (akin to the likelihood that the two languages would share the feature without being historically related).
</p>

<%def name="sidebar()">
                ${lmap.render()}
</%def>
${request.get_datatable('supports', Support, deepfamily=ctx).render()}
