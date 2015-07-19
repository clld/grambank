from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models.common import (
    Parameter, IdNameDescriptionMixin, Language
)

#-----------------------------------------------------------------------------
# specialized common mapper classes
#-----------------------------------------------------------------------------

class Family(Base, IdNameDescriptionMixin):
    __csv_name__ = 'families'
    glottocode = Column(String)
    color = Column(String, default='ff6600')
    family = Column(Unicode)
    family_glottocode = Column(String)

    def csv_head(self):
        return [
            'id',
            'name',
            'description',
            'glottocode',
            'family',
            'family_glottocode',
            'color']

@implementer(interfaces.ILanguage)
class grambankLanguage(CustomModelMixin, Language):
    __csv_name__ = 'languages'
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    family_pk = Column(Integer, ForeignKey('family.pk'))
    family = relationship(Family, backref='languages')
    glottocode = Column(String)
    macroarea = Column(Unicode)

    def csv_head(self):
        return [
            'id',
            'name',
            'glottocode',
            'families__id',
            'latitude',
            'longitude',
            'macroarea',
            'languages__ids',
        ]

    @classmethod
    def from_csv(cls, row, data=None):
        obj = super(grambankLanguage, cls).from_csv(row)
        obj.lineage = data['Family'][row[5]]
        return obj
