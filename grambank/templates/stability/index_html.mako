<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%inherit file="../home_comp.mako"/>

<h3>Parsimony Stability Rankings</h3>

<p>
<p> Parsimony stability is calculated as follows. First we assuming
the families and subclassifications (trees) of Glottolog. Data from
GramBank is defined for leaves of these trees. All leaf nodes for we
do not have data are ignored and all thusly superflous internal nodes
are left out of consideration. Next, we reconstruct the values at each
internal node such that the total number of changes is minimized (see,
e.g., Felsenstein 2004).  Each branch in the tree now represents a
transition which is either a retention (value stays the same) or an
innovation (value changes). The parsimony stability is the proportion
of retentions and may be taken as a branch-length ignorant upper bound
to "real" (e.g., maximum likelihood) stability. Ties in the parsimony
reconstruction are reflected as fractions in the counts.
</p>

${ctx.render()}
