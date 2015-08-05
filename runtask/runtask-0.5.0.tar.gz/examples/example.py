#!/usr/bin/python
# .+
# .context    : RunTask, coherent time task scheduler
# .title      : example
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Torino - Italy
# .creation   :	7-Feb-2015
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

# set up the time scheduler
sch = rt.RunTask(speed=1.0,tick=0.1)

# a task printing run time and, if not forever, the runs left.
def task(sch):
    now = tm.time()
    task_id, last_runtime, run_count, task_args = sch.task_info()
    runs_left = sch.runs_left()
    if runs_left == -1:
        print 'task','%d %12.3f %10.9f' %(task_id,last_runtime,now-last_runtime)
    else:
        if runs_left == 1:
            print 'task','%d %12.3f %10.9f %d' \
                % (task_id,last_runtime,now-last_runtime,runs_left), \
                    'this is the last run'
        else:
            print 'task','%d %12.3f %10.9f %d' \
                % (task_id,last_runtime,now-last_runtime,runs_left)


# task every 5 seconds, epoch aligned, forever
sch.task(task,([sch],{}),sch.aligned(5.,0.0,-1))

# two tasks every second, half second aligned,
# the first forever, the second 5 times.
sch.task(task,([sch],{}),sch.aligned(1.,0.5,-1))
sch.task(task,([sch],{}),sch.aligned(1.,0.5,5))

# print a start message and start
print 'Schedule 3 tasks for 10 seconds (system time) then terminate.'
print 'Task #0 is scheduled every 5 seconds, epoch aligned, forever.'
print 'Task #1 is scheduled every second, aligned at half second, forever.'
print 'Task #2 is scheduled every second, aligned at half second, for 5 times.'
print 'id     runtime        sys-runtime run number'

sch.start()

# wait 20 seconds then stop scheduler and exit.
tm.sleep(10)
sch.stop()

#### END
