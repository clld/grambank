import pathlib
import itertools

import transaction
from tqdm import tqdm
from sqlalchemy import func
from clld.cliutil import Data, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
from clld.db.util import compute_language_sources
from clld.lib.bibtex import Database

from clld_glottologfamily_plugin.models import Family
from clld_glottologfamily_plugin.util import load_families
from clld_phylogeny_plugin.models import Phylogeny, LanguageTreeLabel, TreeLabel
from pyglottolog.api import Glottolog
from pycldf import StructureDataset
from pygrambank import Grambank

import grambank
from grambank.scripts.util import import_features, import_values
from grambank.scripts.global_tree import tree
from grambank.scripts import coverage

from grambank import models


PROJECT_DIR = pathlib.Path(grambank.__file__).parent.parent.resolve()
REPOS = {'Grambank': None, 'grambank-cldf': None, 'glottolog/glottolog': None}


def main(args):  # pragma: no cover
    for repo in list(REPOS.keys()):
        d = PROJECT_DIR.parent
        if '/' in repo:
            d = d.parent
            repo = repo.split('/', maxsplit=1)
        else:
            repo = [repo]
        d = d.joinpath(*repo)
        REPOS[repo[-1]] = pathlib.Path(input('{} [{}]: '.format(repo[-1], d)) or d)

    api = Grambank(REPOS['Grambank'])
    cldf = StructureDataset.from_metadata(
        REPOS['grambank-cldf'] / 'cldf' / 'StructureDataset-metadata.json')
    data = Data()
    dataset = models.Grambank(
        id=grambank.__name__,
        name="Grambank",
        description="Grambank",
        publisher_name="Max Planck Institute for Evolutionary Anthropology",
        publisher_place="Leipzig",
        publisher_url="https://www.eva.mpg.de",
        license="http://creativecommons.org/licenses/by/4.0/",
        domain='grambank.clld.org',
        contact='grambank@shh.mpg.de',
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'})
    contributors = {}
    for i, contrib in enumerate(api.contributors):
        contrib = common.Contributor(
            contrib.id,
            id=contrib.id,
            name=contrib.name,
        )
        common.Editor(dataset=dataset, contributor=contrib, ord=i)
        DBSession.add(contrib)
        DBSession.flush()
        contributors[contrib.id] = contrib.pk
    contributions = {r['ID']: r for r in cldf['LanguageTable']}

    DBSession.add(dataset)

    for rec in tqdm(list(Database.from_file(cldf.bibpath, lowercase=True)), desc='sources'):
        data.add(common.Source, rec.id, _obj=bibtex2source(rec))
    DBSession.flush()
    sources = {k: v.pk for k, v in data['Source'].items()}

    features, codes = import_features(cldf, contributors)
    transaction.commit()

    values_by_sheet = [(lid, list(v)) for lid, v in itertools.groupby(
        sorted(cldf['ValueTable'], key=lambda r: r['Language_ID']),
        lambda r: r['Language_ID'],
    )]
    for lid, values in tqdm(values_by_sheet, desc='loading values'):
        transaction.begin()
        import_values(values, contributions[lid], features, codes, contributors, sources)
        transaction.commit()

    transaction.begin()

    glottolog = Glottolog(REPOS['glottolog'])
    languoids = {l.id: l for l in glottolog.languoids()}
    gblangs = DBSession.query(models.GrambankLanguage).all()
    load_families(
        data,
        gblangs,
        glottolog_repos=REPOS['glottolog'],
        isolates_icon='dcccccc')

    # Add isolates
    for lg in gblangs:
        gl_language = languoids.get(lg.id)
        if not gl_language.family:
            family = data.add(
                Family, gl_language.id,
                id=gl_language.id,
                name=gl_language.name,
                description=common.Identifier(
                    name=gl_language.id,
                    type=common.IdentifierType.glottolog.value).url(),
                jsondata={"icon": 'tcccccc'})
            lg.family = family
    coverage.main(glottolog)
    return


def prime_cache(args):  # pragma: no cover
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
    langs = {l.pk: l for l in DBSession.query(models.GrambankLanguage)}
    features = {f.pk: f for f in DBSession.query(models.Feature)}

    for lpk, nf in DBSession.query(common.ValueSet.language_pk, func.count(common.ValueSet.pk)) \
            .join(common.Value, common.Value.valueset_pk == common.ValueSet.pk) \
            .group_by(common.ValueSet.language_pk):
        langs[lpk].representation = nf

    for fpk, nl in DBSession.query(common.ValueSet.parameter_pk, func.count(common.ValueSet.pk))\
            .join(common.Value, common.Value.valueset_pk == common.ValueSet.pk)\
            .group_by(common.ValueSet.parameter_pk):
        features[fpk].representation = nl

    compute_language_sources()

    return
    newick, _ = tree([l.id for l in DBSession.query(common.Language)], args.glottolog)
    phylo = Phylogeny(
        id='p',
        name='glottolog global tree',
        newick=newick)
    for l in DBSession.query(common.Language):
        LanguageTreeLabel(
            language=l, treelabel=TreeLabel(id=l.id, name=l.id, phylogeny=phylo))
    DBSession.add(phylo)

