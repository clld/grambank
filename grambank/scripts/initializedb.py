from __future__ import unicode_literals, print_function
import sys
import os

from clld.scripts.util import initializedb, Data
from clld.db.meta import DBSession
from clld.db.models import common
from clld.db.util import compute_language_sources
from clld_glottologfamily_plugin.models import Family
from clld_glottologfamily_plugin.util import load_families
from pyglottolog.api import Glottolog

import grambank
from grambank.scripts.util import (
    import_gb20_features, import_cldf, get_clf_paths, get_names,
    GLOTTOLOG_REPOS, GRAMBANK_REPOS,
)

from stats_util import grp, grp2, feature_stability, feature_dependencies, feature_diachronic_dependencies, dependencies_graph, deep_families, havdist
from grambank.models import Dependency, Transition, Stability, DeepFamily, Support, HasSupport, Feature, GrambankLanguage


def main(args):
    #TODO explain etc diachronic_strength
    #sigtests of dependencies
    #isogloss-maps
    data = Data()
    dataset = common.Dataset(
        id=grambank.__name__,
        name="Grambank",
        publisher_name="Max Planck Institute for the Science of Human History",
        publisher_place="Jena",
        publisher_url="http://shh.mpg.de",
        license="http://creativecommons.org/licenses/by/4.0/",
        domain='grambank.clld.org',
        contact='harald.hammarstrom@gmail.com',
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'})
    DBSession.add(dataset)
    glottolog = Glottolog(GLOTTOLOG_REPOS)
    languoids = {l.id: l for l in glottolog.languoids()}

    import_gb20_features(GRAMBANK_REPOS, data)
    import_cldf(os.path.join(GRAMBANK_REPOS, 'datasets'), data, languoids)
    load_families(
        data,
        data['GrambankLanguage'].values(),
        glottolog_repos=GLOTTOLOG_REPOS,
        isolates_icon='tcccccc')

    # Add isolates
    for lg in data['GrambankLanguage'].values():
        gl_language = languoids.get(lg.id)
        if not gl_language.family:
            family = data.add(
                Family, gl_language.id,
                id=gl_language.id,
                name=gl_language.name,
                description=common.Identifier(
                    name=gl_language.id,
                    type=common.IdentifierType.glottolog.value).url(),
                jsondata={"icon": 'tcccccc'})
            lg.family = family
    return 


def dump(fn = "gbdump.tsv"):
    import io
#    dumpsql = """
#select l.id, p.id, v.name, v.description, s.name
#from value as v, language as l, parameter as p, valueset as vs LEFT OUTER JOIN valuesetreference as vsref ON vsref.valueset_pk = vs.pk LEFT OUTER JOIN source as s ON vsref.source_pk = s.pk
#where v.valueset_pk = vs.pk and vs.language_pk = l.pk and vs.parameter_pk = p.pk
#    """
    #datatriples = grp2([((v[0], v[1], v[2], v[3] or ""), v[4] or "") for v in DBSession.execute(dumpsql)])
    #dump = [xs + ("; ".join(refs),) for (xs, refs) in datatriples.iteritems()]
    dumpsql = """
select l.name, l.id, p.id, p.name, v.name, v.description, vs.source
from value as v, language as l, parameter as p, valueset as vs
where v.valueset_pk = vs.pk and vs.language_pk = l.pk and vs.parameter_pk = p.pk
    """
    dump = [(lgname, lgid, "%s. %s" % (fid, fname), v, com, src) for (lgname, lgid, fid, fname, v, com, src) in DBSession.execute(dumpsql)]
    tab = lambda rows: u''.join([u'\t'.join(row) + u"\n" for row in rows])
    txt = tab([("Language_Name", "Language_ID", "Feature", "Value", "Comment", "Source")] + dump)
    with io.open(fn, 'w', encoding="utf-8") as fp:
        fp.write(txt)
    #copy C:\python27\gb\gbdump.tsv C:\python27\glottobank\grambank\

def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
    from time import time
    _s = time()

    def checkpoint(s, msg=None):
        n = time()
        print(n - s, msg or '')
        return n


    dump()
    
    sql = """
select l.id, p.id, v.name from value as v, valueset as vs, language as l, parameter as p
where v.valueset_pk = vs.pk and vs.language_pk = l.pk and vs.parameter_pk = p.pk
    """
    datatriples = [(v[0], v[1], v[2]) for v in DBSession.execute(sql)]
    _s = checkpoint(_s, '%s values loaded' % len(datatriples))

    flv = dict([(feature, dict(lvs)) for (feature, lvs) in grp([(f, l, v) for (l, f, v) in datatriples]).iteritems()])
    _s = checkpoint(_s, 'triples grouped')

    clfps = get_clf_paths([row[0] for row in DBSession.execute("select id from language")])
    _s = checkpoint(_s, '%s clfps loaded' % len(clfps))

    features = {f.id: f for f in DBSession.query(Feature)}
    for (f, lv) in flv.iteritems():
        features[f].representation = len(lv)

    languages = {l.id: l for l in DBSession.query(GrambankLanguage)}        
    for (l, fv) in grp2([(l, (f, v)) for (f, lv) in flv.iteritems() for (l, v) in lv.iteritems()]).iteritems():
        languages[l].representation = len(fv)
    DBSession.flush()
    _s = checkpoint(_s, 'representation assigned')

    fs = feature_stability(datatriples, clfps)
    _s = checkpoint(_s, 'feature_stability computed')

    glottolog_names = get_names()
    families = {f.id: f for f in DBSession.query(Family)}
    for (f, (s, transitions, stationarity_p, synchronic_p)) in fs:
        stability = Stability(
            id=f.replace("GB", "S"),
            feature=features[f],
            parsimony_stability_value=s["stability"],
            parsimony_stability_rank=s["rank"],
            parsimony_retentions=s["retentions"],
            parsimony_transitions=s["transitions"],
            jsondata={'diachronic_p': stationarity_p, "synchronic_p": synchronic_p})
        DBSession.add(stability)
        for (i, (fam, (fromnode, tonode), (ft, tt))) in enumerate(transitions):
            DBSession.add(Transition(
                id="%s: %s->%s" % (f, fromnode, tonode),
                stability=stability,
                fromnode=glottolog_names[fromnode],
                tonode=glottolog_names[tonode],
                fromvalue=ft,
                tovalue=tt,
                family=families[fam],
                retention_innovation="Retention" if ft == tt else "Innovation"))
    DBSession.flush()
    _s = checkpoint(_s, 'stability and transitions loaded')

    diachronic_imps = feature_diachronic_dependencies(datatriples, clfps)
    diachronic_imp_strength = {(f1, f2): v for (((v, ccalltrd), lalltr, ccdtr, ldtr, cccdtr, lcdtr), rnk, f1, f2) in diachronic_imps}
    _s = checkpoint(_s, 'feature_diachronic_dependencies computed')
    
    imps = feature_dependencies(datatriples)
    _s = checkpoint(_s, 'feature_dependencies computed')
    if 1:
        (H, V) = dependencies_graph([(v, f1, f2) for ((v, dstats), rnk, f1, f2) in imps])
        _s = checkpoint(_s, 'dependencies_graph written')

        for ((v, dstats), rnk, f1, f2) in imps:
            combinatory_status = ("primary" if H.has_key((f1, f2)) else ("epiphenomenal" if v > 0.0 else None)) if H else "N/A"
            DBSession.add(Dependency(
                id="%s->%s" % (f1, f2),
                strength=v,
                diachronic_strength=diachronic_imp_strength.get((f1, f2)),
                rank=rnk,
                feature1=features[f1],
                feature2=features[f2],
                representation=dstats["representation"],
                combinatory_status=combinatory_status,
                jsondata=dstats))
        DBSession.flush()
        _s = checkpoint(_s, 'dependencies loaded')

    coordinates = {
        lg.id: (lg.longitude, lg.latitude)
        for lg in DBSession.query(common.Language)
        .filter(common.Language.longitude != None)
        .filter(common.Language.latitude != None)}
    deepfams = deep_families(datatriples, clfps, coordinates=coordinates)
    _s = checkpoint(_s, '%s deep_families computed' % len(deepfams))

    missing_families = set()
    data = Data()
    for ((l1, l2), support_value, significance, supports, f1c, f2c) in deepfams:
        dname = "proto-%s x proto-%s" % (glottolog_names[l1], glottolog_names[l2])
        kmdistance = havdist(f1c, f2c)
        (f1lon, f1lat) = f1c if f1c else (None, None)
        (f2lon, f2lat) = f2c if f2c else (None, None)

        for li in [l1, l2]:
            if li not in families:
                missing_families.add(li)

        deepfam = DeepFamily(
            id=dname,
            support_value=support_value,
            significance=significance,
            family1=families.get(l1),
            family2=families.get(l2),
            family1_latitude = f1lat,
            family1_longitude = f1lon,
            family2_latitude = f2lat,
            family2_longitude = f2lon,
            geographic_plausibility = kmdistance)
        DBSession.add(deepfam)
        for (f, v1, v2, historical_score, independent_score, support_score) in supports:
            vid = ("%s: %s %s %s" % (f, v1, "==" if v1 == v2 else "!=", v2)).replace(".", "")
            #vname = ("%s|%s" % (v1, v2)).replace(".", "")
            #print vid, vname
            if vid not in data["Support"]:
                data.add(
                    Support, vid,
                    id = vid,
                    historical_score = historical_score,
                    independent_score = independent_score,
                    support_score = support_score,
                    value1= v1,
                    value2 = v2,
                    feature=features[f])
            DBSession.add(HasSupport(
                id=dname + "-" + vid,
                deepfamily = deepfam,
                support = data["Support"][vid]))
    print('missing_families:')
    print(missing_families)
    DBSession.flush()
    _s = checkpoint(_s, 'deep_families loaded')

    compute_language_sources()


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
