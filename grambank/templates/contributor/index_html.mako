<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributors" %>

<%block name="head">
    <style>
        #people th {
            font-size: larger;
            text-align: left;
            padding-bottom: 10px;
        }
    </style>
</%block>


<h2>People</h2>

<ul class="nav nav-pills">
    <li class="active">
        <a href="#projectleader">Project leader</a>
    </li>
    <li class="active">
        <a href="#senioradvisor">Senior advisors</a>
    </li>
    <li class="active">
        <a href="#projectcoordinator">Project coordinator</a>
    </li>
    <li class="active">
        <a href="#databasemanager">Database manager</a>
    </li>
    <li class="active">
        <a href="#patron">Patrons</a>
    </li>
    <li class="active">
        <a href="#nodeleader">Node leaders</a>
    </li>
    <li class="active">
        <a href="#coder">Coders</a>
    </li>
    <li class="active">
        <a href="#methodsteam">Methods-team</a>
    </li>
</ul>

<table id="people">
    <tr>
        <th colspan="4" id="projectleader">
            Project leader
            <a href="#top" title="go to top of the page" style="vertical-align: bottom">&#x21eb;</a>
        </th>
    </tr>
    <tr>
        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Russell D. Gray</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/russell_gray.jpg"
                     class="img-polaroid">
                <p>Russell Gray Ph.D. (Univ. Auckland), FRSNZ, is the Director of the Department of Linguistic and Cultural Evolution at the Max Planck Institute for the Science of Human History. He is sponsor and co-leader of Glottobank.</p>
            </div>
        </td>

        <td></td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th colspan="4" id="senioradvisor">
            Senior advisors
            <a href="#top" title="go to top of the page" style="vertical-align: bottom">&#x21eb;</a>
        </th>
    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Michael Dunn</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/michael_dunn.jpg"
                     class="img-polaroid">
                <p>Michael Dunn studies the evolution of language structure and the history of language families. His work combines traditional linguistic methods with computational (phylogenetic) approaches from the biological and ecological sciences. Michael is Professor of General Linguistics at Uppsala University in Sweden.</p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Ger Reesink</h5>
            </div>
        </td>

        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Nicholas Evans</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/nick_evans.jpg"
                     class="img-polaroid">
                <p>Nick Evans is a typologist and anthropological linguist specialising in Australian and Papuan languages. He is an ARC Laureate Professor at the Australian National University and director of the ARC Research Centre for the Dynamics of Language (CoEDL). Within Glottobank he is a member of the Parabank Collective and an Associated Collaborator in Grambank.</p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Stephen C. Levinson</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/stephen_levinson.jpg"
                     class="img-polaroid">
                <p>Stephen Levinson is Director of the Max Planck Institute for Psycholinguistics. His work focusses on language diversity and its implications for theories of human cognition. He is a designer and senior advisor on the Grambank project.</p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Martin Haspelmath</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/martin_haspelmath.png"
                     class="img-polaroid">
                <p>Martin Haspelmath is a senior scientist at MPI-EVA Leipzig and a professor at Leipzig University. He was one of the creators of the World Atlas of Language Structures (2005) and was heavily involved in feature design in the Atlas of Pidgin and Creole Language Structures (2013). He is a senior advisor in the Grambank project.</p>
            </div>
        </td>

        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Quentin D. Atkinson</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/quentin_atkinson.jpg"
                     class="img-polaroid">
                <p>Quentin Atkinson is Professor in Psychology at the University of Auckland and co-director of the Language, Culture and Cognition Lab. His research uses computational modeling tools to study the evolution of language and culture. He is co-leader of Glottobank.</p>
            </div>
        </td>

        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Simon J. Greenhill</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Greenhill.jpeg"
                     class="img-polaroid">
                <p>Simon Greenhill studies how languages evolve using computational methods and large-scale cross-linguistic databases. He is currently a research fellow in the ARC Research Centre for the Dynamics of Language (CoEDL), and at the Max Planck Institute for the Science of Human History. His role in this project is design and analysis of Lexibank and Parabank.</p>
            </div>
        </td>

        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Outi Vesakoski</h5>
            </div>
        </td>
    </tr>
    <tr>
        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Harald Hammarström</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/harald_hammarstrom.jpg"
                     class="img-polaroid">
                <p>Harald Hammarström has a background in linguistics and computer science. He is working in the Grambank project in the design, planning and management as well as website programming and occasional coding.</p>
            </div>
        </td>
        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Claire Bowern</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Claire.jpg"
                     class="img-polaroid">
                <p>Claire Bowern (PhD, Harvard, 2004) is Associate Professor of Linguistics at Yale University. She is a specialist in historical linguistics and language documentation, with particular reference to the languages of Australia - Yale Pama-Nyungan Lab. She does fieldwork in northern Australia on Yolŋu and Nyulnyulan languages and her reference grammar of Bardi appeared in 2012. Her current research involves the possible differences between languages spoken by hunter-gatherer groups and the better-studied languages of agriculturalists. She has led an interdisciplinary initiative funded by the National Science Foundation’s Human Social Dynamics program to investigate hunter-gatherer language change, including differences in loan rates, material culture nomenclature, and ethnobiology.</p>
            </div>
        </td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th colspan="4" id="projectcoordinator">
            Project coordinator
            <a href="#top" title="go to top of the page" style="vertical-align: bottom">&#x21eb;</a>
        </th>
    </tr>
    <tr>
        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Hedvig Skirgård</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/hedvig_skirgard.jpg"
                     class="img-polaroid">
                <p>Hedvig Skirgård is a postdoctoral researcher at DLCE at MPI-EVA in Leipzig. She is the main project coordinator for Grambank. She was previously employed as a coder within the Nijmegen Typological Survey which is the precursor to Grambank. She is also the patron for a set of Grambank features, including features concerning negation and tense &amp; aspect.</p>
            </div>
        </td>
        <td></td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th colspan="4" id="databasemanager">
            Database manager
            <a href="#top" title="go to top of the page" style="vertical-align: bottom">&#x21eb;</a>
        </th>
    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Robert Forkel</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/robert_forkel.jpg"
                     class="img-polaroid">
                <p>Robert Forkel is responsible for strategies and infrastructure for data curation and presentation within the consortium, bringing in the experiences gathered in the CLLD project.</p>
            </div>
        </td>
        <td></td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th colspan="4" id="patron">
            Patrons
            <a href="#top" title="go to top of the page" style="vertical-align: bottom">&#x21eb;</a>
        </th>
    </tr>
    <tr>
        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Hedvig Skirgård</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/hedvig_skirgard.jpg"
                     class="img-polaroid">
                <p>Hedvig Skirgård is a postdoctoral researcher at DLCE at MPI-EVA in Leipzig. She is the main project coordinator for Grambank. She was previously employed as a coder within the Nijmegen Typological Survey which is the precursor to Grambank. She is also the patron for a set of Grambank features, including features concerning negation and tense &amp; aspect.</p>
            </div>
        </td>
        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Hannah J. Haynie</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/hannah_haynie.jpg"
                     class="img-polaroid">
                <p>Hannah Haynie is an Assistant Professor of Linguistics at the University of Colorado. Her research focuses on language diversity and language change, integrating ideas from ecology and biology with rigorous linguistic analysis to answer questions in linguistic typology and diachronic linguistics. She is particularly interested in interactions between language, culture, and the physical environment. Patterns of linguistic diversity in North America have been central to her work to date. Hannah is one of the Grambank questionnaire designers and a &#39;feature patron&#39; for the coding effort.</p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Harald Hammarström</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/harald_hammarstrom.jpg"
                     class="img-polaroid">
                <p>Harald Hammarström has a background in linguistics and computer science. He is working in the Grambank project in the design, planning and management as well as website programming and occasional coding.</p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Jeremy Collins</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/jeremy_collins.jpg"
                     class="img-polaroid">
                <p>Jeremy Collins is a PhD student at Radboud University, Nijmegen and the Max Planck Institute for Psycholinguistics, researching language structures and what their distributions can show about prehistoric relatedness and contact between languages. He is a Grambank designer and feature patron.</p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Jay Latarche</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Jay.jpg"
                     class="img-polaroid">
                <p>Jay Latarche is the team coordinator (and coder) at SOAS/ELDP University, London, and particularly enjoys coding from East Asian language families. He is currently interested in conducting further research on logogram amnesia in Mainland China. He is also interested in transgender specific speech patterns in Mandarin Chinese.</p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Jakob Lesage</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/lesage.jpg"
                     class="img-polaroid">
                <p>Jakob Lesage PhD (INALCO at LLACAN, 2020) specializes in language description, language documentation and linguistic typology. He focuses on African languages, particularly on Kam and other less documented languages of Nigeria. Jakob is a Grambank patron and longtime coder.</p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Alena Witzlack-Makarevich</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Alena.png"
                     class="img-polaroid">
                <p>Alena Witzlack-Makarevich is a senior lecturer at the Hebrew University of Jerusalem. In the past, she supervised the GramBank coders at the University of Kiel. Currently she is a patron of twenty feature related to grammatical relations and alignment.</p>
            </div>
        </td>



        <td></td>

    </tr>
    <tr>
        <th colspan="4" id="nodeleader">
            Node leaders
            <a href="#top" title="go to top of the page" style="vertical-align: bottom">&#x21eb;</a>
        </th>
    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Hedvig Skirgård</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/hedvig_skirgard.jpg"
                     class="img-polaroid">
                <p>Hedvig Skirgård is a postdoctoral researcher at DLCE at MPI-EVA in Leipzig. She is the main project coordinator for Grambank. She was previously employed as a coder within the Nijmegen Typological Survey which is the precursor to Grambank. She is also the patron for a set of Grambank features, including features concerning negation and tense &amp; aspect.</p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Harald Hammarström</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/harald_hammarstrom.jpg"
                     class="img-polaroid">
                <p>Harald Hammarström has a background in linguistics and computer science. He is working in the Grambank project in the design, planning and management as well as website programming and occasional coding.</p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Jeremy Collins</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/jeremy_collins.jpg"
                     class="img-polaroid">
                <p>Jeremy Collins is a PhD student at Radboud University, Nijmegen and the Max Planck Institute for Psycholinguistics, researching language structures and what their distributions can show about prehistoric relatedness and contact between languages. He is a Grambank designer and feature patron.</p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Jay Latarche</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Jay.jpg"
                     class="img-polaroid">
                <p>Jay Latarche is the team coordinator (and coder) at SOAS/ELDP University, London, and particularly enjoys coding from East Asian language families. He is currently interested in conducting further research on logogram amnesia in Mainland China. He is also interested in transgender specific speech patterns in Mandarin Chinese.</p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Jakob Lesage</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/lesage.jpg"
                     class="img-polaroid">
                <p>Jakob Lesage PhD (INALCO at LLACAN, 2020) specializes in language description, language documentation and linguistic typology. He focuses on African languages, particularly on Kam and other less documented languages of Nigeria. Jakob is a Grambank patron and longtime coder.</p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Tobias Weber</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Tobias.jpg"
                     class="img-polaroid">
                <p>Tobias Weber is a research associate at the University of Kiel. His research interests include diachronic typology, grammatical relations, and the languages of Southeast Asia. Within Glottobank, he is involved in the Grambank project.</p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Alena Witzlack-Makarevich</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Alena.png"
                     class="img-polaroid">
                <p>Alena Witzlack-Makarevich is a senior lecturer at the Hebrew University of Jerusalem. In the past, she supervised the GramBank coders at the University of Kiel. Currently she is a patron of twenty feature related to grammatical relations and alignment.</p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Roberto Zariquiey</h5>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Hannah Gibson</h5>
            </div>
        </td>



        <td></td>



        <td></td>



        <td></td>

    </tr>
    <tr>
        <th colspan="4" id="coder">
            Coders
            <a href="#top" title="go to top of the page" style="vertical-align: bottom">&#x21eb;</a>
        </th>
    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Hedvig Skirgård</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/hedvig_skirgard.jpg"
                     class="img-polaroid">
                <p>Hedvig Skirgård is a postdoctoral researcher at DLCE at MPI-EVA in Leipzig. She is the main project coordinator for Grambank. She was previously employed as a coder within the Nijmegen Typological Survey which is the precursor to Grambank. She is also the patron for a set of Grambank features, including features concerning negation and tense &amp; aspect.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/HS" title="Contributed 6860 datapoints for 68 languages and dialects">Contributed 6860 datapoints for 68 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Hannah J. Haynie</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/hannah_haynie.jpg"
                     class="img-polaroid">
                <p>Hannah Haynie is an Assistant Professor of Linguistics at the University of Colorado. Her research focuses on language diversity and language change, integrating ideas from ecology and biology with rigorous linguistic analysis to answer questions in linguistic typology and diachronic linguistics. She is particularly interested in interactions between language, culture, and the physical environment. Patterns of linguistic diversity in North America have been central to her work to date. Hannah is one of the Grambank questionnaire designers and a &#39;feature patron&#39; for the coding effort.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/HJH" title="Contributed 1130 datapoints for 7 languages and dialects">Contributed 1130 datapoints for 7 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Harald Hammarström</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/harald_hammarstrom.jpg"
                     class="img-polaroid">
                <p>Harald Hammarström has a background in linguistics and computer science. He is working in the Grambank project in the design, planning and management as well as website programming and occasional coding.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/HH" title="Contributed 9768 datapoints for 55 languages and dialects">Contributed 9768 datapoints for 55 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Damián E. Blasi</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Damian.jpg"
                     class="img-polaroid">
                <p>Damián Blasi is a postdoc at the University of Zürich and an external member of the MPI SHH where he uses large-scale typological databases to make inferences on the relevance of non-linguistic factors on linguistic structures, and provides general statistical assistance for Glottobank.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/DB" title="Contributed 780 datapoints for 4 languages and dialects">Contributed 780 datapoints for 4 languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Jeremy Collins</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/jeremy_collins.jpg"
                     class="img-polaroid">
                <p>Jeremy Collins is a PhD student at Radboud University, Nijmegen and the Max Planck Institute for Psycholinguistics, researching language structures and what their distributions can show about prehistoric relatedness and contact between languages. He is a Grambank designer and feature patron.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/JC" title="Contributed 1993 datapoints for 16 languages and dialects">Contributed 1993 datapoints for 16 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Jay Latarche</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Jay.jpg"
                     class="img-polaroid">
                <p>Jay Latarche is the team coordinator (and coder) at SOAS/ELDP University, London, and particularly enjoys coding from East Asian language families. He is currently interested in conducting further research on logogram amnesia in Mainland China. He is also interested in transgender specific speech patterns in Mandarin Chinese.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/JLA" title="Contributed 31048 datapoints for 183 languages and dialects">Contributed 31048 datapoints for 183 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Jakob Lesage</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/lesage.jpg"
                     class="img-polaroid">
                <p>Jakob Lesage PhD (INALCO at LLACAN, 2020) specializes in language description, language documentation and linguistic typology. He focuses on African languages, particularly on Kam and other less documented languages of Nigeria. Jakob is a Grambank patron and longtime coder.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/JLE" title="Contributed 11582 datapoints for 180 languages and dialects">Contributed 11582 datapoints for 180 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Tobias Weber</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Tobias.jpg"
                     class="img-polaroid">
                <p>Tobias Weber is a research associate at the University of Kiel. His research interests include diachronic typology, grammatical relations, and the languages of Southeast Asia. Within Glottobank, he is involved in the Grambank project.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/TWE" title="Contributed 4210 datapoints for 22 languages and dialects">Contributed 4210 datapoints for 22 languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Alena Witzlack-Makarevich</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Alena.png"
                     class="img-polaroid">
                <p>Alena Witzlack-Makarevich is a senior lecturer at the Hebrew University of Jerusalem. In the past, she supervised the GramBank coders at the University of Kiel. Currently she is a patron of twenty feature related to grammatical relations and alignment.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/AWM" title="Contributed 369 datapoints for 2 languages and dialects">Contributed 369 datapoints for 2 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Angela Chira</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/AC" title="Contributed  datapoints for  languages and dialects">Contributed  datapoints for  languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Olena Shcherbakova</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/OSI" title="Contributed  datapoints for  languages and dialects">Contributed  datapoints for  languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Michael Dunn</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/michael_dunn.jpg"
                     class="img-polaroid">
                <p>Michael Dunn studies the evolution of language structure and the history of language families. His work combines traditional linguistic methods with computational (phylogenetic) approaches from the biological and ecological sciences. Michael is Professor of General Linguistics at Uppsala University in Sweden.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/MD" title="Contributed 14847 datapoints for 145 languages and dialects">Contributed 14847 datapoints for 145 languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Ger Reesink</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/GR" title="Contributed 14319 datapoints for 142 languages and dialects">Contributed 14319 datapoints for 142 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Ruth Singer</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/RSI" title="Contributed 14581 datapoints for 144 languages and dialects">Contributed 14581 datapoints for 144 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Claire Bowern</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Claire.jpg"
                     class="img-polaroid">
                <p>Claire Bowern (PhD, Harvard, 2004) is Associate Professor of Linguistics at Yale University. She is a specialist in historical linguistics and language documentation, with particular reference to the languages of Australia - Yale Pama-Nyungan Lab. She does fieldwork in northern Australia on Yolŋu and Nyulnyulan languages and her reference grammar of Bardi appeared in 2012. Her current research involves the possible differences between languages spoken by hunter-gatherer groups and the better-studied languages of agriculturalists. She has led an interdisciplinary initiative funded by the National Science Foundation’s Human Social Dynamics program to investigate hunter-gatherer language change, including differences in loan rates, material culture nomenclature, and ethnobiology.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/CB" title="Contributed 1098 datapoints for 21 languages and dialects">Contributed 1098 datapoints for 21 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Patience Epps</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/PE" title="Contributed 1098 datapoints for 21 languages and dialects">Contributed 1098 datapoints for 21 languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Jane Hill</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/JH" title="Contributed  datapoints for  languages and dialects">Contributed  datapoints for  languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Noor Karolin Abbas</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/KA" title="Contributed 585 datapoints for 3 languages and dialects">Contributed 585 datapoints for 3 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Sunny Ananth</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/SA" title="Contributed 15 datapoints for 1 languages and dialects">Contributed 15 datapoints for 1 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Daniel Auer</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/daniel_auer.jpg"
                     class="img-polaroid">
                <p>Daniel Auer is a graduate student at the Humboldt University of Berlin and a coder for Grambank. He focuses on Bantu and so-called Khoisan languages in East and Southern Africa.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/DA" title="Contributed 2663 datapoints for 14 languages and dialects">Contributed 2663 datapoints for 14 languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Roberto Zariquiey</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/RZ" title="Contributed 2145 datapoints for 11 languages and dialects">Contributed 2145 datapoints for 11 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Nancy A. Bakker</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Nancy.jpg"
                     class="img-polaroid">
                <p>Nancy Bakker (formerly Nancy Poo) studied German and English in Potsdam as well as linguistics and Islamic Studies in Kiel. She is now a teacher for German as a foreign language and codes languages for Grambank.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/NB" title="Contributed 6168 datapoints for 34 languages and dialects">Contributed 6168 datapoints for 34 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Giulia Barbos</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Giulia.jpg"
                     class="img-polaroid">
                <p>Giulia Barbos is a Grambank language coder based in London. She is part of the SOAS/ELDP team and she holds a degree in Linguistics and International Relations. She has an interest for the area of intersection of language/discourse and the political sphere. In particular, she is passionate about language change and variation in political discourse, including transformations at the lexical, morphosyntactic, and discourse-pragmatic levels.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/GB" title="Contributed 6586 datapoints for 34 languages and dialects">Contributed 6586 datapoints for 34 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Russell Barlow</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/RBA" title="Contributed  datapoints for  languages and dialects">Contributed  datapoints for  languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Anina Bolls</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/AB" title="Contributed 585 datapoints for 3 languages and dialects">Contributed 585 datapoints for 3 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Robert D. Borges</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/RB" title="Contributed 701 datapoints for 4 languages and dialects">Contributed 701 datapoints for 4 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Mitchell Browen</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/MB" title="Contributed 195 datapoints for 1 languages and dialects">Contributed 195 datapoints for 1 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Hoju Cha 차호주</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/hoju_cha.jpg"
                     class="img-polaroid">
                <p>Hoju Cha is an undergraduate student of linguistics at Seoul National University. He has been an avid reader of grammars for some time, and now he&#39;s been tasked to code languages at Grambank. He is interested in linguistic typology and mathematics.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/HC" title="Contributed  datapoints for  languages and dialects">Contributed  datapoints for  languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Lennart Chevallier</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/lennart_chevallier.jpg"
                     class="img-polaroid">
                <p>Lennart Chevallier codes languages for Grambank. He is a master student at CAU Kiel studying Language and Variation and Political Science.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/LC" title="Contributed 390 datapoints for 2 languages and dialects">Contributed 390 datapoints for 2 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Swintha Danielsen</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/SD" title="Contributed 3076 datapoints for 32 languages and dialects">Contributed 3076 datapoints for 32 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Hugo de Vos</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/HDV" title="Contributed  datapoints for  languages and dialects">Contributed  datapoints for  languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Sinoël Dohlen</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/sinoel_dohlen.png"
                     class="img-polaroid">
                <p>Sinoël Dohlen is an undergrad student of Theoretical Linguistics at the University of Leipzig. He&#39;s also interested in typology, language change and the origin of language. His task is coding languages for Grambank.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/SDO" title="Contributed 594 datapoints for 4 languages and dialects">Contributed 594 datapoints for 4 languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Luise Dorenbusch</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Luise.png"
                     class="img-polaroid">
                <p>Luise Dorenbusch studied linguistics in Leipzig and Nijmegen and has worked at the MPI for Evolutionary Anthropology and the MPI for Psycholinguistics. Currently based in Leipzig, she codes language data for Grambank with a focus on the non-Pama-Nyungan languages of Australia.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/LD" title="Contributed 3624 datapoints for 20 languages and dialects">Contributed 3624 datapoints for 20 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Ella Dorn</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/ella_dorn.jpg"
                     class="img-polaroid">
                <p>Ella Dorn is a BA Chinese and Linguistics student at SOAS/ELDP, University of London and a coder for Grambank. She enjoys diachronic linguistics, Sino-Korean loanwords, light verse and film history.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/ED" title="Contributed 3120 datapoints for 16 languages and dialects">Contributed 3120 datapoints for 16 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Marie Duhamel</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/MDU" title="Contributed 195 datapoints for 1 languages and dialects">Contributed 195 datapoints for 1 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Farah El Haj Ali</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Farah_El_Haj_Ali.jpg"
                     class="img-polaroid">
                <p>Farah El Haj Ali is a Grambank coder currently studying English Studies and Empirical linguistics at the University of Kiel.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/FE" title="Contributed 585 datapoints for 3 languages and dialects">Contributed 585 datapoints for 3 languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>John Elliott</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/JE" title="Contributed 2534 datapoints for 13 languages and dialects">Contributed 2534 datapoints for 13 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Grace Ephraums</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/GE" title="Contributed  datapoints for  languages and dialects">Contributed  datapoints for  languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Giada Falcone</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/GF" title="Contributed 2087 datapoints for 11 languages and dialects">Contributed 2087 datapoints for 11 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Anna-Maria Fehn</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/AF" title="Contributed 195 datapoints for 1 languages and dialects">Contributed 195 datapoints for 1 languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Jana Fischer</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/JanaWinkler.jpg"
                     class="img-polaroid">
                <p>Jana Fischer is a master&#39;s student of Language &amp; Variation and English Language, Literature &amp; Lingustics at CAU Kiel. She has an interest in creoles. Her role in Grambank is to code languages.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/JW" title="Contributed 3948 datapoints for 21 languages and dialects">Contributed 3948 datapoints for 21 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Yustinus Ghanggo Ate</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Yustinus_Ghanggo_Ate.jpg"
                     class="img-polaroid">
                <p>Yustinus Ghanggo Ate did his MA in General Linguistics at The Australian National University, Canberra, Australia. His research interests are descriptive linguistics, language documentation, theoretical linguistics (paradigm-based analysis and lexically-based analysis), language typology, and mother tongue-based education. He plans to do his PhD study in the future, documenting and describing an unknown and endangered language of eastern Indonesia.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/YGA" title="Contributed 585 datapoints for 3 languages and dialects">Contributed 585 datapoints for 3 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Hannah Gibson</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/HG" title="Contributed  datapoints for  languages and dialects">Contributed  datapoints for  languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Hans-Philipp Göbel</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Hans-Philipp.jpg"
                     class="img-polaroid">
                <p>Hans-Philipp Göbel codes languages for Grambank. He is a bachelor student in empirical linguistics and scandinavian studies at CAU Kiel. In his masters programme he wants to focus on language typology.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/HPG" title="Contributed 11193 datapoints for 76 languages and dialects">Contributed 11193 datapoints for 76 languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Jemima A. Goodall</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Jemima.jpg"
                     class="img-polaroid">
                <p>Jemima Goodall is a Grambank coder based at the SOAS/ELDP university team in London. She is currently a Linguistics BA student at UCL.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/JG" title="Contributed 29351 datapoints for 161 languages and dialects">Contributed 29351 datapoints for 161 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Elizabeth Goodrich</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/LG" title="Contributed  datapoints for  languages and dialects">Contributed  datapoints for  languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Samuel Griggs</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/SG" title="Contributed  datapoints for  languages and dialects">Contributed  datapoints for  languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Victoria Gruner</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/victoria_gruner.jpg"
                     class="img-polaroid">
                <p>Victoria Gruner (who also likes to be called Vicky) joined the Grambank Leipzig Team in October 2020. She has a Bachelor&#39;s degree in Romance Studies from University Leipzig and her role in Grambank is to code languages.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/VG" title="Contributed 2204 datapoints for 13 languages and dialects">Contributed 2204 datapoints for 13 languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Andrew Harvey</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/andrew_harvey.jpg"
                     class="img-polaroid">
                <p>Andrew Harvey is a junior fellow at the Research Institute for Languages and Cultures of Asia and Africa (ILCAA), Tokyo University of Foreign Studies. His interests include the languages of the Tanzanian rift, their documentation and description, their formal morphosyntax, and the histories and cultures of their speaker communities, especially as evinced through linguistic arts and language contact.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/AH" title="Contributed 1740 datapoints for 9 languages and dialects">Contributed 1740 datapoints for 9 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Rebekah Hayes</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/RHA" title="Contributed 7410 datapoints for 38 languages and dialects">Contributed 7410 datapoints for 38 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Leonard Heer</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/LH" title="Contributed 975 datapoints for 5 languages and dialects">Contributed 975 datapoints for 5 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Roberto E. Herrera Miranda</h5>
                <p>Roberto E. Herrera Miranda is a research assistant working on the Grambank and Parabank projects since June 2015. He is based in Leipzig and works mostly on languages of the so-called Intermediate Area in the Americas.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/RHE" title="Contributed 33590 datapoints for 185 languages and dialects">Contributed 33590 datapoints for 185 languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Nataliia Hübler</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Natalia.png"
                     class="img-polaroid">
                <p>Nataliia Hübler (formerly Natalia Neshcheret) studied Language and Variation and German linguistics at CAU Kiel, where she started coding languages. Now she is a PhD student within Eurasia3angle project at the MPI SHH in Jena. She is exploring the history of Transeurasian languages on the basis of their structural features by applying phylogenetic methods.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/NH" title="Contributed 18062 datapoints for 98 languages and dialects">Contributed 18062 datapoints for 98 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Biu H. Huntington-Rainey</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Biu.jpg"
                     class="img-polaroid">
                <p>Biu Huntington-Rainey is a BA student at SOAS/ELDP. Outside of coding languages with Grambank, his study focusses on language and identity on the internet, particularly the orthography of memes and online/offline code-switching.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/BHR" title="Contributed 20978 datapoints for 108 languages and dialects">Contributed 20978 datapoints for 108 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Guglielmo Inglese</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/GI" title="Contributed 87 datapoints for 2 languages and dialects">Contributed 87 datapoints for 2 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Jessica K. Ivani</h5>
                <p>Jessica Katiuscia Ivani is a PhD student at the University of Pavia, conducting typological research on the morphosyntax of grammatical features, with a focus on nominal number and gender. Within Glottobank, she is involved in the Parabank project.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/JI" title="Contributed 1755 datapoints for 9 languages and dialects">Contributed 1755 datapoints for 9 languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Marilen Johns</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Marilen.png"
                     class="img-polaroid">
                <p>Marilen Johns is a Master&#39;s Student at CAU Kiel and is coding languages for Grambank. She is studying Language and Variation and European Ethnography, and is interested in the differences of vulgar speech between English and German.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/MJ" title="Contributed 1950 datapoints for 10 languages and dialects">Contributed 1950 datapoints for 10 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Erika Just</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Erika.jpg"
                     class="img-polaroid">
                <p>Erika Just is a PhD candidate at the University of Kiel. Her research project is concerned with verb agreement domains, combining comparative typological methods with a case study on optional verb agreement in three related Bantu languages. Her role in Grambank is to code languages.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/EJ" title="Contributed 11596 datapoints for 61 languages and dialects">Contributed 11596 datapoints for 61 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Ivan Kapitonov</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/IK" title="Contributed 195 datapoints for 1 languages and dialects">Contributed 195 datapoints for 1 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Eri Kashima</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/eri_kashima.jpg"
                     class="img-polaroid">
                <p>Eri Kashima is a PhD candidate at the Australian National University, and part of the ARC Centre of Excellence for the Dynamics of Language, and a member of the ARC Wellsprings of Linguistic Diversity Project. Eri is a documentary sociolinguist who works on language variation and change in the southern area of Papua New Guinea.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/EK" title="Contributed 1733 datapoints for 9 languages and dialects">Contributed 1733 datapoints for 9 languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Aarifah Khoodoruth</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/AK" title="Contributed  datapoints for  languages and dialects">Contributed  datapoints for  languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Carolina Kipf</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/CK" title="Contributed 1755 datapoints for 9 languages and dialects">Contributed 1755 datapoints for 9 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Janina V. Klingenberg</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/janina_klingenberg.png"
                     class="img-polaroid">
                <p>Janina Klingenberg is a master student of general linguistics at the university of Hamburg with a bachelors degree in Spanish philology and empirical linguistics. She is interested in interrogative constructions and multilingualism. Her role in Grambank is to code languages.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/JK" title="Contributed 9945 datapoints for 51 languages and dialects">Contributed 9945 datapoints for 51 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Nikita König</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/NK" title="Contributed 1560 datapoints for 8 languages and dialects">Contributed 1560 datapoints for 8 languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Aikaterina Koti</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/KK" title="Contributed 975 datapoints for 5 languages and dialects">Contributed 975 datapoints for 5 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Richard G. A. Kowalik</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/RichardKowalik.jpg"
                     class="img-polaroid">
                <p>Richard Kowalik is a PhD student at Stockholm University. His project is to write a grammar for South Saami, a small Finno-Ugric language spoken in Sweden and Norway. Within Grambank, he has been coding African languages and Uralic languages.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/RK" title="Contributed 9723 datapoints for 50 languages and dialects">Contributed 9723 datapoints for 50 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Olga Krasnoukhova</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Olga.jpg"
                     class="img-polaroid">
                <p>Olga Krasnoukhova is a member of the Grambank project and is responsible for coding data on South American languages. Her research interests lie in linguistic typology and areal linguistics focusing on South American languages. Her doctoral thesis (2012) investigated syntactic and morphosyntactic characteristics of the Noun Phrase components. Olga is also one of the designers of the SAILS database (http://sails.clld.org/).</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/OK" title="Contributed 2426 datapoints for 14 languages and dialects">Contributed 2426 datapoints for 14 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Kate Lynn Lindsey</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/KLL" title="Contributed 195 datapoints for 1 languages and dialects">Contributed 195 datapoints for 1 languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Nora  L. M. Lindvall</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/NL" title="Contributed 1755 datapoints for 9 languages and dialects">Contributed 1755 datapoints for 9 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Mandy Lorenzen</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Mandy.jpg"
                     class="img-polaroid">
                <p>Mandy Lorenzen is a bachelor student in Empirical Linguistics and German at CAU Kiel. Her role in Grambank is to code languages.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/ML" title="Contributed 11800 datapoints for 80 languages and dialects">Contributed 11800 datapoints for 80 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Hannah Lutzenberger</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/HL" title="Contributed 46 datapoints for 2 languages and dialects">Contributed 46 datapoints for 2 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Manuel Rüdisühli</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/MRU" title="Contributed  datapoints for  languages and dialects">Contributed  datapoints for  languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Alexandra Marley</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/AM" title="Contributed 195 datapoints for 1 languages and dialects">Contributed 195 datapoints for 1 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Tânia R. A. Martins</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/TM" title="Contributed 585 datapoints for 3 languages and dialects">Contributed 585 datapoints for 3 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Marvin Leonard Martiny</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/marvin_martiny.jpg"
                     class="img-polaroid">
                <p>Marvin Martiny is a Grambank coder from southwest Germany. He has been working on the topic of grammaticalization in the MAGRAM project at the Johannes Gutenberg-University Mainz, where he will start his PhD (on future grams in SAILs) in short. His linguistic interests vary from neurolinguistics to historical linguistics.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/MLM" title="Contributed  datapoints for  languages and dialects">Contributed  datapoints for  languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Celia Mata German</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/CMG" title="Contributed 1170 datapoints for 6 languages and dialects">Contributed 1170 datapoints for 6 languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Suzanne van der Meer</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/SVM" title="Contributed 4093 datapoints for 46 languages and dialects">Contributed 4093 datapoints for 46 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Susanne Maria Michaelis</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/SMI" title="Contributed  datapoints for  languages and dialects">Contributed  datapoints for  languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Jaime Montoya</h5>
                <p>Jaime Montoya is a Grambank coder from Lima, Peru.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/JM" title="Contributed 2535 datapoints for 13 languages and dialects">Contributed 2535 datapoints for 13 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Michael Müller</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/MM" title="Contributed 21442 datapoints for 117 languages and dialects">Contributed 21442 datapoints for 117 languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Saliha Muradoglu</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/SM" title="Contributed 1170 datapoints for 6 languages and dialects">Contributed 1170 datapoints for 6 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5> HunterGatherer</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/HunterGatherer" title="Contributed 16304 datapoints for 119 languages and dialects">Contributed 16304 datapoints for 119 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>David Nash</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/DN" title="Contributed 42 datapoints for 1 languages and dialects">Contributed 42 datapoints for 1 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Kelsey Neely</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/KN" title="Contributed  datapoints for  languages and dialects">Contributed  datapoints for  languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Johanna Nickel</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Johanna_Nickel.JPG"
                     class="img-polaroid">
                <p>Johanna Nickel is a master&#39;s student at CAU Kiel, where she studies Language &amp; Variation and Scandinavian studies. Her role at Grambank is to code languages.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/JN" title="Contributed 4679 datapoints for 24 languages and dialects">Contributed 4679 datapoints for 24 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Miina Norvik</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/MN" title="Contributed 1170 datapoints for 6 languages and dialects">Contributed 1170 datapoints for 6 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Bruno Olsson</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/BO" title="Contributed 195 datapoints for 1 languages and dialects">Contributed 195 datapoints for 1 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Cheryl Akinyi Oluoch</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/CAO" title="Contributed 3315 datapoints for 17 languages and dialects">Contributed 3315 datapoints for 17 languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>David Osgarby</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/DO" title="Contributed 195 datapoints for 1 languages and dialects">Contributed 195 datapoints for 1 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Jesse Peacock</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/JP" title="Contributed 1881 datapoints for 12 languages and dialects">Contributed 1881 datapoints for 12 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>India O.C. Pearey</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/india_castro.jpg"
                     class="img-polaroid">
                <p>India Pearey is a Grambank coder based at SOAS/ELDP London where she is completing a BA in Korean and Linguistics. Her specific interests lie in Koreanic languages and judging prescriptivists. Aside from long hours reading grammars her hobbies include sports, eating, and sleeping.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/IC" title="Contributed 1170 datapoints for 6 languages and dialects">Contributed 1170 datapoints for 6 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Naomi Peck</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/naomi_peck.jpg"
                     class="img-polaroid">
                <p>Naomi Peck is a Grambank coder from the ANU node. She is currently a PhD student at the Johannes Gutenberg-University Mainz, where she is working on a description of Kera&#39;a (Idu Mishmi), a Tibeto-Burman language of North-East India.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/NP" title="Contributed 21437 datapoints for 110 languages and dialects">Contributed 21437 datapoints for 110 languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Jana Peter</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/JPE" title="Contributed 195 datapoints for 1 languages and dialects">Contributed 195 datapoints for 1 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Stephanie Petit</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/SPE" title="Contributed 1950 datapoints for 10 languages and dialects">Contributed 1950 datapoints for 10 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Sören Pieper</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Pieper.jpg"
                     class="img-polaroid">
                <p>Sören Pieper is a Grambank coder from Kiel. He is in the final stages of his MA in Language and Variation and Political Science at the University of Kiel. He is currently writing his MA thesis in typology concerning the cross-linguistic diversity of antipassives.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/SPI" title="Contributed 3120 datapoints for 16 languages and dialects">Contributed 3120 datapoints for 16 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Mariana Poblete</h5>
                <p>Mariana is a chilean-venezuelan Grambank coder currently located in Perú.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/MP" title="Contributed 2145 datapoints for 11 languages and dialects">Contributed 2145 datapoints for 11 languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Daniel Prestipino</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/daniel_prestipino.jpg"
                     class="img-polaroid">
                <p>Daniel Prestipino is an undergraduate student at the Australian National University, studying Linguistics, German language, and Classical Studies. He is a coder at the ANU node of the Grambank project, and is interested in what socio-cultural factors drive language change. He hopes to pursue postgraduate study and research in the future.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/DP" title="Contributed 3368 datapoints for 41 languages and dialects">Contributed 3368 datapoints for 41 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Linda Raabe</h5>
                <p>Linda Raabe is a bachelor student at CAU Kiel, where she studies empirical linguistics. Her role in Grambank is to code languages.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/LR" title="Contributed 1434 datapoints for 8 languages and dialects">Contributed 1434 datapoints for 8 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Amna Raja</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Amna.png"
                     class="img-polaroid">
                <p>Amna Raja is a Grambank coder at SOAS/ELDP who has so far coded languages from the Americas and Africa with outlooks towards other continents. She enjoys reading, kickboxing and henna.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/AR" title="Contributed 3120 datapoints for 16 languages and dialects">Contributed 3120 datapoints for 16 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Tihomir Rangelov</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/TR" title="Contributed  datapoints for  languages and dialects">Contributed  datapoints for  languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Janis Reimringer</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/JR" title="Contributed 1021 datapoints for 91 languages and dialects">Contributed 1021 datapoints for 91 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Sydney C. Rey</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/sydney_rey.jpg"
                     class="img-polaroid">
                <p>Sydney Rey has an MA in Language Documentation and Description from SOAS/ELDP University of London. Her interests lie in syntax and diachronic variation in endangered North American languages as well as data accessibility and community-centric language documentation. She codes language structures for Grambank.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/SR" title="Contributed 4349 datapoints for 26 languages and dialects">Contributed 4349 datapoints for 26 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Julia Rizaew</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/julia_rizaew.jpg"
                     class="img-polaroid">
                <p>Julia Rizaew is an MA Translation student at SOAS/ELDP University of London and a language coder at Grambank. She has background in Japanese and Linguistics, and is interested particularly in East Asian languages.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/JRI" title="Contributed 2535 datapoints for 13 languages and dialects">Contributed 2535 datapoints for 13 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Kristian Roncero Toledo</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/KR" title="Contributed  datapoints for  languages and dialects">Contributed  datapoints for  languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Eloisa Ruppert</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Eloisa.jpg"
                     class="img-polaroid">
                <p>Eloisa Ruppert is a coder from Kiel. She is currently doing her master’s degree in Language and Variation and Scandinavian Studies.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/ER" title="Contributed 9750 datapoints for 50 languages and dialects">Contributed 9750 datapoints for 50 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Kim K. Salmon</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/kim_salmon.jpg"
                     class="img-polaroid">
                <p>Kim Salmon is an undergrad student of linguistics at the University of Leipzig and has been coding languages for Grambank since 2020. She is mostly interrested in morphology and lexicology as well as language change, variety and contact phenomena.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/KSA" title="Contributed 5040 datapoints for 27 languages and dialects">Contributed 5040 datapoints for 27 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Jill Sammet</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/sammet.jpg"
                     class="img-polaroid">
                <p>Jill Sammet is a master&#39;s student at CAU Kiel, studying Language &amp; Variation and Computer Science. Her task at Grambank is to code languages.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/JSA" title="Contributed 6250 datapoints for 36 languages and dialects">Contributed 6250 datapoints for 36 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Rhiannon Schembri</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/rhiannon_schembri.jpg"
                     class="img-polaroid">
                <p>Rhiannon Schembri is a Grambank coder from the ANU node in Canberra. She is currently undertaking an undergraduate double degree in Science and Arts, majoring in biology and linguistics. She hopes to pursue research in computational methods for the study of human history in her postgraduate studies.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/RSC" title="Contributed 9106 datapoints for 47 languages and dialects">Contributed 9106 datapoints for 47 languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Lars Schlabbach</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/LS" title="Contributed 975 datapoints for 5 languages and dialects">Contributed 975 datapoints for 5 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Frederick W. P. Schmidt</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/FS" title="Contributed 585 datapoints for 3 languages and dialects">Contributed 585 datapoints for 3 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Dineke Schokkin</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/DS" title="Contributed 195 datapoints for 1 languages and dialects">Contributed 195 datapoints for 1 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Jeff Siegel</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/JSI" title="Contributed 60 datapoints for 1 languages and dialects">Contributed 60 datapoints for 1 languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Jane Simpson</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/JS" title="Contributed  datapoints for  languages and dialects">Contributed  datapoints for  languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Amalia Skilton</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/AS" title="Contributed 1098 datapoints for 21 languages and dialects">Contributed 1098 datapoints for 21 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Hilário de Sousa</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/HDS" title="Contributed 1529 datapoints for 8 languages and dialects">Contributed 1529 datapoints for 8 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Kristin Sverredal</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/KS" title="Contributed 7995 datapoints for 41 languages and dialects">Contributed 7995 datapoints for 41 languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Daniel Valle</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/DV" title="Contributed  datapoints for  languages and dialects">Contributed  datapoints for  languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Javier Vera</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/JVE" title="Contributed 975 datapoints for 5 languages and dialects">Contributed 975 datapoints for 5 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Judith Voß</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/JV" title="Contributed 11045 datapoints for 70 languages and dialects">Contributed 11045 datapoints for 70 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Daniel Wikalier Smith</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/WDS" title="Contributed  datapoints for  languages and dialects">Contributed  datapoints for  languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Tim Witte</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/TWI" title="Contributed 4323 datapoints for 24 languages and dialects">Contributed 4323 datapoints for 24 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Henry Wu</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/henry_wu.jpeg"
                     class="img-polaroid">
                <p>Henry Wu is an undergraduate Linguistics and Sanskrit student at ANU, and is a Grambank coder there. His research interests in linguistics include historical linguistics, language contact, language description and typology. He is currently planning an interdisciplinary project on the history of Chinese Buddhist translation for his honours year.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/HW" title="Contributed 1618 datapoints for 9 languages and dialects">Contributed 1618 datapoints for 9 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Stephanie Yam</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/SY" title="Contributed 1917 datapoints for 11 languages and dialects">Contributed 1917 datapoints for 11 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Jingting Ye 葉婧婷</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/JY" title="Contributed 4885 datapoints for 59 languages and dialects">Contributed 4885 datapoints for 59 languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Maisie Yong</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/maisie_yong.jpg"
                     class="img-polaroid">
                <p>Maisie Yong is a BA Japanese and Linguistic student at SOAS/ELDP, University of London and is a language coder for Grambank. Versed in both Mandarin and English, she codes mostly for Sino-Tibetan languages whose grammars are written in Mandarin. She inadvertently speaks Singlish when exasperated.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/MY" title="Contributed 8262 datapoints for 43 languages and dialects">Contributed 8262 datapoints for 43 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Tessa Yuditha</h5>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/TY" title="Contributed 1412 datapoints for 8 languages and dialects">Contributed 1412 datapoints for 8 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Nicholas Evans</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/nick_evans.jpg"
                     class="img-polaroid">
                <p>Nick Evans is a typologist and anthropological linguist specialising in Australian and Papuan languages. He is an ARC Laureate Professor at the Australian National University and director of the ARC Research Centre for the Dynamics of Language (CoEDL). Within Glottobank he is a member of the Parabank Collective and an Associated Collaborator in Grambank.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/NE" title="Contributed 390 datapoints for 2 languages and dialects">Contributed 390 datapoints for 2 languages and dialects</a>
                </p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Martin Haspelmath</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/martin_haspelmath.png"
                     class="img-polaroid">
                <p>Martin Haspelmath is a senior scientist at MPI-EVA Leipzig and a professor at Leipzig University. He was one of the creators of the World Atlas of Language Structures (2005) and was heavily involved in feature design in the Atlas of Pidgin and Creole Language Structures (2013). He is a senior advisor in the Grambank project.</p>
                <p>
                    <a class="Contributor" href="https://grambank.clld.org/contributors/MH" title="Contributed 467 datapoints for 5 languages and dialects">Contributed 467 datapoints for 5 languages and dialects</a>
                </p>
            </div>
        </td>

    </tr>
    <tr>
        <th colspan="4" id="methodsteam">
            Methods-team
            <a href="#top" title="go to top of the page" style="vertical-align: bottom">&#x21eb;</a>
        </th>
    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Hedvig Skirgård</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/hedvig_skirgard.jpg"
                     class="img-polaroid">
                <p>Hedvig Skirgård is a postdoctoral researcher at DLCE at MPI-EVA in Leipzig. She is the main project coordinator for Grambank. She was previously employed as a coder within the Nijmegen Typological Survey which is the precursor to Grambank. She is also the patron for a set of Grambank features, including features concerning negation and tense &amp; aspect.</p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Hannah J. Haynie</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/hannah_haynie.jpg"
                     class="img-polaroid">
                <p>Hannah Haynie is an Assistant Professor of Linguistics at the University of Colorado. Her research focuses on language diversity and language change, integrating ideas from ecology and biology with rigorous linguistic analysis to answer questions in linguistic typology and diachronic linguistics. She is particularly interested in interactions between language, culture, and the physical environment. Patterns of linguistic diversity in North America have been central to her work to date. Hannah is one of the Grambank questionnaire designers and a &#39;feature patron&#39; for the coding effort.</p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Damián E. Blasi</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Damian.jpg"
                     class="img-polaroid">
                <p>Damián Blasi is a postdoc at the University of Zürich and an external member of the MPI SHH where he uses large-scale typological databases to make inferences on the relevance of non-linguistic factors on linguistic structures, and provides general statistical assistance for Glottobank.</p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Sam Passmore</h5>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Luke Maurits</h5>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Angela Chira</h5>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Annemarie Verkerk</h5>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Olena Shcherbakova</h5>
            </div>
        </td>

    </tr>
    <tr>


        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Benedict King</h5>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Russell Barlow</h5>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Simon J. Greenhill</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/Greenhill.jpeg"
                     class="img-polaroid">
                <p>Simon Greenhill studies how languages evolve using computational methods and large-scale cross-linguistic databases. He is currently a research fellow in the ARC Research Centre for the Dynamics of Language (CoEDL), and at the Max Planck Institute for the Science of Human History. His role in this project is design and analysis of Lexibank and Parabank.</p>
            </div>
        </td>



        <td style="width: 25%; vertical-align: top;">
            <div class="well-small well">
                <h5>Quentin D. Atkinson</h5>
                <img width="150" style="float: left; margin: 0px 15px 15px 0px;" src="https://glottobank.org/photos/quentin_atkinson.jpg"
                     class="img-polaroid">
                <p>Quentin Atkinson is Professor in Psychology at the University of Auckland and co-director of the Language, Culture and Cognition Lab. His research uses computational modeling tools to study the evolution of language and culture. He is co-leader of Glottobank.</p>
            </div>
        </td>

    </tr>
</table>
