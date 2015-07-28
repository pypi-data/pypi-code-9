# -*- coding: UTF-8 -*-
logger.info("Loading 3 objects to table tickets_tickettype...")
# fields: id, name
loader.save(create_tickets_tickettype(1,[u'Bugfix', u'Bugfix', u'Bugfix', u'Bugfix']))
loader.save(create_tickets_tickettype(2,[u'Enhancement', u'Enhancement', u'Enhancement', u'Enhancement']))
loader.save(create_tickets_tickettype(3,[u'Upgrade', u'Upgrade', u'Upgrade', u'Upgrade']))

loader.flush_deferred_objects()
