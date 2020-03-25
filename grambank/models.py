import collections

from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Integer,
    Unicode,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models.common import Contribution, Parameter, Language, Contributor, Dataset
from clld_glottologfamily_plugin.models import HasFamilyMixin


@implementer(interfaces.IDataset)
class Grambank(CustomModelMixin, Dataset):
    pk = Column(Integer, ForeignKey('dataset.pk'), primary_key=True)

    def formatted_editors(self):
        return 'The Grambank Consortium'


@implementer(interfaces.ILanguage)
class GrambankLanguage(CustomModelMixin, Language, HasFamilyMixin):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    macroarea = Column(Unicode)
    representation = Column(Integer)
    nzrepresentation = Column(Integer)
    contribution_pk = Column(Integer, ForeignKey('contribution.pk'))
    contribution = relationship(Contribution)

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
class Feature(CustomModelMixin, Parameter):
    """Parameters in GramBank are called features. They are always related to one Designer.
    """
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    representation = Column(Integer)
    patron_pk = Column(Integer, ForeignKey('contributor.pk'))
    patron = relationship(Contributor)
    name_french = Column(String)
