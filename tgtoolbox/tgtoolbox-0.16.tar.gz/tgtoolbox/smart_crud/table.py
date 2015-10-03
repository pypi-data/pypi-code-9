# -*- coding: utf-8 -*-
# import sqlalchemy
# from sqlalchemy.sql.elements import Label as sql_label
from tg import request
from tg.render import render
from sqlalchemy import desc
from collections import OrderedDict
from markupsafe import Markup
from .sort import Sort
from .format import Formatter
from .column import Column as TableColumn
from .sa_helpers import extract_columns
__author__ = 'vahid'

class SmartTable(object):
    template = "tgtoolbox.smart_crud.templates.smart_table"
    allow_new = True
    allow_delete = True
    allow_edit = True
    limit_max_rows = None
    limit_min_rows = None

    def __init__(self, session, query=None, paginator_key='data'):
        self.session = session # Not used yet !
        self._query = query

        self.total_count = 0
        self.can_new = False
        self.can_delete = False
        self.can_edit = False

        self.sorts = []
        self.columns = []
        self.paginator_key = paginator_key

    def get_query(self):
        return self._query
    def set_query(self, value):
        self._query = value
        self.total_count = value.count()
        self.can_new = self.allow_new and (not self.limit_max_rows or self.total_count < self.limit_max_rows)
        self.can_delete = self.allow_delete and (not self.limit_min_rows or self.total_count > self.limit_min_rows)
        self.can_edit = self.allow_edit
        self.columns = self._extract_columns()
        self.sorts = Sort.from_request()
    query = property(get_query, set_query)


    def _extract_columns(self):
        columns = OrderedDict()
        omit_fields = [] if not hasattr(self, '__omit_fields__') else self.__omit_fields__
        for alias, sa_column in extract_columns(self._query):
            if alias in omit_fields:
                continue
            columns[alias] = TableColumn(sa_column, table=self, alias=alias)
        return columns

    def format(self, row, column):
        value = getattr(row, column.label)
        if hasattr(self, '__xml_fields__') and column.label in self.__xml_fields__:
            if hasattr(self, column.label):
                value = getattr(self, column.label)(row)
            return Markup(value)
        return Formatter(value).__unicode__()

    @property
    def paginator(self):
        return request.paginators[self.paginator_key]

    @property
    def page_size(self):
        return self.paginator.paginate_items_per_page

    @property
    def page_index(self):
        return self.paginator.paginate_page - 1

    def paginate(self):
        start = self.page_size * self.page_index
        end = start + self.page_size
        self._query = self._query[start:end]

    def sort(self):
        create_sort_expr = lambda c, s: c.sa_column if not s.desc else desc(c.sa_column)
        expressions = []
        for sort in self.sorts:
            expressions.append(create_sort_expr(self.columns[sort.name], sort))
        self._query = self._query.order_by(*expressions)

    def display(self):
        self.sort()
        self.paginate()
        return render(dict(table=self),
                      template_name=self.template)

    def is_sortable(self, col):
        # TODO: sortable columns
        return True
