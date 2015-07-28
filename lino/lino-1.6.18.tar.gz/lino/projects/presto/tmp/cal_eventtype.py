# -*- coding: UTF-8 -*-
logger.info("Loading 2 objects to table cal_eventtype...")
# fields: id, seqno, name, attach_to_email, email_template, description, is_appointment, all_rooms, locks_user, start_date, event_label, max_conflicting
loader.save(create_cal_eventtype(1,1,[u'Holidays', u'Holidays', u'Holidays', u'Holidays'],False,u'',u'',False,True,False,None,[u'', u'', u'', u''],1))
loader.save(create_cal_eventtype(2,2,[u'Meeting', u'Meeting', u'Meeting', u'Meeting'],False,u'',u'',True,False,False,None,[u'', u'', u'', u''],1))

loader.flush_deferred_objects()
