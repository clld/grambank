<%inherit file="../home_comp.mako"/>
<%namespace name="util" file="../util.mako"/>
<% TxtCitation = h.get_adapter(h.interfaces.IRepresentation, ctx, request, ext='md.txt') %>


<%def name="sidebar()">
    <img src="${request.static_url('grambank:static/glottobank_all.jpg')}"/>
    <div class="well well-small">
        <h3>Statistics</h3>
        <table class="table table-condensed">
            <tbody>
            <tr>
                <th>Languages</th>
                <td class="right">${'{:,}'.format(stats['language'])}</td>
            </tr>
            <tr>
                <th>Features</th>
                <td class="right">${'{:,}'.format(stats['parameter'])}</td>
            </tr>
            <tr>
                <th>Datapoints</th>
                <td class="right">${'{:,}'.format(stats['value'])} (${'{:,}'.format(nzvalues)} excl. "not known")</td>
            </tr>
            </tbody>
        </table>
    </div>
</%def>

<h2>Welcome to Grambank</h2>

<p class="lead">
    Grambank is a database of structural (typological) features of language. It consists
    of
    <a href="${req.route_url('parameters')}">${stats['parameter']} logically independent features</a>
    (most of them binary) spanning all subdomains of
    morphosyntax. The Grambank feature questionnaire has been filled in, based on
    reference grammars, for
    <a href="${req.route_url('languages')}">${'{:,}'.format(stats['language'])} languages</a>. The aim is to eventually
    reach as many
    as 3,500 languages. The database can be used to investigate deep language prehistory,
    the geographical-distribution of features, language universals and the functional
    interaction of structural features.
</p>


<h3>How to cite Grambank Online</h3>
<p>
    Grambank is not yet publicly available and should not for the time being be cited.
    If you nevertheless think you need to cite it <a href="${req.route_url('contact')}">contact us</a>. The
    eventual citation will contain the names of
    <a href="${req.route_url('contributors')}">all people who contributed to Grambank</a>.
</p>

<blockquote>
    ${h.newline2br(TxtCitation.render(ctx, request))|n}<br>
</blockquote>

<p>
    Grambank is a publication of the
    ${h.external_link('https://www.eva.mpg.de/linguistic-and-cultural-evolution/index/', label='Department of Linguistic and Cultural Evolution')}
    at the Max Planck Institute for Evolutionary Anthropology, Leipzig. The data
    furnished by the Hunter-Gatherer Language Database was supported by National Science
    Foundation grant HSD-0902114 'Dynamics of Hunter Gatherer Language Change' PIs Claire
    Bowern, Patience Epps, Jane Hill, and Keith Hunley.
</p>


<h3>Terms of use</h3>
<p>
    (Will be in effect once publically available:) The content of this web site is
    published under a Creative Commons Licence.
    We invite the community of users to think about further applications for the available
    data and look forward to your comments, feedback and questions.
</p>

<h3>Contributing</h3>
<p>
    For more information about the coding process and definition of features, see
    ${h.external_link('https://github.com/grambank/grambank/wiki', label='our wiki')}. Want to contribute changes or additions? ${h.external_link('https://github.com/grambank/grambank/wiki/Contribute', label='Go here')}.
</p>
