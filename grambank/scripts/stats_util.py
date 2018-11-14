from __future__ import print_function
from itertools import groupby
import functools
import math
import collections


uchar = '?'
undefined = {}
undefined['?'] = uchar
undefined['n/a'] = uchar
undefined['N/A'] = uchar
undefined['n.a.'] = uchar
undefined['n.a'] = uchar
undefined['N.A.'] = uchar
undefined['N.A'] = uchar
undefined['-'] = uchar
undefined[''] = uchar
undefined[None] = uchar
undefined[()] = uchar
undefined["NODATA"] = uchar
undefined['? - Not known'] = uchar

dottemplate = """digraph G {
%s
}
"""


def dot(H, V=[]):
    return dottemplate % ''.join(
        ['   %s -> %s [label="%.2f"];\n' % (f1, f2, v) for ((f1, f2), v) in H.items()] + ['   %s;\n' % f for f in V])


def avg(xs):
    return sum(xs)/float(len(xs))


def argm(d, f=max):
    if len(d) == 0:
        return None
    (v, m) = f([(v, k) for k, v in d.items()])
    return m


fd = collections.Counter


def norm(d):
    z = float(sum(d.values()))
    if z == 0.0:
        return {k: 0.0 for k, _ in d.items()}
    return {k: x/z for k, x in d.items()}


def allmax(d, f=max):
    if not d:
        return {}
    mv = f(d.values())
    return {k: v for k, v in d.items() if v == mv}


def group(grouper, l):
    return {
        k: [grouper(v)[1] for v in vals] for k, vals in groupby(
            sorted(l, key=lambda m: grouper(m)[0]), lambda m: grouper(m)[0])}


grp = functools.partial(group, lambda m: (str(m[0] if m else None), m[1:]))
grp2 = functools.partial(group, lambda m: (m[0], m[1]))


def lg(z):
    return math.log(z, 2) if z != 0 else 0.0


def ent(pij, pi, pj):
    return pij*lg(pij/(pi*pj))


def entp(pd):
    return -sum([px * lg(px) for px in pd.values()])


def I(X, Y, XY):    
    return sum([ent(XY.get((x, y), 0), px, py) for (x, px) in X.items() for (y, py) in Y.items()])


def percent(k, n):
    return "%.1f" % (100*(k/float(n))) + "%"


def vtable(f):
    n = sum(f.values())
    return [k + (f[k], percent(f[k], n)) if type(k) == type(()) else (k, f[k], percent(f[k], n)) for k in sorted(f.keys())] + [("Total",) + tuple(["" for i in range(1, max([len(k) if type(k) == type(()) else 1 for k in f.keys()] + [0]))]) + (n, "")]


def jnt(X, Y):
    U = set(X.keys()).intersection(Y)
    XY = dict([(z, (X[z], Y[z])) for z in U])
    fx = fd([X[z] for z in U])
    fy = fd([Y[z] for z in U])
    fxy = fd([XY[z] for z in U])
    x = norm(fx)
    y = norm(fy)
    xy = norm(fxy)
    dstats = {"f1stats": vtable(fx), "f2stats": vtable(fy), "f1f2stats": vtable(fxy), "representation": len(U)}
    return ((x, y, xy), dstats)


def pi(X, Y, XY):
    i = I(X, Y, XY) 
    iy = entp(Y)
    strength = i/iy if iy != 0.0 else 0.0
    istats = {"f1h": entp(X), "f2h": iy, "f1f2h": entp(XY), "f1f2mi": i}
    return (strength, istats)


