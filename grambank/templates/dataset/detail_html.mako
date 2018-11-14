<%inherit file="../home_comp.mako"/>
<%namespace name="util" file="../util.mako"/>
<%
    coded_by = {}
    for names, count in contribs:
        ns = names.split(" and ")
        for name in ns:
	    coded_by[name] = coded_by.get(name, 0) + count/len(ns)
%>

<%def name="sidebar()">
    <img src="${request.static_url('grambank:static/glottobank_all.jpg')}"/>
    <div class="well">
        <h3>grambank</h3>
        <p>
            produced by a team directed by Russell Gray and Quentin
            Atkinson. The original questionnaire was designed by Ger Reesink and
            Michael Dunn, subsequent extensions and clarifications were done by
            Hedvig Skirg&aring;rd, Suzanne van der Meer, Harald Hammarstr&ouml;m,
            Stephen Levinson, Hannah Haynie, Jeremy Collins, Alena Witzlack, Jakob Lesage
            and Nicholas Evans.</p>

    </div>

</%def>

<h2>Welcome to Grambank</h2>

<p class="lead">
    Grambank is a database of structural (typological) features of language. It consists
    of 195 logically independent features (most of them binary) spanning all subdomains of
    morphosyntax. The Grambank feature questionnaire has been filled in, based on
    reference grammars, for over 1,000 languages. The aim is to eventually reach as many
    as 3,500 languages. The database can be used to investigate deep language prehistory,
    the geographical-distribution of features, language universals and the functional
    interaction of structural features.
</p>

<table class="table table-condensed table-nonfluid">
    <thead>
    <tr>
        <th colspan="3">Statistics</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <th>Languages</th>
        <td></td>
        <td class="right">${'{:,}'.format(stats['language'])}</td>
    </tr>
    <tr>
        <th>Features</th>
        <td></td>
        <td class="right">${'{:,}'.format(stats['parameter'])}</td>
    </tr>
    <tr>
        <th>Datapoints</th>
        <th>total</th>
        <td class="right">${'{:,}'.format(stats['value'])}</td>
    </tr>
    </tbody>
</table>


<h3>How to cite Grambank Online</h3>
<p>
    Grambank is not yet publically available and should not for the time being be cited.
    If you nevertheless think you need to cite it contact Harald Hammarstr&ouml;m. The
    eventual citation will contain the names of alll people who contributed to Grambank.
</p>
<p>
    Grambank is a publication of the
    ${h.external_link('http://http://www.shh.mpg.de', label='Linguistic and Cultural Evolution Group')}
    at the Max Planck Institute for the Science of Human History, Jena. The datapoints
    furnished by Claire Bowern and Patience Epps was supported by National Science
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
