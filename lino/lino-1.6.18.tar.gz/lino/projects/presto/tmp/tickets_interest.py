# -*- coding: UTF-8 -*-
logger.info("Loading 6 objects to table tickets_interest...")
# fields: id, product, site
loader.save(create_tickets_interest(1,1,1))
loader.save(create_tickets_interest(2,2,1))
loader.save(create_tickets_interest(3,3,1))
loader.save(create_tickets_interest(4,4,2))
loader.save(create_tickets_interest(5,1,2))
loader.save(create_tickets_interest(6,2,2))

loader.flush_deferred_objects()
