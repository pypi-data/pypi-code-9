# -*- coding: UTF-8 -*-
logger.info("Loading 1 objects to table tickets_link...")
# fields: id, type, parent, child
loader.save(create_tickets_link(1,u'10',1,2))

loader.flush_deferred_objects()
