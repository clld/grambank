"""
This module will be available in templates as ``u``.

This module is also used to lookup custom template context providers, i.e. functions
following a special naming convention which are called to update the template context
before rendering resource's detail or index views.
"""
from __future__ import division, unicode_literals

from sqlalchemy import func, desc, text
from sqlalchemy.orm import joinedload

from clld import RESOURCES
from clld.web.util.helpers import get_referents
from clld.web.util.htmllib import HTML
from clld.db.meta import DBSession
from clld.db.models.common import (
    Contributor, ValueSet, Contribution, ContributionContributor, Language,
)
from clld_glottologfamily_plugin.models import Family
from clld.web.icon import SHAPES
from clld.interfaces import IIcon
from clld.web.util.multiselect import CombinationMultiSelect

from grambank.maps import DeepFamilyMap
from grambank.models import Dependency, Transition, GrambankLanguage

COLORS = [
    #            red     yellow
    "00ff00", "ff0000", "ffff00", "0000ff", "ff00ff", "00ffff", "000000",
]


def phylogeny_detail_html(request=None, context=None, **kw):
    return {
        'ms': CombinationMultiSelect,
    }


def table_incidence(*ds):
    values = set([x for d in ds for x in d.keys()])
    totals = [sum(d.values()) for d in ds]
    cellrows = [(value, [(HTML.td("%.1f" % d.get(value, 0.0), class_='right'), HTML.td('\xa0%.1f%%\xa0' % (100*d.get(value, 0.0)/float(total)), class_='right', style='background-color: hsl({0},100%,50%)'.format((d.get(value, 0.0)/float(total)) * 120))) for (d, total) in zip(ds, totals)]) for value in sorted(values)] + [('Total', [(HTML.td("%s" % int(total), class_='right'), HTML.td("")) for total in totals])]
    
    rows = [''.join([HTML.td(value, class_='left')] + [cell for cellpair in row for cell in cellpair]) for (value, row) in cellrows]
    
    return ''.join(["<tr>%s</tr>\n" % row for row in rows])

def td_coverage(glottolog=0, grambank=0, label=None):
    style = ''
    if glottolog == 0:
        style = 'background-color: hsl(120,100%,50%)'
        if grambank == 0:
            percentage = 0
        else:
            percentage = 1
    else:
        percentage = grambank / glottolog
    return HTML.td(
        label if label else '\xa0%s%%\xa0' % int(round(percentage * 100)),
        class_='left' if label else 'center',
        style=style or 'background-color: hsl({0},100%,50%)'.format((percentage) * 120))


def source_detail_html(context=None, request=None, **kw):
    return dict(referents=get_referents(context, exclude=[
        'language',
        'sentence',
        'contribution',
        #'valueset',
    ]))


def contributor_detail_html(context=None, request=None, **kw):
    counts = {
        r[0]: r[1] for r in DBSession.query(Language.pk, func.count(ValueSet.pk))
        .join(ValueSet)
        .join(Contribution)
        .join(ContributionContributor)
        .filter(ContributionContributor.contributor_pk == context.pk)
        .group_by(Language.pk)}
    languages = []
    for lang in DBSession.query(Language) \
            .join(Family) \
            .join(ValueSet) \
            .join(Contribution) \
            .join(ContributionContributor) \
            .filter(ContributionContributor.contributor_pk == context.pk) \
            .order_by(Family.name, Language.name) \
            .options(joinedload(GrambankLanguage.family)):
        languages.append((lang, counts[lang.pk]))
    return {'languages': languages}


def dataset_detail_html(context=None, request=None, **kw):
    contribs = DBSession.query(Contributor.name, func.count(ValueSet.id).label('c'))\
        .join(
            Contributor.contribution_assocs,
            ContributionContributor.contribution,
            Contribution.valuesets)\
        .group_by(Contributor.name)\
        .order_by(desc(text('c')))
    return dict(
        contribs=contribs,
        stats=context.get_stats(
            [rsc for rsc in RESOURCES if rsc.name in ['language', 'parameter', 'value']]),
    )


def combination_detail_html(context=None, request=None, **kw):
    [f1, f2] = context.parameters[:2]
    [dependency] = list(DBSession.query(Dependency).filter(Dependency.feature1_pk == f1.pk, Dependency.feature2_pk == f2.pk))
    r = dependency.jsondata
    r["f1id"] = f1.id
    r["f2id"] = f2.id
    r["f1f2id"] = dependency.id
    r["strength"] = dependency.strength if r["f2h"] > 0.0 else "-"
    r["combinatory_status"] = dependency.combinatory_status
    return {'dependency': r}


def stability_detail_html(context=None, request=None, **kw):
    def norm(d):
        z = float(sum(d.values()))
        if z == 0.0:
            return {k: v for k, v in d.items()}
        return {k: v/z for k, v in d.items()}
    
    def transition_counts_to_matrix(u):
        kall = set(k for ks in u.keys() for k in ks)
        return {k1: norm({k2: u.get((k1, k2), 0) for k2 in kall}) for k1 in kall}

    def sumk(l):
        r = {}
        for (k, v) in l:
            r[k] = r.get(k, 0.0) + v
        return r

    def trcount(transitions):
        tpc = [[(tfi, tti) for tfi in tf.split("/") for tti in tt.split("/")] for (tf, tt) in transitions]
        return sumk([(t, 1/float(len(tpci))) for tpci in tpc for t in tpci])
    
    transitions = DBSession.query(Transition.fromvalue, Transition.tovalue).filter(Transition.stability_pk == context.pk)
    u = trcount(transitions)
    m = transition_counts_to_matrix(u)
    vtotal = sumk([(k1, v) for ((k1, k2), v) in u.items()])
    retentions = dict([(k1, v) for ((k1, k2), v) in u.items() if k1 == k2])
    scounts = [(k, v, vtotal.get(k, 0)) for (k, v) in sorted(retentions.items())] + [("Total", sum(retentions.values()), sum(u.values()))]
    s = [(k, v, t, ("%.5f" % (float(v)/t)) if t > 0 else "-") for (k, v, t) in scounts]
    return {'transition_counts': u, 'transition_matrix': m, 'stability_table': s, 'state_total': vtotal}


def deepfamily_detail_html(request=None, context=None, **kw):
    #family1_pk = Column(Integer, ForeignKey('family.pk'))
    #family1_latitude = Column(
    #family1_longitude = Column(
    #family2_pk = Column(Integer, ForeignKey('family.pk'))
    #family2_longitude = Column(
    #family2_latitude = Column(
    #[context.pk] +
    icon_map = dict(zip([context.family1_pk, context.family2_pk], [s + c for s in SHAPES for c in COLORS]))
    for key in icon_map:
        icon_map[key] = request.registry.getUtility(IIcon, icon_map[key]).url(request)
    return dict(icon_map=icon_map, lmap=DeepFamilyMap(context, request, icon_map=icon_map))
