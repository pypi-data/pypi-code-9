# -*- coding: utf-8 -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2015 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU Affero General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option)
#  any later version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for
#  more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Grid Filters
"""

from __future__ import unicode_literals

import sqlalchemy as sa

from edbob.util import prettify

from rattail.util import OrderedDict
from rattail.core import UNSPECIFIED

from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer
from webhelpers.html import HTML, tags


class FilterRenderer(object):
    """
    Base class for all filter renderers.
    """

    def render(self, value=None, **kwargs):
        """
        Render the filter input element(s) as HTML.  Default implementation
        uses a simple text input.
        """
        name = self.filter.key
        return tags.text(name, value=value, id='filter.{0}.value'.format(name))


class DefaultRenderer(FilterRenderer):
    """
    Default / fallback renderer.
    """


class NumericRenderer(FilterRenderer):
    """
    Input renderer for numeric fields.
    """


class GridFilter(object):
    """
    Represents a filter available to a grid.  This is used to construct the
    'filters' section when rendering the index page template.
    """
    verbmap = {
        'is_any':               "is any",
        'equal':                "equal to",
        'not_equal':            "not equal to",
        'greater_than':         "greater than",
        'greater_equal':        "greater than or equal to",
        'less_than':            "less than",
        'less_equal':           "less than or equal to",
        'is_null':              "is null",
        'is_not_null':          "is not null",
        'is_true':              "is true",
        'is_false':             "is false",
        'contains':             "contains",
        'does_not_contain':     "does not contain",
    }

    def __init__(self, key, label=None, verbs=None, renderer=None,
                 default_active=False, default_verb=None, default_value=None):
        self.key = key
        self.label = label or prettify(key)
        self.verbs = verbs or self.get_default_verbs()
        self.renderer = renderer or DefaultRenderer()
        self.renderer.filter = self
        self.default_active = default_active
        self.default_verb = default_verb
        self.default_value = default_value

    def __repr__(self):
        return "GridFilter({0})".format(repr(self.key))

    def get_default_verbs(self):
        """
        Returns the set of verbs which will be used by default, i.e.  unless
        overridden by constructor args etc.
        """
        verbs = getattr(self, 'default_verbs', None)
        if verbs:
            if callable(verbs):
                return verbs()
            return verbs
        return ['equal', 'not_equal', 'is_null', 'is_not_null']

    def filter(self, data, verb=None, value=UNSPECIFIED):
        """
        Filter the given data set according to a verb/value pair.  If no verb
        and/or value is specified by the caller, the filter will use its own
        current verb/value by default.
        """
        verb = verb or self.verb
        value = value if value is not UNSPECIFIED else self.value
        filtr = getattr(self, 'filter_{0}'.format(verb), None)
        if not filtr:
            raise ValueError("Unknown filter verb: {0}".format(repr(verb)))
        return filtr(data, value)

    def filter_is_any(self, data, value):
        """
        Special no-op filter which does no actual filtering.  Useful in some
        cases to add an "ineffective" option to the verb list for a given grid
        filter.
        """
        return data

    def render(self, **kwargs):
        kwargs['filter'] = self
        return self.renderer.render(**kwargs)


class AlchemyGridFilter(GridFilter):
    """
    Base class for SQLAlchemy grid filters.
    """

    def __init__(self, *args, **kwargs):
        self.column = kwargs.pop('column')
        super(AlchemyGridFilter, self).__init__(*args, **kwargs)

    def filter_equal(self, query, value):
        """
        Filter data with an equal ('=') query.
        """
        if value is None or value == '':
            return query
        return query.filter(self.column == value)

    def filter_not_equal(self, query, value):
        """
        Filter data with a not eqaul ('!=') query.
        """
        if value is None or value == '':
            return query

        # When saying something is 'not equal' to something else, we must also
        # include things which are nothing at all, in our result set.
        return query.filter(sa.or_(
            self.column == None,
            self.column != value,
        ))

    def filter_is_null(self, query, value):
        """
        Filter data with an 'IS NULL' query.  Note that this filter does not
        use the value for anything.
        """
        return query.filter(self.column == None)

    def filter_is_not_null(self, query, value):
        """
        Filter data with an 'IS NOT NULL' query.  Note that this filter does
        not use the value for anything.
        """
        return query.filter(self.column != None)

    def filter_greater_than(self, query, value):
        """
        Filter data with a greater than ('>') query.
        """
        if value is None or value == '':
            return query
        return query.filter(self.column > value)

    def filter_greater_equal(self, query, value):
        """
        Filter data with a greater than or equal ('>=') query.
        """
        if value is None or value == '':
            return query
        return query.filter(self.column >= value)

    def filter_less_than(self, query, value):
        """
        Filter data with a less than ('<') query.
        """
        if value is None or value == '':
            return query
        return query.filter(self.column < value)

    def filter_less_equal(self, query, value):
        """
        Filter data with a less than or equal ('<=') query.
        """
        if value is None or value == '':
            return query
        return query.filter(self.column <= value)


class AlchemyStringFilter(AlchemyGridFilter):
    """
    String filter for SQLAlchemy.
    """

    def default_verbs(self):
        """
        Expose contains / does-not-contain verbs in addition to core.
        """
        return ['contains', 'does_not_contain',
                'equal', 'not_equal', 'is_null', 'is_not_null']

    def filter_contains(self, query, value):
        """
        Filter data with a full 'ILIKE' query.
        """
        if value is None or value == '':
            return query
        return query.filter(self.column.ilike('%{0}%'.format(value)))

    def filter_does_not_contain(self, query, value):
        """
        Filter data with a full 'NOT ILIKE' query.
        """
        if value is None or value == '':
            return query

        # When saying something is 'not like' something else, we must also
        # include things which are nothing at all, in our result set.
        return query.filter(sa.or_(
            self.column == None,
            ~self.column.ilike('%{0}%'.format(value)),
        ))


class AlchemyNumericFilter(AlchemyGridFilter):
    """
    Numeric filter for SQLAlchemy.
    """

    def default_verbs(self):
        """
        Expose greater-than / less-than verbs in addition to core.
        """
        return ['equal', 'not_equal', 'greater_than', 'greater_equal',
                'less_than', 'less_equal', 'is_null', 'is_not_null']


class AlchemyBooleanFilter(AlchemyGridFilter):
    """
    Boolean filter for SQLAlchemy.
    """
    default_verbs = ['is_true', 'is_false', 'is_any']

    def filter_is_true(self, query, value):
        """
        Filter data with an "is true" query.  Note that this filter does not
        use the value for anything.
        """
        return query.filter(self.column == True)

    def filter_is_false(self, query, value):
        """
        Filter data with an "is false" query.  Note that this filter does not
        use the value for anything.
        """
        return query.filter(self.column == False)


class GridFilterSet(OrderedDict):
    """
    Collection class for :class:`GridFilter` instances.
    """


class GridFiltersForm(Form):
    """
    Form for grid filters.
    """

    def __init__(self, request, filters, *args, **kwargs):
        super(GridFiltersForm, self).__init__(request, *args, **kwargs)
        self.filters = filters

    def iter_filters(self):
        return self.filters.itervalues()


class GridFiltersFormRenderer(FormRenderer):
    """
    Renderer for :class:`GridFiltersForm` instances.
    """

    @property
    def filters(self):
        return self.form.filters

    def iter_filters(self):
        return self.form.iter_filters()

    def tag(self, *args, **kwargs):
        """
        Convenience method which passes all args to the
        :func:`webhelpers:webhelpers.HTML.tag()` function.
        """
        return HTML.tag(*args, **kwargs)

    # TODO: This seems hacky..?
    def checkbox(self, name, checked=None, **kwargs):
        """
        Custom checkbox implementation.
        """
        if name.endswith('-active'):
            return tags.checkbox(name, checked=checked, **kwargs)
        if checked is None:
            checked = False
        return super(GridFiltersFormRenderer, self).checkbox(name, checked=checked, **kwargs)

    def filter_verb(self, filtr):
        """
        Render the verb selection dropdown for the given filter.
        """
        options = [(v, filtr.verbmap.get(v, "unknown verb '{0}'".format(v)))
                   for v in filtr.verbs]
        return self.select('{0}.verb'.format(filtr.key), options, class_='verb')

    def filter_value(self, filtr):
        """
        Render the value input element(s) for the filter.
        """
        # TODO: This surely needs some work..?
        return HTML.tag('div', class_='value', c=filtr.render(value=self.value(filtr.key)))
