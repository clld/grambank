import itertools

from tqdm import tqdm

from clld.db.meta import DBSession
from clld.db.models.common import (
    ValueSet, Value, DomainElement, ValueSetReference, ContributionContributor, Contribution,
)

from grambank.models import GrambankLanguage, Feature


def import_languages(cldf, data):  # pragma: no cover
    for lang in tqdm(list(cldf['LanguageTable']), desc='loading languages'):
        lname = '{0} [{1}]'.format(lang['Name'], lang['ID'])
        c = data.add(
            Contribution,
            lang['ID'],
            id=lang['ID'],
            name='Dataset for {0}'.format(lname),
        )
        for i, cid in enumerate(lang['Coders'], start=1):
            DBSession.add(ContributionContributor(
                contribution=c,
                contributor=data['Contributor'][cid],
                ord=i,
            ))
        data.add(
            GrambankLanguage,
            lang['ID'],
            id=lang['ID'],
            name=lname,
            macroarea=lang['Macroarea'],
            latitude=lang['Latitude'],
            longitude=lang['Longitude'],
        )


def import_values(cldf, data):  # pragma: no cover
    for value in tqdm(list(cldf['ValueTable']), desc='loading values'):
        vs = data.add(
            ValueSet, value['ID'],
            id=value['ID'],
            parameter=data['Feature'][value['Parameter_ID']],
            language=data['GrambankLanguage'][value['Language_ID']],
            contribution=data['Contribution'][value['Language_ID']],
        )
        data.add(
            Value,
            value['ID'],
            id=value['ID'],
            valueset=vs,
            name=value['Value'],
            description=value['Comment'],
            domainelement=data['DomainElement'][value['Parameter_ID'], value['Value']])

        if value['Source']:
            for ref in value['Source']:
                sid, pages = cldf.sources.parse(ref)
                ValueSetReference(valueset=vs, source=data['Source'][sid], description=pages)


def import_features(cldf, data):  # pragma: no cover
    icons = [
        'cffffff',
        'cff0000',
        'c0000ff',
        'cffff00',
    ]
    patrons = {
        'Alena': 'AWM',
        'Hannah': 'HJH',
        'Harald': 'HH',
        'Hedvig': 'HS',
        'Jakob': 'JLE',
        'Jeremy': 'JC',
    }
    domains = {}
    for fid, codes in itertools.groupby(
            sorted(cldf['CodeTable'], key=lambda c: c['Parameter_ID']),
            lambda c: c['Parameter_ID']):
        domains[fid] = list(codes) + [dict(ID=fid + '-NA', Name='?', Description='Not known')]

    for feature in tqdm(list(cldf['ParameterTable']), desc='loading features'):
        fid = feature['ID']
        f = data.add(
            Feature,
            fid,
            id=fid,
            name=feature['Name'],
            description=feature['Description'],
            patron=data['Contributor'][patrons[feature['patron']]],
            name_french=feature['name_in_french'],
        )
        for code in domains[fid]:
            if code['Name'] == '?':
                icon, number, value = 'tcccccc', 999, None
            else:
                icon, number, value = icons[int(code['Name'])], int(code['Name']), code['Name']
            data.add(
                DomainElement,
                (fid, value),
                id=code['ID'],
                parameter=f,
                name=code['Name'],
                number=number,
                description=code['Description'],
                jsondata=dict(icon=icon))
