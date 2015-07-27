from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.versioned import Versioned
from clld.db.models.common import Parameter, Language

from clld_glottologfamily_plugin.models import HasFamilyMixin


@implementer(interfaces.ILanguage)
class GrambankLanguage(CustomModelMixin, Language, HasFamilyMixin):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)


class FeatureDomain(Base, Versioned):
    name = Column(Unicode, unique=True)


@implementer(interfaces.IParameter)
class Feature(CustomModelMixin, Parameter):
    """Parameters in GramBank are called features. They are always related to one Designer.
    """
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    doc = Column(String)
    newdoc = Column(String)
    vdoc = Column(String)
    std_comments = Column(String)
    name_french = Column(String)
    clarification = Column(String)
    alternative_id = Column(String)
    representation = Column(Integer)
    featuredomain_pk = Column(Integer, ForeignKey('featuredomain.pk'))
    featuredomain = relationship(FeatureDomain, lazy='joined')
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


#\* Feature number
#Feature question in English
#Value set
#suggested standardised comments
#progress on new description
#Feature question in French
#Relevant unit(s)
#Function
#Formal means
#Legacy status
#GramBank-status
#Draft of clarifying comments to outsiders (from the proposal by Jeremy, Hannah and Hedvig
#Work in progress comment
#NTS or GramBank?
#Very hard to deny
#Prone to misunderstandings among researchers
#Requires extensive data on the language
#Last edited
#Is there a typological survey that already covers this feature somehow?
