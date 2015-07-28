# -*- coding: UTF-8 -*-
logger.info("Loading 2 objects to table tickets_site...")
# fields: id, partner, name, remark
loader.save(create_tickets_site(1,None,u'welket',u''))
loader.save(create_tickets_site(2,None,u'welsch',u''))

loader.flush_deferred_objects()
