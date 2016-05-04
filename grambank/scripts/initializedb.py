from __future__ import unicode_literals
import sys
import os
import getpass
import json

import transaction
from clld.scripts.util import initializedb, Data, gbs_func
from clld.db.meta import DBSession
from clld.db.models import common
from clld.db.util import compute_language_sources

import grambank
from grambank.scripts.util import import_features_collaborative_sheet, import_cldf, get_clf_paths

#from clld_glottologfamily_plugin.util import Family
from localglottolog import load_families, LocalGlottolog
from stats_util import grp, feature_stability, feature_dependencies, dependencies_graph, deep_families, havdist
from grambank.models import Dependency, Transition, Stability, DeepFamily, Support, HasSupport


def main(args):
    user = getpass.getuser()
    data = Data()
    datadir = 'C:\\Python27\\glottobank\\Grambank\\' if user != 'robert' \
        else '/home/robert/venvs/glottobank/Grambank'

    dataset = common.Dataset(
        id=grambank.__name__,
        name="GramBank",
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

    import_features_collaborative_sheet(datadir, data)
    import_cldf(os.path.join(datadir, 'datasets'), data)
    ##import_cldf("C:\\python27\\dbs\\bwohh\\", data, add_missing_features = True)
    load_families(data, data['GrambankLanguage'].values(), isolates_icon='tcccccc')
    glottolog = LocalGlottolog()
    #for lg in data['GrambankLanguage'].values():
    #    gl_language = glottolog.languoid(lg.id)
    #    if not gl_language.family:
    #        family = data.add(Family, gl_language.id, id = gl_language.id, name = gl_language.name, description=common.Identifier(name=gl_language.id, type=common.IdentifierType.glottolog.value).url(), jsondata={"icon": 'tcccccc'})
    #        lg.family = family
    
    datatriples = [(v.valueset.language.id, v.valueset.parameter.id, v.name) for v in data["Value"].itervalues()]
    flv = dict([(feature, dict(lvs)) for (feature, lvs) in grp([(f, l, v) for (l, f, v) in datatriples]).iteritems()])
    clfps = get_clf_paths([lg.id for lg in data['GrambankLanguage'].values()])

    for (f, lv) in flv.iteritems():
        data['Feature'][f].representation = len(lv)

    
    fs = feature_stability(datatriples, clfps)
    for (f, (s, transitions, stationarity_p, synchronic_p)) in fs:
        data.add(Stability, f, id = f.replace("GB", "S"), feature = data['Feature'][f], parsimony_stability_value = s["stability"], parsimony_retentions = s["retentions"], parsimony_transitions = s["transitions"], jsondata={'diachronic_p': stationarity_p, "synchronic_p": synchronic_p})
        for (i, (fam, (fromnode, tonode), (ft, tt))) in enumerate(transitions):
            DBSession.add(Transition, i, id = "%s: %s->%s" % (f, fromnode, tonode), stability = data['Stability'][f], fromnode=glottolog.languoid(fromnode).name, tonode=glottolog.languoid(tonode).name, fromvalue=ft, tovalue=tt, family = data['Family'][fam], retention_innovation = "Retention" if ft == tt else "Innovation")


    

        
    imps = feature_dependencies(datatriples)
    H = {}
    (H, V) = dependencies_graph([(v, f1, f2) for ((v, dstats), f1, f2) in imps])
    
    for (i, ((v, dstats), f1, f2)) in enumerate(imps):
        combinatory_status = ("primary" if H.has_key((f1, f2)) else ("epiphenomenal" if v > 0.0 else None)) if H else "N/A"
        DBSession.add(Dependency, i, id = "%s->%s" % (f1, f2), strength = v, feature1 = data['Feature'][f1], feature2 = data['Feature'][f2], representation = dstats["representation"], combinatory_status = combinatory_status, jsondata = dstats)

    coordinates = {lg.id: (lg.longitude, lg.latitude) for lg in data['GrambankLanguage'].values() if lg.longitude != None and lg.latitude != None}
    deepfams = deep_families(datatriples, clfps, coordinates = coordinates)
    
    for ((l1, l2), support_value, significance, supports, f1c, f2c) in deepfams:
        dname = "proto-%s x proto-%s" % (glottolog.languoid(l1).name, glottolog.languoid(l2).name)
        kmdistance = havdist(f1c, f2c)
        (f1lon, f1lat) = f1c if f1c else (None, None)
        (f2lon, f2lat) = f2c if f2c else (None, None)
        data.add(DeepFamily, dname, id = dname, support_value = support_value, significance = significance, family1 = data["Family"][l1], family2 = data["Family"][l2], family1_latitude = f1lat, family1_longitude = f1lon, family2_latitude = f2lat, family2_longitude = f2lon, geographic_plausibility = kmdistance)
        for (f, v1, v2, historical_score, independent_score, support_score) in supports:
            vid = ("%s: %s %s %s" % (f, v1, "==" if v1 == v2 else "!=", v2)).replace(".", "")
            #vname = ("%s|%s" % (v1, v2)).replace(".", "")
            #print vid, vname
            if not data["Support"].get(vid):
                data.add(Support, vid, id = vid, historical_score = historical_score, independent_score = independent_score, support_score = support_score, value1= v1, value2 = v2, feature = data['Feature'][f])
            hsvid = dname + " has " + vid
            DBSession.add(HasSupport, hsvid, deepfamily = data["DeepFamily"][dname], support = data["Support"][vid])
                
def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """

    compute_language_sources()
    transaction.commit()
    transaction.begin()

    #gbs_func('update', args)

if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
