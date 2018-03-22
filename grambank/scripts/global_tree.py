# coding: utf8
"""
Recreate glottolog data files from the current version published at http://glottolog.org
"""
from __future__ import unicode_literals
import re

from ete3 import Tree
from pyglottolog.api import Glottolog


def tree(glottocodes, gl_repos):
    label_pattern = re.compile("'[^\[]+\[([a-z0-9]{4}[0-9]{4})[^']*'")

    def rename(n):
        n.name = label_pattern.match(n.name).groups()[0]
        n.length = 1

    glottocodes = set(glottocodes)
    glottocodes_in_global_tree = set()
    languoids = {}
    families = []
    for lang in Glottolog(gl_repos).languoids():
        if not lang.lineage:  # a top-level node
            if not lang.category.startswith('Pseudo '):
                families.append(lang)
        languoids[lang.id] = lang

    glob = Tree()
    glob.name = 'glottolog_global'

    for family in sorted(families):
        node = family.newick_node(nodes=languoids)
        node.visit(rename)
        langs_in_tree = set(n.name for n in node.walk())
        langs_selected = glottocodes.intersection(langs_in_tree)
        if not langs_selected:
            continue

        tree = Tree("({0});".format(node.newick), format=3)
        tree.name = 'glottolog_{0}'.format(family.id)
        if family.level.name == 'family':
            tree.prune([n.encode('ascii') for n in langs_selected])
            glottocodes_in_global_tree = glottocodes_in_global_tree.union(
                set(n.name for n in tree.traverse()))
        else:
            glottocodes_in_global_tree = glottocodes_in_global_tree.union(langs_in_tree)
        glob.add_child(tree)

    # global
    nodes = glottocodes_in_global_tree.intersection(glottocodes)
    glob.prune([n.encode('ascii') for n in nodes])
    return glob.write(format=9), nodes
