<%inherit file="../home_comp.mako"/>
<%namespace name="util" file="../util.mako"/>

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
        % for name, count in contribs:
            <tr>
                <td></td>
                <td>${name}</td>
                <td class="right">${'{:,}'.format(count)}</td>
            </tr>
        % endfor
    </tbody>
</table>

<h3>For Coders</h3>

<ul>
    <li>Example sheets:
        <ul>
            <li>Empty GB coder sheet, i.e., the most recent version of Grambank sheet with
                feature categories and standardised comments:
                <a href="https://github.com/glottobank/Grambank/blob/master/For_coders/GramBank_most_updated_sheet.xlsx"><b>.xlsx</b></a>
                (requires github login, click the download-button to download it).
            </li>
            <li>Example filled-in sheet (by Harald on a slightly earlier version of
                grambank)
                <a href="https://github.com/glottobank/Grambank/blob/master/For_coders/Harald Hammarstr%C3%B6m_Urama [kiw].tsv"><b>.tsv</b></a>
                (requires github login, click the download-button to download it).
            </li>
        </ul>
    </li>
    <li>
        <a href="https://github.com/glottobank/Grambank/blob/master/Presentation%20slides%20and%20handouts/grambankcoding2016.pdf"><b>Grambank
            coding manual</b></a> (presentation, requires github login)
    </li>
    <li>The mailing list for all kinds of questions is <a
            href="https://groups.google.com/forum/#!forum/grambank-coders">grambank-coders@googlegroups.com</a>.
        Note:
        <ul>
            <li>There are (almost) no stupid questions</li>
            <li>Provide context to your issue (minimally provide the feature number and
                question in full and your language-specific situation)
            </li>
            <li>One email thread per issue</li>
            <li>If the issue is not solved in the mailing list, it will be discussed at
                the next meeting. Remember, one solution can also be "it is not clear what
                to do, code it with "?"
            </li>
        </ul>
    </li>
    <li>
        <a href="https://github.com/glottobank/Grambank/wiki/List-of-all-features"><b>List</b></a>
        of all Wiki articles
    </li>
    <li>
        <a href="https://docs.google.com/document/d/1L5W61zI1_xSTzHC8okqc-0g0o27dGbl6hnEoBJczqqY/edit?usp=sharing"><b>Procedures
            and examples</b></a> by Jeremy Collins
    </li>
    <li>
        <a href="https://drive.google.com/folderview?id=0B-lVFHmduY1Wb3FURnhTVkJvakE&usp=sharing&tid=0B-lVFHmduY1WQ1UxZXhmZWo5SUU"><b>Meeting
            notes (2015 and back)</b></a></li>
    <li>
        <a href="https://docs.google.com/document/d/125fBEZ80CY-9DYEipAwcPOHEdlZpJDzaFfrzef_kOVc/edit"><b>Agenda
            for next meeting</b></a> (fill in your issues!)
    </li>
    <li>
        <a href="https://docs.google.com/document/d/1YAPZGtpBrMzfNdAoSsplM71CudRudIq9AePQ8Cz8ksQ/edit?usp=sharing"><b>General
            notes on coding</b></a></li>
    <li>
        <a href="https://docs.google.com/document/d/1V5rVmCisUa1dP1zz-UdrmDfuA9JseC7KlUHLQWFDv5o/edit?usp=sharing"><b>History
            of the questionnaire</b></a></li>
    <li>
        <a href="https://github.com/glottobank/Grambank/blob/master/grambank_goals.txt"><b>Grambank
            Statement of Goals (requires github login)</b></a></li>

    <li>NOW OBSOLETE (historical purposes only): <a
            href="https://docs.google.com/spreadsheets/d/1xS6r8G2gdveEBB1kIHdR3eF1A_G-U7fe30hK0tJ2SC8/edit#gid=1504847426"><b>NTS-Collaborative
        feature sheet</b></a> a large excel document with correspondences between Grambank
        and other databases (SAILS, WALS, NTS, etc), deprecated features as well as a lot
        of features metadata.
    </li>
</ul>


<h3>How to use Grambank</h3>
<p>
    Using Grambank requires a browser with Javascript enabled.
</p>
<p>
    You find the features or languages of Grambank through the items "Features" and
    "Languages" in the navigation bar.
</p>

<p>
    Grambank is a publication of the
    ${h.external_link('http://http://www.shh.mpg.de', label='Linguistic and Cultural Evolution Group')}
    at the Max Planck Institute for the Science of Human History, Jena. The datapoints
    furnished by Claire Bowern and Patience Epps was supported by National Science
    Foundation grant HSD-0902114 'Dynamics of Hunter Gatherer Language Change' PIs Claire
    Bowern, Patience Epps, Jane Hill, and Keith Hunley.
</p>

<h3>How to cite Grambank Online</h3>
<p>
    Grambank is not yet publically available and should not for the time being be cited.
    If you nevertheless think you need to cite it contact Harald Hammarstr&ouml;m. The
    eventual citation will contain the names of alll people who contributed to Grambank.
</p>

<h3>Terms of use</h3>
<p>
    (Will be in effect once publically available:) The content of this web site is
    published under a Creative Commons Licence.
    We invite the community of users to think about further applications for the available
    data and look forward to your comments, feedback and questions.
</p>
