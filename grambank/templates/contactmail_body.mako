% if isinstance(ctx, h.models.ValueSet):
The coding of ${ctx.language.name} [${ctx.language.id}] for feature ${ctx.parameter.id} (${ctx.parameter.name})
should be changed from
"${ctx.values[0].domainelement.description}"
to
... (${' or '.join(['"{}"'.format(de.description) for de in ctx.parameter.domain if de != ctx.values[0].domainelement])|n})
because
...
as stated in
... [source]

I have read the feature description at ${req.route_url('parameter', id=ctx.parameter.id)}.
My expertise in regards to this language or dialect is
...
% endif
