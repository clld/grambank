"""
Recreate glottolog data files from the current version published at http://glottolog.org
"""
import re

from ete3 import Tree


def iter_trees(glottocodes, glottolog):  # pragma: no cover
    label_pattern = re.compile("'[^\[]+\[([a-z0-9]{4}[0-9]{4})[^']*'")

    def rename(n):
        n.name = label_pattern.match(n.name).groups()[0]
        n.length = 1

    glottocodes = set(glottocodes)
    languoids = {}
    families = []
    for lang in glottolog.languoids():
        if not lang.lineage:  # a top-level node
            if not lang.category.startswith('Pseudo '):
                families.append(lang)
        languoids[lang.id] = lang

    for family in sorted(families, key=lambda f: f.name):
        node = family.newick_node(nodes=languoids)
        node.visit(rename)
        langs_in_tree = set(n.name for n in node.walk())
        langs_selected = glottocodes.intersection(langs_in_tree)
        if not langs_selected:
            continue

        tree = Tree("({0});".format(node.newick), format=3)
        tree.name = 'glottolog_{0}'.format(family.id)
        if family.level.name == 'family':
            tree.prune(langs_selected)
            yield tree
