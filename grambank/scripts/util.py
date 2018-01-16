from __future__ import unicode_literals
import os
import re
from collections import OrderedDict, Counter
import csv
import getpass

from nameparser import HumanName

from clldutils.jsonlib import load as jsonload
from clldutils.misc import slug
from clldutils.dsv import reader
from clldutils.path import Path
from pyglottolog.api import Glottolog

from clld.db.meta import DBSession
from clld.db.models.common import (
    ValueSet, Value, DomainElement, Source, ValueSetReference,
    ContributionContributor, Contributor,
)
from clld.lib.bibtex import Database
from clld.web.icon import ORDERED_ICONS
from clld.scripts.util import bibtex2source

import grambank
from grambank.models import GrambankLanguage, Feature, GrambankContribution


GRAMBANK_REPOS = 'C:\\Python27\\glottobank\\Grambank\\' \
    if getpass.getuser() not in ['forkel@shh.mpg.de'] \
    else '/home/shh.mpg.de/forkel/venvs/grambank/Grambank'
GLOTTOLOG_REPOS = Path(grambank.__file__).parent.parent.parent.parent.joinpath(
    'glottolog3', 'glottolog') \
    if getpass.getuser() in ['forkel@shh.mpg.de'] \
    else Path('C:\\Python27\\glottolog\\')  # add your path to the glottolog repos clone here!


def import_dataset(path, data, languoids, invalid_features, add_missing_features=False):
    # look for metadata
    # look for sources
    # then loop over values

    dirpath, fname = os.path.split(path)
    basename, ext = os.path.splitext(fname)

    contrib = GrambankContribution(id=basename, name=basename, desc=languoids[basename].name)

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
            if add_missing_features:
                parameter = data.add(Feature, row['Feature_ID'], id=row['Feature_ID'], name=row.get('Feature', row['Feature_ID']))
            else:
                invalid_features.update([row['Feature_ID']])
                continue

        language = data['GrambankLanguage'].get(row['Language_ID'])
        if language is None:
            languoid = languoids.get(row['Language_ID'])
            if languoid is None:
                print('Skipping, no Glottocode found for %s' % row['Language_ID'])
                continue

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

        data.add(
            Value,
            vid,
            id=vid,
            valueset=vs,
            name=name,
            description=row['Comment'],
            domainelement=domain.get(row['Value']))

        for key, src in data['Source'].items():
            if key in vs.source:
                ValueSetReference(valueset=vs, source=src, key=key)


def import_cldf(srcdir, data, languoids, add_missing_features=False, maxnsheets = None):
    # loop over values
    # check if language needs to be inserted
    # check if feature needs to be inserted
    # add value if in domain
    invalid_features = Counter()
    for dirpath, dnames, fnames in os.walk(srcdir):
        for fname in (fnames[:maxnsheets] if maxnsheets else fnames):
            if os.path.splitext(fname)[1] in ['.tsv', '.csv']:
                import_dataset(
                    os.path.join(dirpath, fname),
                    data,
                    languoids,
                    invalid_features,
                    add_missing_features=add_missing_features)
    print(len(invalid_features), sum(invalid_features.values()))


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
        self.id = (d.get('GramBank ID') or d['Grambank ID']).strip()
        self.name = d['Feature']
        self.doc = d['Clarifying Comments']
        self.vdoc = d['Possible Values']
        self.patron = d['Feature patron']
        self.std_comments = d['Suggested standardised comments']
        self.name_french = d['Feature question in French']
        self.jl_relevant_unit = d['Relevant unit(s)']
        self.jl_function = d['Function']
        self.jl_form = d['Form']
        self.hard_to_deny = d['Very hard to deny']
        self.prone_misunderstanding = d['Prone to misunderstandings among researchers']
        self.requires_extensive_data = d['Requires extensive data on the language']
        self.last_edited = "See the Grambank Wiki" #d['Last edited']
        self.other_survey = d['Is there a typological survey that already covers this feature somehow?']
        self.designer = d['Design (just from Hedvigs memory)']
        self.thematic_order = d['Hedvigs thematic order']
        self.legacy_status = d['Legacy status']
        self.grambank_status = d['GramBank-status'] 
    	self.nts_grambank = d['NTS or GramBank?']
        self.old_feature = d['Old feature']
    #u'Wordhood issues', u'Old feature number', u'Dependencies'
    #wip_comments = Column(String) alternative_id??
    
        self.domain = OrderedDict()
        for n, desc in self.yield_domainelements(d['Possible Values']):
            self.domain[n] = desc
        self.domain.update({'?': 'Not known'})

    def format_domain(self):
        return '; '.join('%s: %s' % item for item in self.domain.items() if item[0] != '?')


def import_gb20_features(datadir, data):
    for feature in reader(
            os.path.join(datadir, 'gb20features.tsv'), delimiter='\t', dicts=True):
        feature = FeatureSpec(feature)
        f = data.add(
            Feature,
            feature.id,
            id=feature.id,
            name=feature.name,
            doc=feature.doc,
            patron=feature.patron,
            std_comments=feature.std_comments,
            name_french=feature.name_french,
            jl_relevant_unit=feature.jl_relevant_unit,
            jl_function=feature.jl_function,
            jl_form=feature.jl_form,
            hard_to_deny=feature.hard_to_deny,
            prone_misunderstanding=feature.prone_misunderstanding,
            requires_extensive_data=feature.requires_extensive_data,
            last_edited=feature.last_edited,
            other_survey=feature.other_survey)
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
    glottolog = Glottolog(GLOTTOLOG_REPOS)
    return [
        tuple([ll.id for ll in l.ancestors] + [l.id]) for l in glottolog.languoids(lgs)]


def get_names():
    return {l.id: l.name for l in Glottolog(GLOTTOLOG_REPOS).languoids()}
