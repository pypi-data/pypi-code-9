import logging


logger = logging.getLogger('Products.PloneHotfix20150910')

hotfixes = [
    'addMember',
    'isURLInPortal',
    'kupu',
    'setHeader',
]


PLONE_ONLY = []

try:
    from Products import kupu  # noqa
except ImportError:
    hotfixes.remove('kupu')
try:
    import Products.CMFPlone  # noqa
except ImportError:
    # No Plone. Remove all but the Zope patches.
    for f in PLONE_ONLY:
        if f in hotfixes:
            hotfixes.remove(f)


# Apply the fixes
for hotfix in hotfixes:
    try:
        __import__('Products.PloneHotfix20150910.%s' % hotfix)
        logger.info('Applied %s patch' % hotfix)
    except:
        logger.warn('Could not apply %s' % hotfix)
logger.info('Hotfix installed')
