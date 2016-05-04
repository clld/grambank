from clldclient.glottolog import Glottolog as OnlineGlottolog
from clld_glottologfamily_plugin.util import ORDERED_ICONS, ISOLATES_ICON, Family
from clld.db.models.common import IdentifierType, Identifier
from clld.scripts.util import add_language_codes

from itertools import cycle

import re

class LocalLanguoid():
    def __init__(self, name = "", latitude = None, longitude = None, iso_code = None, glottocode = None, parent = None, family = None, children = [], macroareas = []):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.iso_code = iso_code
        self.glottocode = glottocode
        self.parent = parent
        self.family = family
        self.children = children
        self.macroareas = macroareas
        self.id = glottocode

class LocalGlottolog(OnlineGlottolog):
    def languoid(self, x):
        onlineglottolog = OnlineGlottolog()
        try:
            lg = onlineglottolog.languoid(x)
        except AttributeError:
            try:
                gfp = gtreetxt(loadunicode("C:\\python27\\glottolog\\build\\dff.txt"))
            except IOError:
                return None

            for ((name, gc, iso), pth) in codeclf(gfp).iteritems():
                if gc == x:
                    gcpth = [getbrack(p) for p in pth]
                    parentcode = gcpth[-1] if gcpth else None
                    parent = onlineglottolog.languoid(parentcode)
                    return LocalLanguoid(glottocode = gc, name = name, parent = parent, family = parent.family, macroareas = parent.macroareas, latitude = parent.latitude, longitude = parent.longitude)
            return None
        return lg

def grp(l):
    def sdl(d, k, v):
        if d.has_key(k):
            d[k][len(d[k])] = v
        else:
            d[k] = {0: v}
    r = {}
    for x in l:
        sdl(r, x[0] if x else None, x[1:])
    return dict([(k, vs.values()) for (k, vs) in r.iteritems()])    

def paths_to_d(pths):
    if pths == [()] or pths == [[]]:
        return None
    #print pths[0]
    z = grp(pths)
    return {k: paths_to_d(v) for (k, v) in z.iteritems()}

def loadunicode(fn, encoding = "utf-8"):
    f = open(fn, "r")
    a = f.read()
    f.close()
    utxt = unicode(a, encoding)
    if utxt.startswith(u'\ufeff'):
        utxt = utxt[1:]
    if utxt.startswith(u'# -*- coding: utf-8 -*-\n'):
        utxt = utxt[len(u'# -*- coding: utf-8 -*-\n'):]
    return utxt


reinfirstbrack = re.compile("[^\[]+\[(?P<gc>[^\]]+)\][^\n]*$")
def getbrack(s):
    return reinfirstbrack.match(s.strip()).group("gc")

rengciso = re.compile("\s+(?P<name>[^\[]+)\s+\[(?P<gc>[a-z][a-z][a-z][a-z\d]\d\d\d\d+)\]\[(?P<iso>[a-zA-Z][a-zA-Z][a-zA-Z]|NOCODE\_[A-Z][^\s\]]+)?\]$")
def gtreetxt(txt):
    ls = [l.rstrip() for l in txt.split("\n") if l.strip()]
    r = {}
    thisclf = None
    for l in ls:
        o = rengciso.match(l)
        if o:
            r[thisclf + ((o.group("name"), o.group("gc"), o.group("iso")),)] = None
        else:
            thisclf = tuple(l.split(", "))

    return paths_to_d(r.iterkeys())

def setall(xs):
    a = set()
    for x in xs:
        a.update(x)
    return a

def grp2l(l):
    r = {}
    for (a, b) in l:
        r[a] = r.get(a, [])
        r[a].append(b)
    return r

def paths(d):
    if not d:
        return set([])
    if type(d) == type(""):
        print d
    l = set([(k,) for (k, v) in d.iteritems() if not v])
    return l.union(setall([[(k,) + p for p in paths(v)] for (k, v) in d.iteritems() if v]))

def codeclf(e):
    ps = paths(e)
    pcheck = grp2l([(p[-1], p[:-1]) for p in ps])
    for x in [(k, pths) for (k, pths) in pcheck.iteritems() if len(pths) != 1]:
        print "DUPL:", x
    path = dict([(p[-1], p[:-1]) for p in ps])
    return path

#cjin1234
#stan1295


def load_families(data, languages, icons=ORDERED_ICONS, isolates_icon=ISOLATES_ICON):
    """Add Family objects to a database and update Language object from Glottolog.
    Family information is retrieved from Glottolog based on the id attribute of a
    language. This id must be either a glottocode or an ISO 639-3 code.
    :param data:
    :return:
    """
    icons = cycle([getattr(i, 'name', i) for i in icons if getattr(i, 'name', i) != isolates_icon])
    glottolog = LocalGlottolog()

    for language in languages:
        if isinstance(language, (tuple, list)) and len(language) == 2:
            code, language = language
        else:
            code = language.id
        gl_language = glottolog.languoid(code)
        if gl_language:
            gl_family = gl_language.family
            if gl_family:
                family = data['Family'].get(gl_family.id)
                if not family:
                    family = data.add(
                        Family,
                        gl_family.id,
                        id=gl_family.id,
                        name=gl_family.name,
                        description=Identifier(
                            name=gl_family.id, type=IdentifierType.glottolog.value).url(),
                        jsondata=dict(icon=icons.next()))
                language.family = family

            language.macroarea = gl_language.macroareas[0]
            add_language_codes(
                data, language, gl_language.iso_code, glottocode=gl_language.id)
            for attr in 'latitude', 'longitude', 'name':
                if getattr(language, attr) is None:
                    setattr(language, attr, getattr(gl_language, attr))

        
