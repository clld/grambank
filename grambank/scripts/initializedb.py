from __future__ import unicode_literals, print_function
import sys

from sqlalchemy import func
from clldutils.path import Path
from clldutils.misc import slug
from clld.scripts.util import initializedb, Data
from clld.db.meta import DBSession
from clld.db.models import common
from clld.db.util import compute_language_sources
from clld.scripts.util import bibtex2source
from clld.lib.bibtex import Database
from csvw.dsv import reader

from clld_glottologfamily_plugin.models import Family
from clld_glottologfamily_plugin.util import load_families
from clld_phylogeny_plugin.models import Phylogeny, LanguageTreeLabel, TreeLabel
from pyglottolog.api import Glottolog
from pycldf import StructureDataset

import grambank
from grambank.scripts.util import (
    import_features, import_values, import_languages,
    GLOTTOLOG_REPOS, GRAMBANK_REPOS,
)
from grambank.scripts.global_tree import tree

from grambank.models import Feature, GrambankLanguage, Coder, Grambank


def main(args):  # pragma: no cover
    cldf = StructureDataset.from_metadata(Path(GRAMBANK_REPOS) / 'cldf' / 'StructureDataset-metadata.json')
    data = Data()
    dataset = Grambank(
        id=grambank.__name__,
        name="Grambank",
        description="Grambank",
        publisher_name="Max Planck Institute for the Science of Human History",
        publisher_place="Jena",
        publisher_url="http://shh.mpg.de",
        license="http://creativecommons.org/licenses/by/4.0/",
        domain='grambank.clld.org',
        contact='harald.hammarstrom@gmail.com',
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'})
    for i, row in enumerate(reader(Path(__file__).parent / 'contributors.csv', dicts=True), start=1):
        key = slug(row['first name'] + row['last name'])
        contributor_id = slug(row['last name'] + row['first name'])
        contrib = data.add(
            Coder,
            key,
            id=contributor_id,
            name='{0} {1}'.format(row['first name'], row['last name']))
        common.Editor(dataset=dataset, contributor=contrib, ord=i)

    DBSession.add(dataset)
    glottolog = Glottolog(GLOTTOLOG_REPOS)
    languoids = {l.id: l for l in glottolog.languoids()}

    for rec in Database.from_file(cldf.bibpath, lowercase=True):
        data.add(common.Source, rec.id, _obj=bibtex2source(rec))

    import_features(cldf, data)
    import_languages(cldf, data)
    import_values(cldf, data)
    load_families(
        data,
        data['GrambankLanguage'].values(),
        glottolog_repos=GLOTTOLOG_REPOS,
        isolates_icon='tcccccc')

    # Add isolates
    for lg in data['GrambankLanguage'].values():
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
    return 


def prime_cache(args):  # pragma: no cover
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
    langs = {l.pk: l for l in DBSession.query(GrambankLanguage)}
    features = {f.pk: f for f in DBSession.query(Feature)}

    for lpk, nf in DBSession.query(common.ValueSet.language_pk, func.count(common.ValueSet.pk)) \
            .join(common.Value, common.Value.valueset_pk == common.ValueSet.pk) \
            .filter(common.Value.name != None) \
            .group_by(common.ValueSet.language_pk):
        langs[lpk].representation = nf

    for fpk, nl in DBSession.query(common.ValueSet.parameter_pk, func.count(common.ValueSet.pk))\
            .join(common.Value, common.Value.valueset_pk == common.ValueSet.pk)\
            .filter(common.Value.name != None)\
            .group_by(common.ValueSet.parameter_pk):
        features[fpk].representation = nl

    newick, _ = tree([l.id for l in DBSession.query(common.Language)], GLOTTOLOG_REPOS)
    phylo = Phylogeny(
        id='p',
        name='glottolog global tree',
        newick=newick)
    for l in DBSession.query(common.Language):
        LanguageTreeLabel(
            language=l, treelabel=TreeLabel(id=l.id, name=l.id, phylogeny=phylo))
    DBSession.add(phylo)

    contributors = {c.pk: c for c in DBSession.query(common.Contributor)}
    for cpk, ndp in DBSession.execute("""\
select cc.contributor_pk, count(distinct vs.pk) 
from valueset as vs, contribution as co, contributioncontributor as cc
where vs.contribution_pk = co.pk and co.pk = cc.contribution_pk
group by cc.contributor_pk"""):
        contributors[cpk].count_datapoints = ndp

    compute_language_sources()


if __name__ == '__main__':  # pragma: no cover
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
