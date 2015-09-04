# encoding: utf-8

from collective.compoundcriterion.interfaces import ICompoundCriterionFilter
from zope.component import queryAdapter


def _filter_is(context, row):
    named_adapter = queryAdapter(context,
                                 ICompoundCriterionFilter,
                                 name=row.values)
    if named_adapter:
        # check that query is plone.app.querystring compliant
        # the value needs to be defined with a 'query' dict like :
        # {
        #  'portal_type':
        #  {'query': ['portal_type1', 'portal_type2']},
        #  'created':
        #  {'query': DateTime('2015/05/05'),
        #   'range': 'min'},
        # }
        for term in named_adapter.query.values():
            if not isinstance(term, dict) or \
               not 'query' in term:
                raise ValueError("The query format is not returned by {0}"
                                 "plone.app.querystring compliant !".format(
                                 named_adapter))
        return named_adapter.query
    return {}
