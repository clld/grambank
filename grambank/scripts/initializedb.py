import itertools

import transaction
from tqdm import tqdm
from sqlalchemy import func
from clld.cliutil import Data, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
from clld.db.util import compute_language_sources
from clld.web.icon import ORDERED_ICONS
from clld.lib.bibtex import Database
from clld_glottologfamily_plugin.models import Family
from clld_phylogeny_plugin.models import Phylogeny, LanguageTreeLabel, TreeLabel
from ete3 import Tree

import grambank
from grambank.scripts.util import import_features, import_values

from grambank import models


def iter_trees(families):  # pragma: no cover
    for row in families:
        tree = Tree("({0});".format(row['Newick']), format=3)
        tree.name = 'glottolog_{0}'.format(row['ID'])
        yield tree


def main(args):  # pragma: no cover
    cldf = args.cldf
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
    for i, contrib in enumerate(cldf['contributors.csv']):
        contrib = common.Contributor(contrib['ID'], id=contrib['ID'], name=contrib['Name'])
        common.Editor(dataset=dataset, contributor=contrib, ord=i)
        DBSession.add(contrib)
        DBSession.flush()
        contributors[contrib.id] = contrib.pk
    contributions = {r['ID']: r for r in cldf['LanguageTable']}

    DBSession.add(dataset)

    for rec in list(Database.from_file(cldf.bibpath, lowercase=True)):
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
    icons = itertools.cycle(
        [getattr(i, 'name', i) for i in ORDERED_ICONS if getattr(i, 'name', i) != 'dcccccc'])
    gblangs = {l.id: l for l in DBSession.query(models.GrambankLanguage).all()}
    for (fid, fname), langs in itertools.groupby(
            sorted(args.cldf['LanguageTable'], key=lambda l: l['Family_level_ID'] or ''),
            lambda l: (l['Family_level_ID'], l['Family_name']),
    ):
        if fid:
            family = data.add(
                Family, fid,
                    id=fid,
                    name=fname,
                    description=common.Identifier(
                        name=fid, type=common.IdentifierType.glottolog.value).url(),
                    jsondata=dict(icon=next(icons)))
            for l in langs:
                if l['ID'] not in gblangs:
                    print('skipping languoid with no values: {}'.format(l['ID']))
                    continue
                gblangs[l['ID']].family = family
        else:
            # Add isolates
            for l in langs:
                if l['ID'] not in gblangs:
                    print('skipping languoid with no values: {}'.format(l['ID']))
                    continue
                family = data.add(
                    Family, l['ID'],
                        id=l['ID'],
                        name=l['Name'],
                        description=common.Identifier(
                            name=l['ID'], type=common.IdentifierType.glottolog.value).url(),
                        jsondata={"icon": 'dcccccc'})
                gblangs[l['ID']].family = family


def prime_cache(args):  # pragma: no cover
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
    if 1:
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

    for obj in DBSession.query(LanguageTreeLabel).all():
        DBSession.delete(obj)
    for obj in DBSession.query(TreeLabel).all():
        DBSession.delete(obj)
    for obj in DBSession.query(Phylogeny).all():
        DBSession.delete(obj)
    DBSession.flush()

    for tree in iter_trees(list(args.cldf['families.csv'])):
        nodes = set(n.name for n in tree.traverse())
        phylo = Phylogeny(
            id=tree.name.split('_')[1],
            name=tree.name,
            newick=tree.write(format=9))
        for l in DBSession.query(common.Language).filter(common.Language.id.in_(nodes)):
            LanguageTreeLabel(
                language=l, treelabel=TreeLabel(id=l.id, name=l.id, phylogeny=phylo))
        DBSession.add(phylo)
