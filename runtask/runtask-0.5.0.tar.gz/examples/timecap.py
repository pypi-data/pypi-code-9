#!/usr/bin/python
# .+
# .context    : RunTask, coherent time task scheduler
# .title      : timing capabilities example
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Torino - Italy
# .creation   :	14-May-2015
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

# set up the time scheduler at the system time
sch = rt.RunTask(speed=1.0,tick=0.01)

# a task printing run time and, if not forever, the runs left.
def task(sch):
    now = tm.time()
    task_id, runtime, run_count, task_args = sch.task_info()
    runs_left = sch.runs_left()
    if runs_left == -1:
        print 'task','%d %12.3f %10.9f' % (task_id,runtime,now-runtime)
    else:
        if runs_left == 1:
            print 'task','%d %12.3f %10.9f %d' \
                % (task_id,runtime,now-runtime,runs_left), \
                    'this is the last run'
        else:
            print 'task','%d %12.3f %10.9f %d' \
                % (task_id,runtime,now-runtime,runs_left)

            
# run task at each minute, 15 seconds after minute beginning, forever
period = 1 * 60.         # (1 min = 1 min * 60 sec)
phase = 15.              # (15 sec = 15 sec)
sch.task(task,([sch],{}),sch.aligned(period,phase))

# run task with period = 19/3, phase=0.1, forever
period = (19,3)
phase = 0.1
sch.task(task,([sch],{}),sch.aligned(period,phase))

# run task immediately with period = 5, forever
period = 5.
sch.task(task,([sch],{}),sch.now(period))

# run task imediately with period = 19/3, forever
period = (19,3)
sch.task(task,([sch],{}),sch.now(period))

# run task randomly with uniform distribution, min period 8, max period 16, forever
period_min = 8 
period_max = 16 
sch.task(task,([sch],{}),sch.uniform(period_min,period_max))

# print a start message and start
print 'Schedule 5 tasks for 60 seconds (system time) then terminate.'
print 'Task 0 is run at each minute, 15 seconds after minute begining. Forever'
print 'Task 1 is run every 19/3 seconds with phase 0.1. Forever'
print 'Task 2 is run every 5 seconds, starting immediately. Forever'
print 'Task 3 is run every 19/3 seconds, starting immediately. Forever'
print 'Task 4 is run randomnly with uniform distribution, period min 8 seconds and max 16 seconds. Forever'
print 'Now is ',tm.asctime()
print 'id     runtime        sys-runtime'

sch.start()

# wait one minute then stop scheduler and exit.
tm.sleep(60)
sch.stop()

#### END
