from itertools import chain
import math

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
def dot(H, V = []):
    return dottemplate % ''.join(['   %s -> %s [label="%.2f"];\n' % (f1, f2, v) for ((f1, f2), v) in H.iteritems()] + ['   %s;\n' % f for f in V])


def argm(d, f = max):
    if len(d) == 0:
        return None
    (v, m) = f([(v, k) for (k, v) in d.iteritems()])
    return m


def fd(ws):
    d = {}
    for w in ws:
        d[w] = d.get(w, 0) + 1
    return d

def norm(d):
    z = float(sum(d.itervalues()))
    if z == 0.0:
        return dict([(k, 0.0) for (k, _) in d.iteritems()])
    return dict([(k, x/z) for (k, x) in d.iteritems()])


def allmax(d, f=max):
    if not d:
        return {}
    mv = f(d.itervalues())
    return dict([(k, v) for (k, v) in d.iteritems() if v == mv])

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

def grp2(l):
    def sdl(d, k, v):
        if d.has_key(k):
            d[k][len(d[k])] = v
        else:
            d[k] = {0: v}
    r = {}
    for (x, y) in l:
        sdl(r, x, y)
    return dict([(k, vs.values()) for (k, vs) in r.iteritems()])    


#def grp(xs):
#    return dict([(g, [tup[1:] for tup in tups]) for (g, tups) in groupby(xs, lambda x: x[0])])

def leaves(d):
    if not d:
        return set()
    l = set([k for (k, v) in d.iteritems() if not v])
    return l.union(chain(*[leaves(v) for (k, v) in d.iteritems() if v]))

def paths_to_d(pths):
    if pths == [()] or pths == [[]]:
        return None
    return dict([(p, paths_to_d(tails)) for (p, tails) in grp(pths).iteritems()])

def sumds(ds):
    r = {}
    for (i, v) in chain(*[d.iteritems() for d in ds]):
        r[i] = r.get(i, 0) + v
    return r

def stability_tp(lv, fp):
    ftp = {}
    for (fam, famt) in fp.iteritems():
        if not leaves({fam: famt}).intersection(lv):
            continue
        (t, pr) = prr(fam, lv, fp)
        if not t:
            continue
        tr = transitions(t)
        ftp[fam] = [((tf, tt), (pr[tf], pr[tt])) for (tf, tt) in tr]
    return ftp        

def prune(d, lvs):
    if not d:
        return d
    ls = [(k, v) for (k, v) in d.iteritems() if not v and k in lvs]
    sdl = [(k, prune(v, lvs)) for (k, v) in d.iteritems() if v]
    return dict(ls + [(k, v) for (k, v) in sdl if v and len(v) != 1] + [(a, b) for (k, v) in sdl if v and len(v) == 1 for (a, b) in v.iteritems()])


def prr(f, a, fp):
    dlgs = leaves(fp.get(f, dict.fromkeys(a))).intersection([lg for (lg, v) in a.iteritems() if not undefined.has_key(v)])
    t = prune({f: fp.get(f, dict.fromkeys(a))}, dlgs)
    done = parsimony_reconstruct(t, a)
    r = dict([(k, v) for (k, v) in a.iteritems() if k in dlgs])
    for (n, rd) in done.iteritems():
        r[n] = '/'.join(allmax(rd, min).keys())
    return (t, r)

def transitions(t):
    if not t:
        return []
    thislev = [(k, kp) for (k, v) in t.iteritems() if v for kp in v.keys()]
    return thislev + [ti for (k, v) in t.iteritems() if v for ti in transitions(v)]

def trcount(tp):
    tpc = [[(tfi, tti) for tfi in tf.split("/") for tti in tt.split("/")] for (tf, tt) in tp]
    s = {}
    for (k, v) in [((tfi, tti), 1/float(len(tpci))) for tpci in tpc for (tfi, tti) in tpci]:
        s[k] = s.get(k, 0) + v
    return s

#def stability_ftp(lv, fp):
#    return dict([(l, trcount([(tf, tt) for (label, (tf, tt)) in labeled_tr])) for (l, labeled_tr) in stability_tp(lv, fp).iteritems()])

def stability_ftp(lv, fp):
    return [(l, label, tft) for (l, labeled_tr) in stability_tp(lv, fp).iteritems() for (label, tft) in labeled_tr]


def feature_stability(datatriples, clfps):
    clf = paths_to_d(clfps)
    flv = dict([(feature, dict(lvs)) for (feature, lvs) in grp([(f, l, v) for (l, f, v) in datatriples if not undefined.has_key(v)]).iteritems()])
    return [(f, parsimony_stability(lv, clf)) for (f, lv) in flv.iteritems()]

