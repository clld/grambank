from __future__ import unicode_literals
import os
import re
from collections import OrderedDict
from itertools import cycle
import csv

from nameparser import HumanName

from clld.util import jsonload, slug
from clld.db.meta import DBSession
from clld.db.models.common import (
    ValueSet, Value, DomainElement, Source, ValueSetReference,
    ContributionContributor, Contributor,
)
from clld.lib.dsv import reader
from clld.lib.bibtex import Database
from clld.web.icon import ORDERED_ICONS
from clld.scripts.util import bibtex2source

from clldclient.glottolog import Glottolog

from grambank.models import GrambankLanguage, Feature, GrambankContribution


def import_dataset(path, data, icons):
    # look for metadata
    # look for sources
    # then loop over values
    dirpath, fname = os.path.split(path)
    basename, ext = os.path.splitext(fname)
    glottolog = Glottolog()

    contrib = GrambankContribution(id=basename, name=basename, desc=glottolog.languoid(basename).name)

    md = {}
    mdpath = path + '-metadata.json'
    if os.path.exists(mdpath):
        md = jsonload(mdpath)
    contributor_name = HumanName(md.get('contributed_datapoint', 'Team NTS'))
    contributor_id = slug(contributor_name.last + contributor_name.first)
    contributor = data['Contributor'].get(contributor_id)
    if not contributor:
        contributor = data.add(
            Contributor,
            contributor_id,
            id=contributor_id,
            name='%s' % contributor_name)
    DBSession.add(ContributionContributor(contribution=contrib, contributor=contributor))

    bibpath = os.path.join(dirpath, basename + '.bib')
    if os.path.exists(bibpath):
        for rec in Database.from_file(bibpath):
            if rec['key'] not in data['Source']:
                data.add(Source, rec['key'], _obj=bibtex2source(rec))

    languages = {f['properties']['glottocode']: f for f in md.get('features', [])}

    for i, row in enumerate(reader(path, dicts=True, quoting=csv.QUOTE_NONE, delimiter=',' if 'c' in ext else '\t')):
        if not row['Value'] or not row['Feature_ID']:
            continue
        vsid = '%s-%s-%s' % (basename, row['Language_ID'], row['Feature_ID'])
        vid = row.get('ID', '%s-%s' % (basename, i + 1))

        parameter = data['Feature'].get(row['Feature_ID'])
        if parameter is None:
            print('skip value for invalid feature %s' % row['Feature_ID'])
            continue
            #parameter = data.add(
            #    Feature, row['Feature_ID'], id=row['Feature_ID'], name=row.get('Feature', row['Feature_ID']))

        language = data['GrambankLanguage'].get(row['Language_ID'])
        if language is None:
            # query glottolog!
            languoid = glottolog.languoid(row['Language_ID'])
            gl_md = {
                'name': languoid.name,
                'longitude': languoid.longitude,
                'latitude': languoid.latitude}
            lmd = languages.get(row['Language_ID'])
            if lmd:
                if lmd.get('properties', {}).get('name'):
                    gl_md['name'] = lmd['properties']['name']
                if lmd.get('geometry', {}).get('coordinates'):
                    gl_md['longitude'], gl_md['latitude'] = lmd['geometry']['coordinates']

            language = data.add(
                GrambankLanguage, row['Language_ID'],
                id=row['Language_ID'],
                name=gl_md['name'],
                latitude=gl_md.get('latitude'),
                longitude=gl_md.get('longitude'))

        domain = {de.abbr: de for de in parameter.domain}    
	if not domain.get(row['Value']):
            #print "skipped", row, "not in", domain
            continue
        
        vs = data['ValueSet'].get(vsid)
        if vs is None:
            vs = data.add(
                ValueSet, vsid,
                id=vsid,
                parameter=parameter,
                language=language,
                contribution=contrib,
                source=row['Source'])

        name = row['Value']
        if name in domain:
            name = domain[name].name

        data.add(Value,
            vid,
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
                    print os.path.join(dirpath, fname)
                except:
                    print 'ERROR'
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

def get_clf_paths(lgs):
    def path(languoid):
        if not languoid:
            return ()
        return path(languoid.parent) + (languoid.id,)
    glottolog = Glottolog()
    return [path(glottolog.languoid(lg)) for lg in lgs]
    
