# postcreate script

for code, name in ((u'en', _('English')), (u'fr', _('French'))):
    create_entity('Language', code=code, name=name)