def parsimony_stability(lv, fp):
    transitions = stability_ftp(lv, fp)
    u = trcount([tft for (f, label, tft) in transitions])    
    stability = sum([v for ((a, b), v) in u.iteritems() if a == b])
    total = float(sum(u.values()))
    r = {"retentions": stability, "transitions": total}
    r["stability"] = stability/total if total > 0 else None
    return (r, transitions)

def parsimony_reconstruct(fp, r):
    done = {}
    def rec(d):
        if not d:
            return None
        t = {}
        for (k, v) in d.iteritems():
            if done.has_key(k):
                t[k] = done[k]
                continue
            if v:
                t[k] = rec(v)
                done[k] = t[k]
                continue
            if r.has_key(k) and r[k] != "NODATA": #TODO
                t[k] = {r[k]: 0}

        tvals = [x for x in t.values() if x != None]
        if not tvals:
            return None
        return dict([(k, sum([min(d.get(k, 1), 1+min(d.values())) for d in tvals])) for k in types])
    types = set(r.values())
    rd = rec(fp)
    return done #allmax(rd, min)

def lg(z):
    if z == 0:
        return 0.0
    return math.log(z, 2)

def ent(pij, pi, pj):
    return pij*lg(pij/(pi*pj))

def entp(pd):
    return -sum([px * lg(px) for px in pd.itervalues()])

def I(X, Y, XY):    
    I = sum([ent(XY.get((x, y), 0), px, py) for (x, px) in X.iteritems() for (y, py) in Y.iteritems()])
    return I

#E.g. X = {L1: 'a', L2: 'a'} Y = {L1: 'a', L2: 'b'}
def implies((X, Y)):
    ((x, y, xy), dstats) = jnt(X, Y)
    (strength, istats) = pi(x, y, xy)
    return (strength, dict(dstats.items() + istats.items()))
    
def percent(k, n):
    return "%.1f" % (100*(k/float(n))) + "%"

def vtable(f):
    n = sum(f.itervalues())
    return [k + (f[k], percent(f[k], n)) if type(k) == type(()) else (k, f[k], percent(f[k], n)) for k in sorted(f.iterkeys())] + [("Total",) + tuple(["" for i in range(1, max([len(k) if type(k) == type(()) else 1 for k in f.iterkeys()] + [0]))]) + (n, "")]
    
def jnt(X, Y):
    U = set(X.iterkeys()).intersection(Y)
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

def has_cycle(G):
    def find_cycle_to_ancestor(node, ancestor):
        """
        Find a cycle containing both node and ancestor.
        """
        path = []
        while (node != ancestor):
            if (node is None):
                return []
            path.append(node)
            node = spanning_tree[node]
        path.append(node)
        path.reverse()
        return path
   
    def dfs(node):
        """
        Depht-first search subfunction.
        """
        visited[node] = 1
        # Explore recursively the connected component
        for each in graph.get(node, []):
            if (cycle):
                return
            if (each not in visited):
                spanning_tree[each] = node
                dfs(each)
            else:
                cycle.extend(find_cycle_to_ancestor(node, each))

    graph = dict([(k, dict(vs)) for (k, vs) in grp2([(x, (y, v)) for ((x, y), v) in G.iteritems()]).iteritems()])
    visited = {}              # List for marking visited and non-visited nodes
    spanning_tree = {}        # Spanning tree
    cycle = []

    # Algorithm outer-loop
    for each in graph:
        # Select a non-visited node
        if (each not in visited):
            spanning_tree[each] = None
            # Explore node's connected component
            dfs(each)
            if (cycle):
                return cycle
    return None


