# -*- coding: UTF-8 -*-
logger.info("Loading 1 objects to table clocking_servicereport...")
# fields: id, start_date, end_date, printed_by, interesting_for, ticket_state
loader.save(create_clocking_servicereport(1,date(2015,6,3),None,None,1,None))

loader.flush_deferred_objects()
