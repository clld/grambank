import itertools

from tqdm import tqdm
from pycldf.sources import Sources

from clld.db.meta import DBSession
from clld.db.models.common import (
    ValueSet, Value, DomainElement, ValueSetReference, ContributionContributor, Contribution,
)

from grambank.models import GrambankLanguage, Feature, FeaturePatron, Datapoint, DatapointContributor


def import_values(values, lang, features, codes, contributors, sources):  # pragma: no cover
    c = Contribution(
        id=lang['ID'],
        name='Dataset for {0}'.format(lang['Name']),
    )
    coders = lang['Coders'][:]
    l = GrambankLanguage(
        id=lang['ID'],
        name=lang['Name'],
        macroarea=lang['Macroarea'],
        latitude=lang['Latitude'],
        longitude=lang['Longitude'],
    )
    for value in values:
        vs = Datapoint(
            id=value['ID'],
            parameter_pk=features[value['Parameter_ID']],
            language=l,
            contribution=c,
            source=value['Source_comment'] if not value['Source'] else None,
        )
        Value(
            id=value['ID'],
            valueset=vs,
            name=value['Value'] if value['Value'] else '?',
            description=value['Comment'],
            domainelement_pk=codes[value['Code_ID'] or '{}-NA'.format(value['Parameter_ID'])])
        for cid in set(lang['Coders']).union(value['Coders']):
            DBSession.add(DatapointContributor(datapoint=vs, contributor_pk=contributors[cid]))
        for cid in value['Coders']:
            if cid not in coders:
                coders.append(cid)

        if value['Source']:
            for ref in value['Source']:
                sid, pages = Sources.parse(ref)
                ValueSetReference(valueset=vs, source_pk=sources[sid], description=pages)
    for i, cid in enumerate(coders, start=1):
        DBSession.add(ContributionContributor(
            contribution=c,
            contributor_pk=contributors[cid],
            ord=i,
        ))
    DBSession.add(l)
    DBSession.add(c)


def import_features(cldf, contributors):  # pragma: no cover
    """
    ? = gray cbbbbbb (is ? mapped? if not then don't worry)
    0 = blue c0077bb
    1 = red ccc3311
    2 = teal c009988
    3 = orange cee7733
    """
    features, codes = {}, {}
    icons = [
        'cffffff',  # 'c0077bb'
        'cff0000',  # 'ccc3311'
        'c0000ff',  # 'c009988'
        'cffff00',  # 'cee7733'
    ]
    domains = {}
    for fid, des in itertools.groupby(
            sorted(cldf['CodeTable'], key=lambda c: c['Parameter_ID']),
            lambda c: c['Parameter_ID']):
        domains[fid] = list(des) + [dict(ID=fid + '-NA', Name='?', Description='Not known')]

    for feature in cldf['ParameterTable']:
        fid = feature['ID']
        f = Feature(
            id=fid,
            name=feature['Name'],
            description=feature['Description'],
        )
        for ord, patron in enumerate(feature['Patrons'], start=1):
            DBSession.add(FeaturePatron(ord=1, feature=f, contributor_pk=contributors[patron]))
        for code in domains[fid]:
            if code['Name'] == '?':
                icon, number, value = 'tcccccc', 999, None
            else:
                icon, number, value = icons[int(code['Name'])], int(code['Name']), code['Name']
            DomainElement(
                id=code['ID'],
                parameter=f,
                name=code['Name'],
                number=number,
                description=code['Description'],
                jsondata=dict(icon=icon)
            )
        DBSession.add(f)
        DBSession.flush()
        features[fid] = f.pk
        for de in f.domain:
            codes[de.id] = de.pk

    return features, codes
