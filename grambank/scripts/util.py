from __future__ import unicode_literals
import re
import getpass
from itertools import groupby

from nameparser import HumanName

from clldutils.misc import slug
from clldutils.path import Path

from clld.db.meta import DBSession
from clld.db.models.common import (
    ValueSet, Value, DomainElement, Source, ValueSetReference,
    ContributionContributor, Contributor, Contribution,
)

import grambank
from grambank.models import GrambankLanguage, Feature, Coder


GRAMBANK_REPOS = 'C:\\Python27\\glottobank\\grambank-cldf\\' \
    if getpass.getuser() not in ['forkel@shh.mpg.de'] \
    else '/home/forkel/venvs/grambank/grambank-cldf'
GLOTTOLOG_REPOS = Path(grambank.__file__).parent.parent.parent.parent.joinpath(
    'glottolog', 'glottolog') \
    if getpass.getuser() in ['forkel@shh.mpg.de'] \
    else Path('C:\\Python27\\glottolog\\')  # add your path to the glottolog repos clone here!


def import_languages(cldf, data):  # pragma: no cover
    for lang in cldf['LanguageTable']:
        lname = '{0} [{1}]'.format(lang['Name'], lang['ID'])
        contrib = data.add(
            Contribution,
            lang['ID'],
            id=lang['ID'],
            name=lname,
        )
        for name in re.split(',|\s+and\s+', lang['contributed_datapoints']):
            contributor_name = HumanName(name.strip())
            key = slug('{0}'.format(contributor_name))
            contributor_id = slug(contributor_name.middle + contributor_name.last + contributor_name.first)
            contributor = data['Coder'].get(key)
            if not contributor:
                contributor = data.add(
                    Coder,
                    key,
                    id=contributor_id,
                    name='%s' % contributor_name)
            DBSession.add(
                ContributionContributor(contribution=contrib, contributor=contributor))
        data.add(
            GrambankLanguage,
            lang['ID'],
            id=lang['ID'],
            name=lname,
            macroarea=lang['Macroarea'],
            latitude=lang['Latitude'],
            longitude=lang['Longitude'],
            contribution=contrib,
        )


def import_values(cldf, data):  # pragma: no cover
    for value in cldf['ValueTable']:
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
    domains = {}
    for fid, codes in groupby(
            sorted(cldf['CodeTable'], key=lambda c: c['Parameter_ID']),
            lambda c: c['Parameter_ID']):
        domains[fid] = list(codes) + [dict(ID=fid + '-NA', Name='?', Description='Not known')]

    for feature in cldf['ParameterTable']:
        fid = feature['ID']
        f = data.add(
            Feature,
            fid,
            id=fid,
            name=feature['Name'],
            description=feature['Description'],
            patron=feature['patron'],
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
