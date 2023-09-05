from collections import defaultdict
import itertools
import sys

from sqlalchemy import func
from clld.cliutil import bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
from clld.db.util import compute_language_sources
from clld.web.icon import ORDERED_ICONS
from clld.lib.bibtex import Database
from clld_glottologfamily_plugin.models import Family
from clld_phylogeny_plugin.models import Phylogeny, LanguageTreeLabel, TreeLabel
from pycldf.sources import Sources
from ete3 import Tree

import grambank
from grambank import models


def iter_trees(families):  # pragma: no cover
    for row in families:
        tree = Tree("({0});".format(row['Newick']), format=3)
        tree.name = 'glottolog_{0}'.format(row['ID'])
        yield tree


def main(args):  # pragma: no cover
    cldf = args.cldf
    nsheets = input('Sheets to load [int]: ') or None
    if nsheets:
        nsheets = int(nsheets)

    dataset = models.Grambank(
        id=grambank.__name__,
        name="Grambank",
        description="Grambank",
        publisher_name="Max Planck Institute for Evolutionary Anthropology",
        publisher_place="Leipzig",
        publisher_url="https://www.eva.mpg.de",
        license="http://creativecommons.org/licenses/by/4.0/",
        domain='grambank.clld.org',
        contact='grambank_admin@eva.mpg.de',
        jsondata={
            'faq': cldf.directory.joinpath('FAQ.md').read_text(encoding='utf8'),
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'})
    DBSession.add(dataset)

    DBSession.flush()
    print('adding contributors...', file=sys.stderr)

    photo_url = cldf['contributors.csv', 'Photo'].valueUrl
    contributors = {
        contributor['ID']: common.Contributor(
            id=contributor['ID'],
            name=contributor['Name'],
            description=contributor['Description'],
            url=photo_url.expand(contributor) if contributor['Photo'] else None,
            jsondata=dict(roles=contributor['Roles']))
        for contributor in cldf['contributors.csv']}
    DBSession.add_all(contributors.values())

    DBSession.flush()

    DBSession.add_all(
        common.Editor(
            dataset_pk=dataset.pk,
            contributor_pk=contributor.pk,
            ord=ord)
        for ord, contributor in enumerate(contributors.values()))

    print('done.', file=sys.stderr)
    print('adding sources...', file=sys.stderr)

    sources = {
        rec.id: bibtex2source(rec)
        for rec in Database.from_file(cldf.bibpath, lowercase=True)}
    DBSession.add_all(sources.values())

    print('done.', file=sys.stderr)
    print('adding features and codes...', file=sys.stderr)

    cldf_features = {
        feature['ID']: feature for feature in cldf['ParameterTable']}

    features = {
        feature_id: models.Feature(
            id=feature['ID'],
            name=feature['Name'],
            description=feature['Description'],
        )
        for feature_id, feature in cldf_features.items()}
    DBSession.add_all(features.values())

    DBSession.flush()

    DBSession.add_all(
        models.FeaturePatron(
            ord=ord,
            feature_pk=features[feature_id].pk,
            contributor_pk=contributors[patron].pk)
        for feature_id, feature in cldf_features.items()
        for ord, patron in enumerate(feature['Patrons'], start=1))

    cldf_codes = {}
    for fid, des in itertools.groupby(
        sorted(cldf['CodeTable'], key=lambda c: c['Parameter_ID']),
        lambda c: c['Parameter_ID']
    ):
        cldf_codes[fid] = list(des) + [dict(ID=fid + '-NA', Name='?', Description='Not known')]

    # ? = gray cbbbbbb (is ? mapped? if not then don't worry)
    # 0 = blue c0077bb
    # 1 = red ccc3311
    # 2 = teal c009988
    # 3 = orange cee7733
    icons = {
        '?': 'cffffff',
        '0': 'c009E73',  # 'c00ffff',
        '1': 'cF0E442',  # 'c593d9c',
        '2': 'c0072B2',  # 'cf68f46',
        '3': 'cD55E00',  # 'c73d055',
    }
    codes = {
        cldf_code['ID']: common.DomainElement(
            id=cldf_code['ID'],
            parameter_pk=features[feature_id].pk,
            name=(value := cldf_code['Name']),
            number=int(value) if value != '?' else 999,
            description=cldf_code['Description'],
            jsondata=dict(icon=icons[value] if value != '?' else 'tcccccc')
        )
        for feature_id, codes in cldf_codes.items()
        for cldf_code in codes}
    DBSession.add_all(codes.values())

    print('done.', file=sys.stderr)
    print('adding languages and families...', file=sys.stderr)

    cldf_languages = {
        cldf_language['ID']: cldf_language
        for cldf_language in cldf['LanguageTable']}
    cldf_families = {
        family_id: cldf_language['Family_name']
        for cldf_language in cldf_languages.values()
        if (family_id := cldf_language.get('Family_level_ID'))}

    # sorting family ids to make the icon colours idempotent
    family_glottocodes = sorted(cldf_families)

    glottocodes = {
        language_id: common.Identifier(
            id=language_id,
            name=language_id,
            type=common.IdentifierType.glottolog.value)
        for language_id in itertools.chain(cldf_languages, family_glottocodes)}
    DBSession.add_all(glottocodes.values())

    isocodes = {
        language_id: common.Identifier(
            id=isocode,
            name=isocode,
            type=common.IdentifierType.iso.value)
        for language_id, cldf_language in cldf_languages.items()
        if (isocode := cldf_language.get('ISO639P3code'))}
    DBSession.add_all(isocodes.values())

    DBSession.flush()

    family_icons = itertools.cycle([
        getattr(i, 'name', i)
        for i in ORDERED_ICONS
        if getattr(i, 'name', i) != 'dcccccc'])
    families_proper = {
        family_id: Family(
            id=family_id,
            name=cldf_families[family_id],
            description=glottocodes[family_id].url(),
            jsondata={'icon': next(family_icons)})
        for family_id in family_glottocodes}
    DBSession.add_all(families_proper.values())

    isolate_families = {
        language_id: Family(
            id=language_id,
            name=cldf_languages[language_id]['Name'],
            description=glottocodes[language_id].url(),
            jsondata={'icon': 'dcccccc'})
        for language_id, cldf_language in cldf_languages.items()
        if not cldf_languages.get('Family_level_ID')}
    DBSession.add_all(isolate_families.values())

    DBSession.flush()

    languages = {
        language_id: models.GrambankLanguage(
            id=language_id,
            name=cldf_language['Name'],
            macroarea=cldf_language['Macroarea'],
            latitude=cldf_language['Latitude'],
            longitude=cldf_language['Longitude'],
            family_pk=(
                families_proper.get(cldf_language.get('Family_level_ID'))
                or isolate_families[language_id]).pk)
        for language_id, cldf_language in cldf_languages.items()}
    DBSession.add_all(languages.values())

    DBSession.flush()

    contributions = {
        language_id: common.Contribution(
            id=language_id,
            name='Dataset for {0}'.format(language.name))
        for language_id, language in languages.items()}
    DBSession.add_all(contributions.values())

    DBSession.flush()

    DBSession.add_all(
        common.LanguageIdentifier(
            language_pk=language.pk,
            identifier_pk=identifier.pk)
        for language in languages.values()
        if (identifier := glottocodes.get(language.id)))
    DBSession.add_all(
        common.LanguageIdentifier(
            language_pk=language.pk,
            identifier_pk=identifier.pk)
        for language in languages.values()
        if (identifier := isocodes.get(language.id)))

    print('done.', file=sys.stderr)
    print('loading cldf values...', file=sys.stderr)

    def _limit_sheets(nsheets, values):
        if nsheets is None:
            return values
        else:
            subset = set(itertools.islice(languages, nsheets))
            return (val for val in values if val['Language_ID'] in subset)

    cldf_values = list(_limit_sheets(nsheets, cldf['ValueTable']))
    print('done.', file=sys.stderr)

    print('adding value sets...', file=sys.stderr)
    valuesets = {
        (value['Language_ID'], value['Parameter_ID']): models.Datapoint(
            id=value['ID'],
            parameter_pk=features[value['Parameter_ID']].pk,
            language_pk=languages[value['Language_ID']].pk,
            contribution_pk=contributions[value['Language_ID']].pk,
            source=value['Source_comment'] if not value['Source'] else None)
        for value in cldf_values}
    DBSession.add_all(valuesets.values())

    DBSession.flush()

    print('done.', file=sys.stderr)
    print('adding values...', file=sys.stderr)

    DBSession.add_all(
        common.Value(
            id=value['ID'],
            valueset_pk=valuesets[value['Language_ID'], value['Parameter_ID']].pk,
            name=value['Value'] if value['Value'] else '?',
            description=value['Comment'],
            domainelement_pk=codes[value['Code_ID'] or '{}-NA'.format(value['Parameter_ID'])].pk)
        for value in cldf_values)

    DBSession.flush()

    print('done.', file=sys.stderr)
    print('adding coders and source refs...', file=sys.stderr)

    coders_by_language = {}
    for value in cldf_values:
        language_id = value['Language_ID']
        if language_id not in coders_by_language:
            coders_by_language[language_id] = list(
                cldf_languages[language_id].get('Coders') or ())
        coders = coders_by_language[language_id]
        coders.extend(coder for coder in value['Coders'] if coder not in coders)
    DBSession.add_all(
        common.ContributionContributor(
            contribution_pk=contributions[language_id].pk,
            contributor_pk=contributors[contributor_id].pk,
            ord=ord)
        for language_id, coders in coders_by_language.items()
        for ord, contributor_id in enumerate(coders, start=1))

    datapoint_coders = (
        (
            value['Language_ID'],
            value['Parameter_ID'],
            set(cldf_languages[value['Language_ID']].get('Coders') or ()).union(
                value['Coders']),
        )
        for value in cldf_values)
    DBSession.add_all(
        models.DatapointContributor(
            datapoint_pk=valuesets[language_id, parameter_id].pk,
            contributor_pk=contributors[coder_id].pk)
        for language_id, parameter_id, coders in datapoint_coders
        for coder_id in coders)

    value_sources = (
        (value['Language_ID'], value['Parameter_ID'], Sources.parse(ref))
        for value in cldf_values
        for ref in value.get('Source', ()))
    DBSession.add_all(
        common.ValueSetReference(
            valueset_pk=valuesets[language_id, feature_id].pk,
            source_pk=sources[sid].pk,
            description=pages)
        for language_id, feature_id, (sid, pages) in value_sources)

    print('done.', file=sys.stderr)


def prime_cache(args):  # pragma: no cover
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
    print('counting things...', file=sys.stderr)

    langs = {l.pk: l for l in DBSession.query(models.GrambankLanguage)}
    features = {f.pk: f for f in DBSession.query(models.Feature)}

    for lpk, nf in DBSession.query(common.ValueSet.language_pk, func.count(common.ValueSet.pk)) \
            .join(common.Value, common.Value.valueset_pk == common.ValueSet.pk) \
            .group_by(common.ValueSet.language_pk):
        langs[lpk].representation = nf

    for lpk, nf in DBSession.query(common.ValueSet.language_pk, func.count(common.ValueSet.pk)) \
            .join(common.Value, common.Value.valueset_pk == common.ValueSet.pk) \
            .filter(common.Value.name != '?') \
            .group_by(common.ValueSet.language_pk):
        langs[lpk].nzrepresentation = nf

    for fpk, nl in DBSession.query(common.ValueSet.parameter_pk, func.count(common.ValueSet.pk)) \
            .join(common.Value, common.Value.valueset_pk == common.ValueSet.pk) \
            .group_by(common.ValueSet.parameter_pk):
        features[fpk].representation = nl

    for fpk, nl in DBSession.query(common.ValueSet.parameter_pk, func.count(common.ValueSet.pk))\
            .join(common.Value, common.Value.valueset_pk == common.ValueSet.pk) \
            .filter(common.Value.name != '?') \
            .group_by(common.ValueSet.parameter_pk):
        features[fpk].nzrepresentation = nl

    print('done.', file=sys.stderr)
    print('connecting sources to languages...', file=sys.stderr)

    compute_language_sources()

    print('done.', file=sys.stderr)
    print('cleaning up old tree information if any...', file=sys.stderr)

    for obj in DBSession.query(LanguageTreeLabel).all():
        DBSession.delete(obj)
    for obj in DBSession.query(TreeLabel).all():
        DBSession.delete(obj)
    for obj in DBSession.query(Phylogeny).all():
        DBSession.delete(obj)

    DBSession.flush()

    print('done.', file=sys.stderr)
    print('computing language tree...', file=sys.stderr)

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
