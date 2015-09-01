# -*- coding: UTF-8 -*-
logger.info("Loading 3 objects to table tickets_project...")
# fields: id, ref, parent, company, contact_person, contact_role, closed, private, planned_time, name, assign_to, type, description, srcref_url_template, changeset_url_template
loader.save(create_tickets_project(1,u'lin\xf6',None,None,None,None,False,True,None,u'Framew\xf6rk',None,None,u'',u'',u''))
loader.save(create_tickets_project(2,u't\xe9am',None,None,None,None,False,True,None,u'T\xe9am',None,None,u'',u'',u''))
loader.save(create_tickets_project(3,u'docs',None,None,None,None,False,True,None,u'Documentati\xf3n',None,None,u'',u'',u''))

loader.flush_deferred_objects()
