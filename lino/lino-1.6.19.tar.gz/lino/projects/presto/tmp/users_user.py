# -*- coding: UTF-8 -*-
logger.info("Loading 8 objects to table users_user...")
# fields: id, modified, created, username, password, profile, initials, first_name, last_name, email, remarks, language, partner, open_session_on_new_ticket, access_class, event_type
loader.save(create_users_user(8,dt(2015,9,1,23,6,5),dt(2015,9,1,23,6,5),u'jean',u'pbkdf2_sha256$12000$tKBuh8YbT2rD$cd29a/T/0Z9S9CeiiE1U1P4l8PDAL9LjShZfnAW8lJo=','490',u'',u'',u'',u'',u'',u'en',None,False,u'30',None))
loader.save(create_users_user(7,dt(2015,9,1,23,6,5),dt(2015,9,1,23,6,5),u'luc',u'pbkdf2_sha256$12000$QzD4xNN7JrDT$36OnscdtSgBHoPvhyQrwL+ZEUZazv+b8rNppV/EX2SA=','400',u'',u'',u'',u'',u'',u'en',None,False,u'30',None))
loader.save(create_users_user(6,dt(2015,9,1,23,6,6),dt(2015,9,1,23,6,5),u'marc',u'pbkdf2_sha256$12000$NIOH6hEYhDJC$3q5Qo5XZ3tv2tpV1KG0l41VIo3O0aPNw8tOxvdedc8U=','200',u'',u'',u'',u'',u'',u'en',None,False,u'30',None))
loader.save(create_users_user(5,dt(2015,9,1,23,6,6),dt(2015,9,1,23,6,5),u'mathieu',u'pbkdf2_sha256$12000$MVxUYqrMjFs4$UVnmjh/PZSriGPfRzd5L14kCo3W4evARmkurls08YvA=','200',u'',u'',u'',u'',u'',u'en',None,False,u'30',None))
loader.save(create_users_user(3,dt(2015,9,1,23,6,6),dt(2015,9,1,23,6,3),u'romain',u'pbkdf2_sha256$12000$N1ovWtkAmbUF$7B6nZOW9ZfKDDk+uWME9uFpFBGorOXcW4hs2WH+mUdU=','900',u'RR',u'Romain',u'Raffault',u'luc.saffre@gmx.net',u'',u'fr',None,False,u'30',None))
loader.save(create_users_user(2,dt(2015,9,1,23,6,6),dt(2015,9,1,23,6,3),u'rolf',u'pbkdf2_sha256$12000$roHdLrx42Nji$i8/xWwcGgdb/Tj4YeWPsC91UuPy3q96Kz7H/hFtXYXI=','900',u'RR',u'Rolf',u'Rompen',u'luc.saffre@gmx.net',u'',u'de',None,False,u'30',None))
loader.save(create_users_user(1,dt(2015,9,1,23,6,6),dt(2015,9,1,23,6,3),u'robin',u'pbkdf2_sha256$12000$brIahSFNvYA1$wHIZJVE7anMI+vyuQPzpMia63CNxrkUpR367eRq7HGo=','900',u'RR',u'Robin',u'Rood',u'luc.saffre@gmx.net',u'',u'en',None,False,u'30',None))
loader.save(create_users_user(4,dt(2015,9,1,23,6,6),dt(2015,9,1,23,6,3),u'rando',u'pbkdf2_sha256$12000$se6ltUlVfso3$Vr6i7YkduNOMWfwEsSt5WE7MAwX5Uq2oA6Bvp1relKA=','900',u'RR',u'Rando',u'Roosi',u'luc.saffre@gmx.net',u'',u'et',None,False,u'30',None))

loader.flush_deferred_objects()
