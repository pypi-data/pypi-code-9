# -*- coding: utf-8 -*-
# Copyright (C) 2015 Sebastian Eckweiler
#
# This module is part of SQLAlchemyViz and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
from __future__ import unicode_literals
"""
Module containing the graph building logic.
"""

import itertools
import os
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


from sqlalchemy import (MetaData, ForeignKeyConstraint,
                        UniqueConstraint, PrimaryKeyConstraint,
                        Index, CheckConstraint)

import pydot
from pydot import Node, Edge, Dot

ONE = '1'
ONE_TO_N = '1-n'
ZERO_TO_N = '0-n'
ZERO_TO_ONE = '0-1'


default_config = {'cell_align': 'left',
                  'table_border': '1',
                  'table_cellborder': '0',
                  'table_cellspacing': '0',
                  'table_bgcolor': 'azure2',
                  'node_shape': 'box',
                  'node_margin': '0,0',
                  'graph_bgcolor': 'transparent',
                  'graph_orientation': 'portrait',
                  'edge_dir': 'both',
                  'edge_len': '3'}

default_kwargs = {'sort_columns': True,
                  'unique_relations': True,
                  'show_constraints': False,
                  'max_cols': 0}

arrowstyles = {ONE: "noneteetee",
               ZERO_TO_ONE: "noneteeodot",
               ZERO_TO_N: "crowodot",
               ONE_TO_N: "crowtee"}


column_fmt = '%(name)s : %(type)s'

_valid_configs = dict(graph=pydot.GRAPH_ATTRIBUTES.copy(),
                      edge=pydot.EDGE_ATTRIBUTES.copy(),
                      node=pydot.NODE_ATTRIBUTES.copy(),
                      table={"align", "bgcolor", "border", "cellborder",
                             "cellpadding", "cellspacing", "color",
                             "columns", "fixedsize", "gradientangle",
                             "height", "href", "id", "port", "rows",
                             "sides", "style", "target", "title",
                             "tooltip", "valign", "width"},
                      cell={"align", "balign", "bgcolor", "border",
                            "cellpadding", "cellspacing", "color",
                            "colspan", "fixedsize", "gradientangle",
                            "height", "href", "id", "port", "rowspan",
                            "sides", "style", "target", "title", "tooltip",
                            "valign", "width"})
# all
_valid_configs[None] = (_valid_configs['graph'] |
                        _valid_configs['edge'] |
                        _valid_configs['table'] |
                        _valid_configs['cell'] |
                        _valid_configs['node'])

def _pop_default(arg, kwargs=None):
    if kwargs is None:
        return default_kwargs[arg]
    else:
        return kwargs.pop(arg, default_kwargs[arg])

