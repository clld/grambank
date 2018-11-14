from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Integer,
    Unicode,
    Float,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import relationship, backref

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.versioned import Versioned
from clld.db.models.common import Contribution, Parameter, Language, Contributor
from clld_glottologfamily_plugin.models import HasFamilyMixin, Family


@implementer(interfaces.IContributor)
class Coder(CustomModelMixin, Contributor):
    pk = Column(Integer, ForeignKey('contributor.pk'), primary_key=True)
    count_datapoints = Column(Integer)


@implementer(interfaces.ILanguage)
class GrambankLanguage(CustomModelMixin, Language, HasFamilyMixin):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    macroarea = Column(Unicode)
    representation = Column(Integer)
    nzrepresentation = Column(Integer)
    contribution_pk = Column(Integer, ForeignKey('contribution.pk'))
    contribution = relationship(Contribution, backref=backref("language", uselist=False))

@implementer(interfaces.IParameter)
class Feature(CustomModelMixin, Parameter, Versioned):
    """Parameters in GramBank are called features. They are always related to one Designer.
    """
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    representation = Column(Integer)
    patron = Column(String)
    name_french = Column(String)
