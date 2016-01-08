from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    Float,
    Boolean,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.versioned import Versioned
from clld.db.models.common import (
    Contribution, Parameter, IdNameDescriptionMixin, Language
)
from clld_glottologfamily_plugin.models import HasFamilyMixin, Family

from interfaces import IDependency, ITransition, IStability, IDeepFamily, ISupport, IHasSupport

@implementer(interfaces.ILanguage)
class GrambankLanguage(CustomModelMixin, Language, HasFamilyMixin):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)


@implementer(interfaces.IParameter)
class Feature(CustomModelMixin, Parameter, Versioned):
    """Parameters in GramBank are called features. They are always related to one Designer.
    """
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    doc = Column(String)
    patron = Column(String)
    newdoc = Column(String)
    vdoc = Column(String)
    std_comments = Column(String)
    name_french = Column(String)
    clarification = Column(String)
    alternative_id = Column(String)
    representation = Column(Integer)
    designer = Column(String)
    abbreviation = Column(String)
    sortkey_str = Column(String)
    sortkey_int = Column(Integer)
    jl_relevant_unit = Column(String)
    jl_function = Column(String)
    jl_formal_means = Column(String)
    legacy_status = Column(String) 
    grambank_status = Column(String) 
    wip_comments = Column(String)
    nts_grambank = Column(String)
    hard_to_deny = Column(String)
    prone_misunderstanding = Column(String)
    requires_extensive_data = Column(String)
    last_edited = Column(String)
    other_survey = Column(String)

@implementer(IStability)
class Stability(Base, CustomModelMixin):
    pk = Column(Integer, primary_key=True)
    id = Column(String)
    parsimony_stability_value = Column(Float) 
    parsimony_retentions = Column(Float)
    parsimony_transitions = Column(Float)
    feature_pk = Column(Integer, ForeignKey('feature.pk'))
    feature = relationship(Feature, lazy='joined', foreign_keys = feature_pk, backref = "stability")
    

@implementer(IDependency)
class Dependency(Base, CustomModelMixin):
    pk = Column(Integer, primary_key=True)
    id = Column(String)
    feature1_pk = Column(Integer, ForeignKey('feature.pk'))
    feature1 = relationship(Feature, lazy='joined', foreign_keys = feature1_pk)
    feature2_pk = Column(Integer, ForeignKey('feature.pk'))
    feature2 = relationship(Feature, lazy='joined', foreign_keys = feature2_pk)
    strength = Column(Float)
    representation = Column(Integer)
    combinatory_status = Column(String)

@implementer(ITransition)
class Transition(Base, CustomModelMixin):
    pk = Column(Integer, primary_key=True)
    id = Column(String)
    fromnode = Column(String)
    fromvalue = Column(String)
    tonode = Column(String)
    tovalue = Column(String)
    stability_pk = Column(Integer, ForeignKey('stability.pk'))
    stability = relationship(Stability, lazy='joined', foreign_keys = stability_pk)
    family_pk = Column(Integer, ForeignKey('family.pk'))
    family = relationship(Family, backref='transitions')
    retention_innovation = Column(String)
    
@implementer(interfaces.IContribution)
class GrambankContribution(CustomModelMixin, Contribution):
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    desc = Column(String)

@implementer(IDeepFamily)
class DeepFamily(Base, CustomModelMixin):
    pk = Column(Integer, primary_key=True)
    id = Column(String)
    family1_pk = Column(Integer, ForeignKey('family.pk'))
    family1 = relationship(Family, lazy='joined', foreign_keys = family1_pk)
    family1_longitude = Column(
        Float(),
        CheckConstraint('-180 <= family1_longitude and family1_longitude <= 180 '),
        doc='geographical longitude in WGS84')
    family1_latitude = Column(
        Float(),
        CheckConstraint('-90 <= family1_latitude and family1_latitude <= 90'),
        doc='geographical latitude in WGS84')
    family2_pk = Column(Integer, ForeignKey('family.pk'))
    family2 = relationship(Family, lazy='joined', foreign_keys = family2_pk)
    family2_longitude = Column(
        Float(),
        CheckConstraint('-180 <= family2_longitude and family2_longitude <= 180 '),
        doc='geographical longitude in WGS84')
    family2_latitude = Column(
        Float(),
        CheckConstraint('-90 <= family2_latitude and family2_latitude <= 90'),
        doc='geographical latitude in WGS84')
    support_value = Column(Float)
    significance = Column(Float)
    geographic_plausibility = Column(Float)
    
@implementer(ISupport)
class Support(Base, CustomModelMixin):
    pk = Column(Integer, primary_key=True)
    id = Column(String)
    value1 = Column(String)
    value2 = Column(String)
    historical_score = Column(Float)
    independent_score = Column(Float)
    support_score = Column(Float)
    feature_pk = Column(Integer, ForeignKey('feature.pk'))
    feature = relationship(Feature, lazy='joined', foreign_keys = feature_pk)

@implementer(IHasSupport)
class HasSupport(Base, CustomModelMixin):
    id = Column(String)
    deepfamily_pk = Column(Integer, ForeignKey('deepfamily.pk'), primary_key=True)
    deepfamily = relationship(DeepFamily, lazy='joined', foreign_keys = deepfamily_pk)
    support_pk = Column(Integer, ForeignKey('support.pk'), primary_key=True)
    support = relationship(Support, lazy='joined', foreign_keys = support_pk)
    
    
