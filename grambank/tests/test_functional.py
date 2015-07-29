from path import path

from clld.tests.util import TestWithApp

import grambank


class Tests(TestWithApp):
    __cfg__ = path(grambank.__file__).dirname().joinpath('..', 'development.ini').abspath()
    __setup_db__ = False

    def test_home(self):
        self.app.get('/')

    def test_misc(self):
        self.app.get('/parameters/GB028')
        self.app.get_json('/parameters/GB028.geojson?domainelement=GB028-1')
        self.app.get_dt('/values?parameter=GB028')
        self.app.get_dt('/languages')
        self.app.get_dt('/familys')
        self.app.get_html('/sources/skennedykalalagawya')
