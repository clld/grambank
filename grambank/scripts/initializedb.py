from __future__ import unicode_literals
import sys
import os
import getpass
import json

from clld.scripts.util import initializedb, Data
from clld.db.meta import DBSession
from clld.db.models import common

import grambank
from grambank.scripts.util import import_features_collaborative_sheet, import_cldf, get_clf_paths

from clld_glottologfamily_plugin.util import load_families

from stats_util import grp, feature_stability, feature_dependencies, dependencies_graph

from grambank.models import Dependency

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
        
    fs = feature_stability(datatriples, clfps)
    #with open('grambank\\static\\stability.json', 'wb') as fp:
    #    json.dump(fs, fp)
    for (f, s) in fs:
        data['Feature'][f].parsimony_stability_value = s["stability"]
        data['Feature'][f].parsimony_retentions = s["retentions"]
        data['Feature'][f].parsimony_transitions = s["transitions"]
    
    imps = feature_dependencies(datatriples)
    #with open('grambank\\static\\dependencies.json', 'wb') as fp:
    #    json.dump(imps, fp)
    for (i, (v, f1, f2)) in enumerate(imps):
        data.add(Dependency, i, id = "%s->%s" % (f1, f2), strength = v, feature1 = data['Feature'][f1])#, feature2 = data['Feature'][f2]) #feature1_pk = f1, feature2_pk = f2) #
    

    
    #dot = dependencies_graph(imps)        
    #with open('grambank\\static\\dependencies.gv', 'w') as fp:
    #    fp.write(dot)
        
def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """

if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
