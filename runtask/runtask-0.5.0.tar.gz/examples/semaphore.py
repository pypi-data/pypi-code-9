#!/usr/bin/python
# .+
# .context    : RunTask, coherent time task scheduler
# .title      : threading semaphore example
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Torino - Italy
# .creation   :	2-Aug-2015
# .copyright  :	(c) 2015 Fabrizio Pollastri
# .license    : GNU General Public License (see below)
#
# This file is part of "RunTask, Coherent Time Task Scheduler".
#
# RunTask is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# RunTask is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software. If not, see <http://www.gnu.org/licenses/>.
#
# .-

#### import required modules

import runtask as rt           # task scheduler
import time as tm              # time interface
import threading as tg         # thread control


# set up the time scheduler at the system time
sch = rt.RunTask(speed=1.0,tick=0.01)

# create an lock object to control main execution
loop = tg.Semaphore()
loop.acquire(False)

# schedule each main loop with period = 1, phase=0, for ten times: release
# the lock.
period = 1
phase = 0
runs = 10
sch.task(loop,0,sch.aligned(period,phase,runs))

# print a start message and start
print 'Schedule main every second for 10 times, then terminate.'
print 'Now is ',tm.asctime()
print 'id     runtime        sys-runtime'

sch.start()

## main

# loop
while True:

    # wait for run time
    loop.acquire()

    # print task id, run time, difference from sys time and the runs left.
    task_id, runtime, run_count, task_args = sch.task_info(loop)
    runs_left = sch.runs_left(loop) + 1
    now = tm.time()
    if runs_left == 1:
        print 'task','%d %12.3f %10.9f %d' \
            % (task_id,runtime,now-runtime,runs_left), \
                'this is the last run'
        break
    else:
        print 'task','%d %12.3f %10.9f %d' \
            % (task_id,runtime,now-runtime,runs_left)

# terminate
sch.stop()

#### END
