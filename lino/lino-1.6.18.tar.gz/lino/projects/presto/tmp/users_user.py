# -*- coding: UTF-8 -*-
logger.info("Loading 8 objects to table users_user...")
# fields: id, modified, created, username, password, profile, initials, first_name, last_name, email, remarks, language, partner, current_project, open_session_on_new_ticket, access_class, event_type
loader.save(create_users_user(5,dt(2015,7,28,0,46,21),dt(2015,7,28,0,46,21),u'mathieu',u'pbkdf2_sha256$12000$BKr6k0dTV7sQ$kdDULPMBzWWwsUqICshT8vAWupOCtAdILQIT3A0maXA=','100',u'',u'',u'',u'',u'',u'en',None,None,False,u'30',None))
loader.save(create_users_user(6,dt(2015,7,28,0,46,21),dt(2015,7,28,0,46,21),u'marc',u'pbkdf2_sha256$12000$N4QDGZHQKrKL$n/85eQw5EqjUWWrCySxQAMgJ7YV+zifvq/gVrRRDUZo=','100',u'',u'',u'',u'',u'',u'en',None,None,False,u'30',None))
loader.save(create_users_user(7,dt(2015,7,28,0,46,21),dt(2015,7,28,0,46,21),u'luc',u'pbkdf2_sha256$12000$fTwUeD7yX9h5$vFsxIL1eT9Dvml5yb5X1btQMhp0jeKiBeKuK7TaeVxQ=','500',u'',u'',u'',u'',u'',u'en',None,None,False,u'30',None))
loader.save(create_users_user(8,dt(2015,7,28,0,46,21),dt(2015,7,28,0,46,21),u'jean',u'pbkdf2_sha256$12000$o7DfmytkEwXT$Vc4wPjs3DE4AOOwIs71znv2CKJMZTnvLdyyy80i9HWY=','510',u'',u'',u'',u'',u'',u'en',None,None,False,u'30',None))
loader.save(create_users_user(3,dt(2015,7,28,0,46,21),dt(2015,7,28,0,46,19),u'romain',u'pbkdf2_sha256$12000$r2rZDXQOd52f$iCCcf3G2QKfJvKqL9iye/tdQ3RjZeHo5oQDFxduWI6U=','900',u'RR',u'Romain',u'Raffault',u'luc.saffre@gmx.net',u'',u'fr',None,None,False,u'30',None))
loader.save(create_users_user(2,dt(2015,7,28,0,46,22),dt(2015,7,28,0,46,19),u'rolf',u'pbkdf2_sha256$12000$95bEDX2yddeP$gL9gu12ExWo99OlHk0CJKht2KS7h3/YKnzzUUHoSqsY=','900',u'RR',u'Rolf',u'Rompen',u'luc.saffre@gmx.net',u'',u'de',None,None,False,u'30',None))
loader.save(create_users_user(1,dt(2015,7,28,0,46,22),dt(2015,7,28,0,46,19),u'robin',u'pbkdf2_sha256$12000$nekyHUe0Iua8$r3ucK1f73uIjF3i+rpP91Xqgnh9+yvn1xWR21w/BuY8=','900',u'RR',u'Robin',u'Rood',u'luc.saffre@gmx.net',u'',u'en',None,None,False,u'30',None))
loader.save(create_users_user(4,dt(2015,7,28,0,46,22),dt(2015,7,28,0,46,19),u'rando',u'pbkdf2_sha256$12000$PWS9kW3JbxGW$fv/p46rg28TPMFSq4LeDuNje47WW35jyyQBPQR2l7JE=','900',u'RR',u'Rando',u'Roosi',u'luc.saffre@gmx.net',u'',u'et',None,None,False,u'30',None))

loader.flush_deferred_objects()
