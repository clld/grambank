<%inherit file="home_comp.mako"/>

<h3>Parsimony Stability Rankings</h3>

${request.get_datatable('parameters', h.models.Parameter, stability=True).render()}


