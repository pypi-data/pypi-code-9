# -*- coding: UTF-8 -*-

from plone.i18n.normalizer.interfaces import INormalizer
from zope.interface import implements
from plone.i18n.normalizer.base import allowed

from plone.i18n.normalizer.ja import ja_normalize
from plone.i18n.normalizer.ja import MAX_LENGTH


class Normalizer(object):
    """
    This normalizer can normalize any unicode string and returns a version
    that only contains of ASCII characters.

    Let's make sure that this implementation actually fulfills the API.

      >>> from zope.interface.verify import verifyClass
      >>> verifyClass(INormalizer, Normalizer)
      True

    Strings that contain only ASCII characters are returned decoded.

      >>> norm = Normalizer()
      >>> text = unicode("test page", 'utf-8')
      >>> norm.normalize(text)
      'test page'

    Text that contains non-ASCII characters are normalized.

      >>> norm = Normalizer()
      >>> text = unicode("テストページ", 'utf-8')
      >>> normalized = norm.normalize(text)
      >>> all(s in allowed for s in normalized)
      True
      >>> len(normalized)
      6

    The max_length argument is respected.
      >>> normalized = norm.normalize(text, max_length=8)
      >>> len(normalized)
      8

    Text that contains filename of non-ASCII characters are normalized.

      >>> norm = Normalizer()
      >>> text = unicode("テストファイル.pdf", 'utf-8')
      >>> normalized = norm.normalize(text)
      >>> len(normalized)
      10
      >>> normalized[-4:]
      '.pdf'

      >>> norm = Normalizer()
      >>> text = unicode("テストファイル.拡張子", 'utf-8')
      >>> normalized = norm.normalize(text)
      >>> len(normalized)
      6
    """
    implements(INormalizer)

    def normalize(self, text, locale=None, max_length=MAX_LENGTH):
        """
        Returns a normalized text. text has to be a unicode string.
        """
        splited_text = text.rsplit('.', 1)
        if len(splited_text) == 2:
            pre_text, suffix = splited_text
            if len(suffix) < 5 and all(s in allowed for s in suffix):
                pre_normalized = ja_normalize(pre_text, max_length=max_length)
                suffix_normalized = ja_normalize(suffix, max_length=3)
                return pre_normalized + "." + suffix_normalized
        return ja_normalize(text, max_length=max_length)

normalizer = Normalizer()
