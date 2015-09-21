#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Simple scheduler.
    
    Usage example
    -------------
        from scheduler import Scheduler

        def f1(name="world"):
            print("Hello {}!".format(name))

        def f2():
            print("I run infinitely.")

        scheduler = Scheduler()
        a = scheduler.add(
            1,  # Run every second.
            5,  # Just five times (0 can be used to run infinitely).
            f1  # Function to be called...
        )
        b = scheduler.add(3.5, 0, f2)
        c = scheduler.add(0.5, 10, f1, name="Python")

        while True:
            scheduler.run()
    
    Tasks can be removed by using the ID retrieved by Scheduler.add:
        scheduler.remove(a)
    
    Multiple tasks can be removed at once:
        scheduler.remove(a, b)
    
    Don't do this, since it is slower:
        for task in tasks_to_be_removed:
            scheduler.remove(task)
    
    This is the preferred way:
        scheduler.remove(*tasks_to_be_removed)
    
    Finally all tasks are removed when calling Scheduler.remove_all.
        scheduler.remove_all()
    
    Use help(Scheduler.(add/remove/remove_all)) to get extended information.
"""

from scheduler import Scheduler
