# -*- coding: UTF-8 -*-
logger.info("Loading 3 objects to table notes_notetype...")
# fields: id, build_method, template, name, attach_to_email, email_template, important, remark, special_type
loader.save(create_notes_notetype(1,u'appyodt',u'Default.odt',[u'Default', u'', u'', u''],False,u'',False,u'',None))
loader.save(create_notes_notetype(2,None,u'',[u'phone report', u'', u'', u''],False,u'',False,u'',None))
loader.save(create_notes_notetype(3,None,u'',[u'todo', u'', u'', u''],False,u'',False,u'',None))

loader.flush_deferred_objects()