class ERDiagram(object):

    _prefixes = {ForeignKeyConstraint: 'FK',
                 PrimaryKeyConstraint: 'PK',
                 Index: 'IX',
                 CheckConstraint: 'CK',
                 UniqueConstraint: 'UQ'}

    _COLS = '4'

    def __init__(self, tables, **kwargs):
        """

        :param MetaData meta: MetaData describing the schema
        :return:
        """

        self.graph = None
        self.use_pytypes = False
        self.sort_columns = _pop_default('sort_columns', kwargs)
        self.unique_relations = _pop_default('unique_relations', kwargs)
        self.show_constraints = _pop_default('show_constraints', kwargs)
        self.max_cols = _pop_default('max_cols', kwargs)
        self.tables = tables

        self._config = default_config.copy()

        if kwargs:
            raise ValueError('Unknown options: %s' %
                             (',' % ['%r' for key in kwargs]))

    def update_config(self, config):
        self._config.update(config)

    def create_diagram(self):

        self.graph = Dot(splines='ortho',
                         overlap='scale',
                         **self._get_config('graph'))

        for t in self.tables:
            self.graph.add_node(self._create_node(t))

        for t in self.tables:
            for edge in self._create_edges(t):
                self.graph.add_edge(edge)

    # noinspection PyShadowingBuiltins
    def write(self, path, prog='neato', format=None):

        if not self.graph:
            self.create_diagram()

        if not format:
            _, format = os.path.splitext(path)
            if format.startswith('.'):
                format = format[1:]

        self.graph.write(path, prog, format)

    def _get_config(self, prefix):

        c = dict()
        for prefix_key, value in self._config.items():
            prefix_key = prefix_key.lower()

            if '_' in prefix_key:
                pfx, key = prefix_key.split('_', 1)
            else:
                pfx, key = None, prefix_key

            if pfx not in _valid_configs:
                valid = str(filter(None, _valid_configs))
                raise ValueError('"%s" is not a valid configuration group. '
                                 'Must be one of %s.' %
                                 (pfx, valid))

            if key not in _valid_configs[pfx]:
                valid = str(sorted(_valid_configs[pfx]))
                raise ValueError('"%s" is not a valid configuration key. '
                                 'Valid ones are: %s.' %
                                 (key, valid))

            if pfx is None or pfx == prefix:
                c[key] = value
        return c

    def _create_node(self, table):

        t = self._make_table()
        header = ET.Element('B')
        header.text = table.name
        self._make_cell(t, header,
                        border='1', sides='b',
                        colspan=self._COLS)

        cols = table.columns
        if self.sort_columns:
            cols = sorted(cols, key=lambda c: (not c.primary_key,
                                               not bool(c.foreign_keys),
                                               c.name.lower()))
        if self.max_cols:
            skipped_cols = max(0, len(cols)-self.max_cols)
            cols = cols[:self.max_cols]
        else:
            skipped_cols = 0

        for col in cols:
            r = self._make_row(t)
            attrs = self._column_attrs(col)

            flag = ""
            if attrs["primary"]:
                flag += "P"
            else:
                if attrs["unique"]:
                    flag += "U"
                if attrs["foreign"]:
                    flag += "F"
            if not flag:
                flag = " "

            if attrs["nullable"]:
                nullable = ' '
            else:
                nullable = '*'

            self._make_cell(r, flag)
            self._make_cell(r, nullable)
            self._make_cell(r, '%(name)s' % attrs)
            self._make_cell(r, '%(type)s' % attrs)

        if skipped_cols:
            self._make_cell(t, '(%i columns not shown)' % skipped_cols,
                            border='1', sides='t', colspan=self._COLS)

        # sort constraints by type:
        order = {PrimaryKeyConstraint: 0,
                 ForeignKeyConstraint: 1,
                 UniqueConstraint: 2,
                 CheckConstraint: 3,
                 Index: 4}

        constraints = sorted(table.constraints,
                             key=lambda c: order[type(c)])
        const_and_index = itertools.chain(constraints,
                                          table.indexes)

        if self.show_constraints:
            for i, c_or_idx in enumerate(const_and_index):
                if isinstance(c_or_idx, CheckConstraint):
                    continue

                if c_or_idx.name:
                    s = '%s' % c_or_idx.name
                else:
                    s = '(%s)' % ','.join(col.name for col in c_or_idx.columns)

                opts = dict(border='0' if i else '1',
                            sides='' if i else 't',
                            colspan='2')

                r = self._make_row(t)
                self._make_cell(r, self._prefixes[type(c_or_idx)], **opts)
                self._make_cell(r, s, **opts)

        return Node(table.name,
                    label='<%s>' % ET.tostring(t, method='html'),
                    **self._get_config('node'))

    def _column_attrs(self, col):

        if self.use_pytypes:
            type_name = col.type.python_type.__name__
        else:
            type_name = unicode(col.type)
        col_props = {"name": col.name,
                     "type": type_name,
                     "unique": False,
                     "nullable": col.nullable,
                     "primary": col.primary_key,
                     "foreign": bool(col.foreign_keys)}

        flags = []
        if col.primary_key:
            flags.append('P')

        unique = any(col.name in cstr.columns
                     for cstr in col.table.constraints
                     if isinstance(cstr, UniqueConstraint)
                     and len(cstr.columns) == 1)

        if unique or col.unique:
            col_props["unique"] = unique or col.unique

        return col_props

    def _create_edges(self, table):

        unique_cols = set(tuple(c.columns)
                          for c in table.constraints
                          if isinstance(c, (UniqueConstraint,
                                            PrimaryKeyConstraint)))

        seen_edges = set()
        for constraint in table.constraints:
            if not isinstance(constraint, ForeignKeyConstraint):
                continue

            # foreign table:
            ref_table = constraint.elements[0].column.table
            if ref_table not in self.tables:
                continue

            nullable = any(c.nullable for c in constraint.columns)
            unique = tuple(constraint.columns) in unique_cols

            # is also a primary key?
            primary_key = any(c.primary_key for c in constraint.columns)

            n_tail = ZERO_TO_ONE if nullable else ONE
            n_head = ONE if unique else ONE_TO_N
            style = 'solid' if primary_key else 'dashed'

            edge = (table.name, ref_table.name,
                    n_tail, n_head)

            if self.unique_relations and edge in seen_edges:
                continue
            seen_edges.add(edge)

            yield self._make_edge(table.name, ref_table.name,
                                  style=style,
                                  arrowtail=arrowstyles[n_tail],
                                  arrowhead=arrowstyles[n_head])

    def _make_edge(self, from_, to, style='solid', **kwargs):

        edge_attributes = self._get_config('edge')
        edge_attributes.update(kwargs)

        return Edge(from_, to, **edge_attributes)

    def _make_table(self):
        return ET.Element('TABLE', **self._get_config('table'))

    def _make_row(self, parent):
        return ET.SubElement(parent, 'TR')

    def _make_cell(self, parent, contents='', **kwargs):

        if parent.tag == 'TABLE':
            parent = self._make_row(parent)

        attrib = self._get_config('cell').copy()
        attrib.update(kwargs)
        c = ET.SubElement(parent, 'TD', **attrib)
        if ET.iselement(contents):
            c.append(contents)
        else:
            c.text = contents
        return c


