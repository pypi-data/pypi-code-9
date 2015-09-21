#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       scheduler.py
#       
#       Copyright 2015 Francisco Vicent <franciscovicent@outlook.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       
#       

from timeit import default_timer


__all__ = ["Scheduler"]


class Scheduler(object):
    
    def __init__(self):
        self.remove_all()
    
    def add(self, interval, count, callback, *args, **kwargs):
        """
        Append a task to the scheduler and return the assigned ID.
        
        Arguments:
        interval -- Interval in which the callback will be executed (in seconds).
        count    -- Maximum number of times the callback will be executed.
                    The task will be removed after, at least, interval*count seconds.
                    If count is 0 the callback will be executed infinitely.
        callback -- The function to be executed (with *args and **kwargs if any).
        """
        if count < 0:
            raise ValueError("count must be greater than or equal to 0.")
        
        task = [0, interval, count, callback, args, kwargs]
        self._tasks.append(task)
        
        return id(task)
    
    def remove(self, *tasks):
        """
        Remove (a) task(s) from the scheduler. Arguments must be
        as many as tasks to be removed. Attempting to remove an
        unexisting task will do nothing.
        
        Example -- Scheduler.remove(task_id_1, task_id_2, ...)
        """
        for task in self._tasks:
            if id(task) in tasks:
                self._tasks.remove(task)
    
    def remove_all(self):
        """Remove all tasks from the scheduler."""
        self._tasks = []
    
    def run(self):
        completed_tasks = []
        
        for i, task in enumerate(self._tasks):
            prev_ticks, interval, count, callback, args, kwargs = task
            if default_timer() - prev_ticks >= interval:
                callback(*args, **kwargs)
                if count > 0:
                    count -= 1
                    if count == 0:
                        # Do not change indices until all tasks
                        # have been executed.
                        completed_tasks.append(id(task))
                        continue
                    else:
                        self._tasks[i][2] = count
                # Might take a while to execute the callback,
                # so get ticks again.
                self._tasks[i][0] = default_timer()
        
        self.remove(*completed_tasks)
