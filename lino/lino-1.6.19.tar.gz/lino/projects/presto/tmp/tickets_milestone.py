# -*- coding: UTF-8 -*-
logger.info("Loading 8 objects to table tickets_milestone...")
# fields: id, printed_by, site, label, expected, reached, description, changes_since
loader.save(create_tickets_milestone(1,None,1,u'',date(2015,8,12),date(2015,8,12),u'',None))
loader.save(create_tickets_milestone(2,None,2,u'',date(2015,8,14),date(2015,8,14),u'',None))
loader.save(create_tickets_milestone(3,None,1,u'',date(2015,8,16),date(2015,8,16),u'',None))
loader.save(create_tickets_milestone(4,None,2,u'',date(2015,8,18),date(2015,8,18),u'',None))
loader.save(create_tickets_milestone(5,None,1,u'',date(2015,8,20),date(2015,8,20),u'',None))
loader.save(create_tickets_milestone(6,None,2,u'',date(2015,8,22),date(2015,8,22),u'',None))
loader.save(create_tickets_milestone(7,None,1,u'',date(2015,8,24),date(2015,8,24),u'',None))
loader.save(create_tickets_milestone(8,None,2,u'',date(2015,9,1),None,u'',None))

loader.flush_deferred_objects()
