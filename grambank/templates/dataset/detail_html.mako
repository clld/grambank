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
    Skirgård, Hedvig and Haynie, Hannah J. and Blasi, Damián E. and Hammarström, Harald and Collins, Jeremy and Latarche, Jay J. and Lesage, Jakob and Weber, Tobias and Witzlack-Makarevich, Alena and Passmore, Sam and Chira, Angela and Maurits, Luke and Dinnage, Russell and Dunn, Michael and Reesink, Ger and Singer, Ruth and Bowern, Claire and Epps, Patience and Hill, Jane and Vesakoski, Outi and Robbeets, Martine and Abbas, Noor Karolin and Auer, Daniel and Bakker, Nancy A. and Barbos, Giulia and Borges, Robert D. and Danielsen, Swintha and Dorenbusch, Luise and Dorn, Ella and Elliott, John and Falcone, Giada and Fischer, Jana and Ghanggo Ate, Yustinus and Gibson, Hannah and Göbel, Hans-Philipp and Goodall, Jemima A. and Gruner, Victoria and Harvey, Andrew and Hayes, Rebekah and Heer, Leonard and Herrera Miranda, Roberto E. and Hübler, Nataliia and Huntington-Rainey, Biu and Ivani, Jessica K. and Johns, Marilen and Just, Erika and Kashima, Eri and Kipf, Carolina and Klingenberg, Janina V. and König, Nikita and Koti, Aikaterina and Kowalik, Richard G. A. and Krasnoukhova, Olga and Lindvall, Nora L.M. and Lorenzen, Mandy and Lutzenberger, Hannah and Martins, Tônia R.A. and Mata German, Celia and van der  Meer, Suzanne and Montoya Samamé, Jaime and Müller, Michael and Muradoglu, Saliha and Neely, Kelsey and Nickel, Johanna and Norvik, Miina and Oluoch, Cheryl Akinyi and Peacock, Jesse and Pearey, India O.C. and Peck, Naomi and Petit, Stephanie and Pieper, Sören and Poblete, Mariana and Prestipino, Daniel and Raabe, Linda and Raja, Amna and Reimringer, Janis and Rey, Sydney C. and Rizaew, Julia and Ruppert, Eloisa and Salmon, Kim K. and Sammet, Jill and Schembri, Rhiannon and Schlabbach, Lars and Schmidt, Frederick W.P. and Skilton, Amalia and Smith, Wikaliler Daniel and de  Sousa, Hilário and Sverredal, Kristin and Valle, Daniel and Vera, Javier and Voß, Judith and Witte, Tim and Wu, Henry and Yam, Stephanie and Ye 葉婧婷, Jingting and Yong, Maisie and Yuditha, Tessa and Zariquiey, Roberto and Forkel, Robert and Evans, Nicholas and Levinson, Stephen C. and Haspelmath, Martin and Greenhill, Simon J. and Atkinson, Quentin D. and Gray, Russell D. (in press). Grambank reveals the importance of genealogical constraints on linguistic diversity and highlights the impact of language loss. Science Advances.
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
