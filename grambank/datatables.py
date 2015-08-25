from clld.db.util import get_distinct_values, icontains
from clld.web.util.helpers import map_marker_img
from clld.web.util.htmllib import HTML

from clld.web.datatables.base import Col
from clld.web.datatables.language import Languages

from models import GrambankLanguage, Family


class FamilyCol(Col):
    def __init__(self, dt, name, **kw):
        kw['choices'] = get_distinct_values(Family.name)
        Col.__init__(self, dt, name, **kw)

    def order(self):
        return Family.name

    def search(self, qs):
        return icontains(Family.name, qs)

    def format(self, item):
        return HTML.div(map_marker_img(self.dt.req, item), ' ', item.family.name)


class GrambankLanguages(Languages):
    def base_query(self, query):
        return query.join(Family)

    def col_defs(self):
        res = Languages.col_defs(self)
        res.append(Col(self, 'macroarea', model_col=GrambankLanguage.macroarea))
        res.append(FamilyCol(self, 'family'))
        return res


def includeme(config):
    config.register_datatable('languages', GrambankLanguages)
