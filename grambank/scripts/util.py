from __future__ import unicode_literals
import os
import re
from collections import OrderedDict
import json
from itertools import cycle

import requests

from clld.util import jsondump, jsonload
from clld.db.models.common import (
    ValueSet, Value, Contribution, DomainElement, Source, ValueSetReference,
)
#Parameter
from clld.lib.dsv import reader
from clld.lib.bibtex import Database
from clld.web.icon import ORDERED_ICONS
from clld.scripts.util import bibtex2source, add_language_codes

from grambank.models import GrambankLanguage, Family, Feature


GLOTTOLOG_CACHE = os.path.join(os.path.expanduser("~"), '.glottolog-cache.json')


def glottolog_md(glottocode):
    cache = jsonload(GLOTTOLOG_CACHE) if os.path.exists(GLOTTOLOG_CACHE) else {}
    if glottocode not in cache:
        print('cache miss: %s' % glottocode)
        cache[glottocode] = requests.get(
        'http://glottolog.org/resource/languoid/id/{0}.json'.format(glottocode)).json()
    jsondump(cache, GLOTTOLOG_CACHE, indent=4)
    md = cache[glottocode]
    md['family'] = md['classification'][0] if md.get('classification') else None
    md['macroarea'] = list(md['macroareas'].items())[0]
    return md


def import_dataset(path, data, icons):
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
            # query glottolog!
            gl_md = glottolog_md(row['Language_ID'])
            lmd = languages.get(row['Language_ID'])
            if lmd:
                if lmd.get('properties', {}).get('name'):
                    gl_md['name'] = lmd['properties']['name']
                if lmd.get('geometry', {}).get('coordinates'):
                    gl_md['longitude'], gl_md['latitude'] = lmd['geometry']['coordinates']

            if gl_md['family']:
                family = data['Family'].get(gl_md['family']['id'])
                if not family:
                    family = data.add(
                        Family, gl_md['family']['id'],
                        id=gl_md['family']['id'],
                        name=gl_md['family']['name'],
                        description=gl_md['family']['url'],
                        icon=icons.next().name)
            else:
                family = data['Family'].get('isolates')
                if not family:
                    family = data.add(
                        Family, 'isolates',
                        id='isolates',
                        name='Isolates',
                        description='Isolated languages',
                        icon=icons.next().name)

            language = data.add(
                GrambankLanguage, row['Language_ID'],
                id=row['Language_ID'],
                name=gl_md['name'],
                family=family,
                latitude=gl_md.get('latitude'),
                longitude=gl_md.get('longitude'),
                macroarea=gl_md['macroarea'][1])
            add_language_codes(
                data, language, gl_md.get('iso639-3'), glottocode=row['Language_ID'])

        parameter = data['Feature'].get(row['Feature_ID'])
        if parameter is None:
            parameter = data.add(
                Feature, row['Feature_ID'], id=row['Feature_ID'], name=row.get('Feature', row['Feature_ID']))

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
    icons = cycle(ORDERED_ICONS)

    for dirpath, dnames, fnames in os.walk(srcdir):
        for fname in fnames:
            if os.path.splitext(fname)[1] in ['.tsv', '.csv']:
                try:
                    import_dataset(os.path.join(dirpath, fname), data, icons)
                except:
                    print os.path.join(dirpath, fname)
                    raise
                #break

    pass


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
        self.doc = d['Clarifying Comments']
        self.patron = d['Feature patron']
        self.std_comments = d['Suggested standardised comments']
        self.name_french = d['Feature question in French']
        self.jl_relevant_unit = d['Relevant unit(s)']
        self.jl_function = d['Function']
        self.jl_formal_means = d['Formal means']
        self.hard_to_deny = d['Very hard to deny']
        self.prone_misunderstanding = d['Prone to misunderstandings among researchers']
        self.requires_extensive_data = d['Requires extensive data on the language']
        self.last_edited = d['Last edited']
        self.other_survey = d['Is there a typological survey that already covers this feature somehow?']
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

def import_features_collaborative_sheet(datadir, data):
    for feature in reader(os.path.join(datadir, 'features_collaborative_sheet.tsv'), dicts=True):
        feature = FeatureSpec(feature)
        f = data.add(Feature, feature.id, id=feature.id, name=feature.name, doc=feature.doc, patron=feature.patron, std_comments=feature.std_comments, name_french=feature.name_french, jl_relevant_unit=feature.jl_relevant_unit, jl_function=feature.jl_function, jl_formal_means=feature.jl_formal_means, hard_to_deny=feature.hard_to_deny, prone_misunderstanding=feature.prone_misunderstanding, requires_extensive_data=feature.requires_extensive_data, last_edited=feature.last_edited, other_survey=feature.other_survey)
        for i, (deid, desc) in enumerate(feature.domain.items()):
            DomainElement(
                id='%s-%s' % (f.id, deid),
                parameter=f,
                abbr=deid,
                name='%s - %s' % (deid, desc),
                number=int(deid) if deid != '?' else 999,
                description=desc,
                jsondata=dict(icon=ORDERED_ICONS[i].name))
