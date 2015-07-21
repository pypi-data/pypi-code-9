try:
    from zope.app.schema.vocabulary import IVocabularyFactory
except ImportError:
    from zope.schema.interfaces import IVocabularyFactory

from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from plone.app.imaging.utils import getAllowedSizes


class ImageMiniaturesVocabulary(object):
    """
    A simple vocab to return a list of image available miniatures
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        sizes = getAllowedSizes()
        scales = [{'size': size,
                   'value': key,
                   'title': "%s %s" % (key, size)} for key, size in sizes.items()]
        scales.sort(lambda x, y: cmp(x['size'][0], y['size'][0]))
        terms = [SimpleTerm(scale['value'], title=scale['title']) for scale in scales]
        return SimpleVocabulary(terms)

ImageMiniaturesVocabularyFactory = ImageMiniaturesVocabulary()
