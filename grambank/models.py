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


class Family(Base, IdNameDescriptionMixin):
    icon = Column(String, default='cff6600')


@implementer(interfaces.ILanguage)
class GrambankLanguage(CustomModelMixin, Language):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    family_pk = Column(Integer, ForeignKey('family.pk'))
    family = relationship(Family, backref='languages')
    macroarea = Column(Unicode)
