<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "stabilitys" %>
<%! from grambank.models import Transition %>


<h3>Parsimony Stability ${ctx.id} for Feature ${h.link(request, ctx.feature)}</h3>

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

<p>
The set of transitions
define a transition matrix, which, if aperiodic and irreducible,
defines a stationary distribution as per standard Markov theory.
The synchronic distribution is the family-controlled distribution of
values. The stationary distribution and synchronic distributions
should match i) if the feature in question is not so stable that it outlives
the family-depths in Glottolog, ii) the transitions are independent
and sufficiently many to yield reliable estimates, and iii) if typological
features in isolation really obey the Markovian assumptions of Maslova (2000).
</p>

<p>
<blockquote>
Maslova, Elena. (2000) A Dynamic Approach to the Verification of Distributional Universals.  Linguistic Typology 4(3). 307-333.
</blockquote>
</p>
<p>

<table class="table table-condensed">
<thead>
<tr>
            <th>From\To</th>
% for value in sorted(transition_matrix.iterkeys()):
        <th>${value}</th>
% endfor
            <th style="text-align: right;"># Transitions</th>
</tr>
</thead>
% for v1, row in sorted(transition_matrix.iteritems()):
<tr>
            <td>${v1}</td>
% for v2, p in sorted(row.iteritems()):
        <td>${"%.5f" % p}</td>
% endfor
            <td style="text-align: right;">${state_total.get(v1, 0)}</td>
</tr>
% endfor
</table>

</p>

<p>

<table class="table table-condensed">
<thead>
<tr>
            <th></th>
% for value in sorted(transition_matrix.iterkeys()):
        <th>${value}</th>
% endfor
</tr>
</thead>
<tr>
<td>Stationary distribution</td>
% for value in sorted(transition_matrix.iterkeys()):
        <td>${"%.5f" % ctx.jsondata['diachronic_p'].get(value, 0.0)}</td>
% endfor
</tr>
<td>Synchronic distribution</td>
% for value in sorted(transition_matrix.iterkeys()):
        <td>${"%.5f" % ctx.jsondata['synchronic_p'].get(value, 0.0)}</td>
% endfor
</tr>

</table>

</p>

<%def name="sidebar()">

<%util:well>
<table class="table table-condensed">
<thead>
        <tr>
            <th>Value</th>
            <th>Retentions</th>
	    <th>Total</th>
	    <th>Stability</th>
        </tr>
</thead>
% for (value, retentions, total, stability_value) in stability_table:
<tr>
            <td>${value}</td>
            <td style="text-align: right;">${retentions}</td>
            <td style="text-align: right;">${total}</td>
            <td>${stability_value}</td>
</tr>
% endfor
</table>
</%util:well>


</%def>



${request.get_datatable('transitions', Transition, stability=ctx).render()}
