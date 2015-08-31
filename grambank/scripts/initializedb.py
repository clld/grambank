from __future__ import unicode_literals
import sys
import os
import getpass

from clld.scripts.util import initializedb, Data
from clld.db.meta import DBSession
from clld.db.models import common

import grambank
from grambank.scripts.util import import_features_collaborative_sheet, import_cldf

from clld_glottologfamily_plugin.util import load_families


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
    #print data.keys()
    #print data['Parameter'].keys()
    #parameter = data['Parameter'].get(row['Feature_ID'])

    load_families(data, data['GrambankLanguage'].values(), isolates_icon='tcccccc')


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """

if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
