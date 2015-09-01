# -*- coding: UTF-8 -*-
logger.info("Loading 1 objects to table clocking_sessiontype...")
# fields: id, name
loader.save(create_clocking_sessiontype(1,[u'Default', u'', u'', u'']))

loader.flush_deferred_objects()
