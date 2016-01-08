<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%inherit file="../home_comp.mako"/>

<h3>Deep Family Suggestions</h3>

<p>
Deep family suggestions are computed as follows. The proto-language of
each family is parsimony reconstructed and the location of the
proto-language is computed recursively as the mean of its daughter
locations. Each pair of proto-languages is compared where a match
yields a score between 0.0 and 1.0 for each feature. The total score
(support value) is the average score for all features for which both
proto-languages have values defined. Its significance is the proportion
of actually related languages which have a lower support value.
The distance is the distance as the crow flies between the estimated
location of the proto-languages. This method of finding suggestions
for proto-languages is not probabilistically kosher, not controlled
for functional dependencies between features and not controlled for
multiple testing, so it should be interpreted with care.
</p>

${ctx.render()}
