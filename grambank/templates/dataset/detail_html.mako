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

<p>
    Grambank was constructed in an international collaboration between the Max Planck institutes in Leipzig and Nijmegen,
    the Australian National University, the University of Auckland, Harvard University, Yale University, the University of Turku,
    Kiel University, Uppsala University, SOAS, the Endangered Languages Documentation Programme, and over a hundred scholars from
    around the world. Grambank is designed to be used to investigate the global distribution of features, language universals,
    functional dependencies, language prehistory and interactions between language, cognition, culture and environment.

    The Grambank database currently covers
    <a href="${req.route_url('languages')}">${'{:,}'.format(stats['language'])} language varieties</a>,
    capturing a wide range of grammatical phenomena in
    <a href="${req.route_url('parameters')}">${stats['parameter']} features</a>,
    from word order to verbal tense, nominal plurals, and many other well-studied comparative linguistic variables.
    Grambank's coverage spans 215 different language families and 101 isolates from all inhabited continents. The aim is for
    Grambank to ultimately cover all languages for which a grammar or sketch grammar exists. Grambank is part of
    <a href="https://glottobank.org">Glottobank</a>,
    a research consortium that involves work on complementary databases of lexical data, paradigms, numerals and sound patterns
    in the world's languages. Grambank can be used in concert with other databases, such as those in Glottobank and D-PLACE,
    to deepen our understanding of our history and communicative capabilities.
</p>


<h3>How to cite Grambank</h3>

<p>Please cite the Grambank paper</p>

<blockquote>
    Skirgård, Hedvig, Haynie, Hannah J., Blasi, Damián E., Hammarström, Harald, Collins, Jeremy, Latarche, Jay J., Lesage, Jakob, Weber, Tobias, Witzlack-Makarevich, Alena, Passmore, Sam, Chira, Angela, Maurits, Luke, Dinnage, Russell, Dunn, Michael, Reesink, Ger, Singer, Ruth, Bowern, Claire, Epps, Patience, Hill, Jane, Vesakoski, Outi, Robbeets, Martine, Abbas, Noor Karolin, Auer, Daniel, Bakker, Nancy A., Barbos, Giulia, Borges, Robert D., Danielsen, Swintha, Dorenbusch, Luise, Dorn, Ella, Elliott, John, Falcone, Giada, Fischer, Jana, Ghanggo Ate, Yustinus, Gibson, Hannah, Göbel, Hans-Philipp, Goodall, Jemima A., Gruner, Victoria, Harvey, Andrew, Hayes, Rebekah, Heer, Leonard, Herrera Miranda, Roberto E., Hübler, Nataliia, Huntington-Rainey, Biu, Ivani, Jessica K., Johns, Marilen, Just, Erika, Kashima, Eri, Kipf, Carolina, Klingenberg, Janina V., König, Nikita, Koti, Aikaterina, Kowalik, Richard G. A., Krasnoukhova, Olga, Lindvall, Nora L.M., Lorenzen, Mandy, Lutzenberger, Hannah, Martins, Tônia R.A., Mata German, Celia, van der  Meer, Suzanne, Montoya Samamé, Jaime, Müller, Michael, Muradoglu, Saliha, Neely, Kelsey, Nickel, Johanna, Norvik, Miina, Oluoch, Cheryl Akinyi, Peacock, Jesse, Pearey, India O.C., Peck, Naomi, Petit, Stephanie, Pieper, Sören, Poblete, Mariana, Prestipino, Daniel, Raabe, Linda, Raja, Amna, Reimringer, Janis, Rey, Sydney C., Rizaew, Julia, Ruppert, Eloisa, Salmon, Kim K., Sammet, Jill, Schembri, Rhiannon, Schlabbach, Lars, Schmidt, Frederick W.P., Skilton, Amalia, Smith, Wikaliler Daniel, de  Sousa, Hilário, Sverredal, Kristin, Valle, Daniel, Vera, Javier, Voß, Judith, Witte, Tim, Wu, Henry, Yam, Stephanie, Ye 葉婧婷, Jingting, Yong, Maisie, Yuditha, Tessa, Zariquiey, Roberto, Forkel, Robert, Evans, Nicholas, Levinson, Stephen C., Haspelmath, Martin, Greenhill, Simon J., Atkinson, Quentin D. and Gray, Russell D. (2023). Grambank reveals the importance of genealogical constraints on linguistic diversity and highlights the impact of language loss. Science Advances. DOI: 10.1126/sciadv.adg6175
</blockquote>


<h3>Data availability</h3>

<p>
    The current release version of the Grambank data can be downloaded from
    <a href="https://doi.org/10.5281/zenodo.7740139">https://doi.org/10.5281/zenodo.7740139</a>
</p>

<p>
    Grambank is a part of the Cross-Linguistic Linked Data-project (CLLD). As such, there will continuously be new versions released.
    As with all CLLD-databases, it is important that you note down what version you have used in any analysis of the dataset.
</p>


<h3>Funding</h3>

<p>
    Grambank is a publication of the
    Department of Linguistic and Cultural Evolution at the Max Planck Institute for Evolutionary Anthropology, Leipzig.
    Additional funding was provided by the Max Planck Institute for Psycholinguistics in Nijmegen and
    a Royal Society of New Zealand Marsden grant (UOA1308) to Quentin Atkinson and Russell Gray, and
    an Australian Research Council Centre of Excellence Grant (CE140100041) for the ARC Centre of Excellence for the Dynamics of Language.
    The data furnished by the Hunter-Gatherer Language Database was supported by
    National Science Foundation grant HSD-0902114 'Dynamics of Hunter Gatherer Language Change' PIs Claire Bowern, Patience Epps, Jane Hill, and Keith Hunley.
</p>

<h3>Background</h3>

<p>
    For detailed information on the background of the Grambank project, including description of the features, the coding design
    and procedures please consult the
    <a href="https://github.com/grambank/grambank/wiki">Grambank wiki</a>.
</p>

<h3>Terms of use</h3>
<p>
    The content of this web site is published under a Creative Commons Licence.
</p>
