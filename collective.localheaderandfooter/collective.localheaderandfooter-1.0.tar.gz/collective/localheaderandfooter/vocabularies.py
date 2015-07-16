# -*- coding: utf-8 -*-

from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.schema.interfaces import IVocabularyFactory

from plone.i18n.normalizer import idnormalizer

from .utils import get_available_headers
from .utils import get_available_footers


class BaseVocabulary(object):
    implements(IVocabularyFactory)

    available_getter = lambda: []

    def __call__(self, context):
        terms = self.get_terms(context)
        return SimpleVocabulary(list(terms))

    def get_dict(self):
        return dict(self.terms)

    def get_terms(self, context):
        for item in self.get_items():
            title = item['title']
            token = idnormalizer.normalize(title)
            value = item['name']
            yield SimpleTerm(value=value,
                             token=token,
                             title=title)

    def get_items(self):
        raise NotImplementedError()


class AvailableHeaders(BaseVocabulary):

    def get_items(self):
        return get_available_headers()


class AvailableFooters(BaseVocabulary):

    def get_items(self):
        return get_available_footers()
