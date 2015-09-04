from zope.component import getGlobalSiteManager
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from collective.compoundcriterion.interfaces import ICompoundCriterionFilter
from Products.CMFPlone import PloneMessageFactory as _p


class CompoundCriterionVocabulary(object):
    """Vocabulary factory for compound criterion.
       This will return every named adapter that provides the ICoumpondCriterionFilter interface."""
    implements(IVocabularyFactory)

    def __call__(self, context):
        sm = getGlobalSiteManager()
        registrations = [a for a in sm.registeredAdapters() if a.provided == ICompoundCriterionFilter]
        terms = [SimpleTerm(adapter.name, adapter.name, _p(adapter.name)) for adapter in registrations]
        return SimpleVocabulary(terms)


CompoundCriterionVocabularyFactory = CompoundCriterionVocabulary()
