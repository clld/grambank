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
            Stephen Levinson, Hannah Haynie, Jeremy Collins and Nicholas Evans.</p>

    </div>

</%def>

<h2>Welcome to grambank</h2>

<p class="lead">
grambank is a database of structural (typological) features of language. It consists of 200 logically independent features (most of them binary) spanning all subdomains of morphosyntax. The grambank feature questionnaire has been filled in, based on reference grammars, for over 500 languages. The aim to eventually reach as many as 3,500 languages. The database can be used to investigate deep language prehistory, the geographical-distribution of features, language universals and the functional interaction of structural features.
</p>

<table class="table table-condensed table-nonfluid">
    <thead>
    <tr>
        <th colspan="3">Statistics</th>
    </tr>
    </thead>
    <tbody>
    <tr><th>Languages</th><td></td><td class="right">${'{:,}'.format(stats['language'])}</td></tr>
    <tr><th>Features</th><td></td><td class="right">${'{:,}'.format(stats['parameter'])}</td></tr>
    <tr><th>Datapoints</th><th>total</th><td class="right">${'{:,}'.format(stats['value'])}</td></tr>
    % for name, count in contribs:
        <tr><td></td><td>${name}</td><td class="right">${'{:,}'.format(count)}</td></tr>
    % endfor
    </tbody>
</table>

<h3>For Coders</h3>
<p>
<ulist>
<ul>Example sheets:
<ulist>
<ul>Empty GB coder sheet, i.e., the most recent version of grambank sheet with feature categories and standardised comments:
<a href="https://github.com/glottobank/Grambank/blob/master/For_coders/grambank_most_updated_sheet.xlsx">.xlsx</a> (requires github login). Note: select the "Empty Sheet" from the workbook.
</ul>
<ul>Example filled-in sheet (by Harald on a slightly earlier version of grambank)
<a href="http://haraldhammarstrom.ruhosting.nl/Harald Hammarstrom_Nyam [nmi].tsv">.tsv</a>
</ul>

</ulist>
</ul>

<ul><a href="http://haraldhammarstrom.ruhosting.nl/grambankcoding.pdf">grambank coding manual</a> (presentation)</ul>


<ul>The mailing list for all kinds of questions is <a href="https://groups.google.com/forum/#!forum/grambank-and-nts-coders-discussion">grambank-and-NTS-coders-discussion@googlegroups.com</a>. Note:

<ulist>
<ul> There are (almost) no stupid questions</ul>
<ul> Provide context to your issue (minimally provide the feature number and question in full and your language-specific situation)</ul>
<ul> One email thread per issue</ul>
<ul> If the issue is not solved in the mailing list, it will be discussed at the next meeting. Remember, one solution can also be "it is not clear what to do, code it with "?"</ul>
</ulist>
</ul>


<ul><a href="https://github.com/glottobank/Grambank/wiki/List-of-all-features">List</a> of all Wiki articles</ul>

<ul><a href="https://github.com/glottobank/Grambank/wiki/Template-for-feature-description">Template</a> for feature description</ul>

<ul><a href="https://docs.google.com/document/d/1L5W61zI1_xSTzHC8okqc-0g0o27dGbl6hnEoBJczqqY/edit?usp=sharing">Procedures and examples</a>by Jeremy Collins</ul>

<ul><a href="https://drive.google.com/folderview?id=0B-lVFHmduY1Wb3FURnhTVkJvakE&usp=sharing&tid=0B-lVFHmduY1WQ1UxZXhmZWo5SUU">Meeting notes</a></ul>

<ul><a href="https://docs.google.com/document/d/125fBEZ80CY-9DYEipAwcPOHEdlZpJDzaFfrzef_kOVc/edit">Agenda for next meeting</a> (fill in your issues!)</ul>

<ul><a href="https://docs.google.com/document/d/1YAPZGtpBrMzfNdAoSsplM71CudRudIq9AePQ8Cz8ksQ/edit?usp=sharing">General notes on coding</a></ul>

<ul><a href="https://docs.google.com/document/d/1V5rVmCisUa1dP1zz-UdrmDfuA9JseC7KlUHLQWFDv5o/edit?usp=sharing">History of the questionnaire</a></ul>

<ul><a href="http://haraldhammarstrom.ruhosting.nl/grambank_goals.txt">grambank Statement of Goals</a></ul>

<ul><a href="https://docs.google.com/spreadsheets/d/1xS6r8G2gdveEBB1kIHdR3eF1A_G-U7fe30hK0tJ2SC8/edit#gid=1504847426">NTS-Collaborative feature sheet</a> a large excel document with correspondences between grambank and other databases (SAILS, WALS, NTS, etc), deprecated features as well as a lot of features metadata.</ul>
</ulist>

</p>



<h3>How to use grambank</h3>
<p>
Using grambank requires a browser with Javascript enabled.
</p>
<p>
You find the features or languages of grambank through the items "Features" and "Languages" in the navigation bar.
</p>


<p>
grambank is a publication of the
${h.external_link('http://http://www.shh.mpg.de', label='Linguistic and Cultural Evolution Group')} at the Max Planck Institute for the Science of Human History, Jena.
</p>


<h3>How to cite grambank Online</h3>
<p>
TODO
Harald Hammarstr\"om, Hedvig Skirg&aring;rd, Jeremy Collins, Hannah Haynie, Michael Dunn, Stephen Levinson, Quentin Atkinson and Russell Gray 2016. Grambank: A world-wide Typological Database. Electronic Database under Development.
</p>

<h3>Terms of use</h3>
<p>
The content of this web site is published under a Creative Commons Licence.
We invite the community of users to think about further applications for the available data
and look forward to your comments, feedback and questions.
</p>
