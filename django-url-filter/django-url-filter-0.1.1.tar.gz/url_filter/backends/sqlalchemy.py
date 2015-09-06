# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from sqlalchemy.sql.expression import not_

from .base import BaseFilterBackend


class SQLAlchemyFilterBackend(BaseFilterBackend):
    def __init__(self, *args, **kwargs):
        super(SQLAlchemyFilterBackend, self).__init__(*args, **kwargs)

        assert len(self.queryset._primary_entity.entities) == 1, (
            '{} does not support filtering when multiple entities '
            'are being queried (e.g. session.query(Foo, Bar)).'
            ''.format(self.__class__.__name__)
        )

        self.model = self.queryset._primary_entity.entities[0]

    def filter(self):
        conditions = [self.build_clause(spec) for spec in self.specs]
        return self.queryset.filter(*conditions)

    def build_clause(self, spec):
        assert len(spec.components) == 1, (
            '{} does not currently support filtering on '
            'related models.'
            ''.format()
        )

        builder = getattr(self, '_build_clause_{}'.format(spec.lookup))
        column = getattr(self.model, spec.components[0])
        clause = builder(spec, column)

        if spec.is_negated:
            clause = not_(clause)

        return clause

    def _build_clause_contains(self, spec, column):
        return column.contains(spec.value)

    def _build_clause_day(self, spec, column):
        raise NotImplementedError

    def _build_clause_endswith(self, spec, column):
        return column.endswith(spec.value)

    def _build_clause_exact(self, spec, column):
        return column == spec.value

    def _build_clause_gt(self, spec, column):
        return column > spec.value

    def _build_clause_gte(self, spec, column):
        return column >= spec.value

    def _build_clause_hour(self, spec, column):
        raise NotImplementedError

    def _build_clause_icontains(self, spec, column):
        # TODO
        return column.contains(spec.value)

    def _build_clause_iendswith(self, spec, column):
        # TODO
        return column.endswith(spec.value)

    def _build_clause_iexact(self, spec, column):
        # TODO
        return column == spec.value

    def _build_clause_in(self, spec, column):
        return column.in_(spec.value)

    def _build_clause_iregex(self, spec, column):
        raise NotImplementedError

    def _build_clause_isnull(self, spec, column):
        if spec.value:
            return column == None  # noqa
        else:
            return column != None  # noqa

    def _build_clause_istartswith(self, spec, column):
        # TODO
        return column.startswith(spec.value)

    def _build_clause_lt(self, spec, column):
        return column < spec.value

    def _build_clause_lte(self, spec, column):
        return column <= spec.value

    def _build_clause_minute(self, spec, column):
        raise NotImplementedError

    def _build_clause_month(self, spec, column):
        raise NotImplementedError

    def _build_clause_range(self, spec, column):
        return column.between(spec.value)

    def _build_clause_regex(self, spec, column):
        raise NotImplementedError

    def _build_clause_search(self, spec, column):
        raise NotImplementedError

    def _build_clause_second(self, spec, column):
        raise NotImplementedError

    def _build_clause_startswith(self, spec, column):
        return column.startswith(spec.value)

    def _build_clause_week_day(self, spec, column):
        raise NotImplementedError

    def _build_clause_year(self, spec, column):
        raise NotImplementedError
