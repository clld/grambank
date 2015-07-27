from __future__ import unicode_literals
import os
import re
from collections import OrderedDict
import json

from clld.db.models.common import (
    Parameter, ValueSet, Value, Contribution, DomainElement, Source, ValueSetReference,
)
from clld.lib.dsv import reader
from clld.lib.bibtex import Database
from clld.web.icon import ORDERED_ICONS
from clld.scripts.util import bibtex2source
from clld_glottologfamily_plugin.util import load_families

from grambank.models import GrambankLanguage


def import_dataset(path, data):
    # look for metadata
    # look for sources
    # then loop over values
    dirpath, fname = os.path.split(path)
    basename, ext = os.path.splitext(fname)

    contrib = Contribution(id=basename, name=basename)

    md = {}
    mdpath = path + '-metadata.json'
    if os.path.exists(mdpath):
        with open(mdpath, 'rb') as fp:
            md = json.load(fp)

    bibpath = os.path.join(dirpath, basename + '.bib')
    if os.path.exists(bibpath):
        for rec in Database.from_file(bibpath):
            if rec['key'] not in data['Source']:
                data.add(Source, rec['key'], _obj=bibtex2source(rec))

    languages = {f['properties']['glottocode']: f for f in md.get('features', [])}

    for i, row in enumerate(reader(path, dicts=True, delimiter=',' if 'c' in ext else '\t')):
        if not row['Value']:
            continue
        vsid = '%s-%s-%s' % (basename, row['Language_ID'], row['Feature_ID'])
        vid = row.get('ID', '%s-%s' % (basename, i + 1))
        language = data['GrambankLanguage'].get(row['Language_ID'])
        if language is None:
            kw = {'id': row['Language_ID'], 'name': row['Language_ID']}
            lmd = languages.get(row['Language_ID'])
            if lmd:
                if lmd.get('properties', {}).get('name'):
                    kw['name'] = lmd['properties']['name']
                if lmd.get('geometry', {}).get('coordinates'):
                    kw['longitude'], kw['latitude'] = lmd['geometry']['coordinates']

            language = data.add(GrambankLanguage, row['Language_ID'], **kw)

        parameter = data['Parameter'].get(row['Feature_ID'])
        if parameter is None:
            parameter = data.add(
                Parameter, row['Feature_ID'],
                id=row['Feature_ID'],
                name=row.get('Feature', row['Feature_ID']))

        vs = data['ValueSet'].get(vsid)
        if vs is None:
            vs = data.add(
                ValueSet, vsid,
                id=vsid,
                parameter=parameter,
                language=language,
                contribution=contrib,
                source=row['Source'])

        domain = {de.abbr: de for de in parameter.domain}
        name = row['Value']
        if name in domain:
            name = domain[name].name

        Value(
            id=vid,
            valueset=vs,
            name=name,
            description=row['Comment'],
            domainelement=domain.get(row['Value']))

        for key, src in data['Source'].items():
            if key in vs.source:
                ValueSetReference(valueset=vs, source=src, key=key)


def import_cldf(srcdir, data):
    # loop over values
    # check if language needs to be inserted
    # check if feature needs to be inserted
    # add value if in domain
    for dirpath, dnames, fnames in os.walk(srcdir):
        for fname in fnames:
            if os.path.splitext(fname)[1] in ['.tsv', '.csv']:
                try:
                    import_dataset(os.path.join(dirpath, fname), data)
                except:
                    print os.path.join(dirpath, fname)
                    raise
    load_families(data, data['GrambankLanguage'].values())


class FeatureSpec(object):
    @staticmethod
    def yield_domainelements(s):
        try:
            for m in re.split('\s*,|;\s*', re.sub('^multistate\s+', '', s.strip())):
                if m.strip():
                    if m.startswith('As many'):
                        for i in range(100):
                            yield '%s' % i, '%s' % i
                    else:
                        number, desc = m.split(':')
                        yield number.strip(), desc.strip()
        except:
            print s
            raise

    def __init__(self, d):
        self.id = d['GramBank ID'].strip()
        self.name = d['Feature']
        self.domain = OrderedDict()
        for n, desc in self.yield_domainelements(d['Possible Values']):
            self.domain[n] = desc
        self.domain.update({'?': 'Not known'})

    def format_domain(self):
        return '; '.join('%s: %s' % item for item in self.domain.items() if item[0] != '?')


def import_features(datadir, data):
    for feature in reader(os.path.join(datadir, 'features.csv'), dicts=True):
        feature = FeatureSpec(feature)
        f = data.add(Parameter, feature.id, id=feature.id, name=feature.name)
        for i, (deid, desc) in enumerate(feature.domain.items()):
            DomainElement(
                id='%s-%s' % (f.id, deid),
                parameter=f,
                abbr=deid,
                name='%s - %s' % (deid, desc),
                number=int(deid) if deid != '?' else 999,
                description=desc,
                jsondata=dict(icon=ORDERED_ICONS[i].name))
