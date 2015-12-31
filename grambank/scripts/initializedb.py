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



from clld_glottologfamily_plugin.util import load_families
from clldclient.glottolog import Glottolog
from stats_util import grp, feature_stability, feature_dependencies, dependencies_graph
from grambank.models import Dependency, Transition, Stability


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
    load_families(data, data['GrambankLanguage'].values(), isolates_icon='tcccccc')


    
    datatriples = [(v.valueset.language.id, v.valueset.parameter.id, v.name) for v in data["Value"].itervalues()]
    flv = dict([(feature, dict(lvs)) for (feature, lvs) in grp([(f, l, v) for (l, f, v) in datatriples]).iteritems()])
    clfps = get_clf_paths([lg.id for lg in data['GrambankLanguage'].values()])

    for (f, lv) in flv.iteritems():
        data['Feature'][f].representation = len(lv)

    glottolog = Glottolog()
    fs = feature_stability(datatriples, clfps)
    for (f, (s, transitions)) in fs:
        data.add(Stability, f, id = f.replace("GB", "S"), feature = data['Feature'][f], parsimony_stability_value = s["stability"], parsimony_retentions = s["retentions"], parsimony_transitions = s["transitions"])
        for (i, (fam, (fromnode, tonode), (ft, tt))) in enumerate(transitions):
            data.add(Transition, i, id = "%s: %s->%s" % (f, fromnode, tonode), stability = data['Stability'][f], fromnode=glottolog.languoid(fromnode).name, tonode=glottolog.languoid(tonode).name, fromvalue=ft, tovalue=tt, family = data['Family'][fam], retention_innovation = "Retention" if ft == tt else "Innovation")


    

        
    imps = feature_dependencies(datatriples)
    H = {}
    #(H, V) = dependencies_graph([(v, f1, f2) for ((v, dstats), f1, f2) in imps])
    #with open('grambank\\static\\dependencies.gv', 'w') as fp:
    #    fp.write(dot(H, V))
    
    for (i, ((v, dstats), f1, f2)) in enumerate(imps):
        combinatory_status = ("primary" if H.has_key((f1, f2)) else ("epiphenomenal" if v > 0.0 else None)) if H else "N/A"
        data.add(Dependency, i, id = "%s->%s" % (f1, f2), strength = v, feature1 = data['Feature'][f1], feature2 = data['Feature'][f2], representation = dstats["representation"], combinatory_status = combinatory_status, jsondata = dstats)
    
    
def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """

    compute_language_sources()
    transaction.commit()
    transaction.begin()

    gbs_func('update', args)

if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
