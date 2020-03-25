from sqlalchemy import func
from clld.scripts.util import Data
from clld.db.meta import DBSession
from clld.db.models import common
from clld.db.util import compute_language_sources
from clld.scripts.util import bibtex2source
from clld.lib.bibtex import Database

from clld_glottologfamily_plugin.models import Family
from clld_glottologfamily_plugin.util import load_families
from clld_phylogeny_plugin.models import Phylogeny, LanguageTreeLabel, TreeLabel
from pyglottolog.api import Glottolog
from pycldf import StructureDataset
from pygrambank import Grambank

import grambank
from grambank.scripts.util import import_features, import_values, import_languages
from grambank.scripts.global_tree import tree

from grambank import models


def main(args):  # pragma: no cover
    api = Grambank(args.Grambank)
    cldf = StructureDataset.from_metadata(
        args.grambank_cldf / 'cldf' / 'StructureDataset-metadata.json')
    data = Data()
    dataset = models.Grambank(
        id=grambank.__name__,
        name="Grambank",
        description="Grambank",
        publisher_name="Max Planck Institute for the Science of Human History",
        publisher_place="Jena",
        publisher_url="https://shh.mpg.de",
        license="http://creativecommons.org/licenses/by/4.0/",
        domain='grambank.clld.org',
        contact='grambank@shh.mpg.de',
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'})
    for i, contrib in enumerate(api.contributors):
        contrib = data.add(
            common.Contributor,
            contrib.id,
            id=contrib.id,
            name=contrib.name,
        )
        common.Editor(dataset=dataset, contributor=contrib, ord=i)

    DBSession.add(dataset)
    glottolog = Glottolog(args.glottolog)
    languoids = {l.id: l for l in glottolog.languoids()}

    for rec in Database.from_file(cldf.bibpath, lowercase=True):
        data.add(common.Source, rec.id, _obj=bibtex2source(rec))

    import_features(cldf, data)
    import_languages(cldf, data)
    import_values(cldf, data)
    load_families(
        data,
        data['GrambankLanguage'].values(),
        glottolog_repos=args.glottolog,
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
    langs = {l.pk: l for l in DBSession.query(models.GrambankLanguage)}
    features = {f.pk: f for f in DBSession.query(models.Feature)}

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

    newick, _ = tree([l.id for l in DBSession.query(common.Language)], args.glottolog)
    phylo = Phylogeny(
        id='p',
        name='glottolog global tree',
        newick=newick)
    for l in DBSession.query(common.Language):
        LanguageTreeLabel(
            language=l, treelabel=TreeLabel(id=l.id, name=l.id, phylogeny=phylo))
    DBSession.add(phylo)

    compute_language_sources()
