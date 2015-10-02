"""
Contains application settings.
"""
import six

from django.conf import settings


# By default, all scoring factors are weighted equally.
FACTORS = {
    'authoritative':    getattr(settings, 'AUTHORITATIVE_FACTOR', 0.25),
    'category':         getattr(settings, 'CATEGORY_FACTOR', 0.25),
    'like_type':        getattr(settings, 'LIKE_TYPE_FACTOR', 0.25),
    'tag':              getattr(settings, 'TAG_FACTOR', 0.25),
}

# Normalize factors so that they add up to "1".
FACTOR_SUM = sum(FACTORS.values())

for k, v in six.iteritems(FACTORS):
    FACTORS[k] = float(v) / float(FACTOR_SUM)

AUTHORITATIVE_FACTOR    = FACTORS['authoritative']
CATEGORY_FACTOR         = FACTORS['category']
LIKE_TYPE_FACTOR        = FACTORS['like_type']
TAG_FACTOR              = FACTORS['like_type']
