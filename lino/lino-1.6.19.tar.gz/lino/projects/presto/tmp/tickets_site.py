# -*- coding: UTF-8 -*-
logger.info("Loading 3 objects to table tickets_site...")
# fields: id, partner, name, remark
loader.save(create_tickets_site(1,None,u'welket',u''))
loader.save(create_tickets_site(2,None,u'welsch',u''))
loader.save(create_tickets_site(3,None,u'pypi',u''))

loader.flush_deferred_objects()
