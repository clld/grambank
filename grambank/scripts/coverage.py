import sys
import io
from itertools import groupby
from collections import Counter, defaultdict
from functools import total_ordering

from clldutils.path import Path
from clldutils.jsonlib import load, dump
from csvw.dsv import reader
from pyglottolog.api import Glottolog

import grambank

GLOTTOLOG_VENV = Path(grambank.__file__).parent.parent.parent.parent.joinpath('glottolog')


@total_ordering
class Language(object):  # pragma: no coverage
    def __init__(self, l, med):
        f, sf, ssf = l.lineage[:3] + [(None, None, None)] * (3 - len(l.lineage[:3]))
        self.id = str(l.id)
        self.name = l.name
        self.ssfid = str(ssf[1])
        self.ssfname = ssf[0]
        self.sfid = str(sf[1])
        self.sfname = sf[0]
        self.fid = str(f[1])
        self.fname = f[0]
        self.med = med.replace(' ', '') if med in ['grammar', 'grammar sketch'] else None
        self.macroareas = [(ma.name, ma.id) for ma in l.macroareas]

    @property
    def gid(self):
        return (self.fid, self.sfid, self.ssfid, self.id)

    def __eq__(self, other):
        return self.gid == other.gid

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return self.gid < other.gid

    def __cmp__(self, other):
        return (self.gid > other.gid) - (self.gid < other.gid)


def iter_languages(api):  # pragma: no coverage
    meds = {
        row['Language_ID']: row['Value'] for row in reader(
            GLOTTOLOG_VENV / 'glottolog-cldf' / 'cldf' / 'values.csv', dicts=True)
        if row['Parameter_ID'] == 'med'}
    for l in api.languoids():
        if l.level == api.languoid_levels.language and not l.category.startswith('Pseudo'):
            yield Language(l, meds.get(l.id))


def read(n):  # pragma: no coverage
    with io.open('%s.csv' % n, encoding='utf8') as fp:
        for i, line in enumerate(fp):
            yield [None if col == '[NULL]' else col for col in line.strip().split('+++')]


def get_md(name, langs):  # pragma: no coverage
    res = dict(name=name, extension=[], macroareas=set(), doctype=None, subgroups={})
    for l in langs:
        if res['doctype'] != 'grammar':
            if l.med:
                res['doctype'] = l.med
        res['macroareas'] = res['macroareas'].union(l.macroareas)
        res['extension'].append(l.id)
    res['macroareas'] = list(res['macroareas'])
    return res


if __name__ == '__main__':  # pragma: no coverage
    res = {}
    api = Glottolog(GLOTTOLOG_VENV.joinpath('glottolog'))
    log = Counter()
    languages = sorted(iter_languages(api))

    for (fid, fname), langs in groupby(languages, lambda l: (l.fid, l.fname)):
        langs = list(langs)
        if fid:
            if fname in 'Bookkeeping|Mixed Language|Pidgin|Sign Language|Unclassifiable|Artificial Language'.split('|'):
                continue

            d = get_md(fname, langs)
            if not d['doctype']:  # ignore everything that doesn't have a grammar or grammarsketch
                continue

            log.update(['family'])
            res[fid] = d

            for (sfid, sfname), slangs in groupby(langs, lambda l: (l.sfid, l.sfname)):
                slangs = list(slangs)
                if sfid:
                    dd = get_md(sfname, slangs)
                    if not dd['doctype']:
                        continue

                    log.update(['subunit'])
                    res[fid]['subgroups'][sfid] = dd
                    for (ssfid, ssfname), sslangs in groupby(slangs, lambda l: (l.ssfid, l.ssfname)):
                        sslangs = list(sslangs)
                        if ssfid:
                            ddd = get_md(ssfname, sslangs)
                            if ddd['doctype']:
                                log.update(['subsubunit'])
                                res[fid]['subgroups'][sfid]['subgroups'][ssfid] = ddd
        else:
            # isolates:
            for l in langs:
                if l.med:
                    log.update(['isolate'])
                    res[l.id] = {
                        'name': l.name,
                        'doctype': l.med,
                        'macroareas': l.macroareas,
                        'extension': [l.id],
                    }

    outdir = Path(grambank.__file__).parent.joinpath('static')
    dump(res, outdir.joinpath('stats_by_classification.json'))

    stats = defaultdict(lambda: defaultdict(list))
    for fid, f in res.items():
        for maname, maid in f['macroareas']:
            stats[maid][f['doctype']].append(fid)
    
    dump(stats, outdir.joinpath('stats_by_macroarea.json'))

    macroareas = {ma.id: ma.name for ma in api.macroareas.values()}
    dump(macroareas, outdir.joinpath('stats_macroareas.json'))

    print(log)
    sys.exit(0)
