<%inherit file="grambank.mako"/>

<h2>Functionalities of the web browser-interface</h2>

<p>
  Grambank is a database that is available in a web browser interface
  (grambank.clld.org) and also as a CLDF-dataset archived with
  ${h.external_link('https://zenodo.org/record/7844558', 'Zenodo')}
  and released on
  ${h.external_link('https://github.com/grambank/grambank/releases', 'GitHub')}.
  The web browser interface is built on the CLLD framework.
</p>

<h3>Menus</h3>

<p>
  <img
    alt="Screenshot 2023-10-06 at 12 59 39"
    src="${request.static_url('grambank:static/screenshot-menu.png')}" />
</p>

<p>
  There are two horizontal menu bars. The top one contains tabs for information
  about the dataset. The bottom one is a sub-menu to the tab "home" on the first
  menu.
</p>

<h3>Visualizing feature values on a map</h3>

<p>
  Click the tab "Features" in the top menu. Select a feature. Scroll down to the
  heading "map".
</p>

<h3>Combining features</h3>

<p>
  Click the tab "Features" in the top menu. Select a feature. Scroll down to
  a section with the sentence <em>You may combine this variable with a different
  variable by selecting on in the list below and clicking "Submit".</em>
</p>

<p>
  Once you click "Submit", you will be taken to a new webpage with a map and
  table illustrating the combination of the features you selected. The URL will
  contain the Feature ID numbers, for example
  <a href="${request.route_url('combination', id='GB020_GB023')}">${request.route_url('combination', id='GB020_GB023')}</a>.
  If you add further Feature ID numbers to this URL, they will also be included,
  for example
  <a href="${request.route_url('combination', id='GB020_GB023_GB058')}">${request.route_url('combination', id='GB020_GB023_GB058')}</a>.
</p>

<h3>Visualizing feature values on a language family tree</h3>

<p>
  Go to the tab "Languages and dialects" in the top menu. Click on the language
  family in the column "Family". At the top of the page, there is a section
  where you can select a feature. Once you click "Submit", you will be taken to
  a page showing that feature for that language family in a map and if you
  scroll down also on a tree, see example
  <a href="${request.route_url('familys', 'aust1307', _anchor='tree-container', _query={'feature': 'GB020'})}">here</a>.
  The URL will specify the language family glottocode and Grambank feature ID,
  you can share this URL to send others to the page.
</p>

<h3>Further functionalities, such as comparing languages, other kinds of plotting, combining datasets, etc</h3>

<p>
  The web browser interface for Grambank is just providing basic access to the
  dataset. For further visualizations and analysis, we suggest you
  <a href="${request.route_url('download')}">download</a> the dataset and
  access it through python/R/spreadsheet programs etc. For advice on using
  R with Grambank, go
  ${h.external_link('https://github.com/grambank/grambank/wiki/Fetching-and-analysing-Grambank-data-with-R', 'here')}.
</p>

<h3>General info</h3>

<h4>Versions and citing</h4>

<p>
  The dataset is released in versions, with additions and revisions each time.
  If you use the dataset, please note clearly what version is used. Please see
  our instructions
  ${h.external_link('https://github.com/grambank/grambank/wiki/Citing-grambank', 'here')}
  for citing Grambank.
</p>

<h4>Suggesting changes/additions</h4>

<p>
  Please go
  ${h.external_link('https://github.com/grambank/grambank/wiki/Contribute', 'here')}
  for instructions on suggesting changes or additions.
</p>

<h4>Practical information for users (including R-scripts, SQL etc)</h4> 

<p>
  Please see the wiki articles
  ${h.external_link('https://github.com/grambank/grambank/wiki#2-practical-information-for-users-and-collaborators', 'here')}.
</p>