from sqlalchemy.orm.properties import ColumnProperty
class UMLDiagram(ERDiagram):

    def __init__(self, tables, **kwargs):
        super(UMLDiagram, self).__init__(tables, **kwargs)

    def create_diagram(self):
        self._relations_seen = set()
        super(UMLDiagram, self).create_diagram()

    def _create_edges(self, mapper):

        for relation in mapper.relationships:
            if relation in self._relations_seen:
                continue

            if relation.uselist:
                arrowtail = 'ediamond'
                arrowhead = ''
            else:
                arrowhead = 'ediamond'
                arrowtail = ''

            self._relations_seen.add(relation)
            self._relations_seen.update(relation._reverse_property)

            tail_label = relation.key
            head_label = ''
            for rev_prop in relation._reverse_property:
                if rev_prop.parent.class_ is relation.mapper.class_:
                    head_label = rev_prop.key

            yield self._make_edge(relation.parent.class_.__name__,
                                  relation.mapper.class_.__name__,
                                  arrowtail=arrowtail,
                                  arrowhead=arrowhead,
                                  headlabel=head_label,
                                  taillabel=tail_label)

    def _create_node(self, mapper):
        from sqlalchemy.orm.mapper import Mapper

        t = self._make_table()

        self._make_cell(t, mapper.class_.__name__,
                        border='1', sides='b',
                        colspan='2')
        assert isinstance(mapper, Mapper)

        for attr in mapper.column_attrs:
            r = self._make_row(t)

            if isinstance(attr, ColumnProperty) and len(attr.columns) == 1:
                lbl = '+ %s: %s' % (attr.key,
                                    attr.columns[0].type.__class__.__name__)
            else:
                lbl = '+ %s'
            self._make_cell(r, lbl, colspan='2')

        return Node(mapper.class_.__name__,
                    label='<%s>' % ET.tostring(t, method='html'),
                    **self._get_config('node'))