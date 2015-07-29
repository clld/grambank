from clld.web.datatables.language import Languages
from clld_glottologfamily_plugin.datatables import FamilyLinkCol, MacroareaCol
from clld_glottologfamily_plugin.models import Family

from models import GrambankLanguage


class GrambankLanguages(Languages):
    def base_query(self, query):
        return query.outerjoin(Family)

    def col_defs(self):
        res = Languages.col_defs(self)
        res.append(MacroareaCol(self, 'macroarea', language_cls=GrambankLanguage))
        res.append(FamilyLinkCol(self, 'family', language_cls=GrambankLanguage))
        return res


def includeme(config):
    config.register_datatable('languages', GrambankLanguages)
