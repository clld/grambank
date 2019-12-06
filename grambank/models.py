import collections

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
from clld.db.models.common import Contribution, Parameter, Language, Contributor, Dataset
from clld_glottologfamily_plugin.models import HasFamilyMixin, Family


@implementer(interfaces.IDataset)
class Grambank(CustomModelMixin, Dataset):
    pk = Column(Integer, ForeignKey('dataset.pk'), primary_key=True)

    def formatted_editors(self):
        return 'The Grambank Consortium'


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

    @property
    def coders(self):
        coders = {}
        datapoints = collections.Counter()
        for vs in self.valuesets:
            for coder in vs.contribution.primary_contributors:
                datapoints.update([coder.id])
                coders[coder.id] = coder
        return [coders[cid] for cid, _ in datapoints.most_common()]


@implementer(interfaces.IParameter)
class Feature(CustomModelMixin, Parameter, Versioned):
    """Parameters in GramBank are called features. They are always related to one Designer.
    """
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    representation = Column(Integer)
    patron = Column(String)
    name_french = Column(String)
