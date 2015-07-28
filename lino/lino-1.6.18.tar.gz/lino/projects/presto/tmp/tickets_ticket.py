# -*- coding: UTF-8 -*-
logger.info("Loading 5 objects to table tickets_ticket...")
# fields: id, modified, created, closed, private, planned_time, project, site, product, nickname, summary, description, ticket_type, duplicate_of, reported_for, fixed_for, assigned_to, reporter, state, feedback, standby, deadline, priority
loader.save(create_tickets_ticket(1,dt(2015,7,28,0,46,21),dt(2015,7,28,0,46,21),False,False,None,1,1,3,u'',u'Foo fails to bar when baz',u'',1,None,None,None,7,5,u'10',False,False,None,0))
loader.save(create_tickets_ticket(2,dt(2015,7,28,0,46,21),dt(2015,7,28,0,46,21),False,False,None,2,None,4,u'',u'Bar is not always baz',u'',2,None,None,None,8,6,u'10',False,False,None,0))
loader.save(create_tickets_ticket(3,dt(2015,7,28,0,46,21),dt(2015,7,28,0,46,21),False,False,None,None,None,1,u'',u'Baz sucks',u'',3,None,None,None,7,7,u'10',False,False,None,0))
loader.save(create_tickets_ticket(4,dt(2015,7,28,0,46,21),dt(2015,7,28,0,46,21),False,False,None,3,None,2,u'',u"Foo and bar don't baz",u'',1,None,None,None,8,8,u'10',False,False,None,0))
loader.save(create_tickets_ticket(5,dt(2015,7,28,0,46,21),dt(2015,7,28,0,46,21),False,False,None,None,None,3,u'',u'Cannot create Foo',u'<p>When I try to create\n    a <b>Foo</b>, then I get a <b>Bar</b> instead of a Foo.</p>',2,None,None,None,7,3,u'10',False,False,None,0))

loader.flush_deferred_objects()
