# -*- coding: utf-8 -*-
from trytond.pool import Pool
from tree import (
    Product, Node, ProductNodeRelationship,
    Website, WebsiteTreeNode,
)


def register():
    Pool.register(
        Product,
        Node,
        ProductNodeRelationship,
        Website,
        WebsiteTreeNode,
        module='nereid_catalog_tree',
        type_='model'
    )