#MSTs = [GT(edmonds.mst(x, G)) for x in fr.keys() if G.has_key(x)]
def mst(G, r, it = 0):
    def contract(G, c, it):
        cnodes = set([x for p in c.keys() for x in p])
        Gc = dict([((x, y), v) for ((x, y), v) in G.iteritems() if (x not in cnodes) and (y not in cnodes)])
        VC = set([x for p in G.keys() for x in p]).difference(cnodes)
        octrack = {}
        for v in VC:
            oc = [(G[cx, v], cx) for cx in cnodes if G.has_key((cx, v))]
            if oc:
                Gc['C' + str(it), v] = max(oc)[0]
                octrack[v] = max(oc)[1]

        ictrack = {}
        for v in VC:
            ic = [(G[v, cx] - G[[y for (y, z) in c.keys() if z == cx][0], cx] + sum(c.values()), cx) for cx in cnodes if G.has_key((v, cx))]
            if ic:
                Gc[v, 'C' + str(it)] = max(ic)[0]
                ictrack[v] = max(ic)[1]
        return (Gc, octrack, ictrack)
    #Chu-Liu-Edmonds(G, s)
    #Graph G = (V,E)
    #Edge weight function s : E \to R
    I = dict([(k, dict(vs)) for (k, vs) in grp2([(y, (x, v)) for ((x, y), v) in G.iteritems()]).iteritems()])
    M = [(argm(ixs), x) for (x, ixs) in I.iteritems()]
    GM = dict([((u, v), G[(u, v)]) for (u, v) in M if v != r])
    #print "Iter", it
    #print "G nodes", len(setall(G.keys())), "edges", len(G)
    #print "GM nodes", len(setall(GM.keys())), "edges", len(GM)
    clist = has_cycle(GM)
    #print "trying", GM
    if not clist:
        #print "OK"
        return GM
    #print "cycle found", clist
    #print
    
    ces = [(clist[i], clist[i+1]) for i in range(len(clist)-1)] + [(clist[-1], clist[0])]
    c = dict([(k, G[k]) for k in ces])
    (Gc, octrack, ictrack) = contract(G, c, it)
    #print G, "contracted to", Gc
    #print "itrack", ictrack
    #print "otrack", octrack
    #if not Gc:
    #    weak = argm(GM, min)
    #    Y = dict([(edge, G[edge]) for edge in M if edge != weak])
    #    return Y
    #else:
    Y = mst(Gc, r, it + 1)
    #print it, "Tree edges", len(setall(Y.keys())), "from", len(setall(Gc.keys()))
    #xs = [([(xpp, ex) for (xpp, ex) in c.keys() if ex == x], x) for (xp, x) in Y.keys()]
    #(xpp, x) = [(xpp[0], x) for (xpp, x) in xs if xpp][0]

    U = dict([((x, y), v) for ((x, y), v) in Y.iteritems() if x != ('C'+ str(it)) and y != ('C' + str(it))])
    #print "All edges except contracted item", 'C' + str(it), U
    intoc = [x for ((x, y), v) in Y.iteritems() if y == 'C' + str(it)]
    #print "Intoc", [x for ((x, y), v) in Y.iteritems() if y == 'C' + str(it)]
    outoc = [y for ((x, y), v) in Y.iteritems() if x == 'C' + str(it)]
    #print it, "Reconstructing", len(U), "outside cycle", intoc, outoc
    #print intoc, ictrack[intoc], octrack[outoc], outoc
    #print
    if intoc:
        U[intoc[0], ictrack[intoc[0]]] = G[intoc[0], ictrack[intoc[0]]]
    if outoc:
        U[octrack[outoc[0]], outoc[0]] = G[octrack[outoc[0]], outoc[0]]

    for x in intoc:
        U[x, ictrack[x]] = G[x, ictrack[x]]
    for y in outoc:
        U[octrack[y], y] = G[octrack[y], y]
    for ((x, y), v) in c.iteritems():
        U[x, y] = v

    for (x, y) in c.iterkeys():
        if [(xpp, z) for (xpp, z) in U.iterkeys() if z == y and xpp != x]:
            del U[x, y]
            break
    else:
        print "ERROR NO KICKOUT", c
    return U


def both_defined(lv1, lv2):
    u = [x for x in set(lv1.iterkeys()).intersection(lv2.iterkeys()) if not undefined.has_key(lv1[x]) and not undefined.has_key(lv2[x])] 
    return (dict([(x, lv1[x]) for x in u]), dict([(x, lv2[x]) for x in u])) 

def feature_dependencies(datatriples):
    flv = dict([(feature, dict(lvs)) for (feature, lvs) in grp([(f, l, v) for (l, f, v) in datatriples]).iteritems()])
    imps = [(implies(both_defined(lv1, lv2)), f1, f2) for (f1, lv1) in flv.iteritems() for (f2, lv2) in flv.iteritems() if f1 != f2]
    return imps

def dependencies_graph(imps):
    deps = dict([((f1, f2), v) for (v, f1, f2) in imps if v > 0.0])
    V = set([f for fs in deps.iterkeys() for f in fs])
    G = dict([(k, v) for (k, v) in deps.items() if v > 0.0])
    MSTs = [mst(G, x) for x in V]
    (mv, H) = max([(sum(H.values()), H) for H in MSTs])
    #W = dict([(y, 1.0-v) for ((x, y), v) in H.iteritems()])
    #sav(dot(H, V), 'grambank_mst.gv')
    return (H, V) #dot(H, V)


def deepfamilies():
    a = 1
    #PRR
    #Stability
    #Sim = Ham * stab


#    \item Automatically discovered feature dependencies
#\item Automatically drawn isogloss-lines on the map
#\item Automatically reconstructed historical trees
#\item \ldots{}



