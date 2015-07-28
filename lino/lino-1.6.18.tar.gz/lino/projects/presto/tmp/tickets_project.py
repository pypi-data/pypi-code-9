# -*- coding: UTF-8 -*-
logger.info("Loading 3 objects to table tickets_project...")
# fields: id, ref, company, contact_person, contact_role, closed, private, planned_time, name, parent, type, description, srcref_url_template, changeset_url_template
loader.save(create_tickets_project(1,u'lino',None,None,None,False,False,None,u'Framework',None,None,u'',u'',u''))
loader.save(create_tickets_project(2,u'team',None,None,None,False,False,None,u'Team',None,None,u'',u'',u''))
loader.save(create_tickets_project(3,u'docs',None,None,None,False,False,None,u'Documentation',None,None,u'',u'',u''))

loader.flush_deferred_objects()
