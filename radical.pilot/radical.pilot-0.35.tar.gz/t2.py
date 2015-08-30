#!/usr/bin/env python

import radical.pilot.utils as rpu

sid = 'rp.session.cameo.merzky.016627.0005'


json  = rpu.fetch_session  (sid)
profs = rpu.fetch_profiles (sid)

for prof in profs:
    f = rpu.get_profile_frame (prof)
    print f
